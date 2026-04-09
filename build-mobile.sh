#!/bin/bash
# Build script for Music Transcriber Mobile App

set -e

echo "📱 Building Music Transcriber Mobile App..."

cd mobile

# Platform detection
if [ "$1" == "android" ]; then
    echo "🤖 Building for Android..."
    npm install
    npx react-native run-android
    echo "✅ Android build complete"
    
elif [ "$1" == "ios" ]; then
    echo "🍎 Building for iOS..."
    npm install
    cd ios
    pod install
    cd ..
    npx react-native run-ios
    echo "✅ iOS build complete"
    
elif [ "$1" == "release-android" ]; then
    echo "🤖 Building Android Release APK..."
    npm install
    npm run build:android
    echo "✅ APK ready: android/app/build/outputs/apk/release/app-release.apk"
    
elif [ "$1" == "release-ios" ]; then
    echo "🍎 Building iOS Release..."
    npm install
    npm run build:ios
    echo "✅ iOS build complete"
    
else
    echo "Usage: ./build-mobile.sh [android|ios|release-android|release-ios]"
    exit 1
fi

echo "✅ Mobile build complete!"
