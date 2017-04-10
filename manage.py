from app import app, db
from flask_bootstrap import Bootstrap
from app.models import User, Items
from flask_script import Manager, prompt_bool

manager = Manager(app)
Bootstrap(app)


@manager.command
def initdb():
    db.create_all()
    db.session.add(
        User(username='admin', email='admin@andela.com', password='andela'))
    db.session.commit()
    print('Intialized')


@manager.command
def dropdb():
    db.drop_all()
    print('Done')


if __name__ == '__main__':
    manager.run()
