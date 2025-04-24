from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KEYCLOAK_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "testing"
    KEYCLOAK_CLIENT_ID: str = "user-service"
    KEYCLOAK_CLIENT_SECRET: str = "u4dXdJgnwKUxNsOMF1JfnoMWm4k8KWNg"
    KEYCLOAK_ADMIN_USER: str = "admin"
    KEYCLOAK_ADMIN_PASSWORD: str = "admin"

    class Config:
        env_file = ".env"

settings = Settings()