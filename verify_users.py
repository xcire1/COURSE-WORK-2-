from pathlib import Path
import sqlite3
import sys

# Try to import the project's connect_database helper. Prefer the package import
# `app.data.db` which matches the project layout; fall back to a direct DB path.
try:
    from app.data.db import connect_database
except Exception:
    # Fallback: use direct DB path
    DB_PATH = Path(r"C:\Users\erick\Desktop\CST1510 COURSE WORK 2\CW2_M01056946_CST1510\DATA") / "intelligence_platform.db"


def main():
    # Use project's connection helper when available
    try:
        conn = connect_database()
    except Exception:
        conn = sqlite3.connect(str(DB_PATH))

    cursor = conn.cursor()

    # Query all users
    cursor.execute("SELECT id, username, role FROM users")
    users = cursor.fetchall()

    print(" Users in database:")
    print(f"{'ID':<5} {'Username':<15} {'Role':<10}")
    print("-" * 35)
    for user in users:
        print(f"{user[0]:<5} {user[1]:<15} {user[2]:<10}")

    print(f"\nTotal users: {len(users)}")
    conn.close()


if __name__ == '__main__':
    main()
