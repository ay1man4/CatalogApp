from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)
app.config['JSON_SORT_KEYS']=False

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

@app.route('/catalog/<category>/<item>')
def show_item_html(category, item):
    item = get_item(category, item)
    return render_template('item.html', item=item)

@app.route('/catalog/<category>/new', methods=['GET', 'POST'])
def new_item_html(category):
    if request.method == 'POST':
        category_name = category
        name = request.form['name']
        description = request.form['description']
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
@app.route('/api/v1/')
@app.route('/api/v1/catalog.json')
def show_catalog_json():
    categories = get_categories()
    latest_items = get_latest_items()
    return jsonify(Category=[c.serialize for c in categories], Latest_Items=[i.serialize for i in latest_items])

@app.route('/api/v1/catalog/<category>/')
@app.route('/api/v1/catalog/<category>/items.json')
def show_category_json(category):
    cat = get_category(category)
    return jsonify(Category=cat.serialize)

@app.route('/api/v1/catalog/category/new', methods=['POST'])
def new_category_json():
    content = request.get_json()
    if content is not None and 'name' in content:
        category = new_category(content['name'])
        return jsonify(Category=category.serialize), 201
    else:
        return jsonify(Message='Failed to create new category!')

@app.route('/api/v1/catalog/<category>/<item>')
def show_item_json(category, item):
    item = get_item(category, item)
    if Item is not None:
        return jsonify(Item=item.serialize)
    else:
        return jsonify(Message='Failed to find item!'), 204

@app.route('/api/v1/catalog/<category>/new', methods=['POST'])
def new_item_json(category):
    content = request.get_json()
    if content is not None and 'name' in content and 'description' in content:
        category_name = category
        name = content['name']
        description = content['description']
        item = new_item(category_name, name, description)
        return jsonify(Item=item.serialize)
    else:
        return jsonify(Message='Failed to create new item!'), 204

@app.route('/api/v1/catalog/<category>/<item>/edit', methods=['POST'])
def edit_item_json(category, item):
    content = request.get_json()
    if content is not None and 'name' in content and 'description' in content:
        name = content['name']
        description = content['description']
        category_name = content['category']
        item = edit_item(category, item, name, description, category_name)
        return jsonify(Item=item.serialize)
    else:
        return jsonify(Message='Failed to edit item!'), 204

@app.route('/api/v1/catalog/<category>/<item>/delete', methods=['POST'])
def del_item_json(category, item):
    if del_item(category, item):
        return jsonify(Message='Item have been deleted!')
    else:
        return jsonify(Message='Failed to find item!'), 204

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
