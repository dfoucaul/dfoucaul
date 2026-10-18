"""Checks for calendar data integrity and the rolling-year aggregation."""

from datetime import date, timedelta
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from update_activity import parse_calendar, weekly_counts, render_activity


def calendar(days, bad_tooltip=False):
    cells = []
    for index, (day, count) in enumerate(reversed(days)):
        text = f"{count:,} contributions on January 1st." if count else "No contributions on January 1st."
        if bad_tooltip and index == 0:
            text = "Unexpected response"
        cells.append(f'<td id="day-{index}" data-date="{day}"></td>'
                     f'<tool-tip for="day-{index}">{text}</tool-tip>')
    return "".join(cells)


class ActivityTests(unittest.TestCase):
    def test_rolling_year_sorts_dates_and_excludes_leading_week(self):
        days = [(date(2024, 1, 1) + timedelta(days=index), 1000 if index < 7 else 1)
                for index in range(372)]
        parsed = parse_calendar(calendar(days))
        self.assertEqual(parsed, days[-365:])
        self.assertEqual(sum(count for _, count in parsed), 365)

    def test_weekly_series_keeps_partial_week_and_total(self):
        days = [(date(2025, 1, 1) + timedelta(days=index), 1)
                for index in range(365)]
        counts = weekly_counts(parse_calendar(calendar(days)))
        self.assertEqual(len(counts), 53)
        self.assertEqual(sum(counts), 365)
        self.assertEqual(counts[-1], 1)

    def test_unknown_tooltip_is_rejected(self):
        days = [(date(2025, 1, 1) + timedelta(days=index), 1)
                for index in range(365)]
        with self.assertRaises(ValueError):
            parse_calendar(calendar(days, bad_tooltip=True))

    def test_gap_is_rejected_even_with_365_records(self):
        days = [(date(2025, 1, 1) + timedelta(days=index), 1)
                for index in range(366) if index != 100]
        with self.assertRaises(ValueError):
            parse_calendar(calendar(days))

    def test_zero_activity_renders_without_invalid_coordinates(self):
        days = [(date(2025, 1, 1) + timedelta(days=index), 0)
                for index in range(365)]
        parsed = parse_calendar(calendar(days))
        for mobile in (False, True):
            svg = render_activity(parsed, "dark", mobile)
            self.assertNotIn("nan", svg.lower())
            self.assertNotIn("inf", svg.lower())
            self.assertIn("0 contributions · 0 active days", svg)


if __name__ == "__main__":
    unittest.main()
