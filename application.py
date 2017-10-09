from flask import Flask, render_template, request, url_for, redirect, flash
app = Flask(__name__)

from database_orm import session, desc
from database_setup import Category, Item


@app.route('/')
@app.route('/catalog')
def homepage():
    categories = session.query(Category).all()
    # items array, latest first
    items = session.query(Item).order_by(desc(Item.id)).all()
    return render_template('homepage.html', categories = categories, items = items)

@app.route('/catalog/<category_name>/items')
def itemsList(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(Item).filter_by(course = category_name).order_by(desc(Item.id)).all()
    count = len(items)
    return render_template('itemsList.html', categories = categories, category = category, items = items, count = count)

@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
    item = session.query(Item).filter_by(name = item_name).one()
    return render_template('itemInfo.html', item = item)

@app.route('/catalog/add', methods=['POST', 'GET'])
def addItem():
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
                return redirect(url_for('itemsList', category_name = request.form['course']))
            else:
                flash('Item %s already exists. Please use a different name.' % request.form['name'])
                return redirect(url_for('homepage'))
        else:
            flash('Please make sure there is no empty value.')
            return redirect(url_for('homepage'))
    else:
        categories = session.query(Category).all()
        return render_template('addItem.html', categories = categories)

@app.route('/catalog/<item_name>/edit', methods=['POST', 'GET'])
def editItem(item_name):
    itemToBeUpdate = session.query(Item).filter_by(name = item_name).one()
    if request.method == 'POST':
        if request.form['name'] and request.form['description'] and \
        request.form['course']:
            if checkUnique(request.form['name']):
                itemToBeUpdate.name = request.form['name']
                itemToBeUpdate.description = request.form['description']
                itemToBeUpdate.course = request.form['course']
                session.add(itemToBeUpdate)
                session.commit()
                flash('Successfully updated the info of %s!' % itemToBeUpdate.name)
            else:
                flash('Item %s already exists. Please use a different name.' % itemToBeUpdate.name)
        else:
            flash('Please make sure there is no empty value.')
        return redirect(url_for('itemsList', category_name = itemToBeUpdate.course))
    else:
        categories = session.query(Category).all()
        return render_template('editItem.html', categories = categories, item = itemToBeUpdate)

@app.route('/catalog/<item_name>/delete', methods=['POST', 'GET'])
def deleteItem(item_name):
    itemToBeDelete = session.query(Item).filter_by(name = item_name).one()
    if request.method == 'POST':
        session.delete(itemToBeDelete)
        session.commit()
        flash('Item %s deleted.' % itemToBeDelete.name)
        return redirect(url_for('itemsList', category_name = itemToBeDelete.course))
    else:
        return render_template('deleteItem.html', item = itemToBeDelete)

# check if the name is unique
def checkUnique(name):
    items = session.query(Item).all()
    for item in items:
        if item.name == name:
            return False
    return True

if __name__ == '__main__':
    app.secret_key = 'superdevkey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
