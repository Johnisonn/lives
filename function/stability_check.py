import subprocess
import re
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from urllib.parse import urlparse
import logging
logger = logging.getLogger(__name__)

from urllib.parse import urlparse


def extract_domain(url):
    """从URL中提取域名（去除端口和路径）"""
    try:
        if url.startswith(('rtmp://', 'udp://', 'rtsp://')):
            netloc = url.split('//')[1].split('/')[0].split('@')[-1]
        else:
            parsed = urlparse(url)
            netloc = parsed.netloc
        domain = netloc.split(':')[0]
        return domain.strip()
    except:
        return None


def analyze_stream(url, timeout=20):
    """检测单个直播源并返回结果（包含域名和FPS）"""
    command = [
        'ffmpeg',
        '-hide_banner',
        '-t', str(timeout),
        '-timeout', '5000000',
        '-rw_timeout', '5000000',
        '-i', url,
        '-f', 'null',
        '-'
    ]

    errors = defaultdict(int)
    log = ''
    try:
        result = subprocess.run(
            command,
            stderr=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            text=True,
            timeout=timeout + 5
        )
        log = result.stderr
    except subprocess.TimeoutExpired as e:
        log = e.stderr.decode('utf-8') if e.stderr else ''
        errors['process_timeout'] = 1

    # 解析FPS和Speed
    fps_values = []
    speed_values = []
    # 匹配FPS和Speed
    fps_pattern = r'frame=\s*\d+\s+fps=([\d.]+)'
    speed_pattern = r'speed=([\d.]+)x'
    for line in log.split('\n'):
        if 'fps=' in line:
            fps_match = re.search(fps_pattern, line)
            if fps_match:
                fps_values.append(float(fps_match.group(1)))
        if 'speed=' in line:
            speed_match = re.search(speed_pattern, line)
            if speed_match:
                speed_values.append(float(speed_match.group(1)))

        # 检测关键错误（新增特征）
        if 'Connection timed out' in line:
            errors['connection_timeout'] += 1
        if 'Connection refused' in line:
            errors['connection_refused'] += 1
        if 'HTTP error 404' in line:
            errors['http_404'] += 1
        if 'Invalid data found' in line:  # 新增：输入数据错误
            errors['invalid_data_error'] += 1
        if 'decode_slice_header error' in line:
            errors['decode_error'] += 1
        if 'Last message repeated' in line:
            errors['repeated_errors'] += 1
        if 'buffer exhausted' in line.lower():
            errors['buffer_exhausted'] += 1
        if 'Stream ends prematurely' in line:  # 新增：流提前终止
            errors['stream_premature_end'] += 1
        if 'corrupt decoded frame' in line:  # 新增：解码帧损坏
            errors['corrupt_frame'] += 1
        if 'concealing' in line and 'errors in' in line:  # 新增：错误掩盖
            errors['concealing_errors'] += 1
        if 'Input/output error' in line:  # 增强：高频I/O错误
            errors['io_error'] += 1

    avg_fps = sum(fps_values) / len(fps_values) if fps_values else 0
    avg_speed = sum(speed_values) / len(speed_values) if speed_values else 0

    # 判定规则
    is_fluent = True
    # 条件1：进程超时或存在致命错误
    if errors.get('process_timeout', 0) > 0:
        is_fluent = False
    elif (
            errors.get('http_404', 0) > 0
            or errors.get('connection_timeout', 0) > 0
            or errors.get('buffer_exhausted', 0) > 0
            or errors.get('stream_premature_end', 0) > 0  # 新增条件
            or errors.get('corrupt_frame', 0) > 0  # 新增条件
            or errors.get('io_error', 0) > 3  # 高频I/O错误
            or errors.get('invalid_data_error',0) > 0
            or errors.get('connection_refused',0) > 0
    ):
        is_fluent = False
    # 条件2：性能指标不达标
    elif avg_fps < 25 or avg_speed < 1.0:
        is_fluent = False
    # 条件3：高频重复错误
    elif errors.get('repeated_errors', 0) > 10 or errors.get('concealing_errors', 0) > 5:
        is_fluent = False

    return {
        'url': url,
        'domain': extract_domain(url),
        'is_fluent': is_fluent,
        'avg_fps': avg_fps
    }


def generate_whitelist(sources, workers=4, output_file='white_lst'):
    """并发检测并生成域名白名单"""
    fluent_domains = {}
    logger.info(' ')
    logger.info('-' * 43 + '开始流畅性检测' + '-' * 43)
    logger.info(' ')
    logger.info('-' * 44 + f'core_num:{os.cpu_count()}' + '-' * 44)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(analyze_stream, url): url for url in sources}
        with tqdm(total=len(sources), desc='检测进度') as pbar:
            for future in as_completed(futures):
                res = future.result()
                if res['is_fluent'] and res['domain']:
                    # 记录最高FPS（避免重复域名）
                    if res['domain'] not in fluent_domains or \
                            res['avg_fps'] > fluent_domains[res['domain']]:
                        fluent_domains[res['domain']] = res['avg_fps']
                pbar.update(1)

    # 写入白名单文件
    domain_lst = []
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("white_lst = [\n")
        for domain, fps in sorted(fluent_domains.items(), key=lambda x: -x[1]):
            f.write(f"    '{domain}',  # {fps:.2f}fps\n")
            domain_lst.append(domain)
        f.write("]\n")
        logger.info('>' * 35 + f'域名白名单已写入：white_lst.txt' + '<' * 35)

    return domain_lst

if __name__ == '__main__':
    # 示例直播源列表
    test_sources = urls.test_urls
    print(os.cpu_count())
    generate_whitelist(
        sources=test_sources,
        workers=os.cpu_count() * 2,
        output_file='white_lst.py'
    )