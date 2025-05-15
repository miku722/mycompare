import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('160K_and_15M_quantization_compare.csv')

# 提取数据
y1 = df['stories15M, no_quantize, rv64gc'].tolist()
y2 = df['stories15M, quantize, rv64gc'].tolist()
y3 = df['stories260K, no_quantize, rv64gc'].tolist()
y4 = df['stories260K, quantize, rv64gc'].tolist()
x_values = df['token_num'].tolist()

# 创建图像和子图
fig = plt.figure(figsize=(10, 6))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.5], hspace=0.05)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)

# 上图
l3, = ax1.plot(x_values, y3, 'b-', marker='o', label='260K no quant')
l4, = ax1.plot(x_values, y4, 'b-', marker='^', label='260K quant')
ax1.set_ylim(45, 75)
ax1.spines['bottom'].set_visible(False)
ax1.tick_params(labelbottom=False)
ax1.set_ylabel("tok/s (high)")

# 下图
l1, = ax2.plot(x_values, y1, 'r-', marker='o', label='15M no quant')
l2, = ax2.plot(x_values, y2, 'r-', marker='^', label='15M quant')
ax2.set_ylim(0.95, 1.35)
ax2.spines['top'].set_visible(False)
ax2.set_ylabel("tok/s (low)")
ax2.set_xlabel("Token Number")

# 设置 X 轴刻度
ax2.set_xticks(x_values)
ax2.set_xticklabels(x_values, rotation=45)

# 明显断轴符号
d = 0.5
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=10, linestyle="none", color='k', clip_on=False)
ax1.plot([0.5, 0.5], [0, 0], transform=ax1.transAxes, **kwargs)
ax2.plot([0.5, 0.5], [1, 1], transform=ax2.transAxes, **kwargs)

# 图例放入 ax1 内部右上角
ax1.legend(handles=[l1, l2, l3, l4], loc='upper right', frameon=False)

plt.suptitle("Token Throughput vs Token Number", fontsize=14)
plt.tight_layout()
plt.show()
