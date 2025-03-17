```mermaid
erDiagram

    POST_STATS {
        bigint id PK
        bigint post_id
        timestamp event_time
        int total_likes
        int total_views
        int total_comments
    }

    COMMENT_STATS {
        bigint id PK
        bigint comment_id
        timestamp event_time
        int total_likes
        int replies_count
    }

    USER_STATS {
        bigint id PK
        bigint user_id
        timestamp event_time
        int posts_created
        int comments_created
        int likes_given
    }
