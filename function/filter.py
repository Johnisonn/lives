
from collections import OrderedDict
from typing import Union, List
from stability_check import extract_keyword
import re
import copy
import logging
logger = logging.getLogger(__name__)




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
def filter_by_names(chs_dict: OrderedDict, target_names: Union[str, List[str], None] = None) -> List[str]:
    result = []
    features = set()
    merged_result = []
    search_names = {}

    logger.info('—' * 100)

    if target_names is None:
        # target_names 为空，提取所有 urls
        logger.info('【开始抽取样本】:全部采集'.center(100))
        for category in chs_dict.values():
            for urls in category.values():
                result.extend(urls)
    else:
        # target_names 不为空，提取指定名称对应的 urls
        search_names = {target_names} if isinstance(target_names, str) else set(target_names)
        logger.info(f'【开始抽取样本】:样本：{','.join(search_names)}'.center(100))
        for category in chs_dict.values():
            for name, urls in category.items():
                if name in search_names:
                    result.extend(urls)

    # 根据 extract_keyword 函数规则去重
    for url in result:
        feature = extract_keyword(url)
        if feature not in features:
            features.add(feature)
            merged_result.append(url)

    logger.info(f'共从 {len(search_names)} 个样本中采集urls {len(merged_result)} 个'.center(100))
    return merged_result