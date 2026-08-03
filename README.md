# sammygis.github.io

Personal portfolio of **Ajeyomi Adedoyin Samuel** — Geospatial Data Scientist, Data Engineer and
Developer.

Live at **[sammygis.github.io](https://sammygis.github.io)**.

## Deployment

Static site, no build step. [.github/workflows/statics.yml](.github/workflows/statics.yml)
publishes the whole repository to GitHub Pages on every push to `main`. Edit the HTML, commit,
push — that's the pipeline.

## Layout

```
index.html                              Landing page: hero, skills, experience, education,
                                        projects, publications, certifications, talks,
                                        gallery, awards
projects/
  projects.html                         Full project catalogue in four categories —
                                        GIS & Remote Sensing, Development, Data Engineering,
                                        Data Analysis
  sub-projects/
    development/                        In-depth case studies for flagship builds
      envirotrust.html                  Pan-European climate risk platform & API
      demand-signal-explorer.html       IWMI / CGIAR demand intelligence platform
      okomu.html                        Okomu enterprise farm intelligence platform
images/                                 Every image, named after the project it belongs to
favicon.svg                             Initials mark
CLAUDE.md                               Conventions for anyone (human or agent) editing the site
```

## How it's built

Plain HTML with CSS and JavaScript inlined in each page. The only external dependencies are
Google Fonts (Space Grotesk) and Font Awesome 6.0.0, both from CDNs. No framework, no bundler,
no `node_modules`.

Each page is self-contained, which means the theme variables are **duplicated** at the top of
every file — change a design token in one place and you must change it everywhere.

## Theming

Colours are CSS custom properties. `:root` holds the **light** theme, which is the default and
applies before JavaScript runs; `[data-theme="dark"]` overrides it. The mode button in the navbar
flips the attribute and remembers the choice in `localStorage` under `theme`.

The palette is teal/green. When adding anything with a coloured background, use `--on-accent`
for its text — it stays white in both themes, so buttons never end up with dark text on a dark
fill.

## Editing

See **[CLAUDE.md](CLAUDE.md)** for the full conventions: how to add a project card or a case
study page, image naming, the layout rules that are easy to break, and the checks to run before
committing.
