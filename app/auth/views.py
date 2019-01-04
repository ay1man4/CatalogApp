import os
import random
import string
import httplib2
import json
import requests
from flask import Flask, Blueprint, render_template, request, redirect
from flask import url_for, flash, make_response
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from app.backend import *

auth = Blueprint('auth', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRETS_FILE = os.path.join(BASE_DIR, 'client_secrets.json')
CLIENT_ID = json.loads(
    open(CLIENT_SECRETS_FILE, 'r').read())['web']['client_id']


# login
# Create anti-forgery state token
@auth.route('/login')
def login():
    """
    Sign in/Register new user using third party providers.
    """
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('auth/login.html', STATE=state)


@auth.route('/logout')
def logout():
    """
    Sign out user from their third party providers.
    """
    if request.args.get('provider') == 'google':
        gdisconnect()
        flash('You have signed out successfully!', 'alert-success')
        return redirect(url_for('home.show_catalog_html'))


@auth.route('/gconnect', methods=['POST'])
def gconnect():
    """
    sign in using Google Account.
    """
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        flash('Failed to sign in, invalid state!', 'alert-danger')
        return response

    # Obtain authorization code
    code = request.data
    # print('state: ' + request.args.get('state'))

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        flash('Failed to sign in, no authorization!', 'alert-danger')
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    # print('access_token: ' + access_token)
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    r = h.request(url, 'GET')[1]
    # Python3 -> must use decode for body
    result = json.loads(r.decode('utf-8'))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        flash('Failed to sign in, no access token!', 'alert-danger')
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    # print('gplus_id: ' + gplus_id)
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        flash('Failed to sign in, Invalid token!', 'alert-danger')
        return response

    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
                                json.dumps(
                                    'Current user is already connected.'),
                                200)
        response.headers['Content-Type'] = 'application/json'
        flash('You are already signed in!', 'alert-warning')
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

    login_session['logged_in'] = True
    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data.get('email')

    # Check existing users, add if new
    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = create_user()
        flash('You have registered successfully!', 'alert-success')

    login_session['user_id'] = user_id
    flash('You have signed in successfully!', 'alert-success')
    return make_response(json.dumps('Signed in successfully!'), 200)


def gdisconnect():
    """
    sign out from Google Account.
    """
    access_token = login_session.get('access_token')
    if access_token is None:
        clear_login_session()
        response = make_response(
            json.dumps('Current user not connected.'),
            401)
        response.headers['content-type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    # print(url)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        clear_login_session()
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        clear_login_session()
        response = make_response(
            json.dumps('Failed to revoke token for given user.'),
            400)
        response.headers['Content-Type'] = 'application/json'
        return response
