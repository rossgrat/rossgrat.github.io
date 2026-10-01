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

Production builds use self-hosted GoatCounter at `https://stats.grattafiori.dev`.
Local Hugo previews omit tracking.
The pinned 2.7.0 script lives in `assets/js/vendor/` with its ISC license.
The analytics partial loads it after page load, during browser idle time when available.
The blog does not wait for the analytics server to respond.

Visit `https://ross.grattafiori.dev/#toggle-goatcounter` to exclude your browser from counts.
Wait for the confirmation. Visit that URL again to enable tracking.

The service, database, and deployment instructions live in the
[potatoserver repository](https://github.com/rossgrat/potatoserver/blob/main/docs/goatcounter.md).
See the [GoatCounter integration documentation](https://www.goatcounter.com/help/js) before upgrading the script.

## Writing posts with Obsidian

One-time setup on a new macOS machine:

1. `brew install --cask obsidian`
2. Open Obsidian → "Open folder as vault" → `~/repos/rossgrat.github.io/content`
3. Trust the vault when prompted
4. Settings → Community plugins → Browse → install "Obsidian Git"
5. Settings → Core plugins → enable "Templates" (if not already enabled — the committed `core-plugins.json` turns it on by default)

The committed `content/.obsidian/` ships with Templates pointed at `posts/_templates`, date format set to `YYYY-MM-DDTHH:mm:ssZ`, and the `Cmd-Shift-T` hotkey bound to "Insert template".

Writing workflow:

* **New post**: `Cmd-N` (in the `posts/` folder), type a filename, then `Cmd-Shift-T` → Enter to insert frontmatter. For a post with images, create a folder first (right-click → New folder) and put `index.md` inside — Hugo renders it as a page bundle and pasted images land next to it.
* **Edit `finds.md`**: it sits at the vault root. Use Source mode to edit the `finds` list in the frontmatter. Each entry has a title, URL, added date, and description. Optional `image` and `image_alt` fields add a preview. Store preview files in `static/images/finds/` and use `/images/finds/filename.jpg` as the image path.
* **Publish**: uncheck the `draft` property, then run "Git: Commit-and-sync" from the command palette (`Cmd-P` → type "sync"). Bind it to a hotkey in Settings → Hotkeys if you want one-key publish.

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
