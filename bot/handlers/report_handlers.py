from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from collections import Counter
from bot.services.routine_service import RoutineService
from bot.services.user_service import UserService
from bot.utils.helpers import get_text, get_today_date, get_week_dates, get_month_dates, calculate_success_rate

class ReportHandlers:
    """Handlers for report generation and statistics"""
    
    def __init__(self, routine_service: RoutineService, user_service: UserService):
        self.routine_service = routine_service
        self.user_service = user_service
    
    async def reports_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show reports menu"""
        user_id = update.effective_user.id
        
        if not self.user_service.is_user_registered(user_id):
            user_lang = "bengali"
            text = get_text(user_lang)
            await update.message.reply_text(text["registration_needed"])
            return
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        keyboard = [
            [InlineKeyboardButton(text["daily_report"], callback_data="report_daily")],
            [InlineKeyboardButton(text["weekly_report"], callback_data="report_weekly")],
            [InlineKeyboardButton(text["monthly_report"], callback_data="report_monthly")],
            [InlineKeyboardButton("📈 সর্বকালের পরিসংখ্যান", callback_data="report_all_time")]
        ]
        
        await update.message.reply_text(
            "📊 *রিপোর্ট মেনু*\n\nকোন ধরনের রিপোর্ট দেখতে চান?",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    async def report_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle report callback buttons"""
        query = update.callback_query
        user_id = query.from_user.id
        data = query.data
        
        user_lang = self.user_service.get_user_language(user_id)
        text = get_text(user_lang)
        
        if data == "report_daily":
            await self._generate_daily_report(query, user_id, text)
        elif data == "report_weekly":
            await self._generate_weekly_report(query, user_id, text)
        elif data == "report_monthly":
            await self._generate_monthly_report(query, user_id, text)
        elif data == "report_all_time":
            await self._generate_all_time_report(query, user_id, text)
    
    async def _generate_daily_report(self, query, user_id: int, text: dict):
        """Generate daily report"""
        today = get_today_date()
        today_routines = self.routine_service.get_today_routines(user_id)
        reports = self.routine_service.db.get_user_reports(user_id)
        
        # Get completions for today
        today_completions = [r for r in reports if r['date'] == today]
        completed_count = len(today_completions)
        total_count = len(today_routines)
        
        if total_count == 0:
            report_text = "📅 *আজকের রিপোর্ট*\n\nআজকের জন্য কোন রুটিন নেই।"
        else:
            success_rate = calculate_success_rate(completed_count, total_count)
            
            report_text = f"""
📅 *আজকের রিপোর্ট* ({today})

✅ সম্পন্ন: {completed_count}/{total_count}
📊 সফলতার হার: {success_rate}%

{'🎉 চমৎকার!' if success_rate >= 80 else '💪 আরো ভালো করার চেষ্টা করুন!' if success_rate >= 50 else '⚡ আরো মনোযোগ দিন!'}
            """
            
            # Add details of today's routines
            if today_routines:
                report_text += "\n📋 *আজকের রুটিনসমূহ:*\n"
                for routine_id, routine in today_routines.items():
                    completed_today = any(r['routine_id'] == routine_id for r in today_completions)
                    status = "✅" if completed_today else "⏸️"
                    report_text += f"{status} {routine['name']} ({routine['time']})\n"
        
        await query.edit_message_text(report_text, parse_mode='Markdown')
    
    async def _generate_weekly_report(self, query, user_id: int, text: dict):
        """Generate weekly report"""
        week_start, week_end = get_week_dates()
        reports = self.routine_service.db.get_user_reports(user_id)
        
        # Filter reports for this week
        week_reports = []
        for report in reports:
            if week_start <= report['date'] <= week_end:
                week_reports.append(report)
        
        # Get all routines to calculate total possible completions
        user_routines = self.routine_service.get_user_routines(user_id)
        daily_routines = [r for r in user_routines.values() if r.get('frequency') in ['daily', 'প্রতিদিন']]
        
        # Calculate statistics
        completed_count = len(week_reports)
        days_in_week = 7
        total_possible = len(daily_routines) * days_in_week
        
        # Count completions by day
        daily_counts = Counter(report['date'] for report in week_reports)
        
        success_rate = calculate_success_rate(completed_count, total_possible) if total_possible > 0 else 0
        
        report_text = f"""
📈 *সাপ্তাহিক রিপোর্ট*
({week_start} থেকে {week_end})

✅ মোট সম্পন্ন: {completed_count}
📊 সফলতার হার: {success_rate}%
📅 সক্রিয় দিন: {len(daily_counts)}/7

🏆 {'চমৎকার সপ্তাহ!' if success_rate >= 70 else '👍 ভালো!' if success_rate >= 50 else '💪 পরের সপ্তাহ আরো ভালো করুন!'}
        """
        
        # Add daily breakdown
        if daily_counts:
            report_text += "\n📊 *দৈনিক ব্রেকডাউন:*\n"
            for date, count in sorted(daily_counts.items()):
                day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
                report_text += f"{date} ({day_name}): {count} টি\n"
        
        await query.edit_message_text(report_text, parse_mode='Markdown')
    
    async def _generate_monthly_report(self, query, user_id: int, text: dict):
        """Generate monthly report"""
        month_start, month_end = get_month_dates()
        reports = self.routine_service.db.get_user_reports(user_id)
        
        # Filter reports for this month
        month_reports = []
        for report in reports:
            if month_start <= report['date'] <= month_end:
                month_reports.append(report)
        
        # Get routine statistics
        user_routines = self.routine_service.get_user_routines(user_id)
        completed_count = len(month_reports)
        
        # Calculate days in month and active days
        start_date = datetime.strptime(month_start, '%Y-%m-%d')
        end_date = datetime.strptime(month_end, '%Y-%m-%d')
        days_in_month = (end_date - start_date).days + 1
        
        daily_counts = Counter(report['date'] for report in month_reports)
        active_days = len(daily_counts)
        
        # Calculate average per day
        avg_per_day = completed_count / days_in_month if days_in_month > 0 else 0
        
        report_text = f"""
📉 *মাসিক রিপোর্ট*
({start_date.strftime('%B %Y')})

✅ মোট সম্পন্ন: {completed_count}
📅 সক্রিয় দিন: {active_days}/{days_in_month}
📊 দৈনিক গড়: {avg_per_day:.1f}
🎯 সবচেয়ে বেশি: {max(daily_counts.values()) if daily_counts else 0} টি (এক দিনে)

{'🏆 অসাধারণ মাস!' if avg_per_day >= 3 else '👍 ভালো!' if avg_per_day >= 2 else '💪 আরো উন্নতি সম্ভব!'}
        """
        
        # Add weekly breakdown
        if daily_counts:
            # Group by weeks
            week_stats = {}
            for date_str, count in daily_counts.items():
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                week_num = date_obj.isocalendar()[1]
                week_stats[week_num] = week_stats.get(week_num, 0) + count
            
            if len(week_stats) > 1:
                report_text += "\n📈 *সাপ্তাহিক ব্রেকডাউন:*\n"
                for week, count in sorted(week_stats.items()):
                    report_text += f"সপ্তাহ {week}: {count} টি\n"
        
        await query.edit_message_text(report_text, parse_mode='Markdown')
    
    async def _generate_all_time_report(self, query, user_id: int, text: dict):
        """Generate all-time statistics report"""
        reports = self.routine_service.db.get_user_reports(user_id)
        user_routines = self.routine_service.get_user_routines(user_id)
        user_data = self.user_service.get_user(user_id)
        
        if not reports:
            await query.edit_message_text("📊 *সর্বকালের পরিসংখ্যান*\n\nএখনও কোন রুটিন সম্পন্ন করেননি।")
            return
        
        total_completions = len(reports)
        total_routines = len(user_routines)
        
        # Calculate date range
        dates = [report['date'] for report in reports]
        first_completion = min(dates)
        last_completion = max(dates)
        
        # Most completed routines
        routine_counts = Counter(report['routine_id'] for report in reports)
        most_completed_id = routine_counts.most_common(1)[0][0] if routine_counts else None
        most_completed_name = "N/A"
        
        if most_completed_id:
            for routine_id, routine in user_routines.items():
                if routine_id == most_completed_id:
                    most_completed_name = routine['name']
                    break
        
        # Calculate streak and other stats
        daily_counts = Counter(report['date'] for report in reports)
        active_days = len(daily_counts)
        
        # Join date
        join_date = user_data.get('created_at', '').split('T')[0] if user_data else ''
        
        report_text = f"""
📊 *সর্বকালের পরিসংখ্যান*

🎯 মোট রুটিন: {total_routines}
✅ মোট সম্পন্ন: {total_completions}
📅 সক্রিয় দিন: {active_days}
📈 দৈনিক গড়: {total_completions/active_days:.1f}

🏆 সবচেয়ে বেশি সম্পন্ন: 
   {most_completed_name} ({routine_counts[most_completed_id] if most_completed_id else 0} বার)

📆 প্রথম সম্পন্ন: {first_completion}
📆 সর্বশেষ সম্পন্ন: {last_completion}
🗓️ যোগদান: {join_date}

{'🏆 দুর্দান্ত! চালিয়ে যান!' if total_completions >= 50 else '👍 ভালো অগ্রগতি!' if total_completions >= 20 else '💪 আরো নিয়মিত হন!'}
        """
        
        await query.edit_message_text(report_text, parse_mode='Markdown')