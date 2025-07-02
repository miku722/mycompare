from tinystories import evaluate, extract_stories
import pandas as pd
import os
import argparse
import time

temp_file_name = 'stories.csv'

if __name__ == '__main__':
    # 解析输入参数
    parser = argparse.ArgumentParser(description="Process an input file.")
    parser.add_argument('--input_file', type=str, required=False, default='test_res.txt', help='Path to the input file')
    parser.add_argument('--output_file', type=str, required=False, default='story_output.csv', help='Path to '
                                                                                                         'output file')
    parser.add_argument('--offline', type=str, choices=['true', 'false', 'True', 'False'], required=False,
                        default='False', help='Using ollama offline model or '
                                              'not')
    args = parser.parse_args()

    # 解析后的路径（支持相对或绝对路径）
    # 检查文件是否存在
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = args.input_file
    output_file = args.output_file
    if not os.path.isfile(input_file):
        print(f"❌ 输入文件不存在：{input_file}, 使用默认文件")
        input_file = os.path.join(current_dir, 'test_res.txt')

    print(f"使用输入文件：{input_file}")
    print(f"使用输出文件：{output_file}")

    if args.offline.lower() in 'true':
        # 本地调用性能无法满足
        # 定义调用本地allama前先在命令行中执行：ollama run deepseek-r1
        base_url = 'http://localhost:11434/v1/'
        # required but ignored
        api_key = 'ollama'
        model = 'deepseek-r1:14b'
        print(f"✅ 当前正在使用本地离线模式")
    else:
        # 本地调用太慢了 我要联网
        api_key = 'sk-df877d0bd61c4707b67d0449ccf42132'
        base_url = "https://api.deepseek.com"
        model = 'deepseek-chat'
        print("✅ 当前正在使用在线模式")

    # 读取文件结构化至csv文本
    extract_stories.export_to_csv(input_file_name=input_file, temp_file_name=temp_file_name)

    df = pd.read_csv(temp_file_name)
    if os.path.isfile(output_file) and os.path.getsize(output_file) > 0:
        df_story_output = pd.read_csv(output_file)
        # 将抽取的故事与已经评估完成的故事进行对比，去重
        keys_set = set(df_story_output.apply(lambda row: (row['rnd_seed'], row['features']), axis=1))
    else:
        print(f"⚠️ 输出文件为空或不存在：{output_file}, 跳过读取.")
        keys_set = set()
    
    # Create an empty list to store evaluation results
    evaluations = []
    all_criteria = set()  # Store all found criteria dynamically

    for idx, row in df.iterrows():
        key = (row.rnd_seed, row.features)
        if key in keys_set:
            print(f"【第{idx}行】该故事 seed{row['rnd_seed']}-{row['features']}已评估, 跳过.")
            continue
        story = row.main_text
        label = row.label
        print(f"【第{idx}行】评估故事: {label} 中... 请稍后")
        start_time = time.time()  # 记录开始时间
        while True:
            evaluation_text = evaluate.evaluate_story(story, api_key=api_key, base_url=base_url, model=model)
            scores = evaluate.extract_scores(evaluation_text)
            if  len(scores) != 3:  # 如果是0分，继续评估，直到有分数
                print("❌ WARNING: 0 in Scores, Reevaluating!")
            else:
                print(f"Scores: {scores}")
                break
        # Track all possible criteria found across different evaluations
        all_criteria.update(scores.keys())
        evaluations.append((scores, evaluation_text))
        end_time = time.time()  # 记录结束时间
        duration = end_time - start_time
        print(f"✅ 评估完成，耗时 {duration:.2f} 秒\n")

    # Initialize DataFrame with dynamic columns
    for criterion in all_criteria:
        df[criterion] = 0  # Default score if missing
    df["Evaluation"] = ""

    # Populate extracted scores into DataFrame
    for idx, (scores, evaluation_text) in enumerate(evaluations):
        for criterion, score in scores.items():
            df.at[idx, criterion] = score
        df.at[idx, "Evaluation"] = evaluation_text

    # Save results to a csv file
    df.to_csv(output_file, index=False, mode='a', header=False)

    print(f"Evaluation completed! Results saved to {output_file}.")
