from database_setup import DBSession, Category, Item, User
from sqlalchemy import desc
from functools import wraps
from flask import request, redirect, url_for, session as login_session

session = DBSession()


def login_required(f):
    """
    A decorator method to check if user is logged in or not
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if login_session.get('logged_in') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def clear_login_session():
    """
    Clears login_session parameters after user sign out
    """
    login_session.pop('access_token', None)
    login_session.pop('gplus_id', None)
    login_session.pop('username', None)
    login_session.pop('email', None)
    login_session.pop('picture', None)
    login_session.pop('provider', None)
    login_session.pop('user_id', None)
    login_session.pop('logged_in', None)


def create_user():
    """
    Creates new user if not exist in DB.
    Returns:
        User: created user instance
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """
    Query user if exist in DB.
    Returns:
        User: instance of User if exist and None if not.
    """
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except Exception as e:
        print(e)
        return None


def getUserID(email):
    """
    Query user id if exist in DB.
    Returns:
        integer: user id if exist and None if not.
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as e:
        print(e)
        return None


def isCreator(user_id):
    """
    Checks if current user is the creator of catalog category or item.
    Returns:
        boolean: True if same user is the creator, False otherwise.
        User: the user instance of creator.
    """
    creator = getUserInfo(user_id)
    if creator.id != login_session.get('user_id'):
        return creator, False
    return creator, True


def show_catalog():
    return session.query(Category).all()


def get_categories():
    return session.query(Category).all()


def get_category(category):
    return session.query(Category).filter(Category.name == category).first()


def new_category(name):
    category = session.query(Category).filter(Category.name == name).first()
    if category is None:
        category = Category()
        category.name = name
        category.user_id = login_session['user_id']
        session.add(category)
        session.commit()

        return session.query(Category).filter(Category.name == name).first()
    else:

        return category


def get_category_items(category):
    return session.query(Category.items).filter(Category.name == category)


def get_item(category, item):
    cat = session.query(Category).filter(Category.name == category).first()
    return session.query(Item)\
        .filter(Item.category == cat, Item.name == item).first()


def get_latest_items():
    return session.query(Item).order_by(desc('created_at')).limit(10)


def new_item(category_name, name, description):
    category = session.query(Category)\
            .filter(Category.name == category_name).first()
    item = Item()
    item.name = name
    item.description = description
    item.category = category
    item.user_id = login_session['user_id']
    session.add(item)
    session.commit()
    return session.query(Item)\
        .filter(Item.category == category, Item.name == name).first()


def edit_item(
                old_category_name, old_item_name,
                name, description, category_name):

    old_category = session.query(Category)\
        .filter(Category.name == old_category_name).first()
    item = session.query(Item)\
        .filter(Item.category == old_category, Item.name == old_item_name)\
        .first()
    item.name = name
    item.description = description
    category = session.query(Category)\
        .filter(Category.name == category_name).first()
    item.category = category
    session.add(item)
    session.commit()
    return session.query(Item)\
        .filter(Item.category == category, Item.name == name).first()


def del_item(category_name, item_name):
    category = session.query(Category)\
        .filter(Category.name == category_name).first()
    item = session.query(Item)\
        .filter(Item.category == category, Item.name == item_name).first()
    creator, editable = isCreator(item.user_id)
    if item is not None and editable:
        session.delete(item)
        session.commit()
        return True
    else:
        return False
