# seeder will create sample database
from database_setup import DBSession, Category, Item, User

session = DBSession()

# Create Demo User
user = User(name='Admin', email='webmaster@example.com')
session.add(user)
session.commit()

# Mobile brands Catalog

brand = Category(name='Samsung', user=user)
session.add(brand)
session.commit()
models = [
    {'name':'Galaxy S9', 'description': 'Latest mobile from Samsung'},
    {'name':'Galaxy Note 9', 'description': 'Awesome note from Samsung with pen'},
    {'name':'Galaxy A9', 'description': 'Mid end brand from Samsung'},
    {'name':'Galaxy S10', 'description': 'comming soon...'},
]
for model in models:
    item = Item(name=model['name'], description=model['description'], category=brand, user=user)
    session.add(item)
    session.commit()

brand = Category(name='Apple', user=user)
session.add(brand)
session.commit()
models = [
    {'name':'iPhone X', 'description': 'Latest mobile from Apple'},
    {'name':'iPhone 9', 'description': 'Awesome and state of art'},
    {'name':'iPhone 4', 'description': 'very old but still the strongest one'},
    {'name':'iPhone 10', 'description': 'comming soon...'},
]
for model in models:
    item = Item(name=model['name'], description=model['description'], category=brand, user=user)
    session.add(item)
    session.commit()

brand = Category(name='Google', user=user)
session.add(brand)
session.commit()
models = [
    {'name':'Pixel 2', 'description': 'Latest mobile from Google'},
    {'name':'Pixel 2 XL', 'description': 'A large version of Pixel 2'},
    {'name':'Nexus 6P', 'description': 'Great mobile but not popular'},
    {'name':'Android One', 'description': 'Low end brand for all'},
]
for model in models:
    item = Item(name=model['name'], description=model['description'], category=brand, user=user)
    session.add(item)
    session.commit()

print("Catalog items have been added!")


