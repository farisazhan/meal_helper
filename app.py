from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import json
import hashlib  # For simple password hashing (use more secure methods like bcrypt in production)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('meals.db')
    conn.row_factory = sqlite3.Row
    return conn

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def default_route():
    # Redirect to login page if user is not logged in
    if 'email' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT firstname FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    firstname = result[0] if result else 'User'
    
    cursor.execute("SELECT id, name FROM meals")
    meals = cursor.fetchall()
    conn.close()
    return render_template('home.html', meals=meals, firstname=firstname)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['email'] = email
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        email = request.form['email']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email already exists. Please choose a different one.', 'danger')
        else:
            # Insert new user into the users table
            cursor.execute("INSERT INTO users (email, firstname, password) VALUES (?, ?, ?)", (email, firstname, hashed_password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        conn.close()

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


def get_meal_by_id(meal_id):
    conn = sqlite3.connect('meals.db')
    conn.row_factory = sqlite3.Row  # This will allow access by column name
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM meals WHERE id = ?", (meal_id,))
    meal = cursor.fetchone()

    conn.close()
    return meal

@app.route('/meal/<int:meal_id>')
def meal_details(meal_id):
    if 'email' not in session:
        return redirect(url_for('login'))
    
    meal = get_meal_by_id(meal_id)

    conn = sqlite3.connect('meals.db')
    conn.row_factory = sqlite3.Row  # This will allow access by column name

    cursor = conn.cursor()
    cursor.execute("SELECT ingredients.name, meals_ingredients.quantity, ingredients.unit FROM meals_ingredients JOIN ingredients ON meals_ingredients.ingredient_id = ingredients.id WHERE meals_ingredients.meal_id = ?;", (meal_id,))
    ingredients = cursor.fetchall()

    if meal:
        return render_template('meal_details.html', meal=meal, ingredients=ingredients)
    return "Meal not found", 404

if __name__ == '__main__':
    app.run(debug=True)
