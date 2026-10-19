# Companies and visual direction

The profile keeps the animated Medusa, the Instrument Serif signature, and the
two language/interests columns. The former activity/chart block is replaced by
one shared company composition: Shredeo and Prometheus Vision.

On desktop, the companies sit side by side beneath a shared co-founder label.
Their original flat monochrome marks are integrated into the name lockups.
System sans-serif typography gives the businesses a separate identity from the
personal Instrument Serif signature. Short descriptions and one common contact
area replace the repeated full-width portraits and dividers.

On mobile, the companies form a compact vertical stack. Light and dark variants
are provided. The six outer Prometheus dots emerge together from the stationary
central dot over 950 milliseconds, then rotate as one group at a constant speed
of one revolution per 24 seconds. The opening runs once; only the rotation loops.
The original dot geometry, colors and text remain intact. The logo viewport lets
the full rotating radius remain visible. Shredeo and all company text stay still.
Explicit static variants and a CSS reduced-motion fallback keep the complete logo
visible when motion is disabled. The personal portrait retains its animation
and reduced-motion alternatives. Website and email links remain real links in
the README. Short email labels avoid broken addresses on narrow screens; the
full addresses appear in link titles and the `mailto:` destinations.
No company application or private business data is changed.

## Public company sources

- [Shredeo](https://shredeo.com/): gym operations, coaching, billing, member apps,
  analytics and AI-powered automation.
- [Shredeo logo SVG](https://shredeo.com/shredeo-favicon.svg): the mark matches
  the SVG used by the Shredeo website repository. Its geometry is preserved in
  `assets/brands/shredeo-mono.svg`.
- [Prometheus Vision](https://prometheus-vision.com/en): bespoke software,
  AI systems, business intelligence and data platforms.
- [Prometheus Vision logo SVG](https://prometheus-vision.com/favicon-dark.svg):
  the seven-dot mark is preserved in `assets/brands/prometheus-vision-mono.svg`.

The two contact addresses and the Shredeo co-founder role were provided by the
profile owner. The owner also requested the same company presentation for
Prometheus Vision.

## README inspiration research

- [Awesome GitHub Profile README](https://github.com/abhisheknaiidu/awesome-github-profile-readme)
  was reviewed for approaches to illustrated, animated and minimalist profiles.
- [Anthony Fu](https://github.com/antfu/antfu) uses a small, deliberately arranged
  set of personal links. The takeaway here is clear navigation and restrained
  content rather than more widgets.
- [Sindre Sorhus](https://github.com/sindresorhus/sindresorhus) gives his profile
  a distinctive identity through animation. This profile keeps its own original
  monochrome art direction and assets.

No artwork or code from those profiles is copied into this repository.

## Generative accent

The small silver figure beside “I'm exploring” is an original three-strand
Lissajous drawing. Its 3:2 frequencies relate to the algorithms and mathematics
in the interests column. The phase evolves over a seamless 32-second loop;
there is no glow, orbit or additional content section.

A matching 2:3-frequency figure accompanies “I build with”. It shares the same
silver strokes, three strands, 32-second rhythm and reduced-motion behavior,
with a complementary curve and starting phase to distinguish the two headings.

[Beetran Dahiya's generative README header](https://github.com/beetrandahiya/beetrandahiya)
inspired the idea of using mathematical art as a personal signature. The curve
geometry, animation and implementation here are original. No artwork or code
from that profile is reused. The effect runs as embedded SVG, with explicit
static header variants and a reduced-motion fallback within the motif itself.

The header builder writes content-hashed filenames and updates the README's
eight picture sources automatically. This avoids stale GitHub raw-image caches:
the GitHub `/raw/` redirect drops query-string versions, while a new filename
gives changed artwork a genuinely new URL. Superseded generated headers are
removed by the builder.

To rebuild the accent and composed headers:

```sh
python3 scripts/build_exploration_motif.py
python3 scripts/build_profile_sections.py
python3 scripts/build_profile_header.py
```

## Rebuilding

```sh
# Optional title/font rebuild: requires fonttools and uharfbuzz.
python3 scripts/build_wordmark.py
python3 scripts/build_companies.py
```

The previous activity workflow is retained at `docs/archive/update-activity.yml`.
It is outside `.github/workflows`, so the removed chart is no longer refreshed
or reinserted into the profile.
