@echo off
echo ===========================================
echo    PARTY PLANNER APPLICATION
echo ===========================================
echo.

echo Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Checking virtual environment...
if not exist ".venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Checking MongoDB connection...
python -c "import os; import certifi; from dotenv import load_dotenv; from pymongo import MongoClient; load_dotenv(); uri = os.getenv('MONGO_URI', 'mongodb+srv://172005varshar_db_user:IA8nFP6NdYqTRmFI@cluster0.q8mdk0p.mongodb.net/?appName=Cluster0'); client = MongoClient(uri, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where()); client.admin.command('ping'); print('✅ Successfully connected to MongoDB Atlas')"
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  WARNING: Database connection failed.
    echo If using Atlas, check your MONGO_URI in the .env file.
    echo If using local, ensure MongoDB is running on localhost:27017.
    echo You can download MongoDB from: https://www.mongodb.com/try/download/community
    echo.
    echo Continuing anyway...
)

echo.
echo ===========================================
echo    STARTING PARTY PLANNER APPLICATION
echo ===========================================
echo.
echo Application will be available at:
echo http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the application
echo ===========================================

python app.py