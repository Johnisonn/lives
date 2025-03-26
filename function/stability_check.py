import subprocess
import re
import os
import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from config import white_lst_stable, DURATION_TIMEOUT
import logging
logger = logging.getLogger(__name__)


# 抽取url中关键字作为后续白名单
def extract_keyword(url: str):
    if url:
        keyword = url.split('//')[1]
        keyword = keyword.split('::')[0] if '[' in keyword else keyword.split('/')[0]
    else:
        print(url)
        return None
    return keyword

# 用FFmpeg检测流畅性
def analyze_stream(url: str, duration_timeout=DURATION_TIMEOUT):
    """检测单个直播源并返回结果（包含域名和FPS）"""
    command = [
        'ffmpeg',
        '-hide_banner',
        '-t', str(duration_timeout),
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
            timeout=duration_timeout + 5
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
    elif (
            errors.get('repeated_errors', 0) > duration_timeout/2
            or errors.get('concealing_errors', 0) > 5
    ):
        is_fluent = False

    return {
        'url': url,
        'domain': extract_keyword(url),
        'is_fluent': is_fluent,
        'avg_fps': avg_fps,
        'avg_speed': avg_speed,
        'errors': errors
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
                if res['is_fluent'] and res['domain']:
                    results['valid'].append((res['url'], res['avg_fps'], res['avg_speed']))
                    # 记录最高FPS（避免重复域名）
                    if sort_by_fps_or_speed == 'F':
                        if res['domain'] not in fluent_domains or \
                                res['avg_fps'] > fluent_domains[res['domain']]:
                            fluent_domains[res['domain']] = res['avg_fps']
                    elif sort_by_fps_or_speed == 'S':
                        if res['domain'] not in fluent_domains or \
                                res['avg_speed'] > fluent_domains[res['domain']]:
                            fluent_domains[res['domain']] = res['avg_speed']
                else:
                    results['error'].append(res['errors'])
                pbar.update(1)
                pbar.set_postfix_str(f"有效:{len(results['valid'])} 无效:{len(results['error'])}")

    # 写入白名单文件
    domain_lst = []
    if sort_by_fps_or_speed == 'F':
        for domain, fps in sorted(fluent_domains.items(), key=lambda x: -x[1]):
            domain_lst.append((domain, f'FPS={fps:.2f}'))
    if sort_by_fps_or_speed == 'S':
        for domain, speed in sorted(fluent_domains.items(), key=lambda x: -x[1]):
            domain_lst.append((domain, f'SPEED={speed:.2f}X'))

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
    test_sources = ['example.com/path.m3u8']
    print(os.cpu_count())
    generate_whitelist(
        sources=test_sources,
        workers=os.cpu_count() * 2,
        output_file='white_lst.py'
    )
