from fastapi import APIRouter, Depends
from db import get_session
from service.itemService import create_item, get_item_by_id, get_items
from sqlmodel import Session
from typing import List
from dto.itemDto import ItemCreate, ItemRead

router = APIRouter(prefix="/item", tags=["item"])

@router.post("/", response_model=ItemRead)
def add(item: ItemCreate, session: Session = Depends(get_session)):
    return create_item(session, item)

@router.get("/", response_model=List[ItemRead])
def read_all(session: Session = Depends(get_session)):
    return get_items(session)

@router.get("/{item_id}", response_model=ItemRead)  # correggi qui
def read_by_id(item_id: int, session: Session = Depends(get_session)):
    return get_item_by_id(session, item_id)