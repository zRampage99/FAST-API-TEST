from fastapi import APIRouter, Depends, Request
from auth.permission import require_role
from repository.db import get_session
from service.item_service import create_item, delete_item_by_id, get_item_by_id, get_items, update_item
from sqlmodel import Session
from typing import List
from dto.item_dto import ItemDtoCreate, ItemDto, ItemDtoUpdate
from handler.api_response import ApiResponse, ApiResponseEmpty

item_router = APIRouter(
    prefix="/item",
    tags=["item"]
)

@item_router.get("/{item_id}", response_model=ApiResponse[ItemDto])
def get_by_id(
        request: Request,
        item_id: int, 
        session: Session = Depends(get_session),
        _: dict = Depends(require_role("ADMIN", "USER"))
    ):
    item = get_item_by_id(session, item_id)
    return ApiResponse(success=True, data=item, token=request.state.new_token)

@item_router.get("", response_model=ApiResponse[List[ItemDto]])
def get_all(
        request: Request, 
        session: Session = Depends(get_session),
        _: dict = Depends(require_role("ADMIN"))
    ):
    items = get_items(session)
    return ApiResponse(success=True, data=items, token=request.state.new_token)

@item_router.post("", response_model=ApiResponse[ItemDto])
def add(
        request: Request,
        item: ItemDtoCreate, 
        session: Session = Depends(get_session),
        _: dict = Depends(require_role("ADMIN", "USER"))
    ):
    created_item = create_item(session, item)
    return ApiResponse(success=True, message="Item creato con successo", data=created_item, token=request.state.new_token)

@item_router.patch("/{item_id}", response_model=ApiResponse[ItemDtoUpdate])
def update_item_by_id(
        request: Request,
        item_id: int, 
        item: ItemDtoUpdate, 
        session: Session = Depends(get_session),
        _: dict = Depends(require_role("ADMIN", "USER"))
    ):
    updated_item = update_item(session, item_id, item)
    return ApiResponse(success=True, message="Item aggiornato con successo", data=updated_item, token=request.state.new_token)

@item_router.delete("/{item_id}", response_model=ApiResponseEmpty)
def delete_by_id(
        request: Request,
        item_id: int, 
        session: Session = Depends(get_session),
        _: dict = Depends(require_role("ADMIN", "USER"))
    ):
    delete_item_by_id(session, item_id)
    return ApiResponseEmpty(success=True, message=f"Item con ID {item_id} eliminato con successo", token=request.state.new_token)