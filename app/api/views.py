from flask import Flask, Blueprint, render_template, request, redirect
from flask import url_for, jsonify, make_response, flash
from flask import session as login_session

from app.backend import *


api = Blueprint('api', __name__)

@api.route('/api/v1/')
@api.route('/api/v1/catalog.json')
def show_catalog_json():
    """
    Returns list of all catalog categories with latest items added in json.
    """
    categories = get_categories()
    latest_items = get_latest_items()
    return jsonify(
                    Category=[c.serialize for c in categories],
                    Latest_Items=[i.serialize for i in latest_items])


@api.route('/api/v1/catalog/<category>/')
@api.route('/api/v1/catalog/<category>/items.json')
def show_category_json(category):
    """
    Returns details of one catalog category including its items in json format.
    Args:
        category (str): name of category.
    """
    cat = get_category(category)
    return jsonify(Category=cat.serialize)


@api.route('/api/v1/catalog/category/new', methods=['POST'])
def new_category_json():
    """
    Creates a new catalog category. It accepts post parameters in json format.
    Args:
        name (str): name of category
    """
    content = request.get_json()
    if content is not None and 'name' in content:
        category = new_category(content['name'])
        return jsonify(Category=category.serialize), 201
    else:
        return jsonify(Message='Failed to create new category!')


@api.route('/api/v1/catalog/<category>/<item>')
def show_item_json(category, item):
    """
    Returns details of one category item in json format.
    Args:
        category (str): name of category.
        item (str): name of item.
    """
    item = get_item(category, item)
    if Item is not None:
        return jsonify(Item=item.serialize)
    else:
        return jsonify(Message='Failed to find item!'), 204


@api.route('/api/v1/catalog/<category>/new', methods=['POST'])
def new_item_json(category):
    """
    Creates a new item in a catalog category.
    It accepts post parameters in json.
    Args:
        name (str): name of item.
        description (str): description of item.
    """
    content = request.get_json()
    if content is not None and 'name' in content and 'description' in content:
        category_name = category
        name = content['name']
        description = content['description']
        item = new_item(category_name, name, description)
        return jsonify(Item=item.serialize)
    else:
        return jsonify(Message='Failed to create new item!'), 204


@api.route('/api/v1/catalog/<category>/<item>/edit', methods=['POST'])
def edit_item_json(category, item):
    """
    Edits an item in a catalog category. It accepts post parameters in json.
    Args:
        name (str): new name of item.
        description (str): new description of item.
        category (str): new name of category.
    """
    content = request.get_json()
    if content is not None and 'name' in content and 'description' in content:
        name = content['name']
        description = content['description']
        category_name = content['category']
        item = edit_item(category, item, name, description, category_name)
        return jsonify(Item=item.serialize)
    else:
        return jsonify(Message='Failed to edit item!'), 204


@api.route('/api/v1/catalog/<category>/<item>/delete', methods=['POST'])
def del_item_json(category, item):
    """
    Deletes an item in a catalog category.
    Args:
        category (str): name of category.
        item (str): name of item.
    """
    if del_item(category, item):
        return jsonify(Message='Item have been deleted!')
    else:
        return jsonify(Message='Failed to find item!'), 204

