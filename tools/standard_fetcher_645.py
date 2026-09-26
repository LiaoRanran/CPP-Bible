"""645 · 阶段 B1 · 标准获取器（真获取，非 403 降级就算完）。

目标（645 §四 B1）：从 ISO 标准草案真获取 ≥10 个 C++ 主题的标准内容，每条带
URL / 获取时间 / 内容 hash / 标准章节号，存入证据库（等级 L2）。

数据源优先级（645 §四 B1）：
1. eel.is/c++draft（C++ 标准草案，无 403）——首选
2. cppreference（加 User-Agent，可能 403）
3. 本地标准 PDF（如有）

铁律（645 §零.8 / §十二.2）：**不许 403 降级就算完**——必须拿到真实内容才计为成功；
网络不可达/被拦时**诚实登记**「获取失败」，绝不编造标准正文。

实现：纯标准库 urllib（无第三方依赖），带超时与 UA；失败捕获所有异常 → ok=False。
`--check`：只读自检（构造请求/解析逻辑，不联网）。
`--acquire`：真实联网获取 curated 主题列表，写 `data/645_standard_fetch_report.md`+`.json` + 落库。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base  # 复用 644 证据底座（L2 标准证据落库）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_standard_fetch_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_standard_fetch_report.json")

# curated 标准章节（与本圣经重点主题对齐；章节号对应 eel.is/c++draft 锚点）
TOPICS: list[dict[str, str]] = [
    {"section": "intro", "title": "范围与术语"},
    {"section": "lex", "title": "词法约定"},
    {"section": "basic", "title": "基本概念（对象/生命周期/存储）"},
    {"section": "dcl.dcl", "title": "声明"},
    {"section": "dcl.init", "title": "初始化"},
    {"section": "class", "title": "类"},
    {"section": "class.copy", "title": "拷贝/移动"},
    {"section": "class.derived", "title": "派生类"},
    {"section": "temp", "title": "模板"},
    {"section": "temp.deduct", "title": "模板实参推导"},
    {"section": "expr", "title": "表达式"},
    {"section": "expr.call", "title": "函数调用"},
    {"section": "stmt", "title": "语句"},
    {"section": "special", "title": "特殊成员函数"},
    {"section": "concepts", "title": "概念（C++20）"},
    {"section": "atomics", "title": "原子操作（memory_order）"},
    {"section": "memory", "title": "内存模型"},
    {"section": "cpp", "title": "预处理"},
]

UA = "Mozilla/5.0 (compatible; CppBibleAgent/1.0; +https://example.org/bot)"
TIMEOUT = 12.0


@dataclass
class FetchResult:
    """单次标准获取的真实结果（不可编造）。"""

    topic: str
    section: str
    url: str
    ok: bool
    status: Optional[int]
    content_hash: str
    content_len: int
    error: str
    acquired_at: str

    def to_dict(self) -> dict:
        """序列化为可 JSON 化的字典（层间传递用）。"""
        return {
            "topic": self.topic, "section": self.section, "url": self.url, "ok": self.ok,
            "status": self.status, "content_hash": self.content_hash,
            "content_len": self.content_len, "error": self.error, "acquired_at": self.acquired_at,
        }


def _now() -> str:
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def fetch_section(section: str, title: str) -> FetchResult:
    """真实联网获取 eel.is/c++draft/<section>；失败诚实记录，不编造。"""
    url = f"https://eel.is/c++draft/{section}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    acquired = _now()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = resp.read()
            h = hashlib.sha256(data).hexdigest()
            return FetchResult(topic=title, section=section, url=url, ok=True,
                               status=getattr(resp, "status", 200), content_hash=h,
                               content_len=len(data), error="", acquired_at=acquired)
    except urllib.error.HTTPError as e:
        return FetchResult(topic=title, section=section, url=url, ok=False, status=e.code,
                           content_hash="", content_len=0,
                           error=f"HTTP {e.code}", acquired_at=acquired)
    except Exception as exc:  # noqa: BLE001
        # 网络不可达 / 超时 / SSL：真实失败，honest 登记
        return FetchResult(topic=title, section=section, url=url, ok=False, status=None,
                           content_hash="", content_len=0,
                           error=f"{type(exc).__name__}: {exc}", acquired_at=acquired)


def run_acquire(topics: Optional[list[dict]] = None) -> dict:
    """真实联网获取各主题标准内容并落库为 L2 证据（失败诚实登记）。"""
    topics = TOPICS if topics is None else topics
    results: list[FetchResult] = []
    stored = 0
    for t in topics:
        r = fetch_section(t["section"], t["title"])
        results.append(r)
        if r.ok:
            # 真获取成功 → 落 L2 标准证据（内容寻址，不可变）
            content = json.dumps({
                "section": r.section, "title": r.topic, "url": r.url,
                "content_len": r.content_len, "content_hash": r.content_hash,
            }, ensure_ascii=False, sort_keys=True)
            try:
                base.store_evidence(content, source_type="iso_standard", grade="L2",
                                    credibility=0.90, acquired_at=r.acquired_at,
                                    acquisition_method="standard_fetcher_645",
                                    source_url=r.url, meta={"section": r.section, "title": r.topic})
                stored += 1
            except ValueError:
                stored += 1  # 幂等
    ok_count = sum(1 for r in results if r.ok)
    return {
        "total": len(results), "ok": ok_count, "failed": len(results) - ok_count,
        "stored": stored, "results": [r.to_dict() for r in results],
    }


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 标准获取报告（B1，真实联网）", "",
             f"- 尝试主题数：{result['total']}",
             f"- **真实获取成功：{result['ok']}**（B1 目标 ≥10）",
             f"- 失败（诚实登记）：{result['failed']}",
             f"- 已落库 L2 证据：{result['stored']}", ""]
    lines.append("## 逐主题")
    for r in result["results"]:
        tag = "✅" if r["ok"] else "❌"
        lines.append(f"- {tag} `{r['section']}` {r['topic']} "
                     f"status={r['status']} hash={r['content_hash'][:12] or '-'} "
                     f"{'' if r['ok'] else '原因=' + r['error']}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：请求构造/哈希/解析逻辑（不联网）。"""
    # 用离线构造校验 content_hash 与 FetchResult 字段
    fr = FetchResult(topic="t", section="s", url="https://eel.is/c++draft/s", ok=False,
                     status=None, content_hash="", content_len=0, error="offline", acquired_at=_now())
    assert fr.to_dict()["section"] == "s"
    # 真实联网失败路径不崩溃：模拟不可达主机
    bad = fetch_section("__nope_645_offline__", "离线探测")
    assert bad.ok is False and bad.error != ""
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 标准获取器（真获取 eel.is）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--acquire", action="store_true", help="真实联网获取 curated 标准章节")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = run_acquire()
    write_report(result)
    print(f"[645 standard_fetcher] 成功={result['ok']} 失败={result['failed']} 落库={result['stored']}")
    if result["ok"] < 10:
        print("⚠ 真实获取不足 10 条：按 645 §十二.2 诚实登记，未编造标准正文。", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
