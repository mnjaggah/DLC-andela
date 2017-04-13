from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from .forms import CoursesForm, TasksForm
from . import admin
from ..models import Course, Tasks
from .. import db


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


@admin.route("/courses", methods=['GET', 'POST'])
@login_required
def list_courses():
    """ List all courses """
    courses = Course.query.all()
    if not courses:
        flash("No available course")
    return render_template('admin_dashboard.html', courses=courses)


@admin.route("/courses/add", methods=['GET', 'POST'])
@login_required
def add_course():
    """ Add course """
    add_course = True
    form = CoursesForm()
    if form.validate_on_submit():
        course = Course(name=form.name.data,
                        description=form.description.data)
        try:
            db.session.add(course)
            db.session.commit()
            flash('You have successfully added a new course.')
        except:
            # in case course name already exists
            flash('Error: course name already exists.')
        # redirect to courses page
        return redirect(url_for('main.admin_dashboard'))
    return render_template('add_course.html', form=form)


@admin.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_course(id):
    """ Edit a course """
    add_course = False
    course = Course.query.get_or_404(id)
    form = CoursesForm(obj=course)
    if form.validate_on_submit():
        course.name = form.name.data
        course.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the course.')
        return redirect(url_for('list_courses'))

    form.description.data = course.description
    form.name.data = course.name
    return render_template('addcourse.html', add_course=add_course, form=form)


@admin.route('/course/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_course(id):
    """ Delete a course from the database """
    course = Course.query.get_or_404(id)
    tasks = Tasks.query.filter_by(course_name=course.name).all()
    for task in tasks:
        db.session.delete(task)
    db.session.delete(course)
    db.session.commit()
    flash('You have successfully deleted the course.')
    # redirect to the courses page
    return redirect(url_for('list_courses'))


@admin.route("/tasks/add/<int:id>", methods=['GET', 'POST'])
@login_required
def add_tasks(id):
    """ Add task """
    if request.method == "POST":
        
        form = TasksForm()
        if form.validate_on_submit():
            task = Tasks(task_name=form.TaskName.data,
                        task_description=form.description.data, course_id=id)
            try:
                db.session.add(task)
                db.session.commit()
                flash('You have successfully added a new task.')
            except:
                # in case course name already exists
                flash('Error: task name already exists.')
            # redirect to courses page
            return redirect(url_for('main.user_tasks'))
        return render_template('add_course.html', form=form)
    elif request.method == 'GET':
        course_id = request.args.get('course_id');
        if not course_id:
            # courses = Course.query.all()
            tasks = Tasks.query.filter_by(course_id=id)
            return redirect(url_for('main.user_checkpoints'))
        form = TasksForm()
        return render_template('add_task.html', course_id=id, form=form)