from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from . import main
# from .learner import LearnerDashboard as ld
from ..models import User, Course, Tasks, Target
from .. import db


@main.route('/')
@main.route('/index')
@main.route('/dashboard')
@login_required
def dashboard():
    # all_courses = ld.get_all_courses()
    return render_template('learner_dashboard.html',) #all_courses=all_courses)


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
    # all_course_tasks = ld.get_all_course_tasks(1)
    return render_template('user_courses.html', )#course_tasks=all_course_tasks)


@main.route('/user/tasks')
def user_tasks():
    # all_task_targets = ld.get_all_task_targets(task_id=1)    
    return render_template('user_courses.html',)# all_task_targets=all_task_targets)


@main.route('/admin/my_checkpoints')
@login_required
def admin_checkpoints():
    return render_template('user_courses.html')


# @main.route('/courses')
# def ld_all_courses():
#     all_courses = ld.get_all_courses()
#     return render_template('learner_dashboard.html', all_courses=all_courses)


# @main.route('/course/<int:course_id>')
# def ld_all_tasks(course_id):
#     all_course_tasks = ld.get_all_course_tasks(course_id)
#     return render_template('user_courses.html', course_tasks=all_course_tasks)


#@learner.route('/course/<int: course_id>/tasks/<int: task_id>')
# @main.route('/targets')
# def ld_all_targets():
#     all_task_targets = ld.get_all_task_targets(task_id)
#     target_form = TargetForm()
#     # return render_template('targets.html', task_targets=all_task_targets)
#     return render_template('user_tasks.html')
