from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Set up MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client["user_db"]  # The database
users_collection = db["users"]  # The collection (table) for users

# Route to the registration page
@app.route('/')
def index():
    return render_template('register.html')

# Route to handle the registration form submission
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if user already exists
        if users_collection.find_one({"username": username}):
            return "Username already taken, try a different one."

        # Hash the password
        hashed_password = generate_password_hash(password, method='sha256')

        # Save user data to MongoDB
        users_collection.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })

        return redirect(url_for('success'))

# Success page
@app.route('/success')
def success():
    return "Registration successful! You can now log in."

if __name__ == '__main__':
    app.run(debug=True)
