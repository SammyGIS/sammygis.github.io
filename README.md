# sammygis.github.io

Personal portfolio of **Ajeyomi Adedoyin Samuel** — Geospatial Data Scientist / Developer.
Static site, deployed to GitHub Pages by [.github/workflows/statics.yml](.github/workflows/statics.yml) on every push to `main`.

## Layout

```
index.html            Landing page (hero, skills, experience, education,
                      projects, certifications, talks, gallery, awards)
projects/
  projects.html       Full project catalogue, grouped by category
images/               Every image used by the site (single source of truth)
  profile.jpg         Hero profile photo
LICENSE.txt           CCA 3.0 licence from the original HTML5 UP template
```

Both pages are self-contained: CSS and JS live inline in each HTML file, with
Google Fonts and Font Awesome pulled from CDNs. There is no build step — edit
the HTML and push.

## Theming

Colours are CSS custom properties defined at the top of each page.
`:root` holds the **light** theme (the default), and `[data-theme="dark"]`
overrides it. The mode button in the navbar flips the attribute and remembers
the choice in `localStorage` under the key `theme`.

Adding a colour? Use the existing variables — in particular `--on-accent` for
text sitting on a filled/coloured surface, so buttons stay readable in both modes.
