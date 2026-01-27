import sqlite3
from pathlib import Path

# -------------------------
# Database path
# -------------------------
DB_PATH = Path(__file__).parent / "bank.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


# -------------------------
# Create Tables
# -------------------------
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        email TEXT,
        password_hash TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        account_number TEXT,
        balance REAL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beneficiaries (
        beneficiary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        transaction_type TEXT,
        description TEXT,
        trans_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        reminder_text TEXT,
        reminder_time TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Tables created successfully")

def insert_users():
    conn = get_connection()
    cursor = conn.cursor()

    users = [
        ("Paromita", "7205013256", "paromitakarmakar06@gmail.com", "paromita@1234"),
        ("User2", "9000000002", "u2@example.com", "pass"),
        ("User3", "9000000003", "u3@example.com", "pass"),
        ("User4", "9000000004", "u4@example.com", "pass"),
        ("User5", "9000000005", "u5@example.com", "pass"),
        ("User6", "9000000006", "u6@example.com", "pass"),
        ("User7", "9000000007", "u7@example.com", "pass"),
        ("User8", "9000000008", "u8@example.com", "pass"),
        ("User9", "9000000009", "u9@example.com", "pass"),
        ("User10", "9000000010", "u10@example.com", "pass"),
    ]

    cursor.executemany("""
    INSERT INTO users (name, phone, email, password_hash)
    VALUES (?, ?, ?, ?)
    """, users)

    conn.commit()
    conn.close()
    print("✅ Users inserted")

def insert_accounts():
    conn = get_connection()
    cursor = conn.cursor()

    accounts = [
        (1, "ACC001", 50000),
        (2, "ACC002", 60000),
        (3, "ACC003", 55000),
        (4, "ACC004", 70000),
        (5, "ACC005", 65000),
        (6, "ACC006", 80000),
        (7, "ACC007", 45000),
        (8, "ACC008", 90000),
        (9, "ACC009", 72000),
        (10, "ACC010", 100000),
    ]

    cursor.executemany("""
    INSERT INTO accounts (user_id, account_number, balance)
    VALUES (?, ?, ?)
    """, accounts)

    conn.commit()
    conn.close()
    print("✅ Accounts inserted")

# -------------------------
# Insert Beneficiaries (ALL 10 USERS)
# -------------------------
def insert_beneficiaries():
    conn = get_connection()
    cursor = conn.cursor()

    beneficiaries = [
        # USER 1
        (1,"Rohit Sharma","9000000001"),(1,"Aman Verma","9000000002"),
        (1,"Simran Kaur","9000000003"),(1,"Neha Kapoor","9000000004"),
        (1,"Kiran Patel","9000000005"),(1,"Vikas Mehta","9000000006"),
        (1,"Pooja Singh","9000000007"),(1,"Dev Mishra","9000000008"),
        (1,"Sonia Arora","9000000009"),(1,"Arjun Malhotra","9000000010"),

        # USER 2
        (2,"Riya Malhotra","9000000011"),(2,"Tarun Sinha","9000000012"),
        (2,"Aditi Rao","9000000013"),(2,"Harsh Vardhan","9000000014"),
        (2,"Sneha Jain","9000000015"),(2,"Kunal Gupta","9000000016"),
        (2,"Komal Sharma","9000000017"),(2,"Nikhil Bansal","9000000018"),
        (2,"Jaya Patel","9000000019"),(2,"Sunil Yadav","9000000020"),

        # USER 3
        (3,"Meena Kumari","9000000021"),(3,"Suresh Nair","9000000022"),
        (3,"Anil Kumar","9000000023"),(3,"Fatima Syed","9000000024"),
        (3,"Ritu Saxena","9000000025"),(3,"Rajesh Khanna","9000000026"),
        (3,"Priya Das","9000000027"),(3,"Imran Ali","9000000028"),
        (3,"Krishna Rao","9000000029"),(3,"Arpita Bose","9000000030"),

        # USER 4
        (4,"Deepak Yadav","9000000031"),(4,"Shalini Gupta","9000000032"),
        (4,"Gaurav Singh","9000000033"),(4,"Tanya Kapoor","9000000034"),
        (4,"Sahil Khan","9000000035"),(4,"Lavanya Iyer","9000000036"),
        (4,"Yash Raj","9000000037"),(4,"Preeti Nair","9000000038"),
        (4,"Ashwin Rao","9000000039"),(4,"Monika Jain","9000000040"),

        # USER 5
        (5,"Kabir Mehta","9000000041"),(5,"Ishita Sharma","9000000042"),
        (5,"Rohan Joshi","9000000043"),(5,"Snehal Patil","9000000044"),
        (5,"Aditya Deshmukh","9000000045"),(5,"Sana Sheikh","9000000046"),
        (5,"Farhan Ali","9000000047"),(5,"Namrata Bose","9000000048"),
        (5,"Jatin Patel","9000000049"),(5,"Bhavya Sethi","9000000050"),

        # USER 6
        (6,"Varun Singh","9000000051"),(6,"Chirag Shah","9000000052"),
        (6,"Aisha Khan","9000000053"),(6,"Ritesh Kumar","9000000054"),
        (6,"Pallavi Roy","9000000055"),(6,"Omar Shaikh","9000000056"),
        (6,"Shreya Rathi","9000000057"),(6,"Harshit Garg","9000000058"),
        (6,"Tara Menon","9000000059"),(6,"Naveen Rao","9000000060"),

        # USER 7
        (7,"Yuvraj Singh","9000000061"),(7,"Mahima Jain","9000000062"),
        (7,"Siddharth Mehra","9000000063"),(7,"Payal Arora","9000000064"),
        (7,"Aman Ali","9000000065"),(7,"Rashmi Das","9000000066"),
        (7,"Vikrant Nair","9000000067"),(7,"Tanvi Shah","9000000068"),
        (7,"Hemant Yadav","9000000069"),(7,"Shruti Verma","9000000070"),

        # USER 8
        (8,"Parth Malhotra","9000000071"),(8,"Jasmine Kaur","9000000072"),
        (8,"Mohit Sinha","9000000073"),(8,"Aarohi Gupta","9000000074"),
        (8,"Tejas Desai","9000000075"),(8,"Ayaan Khan","9000000076"),
        (8,"Bhavika Patel","9000000077"),(8,"Rehan Shaikh","9000000078"),
        (8,"Nidhi Sharma","9000000079"),(8,"Samar Kapoor","9000000080"),

        # USER 9
        (9,"Kartik Mathur","9000000081"),(9,"Manisha Iyer","9000000082"),
        (9,"Saurabh Saxena","9000000083"),(9,"Poonam Kumari","9000000084"),
        (9,"Abdul Rahman","9000000085"),(9,"Vidhi Gupta","9000000086"),
        (9,"Raghav Sharma","9000000087"),(9,"Ishan Patel","9000000088"),
        (9,"Trisha Bose","9000000089"),(9,"Devanshi Mehta","9000000090"),

        # USER 10
        (10,"Ananya Singh","9000000091"),(10,"Harshil Shah","9000000092"),
        (10,"Meera Rao","9000000093"),(10,"Krish Patel","9000000094"),
        (10,"Shivani Sharma","9000000095"),(10,"Ravish Kumar","9000000096"),
        (10,"Ayushi Jain","9000000097"),(10,"Karan Malhotra","9000000098"),
        (10,"Surbhi Thakur","9000000099"),(10,"Aniket Deshmukh","9000000100"),
    ]

    cursor.executemany("""
    INSERT INTO beneficiaries (user_id, name, phone_number)
    VALUES (?, ?, ?)
    """, beneficiaries)

    conn.commit()
    conn.close()
    print("✅ Beneficiaries inserted for all 10 users")


# -------------------------
# Insert Transactions (ALL USERS – CORRECTED)
# -------------------------
def insert_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    transactions = [
        (1,600,"debit","Rohit Sharma"),(1,1200,"debit","Aman Verma"),
        (1,450,"debit","Simran Kaur"),(1,900,"debit","Neha Kapoor"),
        (1,750,"debit","Kiran Patel"),(1,1300,"debit","Vikas Mehta"),
        (1,500,"debit","Pooja Singh"),(1,1100,"debit","Dev Mishra"),
        (1,650,"debit","Sonia Arora"),(1,1600,"debit","Arjun Malhotra"),

        (2,900,"debit","Riya Malhotra"),(2,1500,"debit","Tarun Sinha"),
        (2,700,"debit","Aditi Rao"),(2,1400,"debit","Harsh Vardhan"),
        (2,650,"debit","Sneha Jain"),(2,1800,"debit","Kunal Gupta"),
        (2,550,"debit","Komal Sharma"),(2,1000,"debit","Nikhil Bansal"),
        (2,1300,"debit","Jaya Patel"),(2,1200,"debit","Sunil Yadav"),

        (3,700,"debit","Meena Kumari"),(3,1600,"debit","Suresh Nair"),
        (3,800,"debit","Anil Kumar"),(3,950,"debit","Fatima Syed"),
        (3,400,"debit","Ritu Saxena"),(3,1300,"debit","Rajesh Khanna"),
        (3,600,"debit","Priya Das"),(3,900,"debit","Imran Ali"),
        (3,1100,"debit","Krishna Rao"),(3,1500,"debit","Arpita Bose"),
    ]

    cursor.executemany("""
    INSERT INTO transactions (user_id, amount, transaction_type, description)
    VALUES (?, ?, ?, ?)
    """, transactions)

    conn.commit()
    conn.close()
    print("✅ Transactions inserted correctly")


# -------------------------
# Transfer (FIXED)
# -------------------------
def make_transfer(user_id, receiver_name, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM accounts WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "❌ Account not found"

    balance = row[0]
    if balance < amount:
        conn.close()
        return False, "❌ Insufficient balance"

    cursor.execute("""
    UPDATE accounts SET balance = balance - ?
    WHERE user_id = ?
    """, (amount, user_id))

    cursor.execute("""
    INSERT INTO transactions (user_id, amount, transaction_type, description)
    VALUES (?, ?, 'debit', ?)
    """, (user_id, amount, receiver_name))

    conn.commit()
    conn.close()
    return True, f"✅ ₹{amount} sent to {receiver_name}"


# -------------------------
# Get Balance
# -------------------------
def get_balance(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT balance
    FROM accounts
    WHERE user_id = ?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else 0


# -------------------------
# Get Transaction History (Last 10)
# -------------------------
def get_transaction_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT description, amount, trans_date
    FROM transactions
    WHERE user_id = ?
    ORDER BY trans_date DESC
    LIMIT 10
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

from datetime import datetime

def get_transactions_by_time(user_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT description, amount, trans_date
    FROM transactions
    WHERE user_id = ?
      AND trans_date BETWEEN ? AND ?
    ORDER BY trans_date DESC
    """, (user_id, start_date, end_date))

    rows = cursor.fetchall()
    conn.close()
    return rows


# -------------------------
# OTP TABLE (CREATE ONCE)
# -------------------------
def create_otp_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otp_store (
        user_id INTEGER,
        otp TEXT,
        receiver TEXT,
        amount REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# -------------------------
# SAVE OTP
# -------------------------
def save_otp(user_id, otp, receiver, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM otp_store WHERE user_id = ?
    """, (user_id,))

    cursor.execute("""
    INSERT INTO otp_store (user_id, otp, receiver, amount)
    VALUES (?, ?, ?, ?)
    """, (user_id, otp, receiver, amount))

    conn.commit()
    conn.close()


# -------------------------
# GET OTP
# -------------------------
def get_otp(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT otp, receiver, amount
    FROM otp_store
    WHERE user_id = ?
    """, (user_id,))

    row = cursor.fetchone()
    conn.close()
    return row


# -------------------------
# DELETE OTP
# -------------------------
def delete_otp(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM otp_store WHERE user_id = ?
    """, (user_id,))

    conn.commit()
    conn.close()
