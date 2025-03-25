# 获取直播地址或频道名称

import re
import os
import requests
import logging
from collections import OrderedDict
from duplicate_removel import remove_dump_names
from config import mirror_url_lst
from rename import ch_name_regular


current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..'))
logger = logging.getLogger(__name__)


def readin_required_chs():
# 从模板文件中读入所需要频道分类和频道名称
    required_chs_dict = OrderedDict()

    logger.info('—' * 100)
    logger.info('【开始读入模板信息】'.center(100))

    with open(f'{current_path}/template.txt', 'r', encoding='utf-8') as f:
        chs_count = 0
        for line in f:
            line = line.strip()
            if '#genre#' in line:
                ch_cate = line.split(',')[0]
                if ch_cate not in required_chs_dict:
                    required_chs_dict[ch_cate] = []
            elif line:
                line = line.split(',')[0]
                if line not in required_chs_dict[ch_cate]:
                    required_chs_dict[ch_cate].append(line)
                    chs_count += 1


    logger.info(f'共提取模板中分类 {len(required_chs_dict)} 个、频道 {chs_count} 个'.center(100))
    return required_chs_dict

def fetch_chs(source_urls_lst: list):
    chs_dict = OrderedDict()
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36'}
    total_chs_count = 0
    total_urls_count = 0

    logger.info('—' * 100)
    logger.info('【开始获取频道资源】'.center(100))

    for proxy in mirror_url_lst:
        u = f'{proxy}https://raw.githubusercontent.com/fanmingming/live/refs/heads/main/tv/m3u/ipv6.m3u'
        r = requests.get(u, headers=header, timeout=4)
        if 200 <= r.status_code < 300:
            break

    for source_url in source_urls_lst:
        if 'http' in source_url:  # 网络直播源
            if 'github' in source_url:
                source_url = proxy + source_url
            try:
                resp = requests.get(source_url, headers=header, timeout=4)
                resp.raise_for_status()
                resp.encoding = 'utf-8'
                lines = resp.text.split('\n')
            except requests.exceptions.RequestException as e:
                logger.error(f"{source_url}请求失败，错误信息: {str(e)}")
                continue
        else:  # 本地直播源文件
            with open(source_url, 'r') as file:
                lines = file.readlines()
        chs_count = 0
        urls_count = 0
        source_type = 'm3u' if any('#EXTINF' in line for line in lines[:4]) else 'txt'  # 判定直播源类型（txt或者m3u）
        if source_type == 'txt':
            for line in lines:  # 对txt类型的直播源读入
                if '#genre#' in line:
                    line = line.strip()
                    cate = line.split(',')[0]
                    if cate not in chs_dict:
                        chs_dict[cate] = OrderedDict()
                elif re.match(r'^(.*?),(.*?)$', line):  # 正则匹配IP地址
                    name, url = line.split(',', 1)
                    name = ch_name_regular(name)
                    url = url.strip()
                    if 'cate' not in locals():  # 考虑源中没有分类的情况
                        cate = '无分类'
                        chs_dict[cate] = OrderedDict()
                    if '#' in url:  # 以海阔模式串联多个urls的情况
                        urls = url.split('#')
                        urls = [url.split('$')[0] if '$' in url else url for url in urls]
                        n = len(urls)
                        if name not in chs_dict[cate]:
                            chs_dict[cate][name] = []
                            chs_count += 1
                            chs_dict[cate][name].extend(urls)
                            urls_count += n
                        else:
                            chs_dict[cate][name].extend(urls)
                            urls_count += n
                        continue
                    if '$' in url:
                        url = url.split('$')[0]
                    if name not in chs_dict[cate]:
                        chs_dict[cate][name] = []
                        chs_count += 1
                        chs_dict[cate][name].append(url)
                        urls_count += 1
                    else:
                        chs_dict[cate][name].append(url)
                        urls_count += 1
            total_chs_count += chs_count
            total_urls_count += urls_count
        else:  # 对m3u类型的直播源读入
            for line in lines:
                if '#EXTINF' in line:
                    match = re.search(r'group-title=(.*),(.*)', line)
                    if match:
                        cate = match.group(1).strip()
                        name = match.group(2).strip()
                        name = ch_name_regular(name)
                        if cate not in chs_dict:
                            chs_dict[cate] = OrderedDict()
                            chs_dict[cate][name] = []
                            chs_count += 1
                        elif name not in chs_dict[cate]:
                            chs_dict[cate][name] = []
                            chs_count += 1
                elif line.strip() and not line.startswith('#'):
                    url = line.strip()
                    if '$' in url:
                        url = url.split('$')[0]
                    if cate and name:
                        chs_dict[cate][name].append(url)
                        urls_count += 1
            total_chs_count += chs_count
            total_urls_count += urls_count
        logger.info(f'从<{source_url}>获取频道 {chs_count} 个(类内同名已去重)，获取url地址 {urls_count} 个(未去重)！')
    # 以处内容为保存获取到的频道列表名单到日志
    # logger.info('-'*25 + f'获取到的频道列表' + '-'*25)
    # for k, v in chs_dict.items():
    #     for n, u in v.items():
    #         logger.info(f'{k}-{n}-{u}')

    logger.info('-' * 100)
    logger.info(f'共从 {len(source_urls_lst)} 个源地址中获取频道 {total_chs_count} 个，获取url地址 {total_urls_count} 个'.center(100))
    return chs_dict

def fetch_chs_name(source_urls_lst: list):
# 获取给定的一组直播源地址列表中的频道名称（含频道分类，对分类内重复频道名去重，）
    chs_dict = fetch_chs(source_urls_lst)
    names_dict = OrderedDict()
    name_num = 0
    for cate, vls in chs_dict.items():
        if cate not in names_dict:
            names_dict[cate] = []
        for name, urls in vls.items():
            if name not in names_dict[cate]:
                names_dict[cate].append(name)
                name_num += 1

    logger.info(f'共获取频道名称 {name_num} 个(不同分类间同名频道未去重)！'.center(100))
    names_dict = remove_dump_names(names_dict) #对所有分类内频道名称去重

    return names_dict




if __name__ == '__main__':
    source_urls_lst = [
                        '/home/uos/Desktop/live/0.txt',
                       '/home/uos/Desktop/live/666.txt',
                       '/home/uos/Desktop/live/cqitv.txt',
                        '/home/uos/Desktop/live/junyu.txt',
                        '/home/uos/Desktop/live/kimwang1978.txt',
                        '/home/uos/Desktop/live/kv.txt',
                        '/home/uos/Desktop/live/qingwen07.txt',
                       '/home/uos/Desktop/live/rihou.nzk',
                       '/home/uos/Desktop/live/ssili126.txt',
                        '/home/uos/Desktop/live/vbskycn.txt',
                        '/home/uos/Desktop/live/weidongdong.txt',
                        '/home/uos/Desktop/live/xhztv.txt',
                        '/home/uos/Desktop/live/zhoujie.txt',
                        '/home/uos/Desktop/live/喵TV.txt',
                        '/home/uos/Desktop/live/guovin.m3u',
                        '/home/uos/Desktop/live/meoxin.m3u',
                        '/home/uos/Desktop/live/yangg1989.m3u',
                        '/home/uos/Desktop/live/yuanzl77.m3u',
                        '/home/uos/Desktop/live/YueChan_IPTV.m3u',
                        '/home/uos/Desktop/live/范明明.m3u',

    ]
    # fetch_chs_name(source_urls_lst)

