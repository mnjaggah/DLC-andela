from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from . import main
from ..models import User, Course, Tasks
from .. import db


@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    # if not current_user.is_admin:
    #     abort(403)

    return render_template('admin_dashboard.html', title="Dashboard")