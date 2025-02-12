import aiohttp
import asyncio
from datetime import datetime
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tqdm.asyncio import tqdm as async_tqdm
from tqdm import tqdm
from urllib.parse import urlparse


async def check_live_source(session, url, timeout=5):
    """快速检测单个直播源"""
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
    """带进度条的快速检测"""
    async with aiohttp.ClientSession() as session:
        tasks = [check_live_source(session, url) for url in urls]
        results = []
        for task in async_tqdm.as_completed(tasks, desc="🚀 快速筛选", unit="个"):
            results.append(await task)
        return results


def ffmpeg_test(item, test_duration=10):
    """FFmpeg深度检测"""
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


def extract_domain(url):
    """提取标准化域名"""
    try:
        parsed = urlparse(url)
        if parsed.scheme in ['rtmp', 'rtsp']:
            netloc = parsed.netloc.split('/')[0]
            return netloc.split(':')[0]
        return parsed.hostname.split(':')[0] if parsed.hostname else None
    except:
        return None


async def process_urls(url_list, test_duration=10):
    """
    主处理函数（新增延迟排序功能）
    :param url_list: 待检测的URL列表
    :param test_duration: FFmpeg检测时长(秒)
    :return: 排序后的域名列表（按最快响应时间）
    """
    # 第一阶段：快速检测
    fast_results = await fast_check(url_list)
    valid_sources = [res for res in fast_results if res['fast_check']]

    # 第二阶段：深度检测
    ffmpeg_results = []
    with ThreadPoolExecutor() as executor:
        tasks = [item for item in valid_sources]
        with tqdm(total=len(tasks), desc="🔍 深度检测", unit="个") as pbar:
            for result in executor.map(lambda x: ffmpeg_test(x, test_duration), tasks):
                ffmpeg_results.append(result)
                pbar.update(1)

    # 收集域名及其延迟数据
    domain_data = {}  # {域名: [延迟1, 延迟2, ...]}
    for item in ffmpeg_results:
        if item['ffmpeg_check'] and item['delay'] is not None:
            domain = extract_domain(item['url'])
            if domain:
                if domain not in domain_data:
                    domain_data[domain] = []
                domain_data[domain].append(item['delay'])

    # 按最快响应时间排序（主排序：最小延迟，次排序：域名）
    sorted_domains = sorted(
        domain_data.items(),
        key=lambda x: (min(x[1]), x[0])  # 先按最快延迟，再按字母排序
    )

    # 生成白名单文件
    if sorted_domains:
        formatted = "white_lst = [\n    " + ",\n    ".join(
            [f"'{domain}'" for domain, _ in sorted_domains]
        ) + "\n]"
    else:
        formatted = "white_lst = []"

    with open('white_lst.txt', 'w', encoding='utf-8') as f:
        f.write(formatted)

    return [domain for domain, _ in sorted_domains]


def print_results(results):
    # 结果展示
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





