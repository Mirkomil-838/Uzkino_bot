import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers.user import router as user_router
from handlers.admin import router as admin_router
from handlers.channels import router as channels_router
from database.db import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found in environment variables")
    
    # Initialize bot and dispatcher
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    # Include routers
    dp.include_router(channels_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)
    
    # Initialize database
    print("✅ Database initialized")
    print("✅ Bot started successfully on Railway!")
    
    # Start polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")