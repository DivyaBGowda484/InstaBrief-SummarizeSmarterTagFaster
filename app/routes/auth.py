from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from bson import ObjectId
from app.services.storage import StorageService
from app.utils.security import hash_password, verify_password, create_access_token


router = APIRouter()
storage = StorageService()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(payload: RegisterRequest):
    existing = await storage.db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_doc = {"email": payload.email, "password_hash": hash_password(payload.password)}
    result = await storage.db.users.insert_one(user_doc)
    return {"id": str(result.inserted_id), "email": payload.email}


@router.post("/login")
async def login(payload: LoginRequest):
    user = await storage.db.users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user.get("password_hash", "")):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(str(user["_id"]))
    return {"access_token": token, "token_type": "bearer"}


