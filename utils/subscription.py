from typing import List
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.db import db

async def check_subscription(user_id: int, bot: Bot) -> bool:
    """Check if user is subscribed to all channels"""
    channels = db.get_all_channels()
    
    if not channels:
        return True  # Agar kanal yo'q bo'lsa, obuna tekshirishni o'tkazib yuboramiz
    
    for channel in channels:
        try:
            # Kanal ID sini to'g'ri formatda olish
            chat_id = channel
            
            # Agar @ bilan boshlansa, username sifatida ishlatamiz
            if channel.startswith('@'):
                chat_id = channel
            else:
                # Raqamli ID bo'lsa, integer ga o'tkazamiz
                try:
                    chat_id = int(channel)
                except ValueError:
                    chat_id = channel
            
            # Obunani tekshiramiz
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in ['left', 'kicked']:
                print(f"❌ User {user_id} not subscribed to {channel}")
                return False
                
        except Exception as e:
            print(f"❌ Error checking subscription for {channel}: {e}")
            return False
    
    print(f"✅ User {user_id} subscribed to all channels")
    return True

def create_subscription_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard with channel links"""
    channels = db.get_all_channels()
    keyboard = []
    
    for channel in channels:
        # Kanal linkini to'g'ri yasash
        if channel.startswith('@'):
            channel_username = channel[1:]  # @ ni olib tashlaymiz
            url = f"https://t.me/{channel_username}"
        else:
            # Raqamli ID bo'lsa, username o'rniga ID ishlatamiz
            url = f"https://t.me/c/{channel[4:]}" if str(channel).startswith('-100') else f"https://t.me/{channel}"
        
        keyboard.append([InlineKeyboardButton(
            text=f"📢 Kanalga obuna bo'lish", 
            url=url
        )])
    
    keyboard.append([InlineKeyboardButton(
        text="✅ Tekshirish", 
        callback_data="check_subscription"
    )])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
