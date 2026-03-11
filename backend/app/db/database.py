from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from backend.app.config import USER,PASSWORD,PORT,HOST,DATABASE



DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(DATABASE_URL, isolation_level='AUTOCOMMIT')

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
Session = SessionLocal()

def get_db():
    db = Session
    try :
        yield db
    finally:
        db.close()
    

     