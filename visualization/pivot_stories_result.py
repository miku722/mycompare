import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Process an input file.")
parser.add_argument('--input_file', type=str, required=False, default='../story_output.csv',
                    help='Path to the input file')
parser.add_argument('--q_nq_input_file', type=str, required=False, default='../infer_q_nq_speed.csv',
                    help='Path to the input file')
args = parser.parse_args()


def pivot_token_per_second():
    # Load the CSV
    df = pd.read_csv(args.input_file)
    # Pivot so each feature type becomes a column with tok_per_sec as values
    # Group by tokens and features, then average tok_per_sec
    grouped_token_per_second = df.groupby(['tokens', 'features'], as_index=False)['tok_per_sec'].mean()
    # Pivot to reshape features into columns
    pivoted_token_per_second = grouped_token_per_second.pivot(index='tokens', columns='features',
                                                              values='tok_per_sec').reset_index()
    pivoted_token_per_second.to_csv('token_per_second_compare.csv', index=False)
    print("✅ 已将每个特征的平均每秒token数保存到 'token_per_second_compare.csv' 文件中.")


def pivot_accuracy():
    df = pd.read_csv(args.input_file)
    # 取三列按行平均
    df['avg_score'] = df[[ 'Coherence', 'Grammar & Fluency', 'Commonsense Reasoning']].mean(axis=1)
    grouped_accuracy = df.groupby(['tokens', 'features'], as_index=False)['avg_score'].mean()
    pivoted_accuracy = grouped_accuracy.pivot(index='tokens', columns='features', values='avg_score').reset_index()
    pivoted_accuracy.to_csv('accuracy_compare.csv', index=False)
    print("✅ 已将每个特征的平均准确度保存到 'accuracy_compare.csv' 文件中.")


def pivot_160K_and_15M():

    # 读取 infer_q_nq_speed.csv
    q_nq_df = pd.read_csv(args.q_nq_input_file)
    # 过滤掉features中含'vifmm'的行
    q_nq_df = q_nq_df[~q_nq_df['features'].str.contains('vifmm')]
    print("X 已过滤掉features中含'vifmm'的行.")
    # 过滤掉features中含'gcv'的行
    q_nq_df = q_nq_df[~q_nq_df['features'].str.contains('gcv')]
    print("X 已过滤掉features中含'gcv'的行.")
    # 计算每个特征的平均 tok_per_sec
    q_nq_grouped = q_nq_df.groupby(['tokens', 'features'], as_index=False)['tok_per_sec'].mean()
    # 透视表，将特征作为列
    q_nq_pivoted = q_nq_grouped.pivot(index='tokens', columns='features', values='tok_per_sec').reset_index()
    q_nq_pivoted.to_csv('160K_and_15M_quantization_compare.csv', index=False)
    print("✅ 已将160K和15M量化模型的平均每秒token数保存到 '160K_and_15M_quantization_compare.csv' 文件中.")