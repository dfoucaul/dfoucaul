# Profile layout

The visible profile is in English. The existing Medusa animation remains the
main visual. On desktop it sits on the left, with two borderless columns on the
right showing language symbols and plain-text interests. Interests include
financial modeling and M&A, with no decorative icons.
The language symbols receive one slow silver sheen every 14 seconds. An annual
silver activity curve draws once on load. All animations honor reduced motion.

On small screens the avatar sits above the two compact columns. Activity uses
separate mobile and desktop SVG layouts to keep labels readable, with light and
dark variants.

## Activity data

`scripts/update_activity.py` reads the dated daily cells and tooltips in the public
GitHub contribution calendar. The sum, active days and weekly curve all use the
same latest 365 consecutive dates. Counts include private activity the user
already makes visible through GitHub's aggregate calendar. No private repository
names, contents or access tokens are used. The last weekly bucket may be partial.

The total can differ from GitHub's separately cached headline, whose date range
and cache may differ from the daily cells. Using the dated cells keeps the curve
and both metrics internally consistent. The exact date range is shown under it.

`python3 -m unittest discover -s tests` checks ordering, the rolling year, incomplete
data, partial weeks and zero activity. The scheduled workflow refreshes the
README and the activity SVGs together. Explicit static sources are supplied for
reduced motion, so the fixed chart is complete even in browsers that do not pass
that media preference into SVG image documents.

## Rebuilding

```sh
python3 scripts/build_gooey.py
python3 scripts/build_profile_sections.py
python3 scripts/build_profile_header.py
python3 scripts/update_activity.py
```

Language icons are the original monochrome paths from
[Simple Icons](https://github.com/simple-icons/simple-icons), pinned to commit
`4d29a35c954699b389a834aacc97dd6e7e74143c`. Their license is preserved in
[`licenses/simple-icons-LICENSE.md`](licenses/simple-icons-LICENSE.md).

## Hover interaction

GitHub embeds the README chart as an image. SVG images run in a non-interactive
context, so individual points cannot receive pointer events there. Clicking the
chart opens `assets/activity-interactive.svg` as a standalone SVG document via
the raw GitHub URL. It shows weekly dates and contribution counts on hover or
keyboard focus. The same daily update refreshes this view alongside the README
chart, without a separate website or JavaScript dependency.

Reference: [MDN: scripting SVG and image-context restrictions](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/Scripting).
