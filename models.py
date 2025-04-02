from extension import db

#将orm模型映射成表
# flask db init 初始化环境，生成migrate文件夹
# flask db migrate 生成迁移脚本
# flask db upgrade 运行迁移脚本，同步到数据库中

class Weather(db.Model):
    __tablename__ = "weather_history"
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Text,nullable=False)
    aireaq = db.Column(db.Text,nullable=False)
    dy = db.Column(db.Text,nullable=False)
    qing = db.Column(db.Text,nullable=False)
    hc = db.Column(db.Text,nullable=False)
    yu = db.Column(db.Text,nullable=False)
    xue = db.Column(db.Text,nullable=False)
    yin = db.Column(db.Text,nullable=False)
    city = db.Column(db.Text,nullable=False)
    month = db.Column(db.Text,nullable=False)
    year = db.Column(db.Text,nullable=False)


