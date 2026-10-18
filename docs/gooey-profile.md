# Liquid portrait

The README displays an original silver liquid frame around the monochrome
halftone portrait. It uses native SVG filters and CSS animation as an image,
without React or JavaScript running in GitHub Markdown. Typography is GitHub's
native UI font and the header contains no baked-in text.

The blur and alpha-threshold technique is adapted from
[luukdv/gooey-react](https://github.com/luukdv/gooey-react). Its MIT license is
preserved in [docs/licenses/gooey-react-MIT.txt](licenses/gooey-react-MIT.txt).
The animation, paths, layout and silver shading are specific to this profile.

`python3 scripts/build_gooey.py` rebuilds the dark, light and static SVGs. A small
WebP copy of the existing halftone portrait is embedded, so there are no external
image requests inside the SVG. The original portrait is preserved.

The README uses `<picture>` for light/dark and reduced-motion variants. The SVG
also disables its animations when `prefers-reduced-motion` is set.

The contribution count still uses the aggregate displayed on the GitHub profile,
including private activity already included in that visible count. The scheduled
refresh continues to update it daily.
