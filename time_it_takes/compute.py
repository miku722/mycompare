import argparse
import re
import sys

HIGHLIGHT_GREEN = '\033[1;32m'
HIGHLIGHT_RED = '\033[1;31m'
HIGHLIGHT_END = '\033[0m'


def highlight_keyword(line, keyword, color=HIGHLIGHT_GREEN):
    return re.sub(f'({re.escape(keyword)})', f'{color}\\1{HIGHLIGHT_END}', line)


def print_context(lines, line_no, keyword=None, color=HIGHLIGHT_GREEN, context=1):
    start = max(0, line_no - context)
    end = min(len(lines), line_no + context + 1)
    print(f"🔎 行号 {line_no} 附近上下文:")
    for i in range(start, end):
        prefix = "=>" if i == line_no else "  "
        content = lines[i].rstrip()
        if keyword:
            content = highlight_keyword(content, keyword, color)
        print(f"{prefix} {i}: {content}")
    print("-" * 40)


def parse_ns(ns_str):
    return int(ns_str.rstrip('ns'))


def extract_timestamp_and_ra(line):
    time_match = re.match(r'^(\S+)', line)
    ra_match = re.search(r'ra\s+:([0-9a-f]+)', line)
    return (time_match.group(1) if time_match else None,
            ra_match.group(1) if ra_match else None)


def extract_fourth_column(line):
    parts = line.strip().split()
    return parts[3] if len(parts) >= 4 else None


def find_first_function_addr(lines, function_name):
    pattern = re.compile(r'^(?P<addr>[\da-f]+)\s+<(?P<name>{})>:'.format(re.escape(function_name)))
    for i, line in enumerate(lines):
        if m := pattern.match(line):
            return i, m.group('addr')
    return None, None


def find_nth_trace_match(lines_trace, addr, n):
    pattern = re.compile(rf'\bU\s+{re.escape(addr)}\b')
    count = 0
    for i, line in enumerate(lines_trace):
        if pattern.search(line):
            count += 1
            if count == n:
                return i
    return None


def find_ret_addr_from_dump(dump_lines, start_line):
    pattern = re.compile(r'^([0-9a-f]+):.*\bret\b')
    for i in range(start_line, len(dump_lines)):
        if m := pattern.search(dump_lines[i]):
            return i, m.group(1)
    return None, None


def load_file_lines(filename):
    try:
        with open(filename, 'r') as f:
            return f.readlines()
    except Exception as e:
        print(f"❌ 无法读取文件 {filename}: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Trace softmax 执行耗时及验证返回地址")
    parser.add_argument('--input_dump_file', type=str, required=False, default='llama2c260K.dump', help='Path to the input file')
    parser.add_argument('--input_trace_file', type=str, required=False, default='trace_hart_0.log', help='Path to the input file')
    parser.add_argument('--function_name', type=str, default='softmax', help='函数名')
    parser.add_argument('--match_index', type=int, default=10, help='匹配 trace 文件中第几个 U addr (从 1 开始)')
    args = parser.parse_args()

    dump_file       = args.input_dump_file
    trace_file      = args.input_trace_file
    function_name = args.function_name
    match_index = args.match_index

    print(f"开始分析函数: {function_name}，第 {match_index} 次匹配")

    dump_lines = load_file_lines(dump_file)
    trace_lines = load_file_lines(trace_file)

    match_line_no, addr = find_first_function_addr(dump_lines, function_name)
    if match_line_no is None:
        print(f"❌ 未找到函数 {function_name}")
        sys.exit(1)

    print(f"\n📍 找到函数地址: {addr} (行号 {match_line_no})")
    print_context(dump_lines, match_line_no, keyword=addr)

    match_trace_i_1 = find_nth_trace_match(trace_lines, addr, match_index)
    if match_trace_i_1 is None or match_trace_i_1 == 0:
        print(f"❌ trace 中未找到第 {match_index} 个 U {addr}，或该行已是第一行")
        sys.exit(1)

    print(f"\n🔍 trace 中第 {match_index} 次匹配地址 {addr} 的 U 行号: {match_trace_i_1}")
    print_context(trace_lines, match_trace_i_1, keyword=addr)

    time_ns_1, ra_addr = extract_timestamp_and_ra(trace_lines[match_trace_i_1 - 1])
    if not time_ns_1 or not ra_addr:
        print("❌ 无法提取时间戳或 ra 地址")
        sys.exit(1)

    print(f"🕒 时间戳: {highlight_keyword(time_ns_1, time_ns_1, HIGHLIGHT_RED)}，ra 地址: {ra_addr}")

    match_trace_i_2 = find_nth_trace_match(trace_lines, ra_addr, 1)
    if match_trace_i_2 is None or match_trace_i_2 == 0:
        print(f"❌ trace 中未找到 U {ra_addr}，或该行已是第一行")
        sys.exit(1)

    print(f"\n🔍 trace 中 ra 地址 {ra_addr} 的匹配行号: {match_trace_i_2}")
    print_context(trace_lines, match_trace_i_2, keyword=ra_addr)

    time_ns_2, _ = extract_timestamp_and_ra(trace_lines[match_trace_i_2 - 1])
    if not time_ns_2:
        print("❌ 无法提取第二次时间戳")
        sys.exit(1)

    print(f"🕒 第二次时间戳: {highlight_keyword(time_ns_2, time_ns_2, HIGHLIGHT_RED)}")

    duration = parse_ns(time_ns_2) - parse_ns(time_ns_1)
    print(f"\n⏱️ 总耗时: {duration} ns")

    # 验证 ret 地址
    ret_line_no, ret_addr = find_ret_addr_from_dump(dump_lines, match_line_no)
    fourth_col_addr = extract_fourth_column(trace_lines[match_trace_i_2 - 1])

    if ret_addr:
        print(f"\n🧪 验证 ret 指令: 行号 {ret_line_no}，地址: {ret_addr}")
        print_context(dump_lines, ret_line_no, keyword="ret")
        print(f"📎 trace 中上一行第四列地址: {fourth_col_addr}")

        if ret_addr.lstrip('0').lower() == fourth_col_addr.lstrip('0').lower():
            print("✅ 验证成功：两个地址匹配")
        else:
            print("❌ 验证失败：地址不一致")
    else:
        print("⚠️ 未找到 ret 指令地址用于验证")


if __name__ == '__main__':
    main()
