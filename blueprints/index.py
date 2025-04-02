from flask import Blueprint,render_template,jsonify,request,session, redirect, url_for
from comm.get_weather import weather_province,weather_history,count_aqi_levels,get_forecast
from comm.settings import weather_api_key as key
from comm.warning import warning_list
from comm.help import find_dict_by_id
from comm.py_city import pro_citys,find_province_name,find_first_city
import json
import random

bp = Blueprint("index",__name__,url_prefix="/")

warnings = [] # 存储预警信息

# 渲染首页
@bp.route("/")
def index():
    global warnings
    warnings = warning_list(key,3)

    selected_year = '2023'

    print('selected_year= ',selected_year)

    # print('warnings= ',warnings)

    # 获取默认省市值（这里假设是从某个函数或配置中获取）
    default_province = '北京市'  # 默认省
    default_city = '北京'  # 默认市

    return render_template("index.html", warnings=warnings,default_province=default_province, default_city=default_city,year=selected_year)

# 渲染地图上的天气信息
@bp.route('/weather/<province>', methods=['GET'])
def get_weather(province):
    # 处理参数，将字符转转化成浮点数数组
    print("province= ", province,"province type= ",type(province))
    location = province.split(',')
    location = [float(i) for i in location]
    # 得到天气源数据
    weather_data = weather_province(location,key)
    # print("!!!weather_data= ",weather_data)

    # 解析数据
    weather_data = weather_data.get("now")

    info = {}
    info['temp'] = weather_data.get("temp","ERR")
    info['text'] = weather_data.get("text","ERR")
    info['windDir'] = weather_data.get("windDir","ERR")

    return jsonify(info)


# 渲染详细天气页面
@bp.route('/weather_detail', methods=['GET', 'POST'])
def province_page():
    print("\nin province_page():")

    info = {}
    adcode = request.args.get('adcode')

    pro_name = find_province_name(adcode)
    info['pro_name'] = pro_name
    print('pro_name= ',pro_name)

    city_name = find_first_city(adcode)
    info['city_name'] = city_name
    print('city_name= ', city_name)

    days = '7'
    print("province page days = ",days)

    print("out province_page()\n")
    # 使用adcode进行相应处理
    return render_template('weather.html',info=info,days=days)

# 获取天气预报数据
@bp.route('/weather-data', methods=['POST'])
def weather_data():
    print("in weather_data():")

    # 从前端获取省份和城市参数
    data = request.get_json()
    city = data.get('city')

    # 从session获取天数信息
    days = '7'

    print('city= ',city)

    weather_forecast_data = get_forecast(city,days)

    print('weather_forecast_data= ',weather_forecast_data)

    # 将天气预报数据作为JSON返回
    return jsonify(weather_forecast_data)



# 获取首页的图表数据
@bp.route('/chart-data',methods=['POST','GET'])
def chart_data():
    # print("\nin function chart_data:\n")
    data = request.get_json()
    city = data['city']
    year = '2023'

    print('year= ', year,"type year= ",type(year))
    print('city= ',city)


    line_data = []
    pie_data = []
    pie_tip = []
    pie_flag = False  # 代表pie data里没有数据
    aqi_list = []  # aqi 数值
    aqi_data = []  # aqi统计数据

    for month in range(1, 13):
        data = weather_history(city, year, month)

        print(data)

        line_data.append(data.get('avg_high_temp'))
        aqi_list.append(data.get('avg_air_quality_index'))

        if (not pie_flag):
            pie_flag = True
            for _ in data.get("info"):
                pie_data.append(_.get("value"))
                pie_tip.append(_.get("name"))

    aqi_data = count_aqi_levels(aqi_list)

    print('line_data= ', line_data)
    print("pie_data= ", pie_data)
    print('pie_tip= ', pie_tip)
    print('aqi_list= ', aqi_list)
    print('aqi_data= ', aqi_data)

    info = {
        'line':line_data,
        'pie':pie_data,
        'pie_tip':pie_tip,
        'aqi':aqi_data,
    }

    return jsonify(info)

# 获取预警信息
@bp.route('/warning_detail/<warning_id>')
def warning_detail(warning_id):
    global warnings

    print('warning_id= ',warning_id)

    warning = find_dict_by_id(warnings,warning_id)



    if warning:
        return render_template('warning_detail.html', warning=warning)
    else:
        return "Warning not found", 404


def process_city_list(city_list):
    processed_city_data = {}

    for province in city_list:
        province_name = province['name']
        processed_city_data[province_name] = []

        for city in province['districts']:
            city_name = city['name']
            processed_city_data[province_name].append(city_name)

    return processed_city_data

# 获取城市列表
@bp.route('/get_cities', methods=['GET'])
def get_cities():
    processed_data = process_city_list(pro_citys)
    return jsonify(processed_data)


