from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

from backend import *

# Web views
@app.route('/')
@app.route('/catalog')
def show_catalog_html():
    categories = get_categories()
    latest_items = get_latest_items()
    return render_template('home.html', categories=categories, latest_items=latest_items)

@app.route('/catalog/<category>')
@app.route('/catalog/<category>/items')
def show_category_html(category):
    categories = get_categories()
    active_category = get_category(category)
    return render_template('category-items.html', categories=categories, active_category=active_category)

@app.route('/catalog/category/new', methods=['GET', 'POST'])
def new_category_html():
    if request.method == 'POST':
        new_category(name=request.form['name'])
        return redirect(url_for('show_catalog_html'))
    else:
        return render_template('new-category.html')

@app.route('/catalog/<category>/delete', methods=['GET', 'POST'])
def del_category_html(category):
    
    return "Category have been deleted!"

@app.route('/catalog/<category>/<item>')
def show_item_html(category, item):
    item = get_item(category, item)
    return render_template('item.html', item=item)

@app.route('/catalog/<category>/new', methods=['GET', 'POST'])
def new_item_html(category):
    if request.method == 'POST':
        category_name = category
        name = request.form['name']
        description = request.form['name']
        new_item(category_name, name, description)
        return redirect(url_for('show_item_html', category=category, item=name))
    else:
        return render_template('new-item.html', category=category)

@app.route('/catalog/<category>/<item>/edit', methods=['GET', 'POST'])
def edit_item_html(category, item):
    if request.method == 'POST':
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            category_name = request.form['category']
            item = edit_item(category, item, name, description, category_name)
            return redirect(url_for('show_item_html', category=item.category.name, item=item.name))
    else:
        categories = get_categories()
        item = get_item(category, item)
        return render_template('edit-item.html', categories=categories, item=item)

@app.route('/catalog/<category>/<item>/delete', methods=['GET', 'POST'])
def del_item_html(category, item):
    if request.method == 'POST':
        del_item(category, item)
        return redirect(url_for('show_category_html', category=category))
    else:
        return render_template('del-item.html')

# JSON
@app.route('/api/v1')
@app.route('/api/v1/catalog.json')
def get_catalog_json():
    return {

    }


@app.route('/api/v1/catalog/<cat>')
def get_category_json(category):
    return {

    }

@app.route('/api/v1/catalog/<category>/<item>')
def get_item_json(category, item):
    return {

    }


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
