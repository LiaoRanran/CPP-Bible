"""557 Part A · 人审经济学分桶器（**纯读**；不 accept、不改 severity、不改卡、不跑编译）。

目的（555 L4 自我校准引擎第一块实体）：把 gate 的 136 条 warn（+5 advice）从"逐条读"
变成"只看桶③约 20 条真信号"。机器负责结构化 + 排序 + 给证据；人只做 judge。

四桶（口径见 `_worklog_557.md`）：
  ① 迁移过程债      —— 新规则上线后的**存量迁移**信号（随回填/人签清零，非内容退化）；
  ② 规则设计待甄别  —— `EV-MATRIX-UNBACKED`：逐条判 (a) 刻意排除 actual=规则预期 /
                       (b) 真缺矩阵支撑=真信号（转桶③）；
  ③ 真信号          —— 人必须逐条看（排最前）；
  ④ 已登记豁免/重复 —— golden_lock 已分类的非 real 桶 + 完全重复命中。

输出：`data/review/triage_<gitshort>.json`（大 JSON，`.gitignore` 已忽略）+ 终端摘要。

**铁律**：本工具任何情况下**不得**调用 `golden_lock.py check --accept`——accept 权唯人。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
os.environ.setdefault("CPPBIBLE_OBS", "0")      # 纯读：别写 data/logs

import gate_engine as ge                        # noqa: E402  (path 注入后导入)

REVIEW_DIR = ROOT / "data" / "review"
GOLDEN_STATE = ROOT / "tools" / "golden_state.json"

# 桶①：新规则上线后的存量迁移债（每条附清零动作；指向 526/528 STAGING 名单与 backlog）。
BUCKET1_ACTIONS: dict[str, str] = {
    "ATOM-CLAIM-CONCEPT-NORMALIZED":
        "概念未归一到规范概念（530 任务3 新规则）：按 526/528 STAGING 名单回填 normalized 概念，"
        "或人工签收；**是新规则上线后的存量迁移谷，非内容退化**。",
    "INFERENCE-NOT-MACHINE-VERIFIED":
        "inference 命题缺机器复核（526 P65）：按 526/528 backlog 做命题回填（机器复核或人签）；"
        "**非内容退化**。",
}

# 桶②：需逐条甄别的规则（(a) 设计排除=预期 → 留桶②；(b) 真缺 → 转桶③）。
BUCKET2_RULES = frozenset({"EV-MATRIX-UNBACKED"})

# 桶③：真信号（每条附"为何是真信号 + 建议动作"）。
BUCKET3_RULES: dict[str, str] = {
    "EV-OUT-UNDECLARED-KEY": ".out 读数键未在 run_match_keys 声明：跨平台读数口径漏声明，补声明或删多余键。",
    "EV-FALSIFICATION-QUANT": "证伪对照缺量化取值：判据不可复算（伪证伪），补量化取值。",
    "EV-ASSERT-SYMBOL-MAPPED": "断言文本在夹具/工件/symbol_map 中定位不到：断言可能悬空，补锚或改断言。",
    "ATOM-REL-TARGET": "relations 指向的目标不存在：知识图断链，补目标或修关系。",
    "EV-ENV-DEPENDENT-KEY": "环境量进入读数键：跨机不可复算，移出读数键或声明环境。",
    "EV-OUT-STALE-MTIME": ".out 比源夹具旧：留痕疑似陈旧，重跑生成。",
    "EV-SERVES-EXIST": "证据卡 serves 指向的原子尚未锻造：**若该原子按阶段门待批则属预期中间态**，"
                       "反之补原子或修 serves。",
}

# KIL 数据缺失时的兜底权重（越大越先看）。KIL=知识完整性等级（555 批次 U），当前仓库无该数据。
RULE_WEIGHT: dict[str, int] = {
    "EV-MATRIX-UNBACKED": 85,        # 桶② (b) 转来的真信号
    "EV-OUT-UNDECLARED-KEY": 90, "EV-FALSIFICATION-QUANT": 80, "EV-ASSERT-SYMBOL-MAPPED": 70,
    "ATOM-REL-TARGET": 60, "EV-ENV-DEPENDENT-KEY": 50, "EV-OUT-STALE-MTIME": 40,
    "EV-SERVES-EXIST": 30,
}

# 锚口径与 `check_evidence_matrix_backed` 一致（.out 路径 / run #号 / 10+ 位数字）。
_OUT_RE = re.compile(r"(?:Examples|build)/[^\s\])]+\.out")
_RUN_RE = re.compile(r"run\s*#(\d+)")
_RUN_NO_RE = re.compile(r"\d{10,}")
_LAW_RE = re.compile(r"标准条文|M2.*永久边界")
_NOTICE_RE = re.compile(r"::notice::")


def _git_short() -> str:
    try:
        p = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                           capture_output=True, text=True, timeout=10, check=False)
        return (p.stdout or "").strip() or "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def _split_excluded(raw: str) -> tuple[str, str]:
    """按 `_raw_without_actual` 的同一口径，把文本切成 (可计入体, 被刻意排除段)。"""
    body: list[str] = []
    excluded: list[str] = []
    skipping = False
    for ln in raw.split("\n"):
        if re.match(r"^(actual:|artifact_sha256:)", ln):
            skipping = True
            excluded.append(ln)
            continue
        if skipping:
            if re.match(r"^\S", ln) or ln.startswith("---"):
                skipping = False
            else:
                excluded.append(ln)
                continue
        body.append(ln)
    return "\n".join(body), "\n".join(excluded)


def _anchors(text: str) -> int:
    return (len(set(_OUT_RE.findall(text))) + len(set(_RUN_RE.findall(text)))
            + len(set(_RUN_NO_RE.findall(text))))


def matrix_kind(target: str) -> tuple[str, str]:
    """判 `EV-MATRIX-UNBACKED` 一条是 (a) 设计排除造成的预期，还是 (b) 真缺支撑。

    与规则实现同一口径（三个锚），并额外统计**被刻意排除**的 actual/artifact_sha256 段：
      (a) 把被排除段算进来就 ≥2 锚（或 body 有 notice+锚 / 标准条文）⇒ 命中纯由设计排除造成；
      (b) 即便算上被排除段仍 <2 锚 ⇒ 卡确实缺可核对留痕 ⇒ 真信号。
    """
    p = ROOT / target
    try:
        raw = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return "b_real", f"读取失败 {type(exc).__name__}（fail-loud，按真信号处理）"
    body, excluded = _split_excluded(raw)
    cb, cx = _anchors(body), _anchors(excluded)
    backed_if_counted = (cb + cx >= 2) or (bool(_NOTICE_RE.search(body)) and (cb + cx >= 1)) \
        or bool(_LAW_RE.search(body))
    ev = f"policy=actual-excluded; anchors body={cb} excluded={cx}"
    return ("a_design", ev + "; would-be-backed") if backed_if_counted \
        else ("b_real", ev + "; no-two-anchors-anywhere")


def collect_findings() -> list:
    """gate 全量非 block 信号（warn + advice）——只读一次。"""
    return [f for f in ge.run(include_advice=True) if f.severity in ("warn", "advice")]


def _exempt_rules() -> set[str]:
    """golden_lock 已分类为 false_positive/legacy/accepted 的规则（=已登记豁免）。"""
    try:
        st = json.loads(GOLDEN_STATE.read_text(encoding="utf-8"))
        cmap = st.get("warn_classify")
        cmap = cmap if isinstance(cmap, dict) else {}
    except (OSError, ValueError):
        return set()
    return {str(k) for k, v in cmap.items() if v in ("false_positive", "legacy", "accepted")}


def bucket_of(finding, exempt: frozenset[str], mkind: tuple[str, str] | None = None) -> str:
    """单条 Finding → 桶名（B1..B4）。未登记规则默认落 B3（可见优先，不静默藏）。"""
    rid = finding.rule_id
    if rid in exempt:
        return "B4"
    if rid in BUCKET1_ACTIONS:
        return "B1"
    if rid in BUCKET2_RULES:
        return "B2" if (mkind and mkind[0] == "a_design") else "B3"
    if rid in BUCKET3_RULES:
        return "B3"
    return "B3"          # 未登记规则：默认真信号（fail-loud，别藏）


def triage(findings: list | None = None) -> dict:
    """把 Finding 集分四桶，返回可 JSON 化的报告 dict（确定性）。"""
    findings = collect_findings() if findings is None else list(findings)
    exempt = frozenset(_exempt_rules())
    mcache: dict[str, tuple[str, str]] = {}
    seen: set[tuple] = set()
    buckets: dict[str, list[dict]] = {"B1": [], "B2": [], "B3": [], "B4": []}
    for f in findings:
        rid = f.rule_id
        key = (rid, f.severity, f.target, f.message)
        if key in seen:
            buckets["B4"].append({"rule": rid, "severity": f.severity, "card": f.target,
                                  "why": "完全重复命中", "action": "去重即可"})
            continue
        seen.add(key)
        item = {"rule": rid, "severity": f.severity, "card": f.target, "message": f.message}
        if rid in BUCKET2_RULES:
            if f.target not in mcache:
                mcache[f.target] = matrix_kind(f.target)
            kind, ev = mcache[f.target]
            item["matrix_kind"] = kind
            item["evidence"] = ev
            item["action"] = ("规则预期：锚落在被刻意排除的 actual 段 ⇒ 建议登记豁免或细化规则措辞"
                              if kind == "a_design" else
                              "真信号（处处无两处留痕）：补两处可核对留痕，或按设计确认后登记豁免")
        elif rid in BUCKET1_ACTIONS:
            item["action"] = BUCKET1_ACTIONS[rid]
        elif rid in BUCKET3_RULES:
            item["action"] = BUCKET3_RULES[rid]
        else:
            item["action"] = "未登记规则：请人审定性"
        buckets[bucket_of(f, exempt, mcache.get(f.target))].append(item)
    counts = {b: len(v) for b, v in buckets.items()}
    return {
        "schema": 1, "tool": "review_triage", "commit": _git_short(),
        "totals": {"non_block": len(findings),
                   "warn": sum(1 for f in findings if f.severity == "warn"),
                   "advice": sum(1 for f in findings if f.severity == "advice")},
        "counts": counts,
        "by_rule": dict(sorted(Counter(f.rule_id for f in findings).items())),
        "buckets": buckets,
    }


def review_order(items: list[dict]) -> list[dict]:
    """桶③确定性人审排序：规则权重降序（KIL 缺失兜底）→ 卡 id → 规则 id → 消息首 40 字。"""
    return sorted(items, key=lambda it: (-RULE_WEIGHT.get(it["rule"], 10),
                                         it["card"], it["rule"], it["message"][:40]))


def _print_summary(rep: dict) -> None:
    t, c = rep["totals"], rep["counts"]
    print(f"[triage] commit={rep['commit']} 非 block 命中={t['non_block']}"
          f"（warn {t['warn']} + advice {t['advice']}）")
    print(f"[triage] 四桶计数：①迁移过程债 {c['B1']} · ②规则设计待甄别 {c['B2']}"
          f" · ③真信号 {c['B3']} · ④已登记豁免/重复 {c['B4']}"
          f"  （合计 {sum(c.values())}，与总量对账{'一致' if sum(c.values()) == t['non_block'] else '不一致!!'}）")
    print("[triage] 桶①按规则：" + "、".join(
        f"{r}×{n}" for r, n in sorted(Counter(i["rule"] for i in rep["buckets"]["B1"]).items())))
    print("[triage] 桶②逐条（(a)=规则预期，留桶②；(b)=真信号，已转桶③）：")
    for it in rep["buckets"]["B2"]:
        print(f"    [{it.get('matrix_kind')}] {it['card']}  {it.get('evidence')}")
    nb = [it for it in rep["buckets"]["B3"] if it["rule"] in BUCKET2_RULES]
    print(f"    （其中 (b) 真信号 {len(nb)} 条已并入桶③）")
    print("[triage] 桶③人审顺序（KIL 缺失，用规则权重+卡 id 兜底）：")
    for it in review_order(rep["buckets"]["B3"]):
        print(f"    {it['severity']:6s} {it['rule']:26s} {it['card']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="557 Part A 人审分桶器（纯读，不 accept）")
    ap.add_argument("--json", action="store_true", help="写 data/review/triage_<gitshort>.json")
    ap.add_argument("--review-order", action="store_true", help="只打印桶③的确定性人审顺序")
    ap.add_argument("--order", action="store_true", help=argparse.SUPPRESS)   # 别名
    a = ap.parse_args(argv)
    rep = triage()
    _print_summary(rep)
    if a.json:
        REVIEW_DIR.mkdir(parents=True, exist_ok=True)
        out = REVIEW_DIR / f"triage_{rep['commit']}.json"
        out.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"[triage] 已写 {out.relative_to(ROOT).as_posix()}"
              f"（大 JSON 不入库，.gitignore 已忽略 data/review/）")
    if a.review_order or a.order:
        print("[triage] === 桶③ 人审顺序 ===")
        for i, it in enumerate(review_order(rep["buckets"]["B3"]), 1):
            print(f"  {i:2d}. {it['rule']:26s} {it['card']}  —  {it['action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
