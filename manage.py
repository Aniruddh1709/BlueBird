import unittest

# from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_script import Server


from app import app




# migrate = Migrate(app, db)

# manager.add_command('db', MigrateCommand)
manager = Manager(app)

server = Server(host=app.config['HOST_SERVER_URL'],
                port=app.config['HOST_SERVER_PORT'])
manager.add_command("runserver", server)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1




if __name__ == "__main__":
    app.debug=True
    manager.run()
