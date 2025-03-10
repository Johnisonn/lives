##配置文件

is_dump_remove = 1 # 是否对采集到的地址进行去重
is_match_template = 1 # 是否匹配模板给定频道
is_match_local_chs = 0 # 是否对字典中的地方频道进行匹配
is_stability_test = 0  # 是否对直播地址测试响应时间

response_time = 300  # 设置筛选直播源url的响应时间，单位毫秒
v6_or_v4 = 4  # 根据地址类型排序,IPV6在前值为6，IPV4在前值为4


mirror_url_lst = [
    'https://github.moeyy.xyz/',
    'https://ghproxy.cfd/',
    'https://hub.gitmirror.com/',
    # 'https://ghgo.xyz/',
    'https://ghfast.top/',
    'https://gh.ddlc.top/',
    'https://ghproxy.net/',
    'https://gh.api.99988866.xyz/',

]
mirror = mirror_url_lst[0]
white_lst = [

    '148.135.93.213', # 咪咕源
    '211.101.234.24:866/aishang/sxg',
    '211.101.234.24:866/aishang/migu',
    'gxlive.snrtv.com',
    'livestream-bt.nmtv.cn',
    '36.105.100.208',
    '182.91.124.224',
    '110.7.131.146',
    '110.7.131.40',
    '101.66.198.2',

    '123.113.13.18',
    '58.243.224.244',
    '183.3.134.56',
    '123.138.22.30',
    '180.158.201.25',
    '112.234.21.153',
    '180.140.153.35',
    '120.234.5.29',
    '116.128.242.83',
    '1.180.2.93',
    '218.58.136.82',
    '125.82.168.238',
    '218.29.168.146',
    'home.wwang.pw',
    '60.29.124.66',
    '124.93.18.238',
    'rthktv33-live.akamaized.net',
    '119.32.12.17',
    'api.dbkan.cdn.iptv.xin',
    '61.138.128.226',
    '76.5432123.xyz',
    'drive.mxmy.net'
    
    
    
    '221.2.148.205',
    '8.138.7.223',
    '60.172.130.146',
    '183.191.145.219',
    '220.170.241.204',
    '175.171.30.26',
    '182.91.124.60',
    '110.7.131.4',
    '110.7.131.231',
    '183.215.211.219',
    '222.169.85.8',
    '218.93.208.172'


]

source_urls_0 = [

   # 'http://cqitv.fh4u.org/iptv/jiangsu.txt',
   # 'https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u',
   # 'https://live.kilvn.com/iptv.m3u',
   #  'https://raw.githubusercontent.com/SPX372928/MyIPTV/master/黑龙江PLTV移动CDN版.txt',
   #  "https://raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.m3u",
   #  'https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u',
   #  "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/hd.txt",  # 每日更新，条目较多
   #  'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.m3u',
   #  'https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u',
   #  "https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt",  # 每日更新，条目较多
   #  "http://rihou.cc:567/gggg.nzk",  # 日后线路
   #  "http://meowtv.top/zb", # 喵TV
   #  "https://live.zhoujie218.top/tv/iptv6.txt",  # 可用
   #  "https://live.zhoujie218.top/tv/iptv4.txt",  # 可用
   #  'http://211.101.234.24:866/kxzb.txt', # 开心直播，同 http://211.101.234.24:866/qiyu.php?url=c
   #  'http://211.101.234.24:866/aishang.txt',
   #  'https://raw.githubusercontent.com/lizongying/my-tv-0/main/app/src/main/res/raw/mobile.txt',
   #  'https://raw.githubusercontent.com/lizongying/my-tv-0/main/app/src/main/res/raw/channels.txt',
   #  'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv4.m3u',
   #  'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv4_2.m3u',

    'https://cdn.jsdelivr.net/gh/Johnisonn/tvbox@main/Garter/live.txt'
    # 'https://raw.githubusercontent.com/Johnisonn/tvbox/main/Garter/live.txt',


]



#直播源地址列表
source_urls = [
    # "https://github.com/Johnisonn/tvbox/raw/main/Garter/live.txt",
    'https://raw.githubusercontent.com/Johnisonn/tvbox/main/Garter/live.txt',
    'https://iptv.b2og.com/txt/fmml_ipv6.txt',

    'https://gitee.com/zhang-station1/genius-film-and-television/raw/master/3658',
    'http://8.138.7.223/live.txt',
    'http://cqitv.fh4u.org/iptv/jiangsu.txt',
    'https://live.kilvn.com/iptv.m3u',

    'http://211.101.234.24:866/kxzb.txt', # 开心直播，同 http://211.101.234.24:866/qiyu.php?url=c
    'http://211.101.234.24:866/aishang.txt', # 爱尚直播，同 http://211.101.234.24:866/qiyu.php?url=a

    # 'https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u',
    'https://cdn.jsdelivr.net/gh/fanmingming/live@main/tv/m3u/ipv6.m3u',
    # 'https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/itv.m3u',
    'https://cdn.jsdelivr.net/gh/fanmingming/live@main/tv/m3u/itv.m3u',


    "https://cdn.jsdelivr.net/gh/Guovin/iptv-api@gd/output/result.m3u", #guovin 每日更新
    # "https://raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.m3u",

    'https://raw.githubusercontent.com/SPX372928/MyIPTV/master/黑龙江PLTV移动CDN版.txt',
    'https://raw.githubusercontent.com/SPX372928/MyIPTV/master/山东SNM移动CDN版.txt',

    # "https://cdn.jsdelivr.net/gh/YueChan/live@main/IPTV.m3u", #可用
    'https://raw.githubusercontent.com/YueChan/Live/main/APTV.m3u',
    # 'https://raw.githubusercontent.com/YueChan/Live/main/Global.m3u',
    # 'https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u',


    "https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.m3u",  # 每日更新

    "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/hd.txt", #每日更新，条目较多
    'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.m3u',


    # 'https://raw.githubusercontent.com/lizongying/my-tv-0/main/app/src/main/res/raw/mobile.txt',
    # 'https://raw.githubusercontent.com/lizongying/my-tv-0/main/app/src/main/res/raw/channels.txt',

    'https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u',
    "https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt", #每日更新，条目较多


    # 'https://raw.githubusercontent.com/joevess/IPTV/main/sources/iptv_sources.m3u',
    # 'https://raw.githubusercontent.com/joevess/IPTV/main/sources/home_sources.m3u',


    'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv4.m3u',
    'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv4_2.m3u',
    'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv6.m3u',
    # 'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv6_2.m3u',

    'https://raw.githubusercontent.com/huang770101/my-iptv/main/IPTV-ipv4.m3u',
    # 'https://raw.githubusercontent.com/huang770101/my-iptv/main/IPTV-ipv6.m3u',

    'https://raw.githubusercontent.com/zbefine/iptv/main/iptv.m3u',
    # 'https://raw.githubusercontent.com/BurningC4/Chinese-IPTV/master/TV-IPV4.m3u',
    'https://raw.githubusercontent.com/9527xiao9527/iptv/main/iptv.txt',
    'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.m3u',
    "https://raw.githubusercontent.com/dxawi/0/main/tvlive.txt",
    "https://raw.githubusercontent.com/qingwen07/awesome-iptv/main/tvbox_live_all.txt", #可用，条目较多
    "https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt", #可用
    "https://github.com/Moexin/IPTV/raw/Files/IPTV.m3u",


    'https://live.zbds.top/tv/iptv6.m3u',
    'http://175.178.251.183:6689/live.m3u',
    "http://meowtv.top/zb", # 喵TV
    # "https://live.zhoujie218.top/tv/iptv6.txt", #可用
    "https://live.zhoujie218.top/tv/iptv4.txt", #可用
    "https://tv.youdu.fan:666/live/", #可用，V4酒店源
    "http://home.jundie.top:81/Cat/tv/live.txt",  # 可用，俊佬线路
    # "http://rihou.cc:567/gggg.nzk",  # 日后线路
    "http://rihou.cc:555/gggg.nzk",  # 日后线路
    "http://kv.netsite.cc/tvlive",
    "https://fm1077.serv00.net/SmartTV.m3u",
    "http://ww.weidonglong.com/dsj.txt", # WMDZ源，V4
    "http://cqitv.fh4u.org/iptv/20241126/gitv.txt", # 本地址引发的BUG已修复，地址中无分类引发判断错误，V4
    "http://xhztv.top/zbc.txt", #可用 有字节码\ufeff开头，V4


    # "https://raw.githubusercontent.com/lystv/short/main/影视/tvb/MTV.txt", #MTV
    # "https://raw.githubusercontent.com/Ftindy/IPTV-URL/main/douyuyqk.m3u", #斗鱼视频
    # "http://175.178.251.183:6689/aktvlive.txt", #可用，港澳外台
    # "https://raw.githubusercontent.com/cymz6/AutoIPTV-Hotel/main/lives.txt", #已弃，空分类
    # "https://raw.githubusercontent.com/PizazzGY/TVBox_warehouse/main/live.txt", #仅一组



]

# 对网段地址设置黑名单，待开发...
black_list = []



epg_urls = [
    "https://live.fanmingming.cn/e.xml",
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
