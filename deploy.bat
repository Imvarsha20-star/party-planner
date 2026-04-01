@echo off
echo 🚀 Party Planner Deployment Script for Heroku
echo ==============================================

echo.
echo 📋 Prerequisites Check:
echo - Heroku CLI installed
echo - MongoDB Atlas account created
echo - Git repository initialized
echo.

set /p HEROKU_APP_NAME=Enter your Heroku app name (e.g., my-party-planner):
set /p MONGO_URI=Enter your MongoDB Atlas connection string:
set /p SECRET_KEY=Enter a secret key (or press Enter for auto-generated):

if "%SECRET_KEY%"=="" (
    set SECRET_KEY=%random%%random%%random%%random%
)

echo.
echo 🔧 Setting up Heroku app: %HEROKU_APP_NAME%
heroku create %HEROKU_APP_NAME%

echo.
echo 🔐 Setting environment variables...
heroku config:set MONGO_URI="%MONGO_URI%" --app %HEROKU_APP_NAME%
heroku config:set SECRET_KEY="%SECRET_KEY%" --app %HEROKU_APP_NAME%
heroku config:set FLASK_ENV="production" --app %HEROKU_APP_NAME%

echo.
echo 📦 Deploying to Heroku...
git add .
git commit -m "Deploy to Heroku"
git push heroku main

echo.
echo 🎉 Deployment complete!
echo 🌐 Your app is live at: https://%HEROKU_APP_NAME%.herokuapp.com
echo.
echo 📱 Access from any device with internet connection!
echo.

pause