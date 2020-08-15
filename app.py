from flask import Flask, render_template, request, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menus.db'
db = SQLAlchemy(app)

class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    menu_items = db.relationship('MenuItems', cascade='all, delete-orphan', backref=db.backref('restaurants', lazy=True))
        
    def __repr__(self):
        return f'Restaurant {self.name}'
    
    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            }

class MenuItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'),nullable=False)
    
    def __repr__(self):
        return f'Menu Item {self.name}'
    
    @property
    def serialize(self):
        return{
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'restaurant_id': self.restaurant_id
            }


@app.route('/<int:id>/JSON')
def restaurant_menu_JSON(id):
    menu_items = MenuItems.query.filter_by(restaurant_id = id).all()
    return jsonify(MenuItems=[i.serialize for i in menu_items])

@app.route('/<int:rest_id>/<int:menu_item_id>/JSON')
def menu_item_JSON(rest_id, menu_item_id):
    menu_item = MenuItems.query.filter_by(id = menu_item_id).one()
    return jsonify(menu_item=menu_item.serialize)

@app.route('/', methods=['GET', 'POST'])
def restaurant_list():

    if request.method == 'POST':
        rest_name = request.form['name']
        new_restaurant = Restaurants(name=rest_name)
        db.session.add(new_restaurant)
        db.session.commit()
        return redirect('/')
    else:
        all_restaurants = Restaurants.query.order_by(Restaurants.name).all()
        return render_template('index.html', restaurants = all_restaurants)

@app.route('/delete/<int:id>')
def delete(id):
    rest = Restaurants.query.get_or_404(id)
    db.session.delete(rest)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    rest = Restaurants.query.get_or_404(id)
    if request.method == 'POST':
        rest.name = request.form['name']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', restaurant = rest)

@app.route('/<int:id>', methods=['GET', 'POST'])
def menu_items_list(id):
    all_menu_items = MenuItems.query.filter_by(restaurant_id=id).all()
    rest = Restaurants.query.get_or_404(id)
    
    if request.method == 'POST':
        menu_item_name = request.form['name']
        menu_item_description = request.form['description']
        new_menu_item = MenuItems(restaurant_id=id, name=menu_item_name, description=menu_item_description)
        db.session.add(new_menu_item)
        db.session.commit()
        return redirect(f'/{id}')
    
    return render_template('menu_items.html', restaurant=rest, menu_items=all_menu_items)
    
@app.route('/<int:rest_id>/delete/<int:id>')
def delete_menu_item(rest_id, id):
    menu_item = MenuItems.query.get_or_404(id)
    db.session.delete(menu_item)
    db.session.commit()
    return redirect(f'/{rest_id}')

@app.route('/<int:rest_id>/edit/<int:id>', methods=['GET', 'POST'])
def edit_menu_item(rest_id, id):
    menu_item = MenuItems.query.get_or_404(id)
    rest = Restaurants.query.get_or_404(rest_id)
    if request.method == 'POST':
        menu_item.name = request.form['name']
        menu_item.description = request.form['description']
        db.session.commit()
        return redirect(f'/{rest.id}')
    else:
        return render_template('edit_menu_item.html', restaurant= rest, menu_item = menu_item)

if __name__ == "__main__":
    app.run(debug=True)
