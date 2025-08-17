# -*- coding: utf-8 -*-
"""
Constants and Bengali UI text for the Telegram bot
All Bengali text with emojis for an attractive user experience
"""

# Bot Configuration
BOT_TOKEN = ""  # To be set via environment variable or config
DEFAULT_TIMEZONE = "Asia/Kolkata"
BACKUP_INTERVAL_HOURS = 24

# Reminder intervals (in minutes)
REMINDER_INTERVALS = [5, 10, 15, 30, 60]
DEFAULT_REMINDER_INTERVAL = 15

# File paths
DATA_FILE = "bot_data.json"
BACKUP_DIR = "backups"

# Emojis
EMOJIS = {
    'routine': '📅',
    'task': '✅',
    'reminder': '⏰',
    'settings': '⚙️',
    'stats': '📊',
    'help': '❓',
    'add': '➕',
    'edit': '✏️',
    'delete': '🗑️',
    'view': '👀',
    'back': '🔙',
    'save': '💾',
    'cancel': '❌',
    'done': '✔️',
    'pending': '⏳',
    'warning': '⚠️',
    'success': '🎉',
    'profile': '👤',
    'time': '🕐',
    'date': '📆',
    'daily': '🌅',
    'weekly': '📆',
    'notification': '🔔'
}

# Bengali UI Text
BENGALI_TEXT = {
    # Main Menu
    'welcome': f"{EMOJIS['success']} স্বাগতম! আমি আপনার ব্যক্তিগত রুটিন ও কাজের সহায়ক।",
    'main_menu': f"{EMOJIS['routine']} প্রধান মেনু",
    'choose_option': "অনুগ্রহ করে একটি বিকল্প নির্বাচন করুন:",
    
    # Buttons
    'btn_routines': f"{EMOJIS['routine']} রুটিন ব্যবস্থাপনা",
    'btn_quick_tasks': f"{EMOJIS['task']} দ্রুত কাজ",
    'btn_reminders': f"{EMOJIS['reminder']} স্মার্ট রিমাইন্ডার",
    'btn_settings': f"{EMOJIS['settings']} সেটিংস",
    'btn_stats': f"{EMOJIS['stats']} পরিসংখ্যান",
    'btn_help': f"{EMOJIS['help']} সহায়তা",
    
    # Routine Management
    'routine_menu': f"{EMOJIS['routine']} রুটিন ব্যবস্থাপনা",
    'btn_add_routine': f"{EMOJIS['add']} নতুন রুটিন যোগ করুন",
    'btn_view_routines': f"{EMOJIS['view']} রুটিন দেখুন",
    'btn_edit_routine': f"{EMOJIS['edit']} রুটিন সম্পাদনা করুন",
    'btn_delete_routine': f"{EMOJIS['delete']} রুটিন মুছুন",
    
    # Task Management
    'task_menu': f"{EMOJIS['task']} দ্রুত কাজ",
    'btn_add_task': f"{EMOJIS['add']} নতুন কাজ যোগ করুন",
    'btn_view_tasks': f"{EMOJIS['view']} কাজের তালিকা",
    'btn_complete_task': f"{EMOJIS['done']} কাজ সম্পন্ন করুন",
    'btn_delete_task': f"{EMOJIS['delete']} কাজ মুছুন",
    
    # Common buttons
    'btn_back': f"{EMOJIS['back']} পূর্ববর্তী মেনু",
    'btn_save': f"{EMOJIS['save']} সংরক্ষণ করুন",
    'btn_cancel': f"{EMOJIS['cancel']} বাতিল করুন",
    
    # Input prompts
    'enter_routine_name': f"{EMOJIS['routine']} রুটিনের নাম লিখুন:",
    'enter_routine_time': f"{EMOJIS['time']} সময় নির্ধারণ করুন (যেমন: 07:30):",
    'select_days': f"{EMOJIS['date']} দিন নির্বাচন করুন:",
    'enter_task_name': f"{EMOJIS['task']} কাজের নাম লিখুন:",
    'enter_task_deadline': f"{EMOJIS['time']} শেষ সময় নির্ধারণ করুন (যেমন: 2024-12-25 15:30):",
    'enter_profile_name': f"{EMOJIS['profile']} আপনার নাম লিখুন:",
    
    # Days of week
    'monday': 'সোমবার',
    'tuesday': 'মঙ্গলবার', 
    'wednesday': 'বুধবার',
    'thursday': 'বৃহস্পতিবার',
    'friday': 'শুক্রবার',
    'saturday': 'শনিবার',
    'sunday': 'রবিবার',
    
    # Routine types
    'daily_routine': f"{EMOJIS['daily']} দৈনিক রুটিন",
    'weekly_routine': f"{EMOJIS['weekly']} সাপ্তাহিক রুটিন",
    
    # Messages
    'routine_created': f"{EMOJIS['success']} রুটিন সফলভাবে তৈরি হয়েছে!",
    'task_created': f"{EMOJIS['success']} কাজ সফলভাবে যোগ করা হয়েছে!",
    'task_completed': f"{EMOJIS['done']} অভিনন্দন! কাজটি সম্পন্ন হয়েছে।",
    'item_deleted': f"{EMOJIS['success']} সফলভাবে মুছে ফেলা হয়েছে।",
    'settings_saved': f"{EMOJIS['success']} সেটিংস সংরক্ষিত হয়েছে।",
    
    # Errors
    'error_occurred': f"{EMOJIS['warning']} একটি ত্রুটি ঘটেছে। অনুগ্রহ করে আবার চেষ্টা করুন।",
    'invalid_format': f"{EMOJIS['warning']} ভুল ফরম্যাট। অনুগ্রহ করে সঠিক ফরম্যাটে লিখুন।",
    'no_items_found': f"{EMOJIS['warning']} কোনো আইটেম পাওয়া যায়নি।",
    'operation_cancelled': f"{EMOJIS['cancel']} অপারেশন বাতিল করা হয়েছে।",
    
    # Reminders
    'reminder_5min': f"{EMOJIS['reminder']} ৫ মিনিট পরে",
    'reminder_10min': f"{EMOJIS['reminder']} ১০ মিনিট পরে",
    'reminder_15min': f"{EMOJIS['reminder']} ১৫ মিনিট পরে",
    'reminder_30min': f"{EMOJIS['reminder']} ৩০ মিনিট পরে",
    'reminder_60min': f"{EMOJIS['reminder']} ১ ঘন্টা পরে",
    
    # Settings
    'settings_menu': f"{EMOJIS['settings']} সেটিংস",
    'btn_change_name': f"{EMOJIS['profile']} নাম পরিবর্তন",
    'btn_change_timezone': f"{EMOJIS['time']} টাইমজোন পরিবর্তন",
    'btn_reminder_settings': f"{EMOJIS['notification']} রিমাইন্ডার সেটিংস",
    
    # Stats
    'stats_title': f"{EMOJIS['stats']} আপনার পরিসংখ্যান",
    'total_routines': "মোট রুটিন:",
    'total_tasks': "মোট কাজ:",
    'completed_tasks': "সম্পন্ন কাজ:",
    'pending_tasks': "বাকি কাজ:",
    'completion_rate': "সম্পন্নতার হার:",
    
    # Help
    'help_title': f"{EMOJIS['help']} সহায়তা",
    'help_text': """এই বটটি ব্যবহার করে আপনি:

🔹 দৈনিক ও সাপ্তাহিক রুটিন তৈরি ও পরিচালনা করতে পারবেন
🔹 দ্রুত কাজ যোগ করে সেগুলি ট্র্যাক করতে পারবেন  
🔹 স্মার্ট রিমাইন্ডার সেট করতে পারবেন
🔹 আপনার অগ্রগতি দেখতে পারবেন
🔹 সেটিংস কাস্টমাইজ করতে পারবেন

📝 কমান্ড:
/start - বট শুরু করুন
/menu - প্রধান মেনু
/help - এই সহায়তা বার্তা
/stats - দ্রুত পরিসংখ্যান

❓ কোনো সমস্যা হলে /start কমান্ড ব্যবহার করুন।"""
}

# Command list
COMMANDS = {
    'start': 'start',
    'menu': 'menu', 
    'help': 'help',
    'stats': 'stats'
}

# Callback data patterns
CALLBACK_DATA = {
    'main_menu': 'main_menu',
    'routines': 'routines',
    'tasks': 'tasks',
    'reminders': 'reminders',
    'settings': 'settings',
    'stats': 'stats',
    'help': 'help',
    'add_routine': 'add_routine',
    'view_routines': 'view_routines',
    'edit_routine': 'edit_routine',
    'delete_routine': 'delete_routine',
    'add_task': 'add_task',
    'view_tasks': 'view_tasks',
    'complete_task': 'complete_task',
    'delete_task': 'delete_task',
    'back': 'back',
    'save': 'save',
    'cancel': 'cancel'
}

# States for conversation handlers
STATES = {
    'WAITING_ROUTINE_NAME': 'WAITING_ROUTINE_NAME',
    'WAITING_ROUTINE_TIME': 'WAITING_ROUTINE_TIME',
    'WAITING_ROUTINE_DAYS': 'WAITING_ROUTINE_DAYS',
    'WAITING_TASK_NAME': 'WAITING_TASK_NAME',
    'WAITING_TASK_DEADLINE': 'WAITING_TASK_DEADLINE',
    'WAITING_PROFILE_NAME': 'WAITING_PROFILE_NAME',
    'SELECTING_ROUTINE': 'SELECTING_ROUTINE',
    'SELECTING_TASK': 'SELECTING_TASK'
}