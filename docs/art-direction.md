# Art direction

Built with the built-in `image_gen` tool. Source: the public GitHub avatar of
[@dfoucaul](https://github.com/dfoucaul), retrieved on 2026-10-18.

Assets: [`medusa-halftone.png`](../assets/medusa-halftone.png) and
[`hero.png`](../assets/hero.png). The Medusa artwork is the user's existing avatar;
the GitHub avatar itself was not replaced.

## Portrait prompt

Use case: style-transfer. Edit target: attached GitHub avatar, the painted circular Medusa shield by Caravaggio. Asset type: main portrait art for an editorial developer GitHub profile. Transform the SAME artwork into a stunning sharply resolved screenprint / risograph halftone illustration. Preserve the exact recognizable screaming face, facial proportions, turned pose, snakes, circular shield composition, ornamental round border and expression. Palette strictly two colors: very dark charcoal near #101512 and electric acid lime near #c7fa73, with halftone dot density providing intermediate tones. High contrast, bright face, dark snakes with articulate bright highlights, fine visible regular round halftone dots and sophisticated printed grain. Crisp detailed portrait, beautiful poster print character, no blurry dithering, no photograph appearance, no 3D. Centered circular shield fully contained with small margin on a flat dark charcoal background. Square 1024x1024 image, no lettering, no text, no watermark, no decorative additions. Keep the blood marks as stylized monochrome print shapes consistent with the original painting, do not intensify them. This is the user's existing art avatar: change style only, preserve the subject.

## Banner prompt

Use case: compositing / editorial graphic design. Edit target: attached lime-black halftone Medusa artwork. Create a finished ultra-wide GitHub profile banner, aspect ratio 3:1, 1800x600 if supported. Professional Swiss editorial / independent print studio design. Exact dark charcoal background #101512. Strict palette: acid lime #c7fa73, warm ivory #f3f3e6, charcoal. Preserve the attached halftone Medusa, sharp face and ornamental round border, in a large circle occupying the RIGHT THIRD of the banner, entirely inside the canvas, with small margins. The LEFT TWO THIRDS is a very carefully typeset composition, with generous whitespace and very large bold condensed typography, words spelled exactly. Tiny top-left mono eyebrow: 'DFOUCAUL / GITHUB'. Large uppercase heading split over two lines, 'LUZDE' on first line and 'GUADA.' on second line. This is a visual line-break of the single username luzdeguada. Use bold ivory grotesk, beautiful modern sans, compact tracking, heading should fill the left portion. Under headline a short small monospaced line exactly 'CODE / DATA / CURIOSITY'. Tiny acid lime square and fine horizontal divider at bottom left. Sparse technical registration marks and a single tiny + on upper edge. Art direction: high contrast halftone screenprint, intentional asymmetry, crisp clean typography, premium editorial masthead, not gamer art, not a UI, no gradients, no glow, no extra text, no watermark. Keep the circle separate from all text with ample breathing room. The final banner will be displayed about 850px wide; text must remain very legible at that size.

## Statistics

`python3 scripts/update_stats.py` generates the card from public GitHub REST API
data. No third-party image service or extra Python dependency is required. The
workflow refreshes it at 06:23 UTC daily and can also be run manually. GitHub may
disable scheduled workflows in public repositories after 60 days of inactivity;
they can be re-enabled from the Actions tab.

Sources: [GitHub commit search](https://docs.github.com/en/search-github/searching-on-github/searching-commits),
[workflow schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule).
