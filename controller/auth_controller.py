from fastapi import APIRouter, Depends, HTTPException
from repository.db import get_session
from sqlalchemy.orm import Session
from handler.api_response import ApiResponse, ApiResponseEmpty
from dto.user_dto import UserDto, UserLogged
from repository import user_repository
from auth.auth_handler import create_access_token

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/register", response_model=ApiResponseEmpty[UserDto])
def register(user: UserDto, db: Session = Depends(get_session)):
    db_user = user_repository.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user_repository.create_user(db, user.username, user.password)
    return ApiResponseEmpty(success=True, message=f"User {user.username} created successfully")

@auth_router.post("/login", response_model=ApiResponse[UserLogged])
def login(user: UserDto, db: Session = Depends(get_session)):
    db_user = user_repository.get_user_by_username(db, user.username)
    if not db_user or not user_repository.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    logged_user = UserLogged(username=user.username, access_token=token)
    return ApiResponse(success=True, message="User logged successfully", data=logged_user)