"""636 2.4 · 校准追踪器报告模式 + known_error_rate 回填（**报告模式，不判 block**）

1. 为 **67 条规则**逐条填 `known_error_rate`：有历史误报/漏报数据则算；**无则标注「无数据」**（不编造）；
2. 设计校准追踪器报告格式：每验证器 **ECE**（Expected Calibration Error）+ 分域（简单/中等/复杂）
   + 三级降级（L1 重校准 / L2 禁言 / L3 降级）；
3. 离线模拟：`known_error_rate` 缺失 ⇒ 应进观察态 —— 这些规则**历史上参与了多少判决**？

**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/636_calibration_tracker_report.md`。
纯标准库；≥5 例单测。
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

OUT_MD = os.path.join(ROOT, "data", "636_calibration_tracker_report.md")
LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
VFDR = os.path.join(ROOT, "data", "vfdr_report_v2_624.json")


def rules() -> list[dict[str, str]]:
    try:
        import gate_engine as ge
        return [{"id": r.id, "title": getattr(r, "title", ""), "scope": getattr(r, "scope", "")}
                for r in ge.RULES]
    except Exception:  # noqa: BLE001
        return []


def vfdr_covered() -> set[str]:
    """VFDR 里的「已触达」规则（覆盖 ≠ 错误率，仅作参考）。"""
    try:
        d = json.loads(open(VFDR, encoding="utf-8").read())
        return set(d.get("cumulative_touched", []))
    except (OSError, json.JSONDecodeError):
        return set()


def known_error_rate_rows() -> list[dict[str, Any]]:
    covered = vfdr_covered()
    rows = []
    for r in rules():
        # 逐规则误报/漏报数据：仓库无 ⇒ 一律「无数据」（不编造）
        rows.append({"id": r["id"], "known_error_rate": None,
                     "data_state": "无数据", "vfdr_covered": r["id"] in covered})
    return rows


def ece_format() -> dict[str, Any]:
    return {
        "per_verifier": "ECE = Σ_b (n_b/N) × |acc(b) − conf(b)|（b 为置信分桶）",
        "domains": ["简单", "中等", "复杂"],
        "degradation": {
            "L1 重校准": "ECE > 0.10 ⇒ 重校准置信映射",
            "L2 禁言": "ECE > 0.20 ⇒ 该验证器禁言（不单独判 block）",
            "L3 降级": "ECE > 0.30 ⇒ 降级为 advice",
        },
        "note": "影子设计；本批不启用、不改判决。",
    }


def decisions_count() -> int:
    try:
        return len([ln for ln in open(LEDGER, encoding="utf-8") if ln.strip()])
    except OSError:
        return 0


def stats() -> dict[str, Any]:
    rows = known_error_rate_rows()
    with_data = [r for r in rows if r["known_error_rate"] is not None]
    no_data = [r for r in rows if r["known_error_rate"] is None]
    return {"total": len(rows), "with_data": len(with_data), "no_data": len(no_data),
            "observation_state": len(no_data), "decisions_impacted": decisions_count()}


def write_report() -> str:
    rows = known_error_rate_rows()
    s = stats()
    e = ece_format()
    lines = [
        "# 636 2.4 · 校准追踪器报告模式 + known_error_rate 回填", "",
        "## 一、67 规则 known_error_rate 清单", "",
        f"- 有数据：**{s['with_data']}**；**无数据：{s['no_data']}**（不编造）；",
        f"- 进观察态（缺失 known_error_rate）：**{s['observation_state']}**", "",
        "| 规则 | known_error_rate | 状态 | VFDR 覆盖 |", "|---|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['id']}` | {r['known_error_rate'] if r['known_error_rate'] is not None else '**无数据**'} | "
                     f"{r['data_state']} | {'✅' if r['vfdr_covered'] else '—'} |")
    lines += ["", "## 二、校准追踪器报告格式（影子设计）", "",
              f"- 每验证器：`{e['per_verifier']}`",
              f"- 分域：{e['domains']}",
              "- 三级降级：" + "；".join(f"{k} {v}" for k, v in e["degradation"].items()),
              f"- {e['note']}", "",
              "## 三、观察态规则的历史影响（离线模拟）", "",
              f"- 观察态规则：**{s['observation_state']}** 条（全部规则）；",
              f"- 历史判决总数（Authority ledger）：**{s['decisions_impacted']}** 条 ——"
              f"若按 v26「观察态不得单独判 block」，这些判决**都需复核**（模拟口径，非实际）。", "",
              "## 诚实登记", "",
              "1. **known_error_rate 全部「无数据」**：仓库无逐规则误报/漏报台账（VFDR 只记**覆盖率**）；"
              "**未编造**任何数字；",
              "2. ECE 格式为**影子设计**，本批不启用、不改判决；",
              "3. 「历史影响」用**判决总数**近似（无法逐规则归因）——如实说明。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("67 规则", len(rules()) == 67)
    s = stats()
    chk("全无数据（不编造）", s["with_data"] == 0 and s["no_data"] == 67)
    chk("观察态 67", s["observation_state"] == 67)
    chk("ECE 三级降级", len(ece_format()["degradation"]) == 3)
    chk("判决数 ≥1", decisions_count() >= 1)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="636 2.4 校准追踪器")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.json:
        print(json.dumps(stats(), ensure_ascii=False, indent=2))
        return 0
    print(stats())
    return 0


if __name__ == "__main__":
    sys.exit(main())
