from UI.ui_class import ConfigUi
from function.config import source_urls
from function.duplicate_removel import remove_dump_urls
from function.fetch import fetch_multi_urls_chs, fetch_chs_name
from function.match import match_chs
from function.sort import test_resp_multi_thread
from function.save_as import save_chs_as_txt, save_names_as_txt

cfg = ConfigUi()
cfg.main_win()

# chs = fetch_multi_urls_chs(cfg.selected_urls)
# if cfg.is_dump_remove:
#     chs = remove_dump_urls(chs)
# if cfg.is_match_template:
#     chs = match_chs(chs)
# if cfg.is_response_test:
#     chs = test_resp_multi_thread(chs, cfg.response_time)
# save_chs_as_txt(chs, cfg.save_name)

##  ---------获取各源中的频道名称-------------

names = fetch_chs_name(cfg.selected_urls)
save_names_as_txt(names)