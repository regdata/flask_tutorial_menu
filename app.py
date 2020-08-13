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

@app.route('/')
@app.route('/restaurants')
def index():
   return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
