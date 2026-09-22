"""622 C2 · 原子卡 verdict 提取（27 张，**不修改原始卡**）

**为什么需要**：621 C2 发现 27 张原子卡**全部** UNDECIDED，根因是原子卡
**没有 `verdict` 字段**（原子卡用 `status` + `evidence` + `claim_structured`）。
⇒ 不是"真弃权"，而是"缺字段导致机器无法判定"。

**提取规则**（规则-based，逐条可复算；优先级从上到下）：

| # | 条件 | verdict | 置信度 | basis |
|---|---|---|---|---|
| 1 | `status` ∈ {verified, red-team-verified} | SUPPORTED | **high** | `status=verified` |
| 2 | `status` ∈ {refuted, rejected} 或 status_history 末态为 refuted | REFUTED | **high** | `status=refuted` |
| 3 | `status` = draft 且 `evidence` 非空且 claim_type 全为 observation | SUPPORTED | **medium** | `draft+observation+evidence` |
| 4 | `evidence` 非空 | SUPPORTED | **low** | `evidence_only` |
| 5 | 其余 | UNDECIDED | **high** | `no_signal` |

**硬边界**：**不修改原始卡** —— 提取结果只写 `data/` 下的 JSONL 与报告。
是否把 `verdict` 写回原子卡 = **人拍板项**（622 §八.3）。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

DEFAULT_OUT = os.path.join(ROOT, "data", "atom_verdict_extraction_622.jsonl")
VERIFIED = ("verified", "red-team-verified")
REFUTED = ("refuted", "rejected")


def discover_atoms(root: str = ROOT) -> list[str]:
    out = []
    for dirpath, _dirs, files in os.walk(os.path.join(root, "atoms")):
        for f in sorted(files):
            if f.endswith(".md") and f.startswith("ATOM-"):
                rel = os.path.relpath(os.path.join(dirpath, f), root)
                out.append(rel.replace(os.sep, "/"))
    return sorted(out)


def _signals(fm: dict) -> dict:
    cs = fm.get("claim_structured") or []
    types = [str(c.get("claim_type")) for c in cs if isinstance(c, dict)]
    ev = fm.get("evidence") or []
    hist = fm.get("status_history") or []
    last_hist = ""
    if isinstance(hist, list) and hist:
        h = hist[-1]
        last_hist = str((h or {}).get("level") or "") if isinstance(h, dict) else ""
    return {
        "status": str(fm.get("status") or "").strip().lower(),
        "evidence_count": len(ev) if isinstance(ev, list) else 0,
        "claim_types": sorted(set(types)),
        "status_history_last": last_hist.strip().lower(),
        "has_verdict_field": "verdict" in fm,
    }


def extract(fm: dict) -> dict:
    """从 frontmatter 提取 verdict（不修改卡片）。"""
    s = _signals(fm)
    if s["has_verdict_field"]:
        v = str(fm.get("verdict") or "").strip().lower()
        return {"verdict": "SUPPORTED" if v == "confirm" else
                            ("REFUTED" if v == "refute" else "UNDECIDED"),
                "confidence": "high", "basis": "card_verdict", "signals": s}
    if s["status"] in VERIFIED:
        return {"verdict": "SUPPORTED", "confidence": "high",
                "basis": f"status={s['status']}", "signals": s}
    if s["status"] in REFUTED or s["status_history_last"] in REFUTED:
        return {"verdict": "REFUTED", "confidence": "high",
                "basis": f"status={s['status'] or s['status_history_last']}", "signals": s}
    if (s["status"] == "draft" and s["evidence_count"] > 0
            and s["claim_types"] and all(t == "observation" for t in s["claim_types"])):
        return {"verdict": "SUPPORTED", "confidence": "medium",
                "basis": "draft+observation+evidence", "signals": s}
    if s["evidence_count"] > 0:
        return {"verdict": "SUPPORTED", "confidence": "low",
                "basis": "evidence_only", "signals": s}
    return {"verdict": "UNDECIDED", "confidence": "high", "basis": "no_signal", "signals": s}


def extract_card(card_rel: str) -> dict:
    import pck_batch_migrator_620 as M  # noqa: PLC0415
    fm = M.read_frontmatter(os.path.join(ROOT, card_rel))
    res = extract(fm)
    return {"card": card_rel, "card_id": fm.get("id") or os.path.basename(card_rel)[:-3],
            **res}


def extract_all(cards: list[str] | None = None) -> list[dict]:
    return [extract_card(c) for c in (cards or discover_atoms())]


def verdict_index(rows: list[dict]) -> dict[str, str]:
    """供 C1 v2 分类器消费：{card_id: SUPPORTED|REFUTED|UNDECIDED}。"""
    return {r["card_id"]: r["verdict"] for r in rows}


def write_jsonl(rows: list[dict], path: str = DEFAULT_OUT) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def render_report(rows: list[dict]) -> str:
    v: dict[str, int] = {}
    c: dict[str, int] = {}
    b: dict[str, int] = {}
    for r in rows:
        v[r["verdict"]] = v.get(r["verdict"], 0) + 1
        c[r["confidence"]] = c.get(r["confidence"], 0) + 1
        b[r["basis"]] = b.get(r["basis"], 0) + 1
    o = ["# 622 C2 · 原子卡 verdict 提取（27 张）\n"]
    o.append(f"> 提取总数：**{len(rows)}**（**未修改任何原始卡**）\n")
    o.append("## 一、提取结果分布\n")
    o.append("| verdict | 张数 |")
    for k, n in sorted(v.items(), key=lambda kv: -kv[1]):
        o.append(f"| {k} | {n} |")
    o.append("")
    o.append("## 二、置信度分布\n")
    o.append("| 置信度 | 张数 |")
    for k, n in sorted(c.items(), key=lambda kv: -kv[1]):
        o.append(f"| {k} | {n} |")
    o.append("")
    o.append("## 三、提取依据分布\n")
    o.append("| basis | 张数 |")
    for k, n in sorted(b.items(), key=lambda kv: -kv[1]):
        o.append(f"| `{k}` | {n} |")
    o.append("")
    o.append("## 四、与 621 C2 的对比\n")
    o.append("| 项 | 621 C2（分类器 v1） | 622 C2（提取后） |")
    o.append("|---|---|---|")
    o.append(f"| 原子卡 UNDECIDED | **27 / 27** | **{v.get('UNDECIDED', 0)} / {len(rows)}** |")
    o.append(f"| 原子卡 SUPPORTED | 0 | **{v.get('SUPPORTED', 0)}** |")
    o.append(f"| 原子卡 REFUTED | 0 | **{v.get('REFUTED', 0)}** |")
    o.append("")
    o.append("## 五、逐卡明细\n")
    o.append("| 卡 ID | verdict | 置信度 | basis | status | 证据数 |")
    for r in rows:
        s = r["signals"]
        o.append(f"| {r['card_id']} | {r['verdict']} | {r['confidence']} | "
                 f"`{r['basis']}` | {s['status']} | {s['evidence_count']} |")
    o.append("")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("verified → SUPPORTED(high)",
        extract({"status": "verified", "evidence": ["E1"]})["verdict"] == "SUPPORTED")
    chk("red-team-verified → SUPPORTED",
        extract({"status": "red-team-verified", "evidence": ["E1"]})["verdict"] == "SUPPORTED")
    chk("refuted → REFUTED",
        extract({"status": "refuted", "evidence": ["E1"]})["verdict"] == "REFUTED")
    chk("draft+observation+evidence → SUPPORTED(medium)",
        extract({"status": "draft", "evidence": ["E1"],
                 "claim_structured": [{"claim_type": "observation"}]})["confidence"] == "medium")
    chk("draft+inference → 落到 evidence_only(low)",
        extract({"status": "draft", "evidence": ["E1"],
                 "claim_structured": [{"claim_type": "inference"}]})["basis"] == "evidence_only")
    chk("无证据无状态 → UNDECIDED",
        extract({})["verdict"] == "UNDECIDED")
    chk("卡面已有 verdict 字段时优先",
        extract({"verdict": "confirm"})["basis"] == "card_verdict")
    chk("发现 27 张原子卡", len(discover_atoms()) == 27)
    chk("提取全部 27 张且带 basis",
        all(r.get("basis") and r.get("verdict") in
            ("SUPPORTED", "REFUTED", "UNDECIDED") for r in extract_all()))
    chk("verdict_index 可用", len(verdict_index(extract_all())) == 27)
    print(f"C2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="622 C2 原子卡 verdict 提取（不改原始卡）")
    ap.add_argument("--out", default=DEFAULT_OUT, help="提取结果 JSONL")
    ap.add_argument("--report", help="报告输出路径")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    rows = extract_all()
    write_jsonl(rows, args.out)
    dist: dict[str, int] = {}
    for r in rows:
        dist[r["verdict"]] = dist.get(r["verdict"], 0) + 1
    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(render_report(rows) + "\n")
        print(f"wrote {args.report}")
    print(json.dumps({"total": len(rows), "distribution": dist,
                      "out": args.out}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
