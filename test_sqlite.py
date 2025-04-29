import sqlite3

# Connect to database
conn = sqlite3.connect("random_numbers.db")

# Create a cursor
cursor = conn.cursor()

# Execute SELECT query
cursor.execute("SELECT * FROM random_numbers")

# Fetch all rows
rows = cursor.fetchall()

# Process the rows
for row in rows:
    print(row)

# Close the connection
conn.close()
