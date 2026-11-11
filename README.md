# website-v3
Ross' Portfolio website created using Hugo and custom styling. Supports blog posts.

## Local Development
Run `make local` to preview posts, including drafts.
Run `make build` to build the public site without drafts.
These commands require Hugo 0.122.0 and uv 0.12.19.
To select a specific Hugo executable, pass `HUGO=/path/to/hugo` to `make`.
uv supplies Python 3.12.14 and PyYAML 6.0.3 for the publication date script.
Run `make test` to test publication dates.

## Analytics

Production builds use self-hosted Umami at `https://stats.grattafiori.dev`.
Local Hugo previews omit tracking.
The loader sends one page view after page load, during browser idle time when available.
It omits URL queries and fragments and respects Do Not Track and Global Privacy Control.
The blog remains usable when the analytics server or script is unavailable.

To exclude your browser, open `https://ross.grattafiori.dev/#toggle-analytics`.
Make sure that the message says tracking is disabled.
Repeat this on each browser and device that you use.
Opening the URL again enables tracking in that browser.
Existing GoatCounter browser exclusions transfer to Umami on the next visit.

The [infrastructure guide](https://github.com/rossgrat/potatoserver/blob/main/docs/umami.md) covers deployment, data collection, and backups.
See the [Umami tracker documentation](https://docs.umami.is/docs/tracker-configuration) before changing the loader.

## Writing posts with Pages CMS

Open [Pages CMS](https://cms.grattafiori.dev) on your phone or laptop.
Sign in with your `rossgrat` GitHub account.
Select `rossgrat/rossgrat.github.io`, `main`, and Blog posts.

1. Create a post.
2. Enter its title.
3. Keep Draft enabled while you write.
4. Write in the visual editor or use the Markdown switch.
5. Use the image picker to upload or select images.
6. Save the post.
7. When the post is ready, turn Draft off.
8. Save again to publish.

Each save commits to `main` and starts the GitHub Pages build.
Drafts remain visible in this public GitHub repository, but the build excludes them from the blog.

Posts use standard Markdown in `content/posts/<slug>.md`.
Keep the filename when editing a post to preserve its URL.
Images live under `static/images/posts` and use `/images/posts/...` links.
Diagram source files live under `assets/diagrams/posts`.
The [infrastructure guide](https://github.com/rossgrat/potatoserver/blob/main/docs/pages-cms.md) covers deployment and backups.

Other content, such as `content/finds.md`, remains editable locally.
Find previews use `static/images/finds/` and `/images/finds/filename.jpg` links.

The build derives each publication date from the first Git commit where `draft` is false or absent.
The date stays fixed through later edits and Git-detected renames.
This is the commit date, not the time when deployment finishes.
Article pages, post lists, archive groups, and RSS use this date.
An optional `publishDate` property overrides the automatic date.
The original `date` property stays unchanged in your Markdown files.

Before the first public commit, a post with `draft: false` uses the preview start time.
Draft previews retain the original `date` as a fallback.
After you commit a publication change, restart `make local` to refresh the dates.
The script requires full Git history and writes an ignored `.publication-dates.json` file.
Direct `hugo` commands omit automatic dates unless you pass `--config hugo.toml,.publication-dates.json` after generation.
See [Hugo's cascade documentation](https://gohugo.io/configuration/cascade/) for how the generated values reach each post.

The last commit that changes the post supplies its edit date.
Posts show "Last edited" when the edit date is later than the publication date.
An optional `lastmod` property overrides the automatic edit date.
Use the same timestamp format as `date`.
See [Hugo's date configuration](https://gohugo.io/configuration/front-matter/#dates) for the date sources.
