#!/bin/bash
# Quick script to add the gameplay screenshot to SNAKEIUM repository

echo "SNAKEIUM Screenshot Setup"
echo "========================"
echo ""
echo "To add your gameplay screenshot:"
echo ""
echo "1. Save your game screenshot as 'screenshot.png'"
echo "2. Copy it to: $(pwd)/assets/screenshot.png"
echo ""
echo "Commands:"
echo "  cp /path/to/your/screenshot.png assets/screenshot.png"
echo "  git add assets/screenshot.png"
echo "  git commit -m 'Add gameplay screenshot'"
echo "  git push origin main"
echo ""
echo "The README will automatically display the screenshot on GitHub!"
