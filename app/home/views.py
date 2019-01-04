import os
import random
import string
import httplib2
import json
import requests
from flask import Flask, Blueprint, render_template, request, redirect
from flask import url_for, jsonify, make_response, flash
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from app.backend import *

home = Blueprint('home', __name__)


@home.route('/')
@home.route('/catalog')
def show_catalog_html():
    """
    Renders list of all catalog categories with latest items added.
    """
    categories = get_categories()
    latest_items = get_latest_items()
    return render_template(
        'home/home.html',
        categories=categories, latest_items=latest_items)


@home.route('/catalog/<category>')
@home.route('/catalog/<category>/items')
def show_category_html(category):
    """
    Renders details of one catalog category including its items.
    Args:
        category (str): name of category.
    """
    categories = get_categories()
    active_category = get_category(category)
    return render_template(
                            'home/category-items.html',
                            categories=categories,
                            active_category=active_category)


@home.route('/catalog/category/new', methods=['GET', 'POST'])
@login_required
def new_category_html():
    """
    Renders a form to create a new catalog category.
    """
    if request.method == 'POST':
        new_category(name=request.form['name'])
        flash('New Category have been created!', 'alert-success')
        return redirect(url_for('home.show_catalog_html'))
    else:
        return render_template('home/new-category.html')


@home.route('/catalog/<category>/<item>')
def show_item_html(category, item):
    """
    Renders details of one category item.
    Args:
        category (str): name of category.
        item (str): name of item.
    """
    item = get_item(category, item)
    creator, editable = isCreator(item.user_id)
    return render_template(
                            'home/item.html',
                            item=item, creator=creator, editable=editable)


@home.route('/catalog/<category>/new', methods=['GET', 'POST'])
@login_required
def new_item_html(category):
    """
    Renders a form to create a new item in a catalog category.
    Args:
        category (str): name of category.
    """
    if request.method == 'POST':
        category_name = category
        name = request.form['name']
        description = request.form['description']
        new_item(category_name, name, description)
        flash('New Item have been created!', 'alert-success')
        return redirect(
                        url_for('home.show_category_html', category=category))
    else:
        return render_template('home/new-item.html', category=category)


@home.route('/catalog/<category>/<item>/edit', methods=['GET', 'POST'])
@login_required
def edit_item_html(category, item):
    """
    Renders a form to edit an item in a catalog category.
    Args:
        category (str): name of category.
        item (str): name of item.
    """
    itemToEdit = get_item(category, item)
    editable = isCreator(itemToEdit.user_id)[1]
    if not editable:
        flash('Failed to edit the item!', 'alert-danger')
        return render_template('access-denied.html')
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        category_name = request.form['category']
        item = edit_item(category, item, name, description, category_name)
        flash('Item has been edited successfully!', 'alert-success')
        return redirect(
                        url_for(
                                'home.show_category_html',
                                category=item.category.name)
                        )
    else:
        categories = get_categories()
        item = get_item(category, item)
        return render_template(
                                'home/edit-item.html',
                                categories=categories, item=item)


@home.route('/catalog/<category>/<item>/delete', methods=['GET', 'POST'])
@login_required
def del_item_html(category, item):
    """
    Deletes an item in a catalog category.
    Args:
        category (str): name of category.
        item (str): name of item.
    """
    if request.method == 'POST':
        deleted = del_item(category, item)
        if not deleted:
            flash('Failed to delete the item!', 'alert-danger')
            return render_template('access-denied.html')
        else:
            flash('Item have been deleted successfully!', 'alert-warning')
            return redirect(url_for('home.show_category_html',
                            category=category))
    else:
        return render_template('home/del-item.html')
