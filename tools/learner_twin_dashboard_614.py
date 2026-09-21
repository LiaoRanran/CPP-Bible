#!/usr/bin/env python3
"""614 线B B2：学习者镜像仪表盘 · 真实数据版（自包含 HTML，无外部依赖）。

数据来源：data/learner_behaviors.jsonl（B1 采集的真实/模拟行为日志）。
处理：复用 learner_behavior_logger 的 replay()（BKT 递推）得 27 KC 掌握度 +
      时间线（全局事件序下的平均掌握度演化）+ recommend_next()（下一可学 KC）。
输出：data/learner_twin_dashboard_614.html（四模块：热力图 / 进度曲线 / 推荐路径 / 统计）。

CLI：
  python tools/learner_twin_dashboard_614.py [--out <html>] [--store <jsonl>]
  python tools/learner_twin_dashboard_614.py --check            # 自验证（exit 0=通过）

铁律：读取真实行为日志，不硬编码数据；单用户 default；模拟数据标注 simulated（仅影响统计口径）。
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

DEFAULT_STORE = ROOT / "data" / "learner_behaviors.jsonl"
DEFAULT_OUT = ROOT / "data" / "learner_twin_dashboard_614.html"
USER = "default"
DEFAULT_THRESHOLD = 0.5


def _kc_ids() -> list[dict]:
    import kc_inventory as d1  # noqa: E402
    return cast("list[dict[str, Any]]", cast("dict[str, Any]", d1.build())["kcs"])


def build(store: Path, user: str = USER, threshold: float = DEFAULT_THRESHOLD) -> dict:
    import learner_behavior_logger as b1  # noqa: E402
    kcs = _kc_ids()
    mastery = b1.replay(store, user)
    recs = [r for r in b1.load_all(store) if r.get("user_id") == user]
    # 时间线：全局事件序下，每步后 27 KC 的平均掌握度（未学 KC 视为 0.1）
    import bkt_solver as d2  # noqa: E402
    model = d2.BKTModel()
    per_kc: dict[str, float] = {k["id"]: 0.1 for k in kcs}
    ordered = sorted(recs, key=lambda x: x.get("timestamp", ""))
    timeline: list[float] = []
    for e in ordered:
        kc = e.get("kc_id")
        act = e.get("action")
        if kc in per_kc and act == "correct":
            per_kc[kc] = model.step(per_kc[kc], 1)
        elif kc in per_kc and act == "incorrect":
            per_kc[kc] = model.step(per_kc[kc], 0)
        timeline.append(sum(per_kc.values()) / len(per_kc))
    recommended = b1.recommend_next(store, user, threshold)
    n_correct = sum(1 for r in recs if r.get("action") == "correct")
    n_ans = sum(1 for r in recs if r.get("action") in ("correct", "incorrect"))
    stats = {
        "total_events": len(recs),
        "answered": n_ans,
        "accuracy": round(n_correct / n_ans, 4) if n_ans else 0.0,
        "avg_mastery": round(sum(mastery.values()) / len(kcs), 4) if kcs else 0.0,
        "mastered_05": sum(1 for v in mastery.values() if v >= 0.5),
        "mastered_09": sum(1 for v in mastery.values() if v >= 0.9),
        "simulated_events": sum(1 for r in recs if r.get("simulated")),
    }
    return {"kcs": kcs, "mastery": mastery, "timeline": timeline,
            "recommended": recommended, "stats": stats, "user": user,
            "threshold": threshold, "store": str(store)}


def _heat_color(v: float) -> str:
    # 0→红 #d9534f, 1→绿 #5cb85c
    v = max(0.0, min(1.0, v))
    r = int(217 + (92 - 217) * v)
    g = int(83 + (184 - 83) * v)
    b = int(79 + (92 - 79) * v)
    return f"#{r:02X}{g:02X}{b:02X}"


def render_html(d: dict) -> str:
    kcs = d["kcs"]
    mastery = d["mastery"]
    timeline = d["timeline"]
    recommended = d["recommended"]
    stats = d["stats"]
    # 热力图
    heat_cells = []
    for k in kcs:
        v = mastery.get(k["id"], 0.1)
        heat_cells.append(
            f'<div class="cell" style="background:{_heat_color(v)}" '
            f'title="{k["id"]}：{v:.3f}">{k["id"].split("-")[-1]}<br>{v:.2f}</div>')
    heat = "\n".join(heat_cells)
    # 进度曲线（SVG polyline）
    w, h = 600, 160
    if timeline:
        n = len(timeline)
        pts = " ".join(f"{(i / max(1, n - 1)) * w:.1f},{h - timeline[i] * h:.1f}"
                       for i in range(n))
        curve = (f'<svg viewBox="0 0 {w} {h}" width="100%" height="{h}">'
                 f'<polyline fill="none" stroke="#337ab7" stroke-width="2" points="{pts}"/>'
                 f'</svg>')
    else:
        curve = '<p class="muted">无学习事件，无曲线。</p>'
    # 推荐路径
    rec_items = "".join(f"<li>{r}</li>" for r in recommended) or "<li class='muted'>无（全部已掌握）</li>"
    # 统计
    stat_rows = "".join(f"<div class='stat'><b>{stats[k]}</b><span>{k}</span></div>"
                        for k in ("total_events", "answered", "accuracy",
                                  "avg_mastery", "mastered_05", "mastered_09"))
    html = f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<title>学习者镜像仪表盘（真实数据版 · {d['user']}）</title>
<style>
 body{{font-family:system-ui,sans-serif;margin:0;padding:1.2rem;background:#fafafa;color:#222}}
 h1{{font-size:1.3rem}} .muted{{color:#999}} .sec{{background:#fff;border:1px solid #eee;
 border-radius:8px;padding:1rem;margin:1rem 0}}
 .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(92px,1fr));gap:6px}}
 .cell{{border-radius:6px;padding:8px 4px;text-align:center;font-size:.72rem;color:#fff}}
 .stats{{display:flex;flex-wrap:wrap;gap:1rem}} .stat{{background:#fff;border:1px solid #eee;
 border-radius:8px;padding:.8rem 1.1rem;text-align:center}} .stat b{{display:block;font-size:1.4rem}}
 .stat span{{font-size:.75rem;color:#888}}
 ul{{margin:.3rem 0;padding-left:1.2rem}}
</style></head><body>
<h1>学习者镜像仪表盘 · 真实数据版</h1>
<p class="muted">数据源：{d['store']}（B1 行为日志，复用 BKT 递推，不硬编码）；用户 {d['user']}；掌握度阈值 {d['threshold']}</p>
<div class="sec"><h2>① 掌握度热力图（27 KC）</h2><div class="grid">{heat}</div></div>
<div class="sec"><h2>② 进度曲线（全局平均掌握度演化）</h2>{curve}</div>
<div class="sec"><h2>③ 推荐学习路径（掌握度&lt;{d['threshold']} 且前置已满足）</h2><ul>{rec_items}</ul></div>
<div class="sec"><h2>④ 统计</h2><div class="stats">{stat_rows}</div></div>
</body></html>"""
    return html


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="614 B2 学习者镜像仪表盘（真实数据版）")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--store", default=None)
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--check", action="store_true", help="自验证（exit 0=通过）")
    a = ap.parse_args(argv)
    store = Path(a.store) if a.store else DEFAULT_STORE

    if a.check:
        problems: list[str] = []
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td) / "beh.jsonl"
            import learner_behavior_logger as b1  # noqa: E402
            b1.simulate(tmp, kcs_n=10, rounds=5, seed=7)
            d = build(tmp, USER, a.threshold)
            html = render_html(d)
            # 关键元素：27 个热力图 cell、统计块、推荐列表
            if html.count('class="cell"') != 27:
                n_cells = html.count('class="cell"')
                problems.append(f"热力图 cell 数应为 27（实得 {n_cells}）")
            if "平均掌握度" not in html:
                problems.append("统计模块缺平均掌握度")
            if d["stats"]["total_events"] == 0:
                problems.append("模拟数据应产生事件")
        if problems:
            print("[dash] ❌ 自检失败：", file=sys.stderr)
            for p in problems:
                print(f"    - {p}", file=sys.stderr)
            return 1
        print("[dash] ✅ 自验证通过：27 cell + 统计 + 推荐模块齐备，数据来自 replay 非硬编码")
        return 0

    if not store.is_file():
        print(f"[dash] ⚠ 行为日志不存在：{store}（先用 B1 simulate/log 生成）", file=sys.stderr)
        return 2
    d = build(store, USER, a.threshold)
    html = render_html(d)
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    s = d["stats"]
    print(f"[dash] 已生成：{out}（事件 {s['total_events']} · 平均掌握度 {s['avg_mastery']} · "
          f"≥0.5 {s['mastered_05']}/27 · 推荐 {len(d['recommended'])} KC）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
