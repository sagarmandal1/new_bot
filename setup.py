#!/usr/bin/env python3
"""
Setup script for Daily Routine Bot
দৈনিক রুটিন বট সেটআপ স্ক্রিপ্ট
"""

import json
import os
import sys

def setup_bot():
    """Setup bot configuration"""
    print("🤖 দৈনিক রুটিন বট সেটআপ | Daily Routine Bot Setup")
    print("=" * 50)
    
    # Check if config exists
    if os.path.exists('config.json'):
        print("⚠️  config.json already exists. Do you want to recreate it? (y/n): ", end="")
        if input().lower() != 'y':
            print("✅ Setup cancelled.")
            return
    
    print("\n📝 Please provide the following information:")
    
    # Get bot token
    bot_token = input("🔑 Bot Token (from @BotFather): ").strip()
    if not bot_token:
        print("❌ Bot token is required!")
        return
    
    # Get admin user ID
    admin_id = input("👤 Admin User ID (your Telegram user ID): ").strip()
    try:
        admin_id = int(admin_id)
    except ValueError:
        print("❌ Admin ID must be a number!")
        return
    
    # Create config
    config = {
        "bot_token": bot_token,
        "admin_user_ids": [admin_id],
        "timezone": "Asia/Dhaka",
        "backup_interval_hours": 24,
        "reminder_check_interval_minutes": 5,
        "default_language": "bengali",
        "supported_languages": ["bengali", "english"]
    }
    
    # Save config
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Configuration saved to config.json")
    print(f"🔧 Admin ID: {admin_id}")
    print(f"🌍 Timezone: Asia/Dhaka")
    
    # Create data directories
    os.makedirs('data/backups', exist_ok=True)
    print("📁 Data directories created")
    
    print("\n🚀 Setup completed! You can now run the bot:")
    print("   python main.py")
    print("\n📖 For more information, check README.md")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'telegram',
        'apscheduler',
        'pytz'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them with: pip install -r requirements.txt")
        return False
    
    return True

if __name__ == "__main__":
    print("🔍 Checking dependencies...")
    if check_dependencies():
        print("✅ All dependencies are installed")
        setup_bot()
    else:
        sys.exit(1)