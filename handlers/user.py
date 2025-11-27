from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from database.db import db
from utils.subscription import check_subscription, create_subscription_keyboard
from utils.helpers import extract_movie_code

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message, bot: Bot):  # Bot tipini aniq belgilash
    user_id = message.from_user.id
    db.add_user(user_id)
    
    # Debug: kanallar ro'yxatini ko'rsatish
    channels = db.get_all_channels()
    print(f"📋 Available channels: {channels}")
    
    # Check subscription
    is_subscribed = await check_subscription(user_id, bot)
    
    if not is_subscribed:
        await message.answer(
            "🤖 Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n\n"
            "Obuna bo'lgach, «✅ Tekshirish» tugmasini bosing.",
            reply_markup=create_subscription_keyboard()
        )
        return
    
    await message.answer(
        "🎬 Kino Botiga xush kelibsiz!\n\n"
        "Kino kodini yuboring va kino oling.\n"
        "Misol: 123"
    )

@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, bot: Bot):  # Bot tipini aniq belgilash
    user_id = callback.from_user.id
    is_subscribed = await check_subscription(user_id, bot)
    
    if is_subscribed:
        await callback.message.edit_text(
            "✅ Siz barcha kanallarga obuna bo'lgansiz!\n\n"
            "Endi kino kodini yuboring va kino oling.\n"
            "Misol: 123"
        )
    else:
        await callback.answer(
            "❌ Hali barcha kanallarga obuna bo'lmagansiz!", 
            show_alert=True
        )

@router.message(F.text)
async def movie_code_handler(message: Message, bot: Bot):  # Bot tipini aniq belgilash
    user_id = message.from_user.id
    print(f"🎬 User {user_id} requested: {message.text}")
    
    # Check subscription first
    is_subscribed = await check_subscription(user_id, bot)
    if not is_subscribed:
        await message.answer(
            "❌ Botdan foydalanish uchun barcha kanallarga obuna bo'ling!",
            reply_markup=create_subscription_keyboard()
        )
        return
    
    # Process movie code
    code = message.text.strip()
    print(f"🔍 Processing code: {code}")
    
    # Try to extract code if user sends full text
    extracted_code = extract_movie_code(code)
    if extracted_code:
        code = extracted_code
        print(f"🔍 Extracted code: {code}")
    
    # Search for movie
    movie = db.get_movie_by_code(code)
    
    if movie:
        print(f"✅ Movie found: {movie.code} in channel {movie.channel_id}, message {movie.message_id}")
        try:
            # Kanal ID sini to'g'ri formatda olish
            try:
                # Sonli ID ni integer ga o'tkazish
                channel_id = int(movie.channel_id)
            except ValueError:
                # Agar son bo'lmasa, string sifatida ishlatish
                channel_id = movie.channel_id
            
            print(f"📤 Forwarding from channel: {channel_id}, message: {movie.message_id}")
            
            await bot.forward_message(
                chat_id=user_id,
                from_chat_id=channel_id,
                message_id=movie.message_id
            )
            print(f"✅ Movie successfully forwarded to user {user_id}")
            
        except Exception as e:
            error_msg = f"❌ Kinoni yuborishda xatolik yuz berdi: {str(e)}"
            print(f"🚨 Forward error: {e}")
            await message.answer(error_msg)
    else:
        print(f"❌ Movie not found with code: {code}")
        
        # Debug ma'lumotlari
        try:
            # Database dagi barcha kinolarni olish
            session = db.Session()
            all_movies = session.query(db.Movie).all()
            available_codes = [movie.code for movie in all_movies]
            session.close()
            
            debug_info = f"\n\n📋 Mavjud kodlar: {available_codes[:10]}" if available_codes else "\n\n📋 Hali hech qanday kino qo'shilmagan"
            await message.answer(f"❌ Bunday kodli kino topilmadi.{debug_info}")
        except Exception as e:
            await message.answer("❌ Bunday kodli kino topilmadi.")

# Debug buyrug'i - database holatini tekshirish uchun
@router.message(Command("debug"))
async def debug_handler(message: Message):
    """Debug information for testing"""
    user_id = message.from_user.id
    
    try:
        # Database statistikasi
        stats = db.get_stats()
        
        # Kanallar ro'yxati
        channels = db.get_all_channels()
        
        # Kinolar ro'yxati
        session = db.Session()
        movies = session.query(db.Movie).all()
        available_codes = [movie.code for movie in movies]
        session.close()
        
        debug_text = (
            f"🔧 DEBUG INFORMATION\n\n"
            f"👤 User ID: {user_id}\n"
            f"📊 Foydalanuvchilar: {stats['users']}\n"
            f"📢 Kanallar: {stats['channels']}\n"
            f"🎬 Kinolar: {stats['movies']}\n"
            f"📋 Kanal ID lar: {channels}\n"
            f"🎬 Mavjud kodlar: {available_codes[:15]}\n"
        )
        
        await message.answer(debug_text)
    except Exception as e:
        await message.answer(f"❌ Debug xatosi: {e}")

# Test buyrug'i - ma'lum bir kodni tekshirish
@router.message(Command("test"))
async def test_handler(message: Message, bot: Bot):
    """Test specific movie code"""
    user_id = message.from_user.id
    
    # Check subscription first
    is_subscribed = await check_subscription(user_id, bot)
    if not is_subscribed:
        await message.answer("❌ Avval obuna bo'ling!")
        return
    
    # Test kodi
    test_code = "123"  # O'zingizning test kodingizni qo'ying
    movie = db.get_movie_by_code(test_code)
    
    if movie:
        await message.answer(f"✅ Test movie found: {movie.code}")
        try:
            await bot.forward_message(
                chat_id=user_id,
                from_chat_id=movie.channel_id,
                message_id=movie.message_id
            )
        except Exception as e:
            await message.answer(f"❌ Test forward error: {e}")
    else:
        await message.answer(f"❌ Test movie not found with code: {test_code}")