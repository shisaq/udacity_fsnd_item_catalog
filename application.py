from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/catalog')
def homepage():
    return 'homepage'

@app.route('/catalog/<category_name>/items')
def allCategoryItems(category_name):
    return category_name

@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
    return '%s, %s' % (category_name, item_name)

@app.route('/catalog/add')
def addItem():
    return 'add item'

@app.route('/catalog/<item_name>/edit')
def editItem(item_name):
    return 'edit item'

@app.route('/catalog/<item_name>/delete')
def deleteItem(item_name):
    return 'delete item'


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
