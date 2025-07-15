import evaluate, extract_stories
import pandas as pd
import os
import argparse
import time
import pexpect
import re

def grep_scores(response):
    """
    从模型的回复中提取 Coherence、Grammar & Fluency 和 Commonsense Reasoning 的得分。
    """
    # 使用正则表达式匹配评分项及其分数
    pattern = r"(Coherence|Grammar & Fluency|Commonsense Reasoning).*?\s*(\d+)/10"
    matches = re.findall(pattern, response)
    # 返回一个字典，键为评分项，值为对应的得分（整数）
    return {match[0]: int(match[1]) for match in matches}


def remove_ansi_codes(text):
    """
    移除文本中的 ANSI 控制字符。
    """
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

parser = argparse.ArgumentParser(description="Process an input file.")
parser.add_argument('--input_file', type=str, required=False, default='test_res.txt', help='Path to the input file')
parser.add_argument('--output_file', type=str, required=False, default='story_output.csv', help='Path to output file')

args = parser.parse_args()

# 解析后的路径（支持相对或绝对路径）
# 检查文件是否存在
# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
input_file = args.input_file
output_file = args.output_file

temp_file_name = 'stories.csv'

if not os.path.isfile(input_file):
    print(f"❌ 输入文件不存在：{input_file}, 使用默认文件")
    input_file = os.path.join(current_dir, 'test_res.txt')

print(f"使用输入文件：{input_file}")
print(f"使用输出文件：{output_file}")

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


# 启动 Ollama
child = pexpect.spawn("ollama run deepseek-r1:14b")
# child = pexpect.spawn("ollama run gemma3:12b")
child.expect(">>>")  # 等待初始提示符

all_responses = []  # 保存所有轮次的完整回复
evaluations = []
all_criteria = set()  # Store all found criteria dynamically

# 将 df 中的 main_text 添加到 prompts 中
for idx, row in df.iterrows():
    key = (row.rnd_seed, row.features)
    if key in keys_set:
        print(f"【第{idx}行】该故事 seed{row['rnd_seed']}-{row['features']}已评估, 跳过.")
        continue
    main_text = (f" You are a professional story evaluator. The student is given the opening sentence of a story: \"One day, Lily met a Shoggoth.\" They need to complete it into a full story. The story is \"{row.main_text}\". Please provide your general assessment about the part written by the student. Evaluate the following short story based on these criteria: 1. Coherence: Is it consistent with the beginning of the story? 2. Grammar & Fluency: Is the text grammatically correct and easy to read? 3. Commonsense Reasoning: Do the characters in stories behave in a way that makes sense? You must give the scores in the following strict format (each score must be between 1 and 10): Coherence: X/10; Grammar & Fluency: X/10; Commonsense Reasoning: X/10")
    # 发送当前 prompt
    current_prompt = main_text.replace("\n", "")
    # print(f"\n[用户] {current_prompt}")
    print(f"【第{idx}行】评估故事: {row.label} {row.rnd_seed} {row.features} {row.tokens}tks 中... ")
    while True:  # 循环直到得分满足非 0 条件
        start_time = time.time()  # 记录开始时间
        child.sendline(current_prompt)
        # 实时捕获回复内容
        current_response = []
        try:
            while True:
                # 匹配输出行或结束标记
                child.expect(["\n", ">>>", pexpect.TIMEOUT], timeout=10)
                line = child.before.decode().strip()
                # print(f"[DEBUG] {line}")  # 打印模型的回复
                
                if line:  # 捕获有效输出
                    clean_line = remove_ansi_codes(line)  # 清理 ANSI 控制字符
                    current_response.append(clean_line)
                    # print(f"[模型] {clean_line}")  # 打印清理后的模型回复

                end_time = time.time()  # 记录开始时间
                if end_time - start_time > 60*10:  # 超时设置为10分钟
                    print("❌ TIMEOUT, Reloading prompt...")
                    child.sendline(current_prompt)
                    start_time = time.time()  # 记录开始时间
                # 检测到回复结束标记（Ollama的提示符 >>>）
                if ">>>" in child.after.decode():
                    # 将当前轮次的完整回复合并为字符串，存入列表
                    full_response = "\n".join(current_response)
                    break
        except pexpect.TIMEOUT:
            print("对话超时，终止检测")
            break
         # 提取得分
        # print(f"\n[模型] 完整回复: {full_response}")
        scores = grep_scores(full_response)
        print(f"Scores: {scores}")
        # 检测得分是否满足非 0 条件
        if len(scores) == 3 and all((score > 0 and score <= 10) for score in scores.values()):
            break
        else:
            print("❌ 检测到得分为 0，重新推理...")
    
    all_criteria.update(scores.keys())
    evaluations.append((scores, full_response))

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



# 关闭会话
child.close()