#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
论文级竖向条形图生成器（与 Book/part13_engineering/ch151_benchmark.md 图2 风格严格一致）。

设计约定（来自 ch151 实证，三模式 site/epub/pdf 安全）：
- viewBox 固定 `0 0 680 348`（680 宽不可变）。
- 坐标轴框：左(y轴) + 底(x轴) 实线 #555。
- 浅灰网格：#ececf0 水平参考线。
- 红色虚线参考线：#c0504d，标注文字同色。
- 旋转 Y 轴标题（transform rotate(-90)）。
- 数值标签 bold，置于柱顶上方。
- 配色 seaborn deep：正常柱 #4C72B0(蓝) / 异常强调柱 #DD8452(橙)，
  描边分别 #2f4b73 / #b5651d。禁渐变/阴影。
- 字体三级：标题 14.5 / 标签 11.5~12 / 刻度 10.5（仅 400/500 字重）。

作为模块 import 使用：from academic_chart import vertical_chart
"""
import math

VB_W = 680
VB_H = 348
PLOT_X0 = 72          # y 轴 x 坐标
PLOT_X1 = 620         # 绘图右边界
PLOT_Y0 = 48          # 绘图顶部
PLOT_Y1 = 300         # x 轴(底部)
BAR_W = 76
FONT = "'Microsoft YaHei','PingFang SC','Noto Sans CJK SC',sans-serif"

BLUE = "#4C72B0"
BLUE_S = "#2f4b73"
ORANGE = "#DD8452"
ORANGE_S = "#b5651d"
AXIS = "#555"
GRID = "#ececf0"
REF = "#c0504d"
INK = "#1a1a1a"
GREY = "#777"
LAB = "#333"


def _nice_step(v):
    """给定最大值，返回约 3~4 个刻度的『漂亮』步长。"""
    if v <= 0:
        return 1.0
    raw = v / 4.0
    mag = 10 ** math.floor(math.log10(raw))
    norm = raw / mag
    if norm <= 1:
        step = mag
    elif norm <= 2:
        step = 2 * mag
    elif norm <= 5:
        step = 5 * mag
    else:
        step = 10 * mag
    return float(step)


def _fmt(v):
    """数值标签：保留最多 2 位小数，去尾零。"""
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s


def vertical_chart(title, y_axis_title, unit, bars, ref=None, x_caption=None):
    """
    生成竖向条形图 SVG 字符串（LF 换行）。

    bars: list of (label, value, highlight)
          highlight=True -> 橙色异常强调柱（默认蓝）。
    ref:  (value, label_text) 可选红色虚线参考线（如基线值）。
    unit: 轴单位中文，如 'ms'（数值标签后缀）。
    x_caption: 底部 x 轴总标题（可选）。
    """
    n = len(bars)
    if n == 0:
        raise ValueError("bars 不能为空")
    max_v = max(b[1] for b in bars)
    step = _nice_step(max_v)
    y_max = math.ceil(max_v / step) * step
    if y_max <= 0:
        y_max = step
    ticks = list(range(0, int(y_max) + 1, int(step)))
    if ticks[-1] != int(y_max):
        ticks.append(int(y_max))

    def y_px(v):
        return PLOT_Y1 - (v - 0.0) / (y_max - 0.0) * (PLOT_Y1 - PLOT_Y0)

    # 柱几何：居中排布，柱宽 76，间距上限 120。
    if n > 1:
        gap = min(120.0, (PLOT_X1 - PLOT_X0 - n * BAR_W) / (n - 1))
    else:
        gap = 0.0
    group_w = n * BAR_W + (n - 1) * gap
    start_x = PLOT_X0 + (PLOT_X1 - PLOT_X0 - group_w) / 2.0

    L = []
    L.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VB_W} {VB_H}" '
             f'font-family="{FONT}" font-size="13">')
    L.append(f'  <rect x="0" y="0" width="{VB_W}" height="{VB_H}" fill="#ffffff"/>')
    L.append(f'  <text x="{VB_W // 2}" y="24" text-anchor="middle" font-size="14.5" '
             f'font-weight="bold" fill="{INK}">{title}</text>')
    # 坐标轴
    L.append(f'  <line x1="{PLOT_X0}" y1="{PLOT_Y0}" x2="{PLOT_X0}" y2="{PLOT_Y1}" '
             f'stroke="{AXIS}" stroke-width="1"/>')
    L.append(f'  <line x1="{PLOT_X0}" y1="{PLOT_Y1}" x2="{PLOT_X1}" y2="{PLOT_Y1}" '
             f'stroke="{AXIS}" stroke-width="1"/>')
    # 网格 + y 刻度
    for t in ticks:
        if t == 0:
            continue
        yy = y_px(t)
        L.append(f'  <line x1="{PLOT_X0}" y1="{yy:.1f}" x2="{PLOT_X1}" y2="{yy:.1f}" '
                 f'stroke="{GRID}" stroke-width="1"/>')
    # 参考线
    if ref is not None:
        rv, rlabel = ref
        ry = y_px(rv)
        L.append(f'  <line x1="{PLOT_X0}" y1="{ry:.1f}" x2="{PLOT_X1}" y2="{ry:.1f}" '
                 f'stroke="{REF}" stroke-width="0.8" stroke-dasharray="4 3"/>')
        L.append(f'  <text x="{PLOT_X1}" y="{ry - 4:.1f}" text-anchor="end" '
                 f'fill="{REF}" font-size="9.5">{rlabel}</text>')
    # y 刻度标签 + 刻度线
    for t in ticks:
        yy = y_px(t)
        L.append(f'  <line x1="{PLOT_X0}" y1="{yy:.1f}" x2="{PLOT_X0 - 5}" y2="{yy:.1f}" '
                 f'stroke="{AXIS}" stroke-width="1"/>')
        L.append(f'  <text x="{PLOT_X0 - 9}" y="{yy + 3.5:.1f}" text-anchor="end" '
                 f'fill="{AXIS}" font-size="10.5">{t}</text>')
    # 旋转 Y 轴标题
    mid_y = (PLOT_Y0 + PLOT_Y1) / 2.0
    L.append(f'  <text x="34" y="{mid_y:.0f}" text-anchor="middle" '
             f'transform="rotate(-90 34 {mid_y:.0f})" fill="{GREY}" font-size="11">'
             f'{y_axis_title}</text>')
    # 柱 + 数值标签 + 类别标签
    for i, (label, val, hl) in enumerate(bars):
        bx = start_x + i * (BAR_W + gap)
        by = y_px(val)
        h = PLOT_Y1 - by
        fill = ORANGE if hl else BLUE
        stroke = ORANGE_S if hl else BLUE_S
        L.append(f'  <rect x="{bx:.1f}" y="{by:.1f}" width="{BAR_W}" height="{h:.1f}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="0.75"/>')
        L.append(f'  <text x="{bx + BAR_W / 2:.1f}" y="{by - 6:.1f}" text-anchor="middle" '
                 f'fill="{INK}" font-weight="bold" font-size="12">{_fmt(val)}{unit}</text>')
        L.append(f'  <text x="{bx + BAR_W / 2:.1f}" y="320" text-anchor="middle" '
                 f'fill="{LAB}" font-size="11.5">{label}</text>')
    # x 轴总标题
    if x_caption:
        L.append(f'  <text x="{(PLOT_X0 + PLOT_X1) / 2:.0f}" y="338" text-anchor="middle" '
                 f'fill="{GREY}" font-size="11">{x_caption}</text>')
    L.append('</svg>')
    return "\n".join(L)


if __name__ == "__main__":
    # 自测：复刻 ch151 图2 的几何，确认生成器可用。
    demo = vertical_chart(
        "自测：虚函数分派开销拆解（ms，越低越好）",
        "耗时（ms）", "ms",
        [("inline", 57.1, False), ("branch", 88.8, False),
         ("virtual(devirt)", 48.0, False), ("virtual(real)", 228.8, True)],
        ref=(64.6, "其余均值 ≈64.6 ms"),
    )
    print(demo)
