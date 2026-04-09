@echo off
REM Build script for Music Transcriber Mobile App (Windows)

echo.
echo 📱 Building Music Transcriber Mobile App...
echo.

REM Check if Node.js is installed
where npm >nul 2>nul
if errorlevel 1 (
    echo ❌ Node.js/npm not found. Install from https://nodejs.org/
    exit /b 1
)

cd mobile

if "%1"=="android" (
    echo 🤖 Building for Android...
    call npm install
    call npx react-native run-android
    echo ✅ Android build complete
    
) else if "%1"=="release-android" (
    echo 🤖 Building Android Release APK...
    call npm install
    call npm run build:android
    echo ✅ APK ready: android\app\build\outputs\apk\release\app-release.apk
    
) else (
    echo Usage: build-mobile.bat [android|release-android]
    echo.
    echo Note: iOS build requires macOS
    exit /b 1
)

echo.
echo ✅ Mobile build complete!
echo.
pause
