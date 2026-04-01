@echo off
echo 🚀 Render Deployment Script for Party Planner
echo =============================================
echo.
echo This script will help you deploy to Render (FREE platform)
echo.
echo 📋 Prerequisites:
echo - MongoDB Atlas account and connection string
echo - GitHub repository created and pushed
echo.

set /p GITHUB_REPO=Enter your GitHub repository URL (e.g., https://github.com/username/party-planner):
set /p MONGO_URI=Enter your MongoDB Atlas connection string:
set /p SECRET_KEY=Enter a secret key (press Enter for auto-generated):

if "%SECRET_KEY%"=="" (
    set SECRET_KEY=%random%%random%%random%%random%%random%
)

echo.
echo 🌐 Opening Render deployment page...
echo.
echo 📝 Deployment Checklist:
echo 1. Sign up/login to https://render.com
echo 2. Click "New" → "Web Service"
echo 3. Connect your GitHub repository: %GITHUB_REPO%
echo 4. Configure the following settings:
echo.
echo    Environment: Python
echo    Build Command: pip install -r requirements.txt
echo    Start Command: gunicorn app:app
echo.
echo 5. Add Environment Variables:
echo    MONGO_URI = %MONGO_URI%
echo    SECRET_KEY = %SECRET_KEY%
echo    FLASK_ENV = production
echo    PYTHON_VERSION = 3.11.5
echo.
echo 6. Click "Create Web Service"
echo.
echo ⏱️ Deployment takes 2-3 minutes...
echo.
echo 🎉 Your app will be live at: https://your-app-name.onrender.com
echo.
echo 📱 Test on mobile: Open the URL on your phone!
echo.
echo 📋 Your deployment details:
echo Repository: %GITHUB_REPO%
echo MongoDB: Connected
echo Secret Key: %SECRET_KEY%
echo.
echo 💡 Need help? Check DEPLOY_FREE.md for detailed instructions
echo.
pause