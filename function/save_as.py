## 对给定的频道字典进行保存

from datetime import datetime
from config import head_info, epg_urls, mirror_url_lst
from rename import tvg_name_regular
from response_test import is_v6
import logging
import os

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..')) # 获取上级目录路径

logger = logging.getLogger(__name__)

def save_chs_as_txt(chs_dict, file_name='live', iptype_filter=None):
    all_cate = set()
    all_chs = set()
    urls_num = 0
    current_time = datetime.now().strftime('%Y-%m-%d-%H:%M')

    logger.info(' ')
    logger.info('-' * 42 + '开始保存文件(.txt)' + '-' * 42)
    logger.info(' ')

    if iptype_filter in (4,6):
        '''此段内容为文件名添加后缀
        if iptype_filter == 4:
            v = '-v4'
        elif iptype_filter == 6:
            v = '-v6'
        path_name = f'{parent_path}/{str(file_name)}{v}.txt'
        '''
        path_name = f'{parent_path}/{str(file_name)}.txt'
        with open(path_name, 'w', encoding='utf-8') as f:
            f.write(f'{head_info['cate']},#genre#\n')
            f.write(f'{current_time},{head_info['url']}\n')
            for w_cate, w_vls in chs_dict.items():
                if w_cate not in all_cate:
                    all_cate.add(w_cate)
                    f.write(f'{w_cate},#genre#\n')
                for w_name, w_urls in w_vls.items():
                    for w_url in w_urls:
                        if is_v6(w_url) if iptype_filter == 6 else not is_v6(w_url):  # 三元表达式写法
                            f.write(f'{w_name},{w_url}\n')
                            all_chs.add(w_name)
                            urls_num += 1
    else:
        path_name = f'{parent_path}/{str(file_name)}.txt'
        with open(path_name, 'w', encoding='utf-8') as f:
            f.write(f'{head_info['cate']},#genre#\n')
            f.write(f'{current_time},{head_info['url']}\n')
            for w_cate, w_vls in chs_dict.items():
                if w_cate not in all_cate:
                    all_cate.add(w_cate)
                    f.write(f'{w_cate},#genre#\n')
                for w_name, w_urls in w_vls.items():
                    for w_url in w_urls:
                        f.write(f'{w_name},{w_url}\n')
                        all_chs.add(w_name)
                        urls_num += 1
    logger.info('>' * 10 + f'频道及url地址已保存在目录:【{path_name}】文件中' + '<' * 10)
    logger.info('>' * 34 + f'共保存频道 {len(all_chs)} 个、url地址 {urls_num} 个' + '<' * 34)
    logger.info('-' * 100)

def save_chs_as_m3u(chs_dict, file_name='live', iptype_filter=None):
    all_cate = set()
    all_chs = set()
    urls_num = 0
    current_time = datetime.now().strftime('%Y-%m-%d-%H:%M')

    logger.info(' ')
    logger.info('-' * 42 + '开始保存文件(.m3u)' + '-' * 42)
    logger.info(' ')

    if iptype_filter in (4,6):
        '''
        if iptype_filter == 4:
            v = '-v4'
        elif iptype_filter == 6:
            v = '-v6'
        path_name = f'{parent_path}/{str(file_name)}{v}.m3u'
        '''
        path_name = f'{parent_path}/{str(file_name)}.m3u'
        with open(path_name, 'w', encoding='utf-8') as f:
            f.write(f'#EXTM3U x-tvg-url="{epg_urls[0]}","{epg_urls[1]}"\n') #此处可加入多个EPG地址
            f.write(f'''#EXTINF:-1 tvg-id="之江纪录" tvg-name="之江纪录" tvg-logo="{mirror_url_lst[0]}https://raw.githubusercontent.com/fanmingming/live/main/tv/之江纪录.png" group-title="{head_info['cate']}",{current_time}\n''')
            f.write(f'{head_info['url']}\n')
            for w_cate, w_vls in chs_dict.items():
                if w_cate not in all_cate:
                    all_cate.add(w_cate)
                for w_name, w_urls in w_vls.items():
                    tvg_name = tvg_name_regular(w_name) if 'CETV' in w_name or 'CCTV' in w_name else w_name
                    for w_url in w_urls:
                        if is_v6(w_url) if iptype_filter == 6 else not is_v6(w_url):
                            f.write(f'''#EXTINF:-1 tvg-id="{tvg_name}" tvg-name="{tvg_name}" tvg-logo="{mirror_url_lst[0]}https://raw.githubusercontent.com/fanmingming/live/main/tv/{tvg_name}.png" group-title="{w_cate}",{w_name}\n''')
                            all_chs.add(w_name)
                            f.write(f'{w_url}\n')
                            urls_num += 1
    else:
        path_name = f'{parent_path}/{str(file_name)}.m3u'
        with open(path_name, 'w', encoding='utf-8') as f:
            f.write(f'#EXTM3U x-tvg-url="https://live.fanmingming.cn/e.xml","http://epg.51zmt.top:8000/e.xml"\n') #此处可加入多个EPG地址
            f.write(f'''#EXTINF:-1 tvg-id="之江纪录" tvg-name="之江纪录" tvg-logo="{mirror_url_lst[0]}https://raw.githubusercontent.com/fanmingming/live/main/tv/之江纪录.png" group-title="{head_info['cate']}",{current_time}\n''')
            f.write(f'{head_info['url']}\n')
            for w_cate, w_vls in chs_dict.items():
                if w_cate not in all_cate:
                    all_cate.add(w_cate)
                for w_name, w_urls in w_vls.items():
                    tvg_name = tvg_name_regular(w_name) if 'CETV' in w_name or 'CCTV' in w_name else w_name
                    for w_url in w_urls:
                        f.write(f'''#EXTINF:-1 tvg-id="{tvg_name}" tvg-name="{tvg_name}" tvg-logo="{mirror_url_lst[0]}https://raw.githubusercontent.com/fanmingming/live/main/tv/{tvg_name}.png" group-title="{w_cate}",{w_name}\n''')
                        all_chs.add(w_name)
                        f.write(f'{w_url}\n')
                        urls_num += 1
    logger.info('>' * 10 + f'频道及url地址已保存在目录:【{path_name}】文件中' + '<' * 10)
    logger.info('>' * 34 + f'共保存频道 {len(all_chs)} 个、url地址 {urls_num} 个' + '<' * 34)
    logger.info('=' * 100)

def save_names_as_txt(names_dict, file_name='chs_names'):
    path_name = f'{parent_path}/{str(file_name)}.txt'
    with open(path_name, 'w', encoding='utf-8') as f:
        for w_cate, w_names in names_dict.items():
            f.write(f'{w_cate},#genre#\n')
            for w_name in w_names:
                f.write(f'{w_name},\n')
    logger.info('>' * 15 + f'获取到的频道名称已保存在目录:【{path_name}】文件中' + '<' * 15)