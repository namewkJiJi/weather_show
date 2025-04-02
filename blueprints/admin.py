from flask import Blueprint,render_template, redirect, url_for, flash
from flask import request
from models import Weather

from extension import db

bp = Blueprint("admin",__name__,url_prefix="/admin")


@bp.route("/")
def index():
    print("enter admin")
    # 从数据库中获取所有数据
    datas = Weather.query.all()
    print(datas)  # 打印调试
    # 将数据数据传递到模板
    return render_template("admin.html", datas=datas)



# 添加数据
@bp.route('/add_data', methods=['POST'])
def add_data():
    print("in add data")
    data = request.get_json()  # 获取 JSON 数据
    id = data.get('id')
    temp = data.get('temp')
    aireaq = data.get('aireaq')
    dy = data.get('dy')
    qing = data.get('qing')
    hc = data.get('hc')
    xue = data.get('xue')
    yu = data.get('yu')
    yin = data.get('yin')
    city = data.get('city')
    month = data.get('month')
    year = data.get('year')


    if Weather.query.filter_by(id=id).first():
        flash('已存在')
        return redirect(url_for('admin.index'))

    new_data = Weather(id=id,
                       temp=temp,
                       aireaq=aireaq,
                       dy=dy,
                       qing=qing,
                       hc=hc,
                       xue=xue,
                       yu=yu,
                       yin=yin,
                       city=city,
                       month=month,
                       year=year,
                       )
    db.session.add(new_data)
    db.session.commit()

    flash('添加成功')
    return redirect(url_for('admin.index'))

# 更新数据
@bp.route('/update_data', methods=['POST'])
def update_data():
    data = request.get_json()
    id = data.get('id')
    field = data.get('field')
    new_value = data.get('newValue')

    # 查找对应 id 的数据
    weather = Weather.query.filter_by(id=id).first()

    if weather:
        # 根据字段名称动态更新对应字段的值
        if field == 'temp':
            weather.temp = new_value
        elif field == 'aireaq':
            weather.aireaq = new_value
        elif field == 'dy':
            weather.dy = new_value
        elif field == 'qing':
            weather.qing = new_value
        elif field == 'hc':
            weather.hc = new_value
        elif field == 'xue':
            weather.xue = new_value
        elif field == 'yu':
            weather.yu = new_value
        elif field == 'yin':
            weather.yin = new_value

        db.session.commit()
        flash('数据更新成功')
    else:
        flash('数据未找到')

    return redirect(url_for('admin.index'))

# 删除数据
@bp.route('/delete_data')
def delete_data():
    id = request.args.get('id')
    weather = Weather.query.filter_by(id=id).first()

    if weather:
        db.session.delete(weather)
        db.session.commit()
        flash('数据删除成功')
    else:
        flash('数据未找到')

    return redirect(url_for('admin.index'))


