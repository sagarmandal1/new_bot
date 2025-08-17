from datetime import datetime, timedelta
from typing import List, Dict, Any
from telegram import Bot, InlineKeyboardMarkup, InlineKeyboardButton
from bot.services.routine_service import RoutineService
from bot.services.user_service import UserService
from bot.utils.helpers import get_text

class NotificationService:
    """Service for handling notifications and reminders"""
    
    def __init__(self, bot: Bot, routine_service: RoutineService, user_service: UserService):
        self.bot = bot
        self.routine_service = routine_service
        self.user_service = user_service
    
    async def send_routine_reminders(self):
        """Send reminders for routines that are due"""
        notification_routines = self.routine_service.get_routines_for_notification()
        
        for item in notification_routines:
            user_id = item['user_id']
            routine_id = item['routine_id']
            routine = item['routine']
            
            # Check if user has notifications enabled
            user_data = self.user_service.get_user(user_id)
            if not user_data or not user_data.get('notifications_enabled', True):
                continue
            
            user_lang = self.user_service.get_user_language(user_id)
            text = get_text(user_lang)
            
            # Format reminder message
            reminder_text = f"""
🔔 *{text['reminder_time']}*

{text['routine_reminder'].format(routine_name=routine['name'])}

📝 বিবরণ: {routine['description']}
⏰ সময়: {routine['time']}
            """
            
            # Create action buttons
            keyboard = [
                [InlineKeyboardButton(text["mark_completed"], 
                                    callback_data=f"complete_{routine_id}")],
                [InlineKeyboardButton(text["skip_today"], 
                                    callback_data=f"skip_{routine_id}"),
                 InlineKeyboardButton(text["postpone"], 
                                    callback_data=f"postpone_{routine_id}")]
            ]
            
            try:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=reminder_text,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            except Exception as e:
                print(f"Failed to send notification to {user_id}: {e}")
    
    async def send_daily_summary(self, user_id: int):
        """Send daily summary to user"""
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        today_routines = self.routine_service.get_today_routines(user_id)
        
        if not today_routines:
            return
        
        # Get completion status from reports
        reports = self.routine_service.db.get_user_reports(user_id)
        today = datetime.now().strftime('%Y-%m-%d')
        completed_today = [r for r in reports if r['date'] == today]
        
        completed_count = len(completed_today)
        total_count = len(today_routines)
        
        summary_text = f"""
📊 *আজকের সারসংক্ষেপ*

✅ সম্পন্ন: {completed_count}/{total_count}
📈 সফলতার হার: {(completed_count/total_count)*100:.0f}%

{'🎉 দুর্দান্ত! সব রুটিন সম্পন্ন!' if completed_count == total_count else '💪 চালিয়ে যান!'}
        """
        
        try:
            await self.bot.send_message(
                chat_id=user_id,
                text=summary_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            print(f"Failed to send daily summary to {user_id}: {e}")
    
    async def send_broadcast_message(self, admin_user_id: int, message: str) -> int:
        """Send broadcast message to all users"""
        users = self.user_service.get_all_users()
        sent_count = 0
        
        for user_id_str in users.keys():
            user_id = int(user_id_str)
            
            # Skip the admin who is sending
            if user_id == admin_user_id:
                continue
            
            try:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=f"📢 *ব্রডকাস্ট বার্তা*\n\n{message}",
                    parse_mode='Markdown'
                )
                sent_count += 1
            except Exception as e:
                print(f"Failed to send broadcast to {user_id}: {e}")
        
        return sent_count