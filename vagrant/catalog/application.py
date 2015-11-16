from flask import Flask
app = Flask(__name__)


@app.route('/')
@app.route('/catalog/')
def catalog():
    return 'This is the first step!!'


@app.route('/catalog/<category_name>/items/')
def showCategoryItems(category_name):
    return 'Show the Category Items here!!'



@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name, item_name):
    return 'Show the selected Item here!!'

@app.route('/catalog/<category_name>/<item_name>/edit')
def editItem(category_name, item_name):
    return 'Edit the selected Item here!!'

@app.route('/catalog/<category_name>/<item_name>/delete')
def deleteItem(category_name, item_name):
    return 'Delete the selected Item here!!'



if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)