# from db.banking_db import get_transactions_by_time
# from datetime import datetime, timedelta


# class AnalyticsAgent:

#     def handle(self, user_id, intent, entities):

#         sub_intent = intent.get("sub_intent")

#         if sub_intent != "spending_analysis":
#             return "Unsupported analytics request."

#         timeframe = entities.get("timeframe")
#         category = entities.get("category")

#         if not timeframe:
#             return "Please specify a time period for spending analysis."

#         # ----------------------------------
#         # Handle last_month
#         # ----------------------------------
#         if timeframe == "last_month":
#             today = datetime.today()
#             first_day_this_month = today.replace(day=1)
#             last_day_last_month = first_day_this_month - timedelta(days=1)
#             start_date = last_day_last_month.replace(day=1).strftime("%Y-%m-%d 00:00:00")
#             end_date = last_day_last_month.strftime("%Y-%m-%d 23:59:59")

#         # ----------------------------------
#         # Handle this_month
#         # ----------------------------------
#         elif timeframe == "this_month":
#             today = datetime.today()
#             start_date = today.replace(day=1).strftime("%Y-%m-%d 00:00:00")
#             end_date = today.strftime("%Y-%m-%d 23:59:59")
#         else:
#             return "Timeframe not supported yet."

#         transactions = get_transactions_by_time(
#             user_id,
#             start_date,
#             end_date
#         )

#         if not transactions:
#             return "No transactions found for this period."

#         total = 0

#         for desc, amount, txn_category, trans_date in transactions:
#             if not category:
#                 total += amount
#             elif txn_category and txn_category.lower() == category.lower():
#                 total += amount

#         return f"You spent ₹{total:.2f} on {category} during {timeframe}."





from db.banking_db import get_transactions_by_time
from datetime import datetime, timedelta


class AnalyticsAgent:

    def handle(self, user_id, intent, entities):

        sub_intent = intent.get("sub_intent")

        if sub_intent != "spending_analysis":
            return "Unsupported analytics request."

        timeframe = entities.get("timeframe")
        category = entities.get("category")

        # Fix invalid category phrases
        invalid_categories = [
            "spending categories",
            "categories",
            "spending",
            "my spending",
            "all categories"
        ]

        if category and category.lower() in invalid_categories:
            category = None

        # -------------------------------------------------
        # DEFAULT TIMEFRAME (fix for "please specify time")
        # -------------------------------------------------
        if not timeframe:
            timeframe = "this_month"

        today = datetime.today()

        # -------------------------------------------------
        # LAST MONTH
        # -------------------------------------------------
        if timeframe == "last_month":

            first_day_this_month = today.replace(day=1)
            last_day_last_month = first_day_this_month - timedelta(days=1)

            start_date = last_day_last_month.replace(day=1).strftime("%Y-%m-%d 00:00:00")
            end_date = last_day_last_month.strftime("%Y-%m-%d 23:59:59")

        # -------------------------------------------------
        # THIS MONTH
        # -------------------------------------------------
        elif timeframe == "this_month":

            start_date = today.replace(day=1).strftime("%Y-%m-%d 00:00:00")
            end_date = today.strftime("%Y-%m-%d 23:59:59")

        else:
            return "Timeframe not supported yet."

        # -------------------------------------------------
        # FETCH TRANSACTIONS
        # -------------------------------------------------
        transactions = get_transactions_by_time(
            user_id,
            start_date,
            end_date
        )

        if not transactions:
            return "No transactions found for this period."

        total = 0

        for desc, amount, txn_category, trans_date in transactions:

            if category:
                if txn_category and txn_category.lower() == category.lower():
                    total += float(amount)
            else:
                total += float(amount)

        # -------------------------------------------------
        # RESPONSE TEXT
        # -------------------------------------------------
        if category:
            return f"You spent ₹{total:.2f} on {category} during {timeframe}."
        else:
            return f"You spent ₹{total:.2f} in total during {timeframe}."