from sqlalchemy.orm import Session
from app.domain.models import Post
from app.domain.schemas import PostCreate



class PostDAO:
    def __init__(self, db: Session):
        self.db = db

    async def create_post(self, post: PostCreate):
        post = Post(**post.dict())
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
    
    async def get_post_by_id(self, post_id: int):
        return self.db.query(Post).filter(Post.id == post_id).first()

    async def update_post(self, id: int):
        post = self.db.query(Post).filter(Post.id == id).first()
        #TODO implement update logic

    async def delete_post(self, id: int):
        post = self.db.query(Post).filter(Post.id == id).first()
        self.db.delete(post)
        self.db.commit()
        
        
    
