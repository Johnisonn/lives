from config import response_time, is_response_test, source_urls, is_dump_remove, is_match_template
from duplicate_removel import remove_dump_urls
from fetch import fetch_chs, fetch_chs_name
from match import match_chs
from response_test import test_resp_multi_thread, sorted_by_iptype
from save_as import save_chs_as_txt, save_chs_as_m3u, save_names_as_txt
import logging
import os

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..'))

logging.basicConfig(
    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S-%p',
    format='%(asctime)s ==> |  %(message)s',
    handlers=[logging.FileHandler(filename=f'{parent_path}/project.log', mode='w'), logging.StreamHandler()])


def main():
    chs = fetch_chs(source_urls)
    if is_dump_remove:
        chs = remove_dump_urls(chs)
    if is_match_template:
        chs = match_chs(chs)
    if is_response_test:
        chs = test_resp_multi_thread(chs, response_time)
    else:
        chs = sorted_by_iptype(chs)
    save_chs_as_txt(chs,iptype_filter=4)
    save_chs_as_m3u(chs,iptype_filter=4)


if __name__ == '__main__':
    main()



##  ---------获取各源中的频道名称-------------

    # chs_names = fetch_chs_name(['/home/uos/Desktop/rsv.txt'])
    # save_names_as_txt(chs_names,'all_names')
