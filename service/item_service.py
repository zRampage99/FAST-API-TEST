from fastapi import HTTPException
from sqlmodel import Session, select
from entity.item import Item
from dto.item_dto import ItemDtoCreate, ItemDto, ItemDtoUpdate
from entity.user import User

def get_item_by_id(session: Session, item_id: int) -> ItemDto:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item con ID {item_id} non trovato")
    return ItemDto.model_validate(item)

def get_items(session: Session) -> list[ItemDto]:
    statement = select(Item)
    results = session.exec(statement).all()
    return [ItemDto.model_validate(item) for item in results]

def create_item(session: Session, item_data: ItemDtoCreate, username: int) -> ItemDto:
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"Utente '{username}' non trovato")
    item = Item(
        name=item_data.name,
        description=item_data.description,
        price=item_data.price,
        user_id=user.id
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return ItemDto.model_validate(item)

def update_item(session: Session, item_id: int, item_data: ItemDtoUpdate) -> ItemDtoUpdate:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item con ID {item_id} non trovato")
    
    update_data = item_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(item, key, value)
    
    session.add(item)
    session.commit()
    session.refresh(item)
    return ItemDto.model_validate(item)

def delete_item_by_id(session: Session, item_id: int) -> None:
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item con ID {item_id} non trovato")
    session.delete(item)
    session.commit()