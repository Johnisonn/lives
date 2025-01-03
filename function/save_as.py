## 对给定的频道字典进行保存

from datetime import datetime
from config import head_info
from rename import tvg_name_regular
from response_test import is_v6
import logging

logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S %p',
    format='%(asctime)s-%(name)s-%(levelname)s-%(massage)s',
    handlers=[logging.FileHandler(filename='../project.log', mode='a'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def save_chs_as_txt(chs_dict, file_name='live', ip_filter=None):
    default_path = '../' #默认路径为上级目录
    all_cate = set()
    all_chs = set()
    urls_num = 0
    current_time = datetime.now().strftime('%Y-%m-%d-%H:%M')
    if ip_filter is None:
        path_name = default_path + str(file_name) + '.txt'
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
    else:
        if ip_filter == 4:
            v = '-v4'
        elif ip_filter == 6:
            v = '-v6'
        else:
            raise ValueError("ip_type 参数只能是 4、6 或不传")
        path_name = default_path + str(file_name) + v + '.txt'
        with open(path_name, 'w', encoding='utf-8') as f:
            f.write(f'{head_info['cate']},#genre#\n')
            f.write(f'{current_time},{head_info['url']}\n')
            for w_cate, w_vls in chs_dict.items():
                if w_cate not in all_cate:
                    all_cate.add(w_cate)
                    f.write(f'{w_cate},#genre#\n')
                for w_name, w_urls in w_vls.items():
                    for w_url in w_urls:
                        if is_v6(w_url) if ip_filter == 6 else not is_v6(w_url):  # 三元表达式写法
                            f.write(f'{w_name},{w_url}\n')
                            all_chs.add(w_name)
                            urls_num += 1
    logger.info('-'*60)
    logger.info(f'频道及url地址已保存在目录【{path_name}】下，共保存频道{len(all_chs)}个、url地址{urls_num}个！')

def save_chs_as_m3u(chs_dict, file_name='live', ip_filter=None):
    default_path = '../' #默认路径为上级目录
    all_cate = set()
    all_chs = set()
    urls_num = 0
    current_time = datetime.now().strftime('%Y-%m-%d-%H:%M')
    if ip_filter is None:
        path_name = default_path + str(file_name) + '.m3u'
        with open(path_name, 'w', encoding='utf-8') as f:
            f.write(f'#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml"\n') #此处可加入多个EPG地址
            f.write(f'''#EXTINF:-1 tvg-id="之江纪录" tvg-name="之江纪录" tvg-logo="https://live.fanmingming.com/tv/之江纪录.png" group-title="{head_info['cate']}",{current_time}\n''')
            f.write(f'{head_info['url']}\n')
            for w_cate, w_vls in chs_dict.items():
                if w_cate not in all_cate:
                    all_cate.add(w_cate)
                for w_name, w_urls in w_vls.items():
                    tvg_name = tvg_name_regular(w_name) if 'CETV' in w_name or 'CCTV' in w_name else w_name
                    for w_url in w_urls:
                        f.write(f'''#EXTINF:-1 tvg-id="{tvg_name}" tvg-name="{tvg_name}" tvg-logo="https://live.fanmingming.com/tv/{tvg_name}.png" group-title="{w_cate}",{w_name}\n''')
                        all_chs.add(w_name)
                        f.write(f'{w_url}\n')
                        urls_num += 1
    else:
        if ip_filter == 4:
            v = '-v4'
        elif ip_filter == 6:
            v = '-v6'
        else:
            raise ValueError("ip_type 参数只能是 4、6 或不传")
        path_name = default_path + str(file_name) + v +'.m3u'
        with open(path_name, 'w', encoding='utf-8') as f:
            f.write(f'#EXTM3U x-tvg-url="https://live.fanmingming.com/e.xml"\n') #此处可加入多个EPG地址
            f.write(f'''#EXTINF:-1 tvg-id="之江纪录" tvg-name="之江纪录" tvg-logo="https://live.fanmingming.com/tv/之江纪录.png" group-title="{head_info['cate']}",{current_time}\n''')
            f.write(f'{head_info['url']}\n')
            for w_cate, w_vls in chs_dict.items():
                if w_cate not in all_cate:
                    all_cate.add(w_cate)
                for w_name, w_urls in w_vls.items():
                    tvg_name = tvg_name_regular(w_name) if 'CETV' in w_name or 'CCTV' in w_name else w_name
                    for w_url in w_urls:
                        if is_v6(w_url) if ip_filter == 6 else not is_v6(w_url):
                            f.write(f'''#EXTINF:-1 tvg-id="{tvg_name}" tvg-name="{tvg_name}" tvg-logo="https://live.fanmingming.com/tv/{tvg_name}.png" group-title="{w_cate}",{w_name}\n''')
                            all_chs.add(w_name)
                            f.write(f'{w_url}\n')
                            urls_num += 1
    logger.info('-'*60)
    logger.info(f'频道及url地址已保存在目录：【{path_name}】下，共保存频道{len(all_chs)}个、url地址{urls_num}个！')

def save_names_as_txt(names_dict, file_name='names'):
    path = '../'
    with open(path + str(file_name) + '.txt', 'w') as f:
        for w_cate, w_names in names_dict.items():
            f.write(f'{w_cate},#genre#\n')
            for w_name in w_names:
                f.write(f'{w_name},\n')
