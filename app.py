from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy 
import os

app = Flask(__name__)
app.secret_key = "Secret Key"

path = os.path.abspath( os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(path , 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Crud(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    birthdate = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    

    def __init__(self, name, lastname, birthdate, email, phone):
        self.name = name
        self.lastname = lastname
        self.birthdate = birthdate
        self.email = email
        self.phone = phone
        



@app.route('/')
def index():
    all_data = Crud.query.all()
    return render_template("index.html", all_data = all_data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['nome']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        email = request.form['email']
        phone = request.form['phone']
        

        my_data = Crud(name, lastname, birthdate, email, phone)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")
        return redirect(url_for('index'))

@app.route('/update', methods = ['POST'])
def update():
    if request.method == "POST":
        my_date = Crud.query.get(request.form.get('id'))
        my_date.name = request.form['nome']
        my_date.lastname = request.form['lastname']
        my_date.birthdate = request.form['birthdate']
        my_date.email = request.form['email']
        my_date.phone = request.form['phone']
        

        db.session.commit()
        flash("Alterado com sucesso")
        return redirect(url_for('index'))

@app.route('/delete/<id>/')
def delete(id):
    my_data = Crud.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Employee Data Deleted Successfully")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug = True)