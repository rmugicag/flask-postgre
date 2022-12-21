from flask import Flask, render_template, request, redirect, url_for, session
import re
from config import config
from models import db, User

enviroment = config['development']


def create_app(enviroment):
    app = Flask(__name__)
    app.secret_key = "super secret key"
    app.config.from_object(enviroment)
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app


app = create_app(enviroment)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = User.query.filter_by(email=username, password=password).first()
        if account:
            account = account.to_json()
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['email']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        account = User.query.filter_by(email=email).first()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            User.create({"name": username,
                         "password": password,
                         "email": email})
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
