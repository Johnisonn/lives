## 对给定的直播源和模板中所需频道进行匹配，筛选出所需频道

from collections import OrderedDict
from config import is_match_local_chs
from fetch import needed_chs
import logging
import os
from name_dict import local_lst

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..'))

logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m_%d %H:%M:%S %p',
    format='%(asctime)s-%(levelname)s-%(name)s-%(message)s',
    handlers=[logging.FileHandler(filename=f'{parent_path}/project.log', mode='a'), logging.StreamHandler()])
logger = logging.getLogger(__name__)

def match_chs(chs_dict): # 将获取到的直播源字典传参
    n_chs_dict = needed_chs() # 从模板导入所需频道
    matched_chs_dict = OrderedDict()
    chs_num = 0
    urls_num = 0
    logger.info('-'*60)
    logger.info('开始匹配模板给定频道...')
    for cate_n, names_n in n_chs_dict.items():
        if cate_n not in matched_chs_dict:
            matched_chs_dict[cate_n] = OrderedDict()
        for name_n in names_n:
            for cate_f, vls_f in chs_dict.items():
                for name_f, urls_f in vls_f.items():
                    n = len(urls_f)
                    if name_f == name_n:
                        if name_n not in matched_chs_dict[cate_n]:
                            matched_chs_dict[cate_n][name_n] = []
                            # logger.info(f'已匹配到【{name_n}】')
                            chs_num += 1
                            matched_chs_dict[cate_n][name_n].extend(urls_f)
                            urls_num += n
                        else:
                            matched_chs_dict[cate_n][name_n].extend(urls_f)
                            urls_num += n

    if is_match_local_chs:  # 获取指定的地方台
        new_cate = '★地方频道★'
        local_chs_num = 0
        local_urls_num = 0
        logger.info('-'*60)
        logger.info('开始查询地方频道...')
        for cate_f, vls_f in chs_dict.items():
            for name_f, urls_f in vls_f.items():
                n = len(urls_f)
                for local_name in local_lst:
                    if local_name in name_f:
                        if new_cate not in matched_chs_dict:
                            matched_chs_dict[new_cate] = OrderedDict()
                        local_name = f'{local_name}电视台'
                        if local_name not in matched_chs_dict[new_cate]:
                            matched_chs_dict[new_cate][local_name] = []
                            logger.info('-' * 60)
                            logger.info(f'查询到【{local_name}】-已归集到【地方频道】！')
                            local_chs_num += 1
                            matched_chs_dict[new_cate][local_name].extend(urls_f)
                            local_urls_num += n
                        else:
                            matched_chs_dict[new_cate][local_name].extend(urls_f)
                            local_urls_num += n
        logger.info('-' * 60)
        logger.info(f'共采集地方频道 {local_chs_num} 个，采集url直播地址 {local_urls_num} 个！')
        logger.info('-'*60)
        logger.info(f'共匹配到模板给定频道(含查询到的地方频道) {chs_num + local_chs_num} 个，采集url直播地址 {urls_num + local_urls_num} 个！')
    return matched_chs_dict

