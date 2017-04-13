import random

from flask import Flask, render_template, url_for, request, redirect, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from .forms import SigninForm, SignupForm, AddFacilitatorsForm, FacilitatorLoginForm, FeedbackForm
from .models import User, Facilitator


def check_admin():
    """
    Checks if current user is admin
    """
    if not current_user.is_admin:
        abort(403)

def get_facilitator():
    """
    Method to get a random facilitator
    """
    facilitators = Facilitator.query.all()
    allocated_facilitator = random.choice(facilitators)

    return allocated_facilitator.email



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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    facilitator=get_facilitator()
                    )
        db.session.add(user)
        db.session.commit()
        # flash("You have successfully registered! You may now login.")
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)    


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            # flash('Logged in successfully')
            return redirect(request.args.get('next') or url_for('dashboard'))
        # flash('Invalid username or password.')

    return render_template('login.html', form=form)


@app.route('/facilitator_login', methods=['GET','POST'])
def facilitator_login():
    form = FacilitatorLoginForm() 
    if form.validate_on_submit():
        facilitator = Facilitator.query.filter_by(email=form.email.data).first()
        if facilitator :
            login_user(facilitator)
            #return render_template('dashboard.html')
            return redirect(url_for('view_allocated_learners'))

    return render_template ('facilitator_login.html', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/facilitators/add', methods=['GET','POST'])
@login_required
def add_facilitator():
    """
    Functionality to add facilitators to the system
    """
    check_admin()
    

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

        return redirect(url_for('view_facilitators'))
    return render_template(
        'add_facilitator.html',form=form)


@app.route('/facilitators', methods=['GET','POST'])
@login_required
def view_facilitators():
    """
    Function to view all facilitators
    """
    check_admin()

    all_facilitators = Facilitator.query.all()
    return render_template('all_facilitators.html',
        all_facilitators=all_facilitators,
        title="Facilitators"
        )


"""@app.route('/facilitator/dashboard', methods=['GET','POST'])
@login_required
def feedback_comments():
    form = FeedbackForm()
    if form.validate_on_submit():
        comment = Comments(
            comment = form.comment.data
        )
        db.session.add(comment)
        db.session.commit()

    return render_template('facilitators_dashboard.html', title="Dashboard")
"""


@app.route('/facilitator/all_learners', methods=['GET','POST'])
@login_required
def view_allocated_learners():
    """
    This function lists all learners allocated
    to a facilitator
    """
    my_learners = User.query.filter_by(facilitator="maz@andela.com").all()


    #my_learners = User.query.all()
        
    return render_template('my_learners.html', my_learners=my_learners)

