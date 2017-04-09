from flask import Flask,render_template,url_for,redirect,url_for,flash
from flask_login import login_required,login_user, logout_user, current_user
from app import app, db, login_manager
from forms import SigninForm, SignupForm
from models import User


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@app.route('/')
# @login_required
def home():
    return 'hello world'

@app.route('/dashboard')
# @login_required
def dashboard():
    return 'hello world'

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    This handles logging in upon
    successful user authentication
    '''    
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            # flash('Logged in successfully')
            return redirect(request.args.get('next') or url_for('dashboard'))
        # flash('Invalid username or password.')
    return render_template('signup_or_register.html', form=form)    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''
    Register a new user to the system
    '''
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()    
        # flash("You have successfully registered! You may now login.")
        return redirect(url_for('login'))
    return render_template('signup_or_register.html' , form=form)   

@app.route("/logout")
def logout():
    '''
    ends a user session and log outs
    '''
    logout_user()
    return redirect(url_for('login'))       