# -*- coding: utf-8 -*-
"""
Telegram bot handlers for commands and callbacks
Handles all user interactions with the bot
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from storage import StorageManager
from ui import UIManager
from constants import BENGALI_TEXT, STATES, EMOJIS

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self, storage_manager: StorageManager):
        self.storage = storage_manager
        self.ui = UIManager()
        self.text = BENGALI_TEXT
        self.states = STATES
        self.emojis = EMOJIS
        
        # Temporary storage for conversation states
        self.temp_data = {}
    
    # Command Handlers
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_data = self.storage.get_user_data(user.id)
        
        # Update profile with user info if available
        if not user_data['profile']['name'] and user.first_name:
            self.storage.update_user_profile(user.id, {
                'name': user.first_name
            })
            user_data = self.storage.get_user_data(user.id)
        
        welcome_message = self.ui.format_welcome_message(user_data['profile']['name'])
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=self.ui.get_main_menu_keyboard(),
            parse_mode='Markdown'
        )
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu command"""
        await update.message.reply_text(
            self.text['main_menu'],
            reply_markup=self.ui.get_main_menu_keyboard()
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(
            self.ui.format_help_message(),
            reply_markup=self.ui.get_back_only_keyboard(),
            parse_mode='Markdown'
        )
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user = update.effective_user
        stats = self.storage.get_user_stats(user.id)
        stats_message = self.ui.format_stats_message(stats)
        
        await update.message.reply_text(
            stats_message,
            reply_markup=self.ui.get_back_only_keyboard(),
            parse_mode='Markdown'
        )
    
    # Callback Query Handlers
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all inline keyboard button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = query.from_user.id
        
        # Main menu navigation
        if data == 'main_menu':
            await self.show_main_menu(query, user_id)
        elif data == 'routines':
            await self.show_routine_menu(query)
        elif data == 'tasks':
            await self.show_task_menu(query)
        elif data == 'settings':
            await self.show_settings_menu(query)
        elif data == 'stats':
            await self.show_stats(query, user_id)
        elif data == 'help':
            await self.show_help(query)
        elif data == 'reminders':
            await self.show_reminder_menu(query)
        
        # Routine operations
        elif data == 'add_routine':
            await self.start_add_routine(query, user_id, context)
        elif data == 'view_routines':
            await self.show_routines_list(query, user_id)
        elif data == 'edit_routine':
            await self.show_routines_for_edit(query, user_id)
        elif data == 'delete_routine':
            await self.show_routines_for_delete(query, user_id)
        
        # Task operations
        elif data == 'add_task':
            await self.start_add_task(query, user_id, context)
        elif data == 'view_tasks':
            await self.show_tasks_list(query, user_id)
        elif data == 'complete_task':
            await self.show_tasks_for_completion(query, user_id)
        elif data == 'delete_task':
            await self.show_tasks_for_delete(query, user_id)
        
        # Dynamic callbacks
        elif data.startswith('select_routine_'):
            routine_id = data.replace('select_routine_', '')
            await self.show_routine_details(query, user_id, routine_id)
        elif data.startswith('complete_task_'):
            task_id = data.replace('complete_task_', '')
            await self.complete_task(query, user_id, task_id)
        elif data.startswith('delete_task_'):
            task_id = data.replace('delete_task_', '')
            await self.confirm_delete_task(query, user_id, task_id)
        elif data.startswith('delete_routine_'):
            routine_id = data.replace('delete_routine_', '')
            await self.confirm_delete_routine(query, user_id, routine_id)
        
        # Settings
        elif data == 'change_name':
            await self.start_change_name(query, user_id, context)
        elif data == 'change_timezone':
            await self.show_timezone_options(query)
        elif data == 'reminder_settings':
            await self.show_reminder_settings(query, user_id)
        
        # Cancel operations
        elif data == 'cancel':
            await self.cancel_operation(query, user_id, context)
    
    async def show_main_menu(self, query, user_id):
        """Show main menu"""
        user_data = self.storage.get_user_data(user_id)
        welcome_message = self.ui.format_welcome_message(user_data['profile']['name'])
        
        await query.edit_message_text(
            welcome_message,
            reply_markup=self.ui.get_main_menu_keyboard(),
            parse_mode='Markdown'
        )
    
    async def show_routine_menu(self, query):
        """Show routine management menu"""
        await query.edit_message_text(
            self.text['routine_menu'],
            reply_markup=self.ui.get_routine_menu_keyboard()
        )
    
    async def show_task_menu(self, query):
        """Show task management menu"""
        await query.edit_message_text(
            self.text['task_menu'],
            reply_markup=self.ui.get_task_menu_keyboard()
        )
    
    async def show_settings_menu(self, query):
        """Show settings menu"""
        await query.edit_message_text(
            self.text['settings_menu'],
            reply_markup=self.ui.get_settings_menu_keyboard()
        )
    
    async def show_stats(self, query, user_id):
        """Show user statistics"""
        stats = self.storage.get_user_stats(user_id)
        stats_message = self.ui.format_stats_message(stats)
        
        await query.edit_message_text(
            stats_message,
            reply_markup=self.ui.get_back_only_keyboard(),
            parse_mode='Markdown'
        )
    
    async def show_help(self, query):
        """Show help message"""
        await query.edit_message_text(
            self.ui.format_help_message(),
            reply_markup=self.ui.get_back_only_keyboard(),
            parse_mode='Markdown'
        )
    
    async def show_reminder_menu(self, query):
        """Show reminder menu"""
        message = f"{self.emojis['reminder']} রিমাইন্ডার সিস্টেম\n\n"
        message += "আপনার রুটিন এবং কাজের জন্য স্মার্ট রিমাইন্ডার পেতে সেটিংসে যান।\n\n"
        message += "রিমাইন্ডার সময়:\n"
        message += "🔹 ৫ মিনিট আগে\n"
        message += "🔹 ১০ মিনিট আগে\n"
        message += "🔹 ১৫ মিনিট আগে\n"
        message += "🔹 ৩০ মিনিট আগে\n"
        message += "🔹 ১ ঘন্টা আগে"
        
        await query.edit_message_text(
            message,
            reply_markup=self.ui.get_back_only_keyboard()
        )
    
    async def show_routines_list(self, query, user_id):
        """Show list of user routines"""
        routines = self.storage.get_user_routines(user_id)
        message = self.ui.format_routine_list_message(routines)
        
        await query.edit_message_text(
            message,
            reply_markup=self.ui.get_routine_list_keyboard(routines)
        )
    
    async def show_tasks_list(self, query, user_id):
        """Show list of user tasks"""
        tasks = self.storage.get_user_tasks(user_id)
        message = self.ui.format_task_list_message(tasks)
        
        await query.edit_message_text(
            message,
            reply_markup=self.ui.get_task_list_keyboard(tasks, "select")
        )
    
    async def show_tasks_for_completion(self, query, user_id):
        """Show pending tasks for completion"""
        tasks = self.storage.get_user_tasks(user_id, completed=False)
        message = self.ui.format_task_list_message(tasks, completed=False)
        
        if not tasks:
            message = f"{self.emojis['success']} সমস্ত কাজ সম্পন্ন হয়েছে!"
        
        await query.edit_message_text(
            message,
            reply_markup=self.ui.get_task_list_keyboard(tasks, "complete")
        )
    
    async def show_tasks_for_delete(self, query, user_id):
        """Show tasks for deletion"""
        tasks = self.storage.get_user_tasks(user_id)
        message = self.ui.format_task_list_message(tasks)
        
        await query.edit_message_text(
            message,
            reply_markup=self.ui.get_task_list_keyboard(tasks, "delete")
        )
    
    async def show_routines_for_edit(self, query, user_id):
        """Show routines for editing"""
        routines = self.storage.get_user_routines(user_id)
        message = f"{self.emojis['edit']} সম্পাদনার জন্য রুটিন নির্বাচন করুন:\n\n"
        message += self.ui.format_routine_list_message(routines)
        
        await query.edit_message_text(
            message,
            reply_markup=self.ui.get_routine_list_keyboard(routines)
        )
    
    async def show_routines_for_delete(self, query, user_id):
        """Show routines for deletion"""
        routines = self.storage.get_user_routines(user_id)
        message = f"{self.emojis['delete']} মুছে ফেলার জন্য রুটিন নির্বাচন করুন:\n\n"
        message += self.ui.format_routine_list_message(routines)
        
        # Create delete-specific keyboard
        keyboard = []
        for routine in routines[:10]:
            keyboard.append([InlineKeyboardButton(
                f"{self.emojis['delete']} {routine['name'][:30]}",
                callback_data=f"delete_routine_{routine['id']}"
            )])
        keyboard.append([InlineKeyboardButton(self.text['btn_back'], callback_data='routines')])
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def complete_task(self, query, user_id, task_id):
        """Mark task as completed"""
        try:
            self.storage.complete_task(user_id, task_id)
            await query.edit_message_text(
                self.text['task_completed'],
                reply_markup=self.ui.get_back_only_keyboard()
            )
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            await query.edit_message_text(
                self.text['error_occurred'],
                reply_markup=self.ui.get_back_only_keyboard()
            )
    
    async def confirm_delete_task(self, query, user_id, task_id):
        """Confirm task deletion"""
        keyboard = [
            [
                InlineKeyboardButton(f"{self.emojis['delete']} নিশ্চিত মুছুন", callback_data=f"confirm_delete_task_{task_id}"),
                InlineKeyboardButton(self.text['btn_cancel'], callback_data='tasks')
            ]
        ]
        
        await query.edit_message_text(
            f"{self.emojis['warning']} আপনি কি নিশ্চিত যে এই কাজটি মুছে ফেলতে চান?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def confirm_delete_routine(self, query, user_id, routine_id):
        """Confirm routine deletion"""
        keyboard = [
            [
                InlineKeyboardButton(f"{self.emojis['delete']} নিশ্চিত মুছুন", callback_data=f"confirm_delete_routine_{routine_id}"),
                InlineKeyboardButton(self.text['btn_cancel'], callback_data='routines')
            ]
        ]
        
        await query.edit_message_text(
            f"{self.emojis['warning']} আপনি কি নিশ্চিত যে এই রুটিনটি মুছে ফেলতে চান?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # Conversation handlers for complex operations
    async def start_add_routine(self, query, user_id, context):
        """Start routine creation conversation"""
        self.temp_data[user_id] = {'step': 'routine_name'}
        
        await query.edit_message_text(
            self.text['enter_routine_name'],
            reply_markup=self.ui.get_cancel_keyboard()
        )
        
        return self.states['WAITING_ROUTINE_NAME']
    
    async def start_add_task(self, query, user_id, context):
        """Start task creation conversation"""
        self.temp_data[user_id] = {'step': 'task_name'}
        
        await query.edit_message_text(
            self.text['enter_task_name'],
            reply_markup=self.ui.get_cancel_keyboard()
        )
        
        return self.states['WAITING_TASK_NAME']
    
    async def start_change_name(self, query, user_id, context):
        """Start name change conversation"""
        await query.edit_message_text(
            self.text['enter_profile_name'],
            reply_markup=self.ui.get_cancel_keyboard()
        )
        
        return self.states['WAITING_PROFILE_NAME']
    
    async def cancel_operation(self, query, user_id, context):
        """Cancel current operation"""
        if user_id in self.temp_data:
            del self.temp_data[user_id]
        
        await query.edit_message_text(
            self.text['operation_cancelled'],
            reply_markup=self.ui.get_main_menu_keyboard()
        )
        
        return ConversationHandler.END
    
    # Message handlers for conversation states
    async def handle_routine_name_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle routine name input"""
        user_id = update.effective_user.id
        routine_name = update.message.text.strip()
        
        if not routine_name:
            await update.message.reply_text(
                self.text['invalid_format'],
                reply_markup=self.ui.get_cancel_keyboard()
            )
            return self.states['WAITING_ROUTINE_NAME']
        
        # Store routine name and ask for time
        if user_id not in self.temp_data:
            self.temp_data[user_id] = {}
        
        self.temp_data[user_id]['routine_name'] = routine_name
        self.temp_data[user_id]['step'] = 'routine_time'
        
        await update.message.reply_text(
            self.text['enter_routine_time'],
            reply_markup=self.ui.get_cancel_keyboard()
        )
        
        return self.states['WAITING_ROUTINE_TIME']
    
    async def handle_routine_time_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle routine time input"""
        user_id = update.effective_user.id
        time_input = update.message.text.strip()
        
        # Basic time format validation
        if not self._validate_time_format(time_input):
            await update.message.reply_text(
                f"{self.text['invalid_format']} সঠিক ফরম্যাট: 07:30",
                reply_markup=self.ui.get_cancel_keyboard()
            )
            return self.states['WAITING_ROUTINE_TIME']
        
        # Store time and ask for routine type
        self.temp_data[user_id]['routine_time'] = time_input
        
        await update.message.reply_text(
            f"{self.emojis['date']} রুটিনের ধরন নির্বাচন করুন:",
            reply_markup=self.ui.get_routine_type_keyboard()
        )
        
        return ConversationHandler.END
    
    async def handle_task_name_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle task name input"""
        user_id = update.effective_user.id
        task_name = update.message.text.strip()
        
        if not task_name:
            await update.message.reply_text(
                self.text['invalid_format'],
                reply_markup=self.ui.get_cancel_keyboard()
            )
            return self.states['WAITING_TASK_NAME']
        
        # Create task with basic info
        try:
            task_data = {
                'name': task_name,
                'reminder_intervals': [15]  # Default reminder
            }
            
            task_id = self.storage.add_task(user_id, task_data)
            
            await update.message.reply_text(
                self.text['task_created'],
                reply_markup=self.ui.get_main_menu_keyboard()
            )
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            await update.message.reply_text(
                self.text['error_occurred'],
                reply_markup=self.ui.get_main_menu_keyboard()
            )
        
        return ConversationHandler.END
    
    async def handle_profile_name_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle profile name input"""
        user_id = update.effective_user.id
        new_name = update.message.text.strip()
        
        if not new_name:
            await update.message.reply_text(
                self.text['invalid_format'],
                reply_markup=self.ui.get_cancel_keyboard()
            )
            return self.states['WAITING_PROFILE_NAME']
        
        try:
            self.storage.update_user_profile(user_id, {'name': new_name})
            await update.message.reply_text(
                self.text['settings_saved'],
                reply_markup=self.ui.get_main_menu_keyboard()
            )
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            await update.message.reply_text(
                self.text['error_occurred'],
                reply_markup=self.ui.get_main_menu_keyboard()
            )
        
        return ConversationHandler.END
    
    def _validate_time_format(self, time_str: str) -> bool:
        """Validate time format (HH:MM)"""
        try:
            parts = time_str.split(':')
            if len(parts) != 2:
                return False
            
            hours = int(parts[0])
            minutes = int(parts[1])
            
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except (ValueError, IndexError):
            return False
    
    # Error handler
    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error("Exception while handling an update:", exc_info=context.error)
        
        if isinstance(update, Update) and update.effective_message:
            await update.effective_message.reply_text(
                self.text['error_occurred'],
                reply_markup=self.ui.get_main_menu_keyboard()
            )