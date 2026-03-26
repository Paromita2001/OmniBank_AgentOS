import threading
import time
from datetime import datetime, timedelta

from db.reminder_db import (
    get_due_reminders,
    update_reminder_time,
    get_user_reminders
)

from services.notification_service import send_email_notification


def start_scheduler():

    def run():
        while True:
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                due_reminders = get_due_reminders(current_time)

                for reminder_id, user_id, message in due_reminders:

                    # ⚠ Replace with real email fetching logic later
                    user_email = "your_email@gmail.com"

                    # Send Email
                    send_email_notification(
                        user_email,
                        "OmniBank Reminder",
                        f"Reminder: {message}"
                    )

                    # -------------------------------
                    # 🔥 Move Reminder to Next Month
                    # -------------------------------

                    # Get original reminder time
                    reminders = get_user_reminders(user_id)
                    original = next(
                        (r for r in reminders if r[0] == reminder_id),
                        None
                    )

                    if not original:
                        continue

                    _, _, remind_at = original

                    try:
                        original_dt = datetime.strptime(
                            remind_at,
                            "%Y-%m-%d %H:%M:%S"
                        )
                    except Exception:
                        continue

                    # Calculate next month
                    month = original_dt.month + 1
                    year = original_dt.year

                    if month > 12:
                        month = 1
                        year += 1

                    try:
                        next_dt = original_dt.replace(
                            year=year,
                            month=month
                        )
                    except ValueError:
                        # Handle cases like 31st Feb
                        next_dt = original_dt + timedelta(days=30)

                    update_reminder_time(
                        reminder_id,
                        next_dt.strftime("%Y-%m-%d %H:%M:%S")
                    )

                time.sleep(30)

            except Exception as e:
                print("Scheduler Error:", e)
                time.sleep(30)

    thread = threading.Thread(target=run, daemon=True)
    thread.start()