from datetime import datetime, timedelta
from typing import Dict, List, Tuple

# Try to import pytz, fallback to basic datetime if not available
try:
    import pytz
    PYTZ_AVAILABLE = True
except ImportError:
    print("⚠️ pytz not installed. Using basic datetime.")
    PYTZ_AVAILABLE = False
    pytz = None

from config.settings import config

class BengaliCalendar:
    """বাংলা ক্যালেন্ডার ক্লাস - Bengali Calendar Class"""
    
    # Bengali month names
    BENGALI_MONTHS = [
        "বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন",
        "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"
    ]
    
    # Bengali day names
    BENGALI_DAYS = [
        "সোমবার", "মঙ্গলবার", "বুধবার", "বৃহস্পতিবার", 
        "শুক্রবার", "শনিবার", "রবিবার"
    ]
    
    # Bengali seasons
    BENGALI_SEASONS = {
        "গ্রীষ্ম": [1, 2],      # বৈশাখ, জ্যৈষ্ঠ
        "বর্ষা": [3, 4],       # আষাঢ়, শ্রাবণ  
        "শরৎ": [5, 6],        # ভাদ্র, আশ্বিন
        "হেমন্ত": [7, 8],      # কার্তিক, অগ্রহায়ণ
        "শীত": [9, 10],       # পৌষ, মাঘ
        "বসন্ত": [11, 12]     # ফাল্গুন, চৈত্র
    }
    
    # Bengali numerals
    BENGALI_NUMERALS = {
        '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
        '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
    }
    
    def __init__(self):
        if PYTZ_AVAILABLE:
            self.timezone = pytz.timezone(config.TIMEZONE)
        else:
            self.timezone = None
    
    def get_current_time(self) -> datetime:
        """Get current time in Bangladesh timezone"""
        if self.timezone:
            return datetime.now(self.timezone)
        else:
            return datetime.now()
    
    def english_to_bengali_number(self, number: str) -> str:
        """Convert English numerals to Bengali"""
        bengali_number = str(number)
        for eng, ben in self.BENGALI_NUMERALS.items():
            bengali_number = bengali_number.replace(eng, ben)
        return bengali_number
    
    def get_bengali_date(self, date: datetime = None) -> Dict[str, str]:
        """Get Bengali date information"""
        if date is None:
            date = self.get_current_time()
        
        # Approximate Bengali calendar conversion
        # This is a simplified conversion - for production, use proper library
        english_year = date.year
        bengali_year = english_year - 593
        
        # Approximate month calculation
        english_month = date.month
        bengali_month_index = (english_month + 8) % 12
        
        bengali_day = date.day
        bengali_weekday = self.BENGALI_DAYS[date.weekday()]
        bengali_month = self.BENGALI_MONTHS[bengali_month_index]
        
        # Get season
        season = self.get_season(bengali_month_index + 1)
        
        return {
            'bengali_date': f"{self.english_to_bengali_number(bengali_day)} {bengali_month} {self.english_to_bengali_number(bengali_year)}",
            'bengali_year': self.english_to_bengali_number(str(bengali_year)),
            'bengali_month': bengali_month,
            'bengali_day': self.english_to_bengali_number(str(bengali_day)),
            'bengali_weekday': bengali_weekday,
            'season': season,
            'english_date': date.strftime('%d %B %Y'),
            'english_time': date.strftime('%I:%M %p')
        }
    
    def get_season(self, bengali_month: int) -> str:
        """Get Bengali season name"""
        for season, months in self.BENGALI_SEASONS.items():
            if bengali_month in months:
                return season
        return "অজানা"
    
    def format_time_bengali(self, time: datetime) -> str:
        """Format time in Bengali"""
        hour = time.hour
        minute = time.minute
        
        if hour == 0:
            hour_str = "১২"
            period = "রাত"
        elif hour < 12:
            hour_str = self.english_to_bengali_number(str(hour))
            period = "সকাল" if hour < 10 else "দুপুর"
        elif hour == 12:
            hour_str = "১২"
            period = "দুপুর"
        else:
            hour_str = self.english_to_bengali_number(str(hour - 12))
            period = "বিকাল" if hour < 18 else "রাত"
        
        minute_str = self.english_to_bengali_number(str(minute).zfill(2))
        
        return f"{hour_str}:{minute_str} {period}"
    
    def get_upcoming_events(self, date: datetime = None, days_ahead: int = 7) -> List[Dict]:
        """Get upcoming Bengali calendar events"""
        if date is None:
            date = self.get_current_time()
        
        events = []
        
        # Add some common Bengali festivals/events
        bengali_events = [
            {"name": "পহেলা বৈশাখ", "month": 1, "day": 1, "description": "বাংলা নববর্ষ"},
            {"name": "রবীন্দ্র জয়ন্তী", "month": 1, "day": 25, "description": "কবিগুরুর জন্মদিন"},
            {"name": "নজরুল জয়ন্তী", "month": 2, "day": 11, "description": "বিদ্রোহী কবির জন্মদিন"}
        ]
        
        for event in bengali_events:
            # This is a simplified calculation
            # In production, use proper Bengali calendar library
            events.append({
                "name": event["name"],
                "description": event["description"],
                "bengali_date": f"{event['day']} {self.BENGALI_MONTHS[event['month']-1]}",
                "is_today": False  # Simplified
            })
        
        return events[:3]  # Return first 3 events

# Global instance
bengali_calendar = BengaliCalendar()