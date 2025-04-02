import requests
from bs4 import BeautifulSoup
import json
from comm.help import IsChinese
from xpinyin import Pinyin
import random
p = Pinyin()
from comm.settings import weather_api_key as key
from comm.py_city import find_city_pinyin,find_city_adcode,find_locid_by_adcode
from models import Weather
import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='wkz',
    password='123456',
    database='weather'
)

cursor = conn.cursor(dictionary=True)



# 对location进行预处理
def preprocess_location(location):
    # 确保location为数组变量
    if(type(location) != list):
        print("type(location)= ", type(location), " != list")
        return None

    # 确保经纬度为两位小数
    location[0] = "{:.2f}".format(location[0])
    location[1] = "{:.2f}".format(location[1])

    return location

# 调用api，根据经纬度获取某个省的气候实况
def weather_province(location, key):
    # 预处理location
    location = preprocess_location(location)
    if location is None:
        return None

    url = f"https://devapi.qweather.com/v7/weather/now?location={location[0]},{location[1]}&key={key}"
    print("url= ", url)
    response = requests.get(url=url)
    return response.json()


# 对天气网进行爬虫，获取html数据
def tianqi_spider(city,year,month):
    # 月份为两位数字 03
    if (month < 10):
        month = f"0{month}"

    date = f"{year}{month}"
    print("date= ", date)

    # 多音字处理不好
    # if (IsChinese(city)):
    #     city = p.get_pinyin(city, '')
    #     print("city= ", city)
    # else:
    #     return None

    city = find_city_pinyin(city_name=city)
    print("city= ", city)

    url = f'http://lishi.tianqi.com/{city}/{date}.html'
    print("url= ", url)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
    }

    response = requests.get(url=url, headers=headers,
                            verify=False)

    return response.text

# 获得天气描述以及对应天数
def get_text(soup):
    # 获取head标签
    head = soup.head

    # 获取head中最后一个script标签的内容
    last_script = head.find_all('script')[-1].string

    # 提取vdata部分
    start_index = last_script.find('var vdata= ') + len('var vdata= ')
    end_index = last_script.find(';', start_index)
    vdata_str = last_script[start_index:end_index].strip()

    # 将vdata字符串转换为Python对象
    vdata = json.loads(vdata_str)
    # print(vdata)

    info = []
    for data in vdata:
        info.append({
            'name':data.get("name"),
            'value':data.get("value")
        })

    return info

# 提取“平均高温”和“平均低温”
def get_temp(soup):

    tian_twoa_divs = soup.find_all('div', class_='tian_twoa')
    tian_twob_divs = soup.find_all('div', class_='tian_twob')

    # 通过内容匹配，找到对应的高温和低温值
    avg_high_temp = None
    avg_low_temp = None

    for temp_div, label_div in zip(tian_twoa_divs, tian_twob_divs):
        if label_div.text == "平均高温":
            avg_high_temp = temp_div.text.strip('℃')
        elif label_div.text == "平均低温":
            avg_low_temp = temp_div.text.strip('℃')

    # 输出提取的值
    # print("平均高温:", avg_high_temp)
    # print("平均低温:", avg_low_temp)

    return avg_high_temp,avg_low_temp


# 提取“平均空气质量指数”
def get_airqua(soup):

    air_quality_divs = soup.find_all('div', class_='tian_twoa')
    air_quality_labels = soup.find_all('div', class_='tian_twob')

    avg_air_quality_index = None

    for value_div, label_div in zip(air_quality_divs, air_quality_labels):
        if label_div.text == "平均空气质量指数":
            avg_air_quality_index = value_div.text.strip()

    # 输出提取的值
    # print("平均空气质量指数:", avg_air_quality_index)

    return avg_air_quality_index


# 根据城市的名字,来获取该城市的历史天气信息
def weather_history_api(city,year,month,disc=True,temp=True,airqua=True):
    html = tianqi_spider(city,year,month)

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')


    #获取天气描述及其天数
    info = get_text(soup)
    # print("info= ",info)


    #获取该月平均最高气温和最低气温
    avg_high_temp,avg_low_temp = get_temp(soup)
    # print("avg_high_temp= ", avg_high_temp)
    # print("avg_low_temp= :", avg_low_temp)


    #平均空气质量指数
    avg_air_quality_index = get_airqua(soup)
    # print("avg_air_quality_index= ", avg_air_quality_index)

    return {
        'info':info,
        'avg_high_temp':avg_high_temp,
        'avg_low_temp':avg_low_temp,
        'avg_air_quality_index':avg_air_quality_index,
    }


# 查询操作的封装
def query_record(city, month, year):
    result = Weather.query.filter_by(city=city, month=month, year=year).first()

    if result:
        print("SQLAlchemy query succeed!")
        # 将查询结果转为字典形式返回
        return {
            'temp': str(result.temp),
            'aireaq': str(result.aireaq),
            'dy': str(result.dy),
            'qing': str(result.qing),
            'hc': str(result.hc),
            'yu': str(result.yu),
            'xue': str(result.xue),
            'yin': str(result.yin),
            'city': result.city,
            'month': str(result.month)
        }
    else:
        return None
#
# def query_record(city, month,year):
#     sql = """
#         SELECT temp, aireaq, dy, qing, hc, yu, xue, yin, city, month
#         FROM weather_history
#         WHERE city = %s AND month = %s AND year = %s
#     """
#
#     cursor.execute(sql, (city, month,year))
#     result = cursor.fetchone()  # 获取单条记录
#     print("query record result =",result)
#     if result:
#         print("mysql succeed!")
#         return result
#     else:
#         return None

# 从数据库获取数据
def weather_history(city,year,month):
    data = query_record(city=city,month=month,year=year)
    print("weather history data= ",data)

    info = {
        'info': [
            {'name': '多云', 'value': int(data['dy'])},
            {'name': '晴', 'value': int(data['qing'])},
            {'name': '雨', 'value': int(data['yu'])},
            {'name': '阴', 'value': int(data['yin'])},
            {'name': '雪', 'value': int(data['xue'])},
            {'name': '沙尘', 'value': int(data['hc'])}],
        'avg_high_temp': data['temp'],
        'avg_low_temp': data['temp'],
        'avg_air_quality_index': data['aireaq']
    }

    return info


# 空气质量：将每个月的数值 转化成文本描述并记录数量
def count_aqi_levels(aqi_list):
    aqi_list = [int(x) for x in aqi_list]

    # 定义各个级别的AQI范围
    levels = {
        '优': 0,
        '良': 0,
        '轻度污染': 0,
        '中度污染': 0,
        '重度污染': 0,
        '严重污染': 0
    }

    # 根据AQI值统计各个级别的数量
    for aqi in aqi_list:
        if 0 <= aqi <= 50:
            levels['优'] += 1
        elif 51 <= aqi <= 100:
            levels['良'] += 1
        elif 101 <= aqi <= 150:
            levels['轻度污染'] += 1
        elif 151 <= aqi <= 200:
            levels['中度污染'] += 1
        elif 201 <= aqi <= 300:
            levels['重度污染'] += 1
        elif aqi > 300:
            levels['严重污染'] += 1

    # 返回各个级别的数量数组
    return list(levels.values())

# 通过api获取 7天 天气预报数据
def get_forecast_data(locid,key,days):
    print("days=",days)

    url=f'https://devapi.qweather.com/v7/weather/{days}d?location={locid}&key={key}'
    print('url= ',url)

    response = requests.get(url=url).json()

    data = response.get('daily')

    return data

# 获取七天天气预报
def get_forecast(city,days):
    print('in get_forecast():')

    # 调用和风天气api进行天气预报展示

    adcode = find_city_adcode(city)
    print('adcode= ',adcode)
    locid = find_locid_by_adcode(adcode)
    print('locid= ',locid)


    # 获取七天天气预报的接口
    data = get_forecast_data(locid,key,days)
    # print('data= ',datas)

    return data

if __name__ == '__main__':
    # line_data = []
    # pie_data = []
    # pie_tip=[]
    # pie_flag = False # 代表pie data里没有数据
    # aqi_list=[] #aqi 数值
    # aqi_data=[] #aqi统计数据
    #
    #
    #
    # for month in range(1, 13):
    #     data = weather_history("淄博", 2023, month)
    #
    #     print(data)
    #
    #     line_data.append(data.get('avg_high_temp'))
    #     aqi_list.append(data.get('avg_air_quality_index'))
    #
    #     if (not pie_flag):
    #         pie_flag = True
    #         for _ in data.get("info"):
    #             pie_data.append(_.get("value"))
    #             pie_tip.append(_.get("name"))
    #
    # aqi_data=count_aqi_levels(aqi_list)
    #
    # print('line_data= ',line_data)
    # print("pie_data= ",pie_data)
    # print('pie_tip= ',pie_tip)
    # print('aqi_list= ',aqi_list)
    # print('aqi_data= ',aqi_data)

    # print(get_forecast('通辽'))

    print(weather_history('济源',2023,12))