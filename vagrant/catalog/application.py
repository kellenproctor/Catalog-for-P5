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
    catalog = session.query(Category).order_by(asc(Category.name))
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(category=category)\
                                .order_by(asc(Items.name))
    count = session.query(Items).filter_by(category=category).count()
    return render_template('showitems.html',
                            category=category.name,
                            categories=catalog,
                            items=items,
                            count=count)

# Add an item
@app.route('/catalog/add')
def addItem():
    return render_template('additem.html')

# Add an item to a Category
@app.route('/catalog/<category_name>/add')
def addCategoryItem(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    return render_template('addcategoryitem.html',
                            category=category)

# Show the specifics of an item
@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name, item_name):
    item = session.query(Items).filter_by(name=item_name).one()
    return render_template('itemdescription.html',
                            item=item)

# Edit an item
@app.route('/catalog/<category_name>/<item_name>/edit')
def editItem(category_name, item_name):
    item = session.query(Items).filter_by(name=item_name).one()
    return render_template('edititem.html',
                            item=item)

# Delete an item
@app.route('/catalog/<category_name>/<item_name>/delete')
def deleteItem(category_name, item_name):
    item = session.query(Items).filter_by(name=item_name).one()
    return render_template('deleteitem.html',
                            item=item)



if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)