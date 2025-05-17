import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv("accuracy_compare.csv")

configs = [
    ('stories15M, no_quantize, rv64gc', '#6C8EBF', 'no_quant rv64gc'),       # 柔和蓝色
    ('stories15M, quantize, rv64gc', '#D79B00', 'quant rv64gc'),             # 金色
    ('stories15M, quantize, rv64gcv', '#B85450', 'quant rv64gcv'),           # 红褐色
    ('stories15M, quantize, rv64gcv_vifmm', '#9673A6', 'quant rv64gcv_vifmm') # 紫灰色
]

# 分组区间
step = 10
min_token = df["tokens"].min()
max_token = df["tokens"].max()
bins = np.arange(min_token, max_token + step, step)
labels = [f"{int(bins[i])}-{int(bins[i+1]-1)}" for i in range(len(bins) - 1)]
df["range"] = pd.cut(df["tokens"], bins=bins, labels=labels, include_lowest=True)

# 平均值统计并填补缺失
col_names = [col for col, _, _ in configs]
bar_data = df.groupby("range")[col_names].mean()
bar_data.fillna(bar_data.mean(), inplace=True)

# 绘图
x = np.arange(len(bar_data))  # 每组柱的位置
bar_width = 0.2

fig, ax = plt.subplots(figsize=(14, 6))

for i, (col, color, short_label) in enumerate(configs):
    offset = (i - 1.5) * bar_width
    ax.bar(x + offset, bar_data[col], width=bar_width, label=short_label, color=color)

# 设置标签和刻度
ax.set_xlabel("Token Number", fontsize=12, weight='bold')
ax.set_ylabel("Score", fontsize=12, weight='bold')
ax.set_xticks(x)
ax.tick_params(axis='y', labelsize=12)
ax.set_xticklabels(bar_data.index, fontstyle='normal', rotation=45, fontsize=12, weight='bold')  # 正常字体
ax.legend(frameon=False, loc='upper right', prop={'weight': 'bold', 'size': 12})


# 设置刻度字体加粗
for label in ax.get_yticklabels():
    label.set_fontweight('bold')

for label in ax.get_xticklabels():
    label.set_fontweight('bold')

for spine in ax.spines.values():
    spine.set_linewidth(1.5)

plt.tight_layout()
plt.savefig("bar_grouped_by_token_range_gray_earth.png", dpi=300)
# plt.style.use(['science', 'ieee'])
plt.show()
