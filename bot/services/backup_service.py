import os
import shutil
import json
from datetime import datetime
from bot.utils.database import JSONDatabase

class BackupService:
    """Service for handling backups and data management"""
    
    def __init__(self, db: JSONDatabase):
        self.db = db
    
    def create_backup(self) -> str:
        """Create a full backup"""
        return self.db.create_backup()
    
    def list_backups(self) -> list:
        """List all available backups"""
        return self.db.list_backups()
    
    def restore_backup(self, backup_name: str) -> bool:
        """Restore from backup"""
        return self.db.restore_backup(backup_name)
    
    def export_user_data(self, user_id: int) -> dict:
        """Export all data for a specific user"""
        user_data = self.db.get_user(user_id)
        user_routines = self.db.get_user_routines(user_id)
        user_reports = self.db.get_user_reports(user_id)
        
        return {
            "user_data": user_data,
            "routines": user_routines,
            "reports": user_reports,
            "exported_at": datetime.now().isoformat()
        }
    
    def get_system_stats(self) -> dict:
        """Get system statistics"""
        users = self.db.get_all_users()
        all_routines = self.db._load_json(self.db.routines_file)
        all_reports = self.db._load_json(self.db.reports_file)
        
        # Calculate stats
        total_users = len(users)
        active_users = len([u for u in users.values() if u.get('is_active', True)])
        total_routines = sum(len(routines) for routines in all_routines.values())
        total_completions = sum(len(reports) for reports in all_reports.values())
        
        # Calculate data sizes
        users_size = os.path.getsize(self.db.users_file) if os.path.exists(self.db.users_file) else 0
        routines_size = os.path.getsize(self.db.routines_file) if os.path.exists(self.db.routines_file) else 0
        reports_size = os.path.getsize(self.db.reports_file) if os.path.exists(self.db.reports_file) else 0
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_routines": total_routines,
            "total_completions": total_completions,
            "data_sizes": {
                "users_kb": round(users_size / 1024, 2),
                "routines_kb": round(routines_size / 1024, 2),
                "reports_kb": round(reports_size / 1024, 2)
            },
            "backups_count": len(self.list_backups())
        }