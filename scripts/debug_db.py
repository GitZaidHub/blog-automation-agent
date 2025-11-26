import sqlite3
import os

db_path = "./data/db.sqlite3"

if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
else:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT sid, state FROM sessions")
        rows = cursor.fetchall()
        
        if not rows:
            print("No sessions found in the database.")
        else:
            print(f"Found {len(rows)} sessions:")
            for row in rows:
                print(f"ID: {row[0]}, State: {row[1]}")
        
        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")
