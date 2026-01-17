import sqlite3
from datetime import datetime, date, timedelta

DB_PATH = "db/bank.db"


# -------------------------
# DB CONNECTION
# -------------------------
def _get_connection():
    return sqlite3.connect(DB_PATH)


# -------------------------
# NATURAL DATE PARSER
# -------------------------
def parse_natural_date(text: str):
    """
    Converts:
    - today
    - tomorrow
    - day after tomorrow
    - 2026-01-05
    - 12 Aug / 12 August
    Returns a Python date object or None
    """
    if not text:
        return None

    text = text.lower().strip()
    today = date.today()

    if "day after tomorrow" in text:
        return today + timedelta(days=2)

    if "tomorrow" in text:
        return today + timedelta(days=1)

    if "today" in text:
        return today

    # ISO format: 2026-01-05
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except:
        pass

    # 12 Aug
    try:
        return datetime.strptime(text, "%d %b").replace(year=today.year).date()
    except:
        pass

    # 12 August
    try:
        return datetime.strptime(text, "%d %B").replace(year=today.year).date()
    except:
        pass

    return None


# -------------------------
# TABLE INIT
# -------------------------
def init_reminder_table():
    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,

            frequency TEXT NOT NULL,        -- once / daily / monthly
            scheduled_date TEXT,            -- ISO date: YYYY-MM-DD
            day INTEGER,                    -- for monthly reminders

            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# -------------------------
# ADD REMINDER
# -------------------------
def add_reminder(
    user_id: int,
    task: str,
    frequency: str,
    scheduled_date: date | None = None,
    day: int | None = None
):
    """
    frequency:
      - once    → scheduled_date required
      - daily   → no date needed
      - monthly → day required
    """
    init_reminder_table()

    # ✅ CRITICAL FIX: store date as ISO string
    scheduled_date_str = (
        scheduled_date.isoformat() if scheduled_date else None
    )

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO reminders
        (user_id, task, frequency, scheduled_date, day, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        task,
        frequency,
        scheduled_date_str,
        day,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


# -------------------------
# GET ALL REMINDERS
# -------------------------
def get_reminders(user_id: int):
    init_reminder_table()

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task, frequency, scheduled_date, day, created_at
        FROM reminders
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


# -------------------------
# FIND REMINDERS BY TASK
# -------------------------
def find_reminders_by_task(user_id: int, task: str):
    init_reminder_table()

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task
        FROM reminders
        WHERE user_id = ?
        AND LOWER(task) LIKE ?
    """, (user_id, f"%{task.lower()}%"))

    rows = cur.fetchall()
    conn.close()
    return rows


# -------------------------
# DELETE REMINDER
# -------------------------
def delete_reminder(reminder_id: int, user_id: int):
    init_reminder_table()

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM reminders
        WHERE id = ? AND user_id = ?
    """, (reminder_id, user_id))

    conn.commit()
    conn.close()


# -------------------------
# GET DUE REMINDERS
# -------------------------
def get_due_reminders(user_id: int):
    """
    Returns reminders that should trigger today
    """
    init_reminder_table()

    today_str = date.today().isoformat()
    today_day = date.today().day

    conn = _get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT task, frequency, scheduled_date, day
        FROM reminders
        WHERE user_id = ?
        AND (
            (frequency = 'once' AND scheduled_date = ?)
            OR frequency = 'daily'
            OR (frequency = 'monthly' AND day = ?)
        )
    """, (user_id, today_str, today_day))

    rows = cur.fetchall()
    conn.close()
    return rows
