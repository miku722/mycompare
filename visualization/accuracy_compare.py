import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def run():
    # 读取数据
    df = pd.read_csv("accuracy_compare.csv")
    configs = [
        ('stories15M, no_quantize, rv64gc', '#6C8EBF', 'NQ-rv64gc'),
        ('stories15M, quantize, rv64gc', '#D79B00', 'Q-rv64gc'),
        ('stories15M, quantize, rv64gcv', '#B85450', 'Q-rv64gcv'),
        ('stories15M, quantize, rv64gcv_vifmm', '#9673A6', 'Q-rv64gcvifmm')
    ]
    # 分组区间
    step = 20
    min_token = df["tokens"].min()
    max_token = df["tokens"].max()
    bins = np.arange(min_token, max_token + step, step)
    labels = [f"{int(bins[i])}-{int(bins[i + 1] - 1)}" for i in range(len(bins) - 1)]
    df["range"] = pd.cut(df["tokens"], bins=bins, labels=labels, include_lowest=True)
    # 统计非空样本数（每个 range × config）
    count_data = df.groupby("range")[[col for col, _, _ in configs]].apply(lambda g: g.notna().sum())
    # 平均值统计并填补缺失
    col_names = [col for col, _, _ in configs]
    bar_data = df.groupby("range")[col_names].mean()
    bar_data.fillna(bar_data.mean(), inplace=True)
    # 绘图
    x = np.arange(len(bar_data))
    bar_width = 0.2
    fig, ax = plt.subplots(figsize=(14, 6))
    for i, (col, color, short_label) in enumerate(configs):
        offset = (i - 1.5) * bar_width
        bars = ax.bar(x + offset, bar_data[col], width=bar_width, label=short_label, color=color)

        # 标注每个柱子的非空样本数
        # for j, rect in enumerate(bars):
        #     count = count_data.iloc[j][col]  # 对应区间和配置列的非空数量
        #     height = rect.get_height()
        #     ax.text(
        #         rect.get_x() + rect.get_width() / 2, height + 0.01,
        #         f"{count}", ha='center', va='bottom',
        #         fontsize=9, fontweight='bold'
        #     )
    # 轴标签和样式设置
    ax.set_xlabel("Token Number", fontsize=14, weight='bold')
    ax.set_ylabel("Score", fontsize=14, weight='bold')
    ax.yaxis.set_label_coords(-0.03, 0.5)
    ax.set_xticks(x)
    ax.set_xticklabels(bar_data.index, fontsize=14, weight='bold')
    ax.tick_params(axis='y', labelsize=14)
    ax.legend(frameon=False, loc='upper right', prop={'weight': 'bold', 'size': 14})
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
    for label in ax.get_xticklabels():
        label.set_fontweight('bold')
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    plt.tight_layout()
    plt.show()

run()