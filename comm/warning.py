import requests
from comm.help import IsChinese

# 调用api，获取某市的天气预警
def get_warning_list(key):
    url = f'https://devapi.qweather.com/v7/warning/list?range=cn&key={key}'
    print("url= ", url)
    response = requests.get(url=url).json()
    warning_list = response.get('warningLocList')

    return warning_list

def get_warning(id,key):

    id = id.get("locationId")
    url = f'https://devapi.qweather.com/v7/warning/now?location={id}&lang=en&key={key}'
    print("url= ", url)
    response = requests.get(url=url).json()


    return response

# 获取预警列表
# title=True 返回标题列表
def warning_list(key,count):
    # 获取发布了预警信息的城市列表
    citys = get_warning_list(key)
    # print('cities: ',citys)

    # 返回数据
    data = []
    # 预警颜色
    color = None
    color_count = 0


    for city in citys:
        warning_data = get_warning(city, key)

        # 获取预警细节
        details = warning_data.get("warning")
        # print(detail)
        for detail in details:
            # 解析数据
            if(color_count <= 1):
                if(detail.get('severityColor').lower() == color):
                    print("color same")
                    continue

            color = detail.get('severityColor').lower()
            color_count += 1
            print("color=",color)

            if(IsChinese(detail.get('title'))):
                info={
                    'id':f"{detail.get('id')}",
                    'title':detail.get('title'),
                    'color':detail.get('severityColor').lower(),
                    'text':detail.get('text'),
                    'type':detail.get('type'),
                    'typeName':detail.get('typeName'),
                    'sender':detail.get('sender'),
                    'pubTime':detail.get('pubTime'),

                }
                data.append(info)

                # 获取固定数量的信息
                count -= 1
                if (count <= 0):
                    return data


if __name__ == '__main__':
    key = '9dad4415a9ac4444b079a55d9db6f44e'
    # print(get_warning_list(key))
    print(warning_list(key, 3))