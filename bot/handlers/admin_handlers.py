from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
from bot.services.user_service import UserService
from bot.services.notification_service import NotificationService
from bot.services.backup_service import BackupService
from bot.utils.helpers import get_text, is_admin

# Conversation states
BROADCAST_MESSAGE = 1

class AdminHandlers:
    """Handlers for admin operations"""
    
    def __init__(self, user_service: UserService, notification_service: NotificationService, 
                 backup_service: BackupService, admin_user_ids: list):
        self.user_service = user_service
        self.notification_service = notification_service
        self.backup_service = backup_service
        self.admin_user_ids = admin_user_ids
    
    def _is_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        return is_admin(user_id, self.admin_user_ids)
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /admin command"""
        user_id = update.effective_user.id
        
        if not self._is_admin(user_id):
            text = get_text("bengali")
            await update.message.reply_text(text["access_denied"])
            return
        
        # Get system statistics
        stats = self.backup_service.get_system_stats()
        
        admin_text = f"""
🔧 *অ্যাডমিন প্যানেল*

👥 *ব্যবহারকারী পরিসংখ্যান:*
• মোট ব্যবহারকারী: {stats['total_users']}
• সক্রিয় ব্যবহারকারী: {stats['active_users']}

📊 *রুটিন পরিসংখ্যান:*
• মোট রুটিন: {stats['total_routines']}
• মোট সম্পন্ন: {stats['total_completions']}

💾 *ডেটা আকার:*
• ব্যবহারকারী: {stats['data_sizes']['users_kb']} KB
• রুটিন: {stats['data_sizes']['routines_kb']} KB
• রিপোর্ট: {stats['data_sizes']['reports_kb']} KB

🗄️ ব্যাকআপ: {stats['backups_count']} টি
        """
        
        keyboard = [
            [InlineKeyboardButton("📢 ব্রডকাস্ট", callback_data="admin_broadcast")],
            [InlineKeyboardButton("💾 ব্যাকআপ তৈরি", callback_data="admin_backup"),
             InlineKeyboardButton("📊 বিস্তারিত স্ট্যাট", callback_data="admin_stats")],
            [InlineKeyboardButton("👥 ব্যবহারকারী তালিকা", callback_data="admin_users"),
             InlineKeyboardButton("🗄️ ব্যাকআপ তালিকা", callback_data="admin_backup_list")]
        ]
        
        await update.message.reply_text(
            admin_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def admin_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle admin callback buttons"""
        query = update.callback_query
        user_id = query.from_user.id
        data = query.data
        
        if not self._is_admin(user_id):
            await query.answer("❌ অনুমতি নেই।")
            return
        
        if data == "admin_broadcast":
            await query.edit_message_text(
                "📢 *ব্রডকাস্ট বার্তা*\n\nসবার কাছে পাঠাতে বার্তা লিখুন:",
                parse_mode='Markdown'
            )
            return BROADCAST_MESSAGE
            
        elif data == "admin_backup":
            backup_name = self.backup_service.create_backup()
            await query.edit_message_text(
                f"✅ *ব্যাকআপ সম্পন্ন*\n\nব্যাকআপ তৈরি হয়েছে: `{backup_name}`",
                parse_mode='Markdown'
            )
            
        elif data == "admin_stats":
            await self._show_detailed_stats(query)
            
        elif data == "admin_users":
            await self._show_user_list(query)
            
        elif data == "admin_backup_list":
            await self._show_backup_list(query)
    
    async def broadcast_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle broadcast message input"""
        user_id = update.effective_user.id
        
        if not self._is_admin(user_id):
            await update.message.reply_text("❌ অনুমতি নেই।")
            return ConversationHandler.END
        
        message = update.message.text
        
        if len(message.strip()) < 5:
            await update.message.reply_text("বার্তা খুবই ছোট। আবার চেষ্টা করুন।")
            return BROADCAST_MESSAGE
        
        # Send broadcast
        await update.message.reply_text("📤 ব্রডকাস্ট পাঠানো হচ্ছে...")
        
        sent_count = await self.notification_service.send_broadcast_message(user_id, message)
        
        await update.message.reply_text(
            f"✅ *ব্রডকাস্ট সম্পন্ন*\n\n{sent_count} জন ব্যবহারকারীর কাছে বার্তা পাঠানো হয়েছে।",
            parse_mode='Markdown'
        )
        
        return ConversationHandler.END
    
    async def _show_detailed_stats(self, query):
        """Show detailed system statistics"""
        stats = self.backup_service.get_system_stats()
        users = self.user_service.get_all_users()
        
        # Calculate more detailed stats
        languages = {}
        recent_users = 0
        from datetime import datetime, timedelta
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        
        for user_data in users.values():
            lang = user_data.get('language', 'bengali')
            languages[lang] = languages.get(lang, 0) + 1
            
            if user_data.get('created_at', '') > week_ago:
                recent_users += 1
        
        detailed_text = f"""
📊 *বিস্তারিত পরিসংখ্যান*

👥 *ব্যবহারকারী বিশ্লেষণ:*
• মোট: {stats['total_users']}
• সক্রিয়: {stats['active_users']}
• নতুন (৭ দিন): {recent_users}

🌐 *ভাষা বিতরণ:*
{chr(10).join([f"• {lang}: {count}" for lang, count in languages.items()])}

📈 *কার্যকলাপ:*
• মোট রুটিন: {stats['total_routines']}
• মোট সম্পন্ন: {stats['total_completions']}
• গড় রুটিন/ব্যবহারকারী: {stats['total_routines']/stats['total_users']:.1f}

💾 *সিস্টেম তথ্য:*
• ডেটা আকার: {sum(stats['data_sizes'].values()):.1f} KB
• ব্যাকআপ: {stats['backups_count']} টি
        """
        
        await query.edit_message_text(detailed_text, parse_mode='Markdown')
    
    async def _show_user_list(self, query):
        """Show recent users list"""
        users = self.user_service.get_all_users()
        
        # Sort by creation date (recent first)
        sorted_users = sorted(
            users.items(), 
            key=lambda x: x[1].get('created_at', ''), 
            reverse=True
        )
        
        user_list = "👥 *ব্যবহারকারী তালিকা* (সর্বশেষ ২০ জন)\n\n"
        
        for i, (user_id, user_data) in enumerate(sorted_users[:20]):
            status = "🟢" if user_data.get('is_active', True) else "🔴"
            name = user_data.get('name', 'N/A')
            join_date = user_data.get('created_at', '')[:10]
            user_list += f"{status} {name} | {user_id}\n   📅 {join_date}\n\n"
        
        if len(sorted_users) > 20:
            user_list += f"... এবং আরো {len(sorted_users) - 20} জন"
        
        await query.edit_message_text(user_list, parse_mode='Markdown')
    
    async def _show_backup_list(self, query):
        """Show backup list"""
        backups = self.backup_service.list_backups()
        
        if not backups:
            await query.edit_message_text("🗄️ *ব্যাকআপ তালিকা*\n\nকোন ব্যাকআপ নেই।")
            return
        
        backup_text = "🗄️ *ব্যাকআপ তালিকা*\n\n"
        
        # Sort by name (which includes timestamp)
        for backup in sorted(backups, reverse=True):
            backup_text += f"📦 `{backup}`\n"
        
        await query.edit_message_text(backup_text, parse_mode='Markdown')
    
    async def cancel_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel broadcast process"""
        await update.message.reply_text("❌ ব্রডকাস্ট বাতিল করা হয়েছে।")
        return ConversationHandler.END

# Conversation handler for broadcast
def get_broadcast_conversation_handler(admin_handlers):
    """Get broadcast conversation handler"""
    return ConversationHandler(
        entry_points=[admin_handlers.admin_callback],
        states={
            BROADCAST_MESSAGE: [admin_handlers.broadcast_message]
        },
        fallbacks=[admin_handlers.cancel_broadcast]
    )