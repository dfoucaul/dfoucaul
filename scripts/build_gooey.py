"""Build self-contained SVG portrait animations for GitHub image embedding.

The blur/alpha-threshold technique follows luukdv/gooey-react (MIT); attribution
and the original license are in docs/licenses/gooey-react-MIT.txt.
"""

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render(theme, still=False):
    image = base64.b64encode((ROOT / "assets/medusa-optimized.webp").read_bytes()).decode()
    ink = "#f5f5f7" if theme == "dark" else "#1d1d1f"
    background = "#0d1117" if theme == "dark" else "#ffffff"
    # Per theme this is the surrounding GitHub canvas, not a card surface.
    animations = "" if still else '''
    <style>
      @keyframes drift-a {
        0%,100% { transform:translate(-138px,-12px) }
        25% { transform:translate(-70px,-64px) }
        50% { transform:translate(-22px,-8px) }
        75% { transform:translate(-70px,52px) }
      }
      @keyframes drift-b {
        0%,100% { transform:translate(136px,26px) }
        25% { transform:translate(80px,64px) }
        50% { transform:translate(28px,8px) }
        75% { transform:translate(80px,-56px) }
      }
      @keyframes drift-c {
        0%,100% { transform:translate(-34px,124px) }
        25% { transform:translate(-16px,84px) }
        50% { transform:translate(20px,36px) }
        75% { transform:translate(-8px,82px) }
      }
      .satellite-a { animation:drift-a 12s cubic-bezier(.45,0,.55,1) infinite }
      .satellite-b { animation:drift-b 12s -4s cubic-bezier(.45,0,.55,1) infinite }
      .satellite-c { animation:drift-c 10s -3s cubic-bezier(.45,0,.55,1) infinite }
      @media(prefers-reduced-motion:reduce) {
        .satellite-a,.satellite-b,.satellite-c { animation:none }
      }
    </style>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="640" height="360" viewBox="0 0 640 360" role="img" aria-labelledby="title description">
    <title id="title">Méduse, métal liquide</title>
    <desc id="description">Ma Méduse en halftone noir et blanc, entourée de gouttes argentées qui fusionnent lentement. L’animation respecte la préférence de mouvement réduit.</desc>
    <!-- Gooey technique: luukdv/gooey-react, MIT. See docs/licenses/. -->
    {animations}
    <defs>
      <filter id="goo" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB">
        <feGaussianBlur stdDeviation="8"/>
        <feColorMatrix values="1 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 48 -24"/>
      </filter>
      <filter id="soft-shadow" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation="9"/>
      </filter>
      <linearGradient id="silver" x1="170" y1="60" x2="450" y2="310" gradientUnits="userSpaceOnUse">
        <stop stop-color="#ffffff"/>
        <stop offset=".15" stop-color="#bfc4cb"/>
        <stop offset=".32" stop-color="#f5f5f7"/>
        <stop offset=".53" stop-color="#737b87"/>
        <stop offset=".69" stop-color="#d4dae2"/>
        <stop offset=".87" stop-color="#929ba8"/>
        <stop offset="1" stop-color="#f5f5f7"/>
      </linearGradient>
      <radialGradient id="glint" cx=".32" cy=".16" r=".8">
        <stop stop-color="#ffffff" stop-opacity=".7"/>
        <stop offset=".5" stop-color="#ffffff" stop-opacity="0"/>
        <stop offset="1" stop-color="#000000" stop-opacity=".24"/>
      </radialGradient>
      <mask id="liquid" maskUnits="userSpaceOnUse" x="0" y="0" width="640" height="360" style="mask-type:luminance">
        <g fill="white" filter="url(#goo)">
          <circle cx="320" cy="180" r="95"/>
          <circle class="satellite-a" cx="320" cy="180" r="27" transform="translate(-138 -12)"/>
          <circle class="satellite-b" cx="320" cy="180" r="22" transform="translate(136 26)"/>
          <circle class="satellite-c" cx="320" cy="180" r="15" transform="translate(-34 124)"/>
        </g>
      </mask>
      <clipPath id="portrait"><circle cx="320" cy="180" r="83"/></clipPath>
    </defs>
    <rect width="640" height="360" fill="{background}"/>
    <g opacity=".14" filter="url(#soft-shadow)" transform="translate(0 7)">
      <rect width="640" height="360" fill="{ink}" mask="url(#liquid)"/>
    </g>
    <g mask="url(#liquid)">
      <rect width="640" height="360" fill="url(#silver)"/>
      <rect width="640" height="360" fill="url(#glint)"/>
    </g>
    <circle cx="320" cy="180" r="85" fill="#050505"/>
    <image x="237" y="97" width="166" height="166" clip-path="url(#portrait)" xlink:href="data:image/webp;base64,{image}"/>
    <circle cx="320" cy="180" r="83.5" fill="none" stroke="#ffffff" stroke-opacity=".28" stroke-width=".7"/>
    </svg>
    '''
    return "\n".join(line.rstrip() for line in svg.strip().splitlines()) + "\n"


def main():
    for theme in ("dark", "light"):
        for still in (False, True):
            suffix = "-still" if still else ""
            destination = ROOT / f"assets/gooey-{theme}{suffix}.svg"
            destination.write_text(render(theme, still), encoding="utf-8")
            print(destination.relative_to(ROOT), destination.stat().st_size)


if __name__ == "__main__":
    main()
