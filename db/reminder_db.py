import sqlite3
from pathlib import Path

# Create proper DB path (same style as bank.db)
DB_PATH = Path(__file__).parent / "reminder.sqlite"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ===============================
# CREATE TABLE
# ===============================
def create_reminder_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            message TEXT,
            remind_at TEXT,
            notified INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


# ===============================
# ADD REMINDER
# ===============================
def add_reminder(user_id, message, remind_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reminders (user_id, message, remind_at, notified)
        VALUES (?, ?, ?, 0)
    """, (user_id, message, remind_at))

    conn.commit()
    conn.close()


# ===============================
# GET USER REMINDERS
# ===============================
def get_user_reminders(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, message, remind_at
        FROM reminders
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


# ===============================
# DELETE REMINDER
# ===============================
def delete_reminder(reminder_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM reminders
        WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()

def update_reminder_time(reminder_id, new_time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reminders
        SET remind_at = ?, notified = 0
        WHERE id = ?
    """, (new_time, reminder_id))

    conn.commit()
    conn.close()
# ===============================
# DUE REMINDERS (Scheduler)
# ===============================
def get_due_reminders(current_time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_id, message
        FROM reminders
        WHERE remind_at <= ? AND notified = 0
    """, (current_time,))

    results = cursor.fetchall()
    conn.close()
    return results


def mark_reminder_notified(reminder_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE reminders
        SET notified = 1
        WHERE id = ?
    """, (reminder_id,))

    conn.commit()
    conn.close()