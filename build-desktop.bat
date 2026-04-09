@echo off
REM Build script for Music Transcriber Desktop App (Windows)

echo.
echo 🔨 Building Music Transcriber Desktop App for Windows...
echo.

REM Check if Node.js is installed
where npm >nul 2>nul
if errorlevel 1 (
    echo ❌ Node.js/npm not found. Install from https://nodejs.org/
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python not found. Install from https://python.org/
    exit /b 1
)

echo ✅ Prerequisites found

cd desktop

echo.
echo 📦 Installing dependencies...
call npm install

echo.
echo 🏗️ Building Windows installer...
call npm run build:windows

echo.
echo ✅ Build complete!
echo 📦 Installer location: .\dist\MusicTranscriber-Setup.exe
echo.
pause
