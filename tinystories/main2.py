from tinystories import evaluate, extract_stories
import pandas as pd
import time

# 本地调用性能无法满足
# 定义调用本地allama前先在命令行中执行：ollama run deepseek-r1
base_url = 'http://localhost:11434/v1/'
# required but ignored
api_key = 'ollama'
model = 'deepseek-r1:14b'
print(f"✅ 当前正在使用本地离线模式")


if __name__ == '__main__':
    df = pd.read_csv('stories_1.csv')
    # Create an empty list to store evaluation results
    evaluations = []
    all_criteria = set()  # Store all found criteria dynamically

    for idx, row in enumerate(df.itertuples(index=True)):
        story = row.main_text
        label = row.label
        print(f"【第{idx}行】评估故事: {label} 中... 请稍后")
        start_time = time.time()  # 记录开始时间
        evaluation_text = evaluate.evaluate_story(story, api_key=api_key, base_url=base_url, model=model)
        scores = evaluate.extract_scores(evaluation_text)
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

    # Save results to an csv file
    df.to_csv("output.csv", index=False)