
from collections import OrderedDict
from typing import Union, List
import ipaddress
from urllib.parse import urlparse
import copy


# 判定IP地址版本
def get_ip_version(url):
    def extract_ip(s):
        parsed = urlparse(s)
        if parsed.hostname:
            host = parsed.hostname
            if host.startswith('[') and host.endswith(']'):
                host = host[1:-1]
            return host
        if s.startswith('[') and ']:' in s:
            return s.split(']:')[0][1:]
        if '://' not in s:
            if s.count(':') > 1 and '[' not in s and ']' not in s:
                parts = s.split(':')
                possible_ip = ':'.join(parts[:-1]) if len(parts) > 1 else s
                return possible_ip
            elif ':' in s and s.count(':') < 2:
                return s.split(':')[0]
        return s

    ip_str = extract_ip(url)
    if not ip_str:
        return None
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.version
    except ValueError:
        return None

# 筛选给定类型的IP地址（v4或v6）
def filter_by_iptype(chs_dict, ip_version=None):
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
def filter_by_names(chs_dict: OrderedDict,
                    target_names: Union[str, List[str]]) -> List[str]:

    # 标准化输入格式为集合
    search_names = {target_names} if isinstance(target_names, str) else set(target_names)

    result = []
    # 遍历所有类别
    for category in chs_dict.values():
        # 遍历当前类别下的所有直播源
        for name, urls in category.items():
            if name in search_names:
                result.extend(urls)
    return result