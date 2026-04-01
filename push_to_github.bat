@echo off
echo 🚀 GitHub Update Script for Party Planner
echo =========================================
echo.
echo This script will commit all changes and push to GitHub
echo.

set /p COMMIT_MESSAGE=Enter commit message (or press Enter for default):

if "%COMMIT_MESSAGE%"=="" (
    set COMMIT_MESSAGE=Add deployment features and cloud-ready configuration
)

echo.
echo 📋 Current status:
git status --short

echo.
echo 🔄 Adding all files...
git add .

echo.
echo 💾 Committing changes...
git commit -m "%COMMIT_MESSAGE%"

echo.
echo 📤 Pushing to GitHub...
git push origin main

echo.
echo ✅ Successfully updated GitHub repository!
echo.
echo 🌐 Your GitHub repository: https://github.com/Varsha1725/party-planner
echo.
echo 📱 Ready for deployment to Render/Railway/PythonAnywhere!
echo.
pause