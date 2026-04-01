@echo off
echo 🚂 Railway Deployment Script for Party Planner
echo ==============================================
echo.
echo This script will help you deploy to Railway (FREE platform)
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
echo 🌐 Opening Railway deployment page...
echo.
echo 📝 Deployment Checklist:
echo 1. Sign up/login to https://railway.app
echo 2. Click "New Project" → "Deploy from GitHub repo"
echo 3. Connect your GitHub repository: %GITHUB_REPO%
echo 4. Railway will auto-detect your Flask app
echo.
echo 5. Add Environment Variables in Railway dashboard:
echo    MONGO_URI = %MONGO_URI%
echo    SECRET_KEY = %SECRET_KEY%
echo    FLASK_ENV = production
echo.
echo 6. Click "Deploy"
echo.
echo ⏱️ Deployment takes 1-2 minutes...
echo.
echo 🎉 Your app will be live at: https://your-app-name.up.railway.app
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