# -*- coding: utf-8 -*-
"""
User Interface components for Bengali Telegram bot
Keyboards, menus, and message formatting
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from typing import List, Dict, Any
from constants import BENGALI_TEXT, CALLBACK_DATA, EMOJIS, REMINDER_INTERVALS

class UIManager:
    """Manages all UI components including keyboards and message formatting"""
    
    def __init__(self):
        self.text = BENGALI_TEXT
        self.callbacks = CALLBACK_DATA
        self.emojis = EMOJIS
    
    def get_main_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Main menu keyboard with all primary options"""
        keyboard = [
            [
                InlineKeyboardButton(self.text['btn_routines'], callback_data=self.callbacks['routines']),
                InlineKeyboardButton(self.text['btn_quick_tasks'], callback_data=self.callbacks['tasks'])
            ],
            [
                InlineKeyboardButton(self.text['btn_reminders'], callback_data=self.callbacks['reminders']),
                InlineKeyboardButton(self.text['btn_settings'], callback_data=self.callbacks['settings'])
            ],
            [
                InlineKeyboardButton(self.text['btn_stats'], callback_data=self.callbacks['stats']),
                InlineKeyboardButton(self.text['btn_help'], callback_data=self.callbacks['help'])
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_routine_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Routine management menu"""
        keyboard = [
            [
                InlineKeyboardButton(self.text['btn_add_routine'], callback_data=self.callbacks['add_routine']),
                InlineKeyboardButton(self.text['btn_view_routines'], callback_data=self.callbacks['view_routines'])
            ],
            [
                InlineKeyboardButton(self.text['btn_edit_routine'], callback_data=self.callbacks['edit_routine']),
                InlineKeyboardButton(self.text['btn_delete_routine'], callback_data=self.callbacks['delete_routine'])
            ],
            [
                InlineKeyboardButton(self.text['btn_back'], callback_data=self.callbacks['main_menu'])
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_task_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Task management menu"""
        keyboard = [
            [
                InlineKeyboardButton(self.text['btn_add_task'], callback_data=self.callbacks['add_task']),
                InlineKeyboardButton(self.text['btn_view_tasks'], callback_data=self.callbacks['view_tasks'])
            ],
            [
                InlineKeyboardButton(self.text['btn_complete_task'], callback_data=self.callbacks['complete_task']),
                InlineKeyboardButton(self.text['btn_delete_task'], callback_data=self.callbacks['delete_task'])
            ],
            [
                InlineKeyboardButton(self.text['btn_back'], callback_data=self.callbacks['main_menu'])
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_settings_menu_keyboard(self) -> InlineKeyboardMarkup:
        """Settings menu"""
        keyboard = [
            [
                InlineKeyboardButton(self.text['btn_change_name'], callback_data='change_name')
            ],
            [
                InlineKeyboardButton(self.text['btn_change_timezone'], callback_data='change_timezone')
            ],
            [
                InlineKeyboardButton(self.text['btn_reminder_settings'], callback_data='reminder_settings')
            ],
            [
                InlineKeyboardButton(self.text['btn_back'], callback_data=self.callbacks['main_menu'])
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_back_only_keyboard(self) -> InlineKeyboardMarkup:
        """Simple back button keyboard"""
        keyboard = [
            [InlineKeyboardButton(self.text['btn_back'], callback_data=self.callbacks['main_menu'])]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_cancel_keyboard(self) -> InlineKeyboardMarkup:
        """Cancel operation keyboard"""
        keyboard = [
            [InlineKeyboardButton(self.text['btn_cancel'], callback_data=self.callbacks['cancel'])]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_save_cancel_keyboard(self) -> InlineKeyboardMarkup:
        """Save and cancel keyboard"""
        keyboard = [
            [
                InlineKeyboardButton(self.text['btn_save'], callback_data=self.callbacks['save']),
                InlineKeyboardButton(self.text['btn_cancel'], callback_data=self.callbacks['cancel'])
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_days_selection_keyboard(self, selected_days: List[str] = None) -> InlineKeyboardMarkup:
        """Days of week selection keyboard"""
        if selected_days is None:
            selected_days = []
        
        days = [
            ('monday', self.text['monday']),
            ('tuesday', self.text['tuesday']),
            ('wednesday', self.text['wednesday']),
            ('thursday', self.text['thursday']),
            ('friday', self.text['friday']),
            ('saturday', self.text['saturday']),
            ('sunday', self.text['sunday'])
        ]
        
        keyboard = []
        for i in range(0, len(days), 2):
            row = []
            for j in range(2):
                if i + j < len(days):
                    day_key, day_text = days[i + j]
                    # Add checkmark if selected
                    display_text = f"✅ {day_text}" if day_key in selected_days else day_text
                    row.append(InlineKeyboardButton(display_text, callback_data=f'day_{day_key}'))
            keyboard.append(row)
        
        # Add save and cancel buttons
        keyboard.extend([
            [
                InlineKeyboardButton(self.text['btn_save'], callback_data=self.callbacks['save']),
                InlineKeyboardButton(self.text['btn_cancel'], callback_data=self.callbacks['cancel'])
            ]
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    def get_routine_type_keyboard(self) -> InlineKeyboardMarkup:
        """Routine type selection keyboard"""
        keyboard = [
            [
                InlineKeyboardButton(self.text['daily_routine'], callback_data='type_daily'),
                InlineKeyboardButton(self.text['weekly_routine'], callback_data='type_weekly')
            ],
            [
                InlineKeyboardButton(self.text['btn_cancel'], callback_data=self.callbacks['cancel'])
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def get_reminder_intervals_keyboard(self, selected_intervals: List[int] = None) -> InlineKeyboardMarkup:
        """Reminder intervals selection keyboard"""
        if selected_intervals is None:
            selected_intervals = [15]  # Default
        
        keyboard = []
        interval_texts = {
            5: self.text['reminder_5min'],
            10: self.text['reminder_10min'],
            15: self.text['reminder_15min'],
            30: self.text['reminder_30min'],
            60: self.text['reminder_60min']
        }
        
        for interval in REMINDER_INTERVALS:
            display_text = f"✅ {interval_texts[interval]}" if interval in selected_intervals else interval_texts[interval]
            keyboard.append([InlineKeyboardButton(display_text, callback_data=f'interval_{interval}')])
        
        keyboard.extend([
            [
                InlineKeyboardButton(self.text['btn_save'], callback_data=self.callbacks['save']),
                InlineKeyboardButton(self.text['btn_cancel'], callback_data=self.callbacks['cancel'])
            ]
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    def get_routine_list_keyboard(self, routines: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
        """Dynamic keyboard for routine selection"""
        if not routines:
            return self.get_back_only_keyboard()
        
        keyboard = []
        for routine in routines[:10]:  # Limit to 10 items
            routine_name = routine['name'][:30]  # Truncate long names
            keyboard.append([InlineKeyboardButton(
                f"{self.emojis['routine']} {routine_name}",
                callback_data=f"select_routine_{routine['id']}"
            )])
        
        keyboard.append([InlineKeyboardButton(self.text['btn_back'], callback_data=self.callbacks['routines'])])
        return InlineKeyboardMarkup(keyboard)
    
    def get_task_list_keyboard(self, tasks: List[Dict[str, Any]], action: str = "select") -> InlineKeyboardMarkup:
        """Dynamic keyboard for task selection"""
        if not tasks:
            return self.get_back_only_keyboard()
        
        keyboard = []
        for task in tasks[:10]:  # Limit to 10 items
            task_name = task['name'][:30]  # Truncate long names
            status_emoji = self.emojis['done'] if task.get('completed', False) else self.emojis['pending']
            keyboard.append([InlineKeyboardButton(
                f"{status_emoji} {task_name}",
                callback_data=f"{action}_task_{task['id']}"
            )])
        
        keyboard.append([InlineKeyboardButton(self.text['btn_back'], callback_data=self.callbacks['tasks'])])
        return InlineKeyboardMarkup(keyboard)
    
    def format_routine_details(self, routine: Dict[str, Any]) -> str:
        """Format routine details for display"""
        details = f"{self.emojis['routine']} **{routine['name']}**\n\n"
        details += f"{self.emojis['time']} সময়: {routine['time']}\n"
        
        if routine.get('type') == 'weekly' and routine.get('days'):
            days_bengali = []
            day_mapping = {
                'monday': self.text['monday'],
                'tuesday': self.text['tuesday'],
                'wednesday': self.text['wednesday'],
                'thursday': self.text['thursday'],
                'friday': self.text['friday'],
                'saturday': self.text['saturday'],
                'sunday': self.text['sunday']
            }
            for day in routine['days']:
                days_bengali.append(day_mapping.get(day, day))
            details += f"{self.emojis['date']} দিনসমূহ: {', '.join(days_bengali)}\n"
        else:
            details += f"{self.emojis['daily']} ধরন: দৈনিক\n"
        
        if routine.get('reminder_intervals'):
            intervals = ', '.join([f"{i} মিনিট" for i in routine['reminder_intervals']])
            details += f"{self.emojis['reminder']} রিমাইন্ডার: {intervals}\n"
        
        return details
    
    def format_task_details(self, task: Dict[str, Any]) -> str:
        """Format task details for display"""
        status_emoji = self.emojis['done'] if task.get('completed', False) else self.emojis['pending']
        details = f"{status_emoji} **{task['name']}**\n\n"
        
        if task.get('deadline'):
            details += f"{self.emojis['time']} শেষ সময়: {task['deadline']}\n"
        
        if task.get('completed_at'):
            details += f"{self.emojis['success']} সম্পন্ন: {task['completed_at'][:10]}\n"
        
        if task.get('reminder_intervals'):
            intervals = ', '.join([f"{i} মিনিট" for i in task['reminder_intervals']])
            details += f"{self.emojis['reminder']} রিমাইন্ডার: {intervals}\n"
        
        return details
    
    def format_stats_message(self, stats: Dict[str, Any]) -> str:
        """Format statistics message"""
        message = f"{self.text['stats_title']}\n\n"
        message += f"{self.emojis['routine']} {self.text['total_routines']}: {stats.get('total_routines', 0)}\n"
        message += f"{self.emojis['task']} {self.text['total_tasks']}: {stats.get('total_tasks', 0)}\n"
        message += f"{self.emojis['done']} {self.text['completed_tasks']}: {stats.get('completed_tasks', 0)}\n"
        message += f"{self.emojis['pending']} {self.text['pending_tasks']}: {stats.get('pending_tasks', 0)}\n"
        message += f"{self.emojis['stats']} {self.text['completion_rate']}: {stats.get('completion_rate', 0)}%"
        
        return message
    
    def format_welcome_message(self, user_name: str = "") -> str:
        """Format welcome message"""
        greeting = f"সালাম {user_name}! " if user_name else ""
        return f"{greeting}{self.text['welcome']}\n\n{self.text['choose_option']}"
    
    def format_help_message(self) -> str:
        """Format help message"""
        return self.text['help_text']
    
    def format_routine_list_message(self, routines: List[Dict[str, Any]]) -> str:
        """Format routines list message"""
        if not routines:
            return f"{self.text['no_items_found']}"
        
        message = f"{self.emojis['routine']} আপনার রুটিনসমূহ:\n\n"
        for i, routine in enumerate(routines[:10], 1):
            status = "🟢" if routine.get('active', True) else "🔴"
            message += f"{i}. {status} {routine['name']} - {routine['time']}\n"
        
        if len(routines) > 10:
            message += f"\n... এবং আরও {len(routines) - 10}টি রুটিন"
        
        return message
    
    def format_task_list_message(self, tasks: List[Dict[str, Any]], completed: bool = None) -> str:
        """Format tasks list message"""
        if not tasks:
            return f"{self.text['no_items_found']}"
        
        if completed is True:
            message = f"{self.emojis['done']} সম্পন্ন কাজসমূহ:\n\n"
        elif completed is False:
            message = f"{self.emojis['pending']} বাকি কাজসমূহ:\n\n"
        else:
            message = f"{self.emojis['task']} সকল কাজসমূহ:\n\n"
        
        for i, task in enumerate(tasks[:10], 1):
            status_emoji = self.emojis['done'] if task.get('completed', False) else self.emojis['pending']
            deadline_info = ""
            if task.get('deadline'):
                deadline_info = f" ({task['deadline'][:10]})"
            message += f"{i}. {status_emoji} {task['name']}{deadline_info}\n"
        
        if len(tasks) > 10:
            message += f"\n... এবং আরও {len(tasks) - 10}টি কাজ"
        
        return message