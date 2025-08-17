"""
বাংলা বট ডেমো স্ক্রিপ্ট
Bengali Bot Demo Script

এই স্ক্রিপ্ট বটের মূল বৈশিষ্ট্যগুলি প্রদর্শন করে
This script demonstrates the main features of the bot
"""

import asyncio
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.database import db
from modules.utils.localization import i18n, _
from modules.utils.bengali_calendar import bengali_calendar
from modules.utils.security import security

# Try to import task managers, use mocks if not available
try:
    from modules.tasks.task_manager import TaskManager
    from modules.notifications.notification_manager import NotificationManager
    from modules.gamification.game_manager import GameManager
    FULL_FEATURES = True
except ImportError:
    # Mock managers for demo
    class MockTaskManager:
        async def create_task(self, *args, **kwargs): return None
        async def get_user_tasks(self, *args, **kwargs): return []
        async def get_task_statistics(self, *args, **kwargs): 
            return {'total_tasks': 3, 'completed_tasks': 1, 'pending_tasks': 2, 'overdue_tasks': 0, 'completion_rate': 33.33}
    
    class MockNotificationManager:
        async def get_daily_motivational_quote(self, lang): return "💪 সফলতা আসে ধৈর্য এবং কঠিন পরিশ্রমের মাধ্যমে।"
        async def generate_daily_summary(self, user_id): return "📊 আজকের সারসংক্ষেপ: আপনার ৫টি টাস্কের মধ্যে ৩টি সম্পন্ন হয়েছে!"
    
    class MockGameManager:
        async def get_daily_quiz(self): 
            return {
                'question': 'বাংলাদেশের রাজধানীর নাম কী?',
                'options': ['ঢাকা', 'চট্টগ্রাম', 'সিলেট', 'খুলনা'],
                'correct': 0,
                'points': 10
            }
        async def get_leaderboard(self): 
            return [
                {'rank': 1, 'name': 'রহিম উদ্দিন', 'points': 500, 'level': 5},
                {'rank': 2, 'name': 'ফাতিমা খাতুন', 'points': 450, 'level': 4},
                {'rank': 3, 'name': 'করিম উল্লাহ', 'points': 400, 'level': 4}
            ]
    
    TaskManager = MockTaskManager
    NotificationManager = MockNotificationManager
    GameManager = MockGameManager
    FULL_FEATURES = False
    print("⚠️ Using mock managers for demo (install dependencies for full features)")

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"🇧🇩 {title}")
    print("="*60)

def demo_localization():
    """Demonstrate Bengali localization"""
    print_header("বাংলা ভাষা সাপোর্ট ডেমো (Bengali Language Support Demo)")
    
    # Show welcome message
    welcome = _('welcome.greeting', lang_code='bn')
    print(f"স্বাগত বার্তা: {welcome}")
    
    # Show various menu items
    print("\nমেনু আইটেমসমূহ:")
    menus = ['tasks', 'calendar', 'profile', 'notifications', 'games', 'help']
    for menu in menus:
        text = _(f'menus.main_menu.{menu}', lang_code='bn')
        print(f"  • {text}")
    
    # Show task priorities
    print("\nটাস্ক অগ্রাধিকার:")
    priorities = ['low', 'medium', 'high', 'urgent']
    for priority in priorities:
        text = _(f'tasks.priority.{priority}', lang_code='bn')
        print(f"  • {text}")

def demo_bengali_calendar():
    """Demonstrate Bengali calendar features"""
    print_header("বাংলা ক্যালেন্ডার ডেমো (Bengali Calendar Demo)")
    
    # Get current Bengali date
    date_info = bengali_calendar.get_bengali_date()
    
    print(f"🗓️  আজকের বাংলা তারিখ: {date_info['bengali_date']}")
    print(f"📆  ইংরেজি তারিখ: {date_info['english_date']}")  
    print(f"📅  বার: {date_info['bengali_weekday']}")
    print(f"🌸  ঋতু: {date_info['season']}")
    print(f"⏰  সময়: {date_info['english_time']}")
    
    # Show upcoming events
    events = bengali_calendar.get_upcoming_events()
    if events:
        print("\n🎉 আসন্ন অনুষ্ঠানসমূহ:")
        for event in events:
            print(f"  • {event['name']} - {event['bengali_date']}")

def demo_security():
    """Demonstrate security features"""  
    print_header("নিরাপত্তা বৈশিষ্ট্য ডেমো (Security Features Demo)")
    
    # Test encryption
    original_text = "এটি একটি গুরুত্বপূর্ণ বার্তা"
    encrypted = security.encrypt_data(original_text)
    decrypted = security.decrypt_data(encrypted)
    
    print(f"মূল টেক্সট: {original_text}")
    print(f"এনক্রিপ্টেড: {encrypted[:50]}...")
    print(f"ডিক্রিপ্টেড: {decrypted}")
    print(f"✅ এনক্রিপশন {'সফল' if original_text == decrypted else 'ব্যর্থ'}")
    
    # Test password hashing
    password = "my_secure_password"
    hashed = security.hash_password(password)
    verified = security.verify_password(password, hashed)
    
    print(f"\nপাসওয়ার্ড: {password}")
    print(f"হ্যাশ: {hashed[:50]}...")
    print(f"✅ ভেরিফিকেশন {'সফল' if verified else 'ব্যর্থ'}")
    
    # Test token generation
    token = security.generate_secure_token(16)
    print(f"\nসিকিউর টোকেন: {token}")

async def demo_task_management():
    """Demonstrate task management"""
    print_header("টাস্ক ম্যানেজমেন্ট ডেমো (Task Management Demo)")
    
    task_manager = TaskManager()
    
    # Create sample tasks
    print("📝 নমুনা টাস্ক তৈরি করা হচ্ছে...")
    
    sample_tasks = [
        {
            'title': 'বই পড়া',
            'description': 'গীতা পড়া শুরু করা',
            'priority': 'high',
            'category': 'education'
        },
        {
            'title': 'দুধ কিনতে হবে', 
            'description': 'বাজার থেকে দুধ কিনে আনা',
            'priority': 'medium',
            'category': 'shopping'
        },
        {
            'title': 'ডাক্তারের কাছে যাওয়া',
            'description': 'মাসিক চেকআপ',
            'priority': 'urgent', 
            'category': 'health'
        }
    ]
    
    user_id = 123456789  # Mock user ID
    created_tasks = []
    
    for task_data in sample_tasks:
        # In a real scenario, this would create in database
        print(f"  ✅ {task_data['title']} - {_('tasks.priority.' + task_data['priority'], lang_code='bn')}")
        created_tasks.append(task_data)
    
    # Show statistics
    stats = {
        'total_tasks': len(created_tasks),
        'completed_tasks': 1,
        'pending_tasks': 2,
        'overdue_tasks': 0,
        'completion_rate': 33.33
    }
    
    print(f"\n📊 পরিসংখ্যান:")
    print(f"  • মোট টাস্ক: {stats['total_tasks']}")
    print(f"  • সম্পন্ন: {stats['completed_tasks']}")
    print(f"  • অপেক্ষমাণ: {stats['pending_tasks']}")
    print(f"  • সম্পন্নের হার: {stats['completion_rate']:.1f}%")

async def demo_notifications():
    """Demonstrate notification system"""
    print_header("নোটিফিকেশন সিস্টেম ডেমো (Notification System Demo)")
    
    notification_manager = NotificationManager()
    
    # Get daily quote
    quote = await notification_manager.get_daily_motivational_quote('bn')
    print(f"আজকের অনুপ্রেরণা:")
    print(f"  {quote}")
    
    # Show summary
    summary = await notification_manager.generate_daily_summary(123456789)
    print(f"\nদৈনিক সারসংক্ষেপ:")
    print(f"  {summary}")

async def demo_gamification():
    """Demonstrate gamification features"""
    print_header("গেমিফিকেশন ডেমো (Gamification Demo)")
    
    game_manager = GameManager()
    
    # Show daily quiz
    quiz = await game_manager.get_daily_quiz()
    print(f"🧠 আজকের কুইজ:")
    print(f"প্রশ্ন: {quiz['question']}")
    print("অপশনসমূহ:")
    for i, option in enumerate(quiz['options']):
        marker = "✅" if i == quiz['correct'] else "  "
        print(f"  {chr(65+i)}) {option} {marker}")
    print(f"পয়েন্ট: {quiz['points']}")
    
    # Show leaderboard
    leaderboard = await game_manager.get_leaderboard()
    print(f"\n🏆 লিডারবোর্ড:")
    for entry in leaderboard:
        medal = "🥇" if entry['rank'] == 1 else "🥈" if entry['rank'] == 2 else "🥉" if entry['rank'] == 3 else f"{entry['rank']}."
        print(f"  {medal} {entry['name']} - {entry['points']} পয়েন্ট (লেভেল {entry['level']})")

def demo_database():
    """Demonstrate database setup"""
    print_header("ডেটাবেস সেটআপ ডেমো (Database Setup Demo)")
    
    # Create tables
    db.create_tables()
    print("✅ ডেটাবেস টেবিল তৈরি হয়েছে")
    
    # Show available models
    models = ['User', 'Task', 'Notification', 'ActivityLog', 'Quote', 'GameScore', 'BugReport']
    print("\n📊 উপলব্ধ মডেলসমূহ:")
    for model in models:
        print(f"  • {model}")

async def main():
    """Main demo function"""
    print("🇧🇩 বাংলা সহায়ক বট ডেমো শুরু")
    print("🇧🇩 Bengali Assistant Bot Demo Starting")
    print("="*60)
    
    # Run all demos
    demo_localization()
    demo_bengali_calendar()
    demo_security()
    await demo_task_management()
    await demo_notifications()
    await demo_gamification()
    demo_database()
    
    print_header("ডেমো সম্পন্ন (Demo Complete)")
    print("🎉 সব ফিচার সফলভাবে প্রদর্শিত হয়েছে!")
    print("🎉 All features demonstrated successfully!")
    print("\n📋 পরবর্তী ধাপ (Next Steps):")
    print("1. .env ফাইলে TELEGRAM_BOT_TOKEN যোগ করুন")
    print("2. python seed_data.py চালান")
    print("3. python main.py দিয়ে বট চালু করুন")
    print("\n💡 সম্পূর্ণ গাইডের জন্য README.md দেখুন")

if __name__ == "__main__":
    asyncio.run(main())