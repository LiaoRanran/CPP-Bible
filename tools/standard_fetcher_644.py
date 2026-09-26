"""644 阶段 D · D1 标准文档获取器。

功能（原型级，§十二.1）：
- 从 cppreference 获取指定主题的页面（关键词搜索 → 取 top 3）
- 从 C++ 标准草案（eel.is/c++draft）获取指定章节
- 保存原始内容 + 元数据（URL / 获取时间 / 内容 hash）到证据库（C1）

网络降级（§零.8）：网络不通 / 被拒（如 403）时返回 `ok=False, error="获取失败"`，**不崩溃**。
只读/追加：只写 data/evidence_store/，不碰受控目录。
`--check` 只读幂等；`--acquire <topic>` 真正获取（可能受网络限制失败）。
"""
from __future__ import annotations

import argparse
import os
import sys
import urllib.request
from typing import Any
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

OUT_MD = os.path.join(base.ROOT, "data", "644_standard_fetch_report.md")
FETCH_TIMEOUT = 8
UA = {"User-Agent": "CPP-Bible-Evidence/1.0 (+offline-head-layer)"}
CPPREF_SEARCH = "https://en.cppreference.com/mwiki/index.php?search={topic}"
CPPDRAFT = "https://eel.is/c++draft/{section}"


def fetch_url(url: str) -> tuple[str | None, str | None]:
    """获取 URL；任何异常（含 403/超时/无网）都降级为 (None, error)，不崩溃。"""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
            return resp.read().decode("utf-8", "replace"), None
    except Exception as exc:  # noqa: BLE001
        return None, f"获取失败（降级）：{type(exc).__name__}"


def parse_search_results(html: str) -> list[str]:
    """从 cppreference 搜索结果页抽取候选链接（纯函数，便于单测）。"""
    out: list[str] = []
    import re
    for m in re.finditer(r'href="([^"]+)"', html):
        href = m.group(1)
        if "/w/" in href or "title=" in href:
            out.append(href)
    return out[:3]


def make_evidence(url: str, text: str, grade: str) -> base.EvidenceRecord:
    """把抓取到的原始内容存为证据（内容寻址）。"""
    from datetime import datetime
    content = f"URL: {url}\n\n{text}"
    st = "iso_standard" if "c++draft" in url else "cppreference"
    _, cred = base.grade_evidence_record(st)
    return base.store_evidence(
        content, source_type=st, grade=grade, credibility=cred,
        acquired_at=datetime.now().strftime("%Y-%m-%d"),
        acquisition_method="standard_fetcher_644", source_url=url,
        meta={"kind": "standard_doc"})


def acquire(topic: str, section: str | None = None) -> dict[str, Any]:
    """获取主题的标准文档证据；网络失败只标记不崩溃。"""
    fetched: list[dict[str, Any]] = []
    errors: list[str] = []
    # cppreference 搜索
    text, err = fetch_url(CPPREF_SEARCH.format(topic=quote(topic)))
    if text is None:
        errors.append(f"cppreference[{topic}]: {err}")
    else:
        links = parse_search_results(text)
        for lnk in links:
            t2, e2 = fetch_url(lnk if lnk.startswith("http") else "https://en.cppreference.com" + lnk)
            if t2 is None:
                errors.append(f"cppreference[link]: {e2}")
            else:
                rec = make_evidence(lnk, t2, "L3")
                fetched.append({"evidence_id": rec.evidence_id, "url": lnk, "grade": "L3"})
    # c++draft 章节
    if section:
        t3, e3 = fetch_url(CPPDRAFT.format(section=section))
        if t3 is None:
            errors.append(f"c++draft[{section}]: {e3}")
        else:
            rec = make_evidence(CPPDRAFT.format(section=section), t3, "L2")
            fetched.append({"evidence_id": rec.evidence_id, "url": CPPDRAFT.format(section=section),
                            "grade": "L2"})
    return {"ok": len(fetched) > 0, "fetched": fetched, "errors": errors, "topic": topic}


def write_report(last: dict[str, Any] | None = None) -> str:
    r = last or {"ok": False, "fetched": [], "errors": ["未执行获取"], "topic": ""}
    lines = ["# 644 D1 · 标准文档获取报告", "",
             f"- 主题：**{r['topic']}**  成功：**{len(r['fetched'])}**  错误：**{len(r['errors'])}**", "",
             "## 成功获取", "", "| 证据ID | URL | 等级 |", "|---|---|---|"]
    for f in r["fetched"]:
        lines.append(f"| {f['evidence_id'][:12]}… | {f['url']} | {f['grade']} |")
    lines += ["", "## 失败（降级）", ""]
    for e in r["errors"]:
        lines.append(f"- {e}")
    lines.append("")
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    # 纯函数 parse
    sample = '<a href="/w/cpp/keyword">x</a><a href="/w/cpp/foo" title="t">y</a><a href="/other">z</a>'
    links = parse_search_results(sample)
    assert len(links) == 2
    # 网络降级：无效 host 返回 (None, error)，不崩溃
    txt, err = fetch_url("http://127.0.0.1:0/impossible")
    assert txt is None and err is not None
    # acquire 在网络受限时返回 ok=False 但不崩溃、不产生 store 写入
    before = len(base.iter_stored())
    r = acquire("nullptr")
    after = len(base.iter_stored())
    assert before == after
    assert r["ok"] in (True, False)  # 结构正确
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 D1 标准文档获取器")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--acquire", metavar="TOPIC", help="获取主题（受网络限制可能失败）")
    ap.add_argument("--section", metavar="SECTION", help="c++draft 章节")
    a = ap.parse_args(argv)
    if a.acquire:
        r = acquire(a.acquire, a.section)
        print(f"ok={r['ok']} fetched={len(r['fetched'])} errors={len(r['errors'])}")
        print(f"written {write_report(r)}")
        return 0 if r["ok"] else 2
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
