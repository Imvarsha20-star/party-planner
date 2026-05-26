@echo off
echo 🚀 Final GitHub Push Script
echo ===========================
echo.
echo This script pushes your committed changes to GitHub
echo Make sure you've created the GitHub repository first!
echo.

set REPO_URL=https://github.com/Imvarsha20-star/party-planner.git

if "%REPO_URL%"=="" (
    echo ❌ No repository URL provided!
    echo Please create a GitHub repository first.
    echo Run: create_github_repo.bat
    pause
    exit /b 1
)

echo.
echo 🔧 Setting remote URL...
git remote add origin "%REPO_URL%" 2>nul || git remote set-url origin "%REPO_URL%"
git branch -M main

echo.
echo 📤 Pushing to GitHub...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS! Your Party Planner is now on GitHub!
    echo 🌐 Repository: %REPO_URL%
    echo.
    echo 🚀 Ready for deployment! Run one of these:
    echo   setup_mongodb.bat     (set up database)
    echo   deploy_render.bat     (deploy to Render)
    echo   deploy_railway.bat    (deploy to Railway)
    echo.
) else (
    echo.
    echo ❌ Push failed! Please check:
    echo - Repository URL is correct
    echo - Repository exists on GitHub
    echo - You have push permissions
    echo.
)

pause