# /// script
# requires-python = "==3.12.14"
# dependencies = ["PyYAML==6.0.3"]
# ///

import json
import subprocess
import sys
import tomllib
from datetime import datetime
from pathlib import Path

import yaml


def git(root, *args):
    return subprocess.check_output(
        ["git", "-c", "core.quotepath=false", *args], cwd=root, text=True
    )


def frontmatter(text):
    text = text.lstrip("\ufeff\n\r")
    if text.startswith("{"):
        data, _ = json.JSONDecoder().raw_decode(text)
    elif text.startswith(("---\n", "+++\n")):
        delimiter, body = text.split("\n", 1)
        header = body.split("\n" + delimiter, 1)[0]
        data = yaml.safe_load(header) if delimiter == "---" else tomllib.loads(header)
    else:
        data = {}
    return {key.lower(): value for key, value in (data or {}).items()}


def first_publication(root, path):
    history = git(root, "log", "--follow", "--format=%x1e%H%x09%cI", "--name-status", "--", path)
    published = None
    for revision in history.split("\x1e")[1:]:
        lines = revision.strip().splitlines()
        commit, timestamp = lines[0].split("\t")
        changes = [line.split("\t") for line in lines[1:] if line]
        if any(change[0] == "D" for change in changes):
            continue
        try:
            metadata = frontmatter(git(root, "show", f"{commit}:{path}"))
        except (ValueError, yaml.YAMLError):
            print(f"Skipping invalid front matter: {commit}:{path}", file=sys.stderr)
            metadata = {"draft": True}
        if not metadata.get("draft", False):
            published = timestamp
        for change in changes:
            if change[0].startswith("R"):
                path = change[1]
        if any(change[0].startswith("C") for change in changes):
            break
    return published


def generate(root):
    if git(root, "rev-parse", "--is-shallow-repository").strip() == "true":
        raise SystemExit("Publication dates require full Git history. Run git fetch --unshallow first.")
    cascade = []
    for post in sorted((root / "content/posts").rglob("*.md")):
        if post.name == "_index.md" or "_templates" in post.parts:
            continue
        metadata = frontmatter(post.read_text())
        if metadata.get("draft", False) or any(
            metadata.get(key) for key in ("publishdate", "pubdate", "published")
        ):
            continue
        published = first_publication(root, post.relative_to(root).as_posix())
        if published is None:
            published = datetime.now().astimezone().isoformat(timespec="seconds")
        source = post.relative_to(root / "content")
        logical = source.parent if source.name == "index.md" else source.with_suffix("")
        paths = [
            "".join("\\" + char if char in "\\*?[]{}," else char for char in str(path).lower())
            for path in (source, logical, str(logical).replace(" ", "-"))
        ]
        cascade.append({
            "publishDate": published,
            "_target": {"path": "{/" + ",/".join(paths) + "}", "kind": "page"},
        })
    return {"cascade": cascade}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    output = root / ".publication-dates.json"
    output.write_text(json.dumps(generate(root), indent=2) + "\n")
