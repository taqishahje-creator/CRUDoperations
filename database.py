# Import Python's built-in SQLite library
import sqlite3

# ---------------------------------------------
# STEP 1: Connect to the SQLite database
# ---------------------------------------------
# If "tasks.db" does not exist, SQLite creates it automatically.
connection = sqlite3.connect("tasks.db")

# Create a cursor object.
# The cursor is used to execute SQL commands.
cursor = connection.cursor()

# ---------------------------------------------
# STEP 2: Create the table (only if it doesn't exist)
# ---------------------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
)
""")

# ---------------------------------------------
# STEP 3: Check whether the table already contains data
# ---------------------------------------------
cursor.execute("SELECT COUNT(*) FROM tasks")

# fetchone() returns a tuple like (0,) or (5,)
# [0] extracts the actual number.
task_count = cursor.fetchone()[0]

# ---------------------------------------------
# STEP 4: Insert sample data ONLY if the table is empty
# ---------------------------------------------
if task_count == 0:

    sample_tasks = [
        ("Buy groceries", False),
        ("Complete assignment", True),
        ("Exercise for 30 minutes", False)
    ]

    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        sample_tasks
    )

    print("Sample tasks inserted.")

else:
    print("Database already contains tasks. Skipping insertion.")

# ---------------------------------------------
# STEP 5: Display all tasks
# ---------------------------------------------
cursor.execute("SELECT * FROM tasks")

tasks = cursor.fetchall()

print("\nCurrent Tasks")

for task in tasks:
    print(task)

# ---------------------------------------------
# STEP 6: Save changes permanently
# ---------------------------------------------
connection.commit()

# ---------------------------------------------
# STEP 7: Close the database connection
# ---------------------------------------------
connection.close()

print("\nDatabase setup completed successfully.")
