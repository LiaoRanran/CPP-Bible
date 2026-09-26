"""643 B2 · **攻击面未覆盖扫描器**（智能层：自动发现问题 #2）。

**定位**：基于 629 的 **35 向量攻击面分类学**，自动评出每个向量的**覆盖深度**，
输出"攻击面盲区清单"。回答 inbox B2 的三问：
① 哪些向量只有结构性探针、没有动态攻击复现？② 哪些只测了"防御机制存在"、没测"真的拦住了"？
③ 哪些向量的 `known_error_rate` 是"无数据"？

**覆盖深度评级（0–4，机械可复算）**：

| 深度 | 名称 | 判据（全部来自**在册数据**，可逐条核） |
|---|---|---|
| 0 | 未触达 | 无探针 **且** 无真实事件 |
| 1 | 结构性 | 有探针（`coverage_metric_630.probe_ready`）—— 只证明"防御机制存在" |
| 2 | 动态复现 | 有**真实发生过的**攻击事件（`real_event`）或被 630 实跑过（`exercised_by_630`） |
| 3 | 拦截验证 | 深度 1+2 且该向量的事件**有修复记录**（`attack_mapping_629` 的 `status="已修"`） |
| 4 | 回归锁定 | 深度 3 且 **有代码/测试引用该向量 id**（扫 `tools/`、`tests/` 字面量） |

**诚实边界**：
- 深度 3 的"修复即拦截"是**推断**（修复事件 ⇒ 该类攻击已被拦），**不是**直接的 blocked 记录
  ⇒ 已在输出里标 `inferred: True`；
- 深度 4 用"向量 id 字面量被引用"作代理，**可能漏**（测试可能不写 id 而写语义）；
- `known_error_rate` 的"无数据"是**全库性**结论：642 追踪器 67 条规则**全是代理初值**
  （`n_with_samples=0`）⇒ 35 向量当前**无一**有自身错误率数据；本工具只把这个事实**归到向量**上。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_attack_gap.md` + `.json`。
纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import attack_mapping_629 as am  # noqa: E402
import attack_surface_taxonomy as ast  # noqa: E402
import calibration_tracker_642 as ct  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_attack_gap.md")
OUT_JSON = os.path.join(ROOT, "data", "643_attack_gap.json")
COV630 = os.path.join(ROOT, "data", "coverage_metric_630.json")
DEPTH_NAMES = {0: "未触达", 1: "结构性", 2: "动态复现", 3: "拦截验证", 4: "回归锁定"}
FIXED_STATUS = "已修"


def coverage_630() -> dict[str, Any]:
    try:
        return json.loads(open(COV630, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        return {}


# ── 深度判据（纯函数，可用合成输入测试）─────────────────────────────────────
def depth_of(vid: str, has_probe: bool, real_event: set[str],
             exercised: set[str], fixed: set[str]) -> tuple[int, list[str]]:
    """返回 (深度, 理由列表)。判据顺序固定：0 → 1 → 2 → 3（深层需先满足浅层）。"""
    why: list[str] = []
    if not has_probe and vid not in real_event:
        return 0, ["无探针且无真实事件"]
    if has_probe:
        why.append("有结构性探针")
    if vid in real_event or vid in exercised:
        why.append("有真实攻击事件" if vid in real_event else "被 630 实跑过")
    else:
        return 1, why + ["（仅结构性：没有动态复现记录）"]
    if vid in fixed:
        why.append("事件有修复记录（**推断**为已拦）")
    else:
        return 2, why + ["（有动态复现，但无修复记录 ⇒ 未验证「真的拦住」）"]
    return 3, why                      # 4 由引用扫描单独提升，见 assess()


#: 引用扫描时**必须排除**的文件：它们**定义/汇总**向量 id，不构成"回归锁定"
SKIP_REF_FILES = frozenset({
    "tools/attack_surface_taxonomy.py",      # 向量定义源
    "tools/attack_mapping_629.py",           # 事件映射表（含 id）
    "tools/coverage_metric_630.py",          # 覆盖度量（含 id 列表）
    "tools/attack_gap_scanner_643.py",       # 本工具（自带 id 逻辑）
})


def reference_index(vids: list[str]) -> dict[str, list[str]]:
    """一次性扫描 `tools/`+`tests/`，返回 `vid -> [文件]`（深度 4 的代理判据）。

    **性能**：每个文件只读一次（先前的实现是"每向量扫全目录"，35×1150 次读盘 = 不可接受）。
    """
    idx: dict[str, list[str]] = {v: [] for v in vids}
    pats = {v: (f"'{v}'", f'"{v}"') for v in vids}
    for sub in ("tools", "tests"):
        d = os.path.join(ROOT, sub)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith(".py"):
                continue
            rel = f"{sub}/{name}"
            if rel in SKIP_REF_FILES:
                continue
            try:
                txt = open(os.path.join(d, name), encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for v, (p1, p2) in pats.items():
                if p1 in txt or p2 in txt:
                    idx[v].append(rel)
    return idx


def assess() -> dict[str, Any]:
    cov = coverage_630()
    probe_ready = set(cov.get("probe_ready", []))
    real_event = set(cov.get("real_event", []))
    exercised = set(cov.get("exercised_by_630", []))
    ran = set(cov.get("ran", []))
    never_run = set(cov.get("never_run", []))
    events = am.events()
    fixed = {e["vector"] for e in events if e.get("status") == FIXED_STATUS}
    ev_by_vec: dict[str, list[dict[str, Any]]] = {}
    for e in events:
        ev_by_vec.setdefault(e["vector"], []).append(e)

    rows = []
    vlist = ast.vectors()
    refs_idx = reference_index([v["id"] for v in vlist])
    for v in vlist:
        vid = v["id"]
        has_probe = vid in probe_ready or bool(v.get("probe"))
        d, why = depth_of(vid, has_probe, real_event, exercised, fixed)
        refs = refs_idx.get(vid, [])
        if d == 3 and refs:
            d = 4
            why.append(f"有代码/测试引用（{len(refs)} 处）⇒ 回归锁定")
        elif d < 4:
            why.append("无代码/测试引用 ⇒ 未锁定回归" if d >= 1 else "无引用")
        rows.append({"id": vid, "layer": v["layer"], "name": v["name"], "risk": v["risk"],
                     "has_probe": has_probe, "depth": d, "depth_name": DEPTH_NAMES[d],
                     "real_event": vid in real_event, "ran_in_630": vid in ran,
                     "fixed_events": sorted({e.get("source", "") for e in ev_by_vec.get(vid, [])
                                             if e.get("status") == FIXED_STATUS}),
                     "refs": refs, "why": why,
                     "inferred": d == 3,
                     "no_error_data": True,
                     "desc": v.get("desc", "")})

    # known_error_rate 数据面（全库性结论，见 docstring）
    tracker = ct.build_tracker()
    snap = tracker.snapshot()
    by_depth = {d: sum(1 for r in rows if r["depth"] == d) for d in range(5)}
    dead = [r for r in rows if r["depth"] <= 1]         # 只有结构性或未触达
    return {"rows": rows, "n_vectors": len(rows), "by_depth": by_depth,
            "depth_names": DEPTH_NAMES,
            "only_structural": [r["id"] for r in rows if r["depth"] == 1],
            "untouched": [r["id"] for r in rows if r["depth"] == 0],
            "never_run_in_630": sorted(never_run),
            "no_error_data_all": bool(snap["n_with_samples"] == 0),
            "tracker_snapshot": {k: snap[k] for k in ("n_rules", "n_with_samples",
                                                      "n_proxy", "n_log_entries")},
            "risky_low_depth": [r["id"] for r in dead if r["risk"] == "high"],
            "coverage_630_pct": cov.get("coverage_pct"),
            "n_fixed_vectors": len(fixed)}


def write_report() -> str:
    a = assess()
    bd = a["by_depth"]
    lines = [
        "# 643 B2 · 攻击面未覆盖扫描（智能层 #2：自动发现问题）", "",
        f"> 数据源：`attack_surface_taxonomy.vectors()`（**{a['n_vectors']} 向量**，629 定义）+ "
        "`data/coverage_metric_630.json` + `attack_mapping_629.events()`（23 事件）+ "
        "`tools/`、`tests/` 的字面量引用扫描。",
        f"> 630 三口径：`coverage_pct={a['coverage_630_pct']}`、"
        f"`never_run={len(a['never_run_in_630'])}` 个、有修复记录的向量 {a['n_fixed_vectors']} 个。", "",
        "## 一、覆盖深度分布（0–4）", "",
        "| 深度 | 名称 | 向量数 | 含义 |", "|---|---|---|---|"]
    meaning = {0: "未触达（无探针无事件）", 1: "只有结构性探针（证明机制存在，未证明拦住）",
               2: "有动态复现（未验证'真的拦住'）", 3: "有修复记录 ⇒ **推断**已拦",
               4: "已回归锁定（有代码/测试引用）"}
    for d in range(5):
        lines.append(f"| {d} | {a['depth_names'][d]} | **{bd[d]}** | {meaning[d]} |")
    lines += ["", f"**高风险但低深度（≤1）的向量**（P0 候选）："
              f"{', '.join('`%s`' % x for x in a['risky_low_depth']) or '（无）'}", "",
              "## 二、盲区清单", "",
              f"- **只有结构性探针（深度 1）**：{', '.join('`%s`' % x for x in a['only_structural']) or '（无）'}",
              f"- **未触达（深度 0）**：{', '.join('`%s`' % x for x in a['untouched']) or '（无）'}",
              f"- **630 里从未实跑**：{', '.join('`%s`' % x for x in a['never_run_in_630']) or '（无）'}",
              f"- **`known_error_rate` 全库无数据**：**{a['no_error_data_all']}** "
              f"（追踪器 `{a['tracker_snapshot']}` ⇒ 67 条规则**全为代理初值**，"
              "35 向量**无一**有自身错误率数据）", "",
              "## 三、逐向量明细", "",
              "| 向量 | 层 | 名称 | risk | 探针 | 深度 | 真实事件 | 修复记录 | 引用 | 判据 |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(a["rows"], key=lambda x: (x["depth"], x["id"])):
        lines.append(f"| `{r['id']}` | {r['layer']} | {r['name']} | {r['risk']} | "
                     f"{'✅' if r['has_probe'] else '—'} | **{r['depth']} {r['depth_name']}** | "
                     f"{'✅' if r['real_event'] else '—'} | "
                     f"{'✅' if r['fixed_events'] else '—'} | {len(r['refs'])} | "
                     f"{'；'.join(r['why'])} |")
    lines += ["", "## 诚实登记", "",
              "1. **自动发现问题 ≠ 问题真的存在**（§十二.1）：深度评级是**启发式**，"
              "清单需人复核；",
              "2. **深度 3 = 推断**（`status=\"已修\"` ⇒ 该类攻击已被拦），**不是**直接的 blocked 记录 ⇒ "
              "输出里逐条标 `inferred: True`；",
              "3. **深度 4 的判据是「向量 id 字面量被引用」，可能漏**（测试可能写语义不写 id）"
              "⇒ 深度 4 是**下界**；且已排除**定义/汇总类**文件（`SKIP_REF_FILES`："
              "分类学、事件映射、覆盖度量、本工具），否则所有向量都会被自己「引用」而虚高；",
              "4. **结构 100% vs 深度不足**：632 的 `coverage_pct` 是按\"有探针/有事件\"算的**结构性覆盖**，"
              "与\"真的拦住了\"**不是一回事** —— 这正是本工具要照出的差距；",
              "5. **沙箱 vs 生产**：630 的实跑发生在沙箱/受控路径，与生产 gate 行为可能有差异"
              "（§十二.6）；",
              "6. 本工具**只读**：不改向量定义、不改 coverage 台账、不跑攻击。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(a, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 合成判据测试
    chk("无探针无事件 ⇒ 深度 0", depth_of("X", False, set(), set(), set())[0] == 0)
    chk("仅探针 ⇒ 深度 1", depth_of("X", True, set(), set(), set())[0] == 1)
    chk("探针 + 真实事件 ⇒ 深度 2", depth_of("X", True, {"X"}, set(), set())[0] == 2)
    chk("无探针但有事件 ⇒ 不再停在 0",
        depth_of("X", False, {"X"}, set(), set())[0] >= 2)
    chk("三类都有 ⇒ 深度 3（推断）", depth_of("X", True, {"X"}, set(), {"X"})[0] == 3)
    chk("深度单调：深层必满足浅层",
        depth_of("X", True, {"X"}, set(), {"X"})[0] > depth_of("X", True, {"X"}, set(), set())[0])

    a = assess()
    chk("35 向量全覆盖", a["n_vectors"] == 35, str(a["n_vectors"]))
    chk("深度分布覆盖 0–4 档且计数自洽",
        sum(a["by_depth"].values()) == 35, str(a["by_depth"]))
    chk("已知低深度向量被标（深度≤1 清单非空）",
        len(a["only_structural"]) + len(a["untouched"]) > 0,
        f"struct={len(a['only_structural'])} untouched={len(a['untouched'])}")
    chk("known_error_rate 无数据结论有据（追踪器 n_with_samples）",
        a["tracker_snapshot"]["n_with_samples"] == 0)
    chk("深度 3 条目都带 inferred 标记",
        all(r["inferred"] for r in a["rows"] if r["depth"] == 3))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 B2 攻击面盲区扫描")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印分析（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    a = assess()
    if x.json:
        print(json.dumps({"by_depth": a["by_depth"], "only_structural": a["only_structural"],
                          "untouched": a["untouched"],
                          "risky_low_depth": a["risky_low_depth"]},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[attack-gap] {a['n_vectors']} 向量 ⇒ 深度分布 {a['by_depth']}；"
          f"高风险低深度 {len(a['risky_low_depth'])} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
