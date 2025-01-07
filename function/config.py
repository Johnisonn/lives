##配置文件

is_match_template = True # 是否匹配模板给定频道
is_response_test = True  # 是否对直播地址测试响应时间
is_dump_remove = True # 是否对采集到的地址进行去重
response_time = 300  # 设置筛选直播源url的响应时间，单位毫秒
v6_or_v4 = 6  # 根据地址类型排序,IPV6在前值为6，IPV4在前值为4
is_match_local_chs = 0 # 是否对字典中的地方频道进行匹配

mirror_url = [
    'https://ghproxy.cn/',
    'https://ghproxy.cc/',
    'https://hub.gitmirror.com/',
    'https://github.moeyy.xyz/',
    'https://ghgo.xyz',

]
#直播源地址列表
source_urls = [
    "https://github.moeyy.xyz/https://github.com/Johnisonn/tvbox/raw/main/Garter/live.txt",

    # "https://live.fanmingming.cn/tv/m3u/ipv6.m3u",  # 范明明
    "https://github.site/fanmingming/live/raw/main/tv/m3u/ipv6.m3u",

    "https://cdn.jsdelivr.net/gh/Guovin/iptv-api@gd/output/result.m3u", #guovin 每日更新
    # "https://ghgo.xyz/raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.m3u",

    "https://cdn.jsdelivr.net/gh/YueChan/live@main/IPTV.m3u", #可用
    # "https://github.moeyy.xyz/https://github.com/YueChan/Live/raw/main/IPTV.m3u",

    "https://github.moeyy.xyz/https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.m3u",  # 每日更新
    "https://github.moeyy.xyz/https://raw.githubusercontent.com/vbskycn/iptv/master/tv/hd.txt", #每日更新，条目较多
    "https://github.moeyy.xyz/https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt", #每日更新，条目较多

    "http://meowtv.top/zb", # 喵TV
    "https://github.moeyy.xyz/https://github.com/Moexin/IPTV/raw/Files/IPTV.m3u",
    "https://github.moeyy.xyz/https://github.com/YanG-1989/m3u/raw/main/Gather.m3u",
    "https://github.moeyy.xyz/https://github.com/joevess/IPTV/raw/main/home.m3u8",
    "https://ghgo.xyz/raw.githubusercontent.com/dxawi/0/main/tvlive.txt",

    "https://live.zhoujie218.top/tv/iptv6.txt", #可用
    "https://live.zhoujie218.top/tv/iptv4.txt", #可用
    "https://tv.youdu.fan:666/live/", #可用，V4酒店源
    "http://home.jundie.top:81/Cat/tv/live.txt",  # 可用，俊佬线路
    "http://rihou.cc:567/gggg.nzk",  # 日后线路
    "http://rihou.cc:555/gggg.nzk",  # 日后线路
    "http://kv.netsite.cc/tvlive",
    "https://fm1077.serv00.net/SmartTV.m3u",
    "http://ww.weidonglong.com/dsj.txt", # WMDZ源，V4
    "https://github.moeyy.xyz/https://raw.githubusercontent.com/qingwen07/awesome-iptv/main/tvbox_live_all.txt", #可用，条目较多
    "https://github.moeyy.xyz/https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt", #可用
    "http://cqitv.fh4u.org/iptv/20241126/gitv.txt", # 本地址引发的BUG已修复，地址中无分类引发判断错误，V4
    "http://xhztv.top/zbc.txt", #可用 有字节码\ufeff开头，V4


    # "https://github.moeyy.xyz/https://raw.githubusercontent.com/lystv/short/main/影视/tvb/MTV.txt", #MTV
    # "https://github.moeyy.xyz/https://raw.githubusercontent.com/Ftindy/IPTV-URL/main/douyuyqk.m3u", #斗鱼视频
    # "http://175.178.251.183:6689/aktvlive.txt", #可用，港澳外台
    # "https://github.moeyy.xyz/https://raw.githubusercontent.com/cymz6/AutoIPTV-Hotel/main/lives.txt", #已弃，空分类
    "https://github.moeyy.xyz/https://raw.githubusercontent.com/PizazzGY/TVBox_warehouse/main/live.txt", #仅一组



    # "/home/uos/Desktop/live_sources/gggg.nzk", #测试本地

]

# 对网段地址设置黑名单，待开发...
black_list = []

epg_urls = [
    "https://live.fanmingming.com/e.xml",
    "http://epg.51zmt.top:8000/e.xml",
    "http://epg.aptvapp.com/xml",
    "https://epg.pw/xmltv/epg_CN.xml",
    "https://epg.pw/xmltv/epg_HK.xml",
    "https://epg.pw/xmltv/epg_TW.xml"
]

# 文件头信息
head_info = {'cate':'★更新日期★',
             'tvg-logo':'https://live.fanmingming.cn/tv/之江纪录.png',
             'url':'https://ali-m-l.cztv.com/channels/lantian/channel012/1080p.m3u8'}
