from html import entities
from itertools import count


from pipeline.timeframe_parser import resolve_timeframe
from db.banking_db import get_transactions_by_time


# agents/bank_agent.py

import random
from typing import Optional

from db.banking_db import (
    get_balance,
    get_transaction_history,
    get_transactions_by_time,
    make_transfer,
    save_otp,
    get_otp,
    delete_otp
)

from pipeline.timeframe_parser import resolve_timeframe


class BankAgent:
    """
    Handles secure banking operations:
    - balance check
    - transaction history (with timeframe support)
    - money transfer with OTP (DB-backed)
    """

    def handle(
        self,
        *,
        user_id: int,
        intent: dict,
        entities: Optional[dict] = None
    ) -> str:

        entities = entities or {}
        sub_intent = intent.get("sub_intent")

        # =========================
        # 1️⃣ BALANCE CHECK
        # =========================
        if sub_intent == "balance_check":
            balance = get_balance(user_id)
            return f"Your current balance is ₹{balance:.2f}"

        # =========================
        # 2️⃣ TRANSACTION HISTORY
        # =========================
        if sub_intent == "transaction_history":

            count = entities.get("count")          # e.g. 2
            timeframe = entities.get("timeframe")  # e.g. "2 days"

            # ---- Timeframe-based ----
            if timeframe:
                start_date, end_date = resolve_timeframe(timeframe)

                if not start_date or not end_date:
                    return "Sorry, I could not understand the time range."

                txs = get_transactions_by_time(
                    user_id=user_id,
                    start_date=start_date,
                    end_date=end_date
                )

            # ---- Count-based (last N) ----
            else:
                txs = get_transaction_history(user_id)

                if count:
                    txs = txs[:int(count)]

            if not txs:
                return "No transactions found."

            label = f"last {count}" if count else "recent"
            reply = f"Your {label} transactions:\n"

            for desc, amount, date in txs:
                reply += f"- ₹{abs(amount)} to {desc} on {date}\n"

            return reply

        # =========================
        # 3️⃣ MONEY TRANSFER (OTP FLOW)
        # =========================
        if sub_intent == "money_transfer":

            # ---- OTP CONFIRMATION STEP ----
            if "otp" in entities:
                return self._verify_otp(
                    user_id=user_id,
                    entered_otp=str(entities["otp"])
                )

            receiver = entities.get("receiver")
            amount = entities.get("amount")

            # ---- Missing info checks ----
            if not receiver and not amount:
                return "Please tell me whom you want to send money to and the amount."

            if not receiver:
                return "Please tell me the receiver name."

            if not amount:
                return "Please tell me the amount you want to transfer."

            # ---- Generate OTP ----
            otp = str(random.randint(100000, 999999))

            save_otp(
                user_id=user_id,
                otp=otp,
                receiver=receiver,
                amount=amount
            )

            return (
                "OTP sent to your registered mobile number.\n"
                f"(Demo OTP: {otp})\n"
                "Please enter the OTP to confirm transfer."
            )

        # =========================
        # 4️⃣ UNKNOWN BANK REQUEST
        # =========================
        return "I could not understand your banking request."

    # --------------------------------------------------
    # OTP VERIFICATION (DB-backed)
    # --------------------------------------------------
    def _verify_otp(self, *, user_id: int, entered_otp: str) -> str:

        record = get_otp(user_id)

        if not record:
            return "No pending transfer found."

        saved_otp, receiver, amount = record

        if entered_otp != saved_otp:
            return "Invalid OTP. Transfer cancelled."

        success, msg = make_transfer(
            user_id=user_id,
            receiver_name=receiver,
            amount=amount
        )

        # Cleanup OTP
        delete_otp(user_id)

        return msg
