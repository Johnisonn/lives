# 获取直播地址或频道名称

import re
from collections import OrderedDict
import requests
from function.duplicate_removel import remove_dump_name
from function.rename import ch_name_regular, cate_name_regular
import logging

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m_%d %H:%M:%S %p', format='%(asctime)s-%(levelname)s-%(name)s-%(message)s', handlers=[logging.FileHandler(filename='../project.log', mode='w'), logging.StreamHandler()])
logger = logging.getLogger(__name__)


def needed_chs():
# 从模板文件中读入所需要频道分类和频道名称
    need_chs_dict = OrderedDict()
    with open('../function/template.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '#genre#' in line:
                ch_cate = line.split(',')[0]
                if ch_cate not in need_chs_dict:
                    need_chs_dict[ch_cate] = []
            elif line:
                line = line.split(',')[0]
                if line not in need_chs_dict[ch_cate]:
                    need_chs_dict[ch_cate].append(line)
    return need_chs_dict

def fetch_multi_urls_chs(source_urls_lst):
# 对给定的一组直播源地址列表中的直播源全部读入（不对地址去重，但规范分类名称）
# #传参为列表
    merge_chs_dict = OrderedDict()
    for url in source_urls_lst:
        merge_chs_dict = merge_dict(merge_chs_dict, fetch_single_url_chs(url))
    return merge_chs_dict

def fetch_chs_name(source_urls_lst):
# 提取给定的一组直播源地址列表中的频道名称（对分类内重复频道名去重）
    chs_dict = fetch_multi_urls_chs(source_urls_lst)
    names_dict = OrderedDict()
    name_num = 0
    for cate, vls in chs_dict.items():
        if cate not in names_dict:
            names_dict[cate] = []
        for name, urls in vls.items():
            if name not in names_dict[cate]:
                names_dict[cate].append(name)
                name_num += 1

    logger.info('-'*60)
    logger.info(f'共提取频道名称{name_num}个(已对不同分类中同名频道去重)！')
    names_dict = remove_dump_name(names_dict) #对频道名称去重

    return names_dict

def fetch_single_url_chs(source_url):
# 对给定的单个直播源地址中的直播源全部读入（不对分类改名，不对地址去重，规范频道名称后原封收入）
# 参数传入网络直播源地址或本地直播源文件路径
    chs_dict = OrderedDict()
    header = {'User-Agent':'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36'}
    if 'http' in source_url: # 打开网络直播源
        try:
            resp = requests.get(source_url, headers = header, timeout=4)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            lines = resp.text.split('\n')
        except requests.exceptions.RequestException as e:
            logger.info('-'*60)
            logger.error(f"{source_url}请求失败，错误信息: {str(e)}")
            return chs_dict
    else:  # 打开本地直播源文件
        with open(source_url, 'r') as file:
            lines = file.readlines()
    source_type = 'm3u' if any('#EXTINF' in line for line in lines[:4]) else 'txt'  # 判定直播源类型（txt或者m3u）
    if source_type == 'txt':
        ch_num = 0
        url_num = 0
        for line in lines:
            if '#genre#' in line:  # 对txt类型的直播源读入
                line = line.strip()
                cate = line.split(',')[0]
                if cate not in chs_dict:
                    chs_dict[cate] = OrderedDict()
            elif re.match(r'^(.*?),(.*?)$', line):  # 正则匹配IP地址
                name, url = line.split(',',1)
                name = ch_name_regular(name)
                url = url.strip()
                if 'cate' not in locals(): # 考虑源中没有分类的情况
                    cate = '无分类'
                    chs_dict[cate] = OrderedDict()
                if '#' in url: # 以海阔模式串联多个url的情况
                    urls = url.split('#')
                    urls = [url.split('$')[0] if '$' in url else url for url in urls]
                    n = len(urls)
                    if name not in chs_dict[cate]:
                        chs_dict[cate][name] = []
                        ch_num += 1
                        chs_dict[cate][name].extend(urls)
                        url_num += n
                    else:
                        chs_dict[cate][name].extend(urls)
                        url_num += n
                    continue
                if '$' in url:
                    url = url.split('$')[0]

                elif name not in chs_dict[cate]:
                    chs_dict[cate][name] = []
                    ch_num += 1
                    chs_dict[cate][name].append(url)
                    url_num += 1
                else:
                    chs_dict[cate][name].append(url)
                    url_num += 1
    else: # 对m3u类型的直播源读入
        ch_num = 0
        url_num = 0
        for line in lines:
            if '#EXTINF' in line:
                match = re.search(r'group-title="(.*?)",(.*)', line)
                cate = match.group(1).strip()
                name = match.group(2).strip()
                name = ch_name_regular(name)
                if cate not in chs_dict:
                    chs_dict[cate] = OrderedDict()
                    chs_dict[cate][name] = []
                    ch_num += 1
                elif name not in chs_dict[cate]:
                    chs_dict[cate][name] = []
                    ch_num += 1
            elif line.strip() and not line.startswith('#'):
                url = line.strip()
                if '$' in url:
                    url = url.split('$')[0]
                if cate and name:
                    chs_dict[cate][name].append(url)
                    url_num += 1
    logger.info('-'*60)
    logger.info(f'从【{source_url}】获取频道{ch_num}个(已合并分类内同名)，获取url地址{url_num}个(未去重)！')
    return chs_dict

def merge_dict(dict1, dict2):
# 对获取到的两个频道字典进行合并（对分类规范名称）
    merged_dict = dict1
    for cate, ch_vls in dict2.items():
        cate = cate_name_regular(cate)
        if cate in merged_dict:
            for name, urls in ch_vls.items():
                if name not in merged_dict[cate]:
                    merged_dict[cate][name] = []
                    merged_dict[cate][name].extend(urls)
                else:
                    merged_dict[cate][name].extend(urls)
        else:
            merged_dict[cate] = ch_vls
    return merged_dict


def fetch_chs(source_urls_lst):
    chs_dict = OrderedDict()
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36'}
    total_ch_num = 0
    total_url_num = 0
    for source_url in source_urls_lst:
        if 'http' in source_url:  # 网络直播源地址
            try:
                resp = requests.get(source_url, headers=header, timeout=4)
                resp.raise_for_status()
                resp.encoding = 'utf-8'
                lines = resp.text.split('\n')
            except requests.exceptions.RequestException as e:
                logger.info('-' * 60)
                logger.error(f"{source_url}请求失败，错误信息: {str(e)}")
        else:  # 本地直播源文件
            with open(source_url, 'r') as file:
                lines = file.readlines()
        source_type = 'm3u' if any('#EXTINF' in line for line in lines[:4]) else 'txt'  # 判定直播源类型（txt或者m3u）
        if source_type == 'txt':
            ch_num = 0
            url_num = 0
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
                    if '#' in url:  # 以海阔模式串联多个url的情况
                        urls = url.split('#')
                        urls = [url.split('$')[0] if '$' in url else url for url in urls]
                        n = len(urls)
                        if name not in chs_dict[cate]:
                            chs_dict[cate][name] = []
                            ch_num += 1
                            chs_dict[cate][name].extend(urls)
                            url_num += n
                        else:
                            chs_dict[cate][name].extend(urls)
                            url_num += n
                        continue
                    if '$' in url:
                        url = url.split('$')[0]
                    if name not in chs_dict[cate]:
                        chs_dict[cate][name] = []
                        ch_num += 1
                        chs_dict[cate][name].append(url)
                        url_num += 1
                    else:
                        chs_dict[cate][name].append(url)
                        url_num += 1
            total_ch_num += ch_num
            total_url_num += url_num
        else:  # 对m3u类型的直播源读入
            for line in lines:
                if '#EXTINF' in line:
                    match = re.search(r'group-title="(.*?)",(.*)', line)
                    cate = match.group(1).strip()
                    name = match.group(2).strip()
                    name = ch_name_regular(name)
                    if cate not in chs_dict:
                        chs_dict[cate] = OrderedDict()
                        chs_dict[cate][name] = []
                        ch_num += 1
                    elif name not in chs_dict[cate]:
                        chs_dict[cate][name] = []
                        ch_num += 1
                elif line.strip() and not line.startswith('#'):
                    url = line.strip()
                    if '$' in url:
                        url = url.split('$')[0]
                    if cate and name:
                        chs_dict[cate][name].append(url)
                        url_num += 1
            total_ch_num += ch_num
            total_url_num += url_num
        logger.info('-' * 60)
        logger.info(f'从【{source_url}】获取频道{ch_num}个(类内同名已去重)，获取url地址{url_num}个(未去重)！')

        logger.info('-'*60)
        for k, v in chs_dict.items():
            for n, u in v.items():
                logger.info(f'{k}-{n}-{u}')
    logger.info('-' * 60)
    logger.info(f'共从{len(source_urls_lst)}个源地址中获取频道{total_ch_num}个，获取url地址{total_url_num}个！')
    return chs_dict


source_urls_lst = ['/home/uos/Desktop/1.txt',
                   '/home/uos/Desktop/2.txt',
                   '/home/uos/Desktop/3.txt'


]

fetch_chs(source_urls_lst)

