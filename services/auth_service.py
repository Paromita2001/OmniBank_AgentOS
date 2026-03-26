from db.banking_db import get_connection


def authenticate_user(email: str, phone: str):
    """
    Returns user_id if valid user, else None
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id
        FROM users
        WHERE email = ? AND phone = ?
    """, (email, phone))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]
    return None