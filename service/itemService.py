from fastapi import HTTPException
from sqlmodel import Session, select
from entity.item import Item

def create_item(session: Session, item: Item):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

def get_items(session: Session):
    statement = select(Item)
    results = session.exec(statement)
    return results.all()


def get_item_by_id(session: Session, item_id: int):
    statement = select(Item).where(Item.id == item_id)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=404, detail=f"Item con ID {item_id} non trovato")
    return result