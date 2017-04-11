
from flask import Flask, render_template, url_for, request, redirect, url_for, flash, abort, g
from flask_login import login_required, login_user, logout_user, current_user
from app import app, db, login_manager
from .forms import SigninForm, SignupForm, PostQuestionForm, PostAnswerForm, PostReplyForm
from .models import User, ForumQuestion, ForumAnswer, ForumAnswerReply
from sqlalchemy.orm import exc
from werkzeug.exceptions import abort


def get_object_or_404(model, *criterion):
    try:
        return model.query.filter(*criterion).one()
    except exc.NoResultFound:
        abort(404)


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


@app.route('/forum_categories')
@login_required
def forum_categories():
    return render_template('forum.html')


@app.route('/post_forum_question', methods=('GET', 'POST'))
@login_required
def post_forum_question():
    form = PostQuestionForm()
    if form.validate_on_submit():
        question = ForumQuestion(question_owner_id=current_user.id,
                                 forum_title=form.title.data.strip(),
                                 forum_category=form.categories.data,
                                 forum_question=form.description.data)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('list_forum_questions'))
    return render_template('post_question.html', form=form)


@app.route('/post_answer', methods=('GET', 'POST'))
@login_required
def post_answer():
    form = PostAnswerForm()
    if form.validate_on_submit():
        pass
    return render_template('post_question.html')


@app.route('/post_reply', methods=('GET', 'POST'))
@login_required
def post_reply():
    form = PostReplyForm()
    if form.validate_on_submit():
        pass
    return render_template('post_question.html')


@app.route('/list_forum_questions')
@login_required
def list_forum_questions():
    return render_template('forum_questions.html')


@app.route('/question_thread/<int:question_id>', methods=('GET', 'POST'))
@login_required
def question_thread(question_id=None):
    question_number = request.args.get('question_id', question_id)
    my_question = get_object_or_404(ForumQuestion, ForumQuestion.id == question_number)
    answer_stream = ForumAnswer.query.filter_by(answer_question_id=question_number).all()
    reply_stream = ForumAnswerReply.query.filter_by(question_id=question_number).all()
    answer_form = PostAnswerForm()
    if answer_form.validate_on_submit():
        answer = ForumAnswer(forum_answer=answer_form.answer.data,
                             answer_owner_id=current_user.id,
                             answer_question_id=question_number)
        db.session.add(answer)
        db.session.commit()
        flash("Awesome. You have posted an answer")

    reply_form = PostReplyForm()
    if reply_form.validate_on_submit():
        reply = ForumAnswerReply(reply_text=reply_form.comment.data,
                                 reply_owner_id=current_user.id,
                                 reply_answer_id=reply_form.answer_id.data,
                                 question_id=reply_form.question_id.data
                                 )
        db.session.add(reply)
        db.session.commit()
        flash("Awesome. You have commented on an answer")
    return render_template('forum_question_thread.html', my_question=my_question, reply_form=reply_form,
                           answer_form=answer_form, answer_stream=answer_stream, reply_stream=reply_stream)
