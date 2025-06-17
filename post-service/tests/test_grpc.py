import pytest
import grpc
from app.generated import post_pb2_grpc
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from app.generated import post_pb2

@pytest.fixture(scope="module")
def grpc_channel():
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()

@pytest.fixture(scope="module")
def grpc_stub(grpc_channel):
    return post_pb2_grpc.SocialServiceStub(grpc_channel)


def test_create_post(grpc_stub):
    test_time = datetime.now()
    timestamp = Timestamp()
    timestamp.FromDatetime(test_time)
    
    request = post_pb2.CreatePostRequest(
        title="Test Post",
        description="Test Content",
        user_id="4f88d31b-6467-4711-b110-a2ab2d857723",
        is_private=False,
        tags=["test", "python"],
        loyalty_platform="test_platform"
    )
    
    response = grpc_stub.CreatePost(request)
    
    assert response.post.id
    assert response.post.title == "Test Post"
    assert response.post.user_id == "4f88d31b-6467-4711-b110-a2ab2d857723"
    assert not response.post.is_private
    assert "test" in response.post.tags

def test_get_post(grpc_stub):
    create_response = grpc_stub.CreatePost(
        post_pb2.CreatePostRequest(
            title="Post to Get",
            user_id="4f88d31b-6467-4711-b110-a2ab2d857723"
        )
    )
    
    response = grpc_stub.GetPost(
        post_pb2.GetRequest(id=create_response.post.id, user_id="4f88d31b-6467-4711-b110-a2ab2d857723")
    )
    
    assert response.post.title == "Post to Get"
    assert response.post.user_id == "4f88d31b-6467-4711-b110-a2ab2d857723"

def test_update_post(grpc_stub):
    create_response = grpc_stub.CreatePost(
        post_pb2.CreatePostRequest(
            title="Original Title",
            user_id="4f88d31b-6467-4711-b110-a2ab2d857723"
        )
    )
    
    update_response = grpc_stub.UpdatePost(
        post_pb2.UpdatePostRequest(
            id=create_response.post.id,
            title="Updated Title",
            user_id="4f88d31b-6467-4711-b110-a2ab2d857723",
            is_private=True
        )
    )
    
    assert update_response.post.title == "Updated Title"
    assert update_response.post.is_private

def test_list_posts(grpc_stub):
    for i in range(3):
        grpc_stub.CreatePost(
            post_pb2.CreatePostRequest(
                title=f"Post {i}",
                user_id="4f88d31b-6467-4711-b110-a2ab2d857723"
            )
        )
    
    response = grpc_stub.ListPosts(
        post_pb2.ListRequest(page=1, page_size=2, user_id="4f88d31b-6467-4711-b110-a2ab2d857723")
    )
    
    assert len(response.posts) == 2
    assert response.total >= 3

def test_like_post(grpc_stub):
    create_response = grpc_stub.CreatePost(
        post_pb2.CreatePostRequest(
            title="Post to Like",
            user_id="4f88d31b-6467-4711-b110-a2ab2d857723"
        )
    )
    
    grpc_stub.LikePost(
        post_pb2.LikePostRequest(
            post_id=create_response.post.id,
            user_id="4f88d31b-6467-4711-b110-a2ab2d857723"
        )
    )
    
    assert True

def test_add_comment(grpc_stub):
    create_response = grpc_stub.CreatePost(
        post_pb2.CreatePostRequest(
            title="Post for Comments",
            user_id="4f88d31b-6467-4711-b110-a2ab2d857723"
        )
    )
    
    comment_response = grpc_stub.AddComment(
        post_pb2.CommentRequest(
            post_id=create_response.post.id,
            user_id="4f88d31b-6467-4711-b110-a2ab2d857723",
            content="Great post!"
        )
    )
    
    assert comment_response.comment.content == "Great post!"
    assert comment_response.comment.user_id == "4f88d31b-6467-4711-b110-a2ab2d857723"

