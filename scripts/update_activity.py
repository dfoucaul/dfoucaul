"""Use the aggregate already displayed on the public GitHub calendar.

This includes private contributions when the user has made those counts visible.
It does not request repository data or require a personal access token.
"""

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
URL = "https://github.com/users/dfoucaul/contributions"


class CalendarHeading(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_heading = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "h2" and dict(attrs).get("id") == "js-contribution-activity-description":
            self.in_heading = True

    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_heading = False

    def handle_data(self, data):
        if self.in_heading:
            self.parts.append(data)


def parse_total(html):
    parser = CalendarHeading()
    parser.feed(html)
    heading = " ".join("".join(parser.parts).split())
    match = re.fullmatch(r"([\d,]+) contributions? in the last year", heading)
    if not match:
        raise ValueError("Contribution calendar total not found; leaving README unchanged")
    return int(match.group(1).replace(",", ""))


def main():
    request = Request(URL, headers={
        "User-Agent": "github-profile-calendar-summary",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urlopen(request, timeout=30) as response:
        count = parse_total(response.read().decode("utf-8"))
    formatted = f"{count:,}".replace(",", " ")
    start, end = "<!-- ACTIVITY:START -->", "<!-- ACTIVITY:END -->"
    readme = ROOT / "README.md"
    current = readme.read_text(encoding="utf-8")
    if current.count(start) != 1 or current.count(end) != 1:
        raise ValueError("Expected exactly one activity block")
    if current.index(start) > current.index(end):
        raise ValueError("Activity markers are in the wrong order")
    replacement = (
        f"{start}\n**{formatted} contributions** sur les douze derniers mois, "
        f"activité privée incluse.\n{end}"
    )
    updated = re.sub(re.escape(start) + r".*?" + re.escape(end), replacement,
                     current, flags=re.DOTALL)
    if updated != current:
        temporary = readme.with_suffix(".md.tmp")
        temporary.write_text(updated, encoding="utf-8")
        temporary.replace(readme)
    print(f"{formatted} contributions — total from the public GitHub calendar")


if __name__ == "__main__":
    main()
