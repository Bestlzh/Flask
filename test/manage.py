
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from flask_script import Manager
# 获取配置参数名
from app.extensions import db

# 根据配置参数名，创建Flask实例
app = create_app('default')
# 添加命令行控制
manager = Manager(app)
manager.add_command('db',MigrateCommand)
# 启动应用程序
if __name__ =='__main__':
    manager.run()