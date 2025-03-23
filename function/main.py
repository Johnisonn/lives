from config import source_urls, white_lst_manual,IS_MATCH_TEMPLATE, IS_STABILITY_TEST, SORT_BY_FPS_OR_SPEED
from duplicate_removel import remove_dump_urls
from fetch import fetch_chs, fetch_chs_name
from filter import filter_by_ip_version, filter_by_names
from stability_check import generate_whitelist
from match import match_chs
from sort import sorted_by_ip_version
from save_as import save_chs_as_txt, save_chs_as_m3u
import logging
import os

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..'))

logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S-%p',
    format='%(asctime)s ==> |  %(message)s',
    handlers=[logging.FileHandler(filename=f'{parent_path}/project.log', mode='w'), logging.StreamHandler()])


def main():
    # chs = fetch_chs(['/home/uos/Desktop/0.txt'])
    chs = fetch_chs(source_urls)
    chs = remove_dump_urls(chs)
    chs = filter_by_ip_version(chs,)
    if IS_MATCH_TEMPLATE:
        chs = match_chs(chs)
    if IS_STABILITY_TEST:
        test_urls = filter_by_names(chs,['CCTV-1 综合','天津卫视'])
        white_list = generate_whitelist(urls=test_urls, sort_by_fps_or_speed=SORT_BY_FPS_OR_SPEED)
    else:
        white_list = white_lst_manual
    chs = sorted_by_ip_version(chs, white_list,)
    save_chs_as_txt(chs)
    save_chs_as_m3u(chs)



if __name__ == '__main__':
    main()



##  ---------获取各源中的频道名称-------------

    # chs_names = fetch_chs_name(['/home/uos/Desktop/rsv.txt'])
    # save_names_as_txt(chs_names,'all_names')
