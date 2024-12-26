from function.config import response_time, is_response_test, source_urls, is_dump_remove, is_match_template
from function.duplicate_removel import remove_dump_urls
from function.fetch import fetch_multi_urls_chs, fetch_chs_name, fetch_single_url_chs
from function.match import match_chs
from function.response_test import test_resp_multi_thread
from function.save_as import save_chs_as_txt, save_chs_as_m3u, save_names_as_txt

if __name__ == '__main__':
    # chs = fetch_multi_urls_chs(source_urls)
    # if is_dump_remove:
    #     chs = remove_dump_urls(chs)
    # if is_match_template:
    #     chs = match_chs(chs)
    # if is_response_test:
    #     chs = test_resp_multi_thread(chs, response_time)
    # save_chs_as_txt(chs,)
    #
    #

##  ---------获取各源中的频道名称-------------


    names = fetch_chs_name(['/home/uos/Desktop/666.txt'])
    save_names_as_txt(names,'去重测试')



    # chs = fetch_single_url_chs('/home/uos/Desktop/666.txt')
    # chs = remove_dump_urls(chs)
    # chs = match_chs(chs)
    # save_chs_as_txt(chs,'test666')