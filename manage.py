from flask_script import Manager
from app import app, db
from app.models import User

manager = Manager(app)


@manager.command
def initdb():
    db.create_all()
    db.session.add(User(firstname='jimmy',lastname='kimani',email='jimmy@gmail.com',password='cat'))
    db.session.commit()
    print 'Intialized'

@manager.command
def dropdb():
    db.drop_all()
    print 'Done'

if __name__ == '__main__':
    manager.run()
