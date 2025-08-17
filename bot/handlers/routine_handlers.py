from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from bot.services.routine_service import RoutineService
from bot.services.user_service import UserService
from bot.utils.helpers import get_text, format_routine_list, create_routine_keyboard

# Conversation states
CREATE_ROUTINE_NAME, CREATE_ROUTINE_DESC, CREATE_ROUTINE_TIME, CREATE_ROUTINE_FREQ = range(4)
EDIT_ROUTINE_SELECT, EDIT_ROUTINE_FIELD, EDIT_ROUTINE_VALUE = range(3)

class RoutineHandlers:
    """Handlers for routine-related operations"""
    
    def __init__(self, routine_service: RoutineService, user_service: UserService):
        self.routine_service = routine_service
        self.user_service = user_service
    
    async def create_routine_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /create_routine command or button"""
        user_id = update.effective_user.id
        
        if not self.user_service.is_user_registered(user_id):
            user_lang = "bengali"
            text = get_text(user_lang)
            await update.message.reply_text(text["registration_needed"])
            return ConversationHandler.END
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        await update.message.reply_text(text["routine_name"])
        return CREATE_ROUTINE_NAME
    
    async def create_routine_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle routine name input"""
        name = update.message.text
        user_id = update.effective_user.id
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        if len(name.strip()) < 2:
            await update.message.reply_text(text["invalid_format"])
            return CREATE_ROUTINE_NAME
        
        context.user_data['routine_name'] = name.strip()
        await update.message.reply_text(text["routine_description"])
        return CREATE_ROUTINE_DESC
    
    async def create_routine_description(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle routine description input"""
        description = update.message.text
        user_id = update.effective_user.id
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        if len(description.strip()) < 5:
            await update.message.reply_text(text["invalid_format"])
            return CREATE_ROUTINE_DESC
        
        context.user_data['routine_description'] = description.strip()
        await update.message.reply_text(text["routine_time"])
        return CREATE_ROUTINE_TIME
    
    async def create_routine_time(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle routine time input"""
        time_str = update.message.text
        user_id = update.effective_user.id
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        # Validate time format
        from bot.utils.validators import validate_time_format
        if not validate_time_format(time_str):
            await update.message.reply_text(text["invalid_format"])
            return CREATE_ROUTINE_TIME
        
        context.user_data['routine_time'] = time_str
        
        # Show frequency options
        keyboard = [
            [InlineKeyboardButton(text["daily"], callback_data="freq_daily")],
            [InlineKeyboardButton(text["weekly"], callback_data="freq_weekly")],
            [InlineKeyboardButton(text["monthly"], callback_data="freq_monthly")]
        ]
        
        await update.message.reply_text(
            text["routine_frequency"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return CREATE_ROUTINE_FREQ
    
    async def create_routine_frequency(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle frequency selection"""
        query = update.callback_query
        user_id = query.from_user.id
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        frequency_map = {
            "freq_daily": text["daily"],
            "freq_weekly": text["weekly"],
            "freq_monthly": text["monthly"]
        }
        
        frequency = frequency_map.get(query.data, text["daily"])
        
        # Create the routine
        name = context.user_data['routine_name']
        description = context.user_data['routine_description']
        time = context.user_data['routine_time']
        
        routine_id = self.routine_service.create_routine(
            user_id, name, description, time, frequency
        )
        
        if routine_id:
            await query.edit_message_text(text["routine_created"])
        else:
            await query.edit_message_text(text["error_occurred"])
        
        # Clear user data
        context.user_data.clear()
        return ConversationHandler.END
    
    async def my_routines_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /my_routines command or button"""
        user_id = update.effective_user.id
        
        if not self.user_service.is_user_registered(user_id):
            user_lang = "bengali"
            text = get_text(user_lang)
            await update.message.reply_text(text["registration_needed"])
            return
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        routines = self.routine_service.get_user_routines(user_id)
        
        if not routines:
            await update.message.reply_text(text["no_routines"])
            return
        
        formatted_list = format_routine_list(routines, text)
        keyboard = create_routine_keyboard(routines)
        
        await update.message.reply_text(
            formatted_list,
            parse_mode='Markdown',
            reply_markup=keyboard
        )
    
    async def today_routine_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /today command or button"""
        user_id = update.effective_user.id
        
        if not self.user_service.is_user_registered(user_id):
            user_lang = "bengali"
            text = get_text(user_lang)
            await update.message.reply_text(text["registration_needed"])
            return
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        today_routines = self.routine_service.get_today_routines(user_id)
        
        if not today_routines:
            await update.message.reply_text("📅 আজকের জন্য কোন রুটিন নেই।")
            return
        
        # Format today's routines
        formatted_text = "📅 *আজকের রুটিন:*\n\n"
        keyboard = []
        
        for routine_id, routine in today_routines.items():
            formatted_text += f"⏰ *{routine['name']}*\n"
            formatted_text += f"   সময়: {routine['time']}\n"
            formatted_text += f"   বিবরণ: {routine['description']}\n\n"
            
            # Add action buttons for each routine
            keyboard.append([
                InlineKeyboardButton(f"✅ {routine['name']} সম্পন্ন", 
                                   callback_data=f"complete_{routine_id}"),
                InlineKeyboardButton(f"⏭️ বাদ দিন", 
                                   callback_data=f"skip_{routine_id}")
            ])
        
        await update.message.reply_text(
            formatted_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard) if keyboard else None
        )
    
    async def routine_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle routine-related callbacks"""
        query = update.callback_query
        user_id = query.from_user.id
        data = query.data
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        if data.startswith("routine_"):
            # Show routine details and options
            routine_id = data.replace("routine_", "")
            routine = self.routine_service.get_routine(user_id, routine_id)
            
            if not routine:
                await query.answer(text["routine_not_found"])
                return
            
            routine_text = f"""
📋 *{routine['name']}*

📝 বিবরণ: {routine['description']}
⏰ সময়: {routine['time']}
🔄 ফ্রিকুয়েন্সি: {routine['frequency']}
✅ সম্পন্ন: {routine.get('completed_count', 0)} বার
🔔 স্ট্যাটাস: {'সক্রিয়' if routine.get('is_active', True) else 'নিষ্ক্রিয়'}
            """
            
            keyboard = [
                [InlineKeyboardButton("✅ সম্পন্ন করুন", callback_data=f"complete_{routine_id}")],
                [InlineKeyboardButton("✏️ সম্পাদনা", callback_data=f"edit_{routine_id}"),
                 InlineKeyboardButton("🗑️ মুছুন", callback_data=f"delete_{routine_id}")],
                [InlineKeyboardButton("⏸️ সক্রিয়/নিষ্ক্রিয়", callback_data=f"toggle_{routine_id}")],
                [InlineKeyboardButton("🔙 পিছনে", callback_data="back_to_routines")]
            ]
            
            await query.edit_message_text(
                routine_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif data.startswith("complete_"):
            # Mark routine as completed
            routine_id = data.replace("complete_", "")
            
            if self.routine_service.mark_routine_completed(user_id, routine_id):
                await query.answer("✅ রুটিন সম্পন্ন হিসেবে চিহ্নিত হয়েছে!")
            else:
                await query.answer("❌ ত্রুটি হয়েছে।")
        
        elif data.startswith("delete_"):
            # Delete routine
            routine_id = data.replace("delete_", "")
            
            if self.routine_service.delete_routine(user_id, routine_id):
                await query.edit_message_text(text["routine_deleted"])
            else:
                await query.answer(text["error_occurred"])
        
        elif data.startswith("toggle_"):
            # Toggle routine active status
            routine_id = data.replace("toggle_", "")
            
            if self.routine_service.toggle_routine_active(user_id, routine_id):
                await query.answer("✅ রুটিনের স্ট্যাটাস পরিবর্তন হয়েছে!")
            else:
                await query.answer(text["error_occurred"])
    
    async def cancel_routine_creation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel routine creation"""
        user_id = update.effective_user.id
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        context.user_data.clear()
        await update.message.reply_text(text["cancelled"])
        return ConversationHandler.END

# Conversation handlers
def get_create_routine_conversation_handler(routine_handlers):
    """Get create routine conversation handler"""
    return ConversationHandler(
        entry_points=[routine_handlers.create_routine_command],
        states={
            CREATE_ROUTINE_NAME: [routine_handlers.create_routine_name],
            CREATE_ROUTINE_DESC: [routine_handlers.create_routine_description],
            CREATE_ROUTINE_TIME: [routine_handlers.create_routine_time],
            CREATE_ROUTINE_FREQ: [routine_handlers.create_routine_frequency]
        },
        fallbacks=[routine_handlers.cancel_routine_creation]
    )