# app/service/auth.py
import requests
from jose import jwt
from app.config import settings
from app.infrastructure.dao import UserDAO
from app.domain.schemas import PostCreate
from passlib.context import CryptContext


class PostService:
    def __init__(self, dao: UserDAO):
        self.dao = dao
        
    async def create_post(self, post: PostCreate):
        return await self.dao.create_post(post)
    
    async def get_post_by_id(self, post_id: int):
        return await self.dao.get_post_by_id(post_id)
    
    async def update_post(self):
        return await self.dao.update_post()

    async def delete_post(self):
        return await self.dao.delete_post()
