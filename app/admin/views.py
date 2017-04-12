from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from forms import CoursesForm, ResourcesForm
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
    return render_template('user_courses.html', courses=courses)


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
        return redirect(url_for('list_courses'))
    return render_template('admin/add_course.html', form=form)


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
    return render_template('admin/add_course.html', add_course=add_course, form=form)


@admin.route('/course/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_course(id):
    """ Delete a course from the database """
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('You have successfully deleted the course.')
    # redirect to the courses page
    return redirect(url_for('list_courses'))


@admin.route("/tasks/add", methods=['GET', 'POST'])
@login_required
def add_tasks():
    """ Add task """
    form = CoursesForm()
    if form.validate_on_submit():
        task = Tasks(task_name=form.name.data,
                     task_description=form.description.data)
        try:
            db.session.add(task)
            db.session.commit()
            flash('You have successfully added a new task.')
        except:
            # in case course name already exists
            flash('Error: task name already exists.')
        # redirect to courses page
        return redirect(url_for('list_courses'))
    return render_template('admin/add_course.html', form=form)


@admin.route('/add/resources', methods=['GET', 'POST'])
@login_required
def add_resource():
    form = ResourcesForm()
    if form.validate_on_submit():
        resource = Course(resource=form.resource.data)
        db.session.add(resource)
        db.session.commit()
        flash('You have successfully added a new resource.')
        return redirect(url_for('list_courses'))
    return render_template('admin/add_course.html', form=form)
@admin.route('/user/my_checkpoints') 
@login_required   
def user_checkpoints():
    return render_template('admin/user_courses.html')