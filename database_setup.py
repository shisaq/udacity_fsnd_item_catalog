from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    name = Column(String, nullable = False)
    id = Column(Integer, primary_key = True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }

class Item(Base):
    __tablename__ = 'item'

    name = Column(String, nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(1000))
    course = Column(String, ForeignKey('category.name'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'course': self.course
        }

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
