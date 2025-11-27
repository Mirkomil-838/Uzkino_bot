from aiogram import Router
from aiogram.types import Message
from database.db import db
from utils.helpers import extract_movie_code

router = Router()

@router.channel_post()
async def channel_post_handler(message: Message):
    """Handle movie posts in channels"""
    if not message.caption and not message.text:
        return
    
    text = message.caption or message.text
    code = extract_movie_code(text)
    
    if code:
        # Kanal ID sini to'g'ri formatda saqlash
        channel_id = str(message.chat.id)
        print(f"🎬 Movie detected - Code: {code}, Channel: {channel_id}, Message ID: {message.message_id}")
        
        # Save movie to database
        success = db.add_movie(
            code=code,
            channel_id=channel_id,
            message_id=message.message_id,
            caption=text[:1000] if text else ""  # Caption uzunligini cheklash
        )
        if success:
            print(f"✅ Movie saved with code: {code} in channel: {channel_id}")
        else:
            print(f"❌ Error saving movie with code: {code}")