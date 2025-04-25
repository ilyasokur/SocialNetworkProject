from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "testing"
    KEYCLOAK_CLIENT_ID: str = "user-service"
    KEYCLOAK_CLIENT_SECRET: str = "Hhz7d1KpU39tSbDHeDgxlNcSmW2UuJqD"
    KEYCLOAK_ADMIN_USER: str = "admin"
    KEYCLOAK_ADMIN_PASSWORD: str = "admin"
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    KAFKA_USER_TOPIC: str = "users"

    class Config:
        env_file = ".env"

settings = Settings()