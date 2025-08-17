import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import shutil

class JSONDatabase:
    """JSON-based database for the bot"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.routines_file = os.path.join(data_dir, "routines.json")
        self.reports_file = os.path.join(data_dir, "reports.json")
        self.backup_dir = os.path.join(data_dir, "backups")
        
        # Ensure directories exist
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Initialize files if they don't exist
        self._init_files()
    
    def _init_files(self):
        """Initialize JSON files with empty structures"""
        if not os.path.exists(self.users_file):
            self._save_json(self.users_file, {})
        
        if not os.path.exists(self.routines_file):
            self._save_json(self.routines_file, {})
        
        if not os.path.exists(self.reports_file):
            self._save_json(self.reports_file, {})
    
    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """Load JSON data from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_json(self, file_path: str, data: Dict[str, Any]):
        """Save JSON data to file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # User management
    def create_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """Create a new user"""
        users = self._load_json(self.users_file)
        if str(user_id) in users:
            return False
        
        users[str(user_id)] = {
            **user_data,
            "created_at": datetime.now().isoformat(),
            "is_active": True,
            "language": "bengali",
            "notifications_enabled": True
        }
        
        self._save_json(self.users_file, users)
        return True
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user data"""
        users = self._load_json(self.users_file)
        return users.get(str(user_id))
    
    def update_user(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update user data"""
        users = self._load_json(self.users_file)
        if str(user_id) not in users:
            return False
        
        users[str(user_id)].update(updates)
        users[str(user_id)]["updated_at"] = datetime.now().isoformat()
        
        self._save_json(self.users_file, users)
        return True
    
    def get_all_users(self) -> Dict[str, Any]:
        """Get all users"""
        return self._load_json(self.users_file)
    
    # Routine management
    def create_routine(self, user_id: int, routine_data: Dict[str, Any]) -> str:
        """Create a new routine"""
        routines = self._load_json(self.routines_file)
        if str(user_id) not in routines:
            routines[str(user_id)] = {}
        
        routine_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        routines[str(user_id)][routine_id] = {
            **routine_data,
            "created_at": datetime.now().isoformat(),
            "is_active": True,
            "completed_count": 0,
            "last_completed": None
        }
        
        self._save_json(self.routines_file, routines)
        return routine_id
    
    def get_user_routines(self, user_id: int) -> Dict[str, Any]:
        """Get all routines for a user"""
        routines = self._load_json(self.routines_file)
        return routines.get(str(user_id), {})
    
    def get_routine(self, user_id: int, routine_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific routine"""
        routines = self.get_user_routines(user_id)
        return routines.get(routine_id)
    
    def update_routine(self, user_id: int, routine_id: str, updates: Dict[str, Any]) -> bool:
        """Update a routine"""
        routines = self._load_json(self.routines_file)
        if str(user_id) not in routines or routine_id not in routines[str(user_id)]:
            return False
        
        routines[str(user_id)][routine_id].update(updates)
        routines[str(user_id)][routine_id]["updated_at"] = datetime.now().isoformat()
        
        self._save_json(self.routines_file, routines)
        return True
    
    def delete_routine(self, user_id: int, routine_id: str) -> bool:
        """Delete a routine"""
        routines = self._load_json(self.routines_file)
        if str(user_id) not in routines or routine_id not in routines[str(user_id)]:
            return False
        
        del routines[str(user_id)][routine_id]
        self._save_json(self.routines_file, routines)
        return True
    
    def mark_routine_completed(self, user_id: int, routine_id: str) -> bool:
        """Mark a routine as completed"""
        routines = self._load_json(self.routines_file)
        if str(user_id) not in routines or routine_id not in routines[str(user_id)]:
            return False
        
        routine = routines[str(user_id)][routine_id]
        routine["completed_count"] += 1
        routine["last_completed"] = datetime.now().isoformat()
        
        self._save_json(self.routines_file, routines)
        
        # Also save to reports
        self._save_completion_report(user_id, routine_id, datetime.now().isoformat())
        return True
    
    # Report management
    def _save_completion_report(self, user_id: int, routine_id: str, completed_at: str):
        """Save completion to reports"""
        reports = self._load_json(self.reports_file)
        if str(user_id) not in reports:
            reports[str(user_id)] = []
        
        reports[str(user_id)].append({
            "routine_id": routine_id,
            "completed_at": completed_at,
            "date": completed_at.split('T')[0]
        })
        
        self._save_json(self.reports_file, reports)
    
    def get_user_reports(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all completion reports for a user"""
        reports = self._load_json(self.reports_file)
        return reports.get(str(user_id), [])
    
    # Backup functionality
    def create_backup(self) -> str:
        """Create a backup of all data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        os.makedirs(backup_path, exist_ok=True)
        
        # Copy all JSON files to backup directory
        shutil.copy2(self.users_file, backup_path)
        shutil.copy2(self.routines_file, backup_path)
        shutil.copy2(self.reports_file, backup_path)
        
        return backup_name
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore from a backup"""
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        if not os.path.exists(backup_path):
            return False
        
        try:
            shutil.copy2(os.path.join(backup_path, "users.json"), self.users_file)
            shutil.copy2(os.path.join(backup_path, "routines.json"), self.routines_file)
            shutil.copy2(os.path.join(backup_path, "reports.json"), self.reports_file)
            return True
        except Exception:
            return False
    
    def list_backups(self) -> List[str]:
        """List available backups"""
        if not os.path.exists(self.backup_dir):
            return []
        
        return [name for name in os.listdir(self.backup_dir) 
                if os.path.isdir(os.path.join(self.backup_dir, name))]