from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "secret123"

client = MongoClient("mongodb://localhost:27017/")
db = client.party_db

# Home
@app.route('/')
def home():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = {
            "username": request.form['username'],
            "password": request.form['password']
        }
        db.users.insert_one(user)
        return redirect('/login')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db.users.find_one({
            "username": request.form['username'],
            "password": request.form['password']
        })
        if user:
            session['user'] = user['username']
            return redirect('/dashboard')
        else:
            return "Invalid Login"
    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        bookings = list(db.bookings.find({"user": session['user']}))
        return render_template('dashboard.html', bookings=bookings)
    return redirect('/login')

# Booking
@app.route('/book', methods=['POST'])
def book():
    if 'user' in session:
        booking = {
            "user": session['user'],
            "event": request.form['event'],
            "venue": request.form['venue']
        }
        db.bookings.insert_one(booking)
        return redirect('/dashboard')
    return redirect('/login')

# Admin
@app.route('/admin')
def admin():
    all_bookings = list(db.bookings.find())
    return render_template('admin.html', bookings=all_bookings)

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)