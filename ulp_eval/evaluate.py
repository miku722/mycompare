import argparse


def process_log_data(filename, keyword):
    max_value = None
    sum_values = 0
    count = 0
    
    with open(filename, 'r') as file:
        for line in file:
            if keyword in line:
                # 分割字符串，获取冒号后的部分
                data_part = line.split(":")[1].strip()
                # 将字符串分割成数字列表，过滤掉空字符串
                numbers = [int(num) for num in data_part.split() if num.isdigit()]
                
                if numbers:  # 确保列表不为空
                    current_max = max(numbers)
                    current_avg = sum(numbers) / len(numbers)
                    
                    # 更新最大值
                    if max_value is None or current_max > max_value:
                        max_value = current_max
                    
                    # 累加用于计算总平均值
                    sum_values += sum(numbers)
                    count += len(numbers)
    
    if count == 0:
        return None, None  # 如果没有找到有效数据
    
    average_value = sum_values / count
    return max_value, average_value, count

parser = argparse.ArgumentParser(description="分析日志文件中的特定关键字数据")
parser.add_argument("--file_path", help="日志文件路径")
args = parser.parse_args()


keyword = "# VIFMM ULP:"
max_val, avg_val, total_num= process_log_data(args.file_path, keyword)
print(f"{keyword} Num: {total_num} ")
print(f" 最大值: {max_val}")
print(f" 平均值: {avg_val}")
keyword = "# X FP32 TO INT8 ULP:"
max_val, avg_val, total_num = process_log_data(args.file_path, keyword)
print(f"{keyword} Num: {total_num} ")
print(f"最大值: {max_val}")
print(f"平均值: {avg_val}")
