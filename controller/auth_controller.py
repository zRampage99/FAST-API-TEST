from fastapi import APIRouter, Depends, HTTPException
from dto.role_dto import RoleDto
from repository.db import get_session
from sqlalchemy.orm import Session
from handler.api_response import ApiResponse, ApiResponseEmpty
from dto.user_dto import UserCredential, UserInfo, UserLogged
from service.auth.user_service import get_user_by_username, create_user, authenticate_user
from auth.auth_handler import create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth_bearer import JWTBearer
from service.auth.token_blacklist_service import add_token_to_blacklist

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/register", response_model=ApiResponse[UserInfo])
def register(
        user: UserCredential, 
        db: Session = Depends(get_session)
    ):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = create_user(db, user.username, user.password)
    
    user_info = UserInfo(
        username=new_user.username,
        roles=[RoleDto(name=role.name) for role in new_user.roles]
    )
    return ApiResponse(
        success=True, 
        message=f"User {new_user.username} created successfully", 
        data=user_info
    )

@auth_router.post("/login", response_model=ApiResponse[UserLogged])
def login(user: UserCredential, 
          db: Session = Depends(get_session)
    ):
    db_user = authenticate_user(db, user.username, user.password)

    token = create_access_token({"sub": db_user.username})
    
    logged_user = UserLogged(
        username=user.username, 
        access_token=token,
        roles=[RoleDto(name=role.name) for role in db_user.roles]
    )
    return ApiResponse(success=True, message="User logged successfully", data=logged_user)

@auth_router.post("/logout", response_model=ApiResponseEmpty)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    _: dict = Depends(JWTBearer()),
    db: Session = Depends(get_session)
    ):
    token = credentials.credentials
    add_token_to_blacklist(db, token)
    return ApiResponseEmpty(success=True, message="User successfully logged out")

@auth_router.get("/info/{username}", response_model=ApiResponse[UserInfo])
def get_user_info(
        username: str,
        db: Session = Depends(get_session)
    ):
    db_user = get_user_by_username(db, username)    
    user_info = UserInfo(
        username=db_user.username,
        roles=[RoleDto(name=role.name) for role in db_user.roles]
    )
    return ApiResponse(
        success=True, 
        message=f"User {db_user.username} info loaded successfully", 
        data=user_info
    )
