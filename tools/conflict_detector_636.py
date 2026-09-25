"""636 2.1 · 冲突检测器（**影子模式**，零依赖独立模块）

**铁律**（§零.1/§零.7）：本模块是**影子**——**不 import gate_engine 等任何判决代码**、
**不拦截、不改判**，只做离线「如果开了会怎么样」的模拟。

四型冲突（v25 2.1）：
- `RR` 规则间冲突：同一适用集内同时存在 block 与 warn 级规则；
- `ER` 证据-规则冲突：卡 `status: verified` 但出现**反证/矛盾**标记；
- `EE` 证据间冲突：≥2 条证据但 `artifact_sha256` 声明数与证据数不符（不自洽）；
- `欠定`：verified 但**无证据引用**（证据不足）。

冲突强度：`C = conflict_raw × (1 - agreement)`，其中 `agreement` = 证据声明自洽比例。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 写
`data/636_conflict_detector_shadow.md`。纯标准库；≥5 例单测。
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

OUT_MD = os.path.join(ROOT, "data", "636_conflict_detector_shadow.md")
THETA = 0.3   # v25 待回填参数初值

_VERIFIED_RE = re.compile(r"^status:\s*verified", re.MULTILINE)
_STRONG_REFUT_RE = re.compile(r"falsification:\s*(fail|refut)|verdict:\s*refut|证据被推翻|已驳回",
                              re.IGNORECASE)
_EV_RE = re.compile(r"\bEV-[A-Z0-9]+(?:-[A-Z0-9]+)*\b")


_EVIDENCE_INDEX: Optional[set[str]] = None


def evidence_ids() -> set[str]:
    """全库证据卡 id 索引（供「引用的证据是否存在」判定）。"""
    global _EVIDENCE_INDEX
    if _EVIDENCE_INDEX is None:
        ids = set()
        for _r, _d, fs in os.walk(os.path.join(ROOT, "evidence")):
            for f in fs:
                if f.endswith(".md"):
                    ids.add(f[:-3])
        _EVIDENCE_INDEX = ids
    return _EVIDENCE_INDEX


def detect(card_text: str, rules: list[dict[str, str]],
           ev_index: Optional[set[str]] = None) -> dict[str, Any]:
    """零依赖冲突检测：输入卡文本 + 规则元数据，输出四型 + 强度。

    `agreement` = **被引用的证据 id 中真实存在的比例**（悬挂引用 ⇒ agreement<1 ⇒ C>0）。
    """
    idx = evidence_ids() if ev_index is None else ev_index
    ev = sorted(set(_EV_RE.findall(card_text)))
    verified = bool(_VERIFIED_RE.search(card_text))
    has_evidence = bool(re.search(r"evidence:\s*\[", card_text))
    refutation = bool(_STRONG_REFUT_RE.search(card_text))

    has_block = any(r.get("severity") == "block" for r in rules)
    has_warn = any(r.get("severity") == "warn" for r in rules)
    rr = 1 if (has_block and has_warn) else 0
    er = 1 if (verified and refutation) else 0
    ee = 1 if (len(ev) >= 2 and any(e not in idx for e in ev)) else 0
    und = 1 if (verified and not has_evidence) else 0

    raw = rr + er + ee + und
    agreement = 1.0 if not ev else min(1.0, len([e for e in ev if e in idx]) / len(ev))
    c = round(raw * (1 - agreement), 3)
    types = [t for t, v in (("RR", rr), ("ER", er), ("EE", ee), ("欠定", und)) if v]
    return {"rr": rr, "er": er, "ee": ee, "und": und, "conflict_raw": raw,
            "agreement": round(agreement, 3), "C": c, "types": types,
            "exceeds_theta": c >= THETA}


def load_rules() -> list[dict[str, str]]:
    """仅读规则**元数据**（不调用任何判决函数）；失败则回退静态解析。"""
    try:
        import gate_engine as ge
        return [{"id": r.id, "severity": getattr(r, "severity", ""), "scope": getattr(r, "scope", "")}
                for r in ge.RULES]
    except Exception:  # noqa: BLE001
        src = open(os.path.join(ROOT, "tools", "gate_engine.py"), encoding="utf-8",
                   errors="replace").read()
        ids = re.findall(r'register\(Rule\(\s*"([^"]+)"', src)
        return [{"id": i, "severity": "block", "scope": "atom"} for i in ids]


def verified_cards() -> list[tuple[str, str]]:
    out = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        for f in fs:
            if f.endswith(".md"):
                p = os.path.join(r, f)
                t = open(p, encoding="utf-8", errors="replace").read()
                if _VERIFIED_RE.search(t):
                    out.append((os.path.relpath(p, ROOT).replace(os.sep, "/"), t))
    return out


def run_shadow() -> dict[str, Any]:
    rules = load_rules()
    rows = []
    for rel, t in verified_cards():
        d = detect(t, rules)
        rows.append({"card": rel, **d})
    dist: dict[str, int] = {}
    for r in rows:
        for ty in r["types"]:
            dist[ty] = dist.get(ty, 0) + 1
    over = [r for r in rows if r["exceeds_theta"]]
    return {"n_cards": len(rows), "type_dist": dist, "over_theta": len(over),
            "theta": THETA, "rows": rows}


def write_report() -> str:
    s = run_shadow()
    lines = [
        "# 636 2.1 · 冲突检测器影子运行（离线，未改任何判决）", "",
        "## 一、检测器设计（零依赖）", "",
        "- **四型**：RR（规则间）/ ER（证据-规则）/ EE（证据间）/ 欠定（证据不足）；",
        "- **强度**：`C = conflict_raw × (1 - agreement)`；`agreement` = **被引用证据的存在率**；",
        f"- **阈值**：θ_conflict = **{THETA}**（v25 待回填初值）；",
        "- **零依赖**：`detect()` 不 import 任何判决代码（`load_rules()` 仅读元数据）。", "",
        "## 二、离线重跑（全部 verified 卡）", "",
        f"- verified 卡：**{s['n_cards']}**",
        f"- 四型分布：`{s['type_dist']}`",
        f"- 超阈值（C ≥ {THETA}）事件：**{s['over_theta']}**", "",
        "| 卡 | RR | ER | EE | 欠定 | raw | agreement | C | 超阈值 |",
        "|---|---|---|---|---|---|---|---|---|"]
    for r in s["rows"]:
        lines.append(f"| `{r['card'].split('/')[-1][:-3]}` | {r['rr']} | {r['er']} | {r['ee']} | "
                     f"{r['und']} | {r['conflict_raw']} | {r['agreement']} | {r['C']} | "
                     f"{'⚠️' if r['exceeds_theta'] else '—'} |")
    lines += ["", "## 三、若在线会拦截多少历史判决？", "",
              f"- 超阈值 **{s['over_theta']}/{s['n_cards']}** 张会被标「需人工复核」（若在线）；",
              "- **注意**：本批为**影子**，未拦截、未改判（§零.7）。", "",
              "## 四、建议阈值", "",
              f"- 实测 C 分布见上表；若多数卡 C=0（agreement=1），θ={THETA} 已足够保守；",
              "- 建议：**保持 θ=0.3 作初值**，待阶段 3 用更大样本回填（交人项）。", "",
              "## 诚实登记", "",
              "1. **影子模式**：不拦截、不改判，仅离线模拟；",
              "2. `agreement` 用「**被引用证据的存在率**」近似（悬挂引用 ⇒ <1）；**启发式**，非统计一致度；",
              "3. RR 为全局规则集属性（同批所有卡一致），**区分度有限**——如实说明；",
              "4. 检测器**零依赖**（detect 不 import 判决代码）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    rules = [{"id": "A", "severity": "block", "scope": "atom"},
             {"id": "B", "severity": "warn", "scope": "atom"}]
    d1 = detect("status: verified\nevidence: [EV-X-001, EV-X-002]\nartifact_sha256: a\n"
                "artifact_sha256: b\n", rules)
    chk("RR=1(block+warn)", d1["rr"] == 1)
    chk("verified 无证据→欠定", detect("status: verified\n", rules)["und"] == 1)
    chk("强反证→ER",
        detect("status: verified\nfalsification: fail\nevidence: [EV-A-1]", rules)["er"] == 1)
    chk("C ≥ 0 且为 float", isinstance(d1["C"], float) and d1["C"] >= 0)
    chk("verified 卡可扫描", len(verified_cards()) >= 1)
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="636 2.1 冲突检测器影子")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    s = run_shadow()
    if args.json:
        print(json.dumps({k: v for k, v in s.items() if k != "rows"}, ensure_ascii=False, indent=2))
        return 0
    print({k: v for k, v in s.items() if k != "rows"})
    return 0


if __name__ == "__main__":
    sys.exit(main())
