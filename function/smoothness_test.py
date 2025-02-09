import cv2
import sys
from urllib.parse import urlparse
import requests


def test_stream_playability(url, num_frames=10):
    try:
        cap = cv2.VideoCapture(url)
        if cap.isOpened():
            success_count = 0
            for _ in range(num_frames):
                ret, _ = cap.read()
                if ret:
                    success_count += 1
            cap.release()
            # 可根据实际情况调整判断阈值
            return success_count / num_frames >= 0.8
    except Exception:
        pass
    return False


def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def filter_stable_live_sources(live_sources):
    stable_domains = set()
    total_sources = len(live_sources)
    for i, url in enumerate(live_sources, start=1):
        # 计算并显示整体进度
        progress = (i / total_sources) * 100
        sys.stdout.write(f"\r正在筛选直播源，已处理 {i} 个，总进度: {progress:.2f}%")
        sys.stdout.flush()

        if test_stream_playability(url):
            domain = get_domain(url)
            stable_domains.add(domain)
    sys.stdout.write("\n")
    return stable_domains

resp = requests.get('https://github.moeyy.xyz/https://raw.githubusercontent.com/Johnisonn/lives/main/live.txt')
resp.encoding = 'utf-8'
lines = resp.text.split('\n')

'''
with open('/home/uos/Desktop/chs.txt', 'r') as file:
    lines = file.readlines()
'''

live_sources = []
for line in lines:
    if '北京卫视' in line:
        line = line.strip()
        line = line.split(',')[1]
        line = line.split('$')[0]
        live_sources.append(line)

# 筛选稳定的直播源域名
stable_domains = filter_stable_live_sources(live_sources)
print("稳定的直播源域名白名单:", stable_domains)



