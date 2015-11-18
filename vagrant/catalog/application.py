from flask import Flask, render_template, url_for, request, redirect
from flask import jsonify, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Category, Items
import datetime

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
    items = session.query(Items).order_by(desc(Items.date)).limit(5)
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
@app.route('/catalog/add', methods=['GET', 'POST'])
def addItem():
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Items(
            name=request.form['name'],
            description=request.form['description'],
            picture=request.form['picture'],
            category=session.query(Category).filter_by(name=request.form['category']).one(),
            date=datetime.datetime.now())
        session.add(newItem)
        session.commit()
        flash('Item Successfully Added!')
        return redirect(url_for('showCatalog'))
    else:
        return render_template('additem.html', categories=categories)

# Add an item to a Category
@app.route('/catalog/<category_name>/add', methods=['GET', 'POST'])
def addCategoryItem(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        newItem = Items(
            name=request.form['name'],
            description=request.form['description'],
            picture=request.form['picture'],
            category=session.query(Category).filter_by(name=request.form['category']).one(),
            date=datetime.datetime.now())
        session.add(newItem)
        session.commit()
        flash('Category Item Successfully Added!')
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('addcategoryitem.html',
                            category=category, categories=categories)

# Show the specifics of an item
@app.route('/catalog/<category_name>/<item_name>/')
def showItem(category_name, item_name):
    item = session.query(Items).filter_by(name=item_name).one()
    return render_template('itemdescription.html',
                            item=item)

# Edit an item
@app.route('/catalog/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    editedItem = session.query(Items).filter_by(name=item_name).one()
    categories = session.query(Category).all()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['picture']:
            editedItem.picture = request.form['picture']
        if request.form['category']:
            category = session.query(Category).filter_by(name=request.form['category']).one()
            editedItem.category = category
        time = datetime.datetime.now()
        editedItem.date = time
        session.add(editedItem)
        session.commit()
        flash('Category Item Successfully Edited!')
        return  redirect(url_for('showCategoryItems',
                                        category_name=editedItem.category.name))
    else:
        return render_template('edititem.html',
                                item=editedItem, categories=categories)

# Delete an item
@app.route('/catalog/<category_name>/<item_name>/delete', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    itemToDelete = session.query(Items).filter_by(name=item_name).one()
    category = session.query(Category).filter_by(name=category_name).one()
    if request.method =='POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted! We will miss that '+itemToDelete.name)
        return redirect(url_for('showCategoryItems', category_name=category.name))
    else:
        return render_template('deleteitem.html', item=itemToDelete)


  #####  ###   ###  #   #
    #   #     #   # ##  #
    #   ####  #   # # # #
    #       # #   # #  ##
  ##     ###   ###  #   #

# JSON APIs to view category and Item information
@app.route('/catalog.JSON')
def allItemsJSON():
    categories = session.query(Category).all()
    category_dict = [c.serialize for c in categories]
    # Best way I found to replicate the JSON call picture in the assignment
    # notes. Does this look ok?
    for c in range(len(category_dict)):
        items = [i.serialize for i in session.query(Items)\
                    .filter_by(category_id=category_dict[c]["id"]).all()]
        if items:
            category_dict[c]["Item"] = items
    return jsonify(Category=category_dict)

@app.route('/catalog/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/catalog/<category_name>/JSON')
def categoryItemsJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Items).filter_by(category=category).all()
    return jsonify(items=[i.serialize for i in items])

@app.route('/catalog/<category_name>/<item_name>/JSON')
def ItemJSON(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    item = session.query(Items).filter_by(name=item_name,\
                                        category=category).one()
    return jsonify(item=[item.serialize])



if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)