"""Render an exact 365-day activity summary from the public GitHub calendar.

Daily totals include private activity the owner already shares on their profile.
No repository data or personal access token is requested. The curve and both
metrics use the same dated cells, rather than GitHub's separately cached heading.
"""

from collections import defaultdict
from datetime import date, timedelta
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
URL = "https://github.com/users/dfoucaul/contributions"


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = {}
        self.tooltips = {}
        self.target = None
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "td" and attrs.get("data-date"):
            if attrs["id"] in self.cells:
                raise ValueError("Duplicate calendar cell")
            self.cells[attrs["id"]] = date.fromisoformat(attrs["data-date"])
        if tag == "tool-tip" and attrs.get("for"):
            self.target = attrs["for"]
            self.parts = []

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.target:
            self.tooltips[self.target] = " ".join("".join(self.parts).split())
            self.target = None

    def handle_data(self, text):
        if self.target:
            self.parts.append(text)


def parse_calendar(html):
    parser = CalendarParser()
    parser.feed(html)
    days = {}
    for identity, day in parser.cells.items():
        text = parser.tooltips.get(identity, "")
        match = re.match(r"([\d,]+) contributions? on ", text)
        if match:
            count = int(match.group(1).replace(",", ""))
        elif text.startswith("No contributions on "):
            count = 0
        else:
            raise ValueError(f"Missing or unrecognized contribution count for {day}")
        if day in days:
            raise ValueError("Duplicate calendar date")
        days[day] = count
    ordered = sorted(days.items())
    if len(ordered) < 365:
        raise ValueError("Incomplete contribution calendar; preserving existing assets")
    # GitHub may include a leading partial week. Use exactly the last 365 dates.
    ordered = ordered[-365:]
    if ordered[-1][0] - ordered[0][0] != timedelta(days=364):
        raise ValueError("The contribution calendar has missing dates")
    return ordered


def weekly_counts(days):
    weeks = defaultdict(int)
    for day, count in days:
        weeks[(day - days[0][0]).days // 7] += count
    return list(weeks.values())


def curve_points(counts, left, top, width, height):
    peak = max(max(counts), 1)
    return [(left + index * width / max(len(counts) - 1, 1),
             top + height - count / peak * height)
            for index, count in enumerate(counts)]


def smooth_path(points):
    commands = [f"M{points[0][0]:.2f},{points[0][1]:.2f}"]
    for index in range(1, len(points) - 1):
        x, y = points[index]
        nx, ny = points[index + 1]
        commands.append(f"Q{x:.2f},{y:.2f} {(x+nx)/2:.2f},{(y+ny)/2:.2f}")
    x, y = points[-1]
    commands.append(f"L{x:.2f},{y:.2f}")
    return " ".join(commands)


def render_activity(days, theme, mobile=False, still=False):
    total = sum(count for _, count in days)
    active = sum(count > 0 for _, count in days)
    dark = theme == "dark"
    foreground = "#e6edf3" if dark else "#1f2328"
    secondary = "#a7adb6" if dark else "#59636e"
    border = "#30363d" if dark else "#d1d9e0"
    background = "#0d1117" if dark else "#ffffff"
    width, height = (360, 280) if mobile else (720, 235)
    left = 24 if mobile else 28
    right = width - left
    second = 204 if mobile else 260
    top, chart_height = (121, 86) if mobile else (104, 75)
    points = curve_points(weekly_counts(days), left, top, right-left, chart_height)
    path = smooth_path(points)
    baseline = top + chart_height
    area = f"{path} L{right},{baseline} L{left},{baseline} Z"
    first, last = days[0][0], days[-1][0]
    period = f"{first.strftime('%b')} {first.day}, {first.year} — {last.strftime('%b')} {last.day}, {last.year}"
    ex, ey = points[-1]
    footer = (f'<text x="{left}" y="247">Private activity included</text><text x="{left}" y="268">{period}</text>' if mobile else
              f'<text x="{left}" y="218">Private activity included</text><text x="{right}" y="218" text-anchor="end">{period}</text>')
    weekly_label = (f'<text x="{left}" y="103" fill="{secondary}" font-size="11">Weekly activity · last week partial</text>' if mobile else
                    f'<text x="{right}" y="69" text-anchor="end" fill="{secondary}" font-size="12">Weekly activity · last week partial</text>')
    motion = "" if still else '''<style>
        @keyframes draw { from { stroke-dashoffset:1 } to { stroke-dashoffset:0 } }
        .curve { stroke-dasharray:1;animation:draw 2.2s cubic-bezier(.22,1,.36,1) both }
        @media(prefers-reduced-motion:reduce) { .curve { animation:none;stroke-dashoffset:0 } }
      </style>'''
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
      <title id="title">{total:,} contributions · {active} active days</title>
      <desc id="desc">{escape(period)}. Private activity included. The silver curve shows weekly contribution totals; the last week can be partial.</desc>
      <defs>
        <linearGradient id="silver" x1="0" x2="1"><stop stop-color="{secondary}"/><stop offset=".55" stop-color="{foreground}"/><stop offset="1" stop-color="{secondary}"/></linearGradient>
        <linearGradient id="wash" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{foreground}" stop-opacity=".07"/><stop offset="1" stop-color="{foreground}" stop-opacity="0"/></linearGradient>
      </defs>
      {motion}
      <rect width="{width}" height="{height}" fill="{background}"/>
      <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif">
        <g fill="{foreground}" font-size="34" font-weight="400" letter-spacing="-1">
          <text x="{left}" y="45">{total:,}</text><text x="{second}" y="45">{active}</text>
        </g>
        <g fill="{secondary}" font-size="13"><text x="{left}" y="69">contributions</text><text x="{second}" y="69">active days</text></g>
        {weekly_label}
        <path d="M{left} {baseline}H{right}" stroke="{border}" stroke-width=".6"/>
        <path d="{area}" fill="url(#wash)"/>
        <path class="curve" d="{path}" pathLength="1" fill="none" stroke="url(#silver)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="{ex:.2f}" cy="{ey:.2f}" r="2.1" fill="{foreground}"/>
        <g fill="{secondary}" font-size="12">{footer}</g>
      </g>
    </svg>'''
    return "\n".join(line.rstrip() for line in svg.splitlines()) + "\n"


def activity_block(days):
    total = sum(count for _, count in days)
    active = sum(count > 0 for _, count in days)
    return f'''<!-- ACTIVITY:START -->
<p align="center">
  <a href="https://raw.githubusercontent.com/dfoucaul/dfoucaul/main/assets/activity-interactive.svg" title="Open the interactive chart">
  <picture>
    <source media="(max-width: 600px) and (prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="assets/activity-mobile-dark-still.svg" />
    <source media="(max-width: 600px) and (prefers-reduced-motion: reduce)" srcset="assets/activity-mobile-light-still.svg" />
    <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)" srcset="assets/activity-dark-still.svg" />
    <source media="(prefers-reduced-motion: reduce)" srcset="assets/activity-light-still.svg" />
    <source media="(max-width: 600px) and (prefers-color-scheme: dark)" srcset="assets/activity-mobile-dark.svg" />
    <source media="(max-width: 600px)" srcset="assets/activity-mobile-light.svg" />
    <source media="(prefers-color-scheme: dark)" srcset="assets/activity-dark.svg" />
    <img src="assets/activity-light.svg" width="720" alt="{total:,} contributions across {active} active days in the past 365 days. Private activity included. Weekly activity shown as a silver curve." />
  </picture>
  </a>
</p>
<!-- ACTIVITY:END -->'''


def render_interactive(days):
    """A standalone SVG document supports pointer/focus interaction, unlike img."""
    svg = render_activity(days, "dark", still=True)
    svg = svg.replace('width="720" height="235" viewBox="0 0 720 235"',
                      'width="100%" height="100%" viewBox="0 0 720 270"')
    counts = weekly_counts(days)
    points = curve_points(counts, 28, 104, 664, 75)
    step = 664 / (len(points) - 1)
    buckets = []
    for index, ((x, _), count) in enumerate(zip(points, counts)):
        start = days[0][0] + timedelta(days=index * 7)
        end = min(start + timedelta(days=6), days[-1][0])
        label = f"{start} — {end}: {count:,} contributions"
        tx = max(28, min(x - 94, 504))
        hit_left = max(28, x - step / 2)
        hit_right = min(692, x + step / 2)
        buckets.append(f'''<g class="week" tabindex="0" role="group" aria-label="{escape(label)}">
          <title>{escape(label)}</title>
          <rect class="target" x="{hit_left:.2f}" y="94" width="{hit_right-hit_left:.2f}" height="96" fill="transparent" pointer-events="all"/>
          <g class="detail" pointer-events="none">
            <path d="M{x:.2f} 95V185" stroke="#b1bac4" stroke-width=".8" stroke-opacity=".6"/>
            <g transform="translate({tx:.2f} 82)">
              <rect width="188" height="59" rx="10" fill="#161b22" stroke="#3d444d" stroke-width=".7"/>
              <text x="12" y="24" fill="#e6edf3" font-size="16">{count:,} contributions</text>
              <text x="12" y="44" fill="#b1bac4" font-size="11">{start} — {end}</text>
            </g>
          </g>
        </g>''')
    interaction = f'''<style>
      svg {{ background:#0d1117 }}
      .week {{ outline:none }}
      .target {{ cursor:crosshair }}
      .detail {{ visibility:hidden;opacity:0 }}
      .week:hover .detail,.week:focus .detail {{ visibility:visible;opacity:1 }}
    </style>
    <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif">
      {''.join(buckets)}
      <text x="360" y="257" text-anchor="middle" fill="#a7adb6" font-size="11">Hover over the curve or use Tab to explore each week.</text>
    </g>'''
    return svg.replace('</svg>', interaction + '\n</svg>')


def main():
    request = Request(URL, headers={
        "User-Agent": "github-profile-calendar-summary",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urlopen(request, timeout=30) as response:
        days = parse_calendar(response.read().decode("utf-8"))
    readme = ROOT / "README.md"
    current = readme.read_text(encoding="utf-8")
    start, end = "<!-- ACTIVITY:START -->", "<!-- ACTIVITY:END -->"
    if current.count(start) != 1 or current.count(end) != 1 or current.index(start) > current.index(end):
        raise ValueError("Expected exactly one valid activity block")
    updated = re.sub(re.escape(start) + r".*?" + re.escape(end), activity_block(days),
                     current, flags=re.DOTALL)
    outputs = {readme: updated,
               ROOT / "assets/activity-interactive.svg": render_interactive(days)}
    for theme in ("dark", "light"):
        for mobile in (False, True):
            suffix = "mobile-" if mobile else ""
            for still in (False, True):
                motion_suffix = "-still" if still else ""
                path = ROOT / f"assets/activity-{suffix}{theme}{motion_suffix}.svg"
                outputs[path] = render_activity(days, theme, mobile, still)
    # Fetch, parse, validate and render everything before replacing any output.
    for path, content in outputs.items():
        if path.exists() and path.read_text(encoding="utf-8") == content:
            continue
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(path)
    print(f"{sum(count for _, count in days):,} contributions; "
          f"{sum(count > 0 for _, count in days)} active days; {days[0][0]} to {days[-1][0]}")


if __name__ == "__main__":
    main()
