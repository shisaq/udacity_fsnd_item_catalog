from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'email': self.email
        }


class Category(Base):
    __tablename__ = 'category'

    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class Item(Base):
    __tablename__ = 'item'

    name = Column(String, nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    course = Column(String, ForeignKey('category.name'))
    category = relationship(Category)
    email = Column(String, ForeignKey('user.email'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'course': self.course,
            'email': self.email
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
