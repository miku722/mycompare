from tinystories import evaluate, extract_stories
import pandas as pd

output_file_name = 'stories.csv'
# 本地调用性能无法满足
# 定义调用本地allama前先在命令行中执行：ollama run deepseek-r1
# base_url = 'http://localhost:11434/v1/'
# # required but ignored
# api_key = 'ollama'
# model = 'deepseek-r1:latest'

# 本地调用太慢了 我要联网
api_key = 'sk-df877d0bd61c4707b67d0449ccf42132'
base_url ="https://api.deepseek.com"
model = 'deepseek-chat'

if __name__ == '__main__':
    # 读取文件结构化至csv文本
    extract_stories.export_to_csv(output_file_name=output_file_name)

    df = pd.read_csv("stories.csv")
    # Create an empty list to store evaluation results
    evaluations = []
    all_criteria = set()  # Store all found criteria dynamically

    for story in df["main_text"]:
        evaluation_text = evaluate.evaluate_story(story, api_key=api_key, base_url=base_url, model=model)
        scores = evaluate.extract_scores(evaluation_text)

        # Track all possible criteria found across different evaluations
        all_criteria.update(scores.keys())

        evaluations.append((scores, evaluation_text))

    # Initialize DataFrame with dynamic columns
    for criterion in all_criteria:
        df[criterion] = 0  # Default score if missing

    df["Evaluation"] = ""

    # Populate extracted scores into DataFrame
    for idx, (scores, evaluation_text) in enumerate(evaluations):
        for criterion, score in scores.items():
            df.at[idx, criterion] = score
        df.at[idx, "Evaluation"] = evaluation_text

    # Save results to an Excel file
    df.to_csv("story_evaluations.csv", index=False)

    print("Evaluation completed! Results saved to 'story_evaluations.csv'.")
