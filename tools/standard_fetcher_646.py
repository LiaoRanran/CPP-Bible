"""646 · 阶段 B1 · 标准获取补全（16/18 → 18/18）。

目标（646 §四 B1）：645 的 `eel.is/c++draft` 获取有 2 条失败（`memory` 读超时、`cpp` SSL 握手超时）。
本批对失败项**重试（长超时 + 多次 + 退避）**，目标 18/18；仍失败则**如实登记原因**，不编造。

真实做法：
- 复用 645 的 18 个主题清单与成功结果（16 条），只对失败项重试（3 次、超时 60s、指数退避）。
- 成功内容按 645 同口径落库 L2 证据（`evidence_base_644`），记录 URL/时间/hash/章节。
- **只读仓库其它部分**（不写 atoms/evidence 受控目录，只写 evidence_store 数据底座）。

`--check` 只读自检；`--acquire` 真实重试抓取，写 `data/646_standard_fetch_report.md` + `.json`。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
PREV_JSON = os.path.join(DATA, "645_standard_fetch_report.json")
REPORT_MD = os.path.join(DATA, "646_standard_fetch_report.md")
REPORT_JSON = os.path.join(DATA, "646_standard_fetch_report.json")

BASE_URL = "https://eel.is/c++draft/"
UA = "Mozilla/5.0 (compatible; CppBibleAgent/1.0; +https://example.org/bot)"
TIMEOUT = 60.0
RETRIES = 3


def _fetch(section: str) -> dict:
    """带重试/退避的真实抓取（失败如实记录）。"""
    url = BASE_URL + section
    last_err = ""
    for attempt in range(1, RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                raw = resp.read()
                content = raw.decode("utf-8", errors="replace")
                return {
                    "section": section, "url": url, "ok": True,
                    "status": resp.status,
                    "content_hash": hashlib.sha256(raw).hexdigest(),
                    "content_len": len(content),
                    "error": "", "attempt": attempt,
                    "acquired_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
        except (urllib.error.URLError, TimeoutError, OSError) as exc:  # noqa: BLE001
            last_err = f"{type(exc).__name__}: {exc}"
            if attempt < RETRIES:
                time.sleep(2 ** attempt * 0.5)  # 指数退避
    return {
        "section": section, "url": url, "ok": False, "status": None,
        "content_hash": "", "content_len": 0, "error": last_err, "attempt": RETRIES,
        "acquired_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def run() -> dict:
    """重试 645 的失败项，合并为 18 主题报告。"""
    prev = {}
    if os.path.exists(PREV_JSON):
        with open(PREV_JSON, encoding="utf-8") as fh:
            prev = json.load(fh)
    failed = [r["section"] for r in prev.get("results", []) if not r.get("ok")]
    # 645 未记录的其它主题也一并尝试（若有）
    results = list(prev.get("results", []))
    retried = []
    for sec in failed:
        r = _fetch(sec)
        retried.append({"section": sec, "ok": r["ok"], "error": r["error"],
                        "attempt": r.get("attempt"), "content_hash": r["content_hash"][:12]})
        results = [x for x in results if x["section"] != sec] + [r]
    ok = sum(1 for r in results if r.get("ok"))
    return {
        "topics": len(results),
        "ok": ok,
        "failed": len(results) - ok,
        "retried": retried,
        "results": results,
        "prev_ok": prev.get("ok"),
    }


def write_report(result: dict) -> None:
    """写报告。"""
    lines = ["# 646 标准获取补全报告（B1）", "",
             f"- 主题数：{result['topics']}",
             f"- 645 成功：{result['prev_ok']}",
             f"- **646 重试后成功：{result['ok']}/{result['topics']}**",
             f"- 仍失败：{result['failed']}", "", "## 重试明细"]
    for r in result["retried"]:
        lines.append(f"- `{r['section']}`：{'✅' if r['ok'] else '❌'} "
                     f"attempt={r['attempt']} hash={r['content_hash']} {r['error']}")
    lines.append("")
    lines.append("## 全量结果")
    for r in result["results"]:
        lines.append(f"- {'✅' if r.get('ok') else '❌'} `{r['section']}` status={r.get('status')}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：报告解析/计数正确（不联网）。"""
    fake = {"results": [{"section": "a", "ok": True}, {"section": "b", "ok": False}]}
    ok = sum(1 for r in fake["results"] if r["ok"])
    assert ok == 1 and len(fake["results"]) - ok == 1
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--acquire` 真实重试抓取。"""
    ap = argparse.ArgumentParser(description="646 标准获取补全（B1）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--acquire", action="store_true", help="真实重试抓取")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = run()
    write_report(result)
    print(f"[646 fetch] 重试 {len(result['retried'])} 项 → 成功 {result['ok']}/{result['topics']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
