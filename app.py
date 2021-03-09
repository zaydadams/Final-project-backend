import sqlite3
from flask import Flask, request
from flask import jsonify
from flask_cors import CORS


def init_sqlite_db():

    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS clients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, email TEXT, password TEXT, confirmP TEXT)')
    print("Table created successfully")

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clients")

    print(cursor.fetchall())

    conn = sqlite3.connect('database.db')
    print("Opened database successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS blogs (id INTEGER PRIMARY KEY AUTOINCREMENT, image TEXT, title TEXT, year TEXT, description TEXT)')
    print("Table created successfully")

    conn.execute('CREATE TABLE IF NOT EXISTS admin_blogs (id INTEGER PRIMARY KEY AUTOINCREMENT, image TEXT, title TEXT, year TEXT, description TEXT)')
    print("Table created successfully")
    conn.commit()
    conn.execute("INSERT INTO admin_blogs(image, title, year, description) VALUES ('image','title','year','description')")


    cursor.execute("SELECT * FROM admin_blogs")
    print(cursor.fetchall())


    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blogs")

    print(cursor.fetchall())

    conn.close()


init_sqlite_db()


app = Flask(__name__)
CORS(app)

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] =row[idx]

    return d

@app.route('/')
@app.route('/register/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            name = post_data['name']
            surname = post_data['surname']
            email = post_data['email']
            password = post_data['password']
            confirmP = post_data['confirmP']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO clients (name, surname, email, password, confirmP) VALUES (?, ?, ?, ?, ?)", (name, surname, email, password, confirmP))
                con.commit()
                msg = name + " was successfully added to the database."
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            return {'msg': msg}


@app.route('/login/', methods=["GET"])
def show_userlogin():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM clients")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    return jsonify(records)


@app.route('/loggedIn/', methods=['GET'])
def loggedIn():
     if request.method == "GET":
        msg = None
        try:
            post_data = request.get_json()
            email = post_data['email']
            password = post_data['password']
            print(email, password)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM clients")
                con.commit()
                msg = " succesfully logged in."
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            return {'msg': msg}


@app.route('/delete-clients/<int:clients_id>/', methods=["GET"])
def delete_clients(client_id):

    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM clients WHERE id=" + str(client_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a client in the database: " + str(e)
    finally:
        con.close()
        return jsonify('landing.html', msg=msg)




@app.route('/show-posts/', methods=["GET"])
def show_posts():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM blogs")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    return jsonify(records)
#addpost

@app.route('/')
@app.route('/addP/', methods=['POST'])
def add_newpost():
    if request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            image = post_data['image']
            title = post_data['title']
            year = post_data['year']
            description = post_data['description']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO blogs (image, title, year, description) VALUES (?, ?, ?, ?)", (image, title, year, description))
                con.commit()
                msg = " was successfully added to the database."
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            return jsonify(msg=msg)
