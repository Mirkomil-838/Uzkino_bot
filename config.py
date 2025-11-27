import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 6313092609))

# Railway uchun database URL
if os.getenv('DATABASE_URL'):
    DATABASE_URL = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://', 1)
else:
    DATABASE_URL = 'sqlite:///movie_bot.db'