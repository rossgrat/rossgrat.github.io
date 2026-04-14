# website-v3
Ross' Portfolio website created using Hugo and custom styling. Supports blog posts.

## Local Development
* `hugo server` (or `make local`)

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
* **Edit `directory.md`**: it sits at the vault root. Edit frontmatter via the Properties panel.
* **Publish**: uncheck the `draft` property, then run "Git: Commit-and-sync" from the command palette (`Cmd-P` → type "sync"). Bind it to a hotkey in Settings → Hotkeys if you want one-key publish.
