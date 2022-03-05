from flask import Flask, render_template, redirect, url_for, flash, session
from flask_cors import CORS
from datetime import timedelta
from services.models import db, User, Post
from forms.signUp import SignUpForm
from forms.login import LoginForm

##### CONSTANTS #####
PORT = 3000
DB_FILENAME = 'dbfile.db'
INIT_DB = True  # to create db file


def create_app():
    '''
    Creates a flask app
    Returns
    -------
    (app, db): tuple
        has the app object and the db object
    '''
    # create flask app
    app = Flask(__name__)
    # app.secret_key = 'asdfads234egrg'
    app.permanent_session_lifetime = timedelta(minutes=5)

    # create database extension
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+DB_FILENAME
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']='41e856c5d1833e5d9836c355e738135e'
    db.init_app(app)

    # create flask cors extension
    CORS(app)

    return app, db


# create flask app
app, db = create_app()

# create db file on demand
if INIT_DB:
    db.create_all(app=app)


@app.route("/")
def home():
    
    return render_template("home.html")

@app.route('/signUp', methods=['GET','POST'])
def signUp():
    form = SignUpForm()
    if form.validate_on_submit():
        print('here 1')
        print(form.name.data, form.username.data, form.email.data, form.password.data, sep="\n")
        try:
            User.insert(name=form.name.data, username=form.username.data, email=form.email.data, password=form.password.data)
        except:
            flash(f'Error: Please register again !', 'danger')
            return redirect("/signUp")
        
        flash(f'Account created for {form.name.data} !', 'success')
        print(type(form.password.data))
        return redirect('/login')
    # if form.errors != {}: #If there are not errors from the validations
    #     for err_msg in form.errors.values():
    #         flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('signUp.html',form=form)

# @app.route('/signUp', methods=['POST'])
# def signUp_post():
#     return redirect('/')

@app.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():

        try:
           user= User.getByUsername(username=form.username.data)
        except:
            flash(f'Error: Please login again !', 'danger')
            return redirect("/login")
        
        if user==None or user.password != form.password.data:
            flash(f' Wrong email or password !', 'danger')
            return redirect("/login")
        else:
            session.permanent = True
            session['username'] = form.username.data
            return redirect('/')
    return render_template('login.html',form=form)

# @app.route('/login', methods=['POST'])
# def login_post():
#     return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/addPost')
def addPost_get():
    return render_template('addPost.html')

@app.route('/addPost', methods=['POST'])
def addPost_post():
    return render_template('addPost.html')


if __name__=='__main__':
    app.run(debug=True,port=PORT)
