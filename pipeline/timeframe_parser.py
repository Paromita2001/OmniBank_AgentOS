# pipeline/timeframe_parser.py

from datetime import datetime, timedelta
import re


def resolve_timeframe(text: str):
    """
    Converts natural language timeframes into (start_date, end_date).
    """

    if not text:
        return None, None

    text = text.lower()
    now = datetime.now()

    # ---------------------------
    # Last N days
    # ---------------------------
    match = re.search(r"(\d+)\s*day", text)
    if match:
        days = int(match.group(1))
        start_date = now - timedelta(days=days)
        return start_date, now

    # ---------------------------
    # Yesterday
    # ---------------------------
    if "yesterday" in text:
        start = now - timedelta(days=1)
        start = start.replace(hour=0, minute=0, second=0)
        end = start.replace(hour=23, minute=59, second=59)
        return start, end

    # ---------------------------
    # Last Month
    # ---------------------------
    if "last month" in text:
        first_this_month = now.replace(day=1)
        last_month_end = first_this_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)
        return last_month_start, last_month_end

    # ---------------------------
    # Default → Today
    # ---------------------------
    start_today = now.replace(hour=0, minute=0, second=0)
    return start_today, now
