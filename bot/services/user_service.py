from typing import Optional, Dict, Any
from bot.utils.database import JSONDatabase
from bot.utils.validators import validate_name, validate_age, sanitize_input

class UserService:
    """Service for user management operations"""
    
    def __init__(self, db: JSONDatabase):
        self.db = db
    
    def register_user(self, user_id: int, telegram_user_data: Dict[str, Any], 
                     name: str, age: int) -> bool:
        """Register a new user"""
        if not validate_name(name) or not validate_age(str(age)):
            return False
        
        user_data = {
            "name": sanitize_input(name),
            "age": age,
            "username": telegram_user_data.get("username", ""),
            "first_name": telegram_user_data.get("first_name", ""),
            "last_name": telegram_user_data.get("last_name", ""),
            "language": "bengali",
            "notifications_enabled": True,
            "timezone": "Asia/Dhaka"
        }
        
        return self.db.create_user(user_id, user_data)
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user data"""
        return self.db.get_user(user_id)
    
    def is_user_registered(self, user_id: int) -> bool:
        """Check if user is registered"""
        return self.db.get_user(user_id) is not None
    
    def update_user_language(self, user_id: int, language: str) -> bool:
        """Update user language"""
        return self.db.update_user(user_id, {"language": language})
    
    def update_user_notifications(self, user_id: int, enabled: bool) -> bool:
        """Update user notification settings"""
        return self.db.update_user(user_id, {"notifications_enabled": enabled})
    
    def update_user_profile(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update user profile"""
        # Validate updates
        if "name" in updates and not validate_name(updates["name"]):
            return False
        if "age" in updates and not validate_age(str(updates["age"])):
            return False
        
        # Sanitize inputs
        sanitized_updates = {}
        for key, value in updates.items():
            if key in ["name"]:
                sanitized_updates[key] = sanitize_input(str(value))
            else:
                sanitized_updates[key] = value
        
        return self.db.update_user(user_id, sanitized_updates)
    
    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language"""
        user = self.get_user(user_id)
        return user.get("language", "bengali") if user else "bengali"
    
    def get_all_users(self) -> Dict[str, Any]:
        """Get all users (admin only)"""
        return self.db.get_all_users()
    
    def get_user_count(self) -> int:
        """Get total user count"""
        users = self.get_all_users()
        return len(users)