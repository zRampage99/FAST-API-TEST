from fastapi import APIRouter, Depends
from db import get_session
from service.item_service import create_item, get_item_by_id, get_items
from sqlmodel import Session
from typing import List
from dto.item_dto import ItemCreate, ItemRead
from handler.api_response import ApiResponse

router = APIRouter(prefix="/item", tags=["item"])

@router.get("/{item_id}", response_model=ApiResponse[ItemRead])
def read_by_id(item_id: int, session: Session = Depends(get_session)):
    item = get_item_by_id(session, item_id)
    return ApiResponse(success=True, data=item)

@router.get("/", response_model=ApiResponse[List[ItemRead]])
def read_all(session: Session = Depends(get_session)):
    items = get_items(session)
    return ApiResponse(success=True, data=items)

@router.post("/", response_model=ApiResponse[ItemRead])
def add(item: ItemCreate, session: Session = Depends(get_session)):
    created_item = create_item(session, item)
    return ApiResponse(success=True, message="Item creato con successo", data=created_item)