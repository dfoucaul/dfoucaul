"""Outline the chosen Instrument Serif name for portable SVG image rendering.

Only this optional rebuild step requires fonttools and uharfbuzz. The profile
renderer consumes the generated SVG and has no additional runtime dependency.
"""

from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
import uharfbuzz as hb

ROOT = Path(__file__).resolve().parents[1]


def build(text, destination, size=26):
    source = ROOT / "assets/fonts/InstrumentSerif-Regular.ttf"
    font = TTFont(source)
    units = font["head"].unitsPerEm
    face = hb.Face(source.read_bytes())
    shaping_font = hb.Font(face)
    shaping_font.scale = (units, units)
    hb.ot_font_set_funcs(shaping_font)
    buffer = hb.Buffer()
    buffer.add_str(text)
    buffer.guess_segment_properties()
    hb.shape(shaping_font, buffer, {"kern": True})
    glyphs = font.getGlyphSet()
    order = font.getGlyphOrder()
    pen = SVGPathPen(glyphs)
    cursor = 0
    for glyph, position in zip(buffer.glyph_infos, buffer.glyph_positions):
        transform = (1, 0, 0, 1, cursor + position.x_offset, position.y_offset)
        glyphs[order[glyph.codepoint]].draw(TransformPen(pen, transform))
        cursor += position.x_advance
    ascent, descent = font["hhea"].ascent, font["hhea"].descent
    width = cursor * size / units
    height = (ascent - descent) * size / units
    baseline = ascent * size / units
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.4f}" height="{height:.4f}" viewBox="0 {-ascent} {cursor} {ascent-descent}" data-baseline="{baseline:.4f}" role="img" aria-labelledby="title">
  <title id="title">{text} — Instrument Serif Regular</title>
  <path d="{pen.getCommands()}" transform="scale(1 -1)" fill="currentColor"/>
</svg>
'''
    destination.write_text(svg, encoding="utf-8")
    print(f"{destination.name}: {width:.2f} × {height:.2f}px")


def main():
    build("Luz de Guada", ROOT / "assets/name-instrument-serif.svg")
    build("Shredeo", ROOT / "assets/brands/shredeo-title.svg", 36)
    build("Prometheus Vision", ROOT / "assets/brands/prometheus-vision-title.svg", 36)


if __name__ == "__main__":
    main()
