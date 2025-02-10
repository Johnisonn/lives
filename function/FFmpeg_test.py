import aiohttp
import asyncio
from datetime import datetime
import subprocess
from concurrent.futures import ThreadPoolExecutor
import requests
from tqdm.asyncio import tqdm as async_tqdm
from tqdm import tqdm
from urllib.parse import urlparse
import json


# 第一阶段：带进度条的异步快速检测
async def check_live_source(session, url, timeout=5):
    try:
        start = datetime.now()
        async with session.get(url, timeout=timeout) as resp:
            if resp.status == 200:
                await resp.content.read(1024)
                delay = (datetime.now() - start).total_seconds()
                return {"url": url, "delay": delay, "fast_check": True}
            return {"url": url, "delay": None, "fast_check": False}
    except Exception:
        return {"url": url, "delay": None, "fast_check": False}


async def fast_check(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [check_live_source(session, url) for url in urls]
        results = []
        # 使用异步进度条
        for task in async_tqdm.as_completed(tasks, desc="🚀 快速筛选", unit="个"):
            results.append(await task)
        return results


# 第二阶段：带进度条的FFmpeg检测
def ffmpeg_test(item, test_duration=10):
    command = [
        'ffmpeg',
        '-i', item['url'],
        '-t', str(test_duration),
        '-c', 'copy',
        '-f', 'null',
        '-loglevel', 'error',
        '-'
    ]
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=test_duration + 5
        )
        return {**item, 'ffmpeg_check': result.returncode == 0}
    except subprocess.TimeoutExpired:
        return {**item, 'ffmpeg_check': False}


# 域名提取函数
def extract_domain(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme in ['rtmp', 'rtsp']:
            # 处理特殊流媒体协议格式
            netloc = parsed.netloc.split('/')[0]
            return netloc.split(':')[0]
        return parsed.hostname.split(':')[0] if parsed.hostname else None
    except:
        return None


# 主检测流程
async def main(urls, test_duration=10):
    # 快速筛选
    fast_results = await fast_check(urls)
    valid_sources = [res for res in fast_results if res['fast_check']]

    # 深度检测
    ffmpeg_results = []
    with ThreadPoolExecutor() as executor:
        # 使用线程池+进度条
        tasks = [item for item in valid_sources]
        with tqdm(total=len(tasks), desc="🔍 深度检测", unit="个") as pbar:
            for result in executor.map(lambda x: ffmpeg_test(x, test_duration), tasks):
                ffmpeg_results.append(result)
                pbar.update(1)

    # 合并最终结果
    final_results = []
    domain_whitelist = set()

    for result in fast_results:
        ffmpeg_res = next(
            (x for x in ffmpeg_results if x['url'] == result['url']),
            {'ffmpeg_check': False}
        )
        final_item = {
            **result,
            'ffmpeg_check': ffmpeg_res['ffmpeg_check']
        }
        final_results.append(final_item)

        # 收集白名单域名
        if final_item['ffmpeg_check']:
            domain = extract_domain(final_item['url'])
            if domain:
                domain_whitelist.add(domain)

    # 保存白名单
    with open('whitelist.txt', 'w') as f:
        f.write("\n".join(sorted(domain_whitelist)))

    return final_results


# 改进的结果展示
def print_results(results):
    print("\n📊 检测结果汇总：")
    headers = ["URL", "延迟", "快速", "流畅", "域名"]
    row_format = "{:<40} | {:<6} | {:<4} | {:<4} | {:<20}"
    print(row_format.format(*headers))
    print("-" * 85)

    for res in results:
        domain = extract_domain(res['url']) or "N/A"
        print(row_format.format(
            res['url'][:40],
            f"{res['delay']:.2f}s" if res['delay'] else "超时",
            '✓' if res['fast_check'] else '✗',
            '✓' if res['ffmpeg_check'] else '✗',
            domain[:20]
        ))


if __name__ == "__main__":

    resp = requests.get('https://github.moeyy.xyz/https://raw.githubusercontent.com/Johnisonn/lives/main/live.txt')
    resp.encoding = 'utf-8'
    lines = resp.text.split('\n')
    '''
    with open('/home/uos/Desktop/chs.txt', 'r') as file:
        lines = file.readlines()
    '''
    test_urls = []
    for line in lines:
        if '河北卫视' in line:
            line = line.strip()
            line = line.split(',')[1]
            line = line.split('$')[0]
            test_urls.append(line)


    final_results = asyncio.run(main(test_urls))
    print_results(final_results)

    # 显示白名单
    with open('whitelist.txt') as f:
        print("\n🎉 域名白名单：")
        print(f.read())

# 依赖安装：
# pip install aiohttp tqdm