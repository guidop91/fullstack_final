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



@app.route('/')
@app.route('/restaurants')
def Restaurant():
    restaurants = session.query(Restaurant).all()
    return render_template('list.html', restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET','POST'])
def NewRestaurant():
    return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit',methods=['GET','POST'])
def EditRestaurant(restaurant_id):
    return render_template('editrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/delete',methods=['GET','POST'])
def DeleteRestaurant(restaurant_id):
    return render_template('deleterestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/menu')
def RestaurantMenu(restaurant_id):
    for r in restaurants:
        current = ''
        if r['id'] == str(restaurant_id):
            current = r
            break
    
    return render_template('restaurant_menu.html',restaurant=current,items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new',methods=['GET','POST'])
def NewMenuItem(restaurant_id):

    return render_template('new_menu_item.html',restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit',methods=['GET','POST'])
def EditMenuItem(restaurant_id,menu_id):
    for i in items:
        current_item = ''
        if i['id'] == str(menu_id):
            current_item = i
            break

    for r in restaurants:
        current = ''
        if r['id'] == str(restaurant_id):
            current_restaurant = r
            break

    return render_template('edit_menu_item.html',restaurant = current_restaurant, item = current_item)
    

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete',methods=['GET','POST'])
def DeleteMenuItem(restaurant_id,menu_id):
    for i in items:
        current_item = ''
        if i['id'] == str(menu_id):
            current_item = i
            break

    for r in restaurants:
        current = ''
        if r['id'] == str(restaurant_id):
            current_restaurant = r
            break

    return render_template('delete_menu_item.html',restaurant = current_restaurant, item = current_item)

session.close()

if __name__ == '__main__':
    app.secret_key = 'super_ssj3_goku'
    app.debug = True
    app.run(host='0.0.0.0',port=5000)