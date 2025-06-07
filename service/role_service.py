from fastapi import HTTPException
from sqlmodel import Session, select
from entity.role import Role
from dto.role_dto import RoleDto, RoleDtoCreate

def get_role_by_id(session: Session, role_id: int) -> RoleDto:
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role con ID {role_id} non trovato")
    return RoleDto.model_validate(role)

def get_roles(session: Session) -> list[RoleDto]:
    statement = select(Role)
    results = session.exec(statement).all()
    return [RoleDto.model_validate(role) for role in results]

def create_role(session: Session, role_data: RoleDtoCreate) -> RoleDto:
    role = Role(**role_data.model_dump())
    session.add(role)
    session.commit()
    session.refresh(role)
    return RoleDto.model_validate(role)

def delete_role_by_id(session: Session, role_id: int) -> None:
    role = session.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail=f"Role con ID {role_id} non trovato")
    session.delete(role)
    session.commit()