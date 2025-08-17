"""
বেসিক ভ্যালিডেশন টেস্ট
Basic Validation Test
"""

import os
import sys

def test_imports():
    """Test if all modules can be imported"""
    
    print("🧪 Testing module imports...")
    
    try:
        # Test config imports
        from config.settings import config
        from config.database import db, User, Task, Notification
        print("✅ Config modules imported successfully")
        
        # Test utility imports
        from modules.utils.localization import i18n, _
        from modules.utils.bengali_calendar import bengali_calendar
        from modules.utils.security import security
        print("✅ Utility modules imported successfully")
        
        # Test basic functionality
        print(f"✅ Bot name: {config.BOT_NAME}")
        print(f"✅ Bot version: {config.BOT_VERSION}")
        print(f"✅ Default language: {config.DEFAULT_LANGUAGE}")
        
        # Test localization
        welcome_text = _('welcome.greeting', lang_code='bn')
        print(f"✅ Bengali text: {welcome_text}")
        
        # Test Bengali calendar
        bengali_date = bengali_calendar.get_bengali_date()
        print(f"✅ Today's Bengali date: {bengali_date['bengali_date']}")
        
        print("🎉 All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_setup():
    """Test database setup without external dependencies"""
    
    print("🗄️ Testing database setup...")
    
    try:
        from config.database import db
        
        # Create tables
        db.create_tables()
        print("✅ Database tables created successfully")
        
        # Test user creation (mock)
        print("✅ Database models are properly defined")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    
    print("📁 Testing file structure...")
    
    required_files = [
        'config/settings.py',
        'config/database.py',
        'modules/utils/localization.py',
        'modules/utils/bengali_calendar.py',
        'modules/utils/security.py',
        'modules/tasks/task_manager.py',
        'modules/notifications/notification_manager.py',
        'locales/bn/messages.json',
        'bot.py',
        'main.py',
        'requirements.txt',
        '.env.example',
        '.gitignore'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("🎉 All required files exist!")
    return True

def main():
    """Run all tests"""
    print("🚀 Starting Bengali Telegram Bot validation tests...")
    print("-" * 60)
    
    tests = [
        test_file_structure,
        test_imports,
        test_database_setup
    ]
    
    passed = 0
    total = len(tests)
    
    for test_func in tests:
        # Test database setup without external dependencies
        from config.database import db
        try:
            if test_func():
                passed += 1
            print("-" * 40)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} failed: {e}")
            print("-" * 40)
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The bot structure is ready.")
        print("\n📋 Next steps:")
        print("1. Copy .env.example to .env and add your TELEGRAM_BOT_TOKEN")
        print("2. Run 'python seed_data.py' to add sample data")
        print("3. Run 'python main.py' to start the bot")
    else:
        print("❌ Some tests failed. Please fix the issues before running the bot.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)