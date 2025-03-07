from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal
from app.service.auth import AuthService
from app.infrastructure.dao import UserDAO
from app.domain.schemas import UserCreate, UserLogin, UserResponse
import jwt
import requests

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


KEYCLOAK_URL = "http://keycloak:8080/realms/MyApp/protocol/openid-connect/certs"

def verify_token(token: str):
    try:
        headers = jwt.get_unverified_header(token)
        kid = headers["kid"]
        certs = requests.get(KEYCLOAK_URL).json()["keys"]
        public_key = next(k["x5c"][0] for k in certs if k["kid"] == kid)

        payload = jwt.decode(token, public_key, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    dao = UserDAO(db)
    auth_service = AuthService(dao)
    try:
        return auth_service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    dao = UserDAO(db)
    auth_service = AuthService(dao)
    try:
        return auth_service.authenticate_user(user)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.get("/profile", response_model=UserResponse)
def get_profile(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    dao = UserDAO(db)
    user = dao.get_user_by_username(token["sub"])
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user