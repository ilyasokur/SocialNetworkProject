from app.config import settings
from app.infrastructure.dao import PostDAO
from app.service.kafka_producer import KafkaProducerService



class PostService:
    def __init__(self, dao: PostDAO, broker: KafkaProducerService):
        self.dao = dao
        self.broker = broker
        
    async def create_post(self, post: dict):
        return await self.dao.create_post(post)
    
    async def get_post_by_id(self, post_id: int):
        result = await self.dao.get_post_by_id(post_id)
        self.broker.send('post', {'post_id': post_id, 'user_id': str(result['user_id'])})
        return result
    
    async def update_post(self, post_data: dict):
        return await self.dao.update_post(post_data)

    async def delete_post(self, id: str):
        return await self.dao.delete_post(id)
    
    async def get_posts_paginated(self, page: int = 1, page_size: int = 10):
        return await self.dao.get_posts_paginated(page, page_size)
    async def like_post(self, post_id: int, user_id: int):
        result = await self.dao.like_post(post_id, user_id)
        self.broker.send('likes', {'post_id': post_id, 'user_id': user_id})
        return result
    async def add_comment(self, post_id: int, user_id: int, content: str):
        result = await self.dao.add_comment(post_id, user_id, content)
        self.broker.send('comments', {'post_id': post_id, 'user_id': user_id, 'comment_id': str(result['id'])})
        return result
    async def get_comments_by_post(self, post_id: int, page: int = 1, page_size: int = 10):
        return await self.dao.get_comments_by_post(post_id, page, page_size)
