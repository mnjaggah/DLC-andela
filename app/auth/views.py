from flask import Flask, render_template, url_for, request, redirect, url_for, flash, abort, request
from flask_login import login_required, login_user, logout_user, current_user
from .import auth
from ..import db
from ..models import User
from .forms import SigninForm, SignupForm


@auth.route('/login', methods=['GET', 'POST'])
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


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@auth.route('/signup', methods=['GET', 'POST'])
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
