from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from . import main
from ..models import User, Course, Tasks
from .. import db


@main.route('/')
@main.route('/index')
@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('learner_dashboard.html')


@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    # if not current_user.is_admin:
    #     abort(403)

    return render_template('admin_dashboard.html', title="Dashboard")

@main.route('/user')
def user():
    # user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_profile.html')
@main.route('/user/my_checkpoints')    
def user_checkpoints():
    return render_template('my_checkpoint.html')

@main.route('/user/tasks')    
def user_tasks():
    return render_template('user_tasks.html')  