from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user
from . import main
# from .learner import LearnerDashboard as ld
from ..models import User, Course, Tasks, Target, Facilitator

from .forms import CoursesForm, TasksForm, AddFacilitatorsForm, FacilitatorLoginForm
from .. import db


# @main.route('/')
@main.route('/user')
@login_required
def dashboard():
    courses = Course.query.all()
    if not courses:
        flash("No available course")
    return render_template('learner_dashboard.html', courses=courses)




@main.route('/')
@main.route('/admin/dashboard')
@main.route('/index')
@main.route("/admin/courses", methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    """ List all courses """
    courses = Course.query.all()
    if not courses:
        flash("No available course")
    return render_template('admin_dashboard.html', courses=courses)


@main.route("/admin/add", methods=['GET', 'POST'])
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


@main.route("/admin/<int:id>", methods=['GET', 'POST'])
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
        course_id = request.args.get('course_id')
        if not course_id:
            # courses = Course.query.all()
            tasks = Tasks.query.filter_by(course_id=id)
            return render_template('user_checkpoints.html', tasks=tasks, course_id=id)
        form = TasksForm()
        return render_template('add_task.html', course_id=id, form=form)

@main.route('/admin/<int:id>', methods=['GET', 'POST'])
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
    return redirect(url_for('main.admin_dashboard'))

@main.route('/admin/all_learners')
@login_required
def get_learner():
    """
    Method to get a random facilitator
    """
    user = User.query.all()

    return render_template('all_learners.html',
                           user=user,
                           email="email"
                           )  


@main.route('/admin/all_facilitators')
@login_required
def get_facilitator():
    """
    Method to get a random facilitator
    """
    facilitator = Facilitator.query.all()

    return render_template('all_facilitators.html',
                           facilitator=facilitator,
                           email="email"
                           )                           

def get_facilitator():
    """
    Method to get a random facilitator
    """
    facilitators = Facilitator.query.all()
    allocated_facilitator = random.choice(facilitators)

    return allocated_facilitator.email


@main.route('/user')
@login_required
def facilitator_ashboard():
    
    return render_template('facilitator_dashboard.html')



@main.route('/facilitator_login', methods=['GET', 'POST'])
def facilitator_login():
    form = FacilitatorLoginForm()
    if form.validate_on_submit():
        facilitator = Facilitator.query.filter_by(
            email=form.email.data).first()
        if facilitator:
            login_user(facilitator)
            # return render_template('dashboard.html')
            return redirect(url_for('view_allocated_learners'))

    return render_template('facilitator_login.html', form=form)


@main.route('/admin/add_facilitator', methods=['GET', 'POST'])
@login_required
def add_facilitator():
    """
    Functionality to add facilitators to the system
    """

    form = AddFacilitatorsForm()
    if form.validate_on_submit():
        facilitator = Facilitator(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
        )
        try:
            db.session.add(facilitator)
            db.session.commit()
            flash('Succesfully added facilitator')
        except:
            flash('Facilitator email already exists.')

        return redirect(url_for('main.admin_dashboard'))
    return render_template(
        'add_facilitator.html', form=form)


@main.route('/admin/facilitators', methods=['GET', 'POST'])
@login_required
def view_facilitators():
    """
    Function to view all facilitators
    """

    all_facilitators = Facilitator.query.all()
    return render_template('all_facilitators.html',
                           all_facilitators=all_facilitators,
                           title="Facilitators"
                           )


@main.route('/facilitator/dashboard', methods=['GET', 'POST'])
@login_required
def facilitator_dashboard():
    return render_template('facilitators_dashboard.html', title="Dashboard")


@main.route('/facilitator/all_learners', methods=['GET', 'POST'])
@login_required
def my_learners():
    """
    This function lists all learners allocated
    to a facilitator
    """
    # my_learners = User.query.filter_by(facilitator='maz@andela.com').all()

    return render_template('my_learners.html') #my_learners=my_learners)


# @main.route('/user')
# def user():
#     # user = User.query.filter_by(username=username).first_or_404()
#     return render_template('user_profile.html')


# @main.route('/user/my_checkpoints')
# def user_checkpoints():
#     # all_course_tasks = ld.get_all_course_tasks(1)
# return render_template('user_checkpoints.html',
# )#course_tasks=all_course_tasks)


# @main.route('/user/tasks')
# def user_tasks():
#     # all_task_targets = ld.get_all_task_targets(task_id=1)
# return render_template('user_checkpoints.html',tasks=tasks)#
# all_task_targets=all_task_targets)


# @main.route('/admin/my_checkpoints')
# @login_required
# def admin_checkpoints():
#     return render_template('user_courses.html')


# # @main.route('/courses')
# # def ld_all_courses():
# #     all_courses = ld.get_all_courses()
# #     return render_template('learner_dashboard.html', all_courses=all_courses)


# # @main.route('/course/<int:course_id>')
# # def ld_all_tasks(course_id):
# #     all_course_tasks = ld.get_all_course_tasks(course_id)
# #     return render_template('user_courses.html', course_tasks=all_course_tasks)


# #@learner.route('/course/<int: course_id>/tasks/<int: task_id>')
# # @main.route('/targets')
# # def ld_all_targets():
# #     all_task_targets = ld.get_all_task_targets(task_id)
# #     target_form = TargetForm()
# #     # return render_template('targets.html', task_targets=all_task_targets)
# #     return render_template('user_tasks.html')
# @main.route("/courses/add", methods=['GET', 'POST'])
# @login_required
# def add_course():
#     """ Add course """
#     add_course = True
#     form = CoursesForm()
#     if form.validate_on_submit():
#         course = Course(name=form.name.data,
#                         description=form.description.data)
#         try:
#             db.session.add(course)
#             db.session.commit()
#             flash('You have successfully added a new course.')
#         except:
#             # in case course name already exists
#             flash('Error: course name already exists.')
#         # redirect to courses page
#         return redirect(url_for('main.admin_dashboard'))
#     return render_template('add_course.html', form=form)
