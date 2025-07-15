import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pivot_stories_result


def draw_bar():
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

    # 将样本数为0的位置设为0（而不是填充平均值）
    bar_data[count_data == 0] = 0
    # bar_data.fillna(bar_data.mean(), inplace=True)

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
    ax.legend(frameon=False, loc='upper right', prop={'weight': 'bold', 'size': 7})
    for label in ax.get_yticklabels():
        label.set_fontweight('bold')
    for label in ax.get_xticklabels():
        label.set_fontweight('bold')
    for spine in ax.spines.values():
        spine.set_linewidth(1.5)
    plt.tight_layout()
    plt.show(block=True)


def draw_scatter():
    # 读取数据
    df = pd.read_csv("accuracy_compare.csv")
    
    # 配置设置：颜色、标记形状、标签、大小
    configs = [
        {'col': 'stories15M, no_quantize, rv64gc', 
         'color': '#1f77b4', 
         'marker': 'o',  # 圆形
         'label': 'NQ-rv64gc',
         'size': 80},
        
        {'col': 'stories15M, quantize, rv64gc', 
         'color': '#ff7f0e', 
         'marker': 's',  # 方形
         'label': 'Q-rv64gc',
         'size': 80},
        
        {'col': 'stories15M, quantize, rv64gcv', 
         'color': '#2ca02c', 
         'marker': '^',  # 三角形
         'label': 'Q-rv64gcv',
         'size': 90},
        
        {'col': 'stories15M, quantize, rv64gcv_vifmm', 
         'color': '#d62728', 
         'marker': 'D',  # 菱形
         'label': 'Q-rv64gcvifmm',
         'size': 85}
    ]
    
    # 创建图形
    plt.figure(figsize=(16, 8))
    ax = plt.gca()
    
    # 为每种配置绘制散点
    for cfg in configs:
        valid_data = df[df[cfg['col']].notna()]
        plt.scatter(
            x=valid_data["tokens"],
            y=valid_data[cfg['col']],
            s=cfg['size'],
            c=cfg['color'],
            marker=cfg['marker'],
            label=cfg['label'],
            alpha=0.8,
            edgecolors='black',
            linewidths=0.8
        )
    
    # 图形装饰
    plt.xlabel("Token Number", fontsize=14, fontweight='bold')
    plt.ylabel("Accuracy Score", fontsize=14, fontweight='bold')
    
    # 添加网格
    plt.grid(True, linestyle='--', alpha=0.4)
    
    # 图例设置
    legend = plt.legend(
        frameon=True,
        framealpha=0.95,
        edgecolor='gray',
        fontsize=12,
        title_fontsize='13',
        loc='upper right',  # 改为右上角
        borderaxespad=0.5,
        facecolor='white'  # 图例背景色
    )
    legend.get_frame().set_linewidth(1.2)
    
    # 调整坐标轴范围
    buffer = df["tokens"].max() * 0.05
    plt.xlim(df["tokens"].min() - buffer, df["tokens"].max() + buffer)
    plt.ylim(0, 10)
    
    # 样式调整
    plt.xticks(fontsize=12, fontweight='bold')
    plt.yticks(fontsize=12, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    
    # 可选：添加趋势线
    # for cfg in configs:
    #     valid_data = df[df[cfg['col']].notna()]
    #     z = np.polyfit(valid_data["tokens"], valid_data[cfg['col']], 1)
    #     p = np.poly1d(z)
    #     plt.plot(valid_data["tokens"], p(valid_data["tokens"]), 
    #              color=cfg['color'], linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show(block=False)

def draw_scatter_4panels():
    # 读取数据
    df = pd.read_csv("accuracy_compare.csv")
    
    # 配置设置：颜色、标记形状、标签、大小
    configs = [
        {'col': 'stories15M, no_quantize, rv64gc', 
         'color': '#1f77b4', 
         'marker': 'o',  # 圆形
         'label': 'NQ-rv64gc',
         'size': 80,
         'title': 'No Quantize (rv64gc)'},
        
        {'col': 'stories15M, quantize, rv64gc', 
         'color': '#ff7f0e', 
         'marker': 's',  # 方形
         'label': 'Q-rv64gc',
         'size': 80,
         'title': 'Quantized (rv64gc)'},
        
        {'col': 'stories15M, quantize, rv64gcv', 
         'color': '#2ca02c', 
         'marker': '^',  # 三角形
         'label': 'Q-rv64gcv',
         'size': 90,
         'title': 'Quantized (rv64gcv)'},
        
        {'col': 'stories15M, quantize, rv64gcv_vifmm', 
         'color': '#d62728', 
         'marker': 'D',  # 菱形
         'label': 'Q-rv64gcvifmm',
         'size': 85,
         'title': 'Quantized (rv64gcv+vifmm)'}
    ]
    
    # 创建2x2的子图画布
    fig, axs = plt.subplots(2, 2, figsize=(18, 12))
    
    # 统一坐标轴范围
    buffer = df["tokens"].max() * 0.05
    x_min = df["tokens"].min() - buffer
    x_max = df["tokens"].max() + buffer
    
    # 为每种配置绘制单独的散点图
    for i, cfg in enumerate(configs):
        ax = axs[i//2, i%2]  # 确定子图位置
        
        # 过滤有效数据
        valid_data = df[df[cfg['col']].notna()]
        
        # 绘制散点
        ax.scatter(
            x=valid_data["tokens"],
            y=valid_data[cfg['col']],
            s=cfg['size'],
            c=cfg['color'],
            marker=cfg['marker'],
            label=cfg['label'],
            alpha=0.8,
            edgecolors='black',
            linewidths=0.8
        )
        
        # 子图装饰
        ax.set_xlabel("Token Number", fontsize=12, fontweight='bold')
        ax.set_ylabel("Accuracy Score", fontsize=12, fontweight='bold')
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(0, 10)  # 固定y轴范围0-10
        
        # 添加网格和样式
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.tick_params(axis='both', labelsize=11)
        for spine in ax.spines.values():
            spine.set_linewidth(1.2)
        
        # 显示数据点数量
        ax.text(0.95, 0.95, f'{cfg["label"]}', 
               transform=ax.transAxes,
               ha='right', va='top',
               fontsize=12, fontweight='bold',
               bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))
    
    # 调整子图间距
    plt.tight_layout()
    plt.show(block=False)

# 调用函数


pivot_stories_result.pivot_accuracy()
draw_scatter()
draw_scatter_4panels()
draw_bar()
