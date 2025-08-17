"""
অ্যাডমিন ম্যানেজমেন্ট মডিউল
Admin Management Module
"""

from typing import List, Dict, Any
from config.database import db, User, Task, BugReport
from modules.utils.security import security

class AdminManager:
    """অ্যাডমিন ম্যানেজার - Admin Manager"""
    
    def __init__(self):
        self.db = db
    
    async def get_user_statistics(self) -> Dict[str, Any]:
        """Get overall user statistics"""
        with self.db.get_session() as session:
            total_users = session.query(User).count()
            active_users = session.query(User).filter(User.is_active == True).count()
            total_tasks = session.query(Task).count()
            completed_tasks = session.query(Task).filter(Task.status == 'completed').count()
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
    
    async def get_bug_reports(self, status: str = 'open') -> List[Dict[str, Any]]:
        """Get bug reports"""
        with self.db.get_session() as session:
            reports = session.query(BugReport).filter(BugReport.status == status).all()
            return [
                {
                    'id': report.id,
                    'title': report.title,
                    'severity': report.severity,
                    'created_at': report.created_at.isoformat() if report.created_at else None
                }
                for report in reports
            ]
    
    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return security.is_admin_user(user_id)