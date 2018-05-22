from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

# Database Stuff
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Stuff for the API thingy. That JSON for the menu info.
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def RestaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)

    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def MenuItemJSON(restaurant_id,menu_id):
    item = session.query(MenuItem).filter_by(_id=menu_id).one()

    return jsonify(item.serialize)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)

    return render_template('menu.html',restaurant=restaurant,items=items)


@app.route('/restaurants/<int:restaurant_id>/new',methods=['POST','GET'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html',restaurant_id=restaurant_id)



@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods=['POST','GET'])
def editMenuItem(restaurant_id,menu_id):

    item = session.query(MenuItem).filter_by(_id=menu_id).one()

    if request.method == 'POST':
        item.name = request.form['name']
        session.add(item)
        session.commit()
        flash('Menu Item successfully edited!')
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))

    else:
        return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id, item=item)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete', methods=['POST','GET'])
def deleteMenuItem(restaurant_id,menu_id):
    item = session.query(MenuItem).filter_by(_id=menu_id).one()

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash('Menu Item successfully deleted!')
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id,menu_id=menu_id))

    else:
        return render_template('deleteitem.html',restaurant_id=restaurant_id,menu_id=menu_id,item=item)

if __name__ == '__main__':
    app.secret_key = 'super_ssj3_goku'
    app.debug = True
    app.run(host='0.0.0.0',port=5000)