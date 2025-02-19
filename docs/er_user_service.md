```mermaid
erDiagram

    USERS {
        bigint id PK
        varchar username
        varchar email
        varchar password_hash
        varchar salt
        timestamp created_at
        timestamp updated_at
    }

    USER_ROLES {
        bigint id PK
        bigint user_id FK
        varchar role_name
        timestamp assigned_at
    }

    USER_SESSIONS {
        bigint id PK
        bigint user_id FK
        varchar session_token
        timestamp created_at
        timestamp expires_at
    }

    USERS ||--|{ USER_ROLES : "has many"
    USERS ||--|{ USER_SESSIONS : "has many"
