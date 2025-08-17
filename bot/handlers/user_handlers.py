from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from bot.services.user_service import UserService
from bot.utils.helpers import get_text, create_main_menu_keyboard
from bot.utils.validators import validate_name, validate_age

# Conversation states
REGISTER_NAME, REGISTER_AGE = range(2)
SETTINGS_MENU, CHANGE_LANGUAGE, EDIT_PROFILE = range(3, 6)

class UserHandlers:
    """Handlers for user-related operations"""
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        if self.user_service.is_user_registered(user_id):
            # User is registered, show welcome message and menu
            await update.message.reply_text(
                text["welcome"] + "\n\n" + text["start_message"],
                parse_mode='Markdown',
                reply_markup=create_main_menu_keyboard()
            )
        else:
            # User not registered, prompt registration
            await update.message.reply_text(text["registration_needed"])
    
    async def register_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /register command"""
        user_id = update.effective_user.id
        
        if self.user_service.is_user_registered(user_id):
            user_lang = self.user_service.get_user_language(user_id)
            text = get_text(user_lang)
            await update.message.reply_text(text["already_registered"])
            return ConversationHandler.END
        
        text = get_text("bengali")  # Default to Bengali for new users
        await update.message.reply_text(text["registration_name"])
        return REGISTER_NAME
    
    async def register_name(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle name input during registration"""
        name = update.message.text
        text = get_text("bengali")
        
        if not validate_name(name):
            await update.message.reply_text(text["invalid_format"])
            return REGISTER_NAME
        
        context.user_data['registration_name'] = name
        await update.message.reply_text(text["registration_age"])
        return REGISTER_AGE
    
    async def register_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle age input during registration"""
        age_str = update.message.text
        text = get_text("bengali")
        
        if not validate_age(age_str):
            await update.message.reply_text(text["invalid_format"])
            return REGISTER_AGE
        
        # Complete registration
        user = update.effective_user
        name = context.user_data['registration_name']
        age = int(age_str)
        
        telegram_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
        
        if self.user_service.register_user(user.id, telegram_data, name, age):
            await update.message.reply_text(
                text["registration_success"],
                reply_markup=create_main_menu_keyboard()
            )
        else:
            await update.message.reply_text(text["error_occurred"])
        
        return ConversationHandler.END
    
    async def cancel_registration(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel registration process"""
        text = get_text("bengali")
        await update.message.reply_text(text["cancelled"])
        return ConversationHandler.END
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu command"""
        user_id = update.effective_user.id
        
        if not self.user_service.is_user_registered(user_id):
            user_lang = "bengali"
            text = get_text(user_lang)
            await update.message.reply_text(text["registration_needed"])
            return
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        await update.message.reply_text(
            "📋 *মূল মেনু* - Main Menu",
            parse_mode='Markdown',
            reply_markup=create_main_menu_keyboard()
        )
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command"""
        user_id = update.effective_user.id
        user_data = self.user_service.get_user(user_id)
        
        if not user_data:
            text = get_text("bengali")
            await update.message.reply_text(text["registration_needed"])
            return
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        profile_text = f"""
👤 *আপনার প্রোফাইল*

নাম: {user_data['name']}
বয়স: {user_data['age']}
ভাষা: {user_data.get('language', 'bengali')}
নোটিফিকেশন: {'চালু' if user_data.get('notifications_enabled', True) else 'বন্ধ'}
যোগদানের তারিখ: {user_data['created_at'][:10]}
        """
        
        await update.message.reply_text(profile_text, parse_mode='Markdown')
    
    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /settings command"""
        user_id = update.effective_user.id
        
        if not self.user_service.is_user_registered(user_id):
            text = get_text("bengali")
            await update.message.reply_text(text["registration_needed"])
            return
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        keyboard = [
            [InlineKeyboardButton("🌐 ভাষা পরিবর্তন", callback_data="settings_language")],
            [InlineKeyboardButton("🔔 নোটিফিকেশন", callback_data="settings_notifications")],
            [InlineKeyboardButton("👤 প্রোফাইল সম্পাদনা", callback_data="settings_profile")],
            [InlineKeyboardButton("❌ বন্ধ করুন", callback_data="settings_close")]
        ]
        
        await update.message.reply_text(
            text["settings_menu"],
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def settings_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle settings callback buttons"""
        query = update.callback_query
        user_id = query.from_user.id
        data = query.data
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        if data == "settings_language":
            keyboard = [
                [InlineKeyboardButton("বাংলা", callback_data="lang_bengali")],
                [InlineKeyboardButton("English", callback_data="lang_english")],
                [InlineKeyboardButton("🔙 পিছনে", callback_data="settings_back")]
            ]
            
            await query.edit_message_text(
                text["change_language"],
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif data == "settings_notifications":
            user_data = self.user_service.get_user(user_id)
            current_status = user_data.get('notifications_enabled', True)
            new_status = not current_status
            
            self.user_service.update_user_notifications(user_id, new_status)
            status_text = "চালু" if new_status else "বন্ধ"
            
            await query.answer(f"নোটিফিকেশন {status_text} করা হয়েছে")
            await self.settings_command(update, context)
        
        elif data == "settings_close":
            await query.edit_message_text("⚙️ সেটিংস বন্ধ করা হয়েছে।")
        
        elif data.startswith("lang_"):
            language = data.split("_")[1]
            self.user_service.update_user_language(user_id, language)
            
            new_text = get_text(language)
            await query.answer("ভাষা পরিবর্তন হয়েছে!")
            await query.edit_message_text("✅ Language changed successfully!")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = update.effective_user.id
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        await update.message.reply_text(text["help_message"], parse_mode='Markdown')

# Registration conversation handler
def get_registration_conversation_handler(user_handlers):
    """Get registration conversation handler"""
    return ConversationHandler(
        entry_points=[user_handlers.register_command],
        states={
            REGISTER_NAME: [user_handlers.register_name],
            REGISTER_AGE: [user_handlers.register_age]
        },
        fallbacks=[user_handlers.cancel_registration]
    )