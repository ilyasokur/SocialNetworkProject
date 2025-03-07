from app.infrastructure.dao import UserDAO
from app.domain.models import User
from app.domain.schemas import UserCreate, UserLogin
from passlib.context import CryptContext
import jwt
import datetime

SECRET_KEY = "supersecret"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def register_user(self, user_data: UserCreate):
        if self.dao.get_user_by_username(user_data.username):
            raise ValueError("User already exists")

        hashed_password = pwd_context.hash(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        return self.dao.create_user(new_user)

    def authenticate_user(self, login_data: UserLogin):
        user = self.dao.get_user_by_username(login_data.username)
        if not user or not pwd_context.verify(login_data.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        access_token = jwt.encode(
            {"sub": user.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            SECRET_KEY
        )
        return {"access_token": access_token, "token_type": "bearer"}
