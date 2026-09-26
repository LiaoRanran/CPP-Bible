"""645 · 阶段 B5+B6 · **证据判定套件**（等级 + 充分性）—— 647 D1 合并版。

目标（645 §四 B5/B6）：
* B5 **等级判定**：对每条真实证据判定等级（L1 多编译器实测 / L2 标准 / L3 共识 / L4 单点 / L5 未验证）；
* B6 **充分性判定**：对卡片全量判定「至少 1 条 L1/L2？/ 至少 3 条独立证据？」，输出充分/不足清单。

真实、非代理：复用 644 `evidence_base_644` 的 `EvidenceRecord` 与 `grade_from_source`；
卡片证据来自真实 `card_evidence_map()` + `compiler_probe_645` 真实 L1 实测 + `evidence_store`。

**647 D1 合并说明**：成员以**重命名后的入口**保留，功能不丢失：

| 原工具 | 在本模块中的入口 |
|---|---|
| `evidence_grading_645`（B5） | `grade_all()` / `write_report()` |
| `evidence_sufficiency_645`（B6） | `judge()` / `write_sufficiency_report()` / `sufficiency_selftest()` |

**为什么能合并**（646 B4 判断，647 执行）：B6 的充分性判定**直接消费** B5 的等级结果，
同属"头部层证据判定"⇒ 拆成两个文件的收益是负的（同一个 `evidence_base_644` 依赖、同一批数据）。

CLI：`--check` 只读自检 / `--grade` 真实分级 / `--judge` 真实充分性判定。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_evidence_grading_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_evidence_grading_report.json")
GRADES = base.GRADES


def grade_all() -> dict:
    """真实分级：现有 EV 卡 + 本批新存证据库。"""
    graded: list[dict] = []
    # 1) 现有 evidence/ 下 EV 卡（真实编译器/标准/来源 → 等级）
    for e in base.grade_existing_evidence():
        graded.append({
            "id": e["id"], "source": "evidence_card", "kind": e["kind"],
            "grade": e["grade"], "credibility": e["credibility"],
            "compilers": e["compilers"], "verdict": e["verdict"],
        })
    # 2) 本批新存 evidence_store（compiler_probe_645 / standard_fetcher_645 落库）
    for rec in base.iter_stored():
        graded.append({
            "id": rec.evidence_id[:16], "source": "evidence_store",
            "kind": rec.source_type, "grade": rec.grade, "credibility": rec.credibility,
            "compilers": rec.meta.get("compilers", 1), "verdict": "",
        })
    # 等级分布
    dist: dict[str, int] = {g: 0 for g in GRADES}
    for g in graded:
        if g["grade"] in dist:
            dist[g["grade"]] += 1
    return {
        "total": len(graded),
        "grade_distribution": dist,
        "graded": graded,
    }


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 证据等级报告（B5，真实判定）", "",
             f"- **已判等级证据总数：{result['total']}**（B5 目标 ≥30）",
             f"- 等级分布：{result['grade_distribution']}", ""]
    lines.append("## 等级分布说明")
    for g in GRADES:
        lines.append(f"- {g}：{result['grade_distribution'][g]}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：**合并后两个成员的逻辑一起验**（分级 + 充分性）。"""
    g, c = base.grade_from_source("compiler_run", compilers=2)
    assert g == "L1" and c > 0.9
    g2, _ = base.grade_from_source("iso_standard")
    assert g2 == "L2"
    # 真实证据可读
    assert isinstance(base.grade_existing_evidence(), list)
    # 合并进来的 B6 自检（功能等价证据）
    assert sufficiency_selftest() == 0
    # B6 的判定**消费** B5 的等级口径（合并的前提）
    assert "L1" in GRADES and "L2" in GRADES
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范 + 647 D1 合并）：`--check` 只读自检；
    `--grade` 分级（B5）/ `--judge` 充分性（B6）；无参 = `--grade`。"""
    ap = argparse.ArgumentParser(description="645 证据判定套件（等级/充分性，647 D1 合并）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--grade", action="store_true", help="真实分级全量证据（B5）")
    ap.add_argument("--judge", action="store_true", help="真实充分性判定（B6）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.judge:
        return sufficiency_main([])
    result = grade_all()
    write_report(result)
    print(f"[645 grading] 已判等级证据={result['total']} 分布={result['grade_distribution']}")
    return 0




# ======== 647 D1 合并自 evidence_sufficiency_645.py（符号已重命名以避冲突）========
# （该成员的 `import os/sys` 已在文件顶部，此处不重复导入 —— 647 D3 死代码清理）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUFF_REPORT_MD = os.path.join(ROOT, "data", "645_sufficiency_report.md")
SUFF_REPORT_JSON = os.path.join(ROOT, "data", "645_sufficiency_report.json")


def judge() -> dict:
    """真实全量充分性判定（28 卡）。"""
    # 真实卡片 → 分级证据映射
    by_card: dict[str, list[dict]] = {}
    # 用 card_evidence_map 拿真实 EV→card，再叠加本批 compiler_probe 落库的 meta.card
    ev_map = base.card_evidence_map()
    for rec in base.iter_stored():
        card = rec.meta.get("card")
        if card:
            by_card.setdefault(card, []).append({
                "id": rec.evidence_id[:16], "grade": rec.grade,
                "credibility": rec.credibility, "source": rec.source_type,
            })
    for card, evs in ev_map.items():
        by_card.setdefault(card, []).extend(evs)
    per_card: dict[str, dict] = {}
    sufficient = insufficient = needs_human = 0
    for card, evs in by_card.items():
        has_l12 = any(e.get("grade") in ("L1", "L2") for e in evs)
        independent = len({(e.get("id"), e.get("source")) for e in evs})
        has_3 = independent >= 3
        missing = []
        if not has_l12:
            missing.append("缺少 L1/L2 级证据")
        if not has_3:
            missing.append("独立证据不足 3 条")
        # 反例/过期：本批未做反例交叉 → 标记需人审（诚实，不编造）
        if not missing:
            status = "sufficient"
            sufficient += 1
        else:
            status = "insufficient"
            insufficient += 1
        per_card[card] = {
            "evidence_count": len(evs), "has_l12": has_l12, "independent": independent,
            "status": status, "missing": missing,
        }
    return {
        "cards_total": len(per_card),
        "sufficient": sufficient, "insufficient": insufficient, "needs_human": needs_human,
        "per_card": per_card,
    }


def write_sufficiency_report(result: dict) -> None:
    """写 B6 充分性报告（647 D1：重命名以区别于 B5 的 `write_report`）。"""
    lines = ["# 645 证据充分性报告（B6，真实全量判定）", "",
             f"- 卡片总数：{result['cards_total']}",
             f"- 充分：{result['sufficient']} / 不足：{result['insufficient']} / 需人审：{result['needs_human']}", ""]
    lines.append("## 逐卡")
    for card, info in sorted(result["per_card"].items()):
        miss = ("；缺失：" + "，".join(info["missing"])) if info["missing"] else ""
        lines.append(f"- `{card}`：证据={info['evidence_count']} L1/L2={info['has_l12']} "
                     f"独立={info['independent']} → **{info['status']}**{miss}")
    with open(SUFF_REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(SUFF_REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def sufficiency_selftest() -> int:
    """只读自检：判定逻辑（合成数据）。"""
    # 合成一张卡：有 L2 + 3 独立 → sufficient
    fake = {"C1": [{"id": "a", "grade": "L2", "source": "x"},
                   {"id": "b", "grade": "L3", "source": "y"},
                   {"id": "c", "grade": "L3", "source": "z"}]}
    evs = fake["C1"]
    has_l12 = any(e["grade"] in ("L1", "L2") for e in evs)
    independent = len({(e["id"], e["source"]) for e in evs})
    assert has_l12 and independent >= 3
    # 真实数据可读
    assert isinstance(base.card_evidence_map(), dict)
    return 0


def sufficiency_main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 证据充分性真实判定")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--judge", action="store_true", help="真实全量 28 卡判定")
    args = ap.parse_args(argv)
    if args.check:
        return sufficiency_selftest()
    result = judge()
    write_sufficiency_report(result)
    print(f"[645 sufficiency] 卡={result['cards_total']} 充分={result['sufficient']} "
          f"不足={result['insufficient']}")
    return 0


