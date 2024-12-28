import sqlite3

# Connect to the database (creates the file if it doesn't exist)
conn = sqlite3.connect('vehicle_data.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table named 'vehicle_entry'
cursor.execute('''
CREATE TABLE IF NOT EXISTS vehicle_entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing ID
    plate_number TEXT NOT NULL,           -- Detected plate number
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP -- Timestamp of detection
)
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully!")
