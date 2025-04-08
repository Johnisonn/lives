import select
import subprocess
import re
import os
import datetime
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from config import white_lst_stable, DURATION_TIMEOUT
import logging
logger = logging.getLogger(__name__)

# 预编译正则表达式
FPS_SPEED_RE = re.compile(r'frame=\s*\d+\s*fps=([\s\d.]+).*speed=\s*([\d.]+)x')
ERROR_PATTERNS = {
    'Connection_timeout': r'Connection timed out',  # 连接超时
    'Connection_refused': r'Connection refused',  # 连接被拒绝
    'Http_error': r'HTTP error',  # HTTP错误
    'Stream_premature_end': r'Stream ends prematurely',  # 流提前结束
    'Packet_corrupt': r'Packet corrupt',  # 数据包损坏
    'Invalid_data': r'Invalid data found',  # 无效数据
    'Buffer_exhausted': r'buffer exhausted',  # 缓冲区耗尽
    'Frame_corrupt': r'corrupt decoded frame',  # 解码帧损坏
    'IO_error': r'Input/output error',  # 输入输出错误

    'repeated_errors': r'Last message repeated',
    'decode_error': r'decode_slice_header error',
    'concealing_errors': r'concealing .* errors',

}
# 编译错误正则表达式
ERROR_REGEX = re.compile(
    '|'.join(f'({pattern})' for pattern in ERROR_PATTERNS.values()),
    flags=re.IGNORECASE
)
ERROR_KEYS = list(ERROR_PATTERNS.keys())

# 抽取url中关键字作为后续白名单
def extract_keyword(url: str):
    if '://' in url:
        keyword = url.split('//')[1]
        keyword = keyword.split('::')[0] if '[' in keyword else keyword.split('/')[0]
        # print(keyword)
    else:
        print(f'此url较特殊：-------------------------------------------------url={url}')
        return None
    return keyword

# 用FFmpeg检测流畅性
def analyze_stream(url: str, duration_timeout=DURATION_TIMEOUT):
    command = [
        'ffmpeg',
        '-hide_banner',
        '-v', 'info',
        '-t', str(duration_timeout),
        '-timeout', '3000000',
        '-rw_timeout', '4000000',
        '-i', url,
        '-f', 'null',
        '-'
    ]

    errors = defaultdict(int)
    fps_values = []
    speed_values = []
    first_packet_time = None
    start_time = time.time()

    process = subprocess.Popen(
        command,
        stderr=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
        text=True,
        errors='replace'
    )

    try:
        while True:
            ready, _, _ = select.select([process.stderr], [], [], 0.1)
            if ready:
                line = process.stderr.readline()
                if not line:
                    break
                # 检测首帧请求
                if 'frame=' in line and not first_packet_time:
                    first_packet_time = time.time() - start_time

                # 批量匹配错误类型
                error_matches = ERROR_REGEX.findall(line)
                for match in error_matches:
                    for i, group in enumerate(match):
                        if group:
                            errors[ERROR_KEYS[i]] += 1
                            break  # 每行每个错误类型只计一次

                # 实时提取性能数据
                fps_speed_match = FPS_SPEED_RE.search(line)
                if fps_speed_match:
                    try:
                        fps_values.append(float(fps_speed_match.group(1)))
                        speed_values.append(float(fps_speed_match.group(2)))
                    except ValueError:
                        pass

            # 超时检查
            if time.time() - start_time > duration_timeout + 5:
                errors['process_timeout'] += 1
                process.kill()
                break

        process.wait()

    except Exception as e:
        print(f"监控异常: {e}")
        errors['runtime_error'] = 1
        process.kill()
        process.wait()

    finally:
        if process.stderr:
            process.stderr.close()

    # 计算平均值
    avg_fps = sum(fps_values)/len(fps_values) if fps_values else 0
    avg_speed = sum(speed_values)/len(speed_values) if speed_values else 0

    # 流畅度判定（新增返回码检查）
    is_fluent = not (
        errors.get('Connection_timeout') or
        errors.get('Connection_refused') or
        errors.get('Http_error') or
        errors.get('Stream_premature_end') or
        errors.get('Corrupt_frame') or
        errors.get('Invalid_data_error') or
        errors.get('Buffer_exhausted') or
        errors.get('IO_error', 0) > 3 or
        errors.get('process_timeout') or
        avg_fps < 25 or
        avg_speed < 1.5

    )

    # print(f'url:{url}')
    # print(f'is_fluent:{is_fluent}')
    # print(f'avg_fps:{avg_fps}')
    # print(f'avg_speed:{avg_speed}')
    # print(f'first_packet_time:{first_packet_time}')
    # print(f'errors:{errors}')

    return {
        'url': url,
        'is_fluent': is_fluent,
        'avg_fps': avg_fps,
        'avg_speed': avg_speed,
        'first_packet_time': round(first_packet_time, 2) if first_packet_time else 10000,
        'errors': dict(errors)
    }


# 线程池并发检测流畅性
def generate_whitelist(urls: list, workers=os.cpu_count() * 2, output_file='white_lst.py', sort_by_fps_or_speed='S'):
    """并发检测并生成域名白名单"""
    fluent_domains = {}
    results = {'valid':[], 'error':[]}

    logger.info('—' * 100)
    logger.info(f'【开始流畅性抽样检测】:CORE_COUNT:{os.cpu_count()}'.center(100))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(analyze_stream, url): url for url in urls}
        with tqdm(total=len(urls), desc='样本检测进度', unit="urls") as pbar:
            for future in as_completed(futures):
                res = future.result()
                if res['is_fluent']:
                    results['valid'].append((res['url'], res['avg_fps'], res['avg_speed'], res['first_packet_time']))
                else:
                    results['error'].append((res['url'], res['errors']))
                pbar.update(1)
                pbar.set_postfix_str(f"有效:{len(results['valid'])} 无效:{len(results['error'])}")

        # 统一提取有效 URL 的域名
    for url, fps, speed, fst_time in results['valid']:
        domain = extract_keyword(url)
        if not domain:
            continue  # 跳过无效域名
        # 更新 fluent_domains
        if sort_by_fps_or_speed == 'F':
            if domain not in fluent_domains or fps > fluent_domains[domain]:
                fluent_domains[domain] = fps
        elif sort_by_fps_or_speed == 'S':
            if domain not in fluent_domains or speed > fluent_domains[domain]:
                fluent_domains[domain] = speed
        elif sort_by_fps_or_speed == 'T':
            if domain not in fluent_domains or fst_time > fluent_domains[domain]:
                fluent_domains[domain] = fst_time

    # 写入白名单文件
    domain_lst = []
    if sort_by_fps_or_speed == 'F':
        for domain, fps in sorted(fluent_domains.items(), key=lambda x: -x[1]):
            domain_lst.append((domain, f'FPS={fps:.2f}'))
    if sort_by_fps_or_speed == 'S':
        for domain, speed in sorted(fluent_domains.items(), key=lambda x: -x[1]):
            domain_lst.append((domain, f'SPEED={speed:.2f}X'))
    if sort_by_fps_or_speed == 'T':
        for domain, fst_time in sorted(fluent_domains.items(), key=lambda x: x[1]):
            domain_lst.append((domain, f'F_TIME={fst_time:.2f}m'))

    for domain in reversed(white_lst_stable):
        if domain not in [d[0] for d in domain_lst]:
            domain_lst.insert(0,(domain, 'reserved'))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'#  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n')
        f.write('white_lst = [\n')
        for domain in domain_lst:
            f.write(f"    '{domain[0]}',   # {domain[1]}\n")
        f.write(f']\n')


        logger.info(f'抽样检测已完成！域名白名单已写入：{output_file}'.center(100))

    domain_lst = [d[0] for d in domain_lst]
    return domain_lst

if __name__ == '__main__':
    #示例直播源列表
    # test_sources = merged_urls_samlpe
    # print(os.cpu_count())
    # generate_whitelist(
    #     urls=test_sources,
    #     workers=os.cpu_count() * 2,
    #     output_file='white_lst.py'
    # )

    analyze_stream('http://nlive.zjkgdcs.com:8091/live/xwzhpd.m3u8')
    # generate_whitelist(urls=merged_urls_samlpe,sort_by_fps_or_speed='T')