import csv
import os
from flask import current_app


# 列表来自网络
py_city_list = []

def process_city_list(city_list):
    # 用于存储处理后的省份列表
    processed_city_list = []

    for province in city_list:
        # 获取省份中的城市列表
        districts = province.get('districts', [])

        # 用于存储处理后的城市列表
        processed_districts = []

        for city in districts:
            # 获取城市名和拼音
            city_name = city.get('name', '')
            city_py = city.get('py', '')

            # 如果城市名以“市”结尾，进行处理
            if city_name.endswith('市'):
                # 删除城市名中的“市”
                city_name = city_name[:-1]

                # 删除拼音中的“shi”
                city_py = city_py.replace('shi', '')

                # 更新城市名和拼音
                city['name'] = city_name
                city['py'] = city_py

                # 将处理后的城市加入列表
                processed_districts.append(city)

        # 如果处理后的城市列表不为空，更新省份的城市列表
        if processed_districts:
            province['districts'] = processed_districts
            processed_city_list.append(province)

    return processed_city_list



# 处理好的符合格式的 citys数据 adcode 拼音 和 名字，用于首页的下拉列表框
# 拼音用于爬虫程序
pro_citys=[{'adcode': '410000', 'name': '河南省', 'py': 'henansheng', 'districts': [{'adcode': '410300', 'name': '洛阳', 'py': 'luoyang'}, {'adcode': '411200', 'name': '三门峡', 'py': 'sanmenxia'}, {'adcode': '411100', 'name': '漯河', 'py': 'luohe'}, {'adcode': '411000', 'name': '许昌', 'py': 'xuchang'}, {'adcode': '411300', 'name': '南阳', 'py': 'nanyang'}, {'adcode': '411500', 'name': '信阳', 'py': 'xinyang'}, {'adcode': '419001', 'name': '济源', 'py': 'jiyuan'}, {'adcode': '410900', 'name': '濮阳', 'py': 'puyang'}, {'adcode': '411700', 'name': '驻马店', 'py': 'zhumadian'}, {'adcode': '410600', 'name': '鹤壁', 'py': 'hebi'}, {'adcode': '410100', 'name': '郑州', 'py': 'zhengzhou'}, {'adcode': '410800', 'name': '焦作', 'py': 'jiaozuo'}, {'adcode': '410200', 'name': '开封', 'py': 'kaifeng'}, {'adcode': '410500', 'name': '安阳', 'py': 'anyang'}, {'adcode': '410700', 'name': '新乡', 'py': 'xinxiang'}, {'adcode': '411400', 'name': '商丘', 'py': 'shangqiu'}, {'adcode': '410400', 'name': '平顶山', 'py': 'pingdingshan'}, {'adcode': '411600', 'name': '周口', 'py': 'zhoukou'}]}, {'adcode': '440000', 'name': '广东省', 'py': 'guangdongsheng', 'districts': [{'adcode': '440500', 'name': '汕头', 'py': 'shantou'}, {'adcode': '440600', 'name': '佛山', 'py': 'foshan'}, {'adcode': '441200', 'name': '肇庆', 'py': 'zhaoqing'}, {'adcode': '441300', 'name': '惠州', 'py': 'huizhou'}, {'adcode': '440300', 'name': '深圳', 'py': 'shenzhen'}, {'adcode': '440400', 'name': '珠海', 'py': 'zhuhai'}, {'adcode': '440800', 'name': '湛江', 'py': 'zhanjiang'}, {'adcode': '440700', 'name': '江门', 'py': 'jiangmen'}, {'adcode': '441700', 'name': '阳江', 'py': 'yangjiang'}, {'adcode': '440900', 'name': '茂名', 'py': 'maoming'}, {'adcode': '440200', 'name': '韶关', 'py': 'shaoguan'}, {'adcode': '441500', 'name': '汕尾', 'py': 'shanwei'}, {'adcode': '445200', 'name': '揭阳', 'py': 'jieyang'}, {'adcode': '445300', 'name': '云浮', 'py': 'yunfu'}, {'adcode': '441600', 'name': '河源', 'py': 'heyuan'}, {'adcode': '445100', 'name': '潮州', 'py': 'chaozhou'}, {'adcode': '441800', 'name': '清远', 'py': 'qingyuan'}, {'adcode': '441900', 'name': '东莞', 'py': 'dongguan'}, {'adcode': '440100', 'name': '广州', 'py': 'guangzhou'}, {'adcode': '441400', 'name': '梅州', 'py': 'meizhou'}, {'adcode': '442000', 'name': '中山', 'py': 'zhongshan'}]}, {'adcode': '150000', 'name': '内蒙古自治区', 'py': 'neimengguzizhiqu', 'districts': [{'adcode': '150300', 'name': '乌海', 'py': 'wuhai'}, {'adcode': '150200', 'name': '包头', 'py': 'baotou'}, {'adcode': '150800', 'name': '巴彦淖尔', 'py': 'bayannaoer'}, {'adcode': '150700', 'name': '呼伦贝尔', 'py': 'hulunbeier'}, {'adcode': '150500', 'name': '通辽', 'py': 'tongliao'}, {'adcode': '150100', 'name': '呼和浩特', 'py': 'huhehaote'}, {'adcode': '150900', 'name': '乌兰察布', 'py': 'wulanchabu'}, {'adcode': '150600', 'name': '鄂尔多斯', 'py': 'eerduosi'}, {'adcode': '150400', 'name': '赤峰', 'py': 'chifeng'}]}, {'adcode': '230000', 'name': '黑龙江省', 'py': 'heilongjiangsheng', 'districts': [{'adcode': '230900', 'name': '七台河', 'py': 'qitaihe'}, {'adcode': '230400', 'name': '鹤岗', 'py': 'hegang'}, {'adcode': '230700', 'name': '伊春', 'py': 'yichun'}, {'adcode': '231200', 'name': '绥化', 'py': 'suihua'}, {'adcode': '230100', 'name': '哈尔滨', 'py': 'haerbin'}, {'adcode': '230600', 'name': '大庆', 'py': 'daqing'}, {'adcode': '230800', 'name': '佳木斯', 'py': 'jiamusi'}, {'adcode': '230500', 'name': '双鸭山', 'py': 'shuangyashan'}, {'adcode': '231100', 'name': '黑河', 'py': 'heihe'}, {'adcode': '231000', 'name': '牡丹江', 'py': 'mudanjiang'}, {'adcode': '230200', 'name': '齐齐哈尔', 'py': 'qiqihaer'}, {'adcode': '230300', 'name': '鸡西', 'py': 'jixi'}]}, {'adcode': '650000', 'name': '新疆维吾尔自治区', 'py': 'xinjiangweiwuerzizhiqu', 'districts': [{'adcode': '659005', 'name': '北屯', 'py': 'beitun'}, {'adcode': '659006', 'name': '铁门关', 'py': 'tiemenguan'}, {'adcode': '659007', 'name': '双河', 'py': 'shuanghe'}, {'adcode': '659009', 'name': '昆玉', 'py': 'kunyu'}, {'adcode': '659001', 'name': '石河子', 'py': 'hezi'}, {'adcode': '659008', 'name': '可克达拉', 'py': 'kekedala'}, {'adcode': '659004', 'name': '五家渠', 'py': 'wujiaqu'}, {'adcode': '659002', 'name': '阿拉尔', 'py': 'alaer'}, {'adcode': '659003', 'name': '图木舒克', 'py': 'tumushuke'}, {'adcode': '650500', 'name': '哈密', 'py': 'hami'}, {'adcode': '650200', 'name': '克拉玛依', 'py': 'kelamayi'}, {'adcode': '659010', 'name': '胡杨河', 'py': 'huyanghe'}, {'adcode': '650400', 'name': '吐鲁番', 'py': 'tulufan'}, {'adcode': '650100', 'name': '乌鲁木齐', 'py': 'wulumuqi'}]}, {'adcode': '420000', 'name': '湖北省', 'py': 'hubeisheng', 'districts': [{'adcode': '420300', 'name': '十堰', 'py': 'yan'}, {'adcode': '420600', 'name': '襄阳', 'py': 'xiangyang'}, {'adcode': '429006', 'name': '天门', 'py': 'tianmen'}, {'adcode': '420100', 'name': '武汉', 'py': 'wuhan'}, {'adcode': '429005', 'name': '潜江', 'py': 'qianjiang'}, {'adcode': '421100', 'name': '黄冈', 'py': 'huanggang'}, {'adcode': '420500', 'name': '宜昌', 'py': 'yichang'}, {'adcode': '429004', 'name': '仙桃', 'py': 'xiantao'}, {'adcode': '420800', 'name': '荆门', 'py': 'jingmen'}, {'adcode': '420900', 'name': '孝感', 'py': 'xiaogan'}, {'adcode': '421000', 'name': '荆州', 'py': 'jingzhou'}, {'adcode': '421200', 'name': '咸宁', 'py': 'xianning'}, {'adcode': '421300', 'name': '随州', 'py': 'suizhou'}, {'adcode': '420200', 'name': '黄石', 'py': 'huang'}, {'adcode': '420700', 'name': '鄂州', 'py': 'ezhou'}]}, {'adcode': '210000', 'name': '辽宁省', 'py': 'liaoningsheng', 'districts': [{'adcode': '210100', 'name': '沈阳', 'py': 'shenyang'}, {'adcode': '211400', 'name': '葫芦岛', 'py': 'huludao'}, {'adcode': '210700', 'name': '锦州', 'py': 'jinzhou'}, {'adcode': '210200', 'name': '大连', 'py': 'dalian'}, {'adcode': '210600', 'name': '丹东', 'py': 'dandong'}, {'adcode': '210400', 'name': '抚顺', 'py': 'fushun'}, {'adcode': '211100', 'name': '盘锦', 'py': 'panjin'}, {'adcode': '210900', 'name': '阜新', 'py': 'fuxin'}, {'adcode': '211200', 'name': '铁岭', 'py': 'tieling'}, {'adcode': '210800', 'name': '营口', 'py': 'yingkou'}, {'adcode': '210500', 'name': '本溪', 'py': 'benxi'}, {'adcode': '211000', 'name': '辽阳', 'py': 'liaoyang'}, {'adcode': '210300', 'name': '鞍山', 'py': 'anshan'}, {'adcode': '211300', 'name': '朝阳', 'py': 'chaoyang'}]}, {'adcode': '370000', 'name': '山东省', 'py': 'shandongsheng', 'districts': [{'adcode': '370600', 'name': '烟台', 'py': 'yantai'}, {'adcode': '371000', 'name': '威海', 'py': 'weihai'}, {'adcode': '370200', 'name': '青岛', 'py': 'qingdao'}, {'adcode': '370300', 'name': '淄博', 'py': 'zibo'}, {'adcode': '371500', 'name': '聊城', 'py': 'liaocheng'}, {'adcode': '370500', 'name': '东营', 'py': 'dongying'}, {'adcode': '371600', 'name': '滨州', 'py': 'binzhou'}, {'adcode': '370400', 'name': '枣庄', 'py': 'zaozhuang'}, {'adcode': '370700', 'name': '潍坊', 'py': 'weifang'}, {'adcode': '371100', 'name': '日照', 'py': 'rizhao'}, {'adcode': '371400', 'name': '德州', 'py': 'dezhou'}, {'adcode': '370100', 'name': '济南', 'py': 'jinan'}, {'adcode': '371300', 'name': '临沂', 'py': 'linyi'}, {'adcode': '370800', 'name': '济宁', 'py': 'jining'}, {'adcode': '371700', 'name': '菏泽', 'py': 'heze'}, {'adcode': '370900', 'name': '泰安', 'py': 'taian'}]}, {'adcode': '610000', 'name': '陕西省', 'py': 'shanxisheng', 'districts': [{'adcode': '611000', 'name': '商洛', 'py': 'shangluo'}, {'adcode': '610700', 'name': '汉中', 'py': 'hanzhong'}, {'adcode': '610200', 'name': '铜川', 'py': 'tongchuan'}, {'adcode': '610800', 'name': '榆林', 'py': 'yulin'}, {'adcode': '610600', 'name': '延安', 'py': 'yanan'}, {'adcode': '610100', 'name': '西安', 'py': 'xian'}, {'adcode': '610300', 'name': '宝鸡', 'py': 'baoji'}, {'adcode': '610900', 'name': '安康', 'py': 'ankang'}, {'adcode': '610500', 'name': '渭南', 'py': 'weinan'}, {'adcode': '610400', 'name': '咸阳', 'py': 'xianyang'}]}, {'adcode': '520000', 'name': '贵州省', 'py': 'guizhousheng', 'districts': [{'adcode': '520400', 'name': '安顺', 'py': 'anshun'}, {'adcode': '520300', 'name': '遵义', 'py': 'zunyi'}, {'adcode': '520200', 'name': '六盘水', 'py': 'liupanshui'}, {'adcode': '520600', 'name': '铜仁', 'py': 'tongren'}, {'adcode': '520500', 'name': '毕节', 'py': 'bijie'}, {'adcode': '520100', 'name': '贵阳', 'py': 'guiyang'}]}, {'adcode': '540000', 'name': '西藏自治区', 'py': 'xicangzizhiqu', 'districts': [{'adcode': '540200', 'name': '日喀则', 'py': 'rikaze'}, {'adcode': '540600', 'name': '那曲', 'py': 'naqu'}, {'adcode': '540300', 'name': '昌都', 'py': 'changdu'}, {'adcode': '540500', 'name': '山南', 'py': 'shannan'}, {'adcode': '540100', 'name': '拉萨', 'py': 'lasa'}, {'adcode': '540400', 'name': '林芝', 'py': 'linzhi'}]}, {'adcode': '340000', 'name': '安徽省', 'py': 'anhuisheng', 'districts': [{'adcode': '341700', 'name': '池州', 'py': 'chizhou'}, {'adcode': '340500', 'name': '马鞍山', 'py': 'maanshan'}, {'adcode': '341200', 'name': '阜阳', 'py': 'fuyang'}, {'adcode': '340600', 'name': '淮北', 'py': 'huaibei'}, {'adcode': '340700', 'name': '铜陵', 'py': 'tongling'}, {'adcode': '341000', 'name': '黄山', 'py': 'huangshan'}, {'adcode': '340800', 'name': '安庆', 'py': 'anqing'}, {'adcode': '341100', 'name': '滁州', 'py': 'chuzhou'}, {'adcode': '340400', 'name': '淮南', 'py': 'huainan'}, {'adcode': '341500', 'name': '六安', 'py': 'luan'}, {'adcode': '340300', 'name': '蚌埠', 'py': 'bengbu'}, {'adcode': '341300', 'name': '宿州', 'py': 'suzhou'}, {'adcode': '341600', 'name': '亳州', 'py': 'bozhou'}, {'adcode': '340200', 'name': '芜湖', 'py': 'wuhu'}, {'adcode': '340100', 'name': '合肥', 'py': 'hefei'}, {'adcode': '341800', 'name': '宣城', 'py': 'xuancheng'}]}, {'adcode': '350000', 'name': '福建省', 'py': 'fujiansheng', 'districts': [{'adcode': '350300', 'name': '莆田', 'py': 'putian'}, {'adcode': '350900', 'name': '宁德', 'py': 'ningde'}, {'adcode': '350100', 'name': '福州', 'py': 'fuzhou'}, {'adcode': '350500', 'name': '泉州', 'py': 'quanzhou'}, {'adcode': '350200', 'name': '厦门', 'py': 'xiamen'}, {'adcode': '350600', 'name': '漳州', 'py': 'zhangzhou'}, {'adcode': '350700', 'name': '南平', 'py': 'nanping'}, {'adcode': '350400', 'name': '三明', 'py': 'sanming'}, {'adcode': '350800', 'name': '龙岩', 'py': 'longyan'}]}, {'adcode': '430000', 'name': '湖南省', 'py': 'hunansheng', 'districts': [{'adcode': '430600', 'name': '岳阳', 'py': 'yueyang'}, {'adcode': '430800', 'name': '张家界', 'py': 'zhangjiajie'}, {'adcode': '430400', 'name': '衡阳', 'py': 'hengyang'}, {'adcode': '431200', 'name': '怀化', 'py': 'huaihua'}, {'adcode': '430100', 'name': '长沙', 'py': 'changsha'}, {'adcode': '430700', 'name': '常德', 'py': 'changde'}, {'adcode': '430300', 'name': '湘潭', 'py': 'xiangtan'}, {'adcode': '430200', 'name': '株洲', 'py': 'zhuzhou'}, {'adcode': '431000', 'name': '郴州', 'py': 'chenzhou'}, {'adcode': '430500', 'name': '邵阳', 'py': 'shaoyang'}, {'adcode': '431100', 'name': '永州', 'py': 'yongzhou'}, {'adcode': '430900', 'name': '益阳', 'py': 'yiyang'}, {'adcode': '431300', 'name': '娄底', 'py': 'loudi'}]}, {'adcode': '460000', 'name': '海南省', 'py': 'hainansheng', 'districts': [{'adcode': '469002', 'name': '琼海', 'py': 'qionghai'}, {'adcode': '469007', 'name': '东方', 'py': 'dongfang'}, {'adcode': '460300', 'name': '三沙', 'py': 'sansha'}, {'adcode': '469006', 'name': '万宁', 'py': 'wanning'}, {'adcode': '460200', 'name': '三亚', 'py': 'sanya'}, {'adcode': '460400', 'name': '儋州', 'py': 'danzhou'}, {'adcode': '469005', 'name': '文昌', 'py': 'wenchang'}, {'adcode': '460100', 'name': '海口', 'py': 'haikou'}, {'adcode': '469001', 'name': '五指山', 'py': 'wuzhishan'}]}, {'adcode': '320000', 'name': '江苏省', 'py': 'jiangsusheng', 'districts': [{'adcode': '320600', 'name': '南通', 'py': 'nantong'}, {'adcode': '320700', 'name': '连云港', 'py': 'lianyungang'}, {'adcode': '321300', 'name': '宿迁', 'py': 'suqian'}, {'adcode': '321200', 'name': '泰州', 'py': 'taizhou'}, {'adcode': '320400', 'name': '常州', 'py': 'changzhou'}, {'adcode': '320100', 'name': '南京', 'py': 'nanjing'}, {'adcode': '320300', 'name': '徐州', 'py': 'xuzhou'}, {'adcode': '320500', 'name': '苏州', 'py': 'suzhou'}, {'adcode': '321000', 'name': '扬州', 'py': 'yangzhou'}, {'adcode': '321100', 'name': '镇江', 'py': 'zhenjiang'}, {'adcode': '320200', 'name': '无锡', 'py': 'wuxi'}, {'adcode': '320900', 'name': '盐城', 'py': 'yancheng'}, {'adcode': '320800', 'name': '淮安', 'py': 'huaian'}]}, {'adcode': '630000', 'name': '青海省', 'py': 'qinghaisheng', 'districts': [{'adcode': '630200', 'name': '海东', 'py': 'haidong'}, {'adcode': '630100', 'name': '西宁', 'py': 'xining'}]}, {'adcode': '450000', 'name': '广西壮族自治区', 'py': 'guangxizhuangzuzizhiqu', 'districts': [{'adcode': '451000', 'name': '百色', 'py': 'baise'}, {'adcode': '450700', 'name': '钦州', 'py': 'qinzhou'}, {'adcode': '450500', 'name': '北海', 'py': 'beihai'}, {'adcode': '450200', 'name': '柳州', 'py': 'liuzhou'}, {'adcode': '450400', 'name': '梧州', 'py': 'wuzhou'}, {'adcode': '450300', 'name': '桂林', 'py': 'guilin'}, {'adcode': '451100', 'name': '贺州', 'py': 'hezhou'}, {'adcode': '451300', 'name': '来宾', 'py': 'laibin'}, {'adcode': '451200', 'name': '河池', 'py': 'hechi'}, {'adcode': '450900', 'name': '玉林', 'py': 'yulin'}, {'adcode': '450100', 'name': '南宁', 'py': 'nanning'}, {'adcode': '450800', 'name': '贵港', 'py': 'guigang'}, {'adcode': '451400', 'name': '崇左', 'py': 'chongzuo'}, {'adcode': '450600', 'name': '防城港', 'py': 'fangchenggang'}]}, {'adcode': '640000', 'name': '宁夏回族自治区', 'py': 'ningxiahuizuzizhiqu', 'districts': [{'adcode': '640200', 'name': '石嘴山', 'py': 'zuishan'}, {'adcode': '640400', 'name': '固原', 'py': 'guyuan'}, {'adcode': '640500', 'name': '中卫', 'py': 'zhongwei'}, {'adcode': '640300', 'name': '吴忠', 'py': 'wuzhong'}, {'adcode': '640100', 'name': '银川', 'py': 'yinchuan'}]}, {'adcode': '330000', 'name': '浙江省', 'py': 'zhejiangsheng', 'districts': [{'adcode': '330400', 'name': '嘉兴', 'py': 'jiaxing'}, {'adcode': '330900', 'name': '舟山', 'py': 'zhoushan'}, {'adcode': '330200', 'name': '宁波', 'py': 'ningbo'}, {'adcode': '331000', 'name': '台州', 'py': 'taizhou'}, {'adcode': '330300', 'name': '温州', 'py': 'wenzhou'}, {'adcode': '331100', 'name': '丽水', 'py': 'lishui'}, {'adcode': '330700', 'name': '金华', 'py': 'jinhua'}, {'adcode': '330500', 'name': '湖州', 'py': 'huzhou'}, {'adcode': '330600', 'name': '绍兴', 'py': 'shaoxing'}, {'adcode': '330800', 'name': '衢州', 'py': 'quzhou'}, {'adcode': '330100', 'name': '杭州', 'py': 'hangzhou'}]}, {'adcode': '130000', 'name': '河北省', 'py': 'hebeisheng', 'districts': [{'adcode': '130200', 'name': '唐山', 'py': 'tangshan'}, {'adcode': '131000', 'name': '廊坊', 'py': 'langfang'}, {'adcode': '130300', 'name': '秦皇岛', 'py': 'qinhuangdao'}, {'adcode': '130400', 'name': '邯郸', 'py': 'handan'}, {'adcode': '130800', 'name': '承德', 'py': 'chengde'}, {'adcode': '130900', 'name': '沧州', 'py': 'cangzhou'}, {'adcode': '130500', 'name': '邢台', 'py': 'xingtai'}, {'adcode': '131100', 'name': '衡水', 'py': 'hengshui'}, {'adcode': '130700', 'name': '张家口', 'py': 'zhangjiakou'}, {'adcode': '130600', 'name': '保定', 'py': 'baoding'}, {'adcode': '130100', 'name': '石家庄', 'py': 'jiazhuang'}]}, {'adcode': '620000', 'name': '甘肃省', 'py': 'gansusheng', 'districts': [{'adcode': '620300', 'name': '金昌', 'py': 'jinchang'}, {'adcode': '620100', 'name': '兰州', 'py': 'lanzhou'}, {'adcode': '620900', 'name': '酒泉', 'py': 'jiuquan'}, {'adcode': '620400', 'name': '白银', 'py': 'baiyin'}, {'adcode': '620200', 'name': '嘉峪关', 'py': 'jiayuguan'}, {'adcode': '620800', 'name': '平凉', 'py': 'pingliang'}, {'adcode': '621200', 'name': '陇南', 'py': 'longnan'}, {'adcode': '620700', 'name': '张掖', 'py': 'zhangye'}, {'adcode': '621100', 'name': '定西', 'py': 'dingxi'}, {'adcode': '620500', 'name': '天水', 'py': 'tianshui'}, {'adcode': '621000', 'name': '庆阳', 'py': 'qingyang'}, {'adcode': '620600', 'name': '武威', 'py': 'wuwei'}]}, {'adcode': '510000', 'name': '四川省', 'py': 'sichuansheng', 'districts': [{'adcode': '510700', 'name': '绵阳', 'py': 'mianyang'}, {'adcode': '510800', 'name': '广元', 'py': 'guangyuan'}, {'adcode': '510100', 'name': '成都', 'py': 'chengdu'}, {'adcode': '511900', 'name': '巴中', 'py': 'bazhong'}, {'adcode': '511300', 'name': '南充', 'py': 'nanchong'}, {'adcode': '511700', 'name': '达州', 'py': 'dazhou'}, {'adcode': '510900', 'name': '遂宁', 'py': 'suining'}, {'adcode': '510600', 'name': '德阳', 'py': 'deyang'}, {'adcode': '511600', 'name': '广安', 'py': 'guangan'}, {'adcode': '512000', 'name': '资阳', 'py': 'ziyang'}, {'adcode': '511000', 'name': '内江', 'py': 'neijiang'}, {'adcode': '510400', 'name': '攀枝花', 'py': 'panzhihua'}, {'adcode': '511100', 'name': '乐山', 'py': 'leshan'}, {'adcode': '510500', 'name': '泸州', 'py': 'luzhou'}, {'adcode': '511400', 'name': '眉山', 'py': 'meishan'}, {'adcode': '510300', 'name': '自贡', 'py': 'zigong'}, {'adcode': '511500', 'name': '宜宾', 'py': 'yibin'}, {'adcode': '511800', 'name': '雅安', 'py': 'yaan'}]}, {'adcode': '360000', 'name': '江西省', 'py': 'jiangxisheng', 'districts': [{'adcode': '360700', 'name': '赣州', 'py': 'ganzhou'}, {'adcode': '360300', 'name': '萍乡', 'py': 'pingxiang'}, {'adcode': '360200', 'name': '景德镇', 'py': 'jingdezhen'}, {'adcode': '360900', 'name': '宜春', 'py': 'yichun'}, {'adcode': '360800', 'name': '吉安', 'py': 'jian'}, {'adcode': '360500', 'name': '新余', 'py': 'xinyu'}, {'adcode': '361100', 'name': '上饶', 'py': 'shangrao'}, {'adcode': '360100', 'name': '南昌', 'py': 'nanchang'}, {'adcode': '360400', 'name': '九江', 'py': 'jiujiang'}, {'adcode': '360600', 'name': '鹰潭', 'py': 'yingtan'}, {'adcode': '361000', 'name': '抚州', 'py': 'fuzhou'}]}, {'adcode': '220000', 'name': '吉林省', 'py': 'jilinsheng', 'districts': [{'adcode': '220200', 'name': '吉林', 'py': 'jilin'}, {'adcode': '220800', 'name': '白城', 'py': 'baicheng'}, {'adcode': '220700', 'name': '松原', 'py': 'songyuan'}, {'adcode': '220400', 'name': '辽源', 'py': 'liaoyuan'}, {'adcode': '220100', 'name': '长春', 'py': 'changchun'}, {'adcode': '220500', 'name': '通化', 'py': 'tonghua'}, {'adcode': '220300', 'name': '四平', 'py': 'siping'}, {'adcode': '220600', 'name': '白山', 'py': 'baishan'}]}, {'adcode': '140000', 'name': '山西省', 'py': 'shanxisheng', 'districts': [{'adcode': '140300', 'name': '阳泉', 'py': 'yangquan'}, {'adcode': '140100', 'name': '太原', 'py': 'taiyuan'}, {'adcode': '141100', 'name': '吕梁', 'py': 'lvliang'}, {'adcode': '140700', 'name': '晋中', 'py': 'jinzhong'}, {'adcode': '140400', 'name': '长治', 'py': 'changzhi'}, {'adcode': '140500', 'name': '晋城', 'py': 'jincheng'}, {'adcode': '140800', 'name': '运城', 'py': 'yuncheng'}, {'adcode': '141000', 'name': '临汾', 'py': 'linfen'}, {'adcode': '140900', 'name': '忻州', 'py': 'xinzhou'}, {'adcode': '140600', 'name': '朔州', 'py': 'shuozhou'}, {'adcode': '140200', 'name': '大同', 'py': 'datong'}]}, {'adcode': '530000', 'name': '云南省', 'py': 'yunnansheng', 'districts': [{'adcode': '530700', 'name': '丽江', 'py': 'lijiang'}, {'adcode': '530600', 'name': '昭通', 'py': 'zhaotong'}, {'adcode': '530400', 'name': '玉溪', 'py': 'yuxi'}, {'adcode': '530300', 'name': '曲靖', 'py': 'qujing'}, {'adcode': '530500', 'name': '保山', 'py': 'baoshan'}, {'adcode': '530800', 'name': '普洱', 'py': 'puer'}, {'adcode': '530900', 'name': '临沧', 'py': 'lincang'}, {'adcode': '530100', 'name': '昆明', 'py': 'kunming'}]},{"adcode":"110000","name":"北京市","py":"beijingshi","districts":[{"adcode":"110100","name":"北京","py":"beijing"}]},{"adcode":"310000","name":"上海市","py":"shanghaishi","districts":[{"adcode":"310100","name":"上海","py":"shanghai"}]},{"adcode":"500000","name":"重庆市","py":"chongqingshi","districts":[{"adcode":"500100","name":"重庆","py":"chongqing"}]},{"adcode":"120000","name":"天津市","py":"tianjinshi","districts":[{"adcode":"120100","name":"天津","py":"tianjin"}]}]

def get_citys(city_list):
    data = {}
    for province in city_list:
        sub_list = []

        for city in province['districts']:
            sub_list.append(city['name'])

        data[f'{province["name"]}']=sub_list

    return data



def find_city_pinyin(city_name):
    for province in pro_citys:
        for city in province['districts']:
            if city['name'] == city_name:
                return city['py']
    return None  # 如果未找到对应的城市，返回 None


def find_province_name(adcode):
    for province in pro_citys:
        if province['adcode'] == adcode:
            return province['name']
    return None  # 如果未找到对应的城市，返回 None


def find_first_city(adcode):
    for province in pro_citys:
        if province['adcode'] == adcode:
            return province['districts'][0].get('name')
    return None  # 如果未找到对应的城市，返回 None


def find_city_adcode(city_name):
    for province in pro_citys:
        for city in province['districts']:
            if city['name'] == city_name:
                return city['adcode']
    return None



def find_locid_by_adcode(adcode):
    from weather_show.app import app

    with app.app_context():
        # 获取项目根目录
        root_dir = current_app.root_path
        # 构建相对于根目录的文件路径
        csv_path = os.path.join(root_dir, 'static/src/city_list.csv')

        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ad_codes = row['AD_code'].split(',')
                if str(adcode) in ad_codes:
                    return row['Location_ID']
    return None




if __name__ == '__main__':
    # print(find_locid_by_adcode('610202'))
    # print(find_first_city('360000'))

    print(get_citys(pro_citys))