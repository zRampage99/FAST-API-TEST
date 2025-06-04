from fastapi import HTTPException
from sqlmodel import Session, select
from entity.item import Item
from dto.item_dto import ItemCreate, ItemRead

def get_item_by_id(session: Session, item_id: int) -> ItemRead:
    statement = select(Item).where(Item.id == item_id)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Item con ID {item_id} non trovato")
    return ItemRead.model_validate(result)

def get_items(session: Session) -> list[ItemRead]:
    statement = select(Item)
    results = session.exec(statement).all()
    return [ItemRead.model_validate(item) for item in results]

def create_item(session: Session, item_data: ItemCreate) -> ItemRead:
    item = Item(**item_data.model_dump())
    session.add(item)
    session.commit()
    session.refresh(item)
    return ItemRead.model_validate(item)