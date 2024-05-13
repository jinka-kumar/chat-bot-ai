from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient


app = Flask(__name__)
app.secret_key = 'JINKA123'  # Change this to a random secret key

# Dummy database (replace this with actual database logic)
client = MongoClient('mongodb://localhost:27017')
db = client['groq']
users_collection = db['users']

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'email': username})  # Find user by email
        if user and user['password'] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        existing_user = users_collection.find_one({'email': username})
        
        if not username or not password or not confirm_password:
            flash('All fields are required.', 'error')
        elif existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match.', 'error')
        else:
            # Insert the new user into the database
            users_collection.insert_one({'email': username, 'password': password})
            flash('Sign up successful! You can now log in.', 'success')
            return redirect(url_for('login'))
            
    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    return "This is the dashboard. Only authenticated users can access this page."

if __name__ == "__main__":
    app.run(debug=True)

