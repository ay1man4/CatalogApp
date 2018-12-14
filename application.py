from flask import Flask
app = Flask(__name__)

from database_setup import DBSession, Category, Item

session = DBSession()

# Web views
@app.route('/')
@app.route('/catalog')
def catalog_html():
    catalog()
    return "This is home page"

@app.route('/catalog/<category>/')
def category_html(category):
    category(category)
    return "This is category page"

@app.route('/catalog/<category>/<item>')
def item_html(category, item):
    item(category, item)
    return "This is item page"

# JSON
@app.route('/api/v1')
@app.route('/api/v1/catalog.json')
def catalog_json():
    return {

    }


@app.route('/api/v1/catalog/<category>')
def category_json(category):
    return {

    }

@app.route('/api/v1/catalog/<category>/<item>')
def item_json(category, item):
    return {

    }

# Backend
def catalog():
    pass

def category(category):
    pass

def item(category, item):
    pass

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
