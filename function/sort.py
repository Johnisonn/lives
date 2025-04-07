## 响应检测，为匹配后的urls地址列表加入响应时间并排序

from collections import OrderedDict
from config import SORT_BY_V6_OR_V4, black_lst, SORT_BY_FPS_OR_SPEED
import re
import logging
logger = logging.getLogger(__name__)



# 判别IPV6地址
def is_v6(url: str):
    return re.search(r'\[[0-9a-fA-F:]+\]',url) is not None

# 优先按照白名单排序，其余按IPV4或IPV6排序
def sorted_by_ip_version(chs_dict, white_lst, black_lst=black_lst, is_keey_only_white_lst=0):
    sorted_chs_dict = OrderedDict()
    white_count = 0
    v6_count = 0
    v4_count = 0

    if not is_keey_only_white_lst:
        logger.info('—' * 100)
        logger.info(f'【开始按地址类型排序】:IPV{SORT_BY_V6_OR_V4}优先'.center(100))
    else:
        logger.info('—' * 100)
        logger.info('【开始按白名单顺序排序】:只保留白名单URLS'.center(100))

    for cate, vls in chs_dict.items():
        sorted_chs_dict[cate] = OrderedDict()
        for name, urls in vls.items():
            sorted_chs_dict[cate][name] = []
            matched_urls = []
            urls_v6 = []
            urls_v4 = []
            idx_white = 1
            idx_v6 = 1
            idx_v4 = 1
            for url in urls:
                for white_keyword in white_lst:
                    if white_keyword in url:
                        if not any(black_keyword in url for black_keyword in black_lst):
                            matched_urls.append((url, white_keyword))
                            white_count += 1
                            break
                else:
                    if is_v6(url):
                        url = f'{url}$C_{idx_v6}_[v6]'
                        idx_v6 += 1
                        urls_v6.append(url)
                        v6_count += 1
                    else:
                        url = f'{url}$B_{idx_v4}_[v4]'
                        idx_v4 += 1
                        urls_v4.append(url)
                        v4_count += 1

#  对白名单urls按照白名单排序
            urls_by_white = []
            for white_keyword in white_lst:
                for url, matched_keyword in matched_urls:
                    if matched_keyword == white_keyword:
                        url = f'{url}$A_{idx_white}_[★]'
                        urls_by_white.append(url)
                        idx_white += 1

            sorted_chs_dict[cate][name].extend(urls_by_white)
            if is_keey_only_white_lst:
                continue

            if SORT_BY_V6_OR_V4 == 6:
                sorted_chs_dict[cate][name].extend(urls_v6)
                sorted_chs_dict[cate][name].extend(urls_v4)
            else:
                sorted_chs_dict[cate][name].extend(urls_v4)
                sorted_chs_dict[cate][name].extend(urls_v6)

    if is_keey_only_white_lst:
        logger.info(f'已按白名单地址完成排序(by_{SORT_BY_FPS_OR_SPEED})，共有白名单地址 {white_count} 个'.center(100))
    else:
        logger.info(f'共有 {white_count + v4_count + v6_count} 个url地址参与排序，其中V6地址 {v6_count} 个、V4地址 {v4_count} 个、白名单地址 {white_count} 个'.center(100))

    return sorted_chs_dict
