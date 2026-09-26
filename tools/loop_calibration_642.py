"""642 C2 · 闭环**校准度追踪**（每次闭环运行记「候选数 / 采纳数 / 事后验证结果」）。

**定位**：闭环（637/638）已跑两轮，但"闭环准不准"只有**散落的单次审计**，没有**台账**。
本模块把它落成 **append-only 台账** + 统一口径 + 扩大门槛判定。

三轮数据点（**全部来自已有证据，不重跑、不改上一批产物**）：

| 轮次 | 批次 | 候选 | 已判定 | 成立 | 校准度 | 来源 |
|---|---|---|---|---|---|---|
| R1 | 637 | 8 | 8 | 3 | **37.5%** | `data/637_loop_quality_audit.md`（靠谱 3 / 半靠谱 3 / 不靠谱 2） |
| R2 | 638 | 4 | 4 | 2 | **50.0%** | `data/638_loop_tuning.md`（调前异常 4，误报 2 ⇒ 真异常 2） |
| R3 | **642** | 见报告 | **0** | — | **None（待人审）** | 本批审计/保护器产出，全部交人**未代决** |

**统一口径**：`校准度 = 成立的已判定项 / 已判定项`；**采纳数**单列（未被采纳即无从验证）。
R3 的校准度是 **None**，不是 0 —— 把它写成 0 是**假精确**（§十.6：2 个点不足以判趋势）。

**扩大门槛**：`校准度 > 60%` 才考虑扩大 `auto_executor` 白名单（C1 的输入）。
当前最高观测值 **50.0% < 60%** ⇒ **门槛未达，本批不扩大白名单**。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/642_loop_calibration.md` +
追加 `data/642_loop_calibration.json`（append-only 台账）。纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "642_loop_calibration.md")
LEDGER = os.path.join(ROOT, "data", "642_loop_calibration.json")
EXPANSION_THRESHOLD = 0.60

LOOP_AUDIT = os.path.join(ROOT, "data", "637_loop_quality_audit.md")
LOOP_TUNING = os.path.join(ROOT, "data", "638_loop_tuning.md")


def _exists(p: str) -> bool:
    return os.path.exists(p)


def round_637() -> dict[str, Any]:
    """R1：来自 637 质量审计的自审结论（人工逐条打分，非机器推断）。"""
    return {"round": "R1", "batch": 637, "at": "2026-09-25",
            "candidates": 8, "decided": 8, "adopted": 3, "reliable": 3,
            "half": 3, "unreliable": 2,
            "source": "data/637_loop_quality_audit.md",
            "source_present": _exists(LOOP_AUDIT),
            "metric": "靠谱率（建议/问题被人工判为靠谱的比例）",
            "derived": False,
            "note": "审计人=执行 637 的 AI（**自审**），不是独立人审"}


def round_638() -> dict[str, Any]:
    """R2：来自 638 调参前后差异（异常 4 → 2，消除 2 条误报）。"""
    return {"round": "R2", "batch": 638, "at": "2026-09-25",
            "candidates": 4, "decided": 4, "adopted": 3, "reliable": 2,
            "false_positive": 2,
            "source": "data/638_loop_tuning.md",
            "source_present": _exists(LOOP_TUNING),
            "metric": "1 − 误报率（异常检出中为真的比例）",
            "derived": True,
            "note": "**口径与 R1 不同**（R1 是建议靠谱率，R2 是异常检出准确率）；"
                    "调参本身是 3 项，故 adopted=3"}


def round_642() -> dict[str, Any]:
    """R3：642 本批产出的可采纳项（**全部交人，未代决** ⇒ 事后验证 = None）。"""
    return {"round": "R3", "batch": 642, "at": "2026-09-26",
            "candidates": 157, "decided": 0, "adopted": 0, "reliable": None,
            "source": "data/642_fail_open_audit.md + data/642_mdl_admission.md + "
                      "data/642_kernel_minimality_audit.md + data/642_protector_rollout.md",
            "source_present": _exists(os.path.join(ROOT, "data", "642_fail_open_audit.md")),
            "metric": "待事后验证（本批**不代决**）",
            "derived": False,
            "breakdown": {
                "B3 已知 fail-open 可修项": 2,
                "B3 扫描命中线索": 145,
                "636 口径误题修正": 1,
                "636 备忘与实测差异": 1,
                "A5 被拒规则（新方向，保留）": 4,
                "B2 内核建议移出": 4,
            },
            "note": "**校准度是 None 而不是 0**：采纳数与事后验证都待人审，写成 0 是假精确"}


def rounds() -> list[dict[str, Any]]:
    return [round_637(), round_638(), round_642()]


def calibration(r: dict[str, Any]) -> Optional[float]:
    """统一口径：`成立的已判定项 / 已判定项`；已判定 0 ⇒ **None**（不假精确）。"""
    d = int(r.get("decided", 0))
    if d <= 0:
        return None
    return round(int(r.get("reliable", 0)) / d, 4)


def table() -> list[dict[str, Any]]:
    out = []
    for r in rounds():
        out.append({**r, "calibration": calibration(r),
                    "adoption_rate": (round(r["adopted"] / r["candidates"], 4)
                                      if r.get("candidates") else None)})
    return out


def best_calibration() -> Optional[float]:
    vals = [c for c in (calibration(r) for r in rounds()) if c is not None]
    return max(vals) if vals else None


def expansion_gate(threshold: float = EXPANSION_THRESHOLD) -> dict[str, Any]:
    """扩大白名单的门槛判定（C1 的输入）。**门槛未达即不扩大**。"""
    best = best_calibration()
    ok = best is not None and best > threshold
    return {"threshold": threshold, "best_observed": best, "passed": bool(ok),
            "verdict": ("达到门槛 ⇒ 可进入白名单扩展评估" if ok else
                        "**未达门槛 ⇒ 本批不扩大 auto_executor 白名单**"),
            "caveat": "样本量极小（已判定 8 + 4），且 R1/R2 口径不同 ⇒ **不足以判趋势**"}


def record(run: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """把一轮记录**追加**进台账（append-only）。默认记 R3（本批）。"""
    run = round_642() if run is None else run
    entry = {"recorded_at": datetime.datetime.now().isoformat(timespec="seconds"),
             "round": run.get("round"), "batch": run.get("batch"),
             "candidates": run.get("candidates"), "decided": run.get("decided"),
             "adopted": run.get("adopted"), "reliable": run.get("reliable"),
             "calibration": calibration(run), "source": run.get("source")}
    entries: list[dict[str, Any]] = []
    if os.path.exists(LEDGER):
        try:
            entries = json.loads(open(LEDGER, encoding="utf-8").read()).get("entries", [])
        except (OSError, json.JSONDecodeError):
            entries = []
    before = len(entries)
    # 幂等：同 (round, batch) 已存在则不重复追加
    if not any(e.get("round") == entry["round"] and e.get("batch") == entry["batch"]
               for e in entries):
        entries.append(entry)
    payload = {"schema": "loop_calibration/1", "append_only": True,
               "expansion_threshold": EXPANSION_THRESHOLD,
               "entries": entries}
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return {"appended": len(entries) > before, "n_entries": len(entries),
            "entry": entry}


def _digest(p: str) -> str:
    try:
        with open(p, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()[:16]
    except OSError:
        return ""


def write_report() -> str:
    t = table()
    g = expansion_gate()
    rec = record()
    lines = [
        "# 642 C2 · 闭环校准度追踪（637 → 638 → **642**）", "",
        "> 口径：`校准度 = 成立的已判定项 / 已判定项`；**采纳数单列**（未被采纳即无从验证）。",
        f"> 扩大门槛：校准度 > **{EXPANSION_THRESHOLD:.0%}** 才考虑扩大白名单（C1 的输入）。", "",
        "## 一、三轮台账（全部来自已有证据，**不重跑、不改上一批产物**）", "",
        "| 轮次 | 批次 | 候选 | 已判定 | 采纳 | 成立 | 校准度 | 口径 |",
        "|---|---|---|---|---|---|---|---|"]
    for r in t:
        cal = "**None（待人审）**" if r["calibration"] is None else f"**{r['calibration']:.1%}**"
        lines.append(f"| {r['round']} | {r['batch']} | {r['candidates']} | {r['decided']} | "
                     f"{r['adopted']} | {r['reliable'] if r['reliable'] is not None else '—'} | "
                     f"{cal} | {r['metric']} |")
    lines += ["", "### 1.1 逐轮说明（含来源可核性）", "",
              "| 轮次 | 来源 | 来源在册 | 是派生值？ | 备注 |", "|---|---|---|---|---|"]
    for r in t:
        lines.append(f"| {r['round']} | `{os.path.basename(r['source'])}` | "
                     f"{'✅' if r['source_present'] else '❌'} | "
                     f"{'派生' if r['derived'] else '直接引用'} | {r['note']} |")
    lines += ["", "### 1.2 R3 的候选构成（642 本批）", "",
              "| 类别 | 条数 |", "|---|---|"]
    for k, v in round_642()["breakdown"].items():
        lines.append(f"| {k} | {v} |")
    lines += ["", "## 二、趋势判定", "",
              f"- 已有两个**可计算**点：R1 {table()[0]['calibration']:.1%}、"
              f"R2 {table()[1]['calibration']:.1%}；R3 = **None**（未代决）；",
              "- **口径警告**：R1 是「建议靠谱率」，R2 是「异常检出准确率」——"
              "**两者不是同一量**，直接连成趋势是不严格的；本工具统一为"
              "「已判定项中成立的占比」，但**样本量 8 与 4 都极小** ⇒"
              "**仍不足以判趋势**（§十.6：2 个点不够，642 新增的是第 3 个**待验证**点）；",
              "- R1/R2 的审计人均为**执行该批的 AI（自审）**，不是独立人审 ⇒ 校准度本身带自评偏差。", "",
              "## 三、扩大门槛判定（C1 的输入）", "",
              f"- 门槛：**{g['threshold']:.0%}**；当前最高观测："
              f"**{('%.1f%%' % (g['best_observed'] * 100)) if g['best_observed'] is not None else '无可计算值'}**",
              f"- **判定：{g['verdict']}**",
              f"- 附加条件：{g['caveat']}", "",
              "## 四、台账写入（append-only）", "",
              f"- 本次追加：**{rec['appended']}**；台账条目数：**{rec['n_entries']}**",
              "- 台账文件：`data/642_loop_calibration.json`（同 (round,batch) **幂等**，不重复追加）",
              f"- 637 审计文件指纹：`{_digest(LOOP_AUDIT)}`；638 调参文件指纹：`{_digest(LOOP_TUNING)}`"
              "（本工具**只读**这两个文件）", "",
              "## 诚实登记", "",
              "1. **R3 的校准度是 None，不是 0**：采纳数与事后验证都待人审；写成 0 是假精确；",
              "2. **R1 与 R2 口径不同**，统一口径后可比性仍受**极小样本**限制；",
              "3. **R1/R2 是自审**（审计人=执行该批的 AI）⇒ 校准度含自评偏差，不能当独立人审；",
              "4. **R2 的 50.0% 是派生值**（由「调前异常 4、误报 2」推出），已在表中标注 `派生`；",
              "5. 本模块**不重跑 637/638 的闭环工具**、**不改写它们的落盘产物**（避免跨批污染）；",
              "6. **门槛未达 ⇒ 本批不扩大白名单**；是否降低门槛或补样本由人裁决（交人项）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("三轮齐全", [r["round"] for r in rounds()] == ["R1", "R2", "R3"])
    chk("R1 校准度 37.5%", calibration(round_637()) == 0.375,
        str(calibration(round_637())))
    chk("R2 校准度 50.0%", calibration(round_638()) == 0.5, str(calibration(round_638())))
    chk("R3 校准度为 None（未代决，不假精确）", calibration(round_642()) is None)
    chk("R3 采纳数为 0（不代签）", round_642()["adopted"] == 0)
    chk("已判定 0 ⇒ None 而非除零", calibration({"decided": 0, "reliable": 0}) is None)
    chk("误报项不计入成立", calibration({"decided": 4, "reliable": 2}) == 0.5)

    g = expansion_gate()
    chk("门槛 60%", g["threshold"] == EXPANSION_THRESHOLD)
    chk("最高观测 50% < 60% ⇒ 未达", g["passed"] is False, str(g["best_observed"]))
    chk("门槛判定含 caveat", bool(g["caveat"]))

    chk("来源文件在册", round_637()["source_present"] and round_638()["source_present"])
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    chk("台账路径在 data 下", LEDGER.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="642 C2 闭环校准度追踪")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + 追加台账")
    ap.add_argument("--json", action="store_true", help="打印台账（JSON）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.report:
        print(f"written {write_report()}")
        return 0
    t = table()
    if a.json:
        print(json.dumps({"rounds": t, "gate": expansion_gate()},
                         ensure_ascii=False, indent=2))
        return 0
    print("[loop-calibration] " + "；".join(
        f"{r['round']}=" + ("None" if r["calibration"] is None else f"{r['calibration']:.1%}")
        for r in t) + f"；门槛 {EXPANSION_THRESHOLD:.0%} "
        f"{'已达' if expansion_gate()['passed'] else '未达 ⇒ 不扩大白名单'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
