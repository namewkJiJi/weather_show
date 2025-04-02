from flask import Flask
from flask_migrate import Migrate
from blueprints.index import bp as index_bp
from blueprints.admin import bp as admin_bp

from extension import db

app = Flask(__name__)

# 数据库配置
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "wkz"
PASSWORD = 123456
DATABASE = "weather"
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
SQLALCHEMY_DATABASE_URI = DB_URI
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI



# 关联配置文件
app.secret_key = 'secret_key'
# 关联蓝图
app.register_blueprint(index_bp)
app.register_blueprint(admin_bp)

# 数据库连接
db.init_app(app)

# orm模型迁移到表中
migrate = Migrate(app, db)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello world!'


if __name__ == '__main__':
    app.run()
