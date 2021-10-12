import sqlite3

banco = sqlite3.connect('database.sqlite')

cursor = banco.cursor()

cursor.execute("CREATE TABLE Crud (id integer not null primary key, name varchar (100), lastname varchar (100), birthdate varchar (100), email varchar (100), phone varchar (100), adddate varchar (100), hour varchar (100)  )")
 

banco.commit()

