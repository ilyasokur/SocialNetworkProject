# app/service/auth.py
from config import settings
from infrastructure.dao import PostDAO



class PostService:
    def __init__(self, dao: PostDAO):
        self.dao = dao
        
    async def create_post(self, post: dict):
        return await self.dao.create_post(post)
    
    async def get_post_by_id(self, post_id: int):
        return await self.dao.get_post_by_id(post_id)
    
    async def update_post(self, post_data: dict):
        return await self.dao.update_post(post_data)

    async def delete_post(self, id: str):
        return await self.dao.delete_post(id)
    
    async def get_posts_paginated(self, page: int = 1, page_size: int = 10):
        return await self.dao.get_posts_paginated(page, page_size)
