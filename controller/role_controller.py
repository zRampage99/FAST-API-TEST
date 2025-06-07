from fastapi import APIRouter, Depends, Request
from auth.permission import require_role
from repository.db import get_session
from service.role_service import create_role, delete_role_by_id, get_role_by_id, get_roles
from sqlmodel import Session
from typing import List
from dto.role_dto import RoleDtoCreate, RoleDto
from handler.api_response import ApiResponse, ApiResponseEmpty

role_router = APIRouter(
    prefix="/role",
    tags=["role"]
)

@role_router.get("/{role_id}", response_model=ApiResponse[RoleDto])
def get_by_id(
        request: Request,
        role_id: int, 
        session: Session = Depends(get_session),
        _: dict = Depends(require_role("ADMIN", "USER"))
    ):
    role = get_role_by_id(session, role_id)
    return ApiResponse(success=True, data=role, token=request.state.new_token)

@role_router.get("", response_model=ApiResponse[List[RoleDto]])
def get_all(
        request: Request, 
        session: Session = Depends(get_session),
        _: dict = Depends(require_role("ADMIN"))
    ):
    roles = get_roles(session)
    return ApiResponse(success=True, data=roles, token=request.state.new_token)

@role_router.post("", response_model=ApiResponse[RoleDto])
def add(
        request: Request,
        role: RoleDtoCreate, 
        session: Session = Depends(get_session),
        _: dict = Depends(require_role("ADMIN"))
    ):
    created_role = create_role(session, role)
    return ApiResponse(success=True, message="Role creato con successo", data=created_role, token=request.state.new_token)

@role_router.delete("/{role_id}", response_model=ApiResponseEmpty)
def delete_by_id(
        request: Request,
        role_id: int, 
        session: Session = Depends(get_session),
        _: dict = Depends(require_role("ADMIN"))
    ):
    delete_role_by_id(session, role_id)
    return ApiResponseEmpty(success=True, message=f"Role con ID {role_id} eliminato con successo", token=request.state.new_token)