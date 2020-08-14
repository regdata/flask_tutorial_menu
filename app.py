from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menus.db'
db = SQLAlchemy(app)

class Restaurants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'Restaurant {self.id}'

class MenuItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rest_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'Menu Item {self.id}'

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


if __name__ == "__main__":
    app.run(debug=True)
