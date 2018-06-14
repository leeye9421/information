from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from info import create_app, db
from info import models

app = create_app('develop')

# 5、创建数据库迁移对象
manager = Manager(app)
Migrate(app, db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    print(app.url_map)
    manager.run()