from sqlite3.dbapi2 import Cursor
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from flask_login import LoginManager, login_user, login_required, UserMixin, current_user
from flask import Flask, request, render_template
from collections import defaultdict
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
    birthdate = db.Column(db.Integer)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    adddate = db.Column(db.Integer) 
    hour = db.Column(db.String(100))

    def __init__(self, name, lastname, birthdate, email, phone, adddate, hour):
        self.name = name
        self.lastname = lastname
        self.birthdate = birthdate
        self.email = email
        self.phone = phone
        self.adddate = adddate
        self.hour = hour


        # login #
        
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = {
    1: User(1, 'admin', 'admin') #usuário e senha
    
}

nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.username]['password'] = i.password
    user_check[i.username]['id'] = i.id

        

@login_manager.user_loader
def load_user(id):
    return users.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if username in user_check and password == user_check[username]['password']:
            id = user_check[username]['id']
            login_user(users.get(id))

            return redirect(url_for('index'))
        else:
            return render_template('401.html')
    else:
        return render_template('login.html')


@app.route('/', methods=['GET', 'POST'], defaults={"page": 1})
@app.route('/<int:page>', methods=['GET', 'POST'])
@login_required
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
    
        # modal novo agendamento

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

        # formulário separado 


@app.route('/form')
def indexfo():
    all_data = Crud.query.all()
    return render_template("form.html", all_data = all_data)

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


                # home 

@app.route('/home')
def home():
    all_data = Crud.query.all()
    return render_template("home.html", all_data = all_data)


            # modal update 

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

        #modal delete

@app.route('/delete/<id>/')
def delete(id):
    my_data = Crud.query.get(id)
    db.session.delete(my_data)
    db.session.commit()

    flash("Dados do paciente foram excluídos com sucesso")
    return redirect(url_for('index'))

@app.route('/401')
def page_not():
    all_data = Crud.query.all()
    return render_template("401.html", all_data = all_data)

#if __name__ == "__main__":
    #port = int(os.getenv('PORT'), '5000')
    #app.run(host='0.0.0.0', port = port)


    
if __name__ == "__main__":
    app.run(debug = True)


