"""
টাস্ক ম্যানেজমেন্ট মডিউল
Task Management Module
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from config.database import db, Task, User
from modules.utils.localization import _
import json

class TaskManager:
    """টাস্ক ম্যানেজার - Task Manager"""
    
    def __init__(self):
        self.db = db
    
    async def create_task(
        self,
        user_id: int,
        title: str,
        description: str = None,
        priority: str = 'medium',
        category: str = None,
        due_date: datetime = None,
        reminder_time: datetime = None,
        repeat_type: str = None,
        repeat_interval: int = 1,
        attachments: List[Dict] = None,
        voice_note_url: str = None,
        dependencies: List[int] = None
    ) -> Task:
        """Create new task"""
        
        with self.db.get_session() as session:
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                priority=priority,
                category=category,
                due_date=due_date,
                reminder_time=reminder_time,
                repeat_type=repeat_type,
                repeat_interval=repeat_interval,
                attachments=attachments or [],
                voice_note_url=voice_note_url,
                dependencies=dependencies or []
            )
            
            session.add(task)
            session.commit()
            session.refresh(task)
            return task
    
    async def get_user_tasks(
        self,
        user_id: int,
        status: str = None,
        category: str = None,
        priority: str = None,
        limit: int = 50
    ) -> List[Dict]:
        """Get user tasks with filters"""
        
        with self.db.get_session() as session:
            query = session.query(Task).filter(Task.user_id == user_id)
            
            if status:
                query = query.filter(Task.status == status)
            if category:
                query = query.filter(Task.category == category)
            if priority:
                query = query.filter(Task.priority == priority)
            
            tasks = query.order_by(Task.created_at.desc()).limit(limit).all()
            
            return [self._task_to_dict(task) for task in tasks]
    
    async def get_upcoming_tasks(self, user_id: int, days_ahead: int = 7) -> List[Dict]:
        """Get upcoming tasks"""
        
        with self.db.get_session() as session:
            end_date = datetime.utcnow() + timedelta(days=days_ahead)
            
            tasks = session.query(Task).filter(
                Task.user_id == user_id,
                Task.status == 'pending',
                Task.due_date.isnot(None),
                Task.due_date <= end_date
            ).order_by(Task.due_date).all()
            
            return [self._task_to_dict(task) for task in tasks]
    
    async def complete_task(self, task_id: int, user_id: int) -> bool:
        """Mark task as completed"""
        
        with self.db.get_session() as session:
            task = session.query(Task).filter(
                Task.id == task_id,
                Task.user_id == user_id
            ).first()
            
            if task:
                task.status = 'completed'
                task.completed_at = datetime.utcnow()
                task.completion_rate = 100.0
                session.commit()
                
                # Create repeat task if needed
                if task.repeat_type:
                    await self._create_repeat_task(task, session)
                
                return True
            return False
    
    async def snooze_task(self, task_id: int, user_id: int, snooze_until: datetime) -> bool:
        """Snooze task until specified time"""
        
        with self.db.get_session() as session:
            task = session.query(Task).filter(
                Task.id == task_id,
                Task.user_id == user_id
            ).first()
            
            if task:
                task.status = 'snoozed'
                task.snooze_until = snooze_until
                session.commit()
                return True
            return False
    
    async def update_task(self, task_id: int, user_id: int, **updates) -> bool:
        """Update task"""
        
        with self.db.get_session() as session:
            task = session.query(Task).filter(
                Task.id == task_id,
                Task.user_id == user_id
            ).first()
            
            if task:
                for key, value in updates.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                
                task.updated_at = datetime.utcnow()
                session.commit()
                return True
            return False
    
    async def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete task"""
        
        with self.db.get_session() as session:
            task = session.query(Task).filter(
                Task.id == task_id,
                Task.user_id == user_id
            ).first()
            
            if task:
                session.delete(task)
                session.commit()
                return True
            return False
    
    async def get_task_statistics(self, user_id: int) -> Dict[str, Any]:
        """Get task statistics for user"""
        
        with self.db.get_session() as session:
            total_tasks = session.query(Task).filter(Task.user_id == user_id).count()
            completed_tasks = session.query(Task).filter(
                Task.user_id == user_id,
                Task.status == 'completed'
            ).count()
            pending_tasks = session.query(Task).filter(
                Task.user_id == user_id,
                Task.status == 'pending'
            ).count()
            overdue_tasks = session.query(Task).filter(
                Task.user_id == user_id,
                Task.status == 'pending',
                Task.due_date.isnot(None),
                Task.due_date < datetime.utcnow()
            ).count()
            
            # Category breakdown
            categories = {}
            for category, in session.query(Task.category).filter(
                Task.user_id == user_id,
                Task.category.isnot(None)
            ).distinct():
                count = session.query(Task).filter(
                    Task.user_id == user_id,
                    Task.category == category
                ).count()
                categories[category] = count
            
            completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            
            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'overdue_tasks': overdue_tasks,
                'completion_rate': round(completion_rate, 2),
                'categories': categories
            }
    
    async def export_tasks(self, user_id: int, format: str = 'json') -> str:
        """Export user tasks to JSON/CSV format"""
        
        tasks = await self.get_user_tasks(user_id, limit=1000)
        
        if format.lower() == 'json':
            return json.dumps(tasks, indent=2, ensure_ascii=False, default=str)
        elif format.lower() == 'csv':
            # Simple CSV export
            if not tasks:
                return ""
            
            headers = ['Title', 'Description', 'Priority', 'Category', 'Status', 'Due Date', 'Created At']
            csv_lines = [','.join(headers)]
            
            for task in tasks:
                row = [
                    task.get('title', ''),
                    task.get('description', ''),
                    task.get('priority', ''),
                    task.get('category', ''),
                    task.get('status', ''),
                    str(task.get('due_date', '')),
                    str(task.get('created_at', ''))
                ]
                csv_lines.append(','.join(f'"{item}"' for item in row))
            
            return '\n'.join(csv_lines)
        
        return ""
    
    async def import_tasks(self, user_id: int, data: str, format: str = 'json') -> int:
        """Import tasks from JSON/CSV data"""
        imported_count = 0
        
        try:
            if format.lower() == 'json':
                tasks_data = json.loads(data)
                
                for task_data in tasks_data:
                    await self.create_task(
                        user_id=user_id,
                        title=task_data.get('title', 'Imported Task'),
                        description=task_data.get('description'),
                        priority=task_data.get('priority', 'medium'),
                        category=task_data.get('category'),
                        due_date=self._parse_datetime(task_data.get('due_date'))
                    )
                    imported_count += 1
            
        except Exception as e:
            print(f"Import error: {e}")
        
        return imported_count
    
    async def get_dependent_tasks(self, task_id: int) -> List[Dict]:
        """Get tasks that depend on this task"""
        
        with self.db.get_session() as session:
            tasks = session.query(Task).all()
            dependent_tasks = []
            
            for task in tasks:
                if task.dependencies and task_id in task.dependencies:
                    dependent_tasks.append(self._task_to_dict(task))
            
            return dependent_tasks
    
    async def can_complete_task(self, task_id: int) -> bool:
        """Check if task can be completed (all dependencies completed)"""
        
        with self.db.get_session() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            
            if not task or not task.dependencies:
                return True
            
            for dep_id in task.dependencies:
                dep_task = session.query(Task).filter(Task.id == dep_id).first()
                if not dep_task or dep_task.status != 'completed':
                    return False
            
            return True
    
    def _task_to_dict(self, task: Task) -> Dict:
        """Convert Task object to dictionary"""
        return {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'category': task.category,
            'status': task.status,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'reminder_time': task.reminder_time.isoformat() if task.reminder_time else None,
            'repeat_type': task.repeat_type,
            'repeat_interval': task.repeat_interval,
            'snooze_until': task.snooze_until.isoformat() if task.snooze_until else None,
            'completion_rate': task.completion_rate,
            'attachments': task.attachments,
            'voice_note_url': task.voice_note_url,
            'dependencies': task.dependencies,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'updated_at': task.updated_at.isoformat() if task.updated_at else None,
            'completed_at': task.completed_at.isoformat() if task.completed_at else None
        }
    
    def _parse_datetime(self, date_str: str) -> Optional[datetime]:
        """Parse datetime string"""
        if not date_str:
            return None
        
        try:
            # Try different formats
            formats = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S']
            for fmt in formats:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
        except:
            pass
        
        return None
    
    async def _create_repeat_task(self, original_task: Task, session: Session):
        """Create repeat task based on original task"""
        
        if original_task.repeat_type == 'daily':
            new_due_date = original_task.due_date + timedelta(days=original_task.repeat_interval)
        elif original_task.repeat_type == 'weekly':
            new_due_date = original_task.due_date + timedelta(weeks=original_task.repeat_interval)
        elif original_task.repeat_type == 'monthly':
            new_due_date = original_task.due_date + timedelta(days=30 * original_task.repeat_interval)
        else:
            return
        
        new_task = Task(
            user_id=original_task.user_id,
            title=original_task.title,
            description=original_task.description,
            priority=original_task.priority,
            category=original_task.category,
            due_date=new_due_date,
            reminder_time=new_due_date - timedelta(hours=1) if new_due_date else None,
            repeat_type=original_task.repeat_type,
            repeat_interval=original_task.repeat_interval,
            attachments=original_task.attachments,
            dependencies=original_task.dependencies
        )
        
        session.add(new_task)
        session.commit()