##配置文件

IS_MATCH_TEMPLATE = 1  # 是否匹配模板给定频道
IS_MATCH_LOCAL_CHS = 0  # 是否对字典中的地方频道进行匹配
IS_STABILITY_TEST = 0  # 是否对直播地址进行稳定测试
SORT_BY_V6_OR_V4 = 4  # 根据地址类型排序,IPV6在前值为6，IPV4在前值为4
DURATION_TIMEOUT = 20  # 对每个url拉流检测时间
SORT_BY_FPS_OR_SPEED = 'T'  # 白名单按fps、speed、firt_packet_time排序(F/S/T)
TEST_SAMPLES = ['CCTV-1 综合','天津卫视','河北卫视','凤凰卫视','北京卫视']
IS_KEEY_ONLY_WHITE_LST = 1  # 稳定性检测完成后，是否只保留白名单地址URLS



# 较为稳定白名单
white_lst_stable = [
    'ali-m-l.cztv.com', # 浙江频道
    # 'livestream-bt.nmtv.cn', # 内蒙频道
    'gxlive.snrtv.com', # 陕西频道
    # 'tv.pull.hebtv.com', # 河北频道
    'tencentplay.gztv.com', # 广州频道
    'nlive.zjkgdcs.com:8572', # zjk
    'nlive.zjkgdcs.com:8091', # zjk

    # '[2409:8087:1:20:20', # FMM
    # '148.135.93.213:81',  # 咪咕源


]

white_lst_manual = [

    'ldocctvwbcdbd.a.bdydns.com',   # F_TIME=0.36m
    'live.junhao.mil.cn',   # F_TIME=0.41m
    '110.7.131.146:9901',   # F_TIME=0.42m
    'stream.qhbtv.com',   # F_TIME=0.43m
    'tv.pull.hebtv.com',   # F_TIME=0.44m
    'cnpull.sccnfb.com',   # F_TIME=0.44m
    'ldocctvwbcdtxy.liveplay.myqcloud.com',   # F_TIME=0.46m
    'pulltv1.wanfudaluye.com',   # F_TIME=0.54m
    'play1-qk.nmtv.cn:80',   # F_TIME=0.54m
    '110.7.131.79:9901',   # F_TIME=0.55m
    'event.pull.hebtv.com',   # F_TIME=0.59m
    'tencentplaywebsite.gztv.com',   # F_TIME=0.64m
    'zhibo.hkstv.tv:80',   # F_TIME=0.69m
    '116.117.107.84:9901',   # F_TIME=0.71m
    'dtrmlive.qhdtrm.cn',   # F_TIME=0.72m
    'tencentplay.gztv.com',   # F_TIME=0.73m
    '116.117.104.248:9901',   # F_TIME=0.77m
    'hwapi.yntv.net',   # F_TIME=0.77m
    '113.195.13.154:9901',   # F_TIME=0.79m
    '112.27.145.212:9901',   # F_TIME=0.80m
    'livecdn.dmqhyadmin.com',   # F_TIME=0.80m
    'nlive.zjkgdcs.com:8091',   # F_TIME=0.82m
    '110.7.131.193:9901',   # F_TIME=0.83m
    'yncbn.ks-cdn.gitv.tv',   # F_TIME=0.83m
    '182.91.124.60:9901',   # F_TIME=0.84m
    'ali-m-l.cztv.com',   # F_TIME=0.85m
    'tencentplaygsm.gztv.com',   # F_TIME=0.87m
    '183.64.174.171:40123',   # F_TIME=0.89m
    '1.24.190.98:10080',   # F_TIME=0.91m
    'tp88.cn',   # F_TIME=0.91m
    '110.7.131.4:9901',   # F_TIME=0.94m
    'ali-m-l.cztv.com:80',   # F_TIME=0.94m
    '113.195.7.56:9901',   # F_TIME=0.97m
    '111.227.196.164:9901',   # F_TIME=0.97m
    'zzy789.xyz',   # F_TIME=0.97m
    'live.shaoxing.com.cn',   # F_TIME=0.98m
    '182.150.115.21:8030',   # F_TIME=1.03m
    'tc-tct.douyucdn2.cn',   # F_TIME=1.04m
    'ct-m-l.cztv.com',   # F_TIME=1.11m
    '101.65.34.130:9901',   # F_TIME=1.12m
    '124.93.18.237:9002',   # F_TIME=1.16m
    '116.117.104.34:9901',   # F_TIME=1.16m
    'zwebl02.cztv.com',   # F_TIME=1.20m
    'txmov2.a.kwimgs.com',   # F_TIME=1.21m
    '110.7.131.40:9901',   # F_TIME=1.23m
    '61.133.118.228:5001',   # F_TIME=1.23m
    'm3u8channel-yc.yunxya.com',   # F_TIME=1.23m
    '219.145.59.166:8888',   # F_TIME=1.25m
    '58.19.38.162:9901',   # F_TIME=1.28m
    'www.lysvc.cc',   # F_TIME=1.28m
    'local-live.jxtvcn.com.cn',   # F_TIME=1.29m
    '156.238.253.62:5555',   # F_TIME=1.31m
    '218.84.12.186:8001',   # F_TIME=1.32m
    '124.116.183.146:9901',   # F_TIME=1.34m
    'live.zohi.tv:80',   # F_TIME=1.34m
    '124.248.69.76:26781',   # F_TIME=1.34m
    'nlive.zjkgdcs.com:8572',   # F_TIME=1.35m
    'aa3.kkwk111.top',   # F_TIME=1.35m
    'hsplay-360.v.btime.com',   # F_TIME=1.44m
    'jwcdnqx.hebyun.com.cn',   # F_TIME=1.44m
    '139.203.180.9:90',   # F_TIME=1.44m
    'live.cztv.cc:85',   # F_TIME=1.45m
    'anren.live',   # F_TIME=1.46m
    'lmt.scqstv.com',   # F_TIME=1.51m
    'lxajh.top',   # F_TIME=1.55m
    '221.226.4.10:9901',   # F_TIME=1.57m
    '119.163.57.235:9901',   # F_TIME=1.59m
    'live.zohi.tv',   # F_TIME=1.60m
    '221.226.215.162:352',   # F_TIME=1.71m
    'zhibo.hkstv.tv',   # F_TIME=1.71m
    'tvbox6.icu',   # F_TIME=1.73m
    'live.jinchuanrmt.com:90',   # F_TIME=1.73m
    'gxlive.snrtv.com',   # F_TIME=1.78m
    'live.wjyanghu.com',   # F_TIME=1.79m
    '113.56.95.69:53765',   # F_TIME=1.80m
    '122.117.71.103:8574',   # F_TIME=1.80m
    'live.dxhmt.cn:9081',   # F_TIME=1.84m
    '222.128.55.152:9080',   # F_TIME=1.89m
    'ldncctvwbcdcnc.v.wscdns.com',   # F_TIME=1.91m
    '183.131.246.250:9901',   # F_TIME=2.05m
    'liveout.btzx.com.cn',   # F_TIME=2.05m
    '110.7.131.231:9901',   # F_TIME=2.16m
    '0472.org',   # F_TIME=2.25m
    '222.173.108.238:352',   # F_TIME=2.31m
    '113.200.148.203:85',   # F_TIME=2.41m
    '1.94.31.214',   # F_TIME=2.44m
    'nctv.top',   # F_TIME=2.45m
    '122.152.202.33',   # F_TIME=2.56m
    '112.123.243.37:50085',   # F_TIME=2.57m
    '123.138.22.30:9901',   # F_TIME=2.57m
    'liveout.xntv.tv',   # F_TIME=2.59m
    '162.62.120.19',   # F_TIME=2.65m
    '47.122.125.40:6666',   # F_TIME=2.97m
    '60.29.124.66:6080',   # F_TIME=3.42m
    'antvlive.ab5c6921.cdnviet.com',   # F_TIME=3.91m
    's1.abntelevision.com',   # F_TIME=4.00m
    'rthktv33-live.akamaized.net',   # F_TIME=4.55m
    'ikcdn01.ikzybf.com',   # F_TIME=4.60m
    '113.15.109.216:59901',   # F_TIME=4.61m
    'svipsvip.ffzyread1.com',   # F_TIME=5.04m
    'cdn5.163189.xyz',   # F_TIME=5.07m
    'cdn.163189.xyz',   # F_TIME=5.20m
    'ik6.iptv8.net:8888',   # F_TIME=5.89m
    'ycsj.aguihome.com:4022',   # F_TIME=6.02m
    '6666666.mghost.site',   # F_TIME=6.29m
    'cdn3.163189.xyz',   # F_TIME=6.71m
    'global.cgtn.cicc.media.caton.cloud',   # F_TIME=7.46m





]

black_lst = [
    '8.138.7.223',
    'www.freetv.top',
    'kkk.jjjj.jiduo.me',
    'stream1.freetv.fun',
    ':9901udp',
    'ali-m-l.cztv.com/channels/lantian/channel21/1080p.m3u8',
    '120.76.248.139',
    '公众号玉玉软件库',
    'zb.xmzb.xyz',
    '76.5432123.xyz',
    '218.93.208.172:35455',
    'jwplay.hebyun.com.cn',
    '150.158.112.123',
    'live-hls-web-ajb.getaj.net',
    'tvbox6.icu',
    'ku9.3n.cc',



]

source_urls0 = [

    # 'https://iptv.b2og.com/txt/fmml_ipv6.txt',

]

source_urls = [

    'https://raw.githubusercontent.com/Johnisonn/lives/main/live.txt',
    'https://raw.githubusercontent.com/Johnisonn/tvbox/main/Garter/live.txt',

    'https://live.izbds.com/tv/iptv4.txt', # live.izbds.com
    'https://live.zbds.top/tv/iptv6.m3u',
    'https://live.izbds.com/tv/iptv6.txt',
    'https://live.kilvn.com/iptv.m3u',
    'https://live.hacks.tools/tv/iptv4.txt',
    'http://124.71.189.194/zb.txt',
    'http://8.138.7.223/live.txt',
    'http://cqitv.fh4u.org/iptv/jiangsu.txt',
    "http://cqitv.fh4u.org/iptv/20241126/gitv.txt",  # 本地址引发的BUG已修复，地址中无分类引发判断错误，V4
    "http://meowtv.top/zb",  # 喵TV
    "https://tv.youdu.fan:666/live/",  # 可用，V4酒店源
    "http://rihou.cc:567/gggg.nzk",  # 日后线路
    "http://rihou.cc:555/gggg.nzk",  # 日后线路
    "http://kv.netsite.cc/tvlive",
    "http://ww.weidonglong.com/dsj.txt",  # WMDZ源，V4
    "http://xhztv.top/zbc.txt",  # 可用 有字节码\ufeff开头，V4

    'https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u', # FMM
    'https://raw.githubusercontent.com/Kimentanm/aptv/refs/heads/master/m3u/iptv.m3u',
    "https://raw.githubusercontent.com/Guovin/iptv-api/gd/output/result.m3u",  # guovin 每日更新
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
    'https://raw.githubusercontent.com/Moexin/IPTV/Files/IPTV.m3u'

    # "https://raw.githubusercontent.com/lystv/short/main/影视/tvb/MTV.txt", #MTV
    # "https://raw.githubusercontent.com/Ftindy/IPTV-URL/main/douyuyqk.m3u", #斗鱼视频




]

mirror_url_lst = [
    'https://github.moeyy.xyz/',
    'https://ghproxy.cfd/',
    'https://gh-proxy.com/',
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