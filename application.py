from flask import Flask, render_template, request, url_for, redirect,\
 flash, jsonify
app = Flask(__name__)

# database
from database_orm import session, desc
from database_setup import Category, Item, User

# login session
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# oauth ids and secrets
G_CLIENT_ID = json.loads(open(
    'client_secrets/g_client_secrets.json', 'r').read())['web']['client_id']
FB_CLIENT_ID = json.loads(open(
    'client_secrets/fb_client_secrets.json', 'r').read())['web']['app_id']
FB_CLIENT_SECRET = json.loads(open(
    'client_secrets/fb_client_secrets.json', 'r').read())['web']['app_secret']

# log in page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

# Google Oauth2
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(\
            'client_secrets/g_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(\
            'Failed to upgrade authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'\
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
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(\
            "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != G_CLIENT_ID:
        response = make_response(json.dumps(\
            "Token's client ID doesn't match app's."), 401)
        print "Token's client ID doesn't match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check to see if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(\
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img class="avatar" src="'
    output += login_session['picture']
    output += '">'
    flash("You've logged in as %s" % login_session['username'])
    return output

# Facebook Oauth2
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(\
            'Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange token to be long-lived server-side token
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (FB_CLIENT_ID, FB_CLIENT_SECRET, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = 'https://graph.facebook.com/v2.10/me'
    # Strip expire tag from access token
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.10/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']

    # Get user picture
    url = 'https://graph.facebook.com/v2.10/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    print data

    login_session['picture'] = data['data']['url']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h2>Welcome, '
    output += login_session['username']
    output += '!</h2>'
    output += '<img class="avatar" src="'
    output += login_session['picture']
    output += '">'
    flash("You've logged in as %s" % login_session['username'])
    return output

# Disconnect oauth2
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            del login_session['facebook_id']

        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash('You have been successfully logged out.')
    else:
        flash('You were not logged in.')
    return redirect(url_for('homepage'))

# APIs
# show all categories
@app.route('/catalog/categories/JSON')
def allCategoriesJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in categories])

# show all items in a specific category
@app.route('/catalog/<category_name>/JSON')
def itemsListJSON(category_name):
    items = session.query(Item).filter_by(course = category_name).all()
    return jsonify(Items=[i.serialize for i in items])

# show datails of an item
@app.route('/catalog/<item_name>/JSON')
def itemInfoJSON(item_name):
    item = session.query(Item).filter_by(name = item_name).one()
    return jsonify(Item=[i.serialize for i in item])


# homepage
@app.route('/')
@app.route('/catalog')
def homepage():
    categories = session.query(Category).all()
    # items array, latest first
    items = session.query(Item).order_by(desc(Item.id)).all()
    return render_template('homepage.html', \
        categories = categories, items = items)

# category page
@app.route('/catalog/<category_name>/items')
def itemsList(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(Item).filter_by(course = category_name).\
    order_by(desc(Item.id)).all()
    count = len(items)
    return render_template('itemsList.html', \
        categories = categories, \
        category = category, \
        items = items, \
        count = count)

# item page
@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
    item = session.query(Item).filter_by(name = item_name).one()
    return render_template('itemInfo.html', item = item)

# add an item
@app.route('/catalog/add', methods=['POST', 'GET'])
def addItem():
    checkLogInStatus()
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and \
        request.form['course']:
            if checkUnique(request.form['name']):
                newItem = Item(name = request.form['name'],\
                               description = request.form['description'],\
                               course = request.form['course'])
                session.add(newItem)
                session.commit()
                flash('A new item has been %s added!' % newItem.name)
                return redirect(url_for('itemsList', \
                    category_name = request.form['course']))
            else:
                flash('Item %s already exists. Please use a different name.'\
                 % request.form['name'])
                return redirect(url_for('homepage'))
        else:
            flash('Please make sure there is no empty value.')
            return redirect(url_for('homepage'))
    else:
        categories = session.query(Category).all()
        return render_template('addItem.html', categories = categories)

# update an item
@app.route('/catalog/<item_name>/edit', methods=['POST', 'GET'])
def editItem(item_name):
    checkLogInStatus()
    itemToBeUpdate = session.query(Item).filter_by(name = item_name).one()
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and \
        request.form['course']:
            # user has updated the name, we need check if it's unique
            if item_name != request.form['name']:
                if checkUnique(request.form['name']):
                    itemToBeUpdate.name = request.form['name']
                    itemToBeUpdate.description = request.form['description']
                    itemToBeUpdate.course = request.form['course']
                    session.add(itemToBeUpdate)
                    session.commit()
                    flash('Successfully updated the info of %s!' \
                        % itemToBeUpdate.name)
                else:
                    flash('Failed to update. Please use a different name.')
            # user doesn't change the name, it's ok to continue
            else:
                itemToBeUpdate.description = request.form['description']
                itemToBeUpdate.course = request.form['course']
                session.add(itemToBeUpdate)
                session.commit()
                flash('Successfully updated the info of %s!' \
                    % itemToBeUpdate.name)
        else:
            flash('Please make sure there is no empty value.')
        return redirect(url_for('itemsList', \
            category_name = itemToBeUpdate.course))
    else:
        categories = session.query(Category).all()
        return render_template('editItem.html', \
            categories = categories, item = itemToBeUpdate)

# delete an item
@app.route('/catalog/<item_name>/delete', methods=['POST', 'GET'])
def deleteItem(item_name):
    checkLogInStatus()
    itemToBeDelete = session.query(Item).filter_by(name = item_name).one()
    if request.method == 'POST':
        session.delete(itemToBeDelete)
        session.commit()
        flash('Item %s deleted.' % itemToBeDelete.name)
        return redirect(url_for('itemsList', \
            category_name = itemToBeDelete.course))
    else:
        return render_template('deleteItem.html', item = itemToBeDelete)


# some assistants to simplify the code
# check if the name is unique
def checkUnique(name):
    items = session.query(Item).all()
    for item in items:
        if item.name == name:
            return False
    return True

# create a user by using login info
def createUser(login_session):
  newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
  session.add(newUser)
  session.commit()
  user = session.query(User).filter_by(email = login_session['email']).one()
  return user.id

# get user id via email
def getUserID(email):
  try:
    user = session.query(User).filter_by(email = email).one()
    return user.id
  except:
    return None

# check if a user has logged in
def checkLogInStatus():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))

if __name__ == '__main__':
    app.secret_key = 'superdevkey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
