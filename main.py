"""
বাংলা সহায়ক বট - প্রধান এন্ট্রি পয়েন্ট
Bengali Assistant Bot - Main Entry Point
"""

import asyncio
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot import BengaliBot
from config.settings import config

async def main():
    """Main function to run the bot"""
    try:
        # Create bot instance
        bot = BengaliBot()
        
        # Initialize bot
        await bot.initialize()
        
        print(f"🚀 {config.BOT_NAME} v{config.BOT_VERSION} is starting...")
        print(f"📝 Debug mode: {config.DEBUG}")
        print(f"🗄️ Database: {config.DATABASE_URL}")
        print("💡 Make sure you have set your TELEGRAM_BOT_TOKEN in .env file")
        print("-" * 50)
        
        # Run bot
        bot.run()
        
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        if config.DEBUG:
            import traceback
            traceback.print_exc()
    finally:
        print("🛑 Bot shutdown complete")

if __name__ == "__main__":
    # Run the bot
    asyncio.run(main())