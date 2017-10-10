from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, exc
from database_setup import Base

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)

session = DBSession()
