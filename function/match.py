## 对给定的直播源和模板中所需频道进行匹配，筛选出所需频道

from collections import OrderedDict
from config import IS_MATCH_LOCAL_CHS
from fetch import readin_required_chs
from name_dict import local_lst
import logging
logger = logging.getLogger(__name__)


def match_chs(chs_dict): # 将获取到的直播源字典传参
    r_chs_dict = readin_required_chs() # 导入所需频道
    matched_chs_dict = OrderedDict()
    chs_count = 0
    urls_count = 0

    logger.info('—' * 100)
    logger.info('【开始匹配模板频道】'.center(100))

    for cate_n, names_n in r_chs_dict.items():
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
                            chs_count += 1
                            matched_chs_dict[cate_n][name_n].extend(urls_f)
                            urls_count += n
                        else:
                            matched_chs_dict[cate_n][name_n].extend(urls_f)
                            urls_count += n
    local_chs_count = 0
    local_urls_count = 0
    if IS_MATCH_LOCAL_CHS:  # 获取地方台
        new_cate = '★地方频道★'
        logger.info('【开始查询地方频道】'.center(100))
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
                            # logger.info('-' * 60)
                            logger.info(f'查询到【{local_name}】-已归集到【地方频道】！')
                            local_chs_count += 1
                            matched_chs_dict[new_cate][local_name].extend(urls_f)
                            local_urls_count += n
                        else:
                            matched_chs_dict[new_cate][local_name].extend(urls_f)
                            local_urls_count += n

    logger.info(f'匹配到地方频道 {local_chs_count} 个、url直播地址 {local_urls_count} 个'.center(100))
    logger.info(f'共匹配到模板给定频道(含匹配的地方频道) {chs_count + local_chs_count} 个、url直播地址 {urls_count + local_urls_count} 个'.center(100))
    return matched_chs_dict

