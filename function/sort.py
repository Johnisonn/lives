## 响应检测，为匹配后的urls地址列表加入响应时间并排序

from collections import OrderedDict
from config import v6_or_v4
from tqdm import tqdm
import re
import time
import urllib.request #这里使用urllib模块代替requests模块，有些直播源用requests模块get请求会无反应，且不抛出异常（浏览器可返回状态200）
import multiprocessing
import concurrent.futures
import logging


logger = logging.getLogger(__name__)




def is_v6(url):
# 判别IPV6地址
    return re.search(r'\[[0-9a-fA-F:]+\]',url) is not None

def sorted_by_ip_version(chs_dict, white_lst, black_lst):
    sorted_chs_dict = OrderedDict()
    white_count = 0
    v6_count = 0
    v4_count = 0

    logger.info(' ')
    logger.info('-' * 42 + '开始按地址类型排序' + '-' * 42)
    logger.info(' ')

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
                if not any(black_domain in url for black_domain in black_lst):
                    for domain in white_lst:
                        if domain in url:
                            matched_urls.append((url, domain))
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
            for domain in white_lst:
                for url, matched_domain in matched_urls:
                    if matched_domain == domain:
                        url = f'{url}$A_{idx_white}_[★]'
                        urls_by_white.append(url)
                        idx_white += 1

#################################################

            sorted_chs_dict[cate][name].extend(urls_by_white)

            if v6_or_v4 == 6:
                sorted_chs_dict[cate][name].extend(urls_v6)
                sorted_chs_dict[cate][name].extend(urls_v4)
            else:
                sorted_chs_dict[cate][name].extend(urls_v4)
                sorted_chs_dict[cate][name].extend(urls_v6)
    logger.info('>' * 39 + f'已按照 IPV{v6_or_v4} 优先完成排序' + '<' * 39)
    logger.info('>' * 12 + f'共有 {white_count + v4_count + v6_count} 个url地址参与排序，其中V6地址 {v6_count} 个、V4地址 {v4_count} 个、白名单地址 {white_count} 个' + '<' * 12)
    return sorted_chs_dict

def sorted_by_response(urls_tuple_lst):
#对传入的（url,t）列表按照响应时间进行排序，并按设定值确定IPV6/IPV4优先序
    ipv6 = []
    ipv4 = []
    [ipv6.append(u) if is_v6(u[0]) else ipv4.append(u) for u in urls_tuple_lst]
    ipv6.sort(key=lambda x: x[1])
    ipv4.sort(key=lambda x: x[1])
    new_urls_tuple_lst = ipv6 + ipv4 if v6_or_v4 == 6 else ipv4 + ipv6
    return new_urls_tuple_lst

def test_resp_multi_thread(chs_dict, resp_threshold=None):
# 对传入的频道字典chs_dict中所有url地址，多线程并发测试响应时间，返回带响应时间的频道字典

    urls_tuple_lst = [] # 用于存放元组的列表，元组为传入频道字典中所有的url和其分类及名称（url,cate,name）
    for cate, vls in chs_dict.items():
        for name, urls in vls.items():
            for url in urls:
                urls_tuple_lst.append((url, cate, name))

    def add_resp_time(url_tuple):
    # 线程池操作函数，传入元组（url, cate, name），返回元组（url, cate, name, resp_time）
        try:
            s_time = time.time()
            resp = urllib.request.urlopen(url_tuple[0], timeout=5)
            e_time = time.time()
            resp_time = round((e_time - s_time)*1000, 2) # 单位为毫秒，保留2位小数
        except Exception:
            resp_time = 10000
        return (url_tuple[0],url_tuple[1],url_tuple[2], resp_time)

    logger.info(' ')
    logger.info('-' * 43 + '多线程响应检测开始' + '-' * 43)
    logger.info(' ')


    start_time = time.time()
    core_count = multiprocessing.cpu_count() # 获取CPU核心数
    logger.info(f'core_count: -{core_count}')
    excutor = concurrent.futures.ThreadPoolExecutor(max_workers=5*core_count+20) # 按照CPU核心数创建线程池,默认为2倍速核心+10
    future = [excutor.submit(add_resp_time, url_tuple) for url_tuple in urls_tuple_lst] # 将所有元组提交到线程池执行

    total_task = len(future)
    new_urls_tuple = [] # 用于存放新元组的列表，新元组为（url, cate, name, resp_time）
    with tqdm(total=total_task, desc=f'响应检测正在进行', ncols=100, colour='green') as t_bar: # 创建进度条
        for f in concurrent.futures.as_completed(future): # 生成器收集已完成的线程
            new_urls_tuple.append(f.result())
            t_bar.update(1) # 更新进度条
    end_time = time.time()
    logger.info(f'响应检测完成，总耗时 {round((end_time-start_time)/60, 2)} 分钟！')

    #  按照传入的频道字典顺序，重新构建值为元组(url,resp_time)的新字典
    total = len(new_urls_tuple)
    new_chs_dict = OrderedDict()
    with tqdm(total=total, desc=f'正在重构频道', ncols=100) as pbar:
        for cate, vls in chs_dict.items():
            new_chs_dict[cate] = OrderedDict()
            for name, urls in vls.items():
                new_chs_dict[cate][name] = []
                for url_tuple in new_urls_tuple:
                    if url_tuple[1] == cate and url_tuple[2] == name:
                        new_chs_dict[cate][name].append((url_tuple[0],url_tuple[3]))
            pbar.update(1)
    logger.info('频道重构完成！')

    # 按照预设响应时间对地址筛选并排序（IPV6/IPV4优先）
    logger.info(f'正在按设定阈值【{resp_threshold}】ms进行筛选和排序...')
    out_chs_dict = OrderedDict()
    for cate, vls in new_chs_dict.items():
        out_chs_dict[cate] = OrderedDict()
        for name, urls in vls.items():
            out_chs_dict[cate][name] = []
            if resp_threshold:
                urls = [url for url in urls if url[1] < resp_threshold] # 按设定阈值筛选
            urls = sorted_by_response(urls) # 调用排序函数
            for url in urls:
                out_chs_dict[cate][name].append(f'{url[0]}${url[1]}ms')
    logger.info('筛选和排序完成！')
    return out_chs_dict

