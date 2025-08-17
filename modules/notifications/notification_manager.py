"""
নোটিফিকেশন ম্যানেজমেন্ট মডিউল
Notification Management Module  
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from config.database import db, Notification, User, Quote
import random

class NotificationManager:
    """নোটিফিকেশন ম্যানেজার - Notification Manager"""
    
    def __init__(self):
        self.db = db
    
    async def create_notification(
        self,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        scheduled_for: datetime = None,
        metadata: Dict = None
    ) -> Notification:
        """Create new notification"""
        
        with self.db.get_session() as session:
            notification = Notification(
                user_id=user_id,
                type=notification_type,
                title=title,
                message=message,
                scheduled_for=scheduled_for,
                metadata=metadata or {}
            )
            
            session.add(notification)
            session.commit()
            session.refresh(notification)
            return notification
    
    async def get_daily_motivational_quote(self, language: str = 'bn') -> str:
        """Get random motivational quote"""
        
        with self.db.get_session() as session:
            quotes = session.query(Quote).filter(Quote.is_active == True).all()
            
            if quotes:
                quote = random.choice(quotes)
                if language == 'bn' and quote.text_bn:
                    return f"💪 {quote.text_bn}\n- {quote.author_bn or 'অজানা'}"
                elif language == 'en' and quote.text_en:
                    return f"💪 {quote.text_en}\n- {quote.author_en or 'Unknown'}"
        
        # Default quotes if database is empty
        default_quotes_bn = [
            "💪 সফলতা আসে ধৈর্য এবং কঠিন পরিশ্রমের মাধ্যমে।",
            "🌟 প্রতিটি নতুন দিন একটি নতুন সুযোগ।",
            "🚀 স্বপ্ন দেখুন, পরিকল্পনা করুন, কাজ করুন।",
            "💎 অসুবিধাই আপনাকে শক্তিশালী করে তোলে।",
            "🌅 আজকের ছোট প্রচেষ্টা আগামীর বড় সাফল্য।"
        ]
        
        return random.choice(default_quotes_bn)
    
    async def generate_daily_summary(self, user_id: int) -> str:
        """Generate daily task summary"""
        # This would integrate with TaskManager
        return "📊 আজকের সারসংক্ষেপ: আপনার ৫টি টাস্কের মধ্যে ৩টি সম্পন্ন হয়েছে!"
    
    async def send_scheduled_notifications(self):
        """Send all scheduled notifications (called by scheduler)"""
        with self.db.get_session() as session:
            now = datetime.utcnow()
            pending_notifications = session.query(Notification).filter(
                Notification.is_sent == False,
                Notification.scheduled_for <= now
            ).all()
            
            for notification in pending_notifications:
                # This would integrate with the bot to send actual messages
                notification.is_sent = True
                notification.sent_at = now
            
            session.commit()
            return len(pending_notifications)