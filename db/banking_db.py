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
        category TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, phone_number),
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
        category TEXT,
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
    print(" Tables created successfully")
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
    INSERT OR IGNORE INTO users (name, phone, email, password_hash)
    VALUES (?, ?, ?, ?)
    """, users)

    conn.commit()
    conn.close()
    print(" Users inserted")
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
    INSERT OR IGNORE  INTO accounts (user_id, account_number, balance)
    VALUES (?, ?, ?)
    """, accounts)

    conn.commit()
    conn.close()
    print(" Accounts inserted")
    print("✅ Accounts inserted")

# -------------------------
# Insert Beneficiaries (ALL 10 USERS)
# -------------------------
def insert_beneficiaries():
    conn = get_connection()
    cursor = conn.cursor()

    beneficiaries = [


        # USER 1
        (1,"Rohit Sharma","9000000001","grocery"),
        (1,"Aman Verma","9000000002","shopping"),
        (1,"Simran Kaur","9000000003","bills"),
        (1,"Neha Kapoor","9000000004","others"),
        (1,"Kiran Patel","9000000005","vegetables"),
        (1,"Vikas Mehta","9000000006","electronics"),
        (1,"Pooja Singh","9000000007","dairy"),
        (1,"Dev Mishra","9000000008","gym"),
        (1,"Sonia Arora","9000000009","school_fee"),
        (1,"Arjun Malhotra","9000000010","emi"),

        # USER 2
        (2,"Riya Malhotra","9000000011","shopping"),
        (2,"Tarun Sinha","9000000012","grocery"),
        (2,"Aditi Rao","9000000013","others"),
        (2,"Harsh Vardhan","9000000014","bills"),
        (2,"Sneha Jain","9000000015","vegetables"),
        (2,"Kunal Gupta","9000000016","electronics"),
        (2,"Komal Sharma","9000000017","dairy"),
        (2,"Nikhil Bansal","9000000018","gym"),
        (2,"Jaya Patel","9000000019","school_fee"),
        (2,"Sunil Yadav","9000000020","emi"),

        # USER 3
        (3,"Meena Kumari","9000000021","grocery"),
        (3,"Suresh Nair","9000000022","shopping"),
        (3,"Anil Kumar","9000000023","bills"),
        (3,"Fatima Syed","9000000024","others"),
        (3,"Ritu Saxena","9000000025","vegetables"),
        (3,"Rajesh Khanna","9000000026","electronics"),
        (3,"Priya Das","9000000027","dairy"),
        (3,"Imran Ali","9000000028","gym"),
        (3,"Krishna Rao","9000000029","school_fee"),
        (3,"Arpita Bose","9000000030","emi"),

        # USER 4
        (4,"Deepak Yadav","9000000031","grocery"),
        (4,"Shalini Gupta","9000000032","shopping"),
        (4,"Gaurav Singh","9000000033","bills"),
        (4,"Tanya Kapoor","9000000034","others"),
        (4,"Sahil Khan","9000000035","vegetables"),
        (4,"Lavanya Iyer","9000000036","electronics"),
        (4,"Yash Raj","9000000037","dairy"),
        (4,"Preeti Nair","9000000038","gym"),
        (4,"Ashwin Rao","9000000039","school_fee"),
        (4,"Monika Jain","9000000040","emi"),

        # USER 5
        (5,"Kabir Mehta","9000000041","grocery"),
        (5,"Ishita Sharma","9000000042","shopping"),
        (5,"Rohan Joshi","9000000043","bills"),
        (5,"Snehal Patil","9000000044","others"),
        (5,"Aditya Deshmukh","9000000045","vegetables"),
        (5,"Sana Sheikh","9000000046","electronics"),
        (5,"Farhan Ali","9000000047","dairy"),
        (5,"Namrata Bose","9000000048","gym"),
        (5,"Jatin Patel","9000000049","school_fee"),
        (5,"Bhavya Sethi","9000000050","emi"),

        # USER 6
        (6,"Varun Singh","9000000051","grocery"),
        (6,"Chirag Shah","9000000052","shopping"),
        (6,"Aisha Khan","9000000053","bills"),
        (6,"Ritesh Kumar","9000000054","others"),
        (6,"Pallavi Roy","9000000055","vegetables"),
        (6,"Omar Shaikh","9000000056","electronics"),
        (6,"Shreya Rathi","9000000057","dairy"),
        (6,"Harshit Garg","9000000058","gym"),
        (6,"Tara Menon","9000000059","school_fee"),
        (6,"Naveen Rao","9000000060","emi"),

        # USER 7
        (7,"Yuvraj Singh","9000000061","grocery"),
        (7,"Mahima Jain","9000000062","shopping"),
        (7,"Siddharth Mehra","9000000063","bills"),
        (7,"Payal Arora","9000000064","others"),
        (7,"Aman Ali","9000000065","vegetables"),
        (7,"Rashmi Das","9000000066","electronics"),
        (7,"Vikrant Nair","9000000067","dairy"),
        (7,"Tanvi Shah","9000000068","gym"),
        (7,"Hemant Yadav","9000000069","school_fee"),
        (7,"Shruti Verma","9000000070","emi"),

        # USER 8
        (8,"Parth Malhotra","9000000071","grocery"),
        (8,"Jasmine Kaur","9000000072","shopping"),
        (8,"Mohit Sinha","9000000073","bills"),
        (8,"Aarohi Gupta","9000000074","others"),
        (8,"Tejas Desai","9000000075","vegetables"),
        (8,"Ayaan Khan","9000000076","electronics"),
        (8,"Bhavika Patel","9000000077","dairy"),
        (8,"Rehan Shaikh","9000000078","gym"),
        (8,"Nidhi Sharma","9000000079","school_fee"),
        (8,"Samar Kapoor","9000000080","emi"),

        # USER 9
        (9,"Kartik Mathur","9000000081","grocery"),
        (9,"Manisha Iyer","9000000082","shopping"),
        (9,"Saurabh Saxena","9000000083","bills"),
        (9,"Poonam Kumari","9000000084","others"),
        (9,"Abdul Rahman","9000000085","vegetables"),
        (9,"Vidhi Gupta","9000000086","electronics"),
        (9,"Raghav Sharma","9000000087","dairy"),
        (9,"Ishan Patel","9000000088","gym"),
        (9,"Trisha Bose","9000000089","school_fee"),
        (9,"Devanshi Mehta","9000000090","emi"),

        # USER 10
        (10,"Ananya Singh","9000000091","grocery"),
        (10,"Harshil Shah","9000000092","shopping"),
        (10,"Meera Rao","9000000093","bills"),
        (10,"Krish Patel","9000000094","others"),
        (10,"Shivani Sharma","9000000095","vegetables"),
        (10,"Ravish Kumar","9000000096","electronics"),
        (10,"Ayushi Jain","9000000097","dairy"),
        (10,"Karan Malhotra","9000000098","gym"),
        (10,"Surbhi Thakur","9000000099","school_fee"),
        (10,"Aniket Deshmukh","9000000100","emi"),
    ]


    # cursor.executemany("""
    # INSERT OR IGNORE INTO beneficiaries (user_id, name, phone_number, category)
    # VALUES (?, ?, ?, ?)
    #     # USER 1
    #     (1,"Rohit Sharma","9000000001"),(1,"Aman Verma","9000000002"),
    #     (1,"Simran Kaur","9000000003"),(1,"Neha Kapoor","9000000004"),
    #     (1,"Kiran Patel","9000000005"),(1,"Vikas Mehta","9000000006"),
    #     (1,"Pooja Singh","9000000007"),(1,"Dev Mishra","9000000008"),
    #     (1,"Sonia Arora","9000000009"),(1,"Arjun Malhotra","9000000010"),

    #     # USER 2
    #     (2,"Riya Malhotra","9000000011"),(2,"Tarun Sinha","9000000012"),
    #     (2,"Aditi Rao","9000000013"),(2,"Harsh Vardhan","9000000014"),
    #     (2,"Sneha Jain","9000000015"),(2,"Kunal Gupta","9000000016"),
    #     (2,"Komal Sharma","9000000017"),(2,"Nikhil Bansal","9000000018"),
    #     (2,"Jaya Patel","9000000019"),(2,"Sunil Yadav","9000000020"),

    #     # USER 3
    #     (3,"Meena Kumari","9000000021"),(3,"Suresh Nair","9000000022"),
    #     (3,"Anil Kumar","9000000023"),(3,"Fatima Syed","9000000024"),
    #     (3,"Ritu Saxena","9000000025"),(3,"Rajesh Khanna","9000000026"),
    #     (3,"Priya Das","9000000027"),(3,"Imran Ali","9000000028"),
    #     (3,"Krishna Rao","9000000029"),(3,"Arpita Bose","9000000030"),

    #     # USER 4
    #     (4,"Deepak Yadav","9000000031"),(4,"Shalini Gupta","9000000032"),
    #     (4,"Gaurav Singh","9000000033"),(4,"Tanya Kapoor","9000000034"),
    #     (4,"Sahil Khan","9000000035"),(4,"Lavanya Iyer","9000000036"),
    #     (4,"Yash Raj","9000000037"),(4,"Preeti Nair","9000000038"),
    #     (4,"Ashwin Rao","9000000039"),(4,"Monika Jain","9000000040"),

    #     # USER 5
    #     (5,"Kabir Mehta","9000000041"),(5,"Ishita Sharma","9000000042"),
    #     (5,"Rohan Joshi","9000000043"),(5,"Snehal Patil","9000000044"),
    #     (5,"Aditya Deshmukh","9000000045"),(5,"Sana Sheikh","9000000046"),
    #     (5,"Farhan Ali","9000000047"),(5,"Namrata Bose","9000000048"),
    #     (5,"Jatin Patel","9000000049"),(5,"Bhavya Sethi","9000000050"),

    #     # USER 6
    #     (6,"Varun Singh","9000000051"),(6,"Chirag Shah","9000000052"),
    #     (6,"Aisha Khan","9000000053"),(6,"Ritesh Kumar","9000000054"),
    #     (6,"Pallavi Roy","9000000055"),(6,"Omar Shaikh","9000000056"),
    #     (6,"Shreya Rathi","9000000057"),(6,"Harshit Garg","9000000058"),
    #     (6,"Tara Menon","9000000059"),(6,"Naveen Rao","9000000060"),

    #     # USER 7
    #     (7,"Yuvraj Singh","9000000061"),(7,"Mahima Jain","9000000062"),
    #     (7,"Siddharth Mehra","9000000063"),(7,"Payal Arora","9000000064"),
    #     (7,"Aman Ali","9000000065"),(7,"Rashmi Das","9000000066"),
    #     (7,"Vikrant Nair","9000000067"),(7,"Tanvi Shah","9000000068"),
    #     (7,"Hemant Yadav","9000000069"),(7,"Shruti Verma","9000000070"),

    #     # USER 8
    #     (8,"Parth Malhotra","9000000071"),(8,"Jasmine Kaur","9000000072"),
    #     (8,"Mohit Sinha","9000000073"),(8,"Aarohi Gupta","9000000074"),
    #     (8,"Tejas Desai","9000000075"),(8,"Ayaan Khan","9000000076"),
    #     (8,"Bhavika Patel","9000000077"),(8,"Rehan Shaikh","9000000078"),
    #     (8,"Nidhi Sharma","9000000079"),(8,"Samar Kapoor","9000000080"),

    #     # USER 9
    #     (9,"Kartik Mathur","9000000081"),(9,"Manisha Iyer","9000000082"),
    #     (9,"Saurabh Saxena","9000000083"),(9,"Poonam Kumari","9000000084"),
    #     (9,"Abdul Rahman","9000000085"),(9,"Vidhi Gupta","9000000086"),
    #     (9,"Raghav Sharma","9000000087"),(9,"Ishan Patel","9000000088"),
    #     (9,"Trisha Bose","9000000089"),(9,"Devanshi Mehta","9000000090"),

    #     # USER 10
    #     (10,"Ananya Singh","9000000091"),(10,"Harshil Shah","9000000092"),
    #     (10,"Meera Rao","9000000093"),(10,"Krish Patel","9000000094"),
    #     (10,"Shivani Sharma","9000000095"),(10,"Ravish Kumar","9000000096"),
    #     (10,"Ayushi Jain","9000000097"),(10,"Karan Malhotra","9000000098"),
    #     (10,"Surbhi Thakur","9000000099"),(10,"Aniket Deshmukh","9000000100"),
    # ]

    cursor.executemany("""
    INSERT INTO beneficiaries (user_id, name, phone_number, category)
    VALUES (?, ?, ?, ?)
    """, beneficiaries)

    conn.commit()
    conn.close()
    print(" Beneficiaries inserted for all 10 users")
    print("✅ Beneficiaries inserted for all 10 users")


# -------------------------
# Insert Transactions (ALL USERS – CORRECTED)
# -------------------------
def insert_transactions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions")


    transactions = [
        

        # USER 1
        (1,600,"debit","Rohit Sharma","grocery"),
        (1,1200,"debit","Aman Verma","shopping"),
        (1,450,"debit","Simran Kaur","bills"),
        (1,900,"debit","Neha Kapoor","others"),
        (1,750,"debit","Kiran Patel","vegetables"),
        (1,1300,"debit","Vikas Mehta","electronics"),
        (1,500,"debit","Pooja Singh","dairy"),
        (1,1100,"debit","Dev Mishra","gym"),
        (1,650,"debit","Sonia Arora","school_fee"),
        (1,1600,"debit","Arjun Malhotra","emi"),

        # USER 2
        (2,900,"debit","Riya Malhotra","shopping"),
        (2,1500,"debit","Tarun Sinha","grocery"),
        (2,700,"debit","Aditi Rao","others"),
        (2,1400,"debit","Harsh Vardhan","bills"),
        (2,650,"debit","Sneha Jain","vegetables"),
        (2,1800,"debit","Kunal Gupta","electronics"),
        (2,550,"debit","Komal Sharma","dairy"),
        (2,1000,"debit","Nikhil Bansal","gym"),
        (2,1300,"debit","Jaya Patel","school_fee"),
        (2,1200,"debit","Sunil Yadav","emi"),

        # USER 3
        (3,700,"debit","Meena Kumari","grocery"),
        (3,1600,"debit","Suresh Nair","shopping"),
        (3,800,"debit","Anil Kumar","bills"),
        (3,950,"debit","Fatima Syed","others"),
        (3,400,"debit","Ritu Saxena","vegetables"),
        (3,1300,"debit","Rajesh Khanna","electronics"),
        (3,600,"debit","Priya Das","dairy"),
        (3,900,"debit","Imran Ali","gym"),
        (3,1100,"debit","Krishna Rao","school_fee"),
        (3,1500,"debit","Arpita Bose","emi"),

        # USER 4
        (4,850,"debit","Deepak Yadav","grocery"),
        (4,1100,"debit","Shalini Gupta","shopping"),
        (4,500,"debit","Gaurav Singh","bills"),
        (4,700,"debit","Tanya Kapoor","others"),
        (4,650,"debit","Sahil Khan","vegetables"),
        (4,1700,"debit","Lavanya Iyer","electronics"),
        (4,450,"debit","Yash Raj","dairy"),
        (4,900,"debit","Preeti Nair","gym"),
        (4,1200,"debit","Ashwin Rao","school_fee"),
        (4,2000,"debit","Monika Jain","emi"),

        # USER 5
        (5,1000,"debit","Kabir Mehta","grocery"),
        (5,900,"debit","Ishita Sharma","shopping"),
        (5,600,"debit","Rohan Joshi","bills"),
        (5,800,"debit","Snehal Patil","others"),
        (5,750,"debit","Aditya Deshmukh","vegetables"),
        (5,1500,"debit","Sana Sheikh","electronics"),
        (5,500,"debit","Farhan Ali","dairy"),
        (5,950,"debit","Namrata Bose","gym"),
        (5,1300,"debit","Jatin Patel","school_fee"),
        (5,2200,"debit","Bhavya Sethi","emi"),

        # USER 6
        (6,700,"debit","Varun Singh","grocery"),
        (6,1050,"debit","Chirag Shah","shopping"),
        (6,480,"debit","Aisha Khan","bills"),
        (6,820,"debit","Ritesh Kumar","others"),
        (6,600,"debit","Pallavi Roy","vegetables"),
        (6,1400,"debit","Omar Shaikh","electronics"),
        (6,520,"debit","Shreya Rathi","dairy"),
        (6,880,"debit","Harshit Garg","gym"),
        (6,1100,"debit","Tara Menon","school_fee"),
        (6,1800,"debit","Naveen Rao","emi"),

        # USER 7
        (7,950,"debit","Yuvraj Singh","grocery"),
        (7,1200,"debit","Mahima Jain","shopping"),
        (7,600,"debit","Siddharth Mehra","bills"),
        (7,750,"debit","Payal Arora","others"),
        (7,680,"debit","Aman Ali","vegetables"),
        (7,1600,"debit","Rashmi Das","electronics"),
        (7,500,"debit","Vikrant Nair","dairy"),
        (7,920,"debit","Tanvi Shah","gym"),
        (7,1350,"debit","Hemant Yadav","school_fee"),
        (7,2100,"debit","Shruti Verma","emi"),

        # USER 8
        (8,800,"debit","Parth Malhotra","grocery"),
        (8,1150,"debit","Jasmine Kaur","shopping"),
        (8,550,"debit","Mohit Sinha","bills"),
        (8,700,"debit","Aarohi Gupta","others"),
        (8,630,"debit","Tejas Desai","vegetables"),
        (8,1500,"debit","Ayaan Khan","electronics"),
        (8,520,"debit","Bhavika Patel","dairy"),
        (8,870,"debit","Rehan Shaikh","gym"),
        (8,1250,"debit","Nidhi Sharma","school_fee"),
        (8,1950,"debit","Samar Kapoor","emi"),

        # USER 9
        (9,900,"debit","Kartik Mathur","grocery"),
        (9,1000,"debit","Manisha Iyer","shopping"),
        (9,620,"debit","Saurabh Saxena","bills"),
        (9,770,"debit","Poonam Kumari","others"),
        (9,640,"debit","Abdul Rahman","vegetables"),
        (9,1550,"debit","Vidhi Gupta","electronics"),
        (9,510,"debit","Raghav Sharma","dairy"),
        (9,880,"debit","Ishan Patel","gym"),
        (9,1400,"debit","Trisha Bose","school_fee"),
        (9,2300,"debit","Devanshi Mehta","emi"),

        # USER 10
        (10,850,"debit","Ananya Singh","grocery"),
        (10,1250,"debit","Harshil Shah","shopping"),
        (10,580,"debit","Meera Rao","bills"),
        (10,730,"debit","Krish Patel","others"),
        (10,610,"debit","Shivani Sharma","vegetables"),
        (10,1650,"debit","Ravish Kumar","electronics"),
        (10,540,"debit","Ayushi Jain","dairy"),
        (10,910,"debit","Karan Malhotra","gym"),
        (10,1450,"debit","Surbhi Thakur","school_fee"),
        (10,2500,"debit","Aniket Deshmukh","emi"),

    ]

    # ----
    cursor.executemany("""
    INSERT OR IGNORE  INTO transactions (user_id, amount, transaction_type, description, category)
    VALUES (?, ?, ?, ?, ?)
    """, transactions)

    # transactions = [
    #     (1,600,"debit","Rohit Sharma"),(1,1200,"debit","Aman Verma"),
    #     (1,450,"debit","Simran Kaur"),(1,900,"debit","Neha Kapoor"),
    #     (1,750,"debit","Kiran Patel"),(1,1300,"debit","Vikas Mehta"),
    #     (1,500,"debit","Pooja Singh"),(1,1100,"debit","Dev Mishra"),
    #     (1,650,"debit","Sonia Arora"),(1,1600,"debit","Arjun Malhotra"),

    #     (2,900,"debit","Riya Malhotra"),(2,1500,"debit","Tarun Sinha"),
    #     (2,700,"debit","Aditi Rao"),(2,1400,"debit","Harsh Vardhan"),
    #     (2,650,"debit","Sneha Jain"),(2,1800,"debit","Kunal Gupta"),
    #     (2,550,"debit","Komal Sharma"),(2,1000,"debit","Nikhil Bansal"),
    #     (2,1300,"debit","Jaya Patel"),(2,1200,"debit","Sunil Yadav"),

    #     (3,700,"debit","Meena Kumari"),(3,1600,"debit","Suresh Nair"),
    #     (3,800,"debit","Anil Kumar"),(3,950,"debit","Fatima Syed"),
    #     (3,400,"debit","Ritu Saxena"),(3,1300,"debit","Rajesh Khanna"),
    #     (3,600,"debit","Priya Das"),(3,900,"debit","Imran Ali"),
    #     (3,1100,"debit","Krishna Rao"),(3,1500,"debit","Arpita Bose"),
    # ]

    # cursor.executemany("""
    # INSERT INTO transactions (user_id, amount, transaction_type, description)
    # VALUES (?, ?, ?, ?)
    # """, transactions)

    conn.commit()
    conn.close()
    print(" Transactions inserted correctly")




# -------------------------
# Transfer (FIXED)
# -------------------------
def make_transfer(user_id, receiver_name, amount, category):
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
        UPDATE accounts
        SET balance = balance - ?
        WHERE user_id = ?
    """, (amount, user_id))

    cursor.execute("""
        INSERT INTO transactions (user_id, amount, transaction_type, description, category)
        VALUES (?, ?, 'debit', ?, ?)
    """, (user_id, amount, receiver_name, category))

    conn.commit()
    conn.close()

    return True, f" ₹{amount} sent to {receiver_name}"
    # UPDATE accounts SET balance = balance - ?
    # WHERE user_id = ?
    # """, (amount, user_id))

    # cursor.execute("""
    # INSERT INTO transactions (user_id, amount, transaction_type, description)
    # VALUES (?, ?, 'debit', ?)
    # """, (user_id, amount, receiver_name))

    # conn.commit()
    # conn.close()
    # return True, f"✅ ₹{amount} sent to {receiver_name}"


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
    SELECT description, amount, category, trans_date
    From transactions
    WHERE user_id = ?
    AND trans_date BETWEEN ? AND ?
    ORDER BY trans_date DESC
    """, (user_id, start_date, end_date))

    rows = cursor.fetchall()
    conn.close()
    return rows

# -------------------------
# Get Beneficiary By Phone
# -------------------------
def get_beneficiary_by_phone(user_id, phone_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, category
        FROM beneficiaries
        WHERE user_id = ? AND phone_number = ?
    """, (user_id, phone_number))

    row = cursor.fetchone()
    conn.close()

    return row  # returns (name, category)


# -------------------------
# Get Beneficiary By Name
# -------------------------
def get_beneficiary_by_name(user_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name, phone_number, category
        FROM beneficiaries
        WHERE user_id = ? AND LOWER(name) = LOWER(?)
    """, (user_id, name))

    rows = cursor.fetchall()
    conn.close()

    return rows  # could be multiple matches


# -------------------------
# Add Beneficiary
# -------------------------
def add_beneficiary(user_id, name, phone_number, category):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO beneficiaries (user_id, name, phone_number, category)
        VALUES (?, ?, ?, ?)
    """, (user_id, name, phone_number, category))

    conn.commit()
    conn.close()

# -------------------------
# OTP TABLE (CREATE ONCE)
# -------------------------
def create_otp_table():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otp (
        user_id INTEGER PRIMARY KEY,
        otp TEXT,
        receiver TEXT,
        phone_number TEXT,
        amount REAL,
        category TEXT,
        created_at TEXT
    )
    """)

    print("Creating OTP table in:", DB_PATH)

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
from datetime import datetime
import sqlite3

def save_otp(user_id, otp, receiver, phone_number, amount, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        DELETE FROM otp WHERE user_id = ?
    """, (user_id,))

    cursor.execute("""
        INSERT INTO otp (
            user_id, otp, receiver, phone_number, amount, category, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        otp,
        receiver,
        phone_number,
        amount,
        category,
        created_at
    ))
    print("Saving OTP in:", DB_PATH)
# def save_otp(user_id, otp, receiver, amount):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     DELETE FROM otp_store WHERE user_id = ?
#     """, (user_id,))

#     cursor.execute("""
#     INSERT INTO otp_store (user_id, otp, receiver, amount)
#     VALUES (?, ?, ?, ?)
#     """, (user_id, otp, receiver, amount))

#     conn.commit()
#     conn.close()


# -------------------------
# GET OTP
# -------------------------
# def get_otp(user_id: int):
#     """
#     Fetch latest OTP record for user.
#     Returns:
#     (otp, receiver, phone_number, amount, category, created_at)
#     """

def get_otp(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT otp, receiver, phone_number, amount, category, created_at
        FROM otp
        WHERE user_id = ?
    """, (user_id,))

    record = cursor.fetchone()
    conn.close()

    return record
    


# -------------------------
# DELETE OTP
# -------------------------
def delete_otp(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    # cursor.execute("""
    # DELETE FROM otp WHERE user_id = ?
    # DELETE FROM otp_store WHERE user_id = ?
    # """, (user_id,))

    cursor.execute("DELETE FROM otp WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM otp_store WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()
