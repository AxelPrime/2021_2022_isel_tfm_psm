import sqlite3
from sqlite3 import Error


def run():
    db_name = "sqlite.patient.db"

    query = """
        CREATE TABLE IF NOT EXISTS patient (
            sns_number TEXT NOT NULL UNIQUE,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            birth_date TEXT NOT NULL,
            address TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            locality TEXT NOT NULL,
            country TEXT NOT NULL,
            subsystem TEXT NOT NULL,
            nationality TEXT NOT NULL
        )
    """

    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        print(e)
        raise e

    cur = conn.cursor()
    cur.execute(query)
