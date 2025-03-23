## 对不同源地址中的频道名称进行规范统一，主要针对央视、及卫视名称进行规范，后续可针对性对地方频道进行规范

import re
import name_dict


def ch_name_regular(name: str):
    name = name.upper()
    cctv_dict = name_dict.cctv_dict #读入需要规范的频道字典
    reg_name = None


    #对央视频道进行名称规范
    if 'CCTV' in name or '央' in name:
        match = re.search(r'(CCTV|央视|中央)[ ,-]{0,1}(\d+\+{0,1}K{0,1})|(CCTV|中央|央视)(\w+)', name)
        if match:
            str = match.group(2) # 匹配到的CCTV的数字台和'4K''8K''5+'
            if str and 'K' not in str and '+' not in str:  # 对央视纯数字台进行判别，加入if str目的是确保str不为空，否则对汉字台报错
                str = int(str) # 对数字台转为数字，匹配名称字典
            str2 = match.group(4) # 匹配到的CCTV的其他汉字命名的台
            if str in cctv_dict :
                reg_name = f"CCTV{cctv_dict[str]}"
            elif str2 in cctv_dict:
                reg_name = f"CCTV{cctv_dict[str2]}"
            else:
                reg_name = f"CCTV-{str2}"
            return reg_name

    # 对央视外语频道名称进行规范
    if 'CGTN' in name:
        for key, value in name_dict.cgtn_dict.items():
            if key in name:
                reg_name = f'CGTN-{value}'
                return reg_name

    # 对中国教育频道名称进行规范
    if ('CETV' in name or '中国教育' in name) and any(x in name for x in ['1','2','3','4']):
        num = ''.join([char for char in name if char.isdigit()])
        num = int(num)
        if num in name_dict.cetv_dict:
            reg_name = f'CETV-{num} {name_dict.cetv_dict[num]}'
            return reg_name

    # 对各省卫视频道名称进行规范
    if '卫视' in name:
        province_dict = name_dict.province_dict
        match = re.search(r'(^\w+)卫视', name)
        if match:
            str = match.group(1)
            if str in province_dict:
                reg_name = f'{province_dict[str]}卫视'
            else:
                reg_name = f'{str}卫视'
            return reg_name

    # 对其他频道名称进行规范
    for k, v in name_dict.other_dict.items():
        if k in name:
            reg_name = v
            return reg_name

    return name

def cate_name_regular(cate: str):
    cates = name_dict.category_dict
    for key in cates:
        if key in cate:
            reg_cate = cates[key]
            break
        else:
            reg_cate = cate
    return reg_cate

def tvg_name_regular(name: str): #对央视频道及教育频道名称进行处理，在写入M3U文件时匹配EPG台标名称
    if 'CCTV' in name and '-' in name:
        name = name.split()[0]
        name1,name2 = name.split('-')
        name = name1 + name2
    elif 'CETV' in name and '-' in name:
        name = name.split()[0]
        name1,name2 = name.split('-')
        name = f'中国教育{name2}台'
    else:
        name = name

    return name

