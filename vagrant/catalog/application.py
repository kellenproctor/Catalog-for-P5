from flask import Flask, render_template, url_for, request, redirect
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Items

app = Flask(__name__)

# Connect to the Database and create a database session
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()




# Basic Routing here:
# Show categories and most recent items
@app.route('/')
@app.route('/catalog/')
def showCatalog():
    catalog = session.query(Category).order_by(asc(Category.name))
    items = session.query(Items).order_by(desc(Items.date))
    return render_template('showcatalog.html',
                            categories=catalog,
                            items=items)


# Show specific category items
@app.route('/catalog/<category_name>/')
@app.route('/catalog/<category_name>/items/')
def showCategoryItems(category_name):
    return 'Show the Category Items here!!'

# Show the specifics of an item
@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name, item_name):
    return 'Show the selected Item here!!'

# Edit an item
@app.route('/catalog/<category_name>/<item_name>/edit')
def editItem(category_name, item_name):
    return 'Edit the selected Item here!!'

# Delete an item
@app.route('/catalog/<category_name>/<item_name>/delete')
def deleteItem(category_name, item_name):
    return 'Delete the selected Item here!!'



if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)