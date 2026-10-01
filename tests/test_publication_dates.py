import csv
import io
from contextlib import redirect_stderr
import json
import os
import shutil
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

from scripts.publication_dates import first_publication, generate


PROJECT = Path(__file__).resolve().parents[1]


class PublicationDatesTest(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Publication test")
        self.git("config", "user.email", "test@example.invalid")
        self.post = self.root / "content/posts/example.md"
        self.post.parent.mkdir(parents=True)

    def git(self, *args, timestamp=None):
        env = os.environ.copy()
        if timestamp:
            env.update(GIT_AUTHOR_DATE=timestamp, GIT_COMMITTER_DATE=timestamp)
        return subprocess.check_output(["git", *args], cwd=self.root, env=env, text=True)

    def commit(self, timestamp):
        self.git("add", "content")
        self.git("commit", "-qm", "Test post", timestamp=timestamp)

    def write_post(self, draft=None, extra="", body="Post body."):
        draft_field = "" if draft is None else f"draft: {str(draft).lower()}\n"
        self.post.write_text(
            f"---\ntitle: Example\ndate: 2023-01-01T12:00:00-06:00\n"
            f"{draft_field}{extra}---\n{body}\n"
        )

    def test_publication_survives_edits_renames_and_redrafting(self):
        self.post.write_text('{"date":"2023-01-01", "draft":true}\nDraft.')
        self.commit("2023-01-01T12:00:00-06:00")
        self.write_post(False)
        self.commit("2024-02-03T12:00:00-06:00")
        self.write_post(False, body="Revised post.")
        self.commit("2024-03-01T12:00:00-06:00")
        renamed = self.post.with_name("renamed.md")
        self.git("mv", str(self.post), str(renamed))
        self.post = renamed
        self.commit("2024-04-01T12:00:00-05:00")
        self.write_post(True)
        self.commit("2024-05-01T12:00:00-05:00")
        self.write_post(False)
        self.commit("2024-06-01T12:00:00-05:00")
        self.assertEqual(
            first_publication(self.root, "content/posts/renamed.md"),
            "2024-02-03T12:00:00-06:00",
        )

    def test_missing_draft_publishes_and_overrides_win(self):
        self.write_post()
        self.commit("2024-02-03T12:00:00-06:00")
        self.assertEqual(generate(self.root)["cascade"][0]["publishDate"], "2024-02-03T12:00:00-06:00")
        self.write_post(extra="publishDate: 2024-02-10T12:00:00-06:00\n")
        self.assertEqual(generate(self.root), {"cascade": []})

    def test_invalid_historical_metadata_is_not_a_publication(self):
        self.post.write_text('{"draft": false, "tags": ["one" "two"]}\nBroken.')
        self.commit("2023-01-01T12:00:00-06:00")
        self.write_post(False)
        self.commit("2024-02-03T12:00:00-06:00")
        with redirect_stderr(io.StringIO()) as warnings:
            self.assertEqual(generate(self.root)["cascade"][0]["publishDate"], "2024-02-03T12:00:00-06:00")
        self.assertIn("Skipping invalid front matter", warnings.getvalue())

    def test_drafts_and_templates_stay_out(self):
        self.write_post(True)
        self.commit("2024-02-03T12:00:00-06:00")
        templates = self.post.parent / "_templates"
        templates.mkdir()
        (templates / "post.md").write_text("---\ndate: {{date}}\n---\n")
        self.assertEqual(generate(self.root), {"cascade": []})

    def test_uncommitted_publication_uses_preview_time_without_changing_post(self):
        self.write_post(True)
        self.commit("2024-02-03T12:00:00-06:00")
        self.write_post(False)
        original = self.post.read_bytes()
        published = datetime.fromisoformat(generate(self.root)["cascade"][0]["publishDate"])
        self.assertLess(abs((datetime.now().astimezone() - published).total_seconds()), 5)
        self.assertEqual(self.post.read_bytes(), original)

    def test_shallow_history_fails(self):
        self.write_post(False)
        self.commit("2024-02-03T12:00:00-06:00")
        with tempfile.TemporaryDirectory() as clone:
            subprocess.run(["git", "clone", "-q", "--depth=1", self.root.as_uri(), clone], check=True)
            with self.assertRaisesRegex(SystemExit, "full Git history"):
                generate(Path(clone))

    def test_hugo_pages_lists_archive_and_rss(self):
        for directory in ("layouts", "assets", "static"):
            shutil.copytree(PROJECT / directory, self.root / directory)
        shutil.copy(PROJECT / "hugo.toml", self.root / "hugo.toml")
        (self.root / "content/archive.md").write_text("---\ntitle: Archive\nlayout: archive\n---\n")
        self.write_post(True, extra="tags: [test]\n")
        self.commit("2023-01-01T12:00:00-06:00")
        self.write_post(False, extra="tags: [test]\n")
        self.commit("2024-02-03T12:00:00-06:00")
        self.write_post(False, extra="tags: [test]\n", body="Later edit.")
        self.commit("2024-03-04T12:00:00-06:00")
        self.post = self.root / "content/posts/A Finished, Named Post/index.md"
        self.post.parent.mkdir()
        self.write_post(False, body="A bundle.")
        self.commit("2025-04-05T12:00:00-05:00")
        self.post = self.root / "content/posts/hidden.md"
        self.write_post(True)
        self.commit("2025-04-06T12:00:00-05:00")
        self.post = self.root / "content/posts/scheduled.md"
        self.write_post(False, extra="publishDate: 2099-01-01T12:00:00-06:00\n")
        self.commit("2025-04-07T12:00:00-05:00")
        config = self.root / ".publication-dates.json"
        config.write_text(json.dumps(generate(self.root)))
        hugo = os.environ.get("HUGO_BIN", "hugo")
        args = ["--config", "hugo.toml,.publication-dates.json"]
        subprocess.run([hugo, *args], cwd=self.root, check=True, capture_output=True)
        listing = subprocess.check_output([hugo, "list", "all", *args], cwd=self.root, text=True)
        rows = {row["path"]: row for row in csv.DictReader(io.StringIO(listing))}
        for path, timestamp in (
            ("content/posts/example.md", "2024-02-03T12:00:00-06:00"),
            ("content/posts/A Finished, Named Post/index.md", "2025-04-05T12:00:00-05:00"),
        ):
            self.assertEqual(rows[path]["publishDate"], timestamp)
            self.assertEqual(rows[path]["date"], timestamp)
        public = self.root / "public"
        article = (public / "posts/example/index.html").read_text()
        self.assertIn('datetime="2024-02-03T12:00:00-06:00"', article)
        self.assertIn('Last edited <time datetime="2024-03-04T12:00:00-06:00"', article)
        self.assertIn("03 Feb 2024", (public / "index.html").read_text())
        archive = (public / "archive/index.html").read_text()
        self.assertIn('id="year-2024"', archive)
        self.assertNotIn('id="year-2023"', archive)
        self.assertFalse((public / "posts/hidden/index.html").exists())
        self.assertFalse((public / "posts/scheduled/index.html").exists())
        items = ET.parse(public / "index.xml").findall("channel/item")
        self.assertEqual(items[0].findtext("pubDate"), "Sat, 05 Apr 2025 12:00:00 -0500")
        self.assertEqual(items[1].findtext("pubDate"), "Sat, 03 Feb 2024 12:00:00 -0600")


if __name__ == "__main__":
    unittest.main()
