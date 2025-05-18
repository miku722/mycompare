import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('160K_and_15M_quantization_compare.csv')

# 提取数据（每两个取一个，减少一半点）
x_values = df['token_num'].tolist()
x_half = x_values[::2]
y1 = df['stories15M, no_quantize, rv64gc'].tolist()[::2]
y2 = df['stories15M, quantize, rv64gc'].tolist()[::2]
y3 = df['stories260K, no_quantize, rv64gc'].tolist()[::2]
y4 = df['stories260K, quantize, rv64gc'].tolist()[::2]

# 创建图像和子图
fig = plt.figure(figsize=(10, 6))
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1], hspace=0.05)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)

# 上图
l3, = ax1.plot(x_half, y3, 'b-', marker='o', markersize=10, linewidth=4, label='260K no quant')
l4, = ax1.plot(x_half, y4, 'b-', marker='^', markersize=10, linewidth=4, label='260K quant')
ax1.set_ylim(45, 75)
ax1.spines['bottom'].set_visible(False)
ax1.tick_params(labelbottom=False)
ax1.set_ylabel("Token/s", fontsize=12, weight='bold')
# 数据坐标系中手动设定位置
ax1.yaxis.set_label_coords(-0.07, 0)  # x为负表示向左移，y为0.5表示垂直居中

# 下图
l1, = ax2.plot(x_half, y1, 'r-', marker='o', markersize=10, linewidth=4, label='15M no quant')
l2, = ax2.plot(x_half, y2, 'r-', marker='^', markersize=10, linewidth=4, label='15M quant')
ax2.set_ylim(0.95, 1.35)
ax2.spines['top'].set_visible(False)
ax2.set_xlabel("Token Number", fontsize=12, weight='bold')

# 设置 X 轴刻度每隔20个画一个
xtick_locs = [x for x in x_values if x % 20 == 0]
ax2.set_xticks(xtick_locs)
ax2.set_xticklabels(xtick_locs, rotation=45, fontsize=12, weight='bold')

# 设置 Y 轴刻度加粗
# Y轴刻度数字加粗
ax1.tick_params(axis='y', labelsize=12)
ax2.tick_params(axis='y', labelsize=12)
# 设置刻度字体加粗
for label in ax1.get_yticklabels():
    label.set_fontweight('bold')
for label in ax2.get_yticklabels():
    label.set_fontweight('bold')

for label in ax2.get_xticklabels():
    label.set_fontweight('bold')

for spine in ax1.spines.values():
    spine.set_linewidth(1.5)
for spine in ax2.spines.values():
    spine.set_linewidth(1.5)

# 明显断轴符号
d = 0.5
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=10, linestyle="none", color='k', clip_on=False)
ax1.plot([0.5, 0.5], [0, 0], transform=ax1.transAxes, **kwargs)
ax2.plot([0.5, 0.5], [1, 1], transform=ax2.transAxes, **kwargs)

# 图例放入 ax1 内部右上角
ax1.legend(handles=[l1, l2, l3, l4], loc='upper right', frameon=False, prop={'weight': 'bold', 'size': 12})

plt.tight_layout()
plt.show()
