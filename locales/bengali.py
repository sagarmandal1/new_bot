# Bengali language constants
BENGALI_TEXT = {
    # Welcome and start messages
    "welcome": "🙏 স্বাগতম! দৈনিক রুটিন আপডেট বটে আপনাকে স্বাগত জানাই।",
    "start_message": """
🌟 *দৈনিক রুটিন আপডেট বট*

এই বটটি আপনার দৈনিক, সাপ্তাহিক এবং মাসিক রুটিন পরিচালনায় সাহায্য করবে।

*বৈশিষ্ট্যসমূহ:*
📝 রুটিন তৈরি ও সম্পাদনা
⏰ রিমাইন্ডার ও নোটিফিকেশন
📊 দৈনিক/সাপ্তাহিক/মাসিক রিপোর্ট
👤 ব্যক্তিগত প্রোফাইল ব্যবস্থাপনা

/help কমান্ডের মাধ্যমে সকল কমান্ড দেখুন।
    """,
    
    # Menu buttons
    "menu_create_routine": "📝 রুটিন তৈরি",
    "menu_my_routines": "📋 আমার রুটিনসমূহ",
    "menu_today_routine": "📅 আজকের রুটিন",
    "menu_reports": "📊 রিপোর্ট",
    "menu_settings": "⚙️ সেটিংস",
    "menu_help": "❓ সাহায্য",
    
    # Registration
    "registration_needed": "আপনাকে প্রথমে রেজিস্ট্রেশন করতে হবে। /register কমান্ড ব্যবহার করুন।",
    "registration_name": "অনুগ্রহ করে আপনার নাম লিখুন:",
    "registration_age": "আপনার বয়স লিখুন:",
    "registration_success": "✅ রেজিস্ট্রেশন সফল! এখন আপনি বট ব্যবহার করতে পারেন।",
    "already_registered": "আপনি ইতিমধ্যে রেজিস্টার করেছেন।",
    
    # Routine management
    "routine_name": "রুটিনের নাম লিখুন:",
    "routine_description": "রুটিনের বিবরণ লিখুন:",
    "routine_time": "সময় নির্ধারণ করুন (HH:MM ফরম্যাটে, যেমন: 07:30):",
    "routine_frequency": "কত ঘন ঘন করবেন?",
    "routine_created": "✅ রুটিন সফলভাবে তৈরি হয়েছে!",
    "routine_updated": "✅ রুটিন আপডেট হয়েছে!",
    "routine_deleted": "🗑️ রুটিন মুছে ফেলা হয়েছে।",
    "no_routines": "আপনার কোন রুটিন নেই। /create_routine দিয়ে একটি তৈরি করুন।",
    
    # Frequency options
    "daily": "প্রতিদিন",
    "weekly": "সাপ্তাহিক",
    "monthly": "মাসিক",
    
    # Reminders
    "reminder_time": "⏰ রিমাইন্ডার সময়!",
    "routine_reminder": "🔔 আপনার '{routine_name}' রুটিনের সময় হয়েছে।",
    "mark_completed": "✅ সম্পন্ন",
    "skip_today": "⏭️ আজ বাদ দিন",
    "postpone": "⏳ পরে করব",
    
    # Reports
    "daily_report": "📊 আজকের রিপোর্ট",
    "weekly_report": "📈 সাপ্তাহিক রিপোর্ট",
    "monthly_report": "📉 মাসিক রিপোর্ট",
    "report_completed": "সম্পন্ন: {completed}",
    "report_pending": "বাকি: {pending}",
    "report_success_rate": "সফলতার হার: {rate}%",
    
    # Settings
    "settings_menu": "⚙️ সেটিংস মেনু",
    "change_language": "🌐 ভাষা পরিবর্তন",
    "notification_settings": "🔔 নোটিফিকেশন সেটিংস",
    "profile_settings": "👤 প্রোফাইল সেটিংস",
    
    # Admin commands
    "admin_panel": "🔧 অ্যাডমিন প্যানেল",
    "total_users": "মোট ব্যবহারকারী: {count}",
    "broadcast_message": "সবার কাছে বার্তা পাঠাতে টেক্সট লিখুন:",
    "broadcast_sent": "✅ বার্তা {count} জন ব্যবহারকারীর কাছে পাঠানো হয়েছে।",
    "backup_created": "✅ ব্যাকআপ তৈরি হয়েছে।",
    
    # Help
    "help_message": """
🤖 *দৈনিক রুটিন বট - সাহায্য*

*মূল কমান্ডসমূহ:*
/start - বট শুরু করুন
/register - রেজিস্ট্রেশন
/menu - মূল মেনু
/help - এই সাহায্য বার্তা

*রুটিন ব্যবস্থাপনা:*
/create_routine - নতুন রুটিন তৈরি
/my_routines - আপনার সব রুটিন দেখুন
/today - আজকের রুটিন
/edit_routine - রুটিন সম্পাদনা
/delete_routine - রুটিন মুছে ফেলুন

*রিপোর্ট ও পরিসংখ্যান:*
/daily_report - দৈনিক রিপোর্ট
/weekly_report - সাপ্তাহিক রিপোর্ট
/monthly_report - মাসিক রিপোর্ট

*সেটিংস:*
/settings - সেটিংস মেনু
/language - ভাষা পরিবর্তন
/profile - প্রোফাইল দেখুন

আরো প্রশ্ন থাকলে /support ব্যবহার করুন।
    """,
    
    # Error messages
    "error_occurred": "❌ একটি ত্রুটি ঘটেছে। আবার চেষ্টা করুন।",
    "invalid_format": "❌ ভুল ফরম্যাট। অনুগ্রহ করে সঠিক ফরম্যাট ব্যবহার করুন।",
    "routine_not_found": "❌ রুটিন খুঁজে পাওয়া যায়নি।",
    "access_denied": "❌ আপনার এই কমান্ড ব্যবহারের অনুমতি নেই।",
    
    # Success messages
    "success": "✅ সফল!",
    "saved": "✅ সংরক্ষিত হয়েছে।",
    "cancelled": "❌ বাতিল করা হয়েছে।"
}

ENGLISH_TEXT = {
    "welcome": "🙏 Welcome to the Daily Routine Update Bot!",
    "start_message": """
🌟 *Daily Routine Update Bot*

This bot will help you manage your daily, weekly, and monthly routines.

*Features:*
📝 Create and edit routines
⏰ Reminders and notifications  
📊 Daily/weekly/monthly reports
👤 Personal profile management

Use /help to see all commands.
    """,
    # Add more English translations as needed...
}