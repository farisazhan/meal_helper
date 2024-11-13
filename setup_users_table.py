import sqlite3

conn = sqlite3.connect('meals.db')
cursor = conn.cursor()

# Create a users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    firstname TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Insert a sample user (hashed password recommended for real-world apps)
#cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('faris', '123'))

conn.commit()
conn.close()
