
from collections import OrderedDict
from typing import Union, List
from stability_check import extract_keyword
import re
import copy




# 判定IP地址版本
def get_ip_version(url: str):
    return 6 if re.search(r'\[[0-9a-fA-F:]+\]',url) is not None else 4

# 筛选v4或v6的URL
def filter_by_ip_version(chs_dict, ip_version=None):
    if ip_version not in (4, 6, None):
        raise ValueError("ip_version must be 4, 6, or None")
    if ip_version is None:
        return copy.deepcopy(chs_dict)

    filtered_dict = OrderedDict()
    for cate, names_dict in chs_dict.items():
        filtered_names = OrderedDict()
        for name, urls in names_dict.items():
            filtered_urls = [url for url in urls if get_ip_version(url) == ip_version]
            if filtered_urls:
                filtered_names[name] = filtered_urls
        if filtered_names:
            filtered_dict[cate] = filtered_names
    return filtered_dict

# 筛选给定频道的urls
def filter_by_names(chs_dict: OrderedDict, target_names: Union[str, List[str]]) -> List[str]:

    # 标准化输入格式为集合
    search_names = {target_names} if isinstance(target_names, str) else set(target_names)
    result = []
    features = set()
    merged_result = []
    # 遍历所有类别
    for category in chs_dict.values():
        for name, urls in category.items():
            if name in search_names:
                result.extend(urls)

    for url in result:
        feature = extract_keyword(url)
        if feature not in features:
            features.add(feature)
            merged_result.append(url)


    return merged_result