# Profile layout

The visible profile is in English. The monochrome Medusa is the main visual.
On desktop it sits beside two borderless columns for languages and interests;
on small screens the avatar sits above those columns. Both headings have small
silver Lissajous figures. Company signatures for Shredeo and Prometheus Vision
sit side by side on desktop and stack on mobile, with native website/email links.

The name uses Instrument Serif Regular, preserved as outlined SVG glyphs.
The font source is in `assets/fonts/InstrumentSerif-Regular.ttf`, with its
SIL Open Font License in `docs/licenses/Instrument-Serif-OFL.txt`. Optional font
rebuilding needs `fonttools` and `uharfbuzz`; ordinary SVG generation uses only
the Python standard library and the generated outlines already in the repo.

Each layout has light/dark and explicit reduced-motion versions. The icon sheen
runs every 14 seconds and the mathematical figures loop over 32 seconds. Header
filenames include a content hash, and rebuilding updates the README sources and
removes superseded generated headers automatically.

Static text and icon artwork are cached in an embedded vector image layer in
animated headers. See [performance.md](performance.md) for optimizations,
measurements and limits, and [company-profile.md](company-profile.md) for branding
sources and visual inspiration.

The former activity chart is no longer part of the README. Its workflow is
archived outside `.github/workflows` and does not run. The historical data scripts
and tests remain in the repository, but are not needed to build the profile.

## Rebuilding

```sh
# Optional: rebuild outlined names after changing their text/font.
python3 scripts/build_wordmark.py

# Build the artwork, then the composed headers and README image sources.
python3 scripts/build_exploration_motif.py
python3 scripts/build_gooey.py
python3 scripts/build_profile_sections.py
python3 scripts/build_companies.py
python3 scripts/build_profile_header.py
```

Language icons use the original monochrome paths from
[Simple Icons](https://github.com/simple-icons/simple-icons), pinned to commit
`4d29a35c954699b389a834aacc97dd6e7e74143c`. Their license is preserved in
[licenses/simple-icons-LICENSE.md](licenses/simple-icons-LICENSE.md).
