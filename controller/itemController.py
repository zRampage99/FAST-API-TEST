from fastapi import APIRouter, Depends
from db import get_session
from entity.item import Item
from service.itemService import create_item, get_item_by_id, get_items
from sqlmodel import Session
from typing import List

router = APIRouter(prefix="/item", tags=["item"])

@router.post("/", response_model=Item)
def add(item: Item, session: Session = Depends(get_session)):
    return create_item(session, item)

@router.get("/", response_model=List[Item])
def read_all(session: Session = Depends(get_session)):
    return get_items(session)

@router.get("/{item_id}", response_model=Item)
def read_by_id(item_id: int, session: Session = Depends(get_session)):
    item = get_item_by_id(session, item_id)
    #if not item:
    #    raise HTTPException(status_code=404, detail="Item not found")
    return item