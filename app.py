from flask import Flask, render_template, request, redirect, session, flash
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import re
import os
import uuid
from dotenv import load_dotenv
import certifi

# Load environment variables from .env file
load_dotenv()

# Create Flask app with explicit configuration
app = Flask(__name__,
            instance_relative_config=True,
            instance_path=os.path.join(os.path.dirname(__file__), 'instance'))

# Get secret key from environment, fallback to default for development
app.secret_key = os.getenv('SECRET_KEY', 'secret123')

# Database connection configuration - Prioritize Environment Variable
MONGO_URI = os.getenv('MONGO_URI', "mongodb+srv://172005varshar_db_user:IA8nFP6NdYqTRmFI@cluster0.q8mdk0p.mongodb.net/party-planner?appName=Cluster0")

try:
    # Determine if we should use TLS (required for Atlas/SRV, usually not for local)
    use_tls = MONGO_URI.startswith("mongodb+srv")
    
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
        tls=use_tls,
        tlsCAFile=certifi.where() if use_tls else None,
        server_api=ServerApi('1')
    )
    # Verify connection
    client.admin.command('ping')
    db = client.get_database('party-planner')
    print('✅ MongoDB connected successfully')
except Exception as e:
    db = None
    print(f'❌ MongoDB connection failed: {e}')

def validate_password(password):
    """
    Validate password strength requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special symbol
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
        return False, "Password must contain at least one special symbol"
    
    return True, "Password is strong"

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

# Home
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health():
    """Health check endpoint for deployment monitoring."""
    db_status = is_db_available()
    return {
        "status": "online" if db_status else "degraded",
        "database": "connected" if db_status else "disconnected"
    }, 200 if db_status else 503

def is_db_available():
    return db is not None

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not is_db_available():
        flash('Database connection is unavailable. Please try again later.')
        return render_template('index.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate password strength
        is_valid, message = validate_password(password)
        if not is_valid:
            flash(f'Password validation failed: {message}')
            return render_template('signup.html', username=username)
        
        # Check if username already exists
        existing_user = db.users.find_one({"username": username})
        if existing_user:
            flash('Username already exists. Please choose a different username.')
            return render_template('signup.html', username=username)
        
        hashed_password = generate_password_hash(password)
        user = {
            "username": username,
            "password": hashed_password # Store hashed password
        }
        db.users.insert_one(user)
        flash('Registration successful! Please sign in.')
        return redirect('/signin')
    return render_template('signup.html')

# Signin
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if not is_db_available():
        flash('Database connection is unavailable. Please try again later.')
        return render_template('index.html')

    if request.method == 'POST':
        user = db.users.find_one({
            "username": request.form['username']
        })
        if user and check_password_hash(user['password'], request.form['password']): # Verify hashed password
            session['user'] = user['username']
            flash('Login successful!')
            return redirect('/dashboard')
        else:
            flash('Invalid username or password. Please try again.')
            return redirect('/signin')
    return render_template('signin.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if not is_db_available():
        flash('Database connection is unavailable. Please try again later.')
        return render_template('index.html')

    if 'user' in session:
        bookings = list(db.bookings.find({"user": session['user']}))
        return render_template('dashboard.html', bookings=bookings)
    return redirect('/signin')

# Booking
@app.route('/book', methods=['POST'])
def book():
    if not is_db_available():
        flash('Database connection is unavailable. Please try again later.')
        return redirect('/dashboard')

    if 'user' in session:
        party_date = request.form.get('party_date')
        venue = request.form.get('venue')
        event_type = request.form.get('event_type')
        time_slot = request.form.get('time_slot')
        
        # Validate that party date is not the same as today
        today = datetime.now().strftime('%Y-%m-%d')
        if party_date == today:
            flash('Booking cannot be made for today. Please select a future date.')
            return redirect('/dashboard')
        
        # Check if the same venue is already booked for the same date and time slot
        existing_booking = db.bookings.find_one({
            "venue": venue,
            "party_date": party_date,
            "time_slot": time_slot
        })
        if existing_booking:
            flash(f'This venue is already booked for {party_date} during {time_slot}. Please select a different time slot, date, or venue.')
            return redirect('/dashboard')
        
        # Calculate costs
        venue_costs = {
            'Hall': 1000,
            'Garden': 800,
            'Beach': 1200,
            'Rooftop': 1500,
            'Banquet Center': 2000,
            'Club': 1800,
            'Hotel Ballroom': 2500,
            'Backyard': 600,
            'Warehouse': 900,
            'Restaurant': 1600,
            'Cultural Center': 1300
        }
        
        venue_cost = venue_costs.get(venue, 1000)
        services_cost = 0
        selected_services = []
        
        # Check selected services
        services = {
            'catering': 500,
            'decoration': 300,
            'photography': 400,
            'dj': 400
        }
        
        for service_key, cost in services.items():
            if request.form.get(service_key):
                services_cost += cost
                selected_services.append(service_key.capitalize())
        
        total_cost = venue_cost + services_cost
        
        # Generate invoice ID
        invoice_id = str(uuid.uuid4())[:8].upper()
        
        booking = {
            "user": session['user'],
            "event": event_type,
            "venue": venue,
            "party_date": party_date,
            "time_slot": time_slot,
            "booking_date": today,
            "venue_cost": venue_cost,
            "services_cost": services_cost,
            "total_cost": total_cost,
            "selected_services": selected_services,
            "invoice_id": invoice_id,
            "status": "confirmed"
        }
        
        db.bookings.insert_one(booking)
        flash(f'Booking created successfully! Your invoice ID is: {invoice_id}')
        return redirect(f'/invoice/{invoice_id}')
    flash('Please sign-in first to make a booking.')
    return redirect('/signin')

# Invoice
@app.route('/invoice/<invoice_id>')
def invoice(invoice_id):
    if not is_db_available():
        flash('Database connection is unavailable.')
        return redirect('/dashboard')

    if 'user' not in session:
        return redirect('/signin')
    
    # Find the booking by invoice ID and user
    booking = db.bookings.find_one({
        "invoice_id": invoice_id,
        "user": session['user']
    })
    
    if not booking:
        flash('Invoice not found or access denied.')
        return redirect('/dashboard')
    
    return render_template('invoice.html', booking=booking)

# Admin
@app.route('/admin')
def admin():
    if not is_db_available():
        flash('Database connection is unavailable. Please try again later.')
        return render_template('index.html')

    all_bookings = list(db.bookings.find())

    # Calculate statistics
    total_bookings = len(all_bookings)
    total_revenue = sum(b.get('total_cost', 0) for b in all_bookings)

    # Event type statistics
    event_stats = {}
    for booking in all_bookings:
        event = booking.get('event', 'Unknown')
        event_stats[event] = event_stats.get(event, 0) + 1

    # Venue statistics
    venue_stats = {}
    for booking in all_bookings:
        venue = booking.get('venue', 'Unknown')
        venue_stats[venue] = venue_stats.get(venue, 0) + 1

    # Time slot statistics
    time_slot_stats = {}
    for booking in all_bookings:
        time_slot = booking.get('time_slot', 'Not Specified')
        time_slot_stats[time_slot] = time_slot_stats.get(time_slot, 0) + 1

    # Monthly revenue (last 6 months)
    monthly_revenue = {}
    six_months_ago = datetime.now() - timedelta(days=180)

    for booking in all_bookings:
        booking_date = booking.get('booking_date')
        if booking_date:
            try:
                # Assuming booking_date is in YYYY-MM-DD format
                date_obj = datetime.strptime(booking_date, '%Y-%m-%d')
                if date_obj >= six_months_ago:
                    month_key = date_obj.strftime('%Y-%m')
                    monthly_revenue[month_key] = monthly_revenue.get(month_key, 0) + booking.get('total_cost', 0)
            except:
                pass

    # Service popularity
    service_stats = {}
    for booking in all_bookings:
        services = booking.get('selected_services', [])
        for service in services:
            service_stats[service] = service_stats.get(service, 0) + 1

    return render_template('admin.html',
                         bookings=all_bookings,
                         total_bookings=total_bookings,
                         total_revenue=total_revenue,
                         event_stats=event_stats,
                         venue_stats=venue_stats,
                         time_slot_stats=time_slot_stats,
                         monthly_revenue=monthly_revenue,
                         service_stats=service_stats)

# Budget Estimation
@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'user' not in session:
        return redirect('/signin')
    
    total_cost = 0
    selected_services = []
    
    if request.method == 'POST':
        # Include venue cost in the total
        venue_cost = request.form.get('venue', 0)
        total_cost += int(venue_cost)

        services = {
            'catering': 500,
            'decoration': 300,
            'photography': 400,
            'dj': 400
        }
        
        for service, cost in services.items():
            if request.form.get(service):
                selected_services.append(service.capitalize())
                total_cost += cost
    
    return render_template('budget.html', total_cost=total_cost, selected_services=selected_services)

# Vendor Selection
@app.route('/vendors', methods=['GET', 'POST'])
def vendors():
    if 'user' not in session:
        return redirect('/signin')
    
    selected_services = []
    
    if request.method == 'POST':
        services = ['catering', 'photography', 'decoration']
        
        for service in services:
            if request.form.get(service):
                selected_services.append(service.capitalize())
    
    # Mock vendor data - in a real app, this would come from database
    vendors_data = {
        'catering': [
            {'name': 'Gourmet Delights', 'rating': 4.8, 'price_range': '$$$', 'specialty': 'Fine Dining'},
            {'name': 'Party Bites', 'rating': 4.5, 'price_range': '$$', 'specialty': 'Finger Foods'},
            {'name': 'Elegant Eats', 'rating': 4.9, 'price_range': '$$$$', 'specialty': 'Gourmet Cuisine'}
        ],
        'photography': [
            {'name': 'Capture Moments', 'rating': 4.7, 'price_range': '$$', 'specialty': 'Event Photography'},
            {'name': 'Lens Masters', 'rating': 4.6, 'price_range': '$$$', 'specialty': 'Professional Shoots'},
            {'name': 'Memory Keepers', 'rating': 4.8, 'price_range': '$$', 'specialty': 'Candid Photography'}
        ],
        'decoration': [
            {'name': 'Dream Decor', 'rating': 4.5, 'price_range': '$$', 'specialty': 'Themed Decorations'},
            {'name': 'Elegant Events', 'rating': 4.7, 'price_range': '$$$', 'specialty': 'Luxury Decor'},
            {'name': 'Party Wizards', 'rating': 4.4, 'price_range': '$', 'specialty': 'Budget-Friendly'}
        ]
    }
    
    return render_template('vendors.html', selected_services=selected_services, vendors_data=vendors_data)

# Event Suggestions
@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    if 'user' not in session:
        return redirect('/signin')
    
    selected_event = None
    suggestions = []
    
    # Event type suggestions mapping
    event_suggestions = {
        'Birthday': [
            {'service': 'Decoration', 'reason': 'Create a festive atmosphere with balloons, banners, and themed decor', 'icon': '🎂'},
            {'service': 'Cake', 'reason': 'Custom birthday cake to make the celebration special', 'icon': '🎈'},
            {'service': 'Photography', 'reason': 'Capture memorable moments with family and friends', 'icon': '📸'}
        ],
        'Wedding': [
            {'service': 'Catering', 'reason': 'Professional catering service for your special day', 'icon': '🍽️'},
            {'service': 'Photography', 'reason': 'Capture your wedding memories professionally', 'icon': '📸'},
            {'service': 'Decoration', 'reason': 'Beautiful floral arrangements and venue styling', 'icon': '💐'},
            {'service': 'DJ', 'reason': 'Music and entertainment for your reception', 'icon': '🎵'}
        ],
        'Concert': [
            {'service': 'DJ', 'reason': 'Professional sound system and music setup', 'icon': '🎵'},
            {'service': 'Photography', 'reason': 'Document the live performance', 'icon': '📸'},
            {'service': 'Catering', 'reason': 'Food and beverages for attendees', 'icon': '🍕'}
        ],
        'Corporate': [
            {'service': 'Catering', 'reason': 'Professional catering for business meetings', 'icon': '🍽️'},
            {'service': 'Decoration', 'reason': 'Professional setup for corporate events', 'icon': '🏢'},
            {'service': 'Photography', 'reason': 'Event documentation and marketing materials', 'icon': '📸'}
        ],
        'Anniversary': [
            {'service': 'Catering', 'reason': 'Romantic dinner or celebration meal', 'icon': '🍽️'},
            {'service': 'Decoration', 'reason': 'Romantic and elegant decor setup', 'icon': '💐'},
            {'service': 'Photography', 'reason': 'Capture your milestone celebration', 'icon': '📸'}
        ],
        'Baby Shower': [
            {'service': 'Decoration', 'reason': 'Themed decorations for the baby shower', 'icon': '👶'},
            {'service': 'Catering', 'reason': 'Delicious food for guests and celebration', 'icon': '🍰'},
            {'service': 'Photography', 'reason': 'Document this special family moment', 'icon': '📸'}
        ],
        'Graduation': [
            {'service': 'Photography', 'reason': 'Capture the graduation ceremony and celebrations', 'icon': '🎓'},
            {'service': 'Catering', 'reason': 'Food for family gatherings and parties', 'icon': '🍽️'},
            {'service': 'Decoration', 'reason': 'Congratulatory banners and decorations', 'icon': '🎈'}
        ],
        'Holiday Party': [
            {'service': 'Decoration', 'reason': 'Festive holiday-themed decorations', 'icon': '🎄'},
            {'service': 'Catering', 'reason': 'Holiday-themed food and beverages', 'icon': '🍗'},
            {'service': 'DJ', 'reason': 'Holiday music and entertainment', 'icon': '🎵'}
        ],
        'Theme Party': [
            {'service': 'Decoration', 'reason': 'Custom decorations matching your theme', 'icon': '🎭'},
            {'service': 'Catering', 'reason': 'Themed food and drinks', 'icon': '🍹'},
            {'service': 'DJ', 'reason': 'Music matching your party theme', 'icon': '🎶'}
        ],
        'Fundraiser': [
            {'service': 'Catering', 'reason': 'Food service for event attendees', 'icon': '🍽️'},
            {'service': 'Decoration', 'reason': 'Professional event setup', 'icon': '🎯'},
            {'service': 'Photography', 'reason': 'Event documentation and promotion', 'icon': '📸'}
        ],
        'Conference': [
            {'service': 'Catering', 'reason': 'Conference catering and refreshments', 'icon': '☕'},
            {'service': 'Decoration', 'reason': 'Professional conference setup', 'icon': '🏢'},
            {'service': 'Photography', 'reason': 'Event documentation', 'icon': '📸'}
        ]
    }
    
    if request.method == 'POST':
        selected_event = request.form.get('event_type')
        if selected_event and selected_event in event_suggestions:
            suggestions = event_suggestions[selected_event]
    
    return render_template('suggestions.html', selected_event=selected_event, suggestions=suggestions, event_types=list(event_suggestions.keys()))

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    # For production deployment, use environment variable
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)