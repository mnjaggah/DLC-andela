from app import app, db
from app.models import User
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    db.session.add(User(username='jimmy', email='jimmy@gmail.com',password='cat'))
    db.session.commit()
    print 'Intialized'

@manager.command
def dropdb():
    db.drop_all()
    print 'Done'

if __name__ == '__main__':
    manager.run()