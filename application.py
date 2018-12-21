from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
from flask import session as login_session
import random, string, httplib2, json, requests
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from backend import *

app = Flask(__name__)
app.config['JSON_SORT_KEYS']=False

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Web views
@app.route('/')
@app.route('/catalog')
def show_catalog_html():
    categories = get_categories()
    latest_items = get_latest_items()
    user = login_session.get('username')
    return render_template('home.html', categories=categories, latest_items=latest_items, user=user)

@app.route('/catalog/<category>')
@app.route('/catalog/<category>/items')
def show_category_html(category):
    categories = get_categories()
    active_category = get_category(category)
    user = login_session.get('username')
    return render_template('category-items.html', user=user, categories=categories, active_category=active_category)

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

# login
# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    # print('state: ' + request.args.get('state'))

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    # print('access_token: ' + access_token)
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    # print('gplus_id: ' + gplus_id)
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    

    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    print(data)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data.get('email', None)
    
    return make_response(json.dumps('Signed in successfully!'), 200)

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['content-type'] = 'application/json'
        return response
    
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' %access_token
    # print(url)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        login_session.pop('access_token', None)
        login_session.pop('gplus_id', None)
        login_session.pop('username', None)
        login_session.pop('email', None)
        login_session.pop('picture', None)
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('show_catalog_html'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

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
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
