from comm.get_weather import weather_history
from comm.py_city import pro_citys
import random
import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='wkz',
    password='123456',
    database='weather'
)

cursor = conn.cursor()

count = 0


def insert_data(city,month,data,year):
    # data = weather_history('北京',2023,month)
    global count

    id = count
    count += 1

    dy = next((item['value'] for item in data['info'] if item['name'] == '多云'), None)
    qing = next((item['value'] for item in data['info'] if item['name'] == '晴'), None)
    yu = next((item['value'] for item in data['info'] if item['name'] == '雨'), None)
    yin = next((item['value'] for item in data['info'] if item['name'] == '阴'), None)
    xue = next((item['value'] for item in data['info'] if item['name'] == '雪'), None)
    hc = next((item['value'] for item in data['info'] if item['name'] == '沙尘'), None)
    temp = data['avg_high_temp']
    aireaq = data['avg_air_quality_index']

    print(city)

    sql = """
        INSERT INTO weather_history (temp,aireaq,dy, qing,hc,yu,xue,yin,city,month,year,id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s)
    """

    cursor.execute(sql, (temp,aireaq,dy, qing,hc,yu,xue,yin,city,month,year,id))

    conn.commit()


    print("数据插入成功")


def generate_weather_data():
    # 定义天气类型
    weather_types = ['多云', '晴', '雨', '阴', '雪', '沙尘']

    # 随机生成info内的value值
    info = [{'name': weather, 'value': random.randint(0, 2000)} for weather in weather_types]

    # 随机生成avg_high_temp, avg_low_temp, avg_air_quality_index
    avg_high_temp = str(random.randint(-10, 40))  # 随机生成 -10 到 40 度之间的高温
    avg_low_temp = str(random.randint(-20, 30))  # 随机生成 -20 到 30 度之间的低温
    avg_air_quality_index = str(random.randint(0, 500))  # 随机生成 0 到 500 之间的空气质量指数

    # 生成的数据格式
    data = {
        'info': info,
        'avg_high_temp': avg_high_temp,
        'avg_low_temp': avg_low_temp,
        'avg_air_quality_index': avg_air_quality_index
    }

    return data

def generate_db():
    for province in pro_citys:
        for city in province['districts']:
            for _ in range(1,13):
                data=generate_weather_data()
                insert_data(city['name'],_,data,2023)




if __name__ == '__main__':
    generate_db()


    cursor.close()
    conn.close()
