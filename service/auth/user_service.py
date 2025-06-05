from fastapi import HTTPException
from sqlalchemy.orm import Session
from entity.role import Role
from entity.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def create_user(db: Session, username: str, password: str):
    hashed_password = pwd_context.hash(password)
    
    user_role = db.query(Role).filter_by(name="USER").first()
    if not user_role:
        raise Exception("Role 'USER' not found in database")

    user = User(
        username=username,
        hashed_password=hashed_password,
        roles=[user_role]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)