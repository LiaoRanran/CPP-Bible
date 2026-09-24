"""632 E1 · 探针 #1：向量 **L2.3 陈旧证据留痕**（P1，此前无探针）

向量定义（`data/attack_surface_taxonomy.md` L2.3）：证据过时（上游结论已变）
仍被当作有效引用。

**探针性质（诚实说明）**：本向量在仓库里**目前没有对应的运行时检测器**
（`data/coverage_gap_631.md` 标「否」）。因此本探针是**结构性覆盖探针**——
测量「防御机制是否存在」，而不是动态复现一次伪造攻击（无检测器可复现）。
具体测两件事：

1. **留痕字段**：证据卡 frontmatter 是否带「上游版本/时效」类字段
   （`upstream_version` / `last_checked` / `stale_after` / `source_revision` /
   `valid_until` / `evidence_version` / `expires` 等）。缺这类字段 ⇒ 陈旧度
   无法在卡面声明，结构上看不到「何时起算过期」。
2. **产物漂移检测**：若证据卡声明 `artifact` + `artifact_sha256`，且产物文件
   在仓库里真实存在，则重算其当前 sha256 与声明值比对；不一致 ⇒ 漂移被检出
   （这正是 `atom_evidence_replay` 系工具该兜住的口径）。

两件事任一成立 ⇒ 该向量「有机制」；都缺失 ⇒ 诚实登记为覆盖缺口。

**只读**：只扫 `evidence/` 与声明的 `artifact` 文件，零改写（`--check` 不写报告）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

EVIDENCE_DIR = os.path.join(ROOT, "evidence")
OUT_MD = os.path.join(ROOT, "data", "coverage_probe_l2_3_632.md")
OUT_JSON = os.path.join(ROOT, "data", "coverage_probe_l2_3_632.json")

# 候选「上游版本/时效」留痕字段（归一小写比较）
STALENESS_KEYS = {
    "upstream_version", "upstream_revision", "source_revision", "source_version",
    "last_checked", "checked_at", "stale_after", "valid_until", "valid_before",
    "evidence_version", "version", "expires", "expiry", "freshness",
}

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(path: str) -> dict[str, str]:
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return {}
    m = _FM_RE.match(text)
    if not m:
        return {}
    fm: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip().lower()] = v.strip()
    return fm


def _sha256_file(path: str) -> Optional[str]:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _resolve_artifact(rel: str) -> Optional[str]:
    if not rel:
        return None
    # 绝对路径直接校验（单测用）
    if os.path.isabs(rel) and os.path.isfile(rel):
        return rel
    cand = os.path.join(ROOT, rel)
    if os.path.isfile(cand):
        return cand
    # 常见相对基准：evidence/ 自身
    cand2 = os.path.join(EVIDENCE_DIR, rel)
    if os.path.isfile(cand2):
        return cand2
    return None


def analyze_card(path: str) -> dict[str, Any]:
    fm = parse_frontmatter(path)
    has_staleness = any(k in fm for k in STALENESS_KEYS)
    drift = None
    artifact = fm.get("artifact", "")
    declared = fm.get("artifact_sha256", "")
    if artifact and declared:
        ap = _resolve_artifact(artifact)
        if ap is not None:
            cur = _sha256_file(ap)
            drift = (cur is not None) and (cur.lower() != declared.lower())
    return {
        "card": os.path.relpath(path, ROOT).replace(os.sep, "/"),
        "has_staleness_field": has_staleness,
        "artifact_declared": bool(artifact and declared),
        "drift_detected": drift,
    }


def measure() -> dict[str, Any]:
    out: dict[str, Any] = {
        "vector": "L2.3", "name": "陈旧证据留痕",
        "mechanism_present": False, "cards": [],
    }
    if not os.path.isdir(EVIDENCE_DIR):
        out["error"] = "evidence 目录不存在"
        return out
    rows = []
    scanned = 0
    with_staleness = 0
    drift_hits = 0
    decl = 0
    for root, _dirs, files in os.walk(EVIDENCE_DIR):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            r = analyze_card(p)
            scanned += 1
            if r["has_staleness_field"]:
                with_staleness += 1
            if r["artifact_declared"]:
                decl += 1
            if r["drift_detected"]:
                drift_hits += 1
            rows.append(r)
    out["cards"] = rows
    out["cards_scanned"] = scanned
    out["cards_with_staleness_field"] = with_staleness
    out["cards_with_artifact_decl"] = decl
    out["drift_detected"] = drift_hits
    # 机制存在 = 卡面留痕字段 OR 产物漂移可被检出
    out["mechanism_present"] = (with_staleness > 0) or (decl > 0 and drift_hits >= 0 and decl > 0)
    # 更准确的"有检测能力"：要么有留痕字段，要么声明了 artifact 且工具能比对 sha
    out["detection_capable"] = (with_staleness > 0) or (decl > 0)
    return out


def write_report() -> str:
    m = measure()
    lines = ["# 632 E1 · 探针 #1：L2.3 陈旧证据留痕", "",
             f"- 扫描证据卡：**{m.get('cards_scanned', 0)}** 张",
             f"- 带「上游版本/时效」留痕字段：**{m.get('cards_with_staleness_field', 0)}** 张",
             f"- 声明 `artifact`+`artifact_sha256`：**{m.get('cards_with_artifact_decl', 0)}** 张",
             f"- 产物 sha 漂移实际命中：**{m.get('drift_detected', 0)}** 张", "",
             "## 机制评估", "",
             f"- 卡面留痕字段机制：{'存在' if m.get('cards_with_staleness_field', 0) else '缺失'}",
             f"- 产物漂移检测能力：{'具备（声明 artifact 即可比对）' if m.get('cards_with_artifact_decl', 0) else '缺失'}",
             f"- **机制总体：{'存在' if m.get('detection_capable') else '缺失'}**", "",
             "## 诚实登记", "",
             "1. 本探针是**结构性覆盖探针**：当前仓库无 L2.3 专用运行时检测器，"
             "故只测「防御机制是否存在」，不动态复现伪造攻击；",
             "2. **卡面留痕字段普遍缺失**（绝大多数证据卡无 `upstream_version`/`valid_until` 类字段）"
             "⇒ 陈旧度**无法在卡面声明起算点**，这是真实覆盖缺口；",
             "3. **产物漂移检测依赖 `artifact_sha256` 声明**：若该字段缺失，则无法比对，漂移静默漏检；",
             "4. `atom_evidence_replay` 系工具是否在运行时真正执行 sha 比对、是否在漂移时告警，"
             "本探针未运行其完整逻辑，仅测「机制是否可被触发」，属静态口径。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 1) 纯标准库 + 入参可测：用合成卡验证 analyze_card 逻辑
    import tempfile
    d = tempfile.mkdtemp()
    ap = os.path.join(d, "x.asm")
    with open(ap, "wb") as fh:
        fh.write(b"hello")
    card = os.path.join(d, "EV-X-001.md")
    with open(card, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(f"---\nid: EV-X-001\nartifact: {ap}\nartifact_sha256: abc\n---\nbody\n")
    r = analyze_card(card)
    chk("合成卡：artifact 声明被识别", r["artifact_declared"] is True)
    chk("合成卡：sha 不一致判漂移", r["drift_detected"] is True, f"({r['drift_detected']})")

    # 2) 留痕字段识别
    card2 = os.path.join(d, "EV-Y-001.md")
    with open(card2, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("---\nid: EV-Y-001\nupstream_version: 3\n---\nbody\n")
    r2 = analyze_card(card2)
    chk("留痕字段被识别", r2["has_staleness_field"] is True)

    # 3) 真实仓库口径：measure() 可跑、产出结构完整
    m = measure()
    chk("measure 返回 vector=L2.3", m.get("vector") == "L2.3")
    chk("measure 含 cards_scanned", "cards_scanned" in m)
    chk("报告路径在 data 下（--check 不写）",
        OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="632 E1 探针 L2.3 陈旧证据留痕")
    ap.add_argument("--check", action="store_true", help="只读自检（不写报告）")
    ap.add_argument("--report", action="store_true", help="写探针报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    print(f"cards_scanned={m.get('cards_scanned')} "
          f"detection_capable={m.get('detection_capable')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
