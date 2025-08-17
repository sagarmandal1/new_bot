# -*- coding: utf-8 -*-
"""
Data storage management with JSON database and auto-backup
Windows-compatible UTF-8 encoding
"""

import json
import os
import shutil
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from constants import DATA_FILE, BACKUP_DIR, DEFAULT_TIMEZONE

logger = logging.getLogger(__name__)

class StorageManager:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.backup_dir = BACKUP_DIR
        self._ensure_directories()
        self._init_data_structure()
    
    def _ensure_directories(self):
        """Create necessary directories if they don't exist"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def _init_data_structure(self):
        """Initialize data structure if file doesn't exist"""
        if not os.path.exists(self.data_file):
            default_data = {
                "users": {},
                "metadata": {
                    "version": "1.0",
                    "created": datetime.now(timezone.utc).isoformat(),
                    "last_backup": None
                }
            }
            self._save_data(default_data)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load data from JSON file with UTF-8 encoding"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error loading data: {e}")
            return {
                "users": {},
                "metadata": {
                    "version": "1.0",
                    "created": datetime.now(timezone.utc).isoformat(),
                    "last_backup": None
                }
            }
    
    def _save_data(self, data: Dict[str, Any]):
        """Save data to JSON file with UTF-8 encoding"""
        try:
            # Create backup before saving
            if os.path.exists(self.data_file):
                backup_name = f"bot_data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_path = os.path.join(self.backup_dir, backup_name)
                shutil.copy2(self.data_file, backup_path)
                
                # Update last backup time
                data["metadata"]["last_backup"] = datetime.now(timezone.utc).isoformat()
                
                # Keep only last 10 backups
                self._cleanup_old_backups()
            
            # Save main data file
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise
    
    def _cleanup_old_backups(self, keep_count: int = 10):
        """Keep only the most recent backup files"""
        try:
            backup_files = [f for f in os.listdir(self.backup_dir) if f.startswith('bot_data_backup_')]
            backup_files.sort(reverse=True)
            
            # Remove old backups
            for backup_file in backup_files[keep_count:]:
                os.remove(os.path.join(self.backup_dir, backup_file))
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
    
    def get_user_data(self, user_id: int) -> Dict[str, Any]:
        """Get user data, create if doesn't exist"""
        data = self._load_data()
        user_id_str = str(user_id)
        
        if user_id_str not in data["users"]:
            # Create new user data structure
            data["users"][user_id_str] = {
                "profile": {
                    "name": "",
                    "timezone": DEFAULT_TIMEZONE,
                    "reminder_interval": 15,
                    "created": datetime.now(timezone.utc).isoformat()
                },
                "routines": [],
                "tasks": [],
                "stats": {
                    "total_routines": 0,
                    "total_tasks": 0,
                    "completed_tasks": 0,
                    "last_activity": datetime.now(timezone.utc).isoformat()
                }
            }
            self._save_data(data)
        
        return data["users"][user_id_str]
    
    def update_user_profile(self, user_id: int, profile_data: Dict[str, Any]):
        """Update user profile information"""
        data = self._load_data()
        user_id_str = str(user_id)
        user_data = self.get_user_data(user_id)
        
        user_data["profile"].update(profile_data)
        data["users"][user_id_str] = user_data
        self._save_data(data)
    
    def add_routine(self, user_id: int, routine_data: Dict[str, Any]) -> str:
        """Add a new routine for user"""
        data = self._load_data()
        user_id_str = str(user_id)
        user_data = self.get_user_data(user_id)
        
        # Generate routine ID
        routine_id = f"routine_{len(user_data['routines']) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        routine = {
            "id": routine_id,
            "name": routine_data["name"],
            "time": routine_data["time"],
            "days": routine_data.get("days", []),
            "type": routine_data.get("type", "daily"),
            "reminder_intervals": routine_data.get("reminder_intervals", [15]),
            "active": True,
            "created": datetime.now(timezone.utc).isoformat(),
            "last_completed": None
        }
        
        user_data["routines"].append(routine)
        user_data["stats"]["total_routines"] += 1
        user_data["stats"]["last_activity"] = datetime.now(timezone.utc).isoformat()
        
        data["users"][user_id_str] = user_data
        self._save_data(data)
        
        return routine_id
    
    def get_user_routines(self, user_id: int, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get user routines"""
        user_data = self.get_user_data(user_id)
        routines = user_data["routines"]
        
        if active_only:
            routines = [r for r in routines if r.get("active", True)]
        
        return routines
    
    def update_routine(self, user_id: int, routine_id: str, update_data: Dict[str, Any]):
        """Update a routine"""
        data = self._load_data()
        user_id_str = str(user_id)
        user_data = self.get_user_data(user_id)
        
        for i, routine in enumerate(user_data["routines"]):
            if routine["id"] == routine_id:
                routine.update(update_data)
                break
        
        data["users"][user_id_str] = user_data
        self._save_data(data)
    
    def delete_routine(self, user_id: int, routine_id: str):
        """Delete a routine"""
        data = self._load_data()
        user_id_str = str(user_id)
        user_data = self.get_user_data(user_id)
        
        user_data["routines"] = [r for r in user_data["routines"] if r["id"] != routine_id]
        
        data["users"][user_id_str] = user_data
        self._save_data(data)
    
    def add_task(self, user_id: int, task_data: Dict[str, Any]) -> str:
        """Add a new task for user"""
        data = self._load_data()
        user_id_str = str(user_id)
        user_data = self.get_user_data(user_id)
        
        # Generate task ID
        task_id = f"task_{len(user_data['tasks']) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        task = {
            "id": task_id,
            "name": task_data["name"],
            "deadline": task_data.get("deadline"),
            "reminder_intervals": task_data.get("reminder_intervals", [15]),
            "completed": False,
            "created": datetime.now(timezone.utc).isoformat(),
            "completed_at": None
        }
        
        user_data["tasks"].append(task)
        user_data["stats"]["total_tasks"] += 1
        user_data["stats"]["last_activity"] = datetime.now(timezone.utc).isoformat()
        
        data["users"][user_id_str] = user_data
        self._save_data(data)
        
        return task_id
    
    def get_user_tasks(self, user_id: int, completed: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Get user tasks, optionally filtered by completion status"""
        user_data = self.get_user_data(user_id)
        tasks = user_data["tasks"]
        
        if completed is not None:
            tasks = [t for t in tasks if t.get("completed", False) == completed]
        
        return tasks
    
    def complete_task(self, user_id: int, task_id: str):
        """Mark a task as completed"""
        data = self._load_data()
        user_id_str = str(user_id)
        user_data = self.get_user_data(user_id)
        
        for task in user_data["tasks"]:
            if task["id"] == task_id and not task.get("completed", False):
                task["completed"] = True
                task["completed_at"] = datetime.now(timezone.utc).isoformat()
                user_data["stats"]["completed_tasks"] += 1
                break
        
        user_data["stats"]["last_activity"] = datetime.now(timezone.utc).isoformat()
        data["users"][user_id_str] = user_data
        self._save_data(data)
    
    def delete_task(self, user_id: int, task_id: str):
        """Delete a task"""
        data = self._load_data()
        user_id_str = str(user_id)
        user_data = self.get_user_data(user_id)
        
        # Check if task was completed before deleting for stats
        task_to_delete = next((t for t in user_data["tasks"] if t["id"] == task_id), None)
        if task_to_delete and task_to_delete.get("completed", False):
            user_data["stats"]["completed_tasks"] -= 1
        
        user_data["tasks"] = [t for t in user_data["tasks"] if t["id"] != task_id]
        user_data["stats"]["total_tasks"] -= 1
        
        data["users"][user_id_str] = user_data
        self._save_data(data)
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        user_data = self.get_user_data(user_id)
        stats = user_data["stats"].copy()
        
        # Calculate additional stats
        pending_tasks = len([t for t in user_data["tasks"] if not t.get("completed", False)])
        stats["pending_tasks"] = pending_tasks
        
        if stats["total_tasks"] > 0:
            stats["completion_rate"] = round((stats["completed_tasks"] / stats["total_tasks"]) * 100, 1)
        else:
            stats["completion_rate"] = 0.0
        
        return stats
    
    def manual_backup(self) -> str:
        """Create manual backup and return backup file path"""
        data = self._load_data()
        backup_name = f"manual_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return backup_path