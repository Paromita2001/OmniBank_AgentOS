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
    delete_otp,
    get_beneficiary_by_phone,
    get_beneficiary_by_name,
    add_beneficiary   
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
        # 🔥 CHECK PENDING OTP FIRST
        # =========================

        record = get_otp(user_id)

        if sub_intent == "money_transfer" and record and record[0] == "PENDING":

            # 🔥 VERY IMPORTANT:
            # Use raw user input as category
            category_input = entities.get("receiver") or entities.get("category")

            # If still empty, fallback to raw text
            if not category_input:
                category_input = intent.get("raw_input")

            if not category_input:
                return "Please enter category or type SKIP."

            saved_otp, receiver, phone_number, amount, _, created_at = record

            # Add beneficiary if not skipping
            if category_input.lower() != "skip":
                add_beneficiary(
                    user_id=user_id,
                    name=phone_number,
                    phone_number=phone_number,
                    category=category_input
                )

            # Generate new OTP
            otp = str(random.randint(100000, 999999))

            save_otp(
                user_id=user_id,
                otp=otp,
                receiver=phone_number,
                phone_number=phone_number,
                amount=amount,
                category=category_input if category_input.lower() != "skip" else None
            )

            return f"OTP sent.\n(Demo OTP: {otp})"

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
                    try:
                        count_int = int(count)
                        txs = txs[:count_int]
                    except:
                        if str(count).lower() == "all":
                            pass  # show all
                        else:
                            txs = txs[:5]  # safe fallback

            if not txs:
                return "No transactions found."

            label = f"last {count}" if count else "recent"
            reply = f"Your {label} transactions:\n"

            for desc, amount, date in txs:
                reply += f"- ₹{abs(amount)} to {desc} on {date}\n"

            return reply
        
        

        # =========================
        # 3️⃣ MONEY TRANSFER
        # =========================
        if sub_intent == "money_transfer":

            # -------------------------
            # 1️⃣ OTP CONFIRMATION
            # -------------------------
            if "otp" in entities:
                return self._verify_otp(
                    user_id=user_id,
                    entered_otp=str(entities["otp"])
                )

            receiver = entities.get("receiver")
            phone_number = entities.get("phone_number")
            amount = entities.get("amount")
            category = entities.get("category")

            # -------------------------
            # 3️⃣ NORMAL FLOW STARTS
            # -------------------------

            if not amount:
                return "Please provide amount."

            # Auto-detect phone if passed as receiver
            if receiver and receiver.isdigit() and len(receiver) == 10:
                phone_number = receiver
                receiver = None

            # ---------------------------------------
            # CASE 1️⃣ — Phone number transfer
            # ---------------------------------------
            if phone_number:

                beneficiary = get_beneficiary_by_phone(user_id, phone_number)

                if not beneficiary:

                    save_otp(
                        user_id=user_id,
                        otp="PENDING",
                        receiver=phone_number,
                        phone_number=phone_number,
                        amount=amount,
                        category="PENDING"
                    )

                    return (
                        "This number is not registered.\n"
                        "If you want to add as beneficiary, enter category.\n"
                        "Otherwise type SKIP to continue."
                    )

                # ✅ IMPORTANT FIX HERE
                receiver, category = beneficiary

            # ---------------------------------------
            # CASE 2️⃣ — Name transfer
            # ---------------------------------------
            elif receiver:

                matches = get_beneficiary_by_name(user_id, receiver)

                # If NOT registered → ask category (same as phone flow)
                if not matches:

                    save_otp(
                        user_id=user_id,
                        otp="PENDING",
                        receiver=receiver,
                        phone_number=receiver,
                        amount=amount,
                        category="PENDING"
                    )

                    return (
                        "This beneficiary is not registered.\n"
                        "If you want to add as beneficiary, enter category.\n"
                        "Otherwise type SKIP to continue."
                    )

                if len(matches) > 1:
                    return "Multiple beneficiaries found. Please provide phone number."

                name, phone_number, stored_category = matches[0]
                receiver = name
                category = stored_category


            else:
                return "Please provide receiver name or phone number."

            # ---------------------------------------
            # 4️⃣ Generate OTP
            # ---------------------------------------
            otp = str(random.randint(100000, 999999))

            save_otp(
                user_id=user_id,
                otp=otp,
                receiver=receiver,
                phone_number=phone_number,
                amount=amount,
                category=category
            )

            return f"OTP sent.\n(Demo OTP: {otp})"




        # =========================
        # 4️⃣ UNKNOWN BANK REQUEST
        # =========================
        return "I could not understand your banking request."

    # --------------------------------------------------
    # OTP VERIFICATION (DB-backed)
    # --------------------------------------------------
    def _verify_otp(self, *, user_id: int, entered_otp: str) -> str:

        from datetime import datetime, timedelta

        record = get_otp(user_id)

        if not record:
            return "No pending transfer found."

        # Expecting: saved_otp, receiver, phone_number, amount, category, created_at
        saved_otp, receiver, phone_number, amount, category, created_at = record

        # 🔒 Safe datetime parsing (SQLite format)
        try:
            created_time = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # fallback if microseconds stored
            created_time = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")

        # 🔒 OTP Expiry Check (2 minutes)
        if datetime.now() - created_time > timedelta(minutes=2):
            delete_otp(user_id)
            return "OTP expired. Please initiate the transfer again."

        # 🔐 OTP Match Check
        if entered_otp != saved_otp:
            delete_otp(user_id)
            return "Invalid OTP. Transfer cancelled."
        
        if not category:
            category = "others"
        # ✅ Perform transfer
        success, msg = make_transfer(
            user_id=user_id,
            receiver_name=receiver,
            amount=amount,
            category=category
        )

        delete_otp(user_id)

        return msg