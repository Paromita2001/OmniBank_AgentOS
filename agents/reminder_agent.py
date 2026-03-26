from datetime import datetime
from db.reminder_db import (
    add_reminder,
    delete_reminder,
    get_user_reminders
)


class ReminderAgent:

    def handle(self, *, user_id: int, intent: dict, entities: dict = None):
        entities = entities or {}
        sub_intent = intent.get("sub_intent")

        # =============================
        # ADD REMINDER
        # =============================
        if sub_intent == "add_reminder":

            task = entities.get("task")
            date = entities.get("date")
            frequency = entities.get("frequency")

            if not task:
                return "Please specify what to remind."

            today = datetime.now()

            if date:
                try:
                    day = int(
                        date.replace("th", "")
                            .replace("st", "")
                            .replace("nd", "")
                            .replace("rd", "")
                    )

                    if today.day >= day:
                        month = today.month + 1
                        year = today.year
                        if month > 12:
                            month = 1
                            year += 1
                    else:
                        month = today.month
                        year = today.year

                    remind_at_dt = datetime(year, month, day, 9, 0, 0)

                except Exception:
                    return "Invalid date format."
            else:
                remind_at_dt = today

            remind_at = remind_at_dt.strftime("%Y-%m-%d %H:%M:%S")

            add_reminder(user_id, task, remind_at)

            return f"Reminder set: {task} ({frequency if frequency else 'one-time'})"

        # =============================
        # SHOW REMINDERS
        # =============================
        if sub_intent == "show_reminders":

            reminders = get_user_reminders(user_id)

            if not reminders:
                return "No reminders found."

            reply = "Your reminders:\n"

            for rid, text, remind_at in reminders:
                reply += f"ID {rid}: {text} at {remind_at}\n"

            return reply

        # =============================
        # DELETE REMINDER (Smart Mode)
        # =============================
        if sub_intent == "delete_reminder":

            task = entities.get("task")
            date = entities.get("date")

            reminders = get_user_reminders(user_id)

            if not reminders:
                return "No reminders found."

            matches = []

            for rid, text, remind_at in reminders:

                task_match = task and task.lower() in text.lower()

                date_match = False
                if date:
                    try:
                        day = int(
                            date.replace("th", "")
                                .replace("st", "")
                                .replace("nd", "")
                                .replace("rd", "")
                        )
                        stored_day = datetime.strptime(
                            remind_at, "%Y-%m-%d %H:%M:%S"
                        ).day

                        if day == stored_day:
                            date_match = True
                    except Exception:
                        pass

                if task and date:
                    if task_match and date_match:
                        matches.append((rid, text, remind_at))
                elif task:
                    if task_match:
                        matches.append((rid, text, remind_at))
                elif date:
                    if date_match:
                        matches.append((rid, text, remind_at))

            if not matches:
                return "No matching reminder found."

            if len(matches) > 1:
                reply = "Multiple reminders found:\n"
                for rid, text, remind_at in matches:
                    reply += f"ID {rid}: {text} at {remind_at}\n"
                reply += "Please be more specific."
                return reply

            rid, text, remind_at = matches[0]
            delete_reminder(rid)

            return f"Reminder '{text}' deleted successfully."

        return "I could not understand your reminder request."