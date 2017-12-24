#Flask项目

###回顾

1. web工作原理

   客户端 <=> WEB服务器(nginx/apache) <=> Flask <=> 数据库

   > Python的web框架自带了一个测试的Web服务器

2. Flask框架的两大核心模块

   1. 路由、调试、WSGI系统
   2. 模板引擎(Jinja2)

3. 标准完整代码

   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def index():
   	return 'Hello Flask!'
   	
   if __name__ == '__main__':
   	app.run()
   ```

4. request（请求）

   http://127.0.0.1:5000/user?username=xiaoming&password=123456

   request.args：get请求参数

   request.method：请求方法

   request.headers：所有的请求头信息

   request.cookies：所有的cookie信息

   request.form：提交的表单

5. response（响应）

   要求：返回字符串 [, 状态码]

   构造响应：make_response

   构造路由：url_for('user', username='xiaoming', page=3, _external=True)

   ​	结果：http://127.0.0.1:5000/user/xiaoming?page=3

   ```python
   @app.route('/user/<username>')
   def user(username):
   	pass
   ```

6. 重定向(redirect)

7. 终止(abort)

8. 会话控制(cookie/session)

9. flask-script、Manager

10. 模板引擎

  模板文件存放在templates

  渲染模板文件：render_template

  渲染模板字符串：render_template_string

  {# 注释 #}

  {{ username }}

  {{ username | capitalize }}

  {% if xxx %}

  {% endif %}

  宏、包含、继承(extends、block、super)

  bootstrap

  错误页面定制

  ```python
  @app.errorhandler(404)
  def page_not_found(e):
      return '页面未找到'
  ```

11. 加载静态资源

    所有的静态资源文件统一存放在static目录下

    url_for('static', filename='meinv.jpg')

12.时间戳显示flask-moment

13. 表单处理（flask-wtf）

    wtf.quick_form(form)

14. 文件上传（flask-uploads）

    post、enctype=multipart/form-data

    上传信息：request.files

15. 邮件发送(flask-mail)

    邮件发送可能受限于网络等原因，封装异步发送邮件函数

16. flash消息

17. 数据库（flask-sqlalchemy）

18. 蓝本（Blueprint）

总结：FMVT、MVC

### Flask项目(blog)

1. 大型项目目录结构

   ```
   project/
   	app/					# 存放所有的应用程序
   		static/					# 静态资源文件
   			js/						# js脚本
   			css/					# 层叠样式表
   			img/					# 图片
   			favicon.ico				# 网站图标
   		templates/				# 模板文件
   			common/					# 通用模板文件			
   			errors/					#  错误显示
   			email/					# 邮件模板
   			main/					# 主页面模板
   			user/					# 用户模块模板
   			posts/					# 帖子模块模板
   		models/					# 数据模型
   		forms/					# 提交表单
   		views/					# 视图函数
   		config.py				# 配置文件
   		email.py				# 邮件发送
   		extensions.py			# 所有扩展
   	migrations/				# 数据库迁移目录
   	test/					# 测试单元
   	venv/					# 虚拟环境目录
   	requirements.txt		# 项目的依赖包
   	manage.py				# 项目启动控制文件
   ```

2. 开始书写项目配置文件


   1. 书写配置文件config.py，对外公开一个配置字段config

      ```python
      # 对外公开的配置字典
      config = {
          'development': DevelopmentConfig,
          'testing': TestingConfig,
          'production': ProductionConfig,

          'default': DevelopmentConfig
      }
      ```

   2. 在上层__ init __.py包文件中使用即可，代码如下：

      ```python
      # 封装一个对外公开的方法，专门用于创建Flask对象
      def create_app(config_name):
          # 创建应用实例
          app = Flask(__name__)
          # 初始化配置
          app.config.from_object(config[config_name])
          # 调用初始化函数
          config[config_name].init_app(app)
          # 返回应用实例
          return app
      ```

   3. 在最外层的启动控制文件manage.py中调用，如下：

      ```python
      import os
      from app import create_app
      from flask_script import Manager

      # 获取配置参数名
      config_name = os.environ.get('FLASK_CONFIG') or 'default'
      # 根据配置参数名，创建Flask实例
      app = create_app(config_name)
      # 添加命令行控制
      manager = Manager(app)

      @app.route('/')
      def index():
          return '欢迎访问本博客'

      # 启动应用程序
      if __name__ == '__main__':
          manager.run()
      ```

3. 添加各种扩展，

   1. 在extensions.py文件中添加代码，如下：

      ```python
      # 导入相关类库
      from flask_bootstrap import Bootstrap
      from flask_sqlalchemy import SQLAlchemy
      from flask_mail import Mail
      from flask_moment import Moment

      # 创建相关对象
      bootstrap = Bootstrap()
      db = SQLAlchemy()
      mail = Mail()
      moment = Moment()

      # 完成相关初始化
      def config_extensions(app):
          bootstrap.init_app(app)
          db.init_app(app)
          mail.init_app(app)
          moment.init_app(app)
      ```

   2. 在上层的包文件__ init __.py中，调用函数即可，如下：

      ```python
      # 封装一个对外公开的方法，专门用于创建Flask对象
      def create_app(config_name):
          # 创建应用实例
          app = Flask(__name__)
          ...
          # 初始化各种扩展
          config_extensions(app)
          # 返回应用实例
          return app
      ```

4. 添加蓝本

   1. 在views目录下创建文件main.py，内容如下：

      ```python
      from flask import Blueprint

      main = Blueprint('main', __name__)

      @main.route('/')
      def index():
          return '欢迎访问本博客'
      ```

   2. 在views的包文件__ init __.py中，添加如下内容：

      ```python
      from .main import main
      from .user import user

      # 蓝本配置
      DEFAULT_BLUEPRINT = (
          # 蓝本，url前缀
          (main, '/main'),
          (user, '/user'),
      )

      # 注册蓝本
      def config_blueprint(app):
          for blue_print, url_prefix in DEFAULT_BLUEPRINT:
              app.register_blueprint(blue_print, url_prefix=url_prefix)
      ```

   3. 上层调用

      ```python
      def create_app(config_name):
          # 创建应用实例
          app = Flask(__name__)
          ...
          # 配置蓝本
          config_blueprint(app)
          # 返回应用实例
          return app
      ```

   4. 自行添加蓝本

      1. 在views下创建蓝本文件
      2. 在views包文件中导入并在配置中添加一条

### 扩展(环境变量)

说明：在系统运行时为了方便查找特定的内容而设置的特殊变量

操作：

​	Windows：

​		设置：set NAME=xiaoming

​		获取：set NAME

​	unix：

​		导出：export NAME=xiaoming

​		使用：echo $NAME	

​	代码：

​		import os

​		name = os.environ.get('NAME')	