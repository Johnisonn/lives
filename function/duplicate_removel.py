## 对urls地址或频道名称进行去重
import logging
import os

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..'))

logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m_%d %H:%M:%S %p',
    format='%(asctime)s-%(levelname)s-%(name)s-%(message)s',
    handlers=[logging.FileHandler(filename=f'{parent_path}/project.log', mode='a'), logging.StreamHandler()])
logger = logging.getLogger(__name__)

def remove_dump_urls(chs_dict):
    urls_set = set()
    to_remove = []
    for cate, vls in chs_dict.items():
        for name, urls in vls.items():
            for url in urls:
                if url not in urls_set:
                    urls_set.add(url)
                else:
                    to_remove.append((cate,name,url)) #对重复的条目进行记录
    dump_urls_num = len(to_remove) #统计重复地址数量
    dump_chs_num = 0 # 统计重复频道名称数量
    logger.info('-' * 60)
    logger.info('开始对urls地址去重...')
    for cate, name, url in to_remove:
        chs_dict[cate][name].remove(url)
        logger.info('-'*60)
        logger.info(f'【{cate}】分类中【{name}】url成功去重1个')
        if len(chs_dict[cate][name]) < 1:
            del chs_dict[cate][name]
            logger.info('-'*60)
            logger.info(f'【{cate}】分类中【{name}】频道名重复已删除')
            dump_chs_num += 1
    logger.info('-'*60)
    logger.info(f'共去除重复频道{dump_chs_num}个，去除重复url地址{dump_urls_num}个！')
    return chs_dict

def remove_dump_name(names_dict):
# 对不同分类内重名频道名称去重
    names_set = set()
    to_remove = []
    logger.info('-'*60)
    logger.info(f'开始对所有分类中同名频道名称去重...')
    for cate, names in names_dict.items():
        for name in names:
            if name not in names_set:
                names_set.add(name)
            else:
                to_remove.append((cate, name))
    dump_names_num = len(to_remove) # 重复频道名数量
    dump_cates_num = 0
    for cate, name in to_remove:
        names_dict[cate].reverse() # 将列表倒序排列，实现列表从后往前删除，确保后边重复的频道名称被删除，而不是删除前边的
        names_dict[cate].remove(name)
        names_dict[cate].reverse()
        logger.info(f'分类【{cate}】中【{name}】名称重复已去重')
        if len(names_dict[cate]) < 1:
            del names_dict[cate]
            logger.info('-'*25 + f'分类【{cate}】重复已删除' + '-'*25)
            dump_cates_num += 1
    logger.info('-'*60)
    logger.info(f'共去除重复频道名 {dump_names_num} 个')
    logger.info(f'去除空分类 {dump_cates_num} 个')
    logger.info(f'去重后共剩余频道名称 {len(names_set)} 个！')
    return names_dict