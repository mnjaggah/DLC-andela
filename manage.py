from app import app, db
from app.models import User,Course, Tasks, Target
from flask_script import Manager, prompt_bool
from flask_bootstrap import Bootstrap

manager = Manager(app)
Bootstrap(app)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username='admin', email='admin@andela.com',password='andela', is_admin=True, is_learner=False))
    db.session.add(User(username='jimmy', email='jimy@andela.com',password='andela', is_admin=False, is_learner=True))
    db.session.add(User(username='maria', email='maria@andela.com',password='andela', is_admin=False, is_learner=False, is_facilitator=True))
    db.session.add(Course(name="python", description="This is a test"))
    # db.session.add(Course(name="Java Script", description="This is a test"))
    # db.session.add(Tasks(task_name="amity", task_description="office space"))
    # db.session.add(Target(name="Create a git repo", task_id=1))

    db.session.commit()
    print ('Intialized')

@manager.command
def dropdb():
    db.drop_all()
    print ('Done')

if __name__ == '__main__':
    manager.run()