from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import re

def get_text(user_lang: str = "bengali") -> Dict[str, str]:
    """Get text constants based on user language"""
    if user_lang == "bengali":
        from locales.bengali import BENGALI_TEXT
        return BENGALI_TEXT
    else:
        from locales.bengali import ENGLISH_TEXT
        return ENGLISH_TEXT

def format_time(time_str: str) -> str:
    """Format time string to display format"""
    try:
        time_obj = datetime.strptime(time_str, '%H:%M')
        return time_obj.strftime('%I:%M %p')
    except:
        return time_str

def get_today_date() -> str:
    """Get today's date in YYYY-MM-DD format"""
    return datetime.now().strftime('%Y-%m-%d')

def get_week_dates() -> tuple:
    """Get start and end dates of current week"""
    today = datetime.now()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def get_month_dates() -> tuple:
    """Get start and end dates of current month"""
    today = datetime.now()
    start = today.replace(day=1)
    next_month = start.replace(month=start.month % 12 + 1) if start.month < 12 else start.replace(year=start.year + 1, month=1)
    end = next_month - timedelta(days=1)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def calculate_success_rate(completed: int, total: int) -> float:
    """Calculate success rate percentage"""
    if total == 0:
        return 0.0
    return round((completed / total) * 100, 2)

def format_routine_list(routines: Dict[str, Any], text: Dict[str, str]) -> str:
    """Format routine list for display"""
    if not routines:
        return text["no_routines"]
    
    formatted = "📋 *আপনার রুটিনসমূহ:*\n\n"
    for routine_id, routine in routines.items():
        status = "✅" if routine.get("is_active", True) else "⏸️"
        formatted += f"{status} *{routine['name']}*\n"
        formatted += f"   ⏰ {format_time(routine['time'])}\n"
        formatted += f"   🔄 {routine['frequency']}\n"
        formatted += f"   ✅ সম্পন্ন: {routine.get('completed_count', 0)} বার\n\n"
    
    return formatted

def create_routine_keyboard(routines: Dict[str, Any]):
    """Create inline keyboard for routine selection"""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    keyboard = []
    for routine_id, routine in routines.items():
        button = InlineKeyboardButton(
            f"{'✅' if routine.get('is_active', True) else '⏸️'} {routine['name']}",
            callback_data=f"routine_{routine_id}"
        )
        keyboard.append([button])
    
    return InlineKeyboardMarkup(keyboard)

def create_main_menu_keyboard():
    """Create main menu keyboard"""
    from telegram import KeyboardButton, ReplyKeyboardMarkup
    
    keyboard = [
        [KeyboardButton("📝 রুটিন তৈরি"), KeyboardButton("📋 আমার রুটিনসমূহ")],
        [KeyboardButton("📅 আজকের রুটিন"), KeyboardButton("📊 রিপোর্ট")],
        [KeyboardButton("⚙️ সেটিংস"), KeyboardButton("❓ সাহায্য")]
    ]
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def parse_notification_time(time_str: str) -> Optional[datetime]:
    """Parse notification time string"""
    try:
        time_obj = datetime.strptime(time_str, '%H:%M')
        now = datetime.now()
        notification_time = now.replace(
            hour=time_obj.hour,
            minute=time_obj.minute,
            second=0,
            microsecond=0
        )
        
        # If time has passed today, schedule for tomorrow
        if notification_time <= now:
            notification_time += timedelta(days=1)
        
        return notification_time
    except ValueError:
        return None

def is_admin(user_id: int, admin_ids: list) -> bool:
    """Check if user is admin"""
    return user_id in admin_ids

def escape_markdown(text: str) -> str:
    """Escape markdown special characters"""
    escape_chars = '_*[]()~`>#+-=|{}.!'
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text