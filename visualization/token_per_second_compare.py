import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# 读取数据
df = pd.read_csv('token_per_second_compare.csv')

# 设置颜色、标记样式、简写标签（用于图例）
configs = [
    ('stories15M, no_quantize, rv64gc', 'o', '#1f77b4', 'no_quant rv64gc'),
    ('stories15M, quantize, rv64gc', 's', '#ff7f0e', 'quant rv64gc'),
    ('stories15M, quantize, rv64gcv', '^', '#2ca02c', 'quant rv64gcv'),
    ('stories15M, quantize, rv64gcv_vifmm', 'D', '#d62728', 'quant rv64gcv_vifmm')
]

# 获取统一的 x 轴范围用于平滑插值
x_uniform = np.linspace(df['tokens'].min(), df['tokens'].max(), 300)

# 创建断层图
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True,
                               gridspec_kw={'height_ratios': [1, 1]},
                               figsize=(12, 8))

# 平滑曲线 + 均匀 marker 函数
def interpolate_and_plot(ax, x, y, marker, color, smooth_s=0.5):
    valid = ~np.isnan(y)
    x_valid, y_valid = x[valid], y[valid]
    if len(x_valid) > 3:
        spline = UnivariateSpline(x_valid, y_valid, s=smooth_s)
        y_smooth = spline(x_uniform)
        ax.plot(x_uniform, y_smooth, color=color, alpha=0.85, zorder=1)

        # 在平滑曲线上均匀分布 marker
        step = 30  # 控制 marker 密度
        marker_x = x_uniform[::step]
        marker_y = y_smooth[::step]
        ax.plot(marker_x, marker_y, marker=marker, linestyle='None', color=color, markersize=6, zorder=3)

# 绘制所有曲线
for full_label, marker, color, _ in configs:
    interpolate_and_plot(ax1, df['tokens'], df[full_label], marker, color)
    interpolate_and_plot(ax2, df['tokens'], df[full_label], marker, color)

# 设置坐标轴范围
ax1.set_ylim(4.7, 5.4)   # 高值范围
ax2.set_ylim(0.95, 1.35) # 低值范围

# 隐藏断轴之间的边界
ax1.spines.bottom.set_visible(False)
ax2.spines.top.set_visible(False)
ax1.tick_params(labelbottom=False)

# 添加断层标记（明显清晰）
d = 0.5
kwargs = dict(marker=[(-1, -d), (1, d)], markersize=10,
              linestyle="none", color='k', clip_on=False)
ax1.plot([0.5, 0.5], [0, 0], transform=ax1.transAxes, **kwargs)
ax2.plot([0.5, 0.5], [1, 1], transform=ax2.transAxes, **kwargs)

# 添加图例（垂直排列，居于图内右上角）
ax1.legend(handles=[
    plt.Line2D([], [], color=color, marker=marker, linestyle='-',
               markersize=8, label=simple_label)
    for _, marker, color, simple_label in configs
], loc='upper right', frameon=False, fontsize=10, title='Model Configs', title_fontsize=11)

# 添加标签
ax1.set_ylabel("tok/s (high)", fontsize=12)
ax2.set_ylabel("tok/s (low)", fontsize=12)
ax2.set_xlabel("Token Number", fontsize=12)
plt.suptitle('Performance Comparison (Broken Axis)', y=0.98, fontsize=14)

# 网格线可选开启
# ax1.grid(alpha=0.2)
# ax2.grid(alpha=0.2)

plt.tight_layout()
plt.savefig('broken_axis_even_markers.png', dpi=300, bbox_inches='tight')
plt.show()
