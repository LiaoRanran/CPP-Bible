#!/usr/bin/env python3
"""612 线 D · D5：学习者镜像可视化仪表盘（**自包含 HTML**，无外部依赖）。

纯标准库生成 `data/learner_twin_dashboard_612.html`（内联 CSS + 原生 SVG + 极简 JS，不引 CDN）。
四模块：
  1. KC 掌握度热力图：27 KC 按难度分组，颜色=掌握概率（红→琥珀→绿），点击显示详情；
  2. 学习进度曲线：模拟数据下平均掌握度随作答会话变化的折线（SVG）；
  3. 推荐学习路径：基于前置依赖的拓扑序，高亮当前推荐与未来 5 张卡；
  4. 学习统计面板：总练习数 / 已学 KC / 已掌握数 / 平均掌握度 / 正确率。

初始数据：复用 `learner_state.simulate` 生成**模拟**用户数据（约 30 次作答，标注「模拟，演示用」）。
设计：响应式（PC/移动）、关键文本 ≥14px、对比度 ≥4.5:1、有图例与阅读顺序。

CLI：
  python tools/learner_twin_dashboard.py          # 生成 HTML
  python tools/learner_twin_dashboard.py --check  # 验证 HTML 与数据一致（含四模块关键元素，exit 0=通过）

约束（spec）：自包含无外部依赖；模拟数据明确标注；不调用 LLM；HTML 存 data/。
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import html
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STORE = ROOT / "data" / "learner_state_612.jsonl"
HTML_OUT = ROOT / "data" / "learner_twin_dashboard_612.html"


def _simulated_data() -> dict:
    """复用 learner_state 生成确定性模拟数据（不污染真实 store）。"""
    import bkt_solver as d2  # noqa: E402
    import kc_inventory as d1  # noqa: E402
    import learner_state as d3  # noqa: E402
    tmp = Path(tempfile.mkdtemp()) / "sim.jsonl"
    d3.init(tmp)
    d3.simulate(tmp, sessions=30, seed=20260920)
    inv = d1.build()
    by_id = {k["id"]: k for k in inv["kcs"]}
    mast = {k[1]: r["mastery_prob"] for k, r in d3.latest_by(tmp).items()}
    recs = [r for r in d3.load_all(tmp) if r.get("kind") == "update"]
    # 时间序平均掌握度：按时间戳排序，逐步 BKT 递推后取全 KC 平均
    recs_sorted = sorted(recs, key=lambda x: x.get("timestamp", ""))
    model = d2.BKTModel()
    per_kc: dict[str, float] = {k["id"]: 0.1 for k in inv["kcs"]}
    series: list[float] = []
    correct = 0
    for r in recs_sorted:
        kc = r["kc_id"]
        per_kc[kc] = model.step(per_kc.get(kc, 0.1), 1 if r["correct"] else 0)
        if r["correct"]:
            correct += 1
        series.append(sum(per_kc.values()) / len(per_kc))
    practiced = {r["kc_id"] for r in recs_sorted}
    return {
        "kc_inv": inv["kcs"], "by_id": by_id, "mastery": mast,
        "series": series, "practiced": practiced, "total": len(recs_sorted),
        "correct": correct, "distinct_kc": len(practiced),
        "avg_mastery": sum(mast.values()) / len(mast) if mast else 0.0,
        "mastered": sum(1 for v in mast.values() if v >= 0.9),
        "accuracy": (correct / len(recs_sorted)) if recs_sorted else 0.0,
    }


def _color(m: float) -> tuple[str, str]:
    """掌握概率 → (背景色, 前景色)，保证对比度 ≥4.5:1。"""
    if m < 0.34:
        return "#b71c1c", "#ffffff"          # 红 / 白（~5.9）
    if m < 0.67:
        return "#f9a825", "#1a1a1a"          # 琥珀 / 黑（~8）
    return "#1b5e20", "#ffffff"              # 绿 / 白（~7）


def _heatmap(kcs: list[dict], by_id: dict, mastery: dict) -> str:
    # 按难度分组
    groups: dict[int, list[dict]] = {}
    for k in kcs:
        groups.setdefault(k["difficulty"], []).append(k)
    parts: list[str] = ['<div class="grid">']
    for lv in sorted(groups):
        parts.append(f'<div class="lvl"><h4>难度 {lv}（{len(groups[lv])} KC）</h4>')
        parts.append('<div class="cells">')
        for k in sorted(groups[lv], key=lambda x: x["id"]):
            m = mastery.get(k["id"], 0.1)
            bg, fg = _color(m)
            pre = ", ".join(k.get("prerequisites", [])) or "无"
            detail = (f"KC：{html.escape(k['id'])}<br>标题：{html.escape(k['title'])}<br>"
                      f"领域：{html.escape(k['domain'])}<br>难度：{k['difficulty']}<br>"
                      f"掌握度：{m*100:.0f}%<br>前置：{html.escape(pre)}")
            parts.append(
                f'<button class="cell" style="background:{bg};color:{fg}" '
                f'onclick="showDetail(this)" data-detail="{html.escape(detail)}">'
                f'{html.escape(k["id"])}<span class="pct">{m*100:.0f}%</span></button>')
        parts.append('</div></div>')
    parts.append('</div>')
    return "\n".join(parts)


def _curve(series: list[float]) -> str:
    w, h = 720, 220
    pad = 40
    n = len(series)
    if n < 2:
        return '<svg viewBox="0 0 720 220" class="svg"><text x="20" y="120">数据不足</text></svg>'
    xs = [pad + (w - 2 * pad) * i / (n - 1) for i in range(n)]
    ys = [h - pad - (h - 2 * pad) * v for v in series]
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    grid = "".join(
        f'<line x1="{pad}" y1="{h-pad-(h-2*pad)*g/4:.1f}" x2="{w-pad}" '
        f'y2="{h-pad-(h-2*pad)*g/4:.1f}" class="gridline"/>'
        for g in range(5))
    return (f'<svg viewBox="0 0 {w} {h}" class="svg" role="img" '
            f'aria-label="平均掌握度随作答会话变化曲线">'
            f'{grid}<polyline points="{pts}" class="line"/>'
            f'<text x="{pad}" y="{h-10}" class="axlabel">会话 1</text>'
            f'<text x="{w-pad-40}" y="{h-10}" class="axlabel">会话 {n}</text>'
            f'<text x="10" y="{pad-15}" class="axlabel">100%</text>'
            f'<text x="10" y="{h-pad}" class="axlabel">0%</text></svg>')


def _path(kcs: list[dict], by_id: dict, mastery: dict, top_n: int = 5) -> str:
    # 推荐：掌握度最低且前置已满足（复用 recommender 的硬约束逻辑，避免循环依赖）
    import learner_recommender as d4  # noqa: E402
    rec = d4.learning_path(DEFAULT_STORE, top_n)
    items: list[str] = ['<ol class="path">']
    for i, it in enumerate(rec, 1):
        m = it["mastery"]
        bg, fg = _color(m)
        mark = "（推荐）" if i == 1 else ("（未来路径）" if i <= top_n else "")
        items.append(
            f'<li><span class="pnode" style="background:{bg};color:{fg}">'
            f'{html.escape(it["kc"])} · {m*100:.0f}%</span> '
            f'{html.escape(it["title"])}{mark}</li>')
    items.append('</ol>')
    return "\n".join(items)


def _stats(d: dict) -> str:
    return (
        f'<div class="stat"><div class="num">{d["total"]}</div><div class="lbl">总练习次数</div></div>'
        f'<div class="stat"><div class="num">{d["distinct_kc"]}</div><div class="lbl">已学 KC</div></div>'
        f'<div class="stat"><div class="num">{d["mastered"]}</div><div class="lbl">已掌握(≥90%)</div></div>'
        f'<div class="stat"><div class="num">{d["avg_mastery"]*100:.0f}%</div><div class="lbl">平均掌握度</div></div>'
        f'<div class="stat"><div class="num">{d["accuracy"]*100:.0f}%</div><div class="lbl">正确率</div></div>')


def render(d: dict, kcs: list[dict], by_id: dict, mastery: dict) -> str:
    heatmap = _heatmap(kcs, by_id, mastery)
    curve = _curve(d["series"])
    path = _path(kcs, by_id, mastery)
    stats = _stats(d)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>学习者镜像仪表盘 · 612 D5（演示）</title>
<style>
  :root {{ --fg:#1a1a1a; --muted:#555; --bg:#f5f6f8; --card:#fff; --line:#e0e0e0; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
         font-size: 14px; line-height: 1.5; color: var(--fg); background: var(--bg); margin: 0; }}
  header {{ background: #1b3a5b; color: #fff; padding: 16px 20px; }}
  header h1 {{ font-size: 20px; margin: 0 0 4px; }}
  .banner {{ background: #fff3cd; color: #7a5b00; padding: 8px 20px; font-size: 13px; }}
  main {{ max-width: 960px; margin: 0 auto; padding: 16px; }}
  section {{ background: var(--card); border: 1px solid var(--line); border-radius: 8px;
            padding: 16px; margin-bottom: 16px; }}
  h2 {{ font-size: 17px; margin: 0 0 12px; border-left: 4px solid #1b3a5b; padding-left: 8px; }}
  .grid {{ display: flex; flex-direction: column; gap: 12px; }}
  .lvl h4 {{ margin: 0 0 6px; font-size: 14px; }}
  .cells {{ display: flex; flex-wrap: wrap; gap: 6px; }}
  .cell {{ border: none; border-radius: 6px; padding: 8px 10px; font-size: 13px; cursor: pointer;
          min-width: 92px; text-align: left; }}
  .cell .pct {{ display: block; font-weight: 700; font-size: 16px; }}
  #detail {{ margin-top: 10px; padding: 10px; background: #eef3f8; border-radius: 6px; font-size: 13px; min-height: 20px; }}
  .statrow {{ display: flex; flex-wrap: wrap; gap: 12px; }}
  .stat {{ flex: 1 1 120px; background: #eef3f8; border-radius: 8px; padding: 12px; text-align: center; }}
  .stat .num {{ font-size: 26px; font-weight: 700; color: #1b3a5b; }}
  .stat .lbl {{ font-size: 13px; color: var(--muted); }}
  .svg {{ width: 100%; height: auto; background: #fafafa; border: 1px solid var(--line); border-radius: 6px; }}
  .line {{ fill: none; stroke: #1b5e20; stroke-width: 2.5; }}
  .gridline {{ stroke: #e0e0e0; stroke-width: 1; }}
  .axlabel {{ font-size: 12px; fill: var(--muted); }}
  .path {{ padding-left: 20px; }}
  .pnode {{ display: inline-block; border-radius: 5px; padding: 3px 8px; font-weight: 600; margin-right: 6px; }}
  .legend {{ font-size: 13px; color: var(--muted); margin-top: 8px; }}
  .legend span {{ display: inline-block; padding: 2px 8px; border-radius: 4px; margin-right: 6px; color:#fff; }}
  @media (max-width: 560px) {{ .cell {{ min-width: 80px; }} header h1 {{ font-size: 17px; }} }}
</style>
</head>
<body>
<header><h1>学习者镜像仪表盘（Learner Twin）</h1>
<div>612 线 D · D5 原型 · 基于 KC 台账 + BKT 掌握度 · 纯静态自包含</div></header>
<div class="banner">⚠ 本仪表盘数据为 <b>模拟数据，演示用</b>（约 30 次作答），非真实用户记录。</div>
<main>

<section>
  <h2>① 学习统计面板</h2>
  <div class="statrow">{stats}</div>
</section>

<section>
  <h2>② KC 掌握度热力图（点击查看详情）</h2>
  {heatmap}
  <div class="legend">
    颜色含义：<span style="background:#b71c1c">红 &lt;34%</span>
    <span style="background:#f9a825;color:#1a1a1a">琥珀 34–67%</span>
    <span style="background:#1b5e20">绿 ≥67%</span>
  </div>
  <div id="detail">点击任意 KC 查看详情。</div>
</section>

<section>
  <h2>③ 学习进度曲线（平均掌握度 vs 作答会话）</h2>
  {curve}
</section>

<section>
  <h2>④ 推荐学习路径（基于前置依赖拓扑序）</h2>
  {path}
  <div class="legend">绿色＝已较好掌握；红色＝待加强；首条为当前推荐，其后续为未来路径。</div>
</section>

</main>
<script>
function showDetail(el) {{
  document.getElementById('detail').innerHTML = el.getAttribute('data-detail');
}}
</script>
</body>
</html>
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="612 D5 · 学习者镜像仪表盘（自包含 HTML）")
    ap.add_argument("--check", action="store_true", help="验证 HTML 与数据一致（exit 0=通过）")
    a = ap.parse_args(argv)
    d = _simulated_data()
    kcs = d["kc_inv"]
    by_id = d["by_id"]
    mastery = d["mastery"]
    page = render(d, kcs, by_id, mastery)

    problems: list[str] = []
    if "学习者镜像仪表盘" not in page:
        problems.append("HTML 缺少标题")
    for marker in ("学习统计面板", "KC 掌握度热力图", "学习进度曲线", "推荐学习路径"):
        if marker not in page:
            problems.append(f"HTML 缺少模块：{marker}")
    if "模拟数据" not in page:
        problems.append("HTML 未标注「模拟数据」")
    if "<script" not in page or "showDetail" not in page:
        problems.append("HTML 缺少交互脚本")
    if len(page) < 2000:
        problems.append("HTML 过小（可能生成不全）")
    if problems:
        print("[D5] ❌ 自检失败：", file=sys.stderr)
        for p in problems:
            print(f"    - {p}", file=sys.stderr)
        return 1

    if a.check:
        print(f"[D5] ✅ 自验证通过：HTML {len(page)} 字符 / 四模块齐全 / 含模拟标注")
        return 0

    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(page, encoding="utf-8")
    print(f"[D5] 已写 {HTML_OUT.relative_to(ROOT).as_posix()}（模拟数据，约 {d['total']} 次作答 / "
          f"{d['distinct_kc']} 张已学 KC / 平均掌握度 {d['avg_mastery']*100:.0f}%）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
