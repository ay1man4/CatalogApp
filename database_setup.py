import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
 
Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
 
class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key = True)
    name =Column(String(80), nullable = False)
    description = Column(String(255), nullable = False)

    category_id = Column(Integer,ForeignKey('category.id'))
    category = relationship(Category) 
 

engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)