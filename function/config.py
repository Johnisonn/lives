##配置文件

IS_MATCH_TEMPLATE = 1  # 是否匹配模板给定频道
IS_MATCH_LOCAL_CHS = 0  # 是否对字典中的地方频道进行匹配
IS_STABILITY_TEST = 1  # 是否对直播地址进行稳定测试
SORT_BY_V6_OR_V4 = 4  # 根据地址类型排序,IPV6在前值为6，IPV4在前值为4
DURATION_TIMEOUT = 30  # 检测每个url流畅性时间
SORT_BY_FPS_OR_SPEED = 'F'  # 白名单按fps或speed排序
TEST_SAMPLES = ['CCTV-1 综合','天津卫视','河北卫视','凤凰卫视','北京卫视']
IS_KEEY_ONLY_WHITE_LST = 1  # 稳定性检测完成后，是否只保留白名单地址URLS



# 较为稳定白名单
white_lst_stable = [
    'ali-m-l.cztv.com', # 浙江频道
    'livestream-bt.nmtv.cn', # 内蒙频道
    'gxlive.snrtv.com', # 陕西频道
    'tv.pull.hebtv.com', # 河北频道
    'tencentplay.gztv.com', # 广州频道

    # '[2409:8087:1:20:20', # FMM
    '148.135.93.213:81',  # 咪咕源


]

white_lst_manual = [

    '[2409:8087:1:20:20',
    '148.135.93.213',  # 咪咕源
    'ali-m-l.cztv.com',  # 浙江频道
    'livestream-bt.nmtv.cn',  # 内蒙频道
    'tv.pull.hebtv.com',  # 57.50fps

    'api.olelive.com',  # 175.75fps
    'rthktv33-live.akamaized.net',  # 149.40fps
    'jwplay.hebyun.com.cn',  # 122.57fps
    'cdn5.163189.xyz',  # 93.67fps
    'php.jdshipin.com',  # 86.50fps
    '39.164.180.36:19901',  # 85.00fps
    'php.jdshipin.com:8880',  # 83.44fps
    'goo.bkpcp.top',  # 71.60fps
    'ttkx.cc:1658',  # 62.20fps
    '36.40.236.13:9999',  # 54.00fps
    '110.7.131.193:9901',  # 34.67fps
    '110.7.131.4:9901',  # 34.67fps
    '116.117.104.248:9901',  # 34.67fps
    '110.7.131.79:9901',  # 34.33fps
    '116.117.107.84:9901',  # 34.33fps


    'z.b.bkpcp.top',  # 3544kbps
    'tv.20191209.xyz',  # 3498kbps
    '218.93.208.172',  # 288.75fps
    'tvbox6.icu',  # 82.00fps
    '125.82.171.210',  # 46.00fps





]

black_lst = [
    '8.138.7.223',
    'www.freetv.top',
    'kkk.jjjj.jiduo.me',
    'stream1.freetv.fun',
    ':9901udp',

]

source_urls0 = [

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

    # 'https://cdn.jsdelivr.net/gh/Johnisonn/tvbox@main/Garter/live.txt',
    # 'https://cdn.jsdelivr.net/gh/Johnisonn/lives@main/live.txt',
    # 'https://raw.githubusercontent.com/Johnisonn/lives/main/live.txt',
    # 'https://raw.githubusercontent.com/Johnisonn/tvbox/main/Garter/live.txt',
    # 'https://iptv.b2og.com/txt/fmml_ipv6.txt',
    # 'https://live.izbds.com/tv/iptv4.txt', # live.izbds.com
    # "https://github.com/Johnisonn/tvbox/raw/main/Garter/live.txt",
    # 'https://iptv.b2og.com/txt/fmml_ipv6.txt',
    # test
    # 'https://raw.githubusercontent.com/lizongying/my-tv-0/main/app/src/main/res/raw/mobile.txt',
    # 'https://raw.githubusercontent.com/lizongying/my-tv-0/main/app/src/main/res/raw/channels.txt',

]

source_urls = [

    'https://raw.githubusercontent.com/Johnisonn/lives/main/live.txt',
    'https://raw.githubusercontent.com/Johnisonn/tvbox/main/Garter/live.txt',

    'https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u', # FMM
    "https://raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.m3u",  # guovin 每日更新
    'https://live.izbds.com/tv/iptv4.txt', # live.izbds.com
    'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/%E4%B8%93%E5%8C%BA/%E2%99%AA%E4%BC%98%E8%B4%A8%E5%A4%AE%E8%A7%86.txt',
    'https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/%E4%B8%93%E5%8C%BA/%E2%99%AA%E4%BC%98%E8%B4%A8%E5%8D%AB%E8%A7%86.txt',
    "https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt",  # 每日更新，条目较多
    'https://raw.githubusercontent.com/SPX372928/MyIPTV/master/黑龙江PLTV移动CDN版.txt',
    'https://raw.githubusercontent.com/SPX372928/MyIPTV/master/山东SNM移动CDN版.txt',
    "https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.m3u",  # 每日更新
    "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/hd.txt",  # 每日更新，条目较多
    'https://raw.githubusercontent.com/vbskycn/iptv/master/tv/iptv4.m3u',
    'https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u',
    'https://raw.githubusercontent.com/joevess/IPTV/main/sources/iptv_sources.m3u',
    'https://raw.githubusercontent.com/joevess/IPTV/main/sources/home_sources.m3u',
    'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv4.m3u',
    'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv4_2.m3u',
    'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv6.m3u',
    'https://raw.githubusercontent.com/jisoypub/iptv/main/ipv6_2.m3u',
    'https://raw.githubusercontent.com/huang770101/my-iptv/main/IPTV-ipv4.m3u',
    'https://raw.githubusercontent.com/huang770101/my-iptv/main/IPTV-ipv6.m3u',
    'https://raw.githubusercontent.com/zbefine/iptv/main/iptv.m3u',
    'https://raw.githubusercontent.com/BurningC4/Chinese-IPTV/master/TV-IPV4.m3u',
    'https://raw.githubusercontent.com/9527xiao9527/iptv/main/iptv.txt',
    'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.m3u',
    "https://raw.githubusercontent.com/dxawi/0/main/tvlive.txt",
    "https://raw.githubusercontent.com/qingwen07/awesome-iptv/main/tvbox_live_all.txt",  # 可用，条目较多
    "https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt",  # 可用
    "https://github.com/Moexin/IPTV/raw/Files/IPTV.m3u",
    'https://gitee.com/zhang-station1/genius-film-and-television/raw/master/3658',
    'http://8.138.7.223/live.txt',
    'http://cqitv.fh4u.org/iptv/jiangsu.txt',
    'https://live.kilvn.com/iptv.m3u',
    'https://live.zbds.top/tv/iptv6.m3u',
    'http://175.178.251.183:6689/live.m3u',
    "http://meowtv.top/zb", # 喵TV
    "https://live.zhoujie218.top/tv/iptv6.txt", #可用
    "https://live.zhoujie218.top/tv/iptv4.txt", #可用
    "https://tv.youdu.fan:666/live/", #可用，V4酒店源
    "http://rihou.cc:567/gggg.nzk",  # 日后线路
    "http://rihou.cc:555/gggg.nzk",  # 日后线路
    "http://kv.netsite.cc/tvlive",
    "http://ww.weidonglong.com/dsj.txt", # WMDZ源，V4
    "http://cqitv.fh4u.org/iptv/20241126/gitv.txt", # 本地址引发的BUG已修复，地址中无分类引发判断错误，V4
    "http://xhztv.top/zbc.txt", #可用 有字节码\ufeff开头，V4
    "https://raw.githubusercontent.com/lystv/short/main/影视/tvb/MTV.txt", #MTV
    "https://raw.githubusercontent.com/Ftindy/IPTV-URL/main/douyuyqk.m3u", #斗鱼视频
    "https://raw.githubusercontent.com/cymz6/AutoIPTV-Hotel/main/lives.txt", #已弃，空分类
    "https://raw.githubusercontent.com/PizazzGY/TVBox_warehouse/main/live.txt", #仅一组



]

mirror_url_lst = [
    'https://github.moeyy.xyz/',
    'https://ghproxy.cfd/',
    'https://hub.gitmirror.com/',
    'https://ghfast.top/',
    'https://gh.ddlc.top/',
    'https://ghproxy.net/',
    'https://gh.api.99988866.xyz/',

]

head_info = {'cate':'★更新日期★',
             'tvg-logo':'https://live.fanmingming.cn/tv/之江纪录.png',
             'url':'https://ali-m-l.cztv.com/channels/lantian/channel012/1080p.m3u8'}

epg_urls = [
    "https://live.fanmingming.cn/e.xml",
    "http://epg.51zmt.top:8000/e.xml",
    "http://epg.aptvapp.com/xml",
    "https://epg.pw/xmltv/epg_CN.xml",
    # "https://epg.pw/xmltv/epg_HK.xml",
    # "https://epg.pw/xmltv/epg_TW.xml"
]