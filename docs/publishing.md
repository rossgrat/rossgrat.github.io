# Publish posts

Open [Pages CMS](https://cms.grattafiori.dev), sign in as `rossgrat`, and select this repository, `main`, and Blog posts.
Create or edit a post, keep Draft enabled while writing, and save.
Turn Draft off and save to publish.

Every save commits to `main` and starts the Pages build.
Draft source is public on GitHub even when the blog build excludes it.
Keep filenames when editing to preserve URLs.

Posts live under `content/posts/`.
Use the CMS image picker or put images in `static/images/posts` with `/images/posts/...` links.
Diagram sources live in `assets/diagrams/posts`.
Edit other pages locally; find previews use `static/images/finds/` and `/images/finds/...` links.

## Publication and edit dates

The [date script](../scripts/publication_dates.py) uses the first Git commit where `draft` is false or absent as the publication date.
Later edits and Git-detected renames retain that date.
This records commit time, not deployment completion.
`publishDate` overrides the automatic value; the original `date` stays unchanged.

An unpublished non-draft preview uses preview start time. Draft previews fall back to `date`.
Restart `make local` after committing a publication change to refresh dates.
The script needs full Git history and writes ignored `.publication-dates.json`.
Direct Hugo commands need that generated file in `--config hugo.toml,.publication-dates.json`.

The last commit touching a post supplies its edit date.
`lastmod` overrides it using the same timestamp format as `date`.
Posts display Last edited only when that date follows publication.

See the [CMS operations guide](https://github.com/rossgrat/potatoserver/blob/main/docs/pages-cms.md) for hosting and backups.
The [analytics implementation](../layouts/partials) omits query strings and fragments and respects Do Not Track and Global Privacy Control.
Tracking failure does not prevent reading the blog.
