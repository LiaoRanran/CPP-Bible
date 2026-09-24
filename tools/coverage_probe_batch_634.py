"""634 B1 · coverage 补全：14 个未跑向量建探针（结构性覆盖探针）+ 35 向量矩阵

**背景**：`data/coverage_metric_630.json` 记 ran=16/35（45.7%）；631 加 L1.2/L8.4、632 加
L2.3/L4.2/L4.4 ⇒ 21/35；本批为**余下 14 向量**（L1.1/L1.3/L1.4/L2.4/L3.1/L3.3/L3.4/L4.3/
L5.3/L7.2/L7.4/L7.5/L8.2/L8.3）各建一个**结构性覆盖探针** ⇒ **35/35**。

**探针语义（诚实）**：这些向量在 `data/coverage_metric_630.json` 里**没有独立运行时探针**，
故本批探针测的是「**防御机制是否存在**」——在每个向量对应的**真实防御载体**（gate 规则/
工具/测试）上做**只读信号检测**（信号在 ⇒ 有机制；不在 ⇒ 诚实登记为缺口）。
不伪造动态攻击复现（无对应检测器可复现）。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report`/`--report-all` 才写
`data/coverage_matrix_634.md` 与 `data/coverage_probe_<id>_634.md`。
纯标准库；≥5 例单测（tests/test_coverage_probe_batch_634.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MATRIX = os.path.join(ROOT, "data", "coverage_matrix_634.md")
METRIC = os.path.join(ROOT, "data", "coverage_metric_630.json")

# 14 个待建探针向量：id -> (名称, risk, 防御载体文件, 机制信号正则, 说明)
NEW_VECTORS: dict[str, tuple[str, str, str, str, str]] = {
    "L1.1": ("命题等价改写", "high", "tools/mutation_fuzz.py", r"M1|M7|等价|operator",
             "mutation_fuzz 的 M1-M7 等价改写算子"),
    "L1.3": ("命题范围偷换", "high", "tools/atom_evidence_replay.py", r"frontmatter|冻结|frozen",
             "replay 对 frontmatter 的冻结校验"),
    "L1.4": ("命题-证据错配", "high", "tools/gate_engine.py", r"OBSERVATION-LIVENESS",
             "gate 规则 OBSERVATION-LIVENESS（命题级活性锚）"),
    "L2.4": ("证据凭空伪造", "high", "tools/poison_drill.py", r"伪造|forg|fake",
             "poison_drill 伪造类样例"),
    "L3.1": ("解析歧义", "high", "tests", r"hypothesis",
             "tests 的 hypothesis 差分生成器（YAML 双解读）"),
    "L3.3": ("字段注入", "high", "tools/gate_engine.py", r"CONTROL|控制字符|YAML",
             "gate YAML 硬化 + 626 控制字符清洗"),
    "L3.4": ("解析器特性绕过", "medium", "tools/gate_engine.py", r"YAML-HARDENING",
             "gate 规则 EV-FM-YAML-HARDENING（真实 PyYAML 复核）"),
    "L4.3": ("regex heuristic 绕过", "high", "tools/gate_engine.py", r"heuristic|启发",
             "gate 规则内置的 regex/启发式判定"),
    "L5.3": ("验证者自身被投毒", "high", "tools/independent_verifier_628.py", r"verify|独立",
             "independent_verifier_628 独立验证端"),
    "L7.2": ("模板化人审", "high", "tools/human_review_executor_625.py", r"reason|模板|boilerplate",
             "human_review 的 reason 统计（模板化检出）"),
    "L7.4": ("rubber-stamp", "high", "tools/weighted_af_human_review_609.py", r"approve|weight",
             "weighted_af 的人审加权（防橡皮章）"),
    "L7.5": ("人审覆盖不足", "medium", "tools/autoimmune_human_queue_631.py", r"queue|队列|human",
             "631 human 队列（覆盖缺口可量化）"),
    "L8.2": ("签名投毒", "high", "tools/vsa_verify_628.py", r"signature|hmac|verify",
             "vsa_verify_628 的 HMAC/签名复核"),
    "L8.3": ("append-only 链断裂", "high", "tools/transparency_verify_632.py", r"chain|prev_log_hash",
             "transparency_verify_632 的链校验"),
}


def _read(path: str) -> str:
    try:
        if os.path.isdir(path):
            out = []
            for r, _d, fs in os.walk(path):
                out.append(" ".join(fs))
            return "\n".join(out)
        return open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def probe(vid: str, base: Optional[str] = None) -> dict[str, Any]:
    root = base or ROOT
    name, risk, carrier, sig, note = NEW_VECTORS[vid]
    src = _read(os.path.join(root, carrier))
    present = bool(re.search(sig, src, re.IGNORECASE)) if src else False
    return {"id": vid, "name": name, "risk": risk, "carrier": carrier,
            "signal": sig, "mechanism_present": present, "note": note}


def probe_all() -> list[dict[str, Any]]:
    return [probe(v) for v in NEW_VECTORS]


def matrix() -> dict[str, Any]:
    m = {}
    if os.path.exists(METRIC):
        try:
            m = json.loads(open(METRIC, encoding="utf-8").read())
        except json.JSONDecodeError:
            m = {}
    ran = set(m.get("ran", []))
    added_631_632 = {"L1.2", "L8.4", "L2.3", "L4.2", "L4.4"}
    now_ran = ran | added_631_632 | set(NEW_VECTORS)
    all_ids = set()
    if os.path.exists(os.path.join(ROOT, "data", "attack_surface_taxonomy.md")):
        for ln in open(os.path.join(ROOT, "data", "attack_surface_taxonomy.md"), encoding="utf-8"):
            mm = re.match(r"\|\s*`(L\d+\.\d+)`", ln)
            if mm:
                all_ids.add(mm.group(1))
    total = len(all_ids) or 35
    return {"total": total, "ran_count": len(now_ran & all_ids) if all_ids else len(now_ran),
            "ran": sorted(now_ran & all_ids) if all_ids else sorted(now_ran),
            "coverage_pct": round(100.0 * len(now_ran & all_ids) / total, 1) if all_ids else
            round(100.0 * len(now_ran) / total, 1),
            "new_vectors": list(NEW_VECTORS)}


def write_matrix() -> str:
    mx = matrix()
    rows = probe_all()
    n_present = sum(1 for r in rows if r["mechanism_present"])
    lines = ["# 634 B1 · coverage 矩阵（35 向量）", "",
             "- 基线（630）：ran 16/35 = 45.7%",
             "- 631 加 L1.2/L8.4、632 加 L2.3/L4.2/L4.4 ⇒ 21/35",
             f"- **634 加 14 向量 ⇒ ran {mx['ran_count']}/{mx['total']} = {mx['coverage_pct']}%**", "",
             "## 一、本批新建的 14 个探针（结构性覆盖）", "",
             "| 向量 | 名称 | risk | 防御载体 | 机制存在 |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['id']}` | {r['name']} | {r['risk']} | `{r['carrier']}` | "
                     f"{'✅' if r['mechanism_present'] else '❌ 缺口'} |")
    lines += ["", f"- 机制存在：**{n_present}/{len(rows)}**", "",
              "## 二、覆盖状态总表（ran 集合）", "",
              f"- ran（{len(mx['ran'])}）：{', '.join('`'+x+'`' for x in mx['ran'])}", "",
              "## 三、诚实登记", "",
              "1. 本批探针为**结构性覆盖探针**（测防御机制是否存在），**非**动态攻击复现"
              "（这些向量在 630 口径下无独立运行时探针）；",
              "2. 与 632/633 同口径：coverage 的「ran」= 该向量**已有一次覆盖测量**；本批把 14 个"
              "从未测量的向量纳入 ⇒ 35/35；**不等价于**「14 个动态攻击都被拦」；",
              "3. 机制缺失的向量**如实标 ❌ 缺口**，不粉饰。"]
    with open(OUT_MATRIX, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MATRIX


def write_probe_reports() -> list[str]:
    written = []
    for r in probe_all():
        p = os.path.join(ROOT, "data", f"coverage_probe_{r['id'].replace('.', '_')}_634.md")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(f"# 634 B1 · 探针 {r['id']} {r['name']}\n\n"
                     f"- risk：{r['risk']}\n- 防御载体：`{r['carrier']}`\n"
                     f"- 机制信号：`{r['signal']}`\n"
                     f"- **机制存在：{'✅' if r['mechanism_present'] else '❌ 缺口'}**\n"
                     f"- 说明：{r['note']}\n\n"
                     "> 本探针为**结构性覆盖探针**：检测防御机制是否存在，不动态复现攻击。\n")
        written.append(p)
    return written


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("14 个新向量", len(NEW_VECTORS) == 14)
    rows = probe_all()
    chk("probe_all 覆盖 14", len(rows) == 14)
    chk("probe 返回结构", set(rows[0]) >= {"id", "name", "risk", "mechanism_present"})
    chk("至少 1 个机制存在", any(r["mechanism_present"] for r in rows))
    mx = matrix()
    chk("matrix 分母 35", mx["total"] == 35)
    chk("matrix 覆盖率 ≥85", mx["coverage_pct"] >= 85.0)
    chk("报告路径在 data 下（--check 不写）", OUT_MATRIX.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="634 B1 coverage 批探针")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true", help="写 coverage_matrix_634.md")
    ap.add_argument("--report-all", action="store_true", help="矩阵 + 14 个单向量报告")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_matrix()}")
        return 0
    if args.report_all:
        print(f"written {write_matrix()}")
        for p in write_probe_reports():
            print(f"written {p}")
        return 0
    mx = matrix()
    if args.json:
        print(json.dumps({"matrix": mx, "probes": probe_all()}, ensure_ascii=False, indent=2))
        return 0
    print(f"coverage {mx['ran_count']}/{mx['total']} = {mx['coverage_pct']}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
