"""
Cold Chain Logistics - AI Assistant
File: db/connection.py

Kaam:
  1. MySQL server se connect karta hai (database naam ke bina pehle)
  2. schema.sql file padhta hai
  3. Usme likhe CREATE DATABASE / CREATE TABLE statements khud chala deta hai

Isse aapko MySQL Workbench mein manually kuch paste karne ki zarurat
nahi - bas yeh file run karo: python db/connection.py
"""

import os
import mysql.connector
from mysql.connector import Error

# ----------------------------------------------------------
# Step 1: Connection settings
# Abhi ke liye yahan seedha likh rahe hain taaki samajhna aasan ho.
# Baad mein hum inhe config/settings.py aur .env mein move kar denge
# (taaki password kahin bhi hardcoded na dikhe).
# ----------------------------------------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",          # apna MySQL username daalo
    "password": "YOUR_PASSWORD_HERE",  # apna MySQL password daalo
}

# schema.sql is file ke ek folder upar, db/ ke andar hai
SCHEMA_FILE_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


def run_schema():
    """schema.sql file padhta hai aur database + tables bana deta hai."""
    connection = None
    try:
        # Step 2: Pehle bina database select kiye connect karo
        # (kyunki database khud abhi bana nahi hai)
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        print("MySQL se connect ho gaya. Ab schema.sql padh rahe hain...")

        # Step 3: schema.sql file ka pura content padho
        with open(SCHEMA_FILE_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()

        # Step 4: File mein multiple statements hain (har ek ';' se alag hota hai)
        # Hum unhe ek-ek karke chalayenge, comments aur khaali lines skip karke.
        statements = [s.strip() for s in schema_sql.split(";") if s.strip()
                     and not s.strip().startswith("--")]

        for statement in statements:
            # Agar statement mein sirf comments hain (koi real SQL nahi), skip karo
            cleaned = "\n".join(
                line for line in statement.split("\n")
                if not line.strip().startswith("--")
            ).strip()
            if not cleaned:
                continue 

            cursor.execute(cleaned)
            print(f"  -> Executed: {cleaned.splitlines()[0][:60]}...")

        connection.commit()
        print("\nDone! Database aur saari tables ban gayi.")

        # Step 5: Confirm karne ke liye tables list karo
        cursor.execute("USE ColdChainDB")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("\nBani hui tables:")
        for t in tables:
            print(f"  - {t[0]}")

    except Error as e:
        print(f"MySQL Error aaya: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("\nConnection band kar diya.")


# ----------------------------------------------------------
# Step 6: Reusable function - baaki files (tools.py, seed_data.py)
# isi function ko use karke database se connect karenge.
# ----------------------------------------------------------
def get_connection():
    """ColdChainDB se ek connection return karta hai (reusable)."""
    config = DB_CONFIG.copy()
    config["database"] = "ColdChainDB"
    return mysql.connector.connect(**config)


if __name__ == "__main__":
    run_schema()