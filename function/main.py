from config import response_time, is_response_test, source_urls, is_dump_remove, is_match_template
from duplicate_removel import remove_dump_urls
from fetch import fetch_chs, fetch_chs_name
from match import match_chs
from response_test import test_resp_multi_thread, sorted_by_iptype
from save_as import save_chs_as_txt, save_chs_as_m3u, save_names_as_txt

if __name__ == '__main__':
    chs = fetch_chs(source_urls)
    if is_dump_remove:
        chs = remove_dump_urls(chs)
    if is_match_template:
        chs = match_chs(chs)
    if is_response_test:
        chs = test_resp_multi_thread(chs, response_time)
    else:
        chs = sorted_by_iptype(chs)
    save_chs_as_txt(chs,)



##  ---------获取各源中的频道名称-------------

    # chs_names = fetch_chs_name(['https://cdn.jsdelivr.net/gh/Guovin/iptv-api@gd/output/result.m3u'])
    # save_names_as_txt(chs_names,'all_names')
