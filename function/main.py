from function.config import response_time, is_response_test, source_urls, is_dump_remove, is_match_template
from function.duplicate_removel import remove_dump_urls
from function.fetch import fetch_chs, fetch_chs_name
from function.match import match_chs
from function.response_test import test_resp_multi_thread
from function.save_as import save_chs_as_txt, save_chs_as_m3u, save_names_as_txt

if __name__ == '__main__':
    chs = fetch_chs(source_urls)
    if is_dump_remove:
        chs = remove_dump_urls(chs)
    if is_match_template:
        chs = match_chs(chs)
    if is_response_test:
        chs = test_resp_multi_thread(chs, response_time)
    save_chs_as_txt(chs,)



##  ---------获取各源中的频道名称-------------


