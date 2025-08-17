from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from bot.utils.database import JSONDatabase
from bot.utils.validators import validate_routine_name, validate_routine_description, validate_time_format, validate_frequency
from bot.utils.helpers import get_today_date, get_week_dates, get_month_dates

class RoutineService:
    """Service for routine management operations"""
    
    def __init__(self, db: JSONDatabase):
        self.db = db
    
    def create_routine(self, user_id: int, name: str, description: str, 
                      time: str, frequency: str) -> Optional[str]:
        """Create a new routine"""
        if not validate_routine_name(name):
            return None
        if not validate_routine_description(description):
            return None
        if not validate_time_format(time):
            return None
        if not validate_frequency(frequency):
            return None
        
        routine_data = {
            "name": name.strip(),
            "description": description.strip(),
            "time": time,
            "frequency": frequency,
            "is_active": True,
            "reminder_enabled": True
        }
        
        return self.db.create_routine(user_id, routine_data)
    
    def get_user_routines(self, user_id: int) -> Dict[str, Any]:
        """Get all routines for a user"""
        return self.db.get_user_routines(user_id)
    
    def get_routine(self, user_id: int, routine_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific routine"""
        return self.db.get_routine(user_id, routine_id)
    
    def update_routine(self, user_id: int, routine_id: str, updates: Dict[str, Any]) -> bool:
        """Update a routine"""
        # Validate updates
        if "name" in updates and not validate_routine_name(updates["name"]):
            return False
        if "description" in updates and not validate_routine_description(updates["description"]):
            return False
        if "time" in updates and not validate_time_format(updates["time"]):
            return False
        if "frequency" in updates and not validate_frequency(updates["frequency"]):
            return False
        
        return self.db.update_routine(user_id, routine_id, updates)
    
    def delete_routine(self, user_id: int, routine_id: str) -> bool:
        """Delete a routine"""
        return self.db.delete_routine(user_id, routine_id)
    
    def toggle_routine_active(self, user_id: int, routine_id: str) -> bool:
        """Toggle routine active status"""
        routine = self.get_routine(user_id, routine_id)
        if not routine:
            return False
        
        new_status = not routine.get("is_active", True)
        return self.update_routine(user_id, routine_id, {"is_active": new_status})
    
    def mark_routine_completed(self, user_id: int, routine_id: str) -> bool:
        """Mark a routine as completed"""
        return self.db.mark_routine_completed(user_id, routine_id)
    
    def get_today_routines(self, user_id: int) -> Dict[str, Any]:
        """Get routines scheduled for today"""
        all_routines = self.get_user_routines(user_id)
        today_routines = {}
        
        for routine_id, routine in all_routines.items():
            if not routine.get("is_active", True):
                continue
            
            frequency = routine.get("frequency", "daily")
            if self._should_show_routine_today(routine, frequency):
                today_routines[routine_id] = routine
        
        return today_routines
    
    def _should_show_routine_today(self, routine: Dict[str, Any], frequency: str) -> bool:
        """Check if routine should be shown today based on frequency"""
        if frequency.lower() in ["daily", "প্রতিদিন"]:
            return True
        
        elif frequency.lower() in ["weekly", "সাপ্তাহিক"]:
            # For weekly routines, show on the same day of week they were created
            created_at = datetime.fromisoformat(routine["created_at"])
            today = datetime.now()
            return created_at.weekday() == today.weekday()
        
        elif frequency.lower() in ["monthly", "মাসিক"]:
            # For monthly routines, show on the same day of month they were created
            created_at = datetime.fromisoformat(routine["created_at"])
            today = datetime.now()
            return created_at.day == today.day
        
        return False
    
    def get_routines_for_notification(self) -> List[Dict[str, Any]]:
        """Get routines that need notification right now"""
        all_routines_data = self.db._load_json(self.db.routines_file)
        notification_routines = []
        current_time = datetime.now().strftime("%H:%M")
        
        for user_id, user_routines in all_routines_data.items():
            for routine_id, routine in user_routines.items():
                if (routine.get("is_active", True) and 
                    routine.get("reminder_enabled", True) and 
                    routine.get("time") == current_time):
                    
                    if self._should_show_routine_today(routine, routine.get("frequency", "daily")):
                        notification_routines.append({
                            "user_id": int(user_id),
                            "routine_id": routine_id,
                            "routine": routine
                        })
        
        return notification_routines