import sqlite3

conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Logs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# People count table
cursor.execute("""
CREATE TABLE IF NOT EXISTS people_count (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    count INTEGER,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# Save alert log
def save_log(message):
    cursor.execute(
        "INSERT INTO logs (message) VALUES (?)",
        (message,)
    )
    conn.commit()

# Save people count
def save_count(count):
    cursor.execute(
        "INSERT INTO people_count (count) VALUES (?)",
        (count,)
    )
    conn.commit()