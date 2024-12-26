## 响应检测，为匹配后的urls地址列表加入响应时间并排序
import re
import time
import urllib.request #这里使用urllib模块代替requests模块，有些直播源用requests模块get请求会无反应，且不抛出异常（浏览器可返回状态200）
from collections import OrderedDict
from function.config import v6_or_v4
from tqdm import tqdm
import multiprocessing
import concurrent.futures
import logging

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m_%d %H:%M:%S %p', format='%(asctime)s-%(levelname)s-%(name)s-%(message)s', handlers=[logging.FileHandler(filename='../project.log', mode='a'), logging.StreamHandler()])
logger = logging.getLogger(__name__)


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
            resp = urllib.request.urlopen(url_tuple[0],timeout=2)
            e_time = time.time()
            resp_time = round((e_time - s_time)*1000, 2) # 单位为毫秒，保留2位小数
        except Exception:
            resp_time = 100000
        return (url_tuple[0],url_tuple[1],url_tuple[2], resp_time)

    logger.info('-'*60)
    logger.info('多线程响应检测开始！')
    start_time = time.time()
    core_count = multiprocessing.cpu_count() # 获取CPU核心数
    logger.info(f'core_count:{core_count}')
    excutor = concurrent.futures.ThreadPoolExecutor(max_workers=2*core_count+10) # 按照CPU核心数创建线程池
    future = [excutor.submit(add_resp_time, url_tuple) for url_tuple in urls_tuple_lst] # 将所有元组提交到线程池执行

    total_task = len(future)
    new_urls_tuple = [] # 用于存放新元组的列表，新元组为（url, cate, name, resp_time）
    with tqdm(total=total_task, desc=f'响应检测正在进行', ncols=100, colour='green') as t_bar: # 创建进度条
        for f in concurrent.futures.as_completed(future): # 生成器收集已完成的线程
            new_urls_tuple.append(f.result())
            t_bar.update(1) # 更新进度条
    end_time = time.time()
    logger.info(f'响应检测完成，总耗时{round((end_time-start_time)/60, 2)}分钟！')

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

def is_v6(url):
# 判别IPV6地址
    return re.search(r'\[[0-9a-zA-Z:]+\]',url) is not None

def sorted_by_response(urls_tuple_lst):
#对传入的（url,t）列表按照响应时间进行排序，并按设定值确定IPV6/IPV4优先序
    ipv6 = []
    ipv4 = []
    [ipv6.append(u) if is_v6(u[0]) else ipv4.append(u) for u in urls_tuple_lst]
    ipv6.sort(key=lambda x: x[1])
    ipv4.sort(key=lambda x: x[1])
    new_urls_tuple_lst = ipv6 + ipv4 if v6_or_v4 == 6 else ipv4 + ipv6
    return new_urls_tuple_lst



##  以下两个函数为单线程测试，已弃用
def test_resp(url):
# 对单个url地址测试响应时间，返回带响应时间的url元组(url,t),因加入线程池写法，此函数弃用
    try:
        start_time = time.time()
        resp = urllib.request.urlopen(url, timeout=2)
        end_time = time.time()
        t = round((end_time - start_time)*1000, 2) #记录响应时间，单位为毫秒
    except Exception: # 对请求失败的url将响应时间置为100000
        t = 100000
    url_tuple = (url, t)
    return url_tuple

def test_resp_single_thread(chs_dict, resp_threshold=None):
# 对传入的频道字典按照响应时间排序，并按传入阈值进行筛选，此函数为单线程方法，已弃用
    chs_t_dict = OrderedDict()
    t1 = time.time()
    for cate, vls in chs_dict.items():
        chs_t_dict[cate] = OrderedDict()
        for name, urls in vls.items():
            urls = [test_resp(url) for url in tqdm(urls, desc=f'【{name}】响应检测中', position=0)]
            urls = sorted_by_response(urls)
            if resp_threshold:
                urls = [url_t for url_t in urls if url_t[1] < resp_threshold] # 筛选响应时间小于给定阈值的url
            urls = [f'{url[0]}${url[1]}ms' for url in urls]
            chs_t_dict[cate][name] = []
            chs_t_dict[cate][name].extend(urls)
    t2 = time.time()
    print(f'响应检测完成，总耗时{round((t2 - t1) / 60, 2)}分钟，阈值为{resp_threshold}ms！')
    return chs_t_dict


