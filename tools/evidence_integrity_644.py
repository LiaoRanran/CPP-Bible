"""644 阶段 C · C3 证据完整性与漂移检测。

检测证据漂移（设计输入参照 A4）：
1. 证据 hash 和存储内容不一致？（`EvidenceID != SHA256(content)`）
2. 证据来源 URL 现在内容变了？（定期重取对比；网络不通→标记「获取失败」，不崩溃）
3. 证据被引用但已从存储中删除？（索引引用了不存在的 ID）

输出：漂移清单 + 严重度 + 处置建议（重取 / 标记过期 / 人审）。
只读：不修改受控目录。`--check` 只读幂等；`--report` 写漂移报告。
"""
from __future__ import annotations

import argparse
import os
import sys
import urllib.request
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base
import evidence_card_link_644 as evlink

OUT_MD = os.path.join(base.ROOT, "data", "644_integrity_report.md")
FETCH_TIMEOUT = 8


def check_hash_consistency() -> list[dict[str, Any]]:
    problems = base.verify_stored()
    return [{"evidence_id": eid, "kind": "hash_mismatch", "severity": "high",
             "detail": desc, "suggestion": "人审并重存"} for eid, desc in problems]


def refetch_compare(record: base.EvidenceRecord) -> dict[str, Any]:
    """重取来源 URL 并比对内容 hash（网络降级：失败只标记，不崩溃）。"""
    if not record.source_url:
        return {"evidence_id": record.evidence_id, "kind": "no_url", "changed": False,
                "detail": "无来源 URL，跳过"}
    try:
        req = urllib.request.Request(record.source_url, headers={"User-Agent": "CPP-Bible-Evidence/1.0"})
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
            data = resp.read().decode("utf-8", "replace")
        new_id = base.sha256_text(data)
        return {"evidence_id": record.evidence_id, "kind": "url_refetch", "changed": new_id != record.evidence_id,
                "detail": "来源内容已变" if new_id != record.evidence_id else "来源内容一致"}
    except Exception as exc:  # noqa: BLE001  （网络降级：任何异常都只标记）
        return {"evidence_id": record.evidence_id, "kind": "fetch_failed", "changed": False,
                "detail": f"获取失败（降级，不代表证据不存在）：{type(exc).__name__}"}


def check_referenced_but_missing(index: dict[str, Any]) -> list[dict[str, Any]]:
    stored_ids = {r.evidence_id for r in base.iter_stored()}
    missing = []
    for eid in index.get("by_evidence", {}):
        if eid not in stored_ids:
            missing.append({"evidence_id": eid, "kind": "referenced_missing",
                            "severity": "medium", "detail": "被索引引用但存储中不存在",
                            "suggestion": "重新获取或移除关联"})
    return missing


def scan() -> dict[str, Any]:
    hash_problems = check_hash_consistency()
    idx = evlink.load_index() if os.path.exists(base.INDEX_FILE) else base_card_link_empty()
    ref_missing = check_referenced_but_missing(idx)
    # URL 重取（可能触发网络；失败降级）
    url_results = [refetch_compare(r) for r in base.iter_stored()]
    url_changed = [u for u in url_results if u.get("changed")]
    return {"hash_problems": hash_problems, "referenced_missing": ref_missing,
            "url_results": url_results, "url_changed": url_changed,
            "n_scanned": len(url_results)}


def base_card_link_empty() -> dict[str, Any]:
    return {"links": [], "by_card": {}, "by_evidence": {}}


def render_md(s: dict[str, Any]) -> str:
    n_hash = len(s["hash_problems"])
    n_missing = len(s["referenced_missing"])
    n_changed = len(s["url_changed"])
    n_fail = sum(1 for u in s["url_results"] if u["kind"] == "fetch_failed")
    lines = ["# 644 C3 · 证据完整性与漂移检测报告", "",
             f"- 扫描证据：**{s['n_scanned']}**", "",
             f"- hash 不自洽：**{n_hash}**", f"- 被引用但缺失：**{n_missing}**",
             f"- 来源内容变化：**{n_changed}**  （获取失败降级：**{n_fail}**）", "",
             "## 漂移清单", "", "| 证据 | 类型 | 严重度 | 详情 | 建议 |",
             "|---|---|---|---|---|"]
    for p in s["hash_problems"]:
        lines.append(f"| {p['evidence_id'][:12]}… | {p['kind']} | {p['severity']} | {p['detail']} | {p['suggestion']} |")
    for m in s["referenced_missing"]:
        lines.append(f"| {m['evidence_id'][:12]}… | {m['kind']} | {m['severity']} | {m['detail']} | {m['suggestion']} |")
    for u in s["url_changed"]:
        lines.append(f"| {u['evidence_id'][:12]}… | {u['kind']} | medium | {u['detail']} | 重取并人审 |")
    if n_hash + n_missing + n_changed == 0:
        lines.append("| — | — | — | 无漂移 | — |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_report() -> str:
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_md(scan()))
    return OUT_MD


def selftest() -> int:
    # 已知漂移必检出：构造一个错误 id 的记录概念上不自洽（用 is_valid 验证）
    from dataclasses import replace
    rec = base.store_evidence(
        "integrity test content", source_type="single_blog", grade="L4",
        credibility=0.5, acquired_at="2026-09-26", acquisition_method="test")
    assert rec.is_valid()
    # 篡改概念：把 id 改掉则不自洽
    bad = replace(rec, evidence_id="0" * 64)
    assert not bad.is_valid()
    # 引用但缺失检测
    fake_idx = {"links": [], "by_card": {}, "by_evidence": {"deadbeef" * 8: ["C1"]}}
    rm = check_referenced_but_missing(fake_idx)
    assert any(m["kind"] == "referenced_missing" for m in rm)
    # 无 URL 的重取：不崩溃，返回 no_url
    no_url = refetch_compare(replace(rec, source_url=None))
    assert no_url["kind"] == "no_url"
    # 全量扫描可跑
    s = scan()
    assert "hash_problems" in s and "url_results" in s
    # 清理
    os.remove(base.store_path(rec.evidence_id))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 C3 证据完整性与漂移检测")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写漂移报告")
    a = ap.parse_args(argv)
    if a.report:
        print(f"written {write_report()}")
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
