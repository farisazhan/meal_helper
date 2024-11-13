import sqlite3

conn = sqlite3.connect('meals.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    meal_category TEXT CHECK(meal_category = 'Breakfast' OR meal_category = 'Lunch' OR meal_category = 'Dinner'),
    name TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL
)
''')

# Insert sample data
meals_data = [
    ('Spaghetti Bolognese', 'Spaghetti, Ground beef, Tomato sauce, Onions, Garlic', 'Cook the spaghetti, sauté the onions and garlic, add ground beef, and mix with tomato sauce. Serve hot.'),
    ('Chicken Curry', 'Chicken, Curry powder, Coconut milk, Onions, Ginger', 'Cook onions and ginger, add chicken and curry powder, pour coconut milk, and simmer. Serve with rice.')
]

cursor.executemany('INSERT INTO meals (name, ingredients, instructions) VALUES (?, ?, ?)', meals_data)

conn.commit()
conn.close()
