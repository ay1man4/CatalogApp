import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app import db

class User(db.Model):
    """
    Create a User table
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(255), nullable=True)

    def __repr__(self):
        return '<User: {}>'.format(self.name)


class Category(db.Model):
    """
    Create a Category table
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    items = relationship('Item')
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

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
    

    def __repr__(self):
        return '<Category: {}>'.format(self.name)


class Item(db.Model):
    """
    Create a Item table
    """
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cat_id': self.category_id,
        }


    def __repr__(self):
        return '<Item: {}>'.format(self.name)
