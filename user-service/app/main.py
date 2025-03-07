from fastapi import FastAPI
from app.api.routes import router
from app.infrastructure.database import init_db

app = FastAPI(
    title="User Service",
    description="Сервис управления пользователями с аутентификацией через Keycloak",
    version="1.0.0"
)

app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
