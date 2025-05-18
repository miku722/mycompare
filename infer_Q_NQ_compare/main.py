from infer_Q_NQ_compare import  extract_stories
import pandas as pd
import os
import argparse

temp_file_name = 'infer_q_nq_speed.csv'

if __name__ == '__main__':
    # 解析输入参数
    parser = argparse.ArgumentParser(description="Process an input file.")
    parser.add_argument('--input_file', type=str, required=False, default='test_res.txt', help='Path to the input file')
    args = parser.parse_args()

    # 解析后的路径（支持相对或绝对路径）
    # 检查文件是否存在
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = args.input_file

    if not os.path.isfile(input_file):
        print(f"❌ 输入文件不存在：{input_file}, 使用默认文件")
        input_file = os.path.join(current_dir, 'test_res.txt')

    print(f"使用输入文件：{input_file}")

    # 读取文件结构化至csv文本
    extract_stories.export_to_csv(input_file_name=input_file, temp_file_name=temp_file_name)

