import sqlite3

# Connect database
conn = sqlite3.connect("threat_logs.db")

# Cursor create
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS threats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attack_type TEXT,
    severity TEXT
)
""")

print("Database Created Successfully")

# Save changes
conn.commit()

# Close connection
conn.close()