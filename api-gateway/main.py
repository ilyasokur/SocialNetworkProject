from fastapi import FastAPI, Request, HTTPException
import httpx
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS (для фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Конфигурация сервисов
SERVICES = {
    "user": "http://user-service:8001",
    "posts": "http://post-service:8002",
    "promos": "http://promo-service:8003"
}

# Публичные эндпоинты (не требуют авторизации)
PUBLIC_ENDPOINTS = {
    "user": [
        "/api/v1/login",
        "/api/v1/register",
        "/api/v1/health"
    ],
    "posts": [
        "/api/v1/health"
    ],
    "promos": [
        "/api/v1/health"
    ]
}

def is_public_endpoint(service: str, path: str) -> bool:
    """Проверяет, является ли endpoint публичным"""
    if service not in PUBLIC_ENDPOINTS:
        return False
    
    # Нормализуем путь
    full_path = f"/{path}" if not path.startswith("/") else path
    
    # Проверяем точное совпадение или префикс
    return any(
        full_path == public_path or 
        full_path.startswith(public_path + "/")
        for public_path in PUBLIC_ENDPOINTS[service]
    )

@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(service: str, path: str, request: Request):
    # Проверка существования сервиса
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    # Проверка публичного эндпоинта
    is_public = is_public_endpoint(service, path)
    
    # Для защищенных эндпоинтов проверяем наличие токена
    if not is_public:
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail="Authorization header missing",
                headers={"WWW-Authenticate": "Bearer"}
            )

    # Подготовка запроса к целевому сервису
    target_url = f"{SERVICES[service]}/{path}"
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ["host", "content-length"]
    }

    try:
        async with httpx.AsyncClient() as client:
            # Обработка разных типов запросов
            if request.method in ["POST", "PUT", "PATCH"]:
                content_type = request.headers.get("content-type", "")
                
                if "application/x-www-form-urlencoded" in content_type:
                    form_data = await request.form()
                    response = await client.request(
                        request.method,
                        target_url,
                        data=dict(form_data),
                        headers=headers,
                        timeout=30.0
                    )
                else:
                    try:
                        json_data = await request.json()
                    except:
                        json_data = None
                    
                    response = await client.request(
                        request.method,
                        target_url,
                        json=json_data,
                        headers=headers,
                        timeout=30.0
                    )
            else:
                response = await client.request(
                    request.method,
                    target_url,
                    headers=headers,
                    timeout=30.0
                )

            # Возвращаем ответ от сервиса
            return response.json()

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"Service {service} unavailable"
        )
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail=f"Service {service} timeout"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)