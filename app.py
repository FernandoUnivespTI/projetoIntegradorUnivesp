from sqlite3.dbapi2 import Cursor
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy 
import os
from sqlalchemy import or_

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
    adddate = db.Column(db.String(100)) 
    hour = db.Column(db.String(100))

    def __init__(self, name, lastname, birthdate, email, phone, adddate, hour):
        self.name = name
        self.lastname = lastname
        self.birthdate = birthdate
        self.email = email
        self.phone = phone
        self.adddate = adddate
        self.hour = hour
       

@app.route('/', methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/<int:page>', methods=['GET', 'POST'])
def index(page):
    page = page
    pages = 5
    all_data = Crud.query.order_by(Crud.id.desc()).paginate(page,pages,error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        all_data = Crud.query.filter(Crud.name.like(search)).paginate(per_page=pages, error_out=False)
        return render_template("index.html", all_data = all_data, tag=tag)
    return render_template("index.html", all_data = all_data,)
    
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['nome']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        email = request.form['email']
        phone = request.form['phone']
        adddate = request.form['adddate']
        hour = request.form['hour']
        

        my_data = Crud(name, lastname, birthdate, email, phone, adddate, hour)
        db.session.add(my_data)
        
        db.session.commit()

        flash("Paciente inserido com sucesso")
        return redirect(url_for('index'))

############################################################

@app.route('/form')
def indexfo():
    all_data = Crud.query.all()
    return render_template("form.html", all_data = all_data)

@app.route('/login')
def lo():
    all_data = Crud.query.all()
    return render_template("login.html", all_data = all_data)

@app.route('/form', methods = ['POST'])
def form():
    if request.method == 'POST':
        name = request.form['nome']
        lastname = request.form['lastname']
        birthdate = request.form['birthdate']
        email = request.form['email']
        phone = request.form['phone']
        adddate = request.form['adddate']
        hour = request.form['hour']

        my_data = Crud(name, lastname, birthdate, email, phone, adddate, hour)
        db.session.add(my_data)
        db.session.commit()

        flash("Sua consulta foi agendada !!! Aguarde contato")
        return redirect(url_for('form'))

######################################################################


@app.route('/update', methods = ['POST'])
def update():
    if request.method == "POST":
        my_date = Crud.query.get(request.form.get('id'))
        my_date.name = request.form['nome']
        my_date.lastname = request.form['lastname']
        my_date.birthdate = request.form['birthdate']
        my_date.email = request.form['email']
        my_date.phone = request.form['phone']
        my_date.adddate = request.form['adddate']
        my_date.hour = request.form['hour']
        
        db.session.commit()
        flash("Paciente alterado com sucesso")
        return redirect(url_for('index'))

@app.route('/delete/<id>/')
def delete(id):
    my_data = Crud.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Dados do paciente foram excluídos com sucesso")
    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug = True)