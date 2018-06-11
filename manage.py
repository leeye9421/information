from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from info import create_app,db

app = create_app('develop')

# 配置flask_script,数据库迁移
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

@app.route('/index')
def index():
    return 'hello'

if __name__ == '__main__':
    manager.run()
