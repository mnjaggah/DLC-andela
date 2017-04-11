
from flask import Flask, render_template, url_for, request, redirect, url_for, flash, abort,request
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from .forms import SigninForm, SignupForm
from .models import User


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
@login_required
def home():
    return render_template('base.html')


@app.route('/index')
@login_required
def index():
    return render_template('base.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully')
            return redirect(request.args.get('next') or url_for('dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("You have successfully registered! You may now login.")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/user')
def user():
    # user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html')

@app.errorhandler(404)
def page_not_found(e):
     return render_template('404.html'), 404
     
@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500    