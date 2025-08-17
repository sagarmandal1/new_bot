#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to demonstrate Bengali Telegram Bot functionality
This script tests core features without requiring a Telegram bot token
"""

from storage import StorageManager
from ui import UIManager
from handlers import BotHandlers
import json
import os

def test_bot_functionality():
    """Test all major bot functionalities"""
    print("🧪 Bengali Telegram Bot - Functionality Test")
    print("=" * 50)
    
    # Initialize components
    storage = StorageManager()
    ui = UIManager()
    handlers = BotHandlers(storage)
    
    print("✅ All components initialized successfully")
    print()
    
    # Test user creation and data structure
    print("📋 Testing User Data Management:")
    user_id = 12345
    user_data = storage.get_user_data(user_id)
    print(f"   User created with ID: {user_id}")
    print(f"   Default timezone: {user_data['profile']['timezone']}")
    print(f"   Reminder interval: {user_data['profile']['reminder_interval']} minutes")
    print()
    
    # Test routine creation
    print("📅 Testing Routine Management:")
    routine_data = {
        'name': 'সকালের নাস্তা',
        'time': '08:00',
        'type': 'daily',
        'reminder_intervals': [15, 30]
    }
    routine_id = storage.add_routine(user_id, routine_data)
    print(f"   ✅ Routine created: {routine_data['name']}")
    print(f"   Routine ID: {routine_id}")
    
    # Test weekly routine
    weekly_routine_data = {
        'name': 'সাপ্তাহিক বাজার',
        'time': '10:00',
        'type': 'weekly',
        'days': ['saturday', 'tuesday'],
        'reminder_intervals': [60]
    }
    weekly_routine_id = storage.add_routine(user_id, weekly_routine_data)
    print(f"   ✅ Weekly routine created: {weekly_routine_data['name']}")
    print()
    
    # Test task creation
    print("✅ Testing Task Management:")
    task_data = {
        'name': 'ডাক্তারের সাথে অ্যাপয়েন্টমেন্ট',
        'deadline': '2024-12-30 15:30',
        'reminder_intervals': [15, 30, 60]
    }
    task_id = storage.add_task(user_id, task_data)
    print(f"   ✅ Task created: {task_data['name']}")
    print(f"   Task ID: {task_id}")
    print(f"   Deadline: {task_data['deadline']}")
    
    # Test another task
    task_data2 = {
        'name': 'বই পড়া',
        'reminder_intervals': [15]
    }
    task_id2 = storage.add_task(user_id, task_data2)
    print(f"   ✅ Simple task created: {task_data2['name']}")
    print()
    
    # Test task completion
    print("🎯 Testing Task Completion:")
    storage.complete_task(user_id, task_id2)
    print(f"   ✅ Task completed: {task_data2['name']}")
    print()
    
    # Test data retrieval
    print("📊 Testing Data Retrieval:")
    routines = storage.get_user_routines(user_id)
    tasks = storage.get_user_tasks(user_id)
    pending_tasks = storage.get_user_tasks(user_id, completed=False)
    completed_tasks = storage.get_user_tasks(user_id, completed=True)
    
    print(f"   Total routines: {len(routines)}")
    print(f"   Total tasks: {len(tasks)}")
    print(f"   Pending tasks: {len(pending_tasks)}")
    print(f"   Completed tasks: {len(completed_tasks)}")
    print()
    
    # Test statistics
    print("📈 Testing Statistics:")
    stats = storage.get_user_stats(user_id)
    print(f"   Total routines: {stats['total_routines']}")
    print(f"   Total tasks: {stats['total_tasks']}")
    print(f"   Completed tasks: {stats['completed_tasks']}")
    print(f"   Pending tasks: {stats['pending_tasks']}")
    print(f"   Completion rate: {stats['completion_rate']}%")
    print()
    
    # Test UI formatting
    print("🎨 Testing UI Formatting:")
    welcome_msg = ui.format_welcome_message("সাগর")
    print(f"   Welcome message: {welcome_msg[:100]}...")
    
    routine_details = ui.format_routine_details(routines[0])
    print(f"   Routine details: {routine_details[:100]}...")
    
    stats_msg = ui.format_stats_message(stats)
    print(f"   Stats message: {stats_msg[:100]}...")
    print()
    
    # Test profile update
    print("👤 Testing Profile Update:")
    storage.update_user_profile(user_id, {
        'name': 'সাগর মন্ডল',
        'timezone': 'Asia/Dhaka',
        'reminder_interval': 10
    })
    updated_user_data = storage.get_user_data(user_id)
    print(f"   ✅ Profile updated: {updated_user_data['profile']['name']}")
    print(f"   New timezone: {updated_user_data['profile']['timezone']}")
    print(f"   New reminder interval: {updated_user_data['profile']['reminder_interval']} minutes")
    print()
    
    # Test backup creation
    print("💾 Testing Backup System:")
    if os.path.exists('backups'):
        backup_files = [f for f in os.listdir('backups') if f.endswith('.json')]
        print(f"   Number of backup files: {len(backup_files)}")
        if backup_files:
            print(f"   Latest backup: {sorted(backup_files)[-1]}")
    
    manual_backup = storage.manual_backup()
    print(f"   ✅ Manual backup created: {manual_backup}")
    print()
    
    # Final stats
    print("🏆 Final Test Results:")
    final_stats = storage.get_user_stats(user_id)
    print(f"   User profile: {updated_user_data['profile']['name']}")
    print(f"   Total routines: {final_stats['total_routines']}")
    print(f"   Total tasks: {final_stats['total_tasks']}")
    print(f"   Completion rate: {final_stats['completion_rate']}%")
    print()
    
    print("🎉 All tests completed successfully!")
    print("✅ Bengali Telegram Bot is ready to deploy!")
    print()
    print("📋 Next Steps:")
    print("   1. Get a bot token from @BotFather on Telegram")
    print("   2. Set BOT_TOKEN environment variable")
    print("   3. Run: python main.py")
    print("   4. Start chatting with your bot!")
    
    return True

if __name__ == '__main__':
    try:
        test_bot_functionality()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()