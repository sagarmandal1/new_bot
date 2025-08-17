from datetime import datetime, timedelta
from typing import Optional, List

# Try to import SQLAlchemy, if not available use mock classes
try:
    from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, Float
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, relationship, Session
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    print("⚠️ SQLAlchemy not installed. Using mock database classes.")
    SQLALCHEMY_AVAILABLE = False
    
    # Mock SQLAlchemy classes for testing
    class MockBase:
        pass
    
    class MockColumn:
        def __init__(self, *args, **kwargs):
            pass
    
    class MockSession:
        def query(self, *args):
            return self
        def filter(self, *args):
            return self
        def first(self):
            return None
        def all(self):
            return []
        def add(self, obj):
            pass
        def commit(self):
            pass
        def refresh(self, obj):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
    
    # Mock decorators and functions
    declarative_base = lambda: MockBase
    Column = MockColumn
    Integer = String = DateTime = Boolean = Text = JSON = ForeignKey = Float = MockColumn
    relationship = lambda *args, **kwargs: None
    create_engine = lambda *args, **kwargs: None
    sessionmaker = lambda **kwargs: lambda: MockSession()
    Session = MockSession

from config.settings import config
import uuid

Base = declarative_base()

class User(Base):
    """ইউজার মডেল - User Model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    language_code = Column(String(10), default='bn')
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_super_admin = Column(Boolean, default=False)
    avatar_url = Column(String(500), nullable=True)
    timezone = Column(String(50), default='Asia/Dhaka')
    theme = Column(String(20), default='light')  # light/dark
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow)
    settings = Column(JSON, default=dict)
    
    # Relationships
    tasks = relationship("Task", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user")

class Task(Base):
    """টাস্ক মডেল - Task Model"""
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String(20), default='medium')  # low, medium, high, urgent
    category = Column(String(100), nullable=True)
    status = Column(String(20), default='pending')  # pending, completed, snoozed, cancelled
    due_date = Column(DateTime, nullable=True)
    reminder_time = Column(DateTime, nullable=True)
    repeat_type = Column(String(20), nullable=True)  # daily, weekly, monthly, yearly
    repeat_interval = Column(Integer, default=1)
    snooze_until = Column(DateTime, nullable=True)
    completion_rate = Column(Float, default=0.0)
    attachments = Column(JSON, default=list)  # File URLs and metadata
    voice_note_url = Column(String(500), nullable=True)
    dependencies = Column(JSON, default=list)  # Task IDs this task depends on
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="tasks")

class Notification(Base):
    """নোটিফিকেশন মডেল - Notification Model"""
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    type = Column(String(50), nullable=False)  # task_reminder, daily_summary, weekly_summary, etc.
    title = Column(String(500), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    scheduled_for = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, default=dict)
    
    # Relationships
    user = relationship("User", back_populates="notifications")

class ActivityLog(Base):
    """অ্যাক্টিভিটি লগ মডেল - Activity Log Model"""
    __tablename__ = 'activity_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    metadata = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="activity_logs")

class Quote(Base):
    """অনুপ্রেরণামূলক উক্তি মডেল - Motivational Quote Model"""
    __tablename__ = 'quotes'
    
    id = Column(Integer, primary_key=True)
    text_bn = Column(Text, nullable=False)  # Bengali text
    text_en = Column(Text, nullable=True)   # English text
    author_bn = Column(String(200), nullable=True)
    author_en = Column(String(200), nullable=True)
    category = Column(String(50), default='general')
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class GameScore(Base):
    """গেম স্কোর মডেল - Game Score Model"""
    __tablename__ = 'game_scores'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    game_type = Column(String(50), nullable=False)  # quiz, challenge, etc.
    score = Column(Integer, default=0)
    level = Column(Integer, default=1)
    achievements = Column(JSON, default=list)
    total_points = Column(Integer, default=0)
    streak_count = Column(Integer, default=0)
    last_played = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")

class BugReport(Base):
    """বাগ রিপোর্ট মডেল - Bug Report Model"""
    __tablename__ = 'bug_reports'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(String(20), default='medium')  # low, medium, high, critical
    status = Column(String(20), default='open')  # open, in_progress, resolved, closed
    screenshot_url = Column(String(500), nullable=True)
    device_info = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User")

class DatabaseManager:
    """ডাটাবেস ম্যানেজার - Database Manager"""
    
    def __init__(self):
        if SQLALCHEMY_AVAILABLE:
            self.engine = create_engine(
                config.DATABASE_URL,
                pool_pre_ping=True,
                echo=config.DEBUG
            )
            self.SessionLocal = sessionmaker(bind=self.engine)
        else:
            self.engine = None
            self.SessionLocal = MockSession
    
    def create_tables(self):
        """Create all tables"""
        if SQLALCHEMY_AVAILABLE and self.engine:
            Base.metadata.create_all(bind=self.engine)
        else:
            print("ℹ️ Mock database: Tables would be created here")
    
    def get_session(self) -> Session:
        """Get database session"""
        return self.SessionLocal()
    
    def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by telegram ID"""
        with self.get_session() as session:
            return session.query(User).filter(User.telegram_id == telegram_id).first()
    
    def create_user(self, telegram_id: int, first_name: str, **kwargs) -> User:
        """Create new user"""
        with self.get_session() as session:
            user = User(
                telegram_id=telegram_id,
                first_name=first_name,
                **kwargs
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
    
    def get_or_create_user(self, telegram_id: int, first_name: str, **kwargs) -> User:
        """Get existing user or create new one"""
        user = self.get_user_by_telegram_id(telegram_id)
        if not user:
            user = self.create_user(telegram_id, first_name, **kwargs)
        return user

# Create database manager instance
db = DatabaseManager()