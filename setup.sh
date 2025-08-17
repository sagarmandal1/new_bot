#!/bin/bash
# Bengali Telegram Bot - Quick Setup Script
# বাংলা টেলিগ্রাম বট - দ্রুত সেটআপ স্ক্রিপ্ট

echo "🇧🇩 বাংলা সহায়ক বট সেটআপ শুরু করা হচ্ছে..."
echo "🇧🇩 Bengali Assistant Bot Setup Starting..."
echo "============================================"

# Check Python version
echo "🐍 Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "   Found: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment file
if [ ! -f .env ]; then
    echo "⚙️ Creating environment configuration..."
    cp .env.example .env
    echo "   ✅ .env file created from template"
    echo "   ⚠️  Please edit .env file and add your TELEGRAM_BOT_TOKEN"
else
    echo "   ✅ .env file already exists"
fi

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p logs uploads static/temp

# Run validation tests
echo "🧪 Running validation tests..."
python test_setup.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 সেটআপ সম্পন্ন! Setup Complete!"
    echo "==============================================="
    echo ""
    echo "📋 পরবর্তী ধাপসমূহ (Next Steps):"
    echo "1. .env ফাইলে আপনার TELEGRAM_BOT_TOKEN যোগ করুন"
    echo "   Add your TELEGRAM_BOT_TOKEN to .env file"
    echo ""
    echo "2. সেম্পল ডেটা যোগ করুন:"
    echo "   python seed_data.py"
    echo ""
    echo "3. বট চালু করুন:"
    echo "   python main.py"
    echo ""
    echo "📖 সম্পূর্ণ গাইডের জন্য README.md দেখুন"
    echo "   See README.md for complete guide"
    echo ""
else
    echo "❌ Setup failed. Please check the errors above."
    exit 1
fi