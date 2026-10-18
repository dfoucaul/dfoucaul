"""Build two quiet, borderless SVG columns with monochrome brand symbols."""

from html import escape
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]


def brand_paths(slug):
    root = ElementTree.parse(ROOT / f"assets/icons/{slug}.svg").getroot()
    return "".join(f'<path d="{escape(node.attrib["d"], quote=True)}"/>'
                   for node in root.iter() if node.tag.endswith("}path"))


def render(kind, theme, still=False):
    dark = theme == "dark"
    foreground = "#e6edf3" if dark else "#1f2328"
    secondary = "#b1bac4" if dark else "#59636e"
    border = "#30363d" if dark else "#d1d9e0"
    background = "#0d1117" if dark else "#ffffff"
    heading = "I build with" if kind == "stack" else "I'm exploring"
    labels = (["Rust", "Go", "TypeScript", "Python"] if kind == "stack" else
              ["Machine learning", "AI & models", "Algorithms", "Data visualization"])
    icons, rows = [], []
    diagrams = [
        '<path d="M5 6l7 6 7-6M5 18l7-6 7 6"/><circle cx="5" cy="6" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/>',
        '<path d="M12 3l2.2 6.8L21 12l-6.8 2.2L12 21l-2.2-6.8L3 12l6.8-2.2Z"/>',
        '<path d="M6 4v10a4 4 0 004 4h8M6 10h7a4 4 0 004-4V4"/><circle cx="6" cy="3" r="2"/><circle cx="17" cy="3" r="2"/><circle cx="19" cy="18" r="2"/>',
        '<path d="M4 3v17h17M8 15l4-5 4 2 5-7"/>',
    ]
    for index, label in enumerate(labels):
        y = 77 + index * 44
        if kind == "stack":
            icons.append(f'<g transform="translate(26 {y-19})">{brand_paths(label.lower())}</g>')
        else:
            icons.append(f'<g transform="translate(26 {y-19})" fill="none" stroke="{secondary}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{diagrams[index]}</g>')
        rows.append(f'<text x="69" y="{y}" font-size="17" fill="{foreground}">{escape(label)}</text>')
    icon_markup = "".join(icons)
    shimmer = ""
    if kind == "stack" and not still:
        shimmer = f'''<defs>
          <mask id="symbols" maskUnits="userSpaceOnUse" x="0" y="0" width="330" height="235"><g fill="white">{icon_markup}</g></mask>
          <linearGradient id="sheen"><stop stop-color="white" stop-opacity="0"/><stop offset=".5" stop-color="white"/><stop offset="1" stop-color="white" stop-opacity="0"/></linearGradient>
        </defs>
        <style>
          @keyframes sheen {{ 0%,25% {{ transform:translateX(-90px);opacity:0 }} 30% {{ opacity:.85 }} 55% {{ opacity:.85 }} 65%,100% {{ transform:translateX(345px);opacity:0 }} }}
          .sheen {{ animation:sheen 14s ease-in-out infinite }}
          @media(prefers-reduced-motion:reduce) {{ .sheen {{ display:none;animation:none }} }}
        </style>
        <g mask="url(#symbols)"><rect class="sheen" x="0" y="48" width="80" height="178" fill="url(#sheen)" opacity="0"/></g>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="330" height="235" viewBox="0 0 330 235" role="img" aria-labelledby="title desc">
      <title id="title">{escape(heading)}</title>
      <desc id="desc">{escape(', '.join(labels))}. Monochrome symbols and a restrained silver highlight.</desc>
      <rect width="330" height="235" fill="{background}"/>
      <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif">
        <text x="26" y="25" fill="{foreground}" font-size="18" font-weight="500">{escape(heading)}</text>
        <path d="M26 43H304" stroke="{border}" stroke-width=".65"/>
        <g fill="{secondary}">{icon_markup}</g>
        {''.join(rows)}
        {shimmer}
      </g>
    </svg>'''
    return "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"


def main():
    for theme in ("dark", "light"):
        for kind in ("stack", "exploring"):
            (ROOT / f"assets/{kind}-{theme}.svg").write_text(render(kind, theme), encoding="utf-8")
            if kind == "stack":
                (ROOT / f"assets/{kind}-{theme}-still.svg").write_text(render(kind, theme, True), encoding="utf-8")


if __name__ == "__main__":
    main()
