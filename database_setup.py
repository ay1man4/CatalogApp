import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
 
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    items = relationship('Item')

    @property
    def items_count(self):
        return len(self.items)
    
    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'items_count': self.items_count,
            'items': [i.serialize for i in self.items],
        }

class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    description = Column(String(255), nullable = False)
    created_at = Column(DateTime, default=datetime.datetime.now())

    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cat_id': self.category_id,
        }


engine = create_engine('sqlite:///db.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)