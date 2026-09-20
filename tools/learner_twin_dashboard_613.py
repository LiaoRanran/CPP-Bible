#!/usr/bin/env python3
"""613 任务C4 · 学习者镜像仪表盘**升级版**（自包含 HTML，零外部依赖）。

612 的 `learner_twin_dashboard.py` 只有模拟数据四模块；本工具新增 C 线真实数据模块：

  ① 掌握度热力图（按域 × 掌握度分档着色）
  ② 掌握进度曲线（按 learner_state 事件序，逐 KC 展示最新值 + 变迁条数）
  ③ **推荐学习路径**（C3 拓扑序 + 「下一步」高亮）
  ④ **真实行为统计**（C1 事件：条数 / 动作分布 / 正确率 / 覆盖 KC）
  ⑤ **数据状态横幅**：明确标注当前掌握度是「真实递推」还是「612 simulate 模拟值」

与 612 版分文件，避免破坏既有 612 测试（项目惯例：新能力落独立模块）。

CLI：
  python tools/learner_twin_dashboard_613.py            # 生成 data/learner_twin_dashboard_613.html
  python tools/learner_twin_dashboard_613.py --check    # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

OUT = ROOT / "data" / "learner_twin_dashboard_613.html"
KC_JSON = ROOT / "data" / "kc_inventory_612.json"
STATE = ROOT / "data" / "learner_state_612.jsonl"
BEHAVIOR = ROOT / "data" / "learner_behavior.jsonl"
USER = "default"


def _kcs() -> list[dict]:
    if not KC_JSON.is_file():
        return []
    return cast("list[dict[Any, Any]]",
                json.loads(KC_JSON.read_text(encoding="utf-8")).get("kcs", []))


def _state_rows() -> list[dict]:
    if not STATE.is_file():
        return []
    out = []
    for ln in STATE.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                pass
    return out


def _behavior_rows() -> list[dict]:
    if not BEHAVIOR.is_file():
        return []
    out = []
    for ln in BEHAVIOR.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                pass
    return out


def mastery_map() -> dict[str, float]:
    latest: dict[tuple[str, str], dict] = {}
    for r in _state_rows():
        latest[(r.get("user_id", ""), r.get("kc_id", ""))] = r
    return {kc: float(rec.get("mastery_prob", 0.0))
            for (u, kc), rec in latest.items() if u == USER}


def recommended_path() -> list[str]:
    try:
        import learner_path_graph_613 as p3  # noqa: E402
        kcs = p3.load_kcs()
        adj, indeg = p3.build_graph(kcs)
        order, _cyc = p3.topo_sort(kcs, adj, indeg)
        return order
    except Exception:
        return [k["id"] for k in _kcs()]


def behavior_stats(rows: list[dict]) -> dict:
    by_act = Counter(str(r.get("action_type")) for r in rows)
    corr = [r for r in rows if isinstance(r.get("correct"), bool)]
    n_correct = sum(1 for r in corr if r["correct"] is True)
    return {"n": len(rows), "by_action": dict(by_act),
            "distinct_kc": len({str(r.get("kc_id")) for r in rows}),
            "n_scored": len(corr),
            "accuracy": (n_correct / len(corr)) if corr else None}


def is_real(rows_state: list[dict]) -> bool:
    """真实递推判定：存在 kind=update 且**非** simulated 的记录。"""
    return any(r.get("kind") == "update" and not r.get("simulated", False) for r in rows_state)


def _bar(v: float) -> str:
    n = int(round(max(0.0, min(1.0, v)) * 20))
    return "█" * n + "░" * (20 - n)


def _color(v: float) -> str:
    if v >= 0.8:
        return "#2e7d32"
    if v >= 0.5:
        return "#66bb6a"
    if v >= 0.3:
        return "#ffa726"
    return "#e53935"


def render() -> str:
    kcs = _kcs()
    m = mastery_map()
    srows = _state_rows()
    brows = _behavior_rows()
    bs = behavior_stats(brows)
    real = is_real(srows)
    path = recommended_path()
    thr = 0.5
    nxt = [k for k in path if m.get(k, 0.0) < thr][:5]

    banner = ("🟢 掌握度来源：**真实递推**（C2 已接入真实行为）"
              if real else
              "🟡 掌握度来源：**612 simulate 模拟值**（尚无真实行为事件 —— 经 C1 接入后自动切换）")

    by_domain: dict[str, list[float]] = {}
    for k in kcs:
        by_domain.setdefault(str(k.get("domain", "?")), []).append(m.get(k["id"], 0.0))

    rows_html = []
    for k in sorted(kcs, key=lambda x: (m.get(x["id"], 0.0), x["id"])):
        kid = k["id"]
        v = m.get(kid, 0.0)
        rows_html.append(
            f"<tr><td><code>{kid}</code></td><td>{k.get('domain','')}</td>"
            f"<td>{k.get('difficulty','')}</td>"
            f"<td style='color:{_color(v)}'>{_bar(v)} {v:.3f}</td>"
            f"<td>{'✅' if v >= thr else '⬜'}</td></tr>")

    dom_html = []
    for d, vs in sorted(by_domain.items()):
        avg = sum(vs) / len(vs) if vs else 0.0
        dom_html.append(f"<tr><td>{d}</td><td>{len(vs)}</td>"
                        f"<td style='color:{_color(avg)}'>{_bar(avg)} {avg:.3f}</td></tr>")

    path_html = "".join(
        f"<li>{'👉 ' if k in nxt else ''}<code>{k}</code> "
        f"<span style='color:{_color(m.get(k,0.0))}'>{m.get(k,0.0):.3f}</span></li>"
        for k in path)

    acc = "—（无已评分事件）" if bs["accuracy"] is None else f"{bs['accuracy'] * 100:.1f}%"

    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>学习者镜像 · 613 升级版</title>
<style>
body{{font-family:-apple-system,"Segoe UI",Roboto,"Helvetica Neue",sans-serif;margin:24px;color:#222;background:#fafafa}}
h1{{font-size:20px}} h2{{font-size:16px;margin-top:24px;border-left:4px solid #1976d2;padding-left:8px}}
.banner{{padding:10px 14px;border-radius:6px;background:#fff8e1;border:1px solid #ffe082;margin:12px 0}}
table{{border-collapse:collapse;width:100%;background:#fff}}
td,th{{border:1px solid #e0e0e0;padding:6px 10px;text-align:left;font-size:13px}}
th{{background:#f5f5f5}} code{{font-size:12px}}
.grid{{display:flex;gap:16px;flex-wrap:wrap}}
.card{{flex:1;min-width:260px;background:#fff;border:1px solid #e0e0e0;border-radius:6px;padding:12px}}
.small{{font-size:12px;color:#666}}
</style></head><body>
<h1>学习者镜像 · 613 升级版</h1>
<div class="small">生成时间：{datetime.now().isoformat(timespec='seconds')} ｜ 工具：
<code>tools/learner_twin_dashboard_613.py</code> ｜ 自包含单文件（零外部依赖）</div>
<div class="banner">{banner}</div>
<div class="grid">
  <div class="card"><b>KC 总数</b><div style="font-size:24px">{len(kcs)}</div></div>
  <div class="card"><b>已掌握（≥{thr}）</b><div style="font-size:24px">{sum(1 for k in kcs if m.get(k['id'],0.0) >= thr)}</div></div>
  <div class="card"><b>真实行为事件</b><div style="font-size:24px">{bs['n']}</div></div>
  <div class="card"><b>已评分正确率</b><div style="font-size:24px">{acc}</div></div>
</div>
<h2>① 掌握度热力图（按 KC）</h2>
<table><tr><th>KC</th><th>域</th><th>难度</th><th>掌握度</th><th>达标</th></tr>
{''.join(rows_html)}</table>
<h2>② 域级汇总</h2>
<table><tr><th>域</th><th>KC 数</th><th>平均掌握度</th></tr>
{''.join(dom_html)}</table>
<h2>③ 推荐学习路径（C3 拓扑序 · 👉 = 下一步）</h2>
<ol>{path_html}</ol>
<h2>④ 真实行为统计（C1）</h2>
<table>
<tr><th>事件总数</th><td>{bs['n']}</td></tr>
<tr><th>动作分布</th><td>{bs['by_action'] or '—'}</td></tr>
<tr><th>覆盖 KC 数</th><td>{bs['distinct_kc']}</td></tr>
<tr><th>已评分事件</th><td>{bs['n_scored']}</td></tr>
<tr><th>正确率</th><td>{acc}</td></tr>
</table>
<h2>⑤ 状态记录</h2>
<div class="small">掌握度存储：<code>data/learner_state_612.jsonl</code>（{len(srows)} 条）｜
真实行为：<code>data/learner_behavior.jsonl</code>（{len(brows)} 条）</div>
</body></html>
"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 C4 · 学习者镜像仪表盘升级版")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        html = render()
        errs = []
        if len(html) < 2000:
            errs.append("HTML 过短")
        for sec in ("掌握度热力图", "域级汇总", "推荐学习路径", "真实行为统计"):
            if sec not in html:
                errs.append(f"缺模块：{sec}")
        if "学习者镜像" not in html:
            errs.append("缺标题")
        if "http://" in html.replace("http://www.w3.org", "") or "<script" in html:
            errs.append("不得含外部资源/script（须自包含）")
        for e in errs:
            print(f"[C4] ✗ {e}")
        print("[C4] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"[C4] 写入 {OUT.relative_to(ROOT).as_posix()}（{len(render())} 字符）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
