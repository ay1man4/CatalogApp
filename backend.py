from database_setup import DBSession, Category, Item
from sqlalchemy import desc

session = DBSession()

def show_catalog():
    return session.query(Category).all()

def get_categories():
    return session.query(Category).all()

def get_category(category):
    return session.query(Category).filter(Category.name==category).first()

def new_category(name):
    category = Category()
    category.name = name
    session.add(category)
    session.commit()

def get_category_items(category):
    return session.query(Category.items).filter(Category.name == category)

def get_item(category, item):
    cat = session.query(Category).filter(Category.name==category).first()
    return session.query(Item).filter(Item.category==cat, Item.name==item).first()

def get_latest_items():
    return session.query(Item).order_by(desc('created_at')).limit(10)

def new_item(category_name, name, description):
    category = session.query(Category).filter(Category.name==category_name).first()
    item = Item()
    item.name = name
    item.description = description
    item.category = category
    session.add(item)
    session.commit()
    return session.query(Item).filter(Item.category==category, Item.name==name).first()
    
def edit_item(old_category_name, old_item_name, name, description, category_name):
    old_category = session.query(Category).filter(Category.name==old_category_name).first()
    item = session.query(Item).filter(Item.category==old_category, Item.name==old_item_name).first()
    item.name = name
    item.description = description
    category = session.query(Category).filter(Category.name==category_name).first()
    item.category = category
    session.add(item)
    session.commit()
    return session.query(Item).filter(Item.category==category, Item.name==name).first()

def del_item(category_name, item_name):
    category = session.query(Category).filter(Category.name==category_name).first()
    item = session.query(Item).filter(Item.category==category, Item.name==item_name).first()
    session.delete(item)
    session.commit()