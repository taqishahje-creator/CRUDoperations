# Import Python's built-in SQLite library
import sqlite3

db_file = "tasks.db"  # Database file name
# ---------------------------------------------
# STEP 1: Connect to the SQLite database
# ---------------------------------------------
def connection():
    
# If "tasks.db" does not exist, SQLite creates it automatically.
    connection = sqlite3.connect(db_file)
    connection.row_factory = sqlite3.Row  # This allows us to access columns by name.
    
    return connection
# Create a cursor object.
# The cursor is used to execute SQL commands.
    
    
    
def initialize_database():
    """
    Creates the database and inserts sample data
    only the first time the application runs.
    """

    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM tasks")
    count = cursor.fetchone()[0]

    if count == 0:

        sample_tasks = [
            ("Buy groceries", False),
            ("Complete assignment", True),
            ("Exercise for 30 minutes", False)
        ]

        cursor.executemany(
            "INSERT INTO tasks(title, done) VALUES (?, ?)",
            sample_tasks
        )

        print("Sample tasks inserted.")

    else:

        print("Database already contains tasks.")

    connection.commit()
    connection.close()
