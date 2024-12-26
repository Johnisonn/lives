本项目可实现对给定网络直播源地址中直播源的自动获取，并生成直播源文件（txt和m3u）

项目大致分为以下几个功能模块：
1.抓取功能
2.去重功能
3.匹配功能
4.保存功能

另外，为方便各项功能更好发挥作用，加入了以下模块：
1.频道规范命名
2.响应检测
3.频道字典

以下为频道字典结构：
dict = OrderedDict({
    'cate1':OrderedDict({
        'name1':['u1','u2','u3','u4'],
        'name2':['u21','u22','u23']
    }),
    'cate2':OrderedDict({
        'name3':['u31','u32','u33','u34'],
        'name4':['u41','u42']
    }),
    'cate3':OrderedDict({
        'name5':['u51','u52','u53','u54','u55'],
        'name6':['u61']
    }),
    'cate4':OrderedDict({
        'name7':['u71','u72']
    }),
    'cate5':OrderedDict({
        'name8':['u81']
    })
})