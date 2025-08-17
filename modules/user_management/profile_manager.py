"""
প্রোফাইল ম্যানেজমেন্ট মডিউল
Profile Management Module
"""

from typing import Dict, Optional, Any
from config.database import db, User

class ProfileManager:
    """প্রোফাইল ম্যানেজার - Profile Manager"""
    
    def __init__(self):
        self.db = db
    
    async def update_profile(self, user_id: int, **updates) -> bool:
        """Update user profile"""
        with self.db.get_session() as session:
            user = session.query(User).filter(User.telegram_id == user_id).first()
            if user:
                for key, value in updates.items():
                    if hasattr(user, key):
                        setattr(user, key, value)
                session.commit()
                return True
            return False
    
    async def get_profile_data(self, user_id: int) -> Dict[str, Any]:
        """Get user profile data for export"""
        with self.db.get_session() as session:
            user = session.query(User).filter(User.telegram_id == user_id).first()
            if user:
                return {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username,
                    'language_code': user.language_code,
                    'timezone': user.timezone,
                    'theme': user.theme,
                    'settings': user.settings,
                    'created_at': user.created_at.isoformat() if user.created_at else None
                }
            return {}