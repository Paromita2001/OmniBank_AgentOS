from datetime import datetime, timedelta
import re


def resolve_timeframe(text: str):
    """
    Public API used by agents.
    Converts natural language timeframes into (start_date, end_date)
    """
    return _parse_timeframe(text)


def _parse_timeframe(text: str):
    text = text.lower()
    now = datetime.now()

    # ---------------------------
    # LAST N DAYS (2 days, 7 days)
    # ---------------------------
    match = re.search(r"(\d+)\s*day", text)
    if match:
        days = int(match.group(1))
        start_date = now - timedelta(days=days)
        return start_date, now

    # ---------------------------
    # LAST MONTH
    # ---------------------------
    if "last month" in text:
        first_this_month = now.replace(day=1)
        last_month_end = first_this_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        return last_month_start, last_month_end

    # ---------------------------
    # MONTH NAME (march, april)
    # ---------------------------
    months = {
        "january": 1, "february": 2, "march": 3,
        "april": 4, "may": 5, "june": 6,
        "july": 7, "august": 8, "september": 9,
        "october": 10, "november": 11, "december": 12
    }

    for month_name, month_num in months.items():
        if month_name in text:
            year = now.year
            start = datetime(year, month_num, 1)

            if month_num == 12:
                end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
            else:
                end = datetime(year, month_num + 1, 1) - timedelta(seconds=1)

            return start, end

    # ---------------------------
    # DEFAULT → TODAY
    # ---------------------------
    start_today = now.replace(hour=0, minute=0, second=0)
    return start_today, now
