
from flask import Flask, render_template, url_for, request, redirect, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from .forms import SigninForm, SignupForm, CoursesForm, TasksForm
from .models import User, Course, Tasks


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
        user = User.query.filter_by(
            username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            # flash('Logged in successfully')
            return redirect(request.args.get('next') or url_for('dashboard'))
        # flash('Invalid username or password.')
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
        # flash("You have successfully registered! You may now login.")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route("/courses", methods=['GET', 'POST'])
@login_required
def list_courses():
    """ List all courses """
    courses = Course.query.all()
    if not courses:
        flash("No available course")
    return render_template('courses.html', courses=courses)


@app.route("/courses/add", methods=['GET', 'POST'])
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
    return render_template('addcourse.html', form=form)


@app.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
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


@app.route('/course/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_course(id):
    """ Delete a course from the database """
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('You have successfully deleted the course.')
    # redirect to the courses page
    return redirect(url_for('list_courses'))


@app.route("/tasks/add", methods=['GET', 'POST'])
@login_required
def add_tasks():
    """ Add task """
    form = TasksForm()
    if form.validate_on_submit():
        task = Tasks(task_name=form.TaskName.data,
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
    return render_template('addcourse.html', form=form)
