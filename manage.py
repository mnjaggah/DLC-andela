from app import app, db
from app.models import User,Course, Task
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username='admin', email='admin@andela.com',password='andela', is_admin=True, is_learner=False))
    db.session.add(Course(name="python", description="This is a test"))
    db.session.add(Course(name="Java Script", description="This is a test"))
    db.session.add(Task(task_name="amity", task_description="office space", course_id=1))

    db.session.commit()
    print ('Intialized')

@manager.command
def dropdb():
    db.drop_all()
    print ('Done')

if __name__ == '__main__':
    manager.run()