from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from mini_shopping import app, db
from mini_shopping.models import *


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()