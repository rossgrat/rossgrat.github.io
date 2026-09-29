# website-v3
Ross' Portfolio website created using Hugo and custom styling. Supports blog posts.

## Local Development
* `hugo server` (or `make local`)

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
