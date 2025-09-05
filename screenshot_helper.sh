#!/bin/bash
# SNAKEIUM Screenshot Setup Script
# Helps you add the gameplay screenshot to the repository

echo ""
echo "==============================================="
echo "🐍 SNAKEIUM Screenshot Setup"
echo "==============================================="
echo ""
echo "To add your gameplay screenshot:"
echo ""
echo "1. Take a screenshot of the game running"
echo "   (or use the one you shared earlier)"
echo ""
echo "2. Save it as 'screenshot.png'"
echo ""
echo "3. Copy it to the assets folder:"
echo "   cp /path/to/screenshot.png $(pwd)/assets/screenshot.png"
echo ""
echo "4. Commit and push:"
echo "   git add assets/screenshot.png"
echo "   git commit -m 'Add gameplay screenshot'"
echo "   git push origin main"
echo ""
echo "5. Check GitHub README - screenshot will appear automatically!"
echo ""
echo "Current assets directory: $(pwd)/assets/"
echo ""

# Check if screenshot exists
if [ -f "assets/screenshot.png" ]; then
    echo "✅ Screenshot already exists!"
    echo "   File size: $(du -h assets/screenshot.png | cut -f1)"
else
    echo "❌ Screenshot not found"
    echo "   Needed: assets/screenshot.png"
fi

echo ""
echo "GitHub will display it at:"
echo "https://raw.githubusercontent.com/chousemp3/SNAKEIUM/main/assets/screenshot.png"
echo ""
