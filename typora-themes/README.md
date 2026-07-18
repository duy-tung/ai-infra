# Rosé Pine — Typora theme

Three [Rosé Pine](https://rosepinetheme.com) variants for [Typora](https://typora.io),
so the markdown in this repo (the hiring audit, career plans, learning resources)
previews beautifully.

| File | Theme name in Typora | Mode |
|---|---|---|
| `rose-pine.css` | **Rosé Pine** | dark (main) |
| `rose-pine-moon.css` | **Rosé Pine Moon** | dark (softer) |
| `rose-pine-dawn.css` | **Rosé Pine Dawn** | light |

All three share one ruleset; only the 16-colour palette differs.

## Install

1. In Typora: **Preferences → Appearance → Open Theme Folder**
   (or `~/.typora/themes` on Linux, `~/Library/Application Support/abnerworks.Typora/themes` on macOS,
   `%APPDATA%\Typora\themes` on Windows).
2. Copy the three `.css` files into that folder.
3. **Restart Typora.**
4. Pick a variant from the **Themes** menu.

That's it — no fonts to download. The theme uses whatever of JetBrains Mono / Fira Code /
Inter you already have installed, and falls back to clean system fonts otherwise.

## Preview

Open [`preview.md`](preview.md) in Typora after selecting a theme — it exercises every
element (headings, tables, code with syntax highlighting, blockquotes, task lists, math)
so you can see the full palette at a glance.

## Palette reference

| Role | Main | Moon | Dawn |
|---|---|---|---|
| base | `#191724` | `#232136` | `#faf4ed` |
| text | `#e0def4` | `#e0def4` | `#575279` |
| iris (accent / h3) | `#c4a7e7` | `#c4a7e7` | `#907aa9` |
| foam (links / h4) | `#9ccfd8` | `#9ccfd8` | `#56949f` |
| rose (inline code) | `#ebbcba` | `#ea9a97` | `#d7827e` |
| gold (strings) | `#f6c177` | `#f6c177` | `#ea9d34` |
| love (errors / tags) | `#eb6f92` | `#eb6f92` | `#b4637a` |

## Regenerating the variants

`rose-pine-moon.css` and `rose-pine-dawn.css` are generated from `rose-pine.css` by
swapping only the `/* PALETTE:START … PALETTE:END */` block. Edit `rose-pine.css` for
any rule change, then re-run the generator so all three stay in sync (the two variants
should never be hand-edited outside their palette block).
