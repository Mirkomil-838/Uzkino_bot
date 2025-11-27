import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base, User, Channel, Movie
from config import DATABASE_URL

class Database:
    def __init__(self):
        # PostgreSQL uchun connection
        self.engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def add_user(self, user_id):
        session = self.Session()
        try:
            if not session.query(User).filter_by(user_id=user_id).first():
                user = User(user_id=user_id)
                session.add(user)
                session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Database error in add_user: {e}")
            return False
        finally:
            session.close()
    
    # ... qolgan methodlar o'zgarmaydi (avvalgidek)