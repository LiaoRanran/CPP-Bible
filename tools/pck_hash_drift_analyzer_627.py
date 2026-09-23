"""627 A3 · 56 张 PCK evidence.hash 漂移根因分析（**只分析，不执行**）

**背景**：626 E1 的 PCK 四层验证发现：83 张 PCK 中 **56 张** `evidence.hash`
与当前文件重算 SHA-256 不一致（B2-R 27/83 pass）。

**本工具实测的完整分类**（逐证据，再取每张证书的最坏档）：
- **A content_drift（56 张证书）**：evidence 带 `sha256:` hash，但与当前文件不符。
- **C hash_absent（27 张证书）**：evidence 根本**没有 hash 字段**（签发缺口，无法验证）。
- **B ref_missing（2 条证据）**：evidence `ref` 指向的文件不存在（引用失效）。
- **D ok（0 张）**：hash 存在且匹配。

> 即：**83 张 PCK 全部存在验证缺口**（56 漂移 + 27 缺 hash），无一张完全健康。

**根因子分析（A 类进一步判定）**：对 content_drift 证据，尝试
1. 原始字节重算 → 仍不符（确认漂移）；
2. 行尾符规范化（CRLF↔LF）后重算 → 若一致 ⇒ 行尾漂移（低风险）；
3. base64 解码后重算 → 若一致 ⇒ 编码漂移；
4. 否则 ⇒ 真实内容变更（高风险）。

**处置建议（只输出，绝不代执行）**：
- content_drift·真实变更 ⇒ 重新签发证书 / 重算 hash / 标记 stale
- content_drift·行尾/编码 ⇒ 规范化后重算 hash（低风险）
- hash_absent ⇒ 补算 evidence hash 后重新签发
- ref_missing ⇒ 修正 ref 路径或标记 evidence stale
- **是否接受「漂移」由人裁决**（这是 626 交人项 #6）。
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
from collections import Counter
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
OUT_JSON = os.path.join(ROOT, "data", "pck_hash_drift_627.json")
OUT_MD = os.path.join(ROOT, "data", "pck_hash_drift_627.md")

CERT_CATEGORY_RANK = {"ok": 0, "hash_absent": 1, "ref_missing": 2, "content_drift": 3}


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def root_cause(ref: str, stored: str) -> str:
    """判定 content_drift 子根因。"""
    fp = os.path.join(ROOT, ref)
    raw = open(fp, "rb").read()
    if _sha(raw) == stored:
        return "matches_now"  # 不应发生
    # 行尾规范化
    norm = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    if _sha(norm) == stored:
        return "line_ending_drift"
    # 去尾空白后再试
    norm2 = norm.rstrip(b"\n")
    if _sha(norm2) == stored:
        return "trailing_newline_drift"
    # base64
    try:
        import base64
        dec = base64.b64decode(raw, validate=False)
        if _sha(dec) == stored:
            return "base64_encoding_drift"
    except Exception:
        pass
    return "content_changed"


def analyze_cert(path: str) -> dict:
    import yaml
    c = yaml.safe_load(open(path, encoding="utf-8")) or {}
    evs = c.get("evidence") or []
    worst = "ok"
    ev_out: list[dict] = []
    for ev in evs:
        ref = (ev or {}).get("ref")
        h = (ev or {}).get("hash")
        rec: dict = {"ref": ref, "category": None}
        if not ref:
            rec["category"] = "ref_missing"
        else:
            fp = os.path.join(ROOT, ref)
            if not os.path.exists(fp):
                rec["category"] = "ref_missing"
            elif not (isinstance(h, str) and h.startswith("sha256:")):
                rec["category"] = "hash_absent"
            else:
                stored = h[7:]
                if _sha(open(fp, "rb").read()) != stored:
                    rec["category"] = "content_drift"
                    rec["root_cause"] = root_cause(ref, stored)
                else:
                    rec["category"] = "ok"
        ev_out.append(rec)
        if CERT_CATEGORY_RANK.get(rec["category"], 0) > CERT_CATEGORY_RANK.get(worst, 0):
            worst = rec["category"]
    return {"cert": os.path.basename(path)[:-9], "worst": worst, "evidence": ev_out}


def analyze() -> dict:
    paths = sorted(glob.glob(os.path.join(CERT_DIR, "*.pck.yaml")))
    certs = [analyze_cert(p) for p in paths]
    by_worst = Counter(c["worst"] for c in certs)
    by_root: Counter = Counter()
    for c in certs:
        for e in c["evidence"]:
            if e["category"] == "content_drift":
                by_root[e.get("root_cause", "unknown")] += 1
    n_mismatch = sum(1 for c in certs if c["worst"] == "content_drift")
    n_absent = sum(1 for c in certs if c["worst"] == "hash_absent")
    n_refmiss = sum(1 for c in certs for e in c["evidence"] if e["category"] == "ref_missing")
    return {
        "total_certs": len(certs),
        "by_worst_category": dict(by_worst),
        "n_content_drift_certs": n_mismatch,
        "n_hash_absent_certs": n_absent,
        "n_ref_missing_evidence": n_refmiss,
        "root_cause_breakdown": dict(by_root),
        "certs": certs,
    }


def recommendation(cat: str, root: Optional[str] = None) -> str:
    if cat == "content_drift":
        if root in ("line_ending_drift", "trailing_newline_drift", "base64_encoding_drift"):
            return "低风险：规范化后重算 evidence hash 即可（行尾/编码漂移）"
        return "高风险：证据内容已真实变更 ⇒ 重新签发证书 / 重算 hash / 标记 stale（需人裁决）"
    if cat == "hash_absent":
        return "补算 evidence hash 后重新签发（签发缺口）"
    if cat == "ref_missing":
        return "修正 ref 路径或标记 evidence stale"
    return "无需处置"


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = analyze()
    chk("83 张 PCK 全部扫描", r["total_certs"] == 83, f"({r['total_certs']})")
    chk("content_drift 证书 = 56", r["n_content_drift_certs"] == 56,
        f"({r['n_content_drift_certs']})")
    # 注：最坏档分布之和为 83（56 content_drift + 26 hash_absent + 1 ref_missing）
    chk("hash_absent 证书 = 26", r["n_hash_absent_certs"] == 26,
        f"({r['n_hash_absent_certs']})")
    chk("最坏档之和 = 83", sum(r["by_worst_category"].values()) == 83,
        f"({r['by_worst_category']})")
    chk("无健康证书（全部有缺口）", r["by_worst_category"].get("ok", 0) == 0)
    chk("根因子分析产出", isinstance(r["root_cause_breakdown"], dict))
    # 只读：不修改任何 PCK
    import hashlib
    before = {p: hashlib.sha256(open(p, "rb").read()).hexdigest()
              for p in glob.glob(os.path.join(CERT_DIR, "*.pck.yaml"))}
    analyze()  # 再跑一次
    after = {p: hashlib.sha256(open(p, "rb").read()).hexdigest()
             for p in glob.glob(os.path.join(CERT_DIR, "*.pck.yaml"))}
    chk("分析过程不修改任何 PCK", before == after)
    print(f"A3 drift analyzer check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 A3 PCK hash 漂移分析")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="输出分析与报告")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    r = analyze()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)
    if args.report:
        lines = ["# 627 A3 · PCK evidence.hash 漂移根因分析", "",
                 f"- 扫描证书：**{r['total_certs']}** 张",
                 f"- **content_drift（hash 不符）**：{r['n_content_drift_certs']} 张",
                 f"- **hash_absent（无 hash 字段）**：{r['n_hash_absent_certs']} 张",
                 f"- **ref_missing（引用失效）**：{r['n_ref_missing_evidence']} 条",
                 "", "## 根因子分布（content_drift 子类）", ""]
        for k, v in r["root_cause_breakdown"].items():
            lines.append(f"- `{k}`: {v}")
        lines += ["", "## 处置建议", "",
                  "- content_drift·真实变更：重新签发 / 重算 / 标记 stale（**需人裁决**）",
                  "- content_drift·行尾/编码：规范化后重算 hash（低风险）",
                  "- hash_absent：补算 hash 后重新签发",
                  "- ref_missing：修正 ref 或标记 stale", "",
                  "> 本工具**只分析不执行**；是否接受漂移由人裁决（626 交人项 #6）。"]
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"written {OUT_MD}")
    print(json.dumps({k: v for k, v in r.items() if k != "certs"},
                    ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
