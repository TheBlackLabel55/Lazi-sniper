#!/bin/bash
# Script to push Lazada Sniper Bot to GitHub
# Repository: https://github.com/TheBlackLabel55/Lazi-sniper

echo "========================================"
echo " PUSH TO GITHUB - Lazi-sniper"
echo "========================================"
echo ""
echo "Repository: https://github.com/TheBlackLabel55/Lazi-sniper"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed!"
    echo ""
    echo "Please install Git:"
    echo "  - Mac: brew install git"
    echo "  - Linux: sudo apt-get install git"
    echo ""
    exit 1
fi

echo "Step 1: Initializing git repository..."
git init

echo ""
echo "Step 2: Adding all files..."
git add .

echo ""
echo "Step 3: Creating initial commit..."
git commit -m "Initial commit: Lazada Sniper Bot with Store Monitor"

echo ""
echo "Step 4: Setting up remote repository..."
git branch -M main
git remote remove origin 2>/dev/null
git remote add origin https://github.com/TheBlackLabel55/Lazi-sniper.git

echo ""
echo "Step 5: Pushing to GitHub..."
echo ""
echo "NOTE: You may be asked to sign in to GitHub"
echo ""
git push -u origin main

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo " PUSH FAILED"
    echo "========================================"
    echo ""
    echo "Possible reasons:"
    echo "  1. Need to authenticate with GitHub"
    echo "  2. No internet connection"
    echo "  3. Repository doesn't exist"
    echo ""
    echo "Try running this command manually:"
    echo "  git push -u origin main"
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo " SUCCESS!"
echo "========================================"
echo ""
echo "Your code has been uploaded to:"
echo "https://github.com/TheBlackLabel55/Lazi-sniper"
echo ""
echo "You can now:"
echo "  - View it on GitHub"
echo "  - Clone it on other devices"
echo "  - Share it with others"
echo ""

