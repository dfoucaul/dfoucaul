# Companies and visual direction

The profile keeps the animated Medusa, the Instrument Serif signature, and the
two language/interests columns. The former activity/chart block is replaced by
two original company portraits: Shredeo and Prometheus Vision.

Each company uses its actual logo geometry in monochrome. A restrained silver
ring, fine print texture and slow orbit connect the new marks visually to the
Medusa. The artwork does not redraw or distort the brand symbols. The full
company portraits link to their websites; contact emails remain real, selectable
`mailto:` links in the README.

Desktop, mobile, light, dark and reduced-motion variants are provided. Company
names use the same outlined Instrument Serif font as the personal signature.
No live site, backend, private business data or application code was changed.

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

## Rebuilding

```sh
# Optional title/font rebuild: requires fonttools and uharfbuzz.
python3 scripts/build_wordmark.py
python3 scripts/build_companies.py
```

The previous activity workflow is retained at `docs/archive/update-activity.yml`.
It is outside `.github/workflows`, so the removed chart is no longer refreshed
or reinserted into the profile.
