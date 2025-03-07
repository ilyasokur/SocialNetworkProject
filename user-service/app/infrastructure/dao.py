from sqlalchemy.orm import Session
from app.domain.models import User

class UserDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User):
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_username(self, username: str):
        return self.db.query(User).filter(User.username == username).first()
