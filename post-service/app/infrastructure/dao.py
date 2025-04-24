from sqlalchemy.orm import Session
from domain.models import Post
from sqlalchemy.exc import NoResultFound
from typing import Optional

class PostDAO:
    def __init__(self, db: Session):
        self.db = db

    async def create_post(self, post_data: dict) -> dict:
        
        db_post = Post(
            title=post_data["title"],
            description=post_data["description"],
            user_id=post_data["user_id"],
            is_private=post_data["is_private"],
            tags=post_data["tags"],
            loyalty_platform=post_data["loyalty_platform"]
        )
        
        self.db.add(db_post)
        self.db.commit()
        self.db.refresh(db_post)
        
        return {
            "id": db_post.id,
            "title": db_post.title,
            "description": db_post.description,
            "user_id": db_post.user_id,
            "is_private": db_post.is_private,
            "tags": db_post.tags,
            "loyalty_platform": db_post.loyalty_platform,
            "created_at": db_post.created_at,
            "updated_at": db_post.updated_at
        }

    async def get_post_by_id(self, post_id: str) -> Optional[dict]:
        try:
            post = self.db.query(Post).filter(Post.id == post_id).one()
            return {
                "id": post.id,
                "title": post.title,
                "description": post.description,
                "user_id": post.user_id,
                "is_private": post.is_private,
                "tags": post.tags,
                "loyalty_platform": post.loyalty_platform,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            }
        except NoResultFound:
            return None

    async def update_post(self, post_data: dict) -> Optional[dict]:
        db_post = self.db.query(Post).filter(Post.id == post_data["id"]).first()
        if db_post:
            db_post.title = post_data["title"]
            db_post.description = post_data["description"]
            db_post.is_private = post_data["is_private"]
            db_post.tags = post_data["tags"]
            db_post.loyalty_platform = post_data["loyalty_platform"]
            self.db.commit()
            self.db.refresh(db_post)
            return {
                "id": db_post.id,
                "title": db_post.title,
                "description": db_post.description,
                "user_id": db_post.user_id,
                "is_private": db_post.is_private,
                "tags": db_post.tags,
                "loyalty_platform": db_post.loyalty_platform,
                "created_at": db_post.created_at,
                "updated_at": db_post.updated_at
            }
        return None

    async def delete_post(self, post_id: str) -> bool:
        db_post = self.db.query(Post).filter(Post.id == post_id).first()
        if db_post:
            self.db.delete(db_post)
            self.db.commit()
            return True
        return False
