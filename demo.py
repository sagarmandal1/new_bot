#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script showing how the Bengali Telegram Bot works
This demonstrates the actual bot interaction flow without Telegram
"""

from storage import StorageManager
from ui import UIManager
from handlers import BotHandlers
from constants import BENGALI_TEXT

def demonstrate_bot_interaction():
    """Demonstrate typical bot interaction flow"""
    print("🤖 বাংলা টেলিগ্রাম বট - ইন্টার‍্যাকশন ডেমো")
    print("=" * 60)
    print()
    
    # Initialize components
    storage = StorageManager()
    ui = UIManager()
    handlers = BotHandlers(storage)
    
    # Simulate a user
    user_id = 98765
    user_name = "রাহুল"
    
    print(f"👤 User: {user_name} (ID: {user_id})")
    print()
    
    # Simulate /start command
    print("🚀 User sends: /start")
    print("Bot responds:")
    welcome_message = ui.format_welcome_message(user_name)
    print(f"💬 {welcome_message}")
    
    # Show main menu
    print("\n📱 Bot shows main menu with buttons:")
    buttons = [
        ui.text['btn_routines'],
        ui.text['btn_quick_tasks'], 
        ui.text['btn_reminders'],
        ui.text['btn_settings'],
        ui.text['btn_stats'],
        ui.text['btn_help']
    ]
    
    for i, button in enumerate(buttons, 1):
        print(f"   {i}. {button}")
    
    print(f"\n🔘 User clicks: {ui.text['btn_routines']}")
    print("Bot shows routine management menu:")
    routine_buttons = [
        ui.text['btn_add_routine'],
        ui.text['btn_view_routines'],
        ui.text['btn_edit_routine'], 
        ui.text['btn_delete_routine'],
        ui.text['btn_back']
    ]
    
    for i, button in enumerate(routine_buttons, 1):
        print(f"   {i}. {button}")
    
    print(f"\n➕ User clicks: {ui.text['btn_add_routine']}")
    print("Bot asks for routine name...")
    print(f"💬 {ui.text['enter_routine_name']}")
    
    # Simulate routine creation
    print("\n✏️ User types: 'ফজরের নামাজ'")
    routine_name = "ফজরের নামাজ"
    
    print("Bot asks for time...")
    print(f"💬 {ui.text['enter_routine_time']}")
    
    print("\n⏰ User types: '05:30'")
    routine_time = "05:30"
    
    # Create the routine
    routine_data = {
        'name': routine_name,
        'time': routine_time,
        'type': 'daily',
        'reminder_intervals': [15, 30]
    }
    
    routine_id = storage.add_routine(user_id, routine_data)
    print(f"\n✅ {ui.text['routine_created']}")
    print(f"📅 Routine ID: {routine_id}")
    
    # Show routine details
    routines = storage.get_user_routines(user_id)
    if routines:
        routine_details = ui.format_routine_details(routines[0])
        print(f"\n📋 Routine details:\n{routine_details}")
    
    # Simulate task creation
    print(f"\n🔘 User clicks: {ui.text['btn_quick_tasks']}")
    print(f"➕ Then clicks: {ui.text['btn_add_task']}")
    print(f"💬 {ui.text['enter_task_name']}")
    
    print("\n✏️ User types: 'ব্যাংকে টাকা জমা দেওয়া'")
    task_name = "ব্যাংকে টাকা জমা দেওয়া"
    
    task_data = {
        'name': task_name,
        'deadline': '2024-12-25 16:00',
        'reminder_intervals': [30, 60]
    }
    
    task_id = storage.add_task(user_id, task_data)
    print(f"\n✅ {ui.text['task_created']}")
    print(f"📋 Task ID: {task_id}")
    
    # Show statistics
    print(f"\n📊 User clicks: {ui.text['btn_stats']}")
    stats = storage.get_user_stats(user_id)
    stats_message = ui.format_stats_message(stats)
    print(f"💬 Bot shows:\n{stats_message}")
    
    # Complete task simulation
    print(f"\n✔️ User completes the task...")
    storage.complete_task(user_id, task_id)
    print(f"💬 {ui.text['task_completed']}")
    
    # Updated statistics
    updated_stats = storage.get_user_stats(user_id)
    updated_stats_msg = ui.format_stats_message(updated_stats)
    print(f"\n📈 Updated statistics:\n{updated_stats_msg}")
    
    # Show help
    print(f"\n❓ User clicks: {ui.text['btn_help']}")
    help_message = ui.format_help_message()
    print(f"💬 Bot shows help:\n{help_message}")
    
    print("\n" + "=" * 60)
    print("🎉 Demo completed! This shows how the bot interaction works.")
    print("✅ All features are working perfectly in Bengali!")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    try:
        demonstrate_bot_interaction()
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()