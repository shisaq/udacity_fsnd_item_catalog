from flask import Flask, render_template
app = Flask(__name__)

# fake database
category = {'name': 'haha1', 'id': '1'}
categories = [
    {'name': 'haha1', 'id': '1'},
    {'name': 'haha2', 'id': '2'}
]
item = {'name': 'item1', 'description': 'wowowowowowowo1', 'course': 'haha1', 'id': '1'}
items = [
    {'name': 'item1', 'description': 'wowowowowowowo1', 'course': 'haha1', 'id': '1'},
    {'name': 'item2', 'description': 'wowowowowowowo2', 'course': 'haha2', 'id': '2'}
]

@app.route('/')
@app.route('/catalog')
def homepage():
    return render_template('homepage.html', categories = categories, items = items)

@app.route('/catalog/<category_name>/items')
def itemsList(category_name):
    return render_template('itemsList.html', categories = categories, category = category, items = items)

@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
    return render_template('itemInfo.html', item = item)

@app.route('/catalog/add')
def addItem():
    return render_template('addItem.html', categories = categories)

@app.route('/catalog/<item_name>/edit')
def editItem(item_name):
    return render_template('editItem.html', categories = categories, item = item)

@app.route('/catalog/<item_name>/delete')
def deleteItem(item_name):
    return render_template('deleteItem.html', item = item)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
