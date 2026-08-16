import os

import psycopg
import psycopg.rows
from dotenv import load_dotenv


# Load variables from .env
load_dotenv(override=True)


# Get DATABASE_URL from environment variables
db_url = os.getenv("DATABASE_URL")

if not db_url:
    raise ValueError("DATABASE_URL environment variable is not set.")


# ---------------------------------------------
# STEP 1: Connect to the PostgreSQL database
# ---------------------------------------------
def connection() -> psycopg.Connection:
    """
    Creates and returns a connection to PostgreSQL.
    """

    conn = psycopg.connect(str(db_url))

    # Allows rows to be accessed using column names
    conn.row_factory = psycopg.rows.dict_row

    return conn


# ---------------------------------------------
# STEP 2: Initialize the database
# ---------------------------------------------
def initialize_database() -> None:
    """
    Creates the tasks table if it doesn't exist
    and inserts sample data if the table is empty.
    """

    conn = connection()

    try:
        cursor = conn.cursor()

        # Create table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL
            )
        """)

        # Check whether tasks already exist
        cursor.execute("SELECT COUNT(*) AS count FROM tasks")

        row = cursor.fetchone()

        if isinstance(row, dict):
            count = row.get("count", 0)
        else:
            count = row[0] if row is not None else 0

        # Insert sample data only if table is empty
        if count == 0:

            sample_tasks = [
                ("Buy groceries", False),
                ("Complete assignment", True),
                ("Exercise for 30 minutes", False)
            ]

            cursor.executemany(
                """
                INSERT INTO tasks (title, done)
                VALUES (%s, %s)
                """,
                sample_tasks
            )

            print("Sample tasks inserted.")

        else:
            print("Database already contains tasks.")

        # Save changes
        conn.commit()

    except Exception:
        # Undo changes if something goes wrong
        conn.rollback()
        raise

    finally:
        # Always close the connection
        conn.close()