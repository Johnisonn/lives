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
    """检测单个直播源并返回结果（包含域名和FPS）"""
    command = [
        'ffmpeg',
        '-hide_banner',
        '-t', str(duration_timeout),
        '-timeout', '10000000',
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
            # 这里需要加入对输出编码的正确解码，有些直播源经ffmpeg处理后的输出为非UTF-8编码，会产生错误，需要更换解码。
            # 可使用latin-1（能处理所有字节）或替换错误字符来处理错误。
            # 可添加encoding='latin-1'和errors='replace'，这样可以避免解码错误
            # 如明确输出编码有中文字符，可使用encoding='gbk',
            errors='replace',  # 用 � 替换非法字符
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
    fps_pattern = r'frame=\s*\d+\s*fps=([\s\d.]+)'
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
        if 'HTTP error' in line:
            errors['http_error'] += 1
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
    elif avg_fps < 25 or avg_speed < 0.8:
        is_fluent = False
    # 条件3：高频重复错误
    elif (
            errors.get('repeated_errors', 0) > duration_timeout/2
            or errors.get('concealing_errors', 0) > 5
    ):
        is_fluent = False

    return {
        'url': url,
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
                if res['is_fluent']:
                    results['valid'].append((res['url'], res['avg_fps'], res['avg_speed']))
                else:
                    results['error'].append((res['url'], res['errors']))
                pbar.update(1)
                pbar.set_postfix_str(f"有效:{len(results['valid'])} 无效:{len(results['error'])}")

        # 统一提取有效 URL 的域名
    for url, fps, speed in results['valid']:
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
    # test_sources = merged_urls_samlpe
    # print(os.cpu_count())
    # generate_whitelist(
    #     urls=test_sources,
    #     workers=os.cpu_count() * 2,
    #     output_file='white_lst.py'
    # )

    analyze_stream('https://nlive.zjkgdcs.com:8572/live/xwzhpd.m3u8')