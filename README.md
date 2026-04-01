# 🎉 Party Planner Application

A comprehensive event planning and booking web application built with Flask and MongoDB.

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (3.11 recommended)
- **MongoDB** running on `localhost:27017`
- **Windows/Linux/Mac** operating system

### Installation & Setup

1. **Download/Extract** the project to your desired location

2. **Run the Application** (Simplest method):
   ```bash
   # Double-click this file or run in command prompt:
   run.bat
   ```

   The script will automatically:
   - ✅ Check Python installation
   - ✅ Create virtual environment
   - ✅ Install all dependencies
   - ✅ Check MongoDB connection
   - ✅ Start the application

3. **Access the Application**:
   Open your browser and go to: **http://127.0.0.1:5000**

### Manual Setup (Alternative)

If you prefer manual setup:

```bash
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py
```

## 📋 Features

### 🎯 Core Features
- **User Authentication** - Secure registration/login with password validation
- **Event Booking** - Book events with venue, date, and time slot selection
- **Service Add-ons** - Catering, Decoration, Photography, DJ services
- **Smart Suggestions** - AI-powered event recommendations
- **Budget Calculator** - Real-time cost estimation
- **Vendor Directory** - Browse and select service providers

### 💼 Business Features
- **Invoice Generation** - Professional receipts with unique IDs
- **Admin Dashboard** - Analytics with interactive charts
- **Revenue Tracking** - Monthly performance monitoring
- **Booking Management** - Complete reservation system

### 🎨 User Experience
- **Responsive Design** - Works on all devices
- **Glassmorphism UI** - Modern, beautiful interface
- **Real-time Validation** - Instant feedback on forms
- **Professional Invoices** - Print-ready receipts

## 🏗️ Project Structure

```
party planner/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── run.bat               # Windows run script
├── instance/             # Flask instance folder
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── budget.html
│   ├── vendors.html
│   ├── suggestions.html
│   ├── invoice.html
│   └── admin.html
├── static/               # CSS, JS, images
│   └── style.css
└── Party_planner/        # Legacy folder (can be removed)
```

## 🗄️ Database Setup

### MongoDB Installation

1. **Download MongoDB Community Edition**:
   - Visit: https://www.mongodb.com/try/download/community
   - Choose your operating system
   - Follow installation instructions

2. **Start MongoDB**:
   ```bash
   # Windows (as service)
   net start MongoDB

   # Or run manually:
   "C:\Program Files\MongoDB\Server\X.X\bin\mongod.exe"
   ```

3. **Verify Connection**:
   The application will automatically connect to `mongodb://localhost:27017`

## � **Deploy to Cloud (Access from Anywhere)**

### **Option 1: Heroku (Recommended - Free & Easy)**

#### **Step 1: Set up MongoDB Atlas (Cloud Database)**
1. Go to [MongoDB Atlas](https://cloud.mongodb.com) and create a free account
2. Create a new cluster (free tier)
3. Create a database user and get your connection string
4. Whitelist IP address `0.0.0.0/0` for global access
5. Copy your connection string (format: `mongodb+srv://user:pass@cluster.mongodb.net/dbname`)

#### **Step 2: Deploy to Heroku**
1. **Install Heroku CLI**: Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
2. **Login to Heroku**:
   ```bash
   heroku login
   ```
3. **Create Heroku App**:
   ```bash
   heroku create your-party-planner-app
   ```
4. **Set Environment Variables**:
   ```bash
   heroku config:set MONGO_URI="your_mongodb_atlas_connection_string"
   heroku config:set SECRET_KEY="your_super_secret_random_key"
   heroku config:set FLASK_ENV="production"
   ```
5. **Deploy**:
   ```bash
   git init
   git add .
   git commit -m "Initial deployment"
   git push heroku main
   ```
6. **Open Your App**:
   ```bash
   heroku open
   ```

### **Option 2: Render (Alternative Free Option)**

1. Go to [render.com](https://render.com) and create account
2. Connect your GitHub repository
3. Create a new **Web Service**
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `gunicorn app:app`
6. Add environment variables (MONGO_URI, SECRET_KEY, FLASK_ENV)
7. Deploy!

### **Option 3: Railway**

1. Go to [railway.app](https://railway.app) and create account
2. Create new project from GitHub
3. Railway will auto-detect Flask app
4. Add environment variables
5. Deploy automatically

## 📱 **Mobile Access**

Once deployed, your app will be accessible from:
- ✅ **Desktop computers**
- ✅ **Tablets**
- ✅ **Smartphones** (iOS/Android)
- ✅ **Any device with internet**

**Your app URL will be something like:**
- Heroku: `https://your-party-planner-app.herokuapp.com`
- Render: `https://your-app.onrender.com`
- Railway: `https://your-app.up.railway.app`

## 🔧 **Local Development with Cloud Database**

To test with your cloud database locally:

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your MongoDB Atlas connection string

3. **Run locally**:
   ```bash
   python app.py
   ```

## ⚙️ **Environment Variables Required**

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGO_URI` | MongoDB Atlas connection string | `mongodb+srv://user:pass@cluster.mongodb.net/db` |
| `SECRET_KEY` | Random secret key for sessions | `your_super_secret_key_here` |
| `FLASK_ENV` | Environment (production/development) | `production` |

## 🚀 **Quick Deploy Script**

For Heroku users, I've included all necessary files:
- ✅ `Procfile` - Heroku deployment config
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - Updated with production dependencies
- ✅ `deploy.bat` - **One-click deployment script for Windows**
- ✅ Environment variable support

**One-Click Windows Deployment:**
```bash
# Just run this script - it will guide you through everything!
deploy.bat
```

**Your app is now cloud-ready! 🎉**

## �🎮 How to Use

1. **Register** a new account (use strong password with uppercase, lowercase, numbers, symbols)
2. **Login** to access the dashboard
3. **Book Events**:
   - Select event type (Birthday, Wedding, etc.)
   - Choose venue and date
   - Pick time slot (Morning/Afternoon/Evening)
   - Add services (optional)
4. **Explore Features**:
   - Budget calculator
   - Vendor selection
   - Smart suggestions
5. **View Invoices** - Professional receipts for all bookings
6. **Admin Access** - Visit `/admin` for analytics dashboard

## 🔧 Troubleshooting

### "MongoDB connection failed"
- Ensure MongoDB is installed and running
- Check if port 27017 is available
- Try restarting MongoDB service

### "Python not found"
- Install Python 3.8+ from https://python.org
- Make sure Python is added to PATH

### "Permission denied" on Windows
- Run command prompt as Administrator
- Or use the `run.bat` script which handles permissions

### Application won't start
- Check if port 5000 is available
- Try `python -c "from app import app; app.run(port=5001)"` for different port

## 📊 Admin Features

Access the admin dashboard at `/admin` to view:
- 📈 **Interactive Charts** - Event types, venue usage, time slots
- 💰 **Revenue Analytics** - Monthly performance tracking
- 📋 **Booking Management** - All user reservations
- 📊 **Service Popularity** - Demand forecasting

## 🛠️ Development

### Adding New Features
1. Add routes in `app.py`
2. Create templates in `templates/` folder
3. Add styles in `static/style.css`
4. Update admin analytics if needed

### Database Schema
- **users**: User accounts with authentication
- **bookings**: Event reservations with all details

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Ensure all prerequisites are installed
3. Try the `run.bat` script for automated setup

---

**Happy Event Planning! 🎉**

---

## 🚀 **FREE DEPLOYMENT OPTIONS (Access from Anywhere!)**

### **🎯 TOP RECOMMENDATION: Render (Easiest & Most Reliable)**

#### **One-Click Windows Deployment:**
```bash
# Run these scripts in order:
setup_mongodb.bat    # Set up free cloud database
deploy_render.bat    # Deploy to Render
```

#### **Manual Render Setup:**
1. **MongoDB Atlas**: [cloud.mongodb.com](https://cloud.mongodb.com) (free)
2. **GitHub repo**: Create and push your code
3. **Render**: [render.com](https://render.com) → New Web Service
4. **Connect GitHub** → Configure Python app → Deploy!

### **🚂 Alternative: Railway (Super Quick)**

#### **One-Click Windows Deployment:**
```bash
setup_mongodb.bat    # Set up free cloud database
deploy_railway.bat   # Deploy to Railway
```

#### **Manual Railway Setup:**
1. **Railway**: [railway.app](https://railway.app) → New Project
2. **Connect GitHub** → Auto-detects Flask → Deploy!

### **🐍 Alternative: PythonAnywhere (No Git Required)**

1. **PythonAnywhere**: [pythonanywhere.com](https://pythonanywhere.com)
2. **Upload files** via web interface
3. **Create web app** → Configure → Go live!

## 📱 **Mobile Access Ready**

Once deployed, your Party Planner works on:
- ✅ **iPhones & Android phones**
- ✅ **Tablets**
- ✅ **Any device with internet**

**All platforms are 100% FREE - No credit card required! 🎉**

---

## 🔄 **Push to GitHub**

### **Complete GitHub Setup (3 Steps):**

#### **Step 1: Create GitHub Repository**
```bash
# Run this script for step-by-step instructions:
create_github_repo.bat
```

#### **Step 2: Push Your Code**
```bash
# After creating repository, run:
final_push.bat
```

#### **Step 3: Deploy to Cloud**
```bash
# Choose your platform:
setup_mongodb.bat    # Set up free database
deploy_render.bat    # Deploy to Render (recommended)
# OR
deploy_railway.bat   # Deploy to Railway
```

### **Manual Git Commands (Alternative):**
```bash
# 1. Create repository on GitHub.com
# 2. Set remote URL:
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
# 3. Push:
git push -u origin main
```

### **Your GitHub Repository:**
**https://github.com/Varsha1725/party-planner**

*All deployment-ready features are committed locally and ready for GitHub! 🚀*