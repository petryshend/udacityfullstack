from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

# Task 1: Create route for newMenuItem function here

@app.route('/create/<int:restaurant_id>/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description'],
            restaurant_id=restaurant_id
             )
        session.add(newItem)
        session.commit()
        flash('New Menu Item Created!!!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('create.html') 

# Task 2: Create route for editMenuItem function here

@app.route('/edit/<int:restaurant_id>/<int:menu_id>/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        menuItem.name = request.form['name']
        menuItem.price = request.form['price']
        menuItem.description = request.form['description']
        session.add(menuItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('edit.html', item=menuItem, restaurant=restaurant)

# Task 3: Create a route for deleteMenuItem function here

@app.route('/delete/<int:restaurant_id>/<int:menu_id>/', methods=['POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(menuItem)
        session.commit()
        flash('You have daleted ' + menuItem.name)
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return "This is only for post!"

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)