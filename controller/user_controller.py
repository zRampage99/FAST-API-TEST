from fastapi import APIRouter, Depends, HTTPException
from dto.shared_dto import RoleInfo
from dto.item_dto import ItemDtoInfo
from repository.db import get_session
from sqlalchemy.orm import Session
from handler.api_response import ApiResponse, ApiResponseEmpty
from dto.user_dto import UserCredential, UserInfo, UserLogged
from service.auth.user_service import exists_user_by_username, get_user_by_username, create_user, authenticate_user
from auth.auth_handler import create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.auth_bearer import JWTBearer
from service.auth.token_blacklist_service import add_token_to_blacklist
from auth.permission import require_role

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@auth_router.post("/register", response_model=ApiResponse[UserInfo])
def register(
        user: UserCredential, 
        db: Session = Depends(get_session)
    ):
    exists_user_by_username(db, user.username)
    new_user = create_user(db, user.username, user.password)
    
    user_info = UserInfo(
        username=new_user.username,
        roles=[RoleInfo(name=role.name) for role in new_user.roles],
        items=[ItemDtoInfo(name=item.name, id=item.id) for item in new_user.items]

    )
    return ApiResponse(
        success=True, 
        message=f"User {new_user.username} created successfully", 
        data=user_info
    )

@auth_router.post("/login", response_model=ApiResponse[UserLogged])
def login(
        user: UserCredential, 
        db: Session = Depends(get_session)
    ):
    db_user = authenticate_user(db, user.username, user.password)

    roles = [role.name for role in db_user.roles]
    token = create_access_token({"sub": db_user.username, "roles": roles})

    logged_user = UserLogged(
        username=user.username, 
        access_token=token,
        roles=[RoleInfo(name=role.name) for role in db_user.roles]
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
        db: Session = Depends(get_session),
        payload: dict = Depends(require_role("ADMIN", "USER"))
    ):
    current_user = payload["sub"]
    user_roles = payload.get("roles", [])

    if "ADMIN" not in user_roles and username != current_user:
        raise HTTPException(status_code=403, detail="Access denied")

    db_user = get_user_by_username(db, username)    
    user_info = UserInfo(
        username=db_user.username,
        roles=[RoleInfo(name=role.name) for role in db_user.roles]
    )
    return ApiResponse(
        success=True, 
        message=f"User {db_user.username} info loaded successfully", 
        data=user_info
    )
