
# 判断是否是纯中文
def IsChinese(character):
    for cha in character:
        if not '\u0e00' <= cha <= '\u9fa5':
            return False
    else:
        return True

def find_dict_by_id(dict_list, search_id):
    """
    通过id在字典列表中找到对应的字典。

    参数:
    dict_list (list): 字典组成的列表。
    search_id (int/str): 要查找的字典的id。

    返回:
    dict: 匹配到的字典，如果未找到则返回None。
    """
    for item in dict_list:
        if item.get('id') == search_id:
            return item
    return None