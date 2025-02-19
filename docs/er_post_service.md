```mermaid
erDiagram

    POSTS {
        bigint id PK
        bigint user_id FK
        text   content
        timestamp created_at
        timestamp updated_at
        int     like_count
        int     view_count
    }

    POST_MEDIA {
        bigint id PK
        bigint post_id FK
        varchar media_url
        varchar media_type
        timestamp uploaded_at
        int     file_size
    }

    COMMENTS {
        bigint id PK
        bigint post_id FK
        bigint user_id FK
        text   text_content
        timestamp created_at
        timestamp updated_at
        bigint parent_comment_id
    }

    POSTS ||--|{ COMMENTS : "has many"
    POSTS ||--|{ POST_MEDIA : "has many"

