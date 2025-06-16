import argparse
import re
import sys


def highlight_keyword(line, keywords):
    HIGHLIGHT_RED_START = '\033[1;31m'  # 红色加粗
    HIGHLIGHT_GREEN_START = '\033[1;32m'  # 绿色加粗
    HIGHLIGHT_END = '\033[0m'

    def repl(match):
        word = match.group(0)
        if word in red_keywords:
            return f"{HIGHLIGHT_RED_START}{word}{HIGHLIGHT_END}"
        else:
            return f"{HIGHLIGHT_GREEN_START}{word}{HIGHLIGHT_END}"

    if not keywords:
        return line

    red_keywords = set()
    green_keywords = set()
    for kw in keywords:
        if re.match(r'^\d+(ns)?$', kw):
            red_keywords.add(kw)
        else:
            green_keywords.add(kw)

    all_keywords = red_keywords.union(green_keywords)
    if not all_keywords:
        return line

    pattern = re.compile('|'.join(re.escape(k) for k in all_keywords))
    return pattern.sub(repl, line)


def print_context(lines, line_no, keywords=None):
    start = max(0, line_no - 1)
    end = min(len(lines), line_no + 2)
    print(f"行号 {line_no} 上下文：")
    for i in range(start, end):
        prefix = "=>" if i == line_no else "  "
        content = lines[i].rstrip()
        if keywords:
            content = highlight_keyword(content, keywords)
        print(f"{prefix} {i}: {content}")
    print("-" * 40)


def verify_address_consistency(dump_lines, match_line_no, keyword, trace_prev_line_fourth_col):
    """
    从 match_line_no 向下搜索最近的类似：
    8000f79c: 82 80         ret
    形式的行，末尾含 keyword。
    取出地址（冒号前的部分），与 trace_prev_line_fourth_col 比较是否一致。
    """

    max_search_dist = 50  # 最多往下搜索50行防止过大
    end = min(len(dump_lines), match_line_no + max_search_dist + 1)

    pattern = re.compile(r'^([0-9a-f]+):.*\b{}\b'.format(re.escape(keyword)))

    for i in range(match_line_no, end):
        line = dump_lines[i]
        m = pattern.search(line)
        if m:
            addr_found = m.group(1)
            print(f"\n🔎 验证步骤: dump 文件中距离匹配行向下最近的 '{keyword}' 行号: {i}, 地址: {addr_found}")
            print(f"trace 匹配行上一行第四列地址: {trace_prev_line_fourth_col}")

            # 去除地址前导0再比较（忽略大小写）
            addr_found_cmp = addr_found.lower().lstrip('0')
            trace_addr_cmp = trace_prev_line_fourth_col.lower().lstrip('0')

            if addr_found_cmp == trace_addr_cmp:
                print("✅ 验证成功：两个地址匹配一致。")
            else:
                print("❌ 验证失败：两个地址不一致。")
            return addr_found, trace_prev_line_fourth_col

    print(f"⚠️ 在 dump 文件中未找到包含关键字 '{keyword}' 的类似地址行进行验证")
    return None, None


def main():
    parser = argparse.ArgumentParser(description="please input your command")
    parser.add_argument('--function_name', type=str, required=False, default='softmax', help='function name')
    parser.add_argument('--match_times', type=int, required=False, default=1, help='number of times to match')
    parser.add_argument('--verify_keyword', type=str, required=False, default='ret', help='verification keyword in dump')
    args = parser.parse_args()

    function_name = args.function_name
    match_times = args.match_times
    verify_keyword = args.verify_keyword
    print(f"开始寻找: {function_name}, 匹配次数: {match_times}次，验证关键字: {verify_keyword}")

    # 读 dump 文件
    with open('llama2c260K.dump', 'r') as f:
        lines = f.readlines()
    print("✅ 已成功读取 dump 文件，共 {} 行".format(len(lines)))

    pattern = re.compile(r'^(?P<addr>[\da-f]+)\s+<(?P<name>{})>:'.format(re.escape(function_name)))

    match_line_no = None
    addr = None
    for i, line in enumerate(lines):
        m = pattern.match(line)
        if m:
            match_line_no = i
            addr = m.group('addr')
            break

    if match_line_no is None:
        print(f"❌ 未找到函数 {function_name} 的匹配项.")
        sys.exit(1)

    print(f"\n📍 第1个匹配项（行号 {match_line_no}）地址：{addr}")
    print_context(lines, match_line_no, keywords=[addr])

    with open('trace_hart_0.log', 'r') as f:
        lines_trace = f.readlines()
    print(f"✅ trace 文件已读取，共 {len(lines_trace)} 行")

    candidate_i = None
    for i, line in enumerate(lines_trace):
        if re.search(rf'U\s+{re.escape(addr)}', line):
            candidate_i = i
            break

    if candidate_i is None:
        print(f"❌ trace 文件中未找到 U {addr} 的匹配行.")
        sys.exit(1)

    print(f"\n🔍 trace 文件中离匹配地址 {addr} 最近的 U 行号: {candidate_i}")

    if candidate_i == 0:
        print("⚠️ 匹配行已经是第一行，无法向上取时间戳和 ra 地址")
        sys.exit(1)

    prev_line = lines_trace[candidate_i - 1]
    time_match = re.match(r'^(\S+)', prev_line)
    if not time_match:
        print("❌ 无法从上一行提取时间戳")
        sys.exit(1)
    time_ns_1 = time_match.group(1)

    ra_match = re.search(r'ra\s+:([0-9a-f]+)', prev_line)
    if not ra_match:
        print("❌ 无法从上一行提取 ra 地址")
        sys.exit(1)
    ra_addr = ra_match.group(1)

    print(f"上一行时间戳: {time_ns_1}，ra 地址: {ra_addr}")

    print_context(lines_trace, candidate_i, keywords=[addr, time_ns_1])

    ra_line_i = None
    for i, line in enumerate(lines_trace):
        if re.search(rf'U\s+{re.escape(ra_addr)}', line):
            ra_line_i = i
            break

    if ra_line_i is None:
        print(f"❌ trace 文件中未找到 U {ra_addr} 的匹配行.")
        sys.exit(1)

    print(f"\n🔍 trace 文件中 ra 地址 {ra_addr} 的匹配行号: {ra_line_i}")

    if ra_line_i == 0:
        print("⚠️ ra 地址匹配行已经是第一行，无法向上取时间戳计算耗时")
        sys.exit(1)

    prev_line_ra = lines_trace[ra_line_i - 1]
    time_match_ra = re.match(r'^(\S+)', prev_line_ra)
    if not time_match_ra:
        print("❌ 无法从 ra 匹配行上一行提取时间戳")
        sys.exit(1)
    time_ns_2 = time_match_ra.group(1)

    print_context(lines_trace, ra_line_i, keywords=[ra_addr, time_ns_2])

    def parse_ns(ns_str):
        return int(ns_str.rstrip('ns'))

    duration = parse_ns(time_ns_2) - parse_ns(time_ns_1)
    print(f"\n⏱️ 计算耗时: {duration} ns (前一时间戳 {time_ns_1} -> 后一时间戳 {time_ns_2})")

    # 验证环节：取trace匹配行上一行第四列地址
    prev_line_fields = prev_line.strip().split()
    if len(prev_line_fields) < 4:
        print("⚠️ trace 匹配行上一行字段不足，无法提取第四列做验证")
        sys.exit(1)
    trace_prev_line_fourth_col = prev_line_fields[3]

    verify_address_consistency(lines, match_line_no, verify_keyword, trace_prev_line_fourth_col)


if __name__ == '__main__':
    main()
