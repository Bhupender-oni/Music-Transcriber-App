#!/bin/bash
# Build script for Music Transcriber Desktop App

set -e

echo "🔨 Building Music Transcriber Desktop App..."

# Platform detection
PLATFORM=$(uname -s)

case $PLATFORM in
    Darwin)
        echo "📱 Building for macOS..."
        cd desktop
        npm install
        npm run build:macos
        echo "✅ macOS app built: dist/MusicTranscriber.dmg"
        ;;
    Linux)
        echo "🐧 Building for Linux..."
        cd desktop
        npm install
        npm run build:linux
        echo "✅ Linux app built: dist/MusicTranscriber.AppImage"
        ;;
    MINGW64_NT*|MSYS_NT*)
        echo "🪟 Building for Windows..."
        cd desktop
        npm install
        npm run build:windows
        echo "✅ Windows app built: dist/MusicTranscriber-Setup.exe"
        ;;
    *)
        echo "❌ Unsupported platform: $PLATFORM"
        exit 1
        ;;
esac

echo "✅ Build complete!"
