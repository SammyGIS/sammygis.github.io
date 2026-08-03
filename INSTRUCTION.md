# Working on this site

Personal portfolio for **Ajeyomi Adedoyin Samuel** (Geospatial / Data Engineer).
Static HTML, no build step, deployed to GitHub Pages from `main` by
[.github/workflows/statics.yml](.github/workflows/statics.yml). Edit the HTML and push — that
is the whole pipeline.

## Layout

```
index.html                          Landing page — every section lives here
projects/projects.html              Full project catalogue, 4 categories
projects/sub-projects/<category>/   Deep-dive case studies, grouped by the catalogue
                                    category they belong to (e.g. development/)
images/                             Every image, single source of truth
images/covers/                      Generated SVG cover art for projects with no screenshot
tools-generate-covers.py            Regenerates that cover art
cv/                                 Hosted CV PDF (linked from the hero and share menu)
favicon.svg                         Initials mark, linked from all pages
```

There is no shared stylesheet. **Each page carries its own inline `<style>` block**, and the
theme variables are duplicated at the top of every one. When you change a design token, change
it in *all* pages or they drift apart.

## Rules that are easy to get wrong

### Theming
- `:root` is the **light** theme; `[data-theme="dark"]` overrides it. Light must be the default
  so the page renders correctly before JS runs. Never invert this.
- The theme is stored in `localStorage` under `theme`, and the toggle button label names the
  mode you will switch *to* ("Dark mode" while in light).
- **Use `--on-accent` for text on any filled/coloured surface.** A previous bug shipped
  blue buttons with near-black text because the text colour variable flipped between themes.
  `--on-accent` is white in both themes for exactly this reason.
- Filled buttons are `font-weight: 700`.
- **No shadows or glows anywhere.** No `box-shadow`, no `text-shadow`, no glow effects. This is
  a deliberate style decision, not an oversight.

### Palette
Teal/green. Light: `--primary-color: #0f766e`, `--accent-color: #0d9488`.
Dark: `--primary-color: #14b8a6`, `--accent-color: #2dd4bf`.

### Font Awesome
Pages load **Font Awesome 6.0.0**. Icons added in 6.1+ (e.g. `fa-people-group`) render as blank
boxes. Verify an icon exists in 6.0 before using it, or bump the CDN version on every page.

### Navigation
- The home nav holds ~10 links plus the "All Projects" call-out and collapses into the menu
  button at **1000px**, because the row cannot fit below that. Adding another link risks
  wrapping — check it before you do.
- The header bar is capped at `1280px` and content must use the **same** width so they align.
- Sections need `scroll-margin-top` to clear the fixed header. "Home" is handled in JS
  (`scrollTo(0)`), not by the `#home` anchor.

### Layout
- Project cards are flex columns with `margin-top: auto` on the link, so **"View Project" sits at
  the same height on every card**. Keep that if you touch card markup.
- Case study body text runs full width (`max-width: 100%`) to match the screenshot above it,
  justified, with `hyphens: none` — words must never be split across lines.
- The global `* { padding: 0 }` reset kills list indentation. Any new `<ul>` needs explicit
  `padding-left` or the bullets hang outside their container.

## Adding things

### A new project
1. Save the screenshot to `images/` named after the project, kebab-case
   (`nigeria-forest-watch.png`, not `img_04.png`).
2. Add an `<article class="project-card">` to the right section of
   `projects/projects.html`: `gis`, `backend` (titled "Development"), `engineering`, `analysis`.
3. If there is no screenshot, generate cover art instead of shipping a bare icon: add an entry to
   `PROJECTS` in `tools-generate-covers.py`, run it, and point the card at
   `../images/covers/<slug>.svg`. Motifs available: `contours`, `raster`, `basin`, `hexbin`,
   `flow`, `points` — pick one that matches what the project actually does. Artwork is
   deterministic, so the same title always regenerates identically.
   Never leave a broken image or a dead `#` link.
4. Optionally mirror it into the Projects grid on `index.html` (that grid shows highlights only).

### A case study page
For flagship work worth explaining, add `projects/sub-projects/<category>/<name>.html` — the
category folder mirrors the catalogue section the card sits in — and point the card's
"View Project" at it instead of at the live product. Copy an existing one — they are deliberately
identical apart from `<title>` and content. Structure: breadcrumb → `case-hero` (h1, `case-role`,
`case-stack` pills) → optional `case-shot` image → `case-body` (lede + `<h2>` sections) →
`case-links`.

Paths from that depth: `../../../images/`, `../../projects.html`, `../../../index.html`,
`../../../favicon.svg`. Re-run the link check below after any folder move — these break silently.

**These pages lead with engineering decisions, not feature lists** — why a format, database, or
framework was chosen. That is the point of them.

### Sharing and the CV
`index.html` carries Open Graph and Twitter card tags so the profile photo and description
appear when the URL is pasted into WhatsApp, LinkedIn, Teams or X. **These need absolute URLs**
(`https://sammygis.github.io/...`) — relative paths do not work for social previews. Update
`og:image` if the profile photo is ever renamed.

The Share button in the nav uses the native OS share sheet on phones and a dropdown elsewhere
(WhatsApp, email, Teams, LinkedIn, X, copy link, download CV).

There are two CVs and they serve different purposes:
- `cv/Adedoyin-Samuel-Ajeyomi-CV.pdf` — Samuel's own PDF, opened by the hero "View CV" button.
  Replace the file when he sends a new version; keep the filename so links survive.
- `cv.html` — a print-optimised CV **generated from the portfolio content**, reached from the
  share menu's "Download CV". Its toolbar button calls `window.print()`, and the browser's
  "Save as PDF" produces an A4 PDF. **When experience, skills or publications change on
  `index.html`, update `cv.html` to match** — they are not linked automatically.

### Experience or publications
Both live in `index.html`. Experience uses `.timeline-item`; publications use `.pub-item` and are
**sorted by citation count descending**, ties broken by newest year. Bold Samuel's name in the
author list with `<strong>`.

## Accuracy

Never invent project details, dates, employers, metrics, or technical rationale. If something is
unknown, ask — or ship the rest and say plainly what is missing. Prefer publisher DOIs over
Google Scholar links for publications. Verify author lists against the actual record.

## Before committing

```bash
python -m http.server 8899          # then curl each page for a 200
node --check <extracted script>     # syntax-check the inline <script> block
```

**Always syntax-check the inline JavaScript.** Each page has a single `<script>` block, so one
malformed line disables the theme toggle, the mobile menu, the carousel, scroll-spy and the share
menu all at once — with no visible error unless you open the console. This has happened before.
Check: markup tags balanced, CSS braces balanced, and **every local `src`/`href` resolves** —
the folder has been reorganised more than once and relative paths break silently.
