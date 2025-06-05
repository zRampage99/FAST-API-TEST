from sqlalchemy.orm import Session
from entity.token_blacklist import TokenBlacklist

def add_token(db: Session, token: str):
    db_token = TokenBlacklist(token=token)
    db.add(db_token)
    db.commit()

def is_token_blacklisted(db: Session, token: str) -> bool:
    return db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None
