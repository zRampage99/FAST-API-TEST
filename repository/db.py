from sqlmodel import SQLModel, create_engine, Session, select
import os
from dotenv import load_dotenv

from entity.role import Role

load_dotenv()  # Carica le variabili d'ambiente dal file .env

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")
MYSQL_DB = os.getenv("MYSQL_DB")

DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# Crea l'engine
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
        
def init_roles():
    with Session(engine) as session:
        existing_roles = session.exec(select(Role)).all()
        if not existing_roles:
            print("⚙️  Inserisco ruoli iniziali...")
            session.add_all([
                Role(name="ADMIN"),
                Role(name="USER")
            ])
            session.commit()
        else:
            print("✅ Ruoli già presenti, nessuna azione necessaria.")

