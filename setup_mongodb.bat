@echo off
echo 🌍 MongoDB Atlas Setup Guide
echo =============================
echo.
echo Your Party Planner app needs a cloud database.
echo MongoDB Atlas provides a FREE cloud database.
echo.
echo 📋 Follow these steps:
echo.
echo 1. Go to: https://cloud.mongodb.com
echo 2. Click "Try Free"
echo 3. Create account with email
echo 4. Choose "M0 Cluster" (FREE)
echo 5. Select your cloud provider and region
echo 6. Create cluster (takes 1-3 minutes)
echo.
echo 🔐 Database User Setup:
echo - Go to "Database Access" → "Add New Database User"
echo - Username: partyuser
echo - Password: [choose strong password]
echo - Built-in Role: Read and write to any database
echo.
echo 🌐 Network Access:
echo - Go to "Network Access" → "Add IP Address"
echo - Choose "Allow Access from Anywhere" (0.0.0.0/0)
echo.
echo 🔗 Get Connection String:
echo - Go to "Clusters" → "Connect"
echo - Choose "Connect your application"
echo - Copy the connection string
echo - It looks like: mongodb+srv://partyuser:password@cluster0.xxxxx.mongodb.net/
echo.
echo 📝 Save your connection string - you'll need it for deployment!
echo.
echo ✅ Once you have the connection string, proceed to deploy on Render/Railway/PythonAnywhere
echo.
pause