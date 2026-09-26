"""648 A · **C 标准原文抓取与条款抽取**（只做"引用可核对"，不解释标准）。

647 E1 把"标准源（WG14 N 文档）可用性与授权"列为**最大未决点**（需人裁决）。
648 的第一步就是把它**实测掉**，而不是继续挂着：

| 标准 | 文档 | 形式 | 648 实测 |
|---|---|---|---|
| C11（ISO/IEC 9899:2011） | **N1570** | HTML（port70 托管） | ✅ **逐条抽取原文**（带 URL + sha256 + 字节偏移） |
| C17（ISO/IEC 9899:2018） | **N2310** | PDF（open-std.org） | ⚠️ 可下载、sha256 留痕；**本环境无 PDF 解析器** ⇒ 原文未抽取（登记） |
| C23（ISO/IEC 9899:2024） | **N3096** | PDF（open-std.org） | ⚠️ 同上 |

**为什么 C17/C23 不靠"我记得"写条款**：记不准的条款号一旦写进卡就是硬错，
所以本批只把**能机器核对的**（N1570 HTML）写进卡的 `sources[]`，
C17/C23 只留**下载留痕**（URL + 字节数 + sha256），并在报告里写明"未逐条核对，需人核"。

抽取方式（N1570 HTML）：`<a name="6.5.6p8" …>` 锚点之后到下一个 `<p>`/`<a name=` 之间的文本，
去标签、压空白 ⇒ 原文一句。找不到锚点时回退到**特征短语**检索（仍要求命中才记录）。

CLI：`--check` 只读自检（不联网）· `--fetch` 抓 + 抽 + 写报告 · `--json`。纯标准库。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

OUT_MD = os.path.join(ROOT, "data", "648_c_standard.md")
OUT_JSON = os.path.join(ROOT, "data", "648_c_standard.json")
#: 下载缓存（build/ 被 .gitignore 忽略 ⇒ 不入库，只留 sha256）
CACHE = os.path.join(ROOT, "build", "c_std_648")

SOURCES: dict[str, dict[str, str]] = {
    "C11": {"doc": "N1570", "url": "https://port70.net/~nsz/c/c11/n1570.html",
            "kind": "html", "iso": "ISO/IEC 9899:2011"},
    "C17": {"doc": "N2310", "url": "https://www.open-std.org/jtc1/sc22/wg14/www/docs/n2310.pdf",
            "kind": "pdf", "iso": "ISO/IEC 9899:2018"},
    "C23": {"doc": "N3096", "url": "https://www.open-std.org/jtc1/sc22/wg14/www/docs/n3096.pdf",
            "kind": "pdf", "iso": "ISO/IEC 9899:2024"},
}

#: 648 十张卡要引的条款（anchor = N1570 的 `X.Y.ZpN` 锚点；phrase = 找不到锚点时的回退特征串）
CLAUSE_SPECS: list[dict[str, str]] = [
    {"key": "decay", "anchor": "6.7.6.3p7", "topic": "数组形参退化为指针",
     "phrase": "shall be adjusted to"},
    {"key": "malloc", "anchor": "7.22.3.3p2", "topic": "free(NULL) 是空操作；free 不清空指针",
     "phrase": "If ptr is a null pointer, no action occurs"},
    {"key": "strbound", "anchor": "7.21.6.5p3", "topic": "snprintf 返回值是'本该写入的长度'",
     "phrase": "would have been written had n been sufficiently large"},
    {"key": "fnptr", "anchor": "6.5.2.2p9", "topic": "经不兼容函数指针调用 ⇒ UB",
     "phrase": "the behavior is undefined"},
    {"key": "volatile", "anchor": "6.7.3p7", "topic": "volatile：什么算一次访问是实现定义",
     "phrase": "What constitutes an access to an object that has volatile-qualified type"},
    {"key": "setjmp", "anchor": "7.13.2.1p3", "topic": "longjmp 后非 volatile 局部变量值不确定",
     "phrase": "are indeterminate"},
    {"key": "intpromo", "anchor": "6.3.1.8p1", "topic": "常用算术转换：有符号/无符号比较",
     "phrase": "the operand with unsigned integer type is converted"},
    {"key": "bitfield", "anchor": "6.7.2.1p11", "topic": "位域分配顺序/对齐是实现定义",
     "phrase": "is implementation-defined"},
    {"key": "macro", "anchor": "6.10.3.1p1", "topic": "宏实参先展开再替换（故括号与副作用由使用者负责）",
     "phrase": "argument substitution takes place"},
    {"key": "signedovf", "anchor": "6.5p5", "topic": "表达式结果超出可表示范围 ⇒ UB",
     "phrase": "the behavior is undefined"},
]


def _download(url: str, timeout: int = 90) -> bytes:
    """真实下载（本批唯一的联网动作；失败即抛，不静默降级）。"""
    req = urllib.request.Request(url, headers={"User-Agent": "queyi-cppbible/648"})
    with urllib.request.urlopen(req, timeout=timeout) as r:  # noqa: S310 - 固定白名单 URL
        return r.read()


def _strip_tags(s: str, drop_leading_para_no: bool = False) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    if drop_leading_para_no:            # 段首的 `<small>8</small>` 段号不是标准正文
        s = re.sub(r"^\s*\d+\s+", "", s)
    s = (s.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<")
         .replace("&gt;", ">").replace("&#8722;", "-").replace("&minus;", "-"))
    return re.sub(r"\s+", " ", s).strip()


def extract_clause(html: str, anchor: str, phrase: str, maxlen: int = 700) -> dict[str, Any]:
    """按 `X.Y.ZpN` 锚点取原文；锚点缺失时回退特征短语。命中即给字节偏移供人复核。"""
    m = re.search(r'<a\s+name="%s"' % re.escape(anchor), html)
    if m:
        # 锚点标签形如 `<a name="6.5.6p8" href="#6.5.6p8"><small>8</small></a>`：
        # ① 先跳到该标签的 `>` 之后（否则 `href="#…">` 会被当成正文）
        gt = html.find(">", m.end())
        start = (gt + 1) if gt != -1 else m.end()
        nxt = re.search(r'<p>|<a\s+name="', html[start:])
        raw = html[start:start + (nxt.start() if nxt else maxlen * 3)]
        # ② 再去标签并丢掉段号（`<small>8</small>` ⇒ "8"）
        text = _strip_tags(raw, drop_leading_para_no=True)
        return {"found": True, "via": "anchor", "anchor": anchor, "offset": m.start(),
                "quote": text[:maxlen]}
    if phrase and phrase in html:
        i = html.find(phrase)
        raw = html[max(0, i - 400):i + 400]
        return {"found": True, "via": "phrase", "anchor": anchor, "offset": i,
                "quote": _strip_tags(raw)[:maxlen]}
    return {"found": False, "via": None, "anchor": anchor, "offset": -1, "quote": ""}


def run_fetch(timeout: int = 90) -> dict[str, Any]:
    os.makedirs(CACHE, exist_ok=True)
    out: dict[str, Any] = {"docs": {}, "clauses": {}, "limitations": []}
    for tag, spec in SOURCES.items():
        try:
            data = _download(spec["url"], timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            out["docs"][tag] = {"doc": spec["doc"], "url": spec["url"], "ok": False,
                                "error": f"{type(exc).__name__}: {exc}"}
            continue
        path = os.path.join(CACHE, f"{spec['doc']}.{spec['kind']}")
        with open(path, "wb") as fh:
            fh.write(data)
        rec: dict[str, Any] = {"doc": spec["doc"], "iso": spec["iso"], "url": spec["url"],
                               "kind": spec["kind"], "ok": True, "bytes": len(data),
                               "sha256": hashlib.sha256(data).hexdigest(),
                               "cache": os.path.relpath(path, ROOT).replace("\\", "/")}
        out["docs"][tag] = rec
        if spec["kind"] == "html":
            html = data.decode("utf-8", errors="replace")
            for cs in CLAUSE_SPECS:
                got = extract_clause(html, cs["anchor"], cs["phrase"])
                got["topic"] = cs["topic"]
                got["doc"] = spec["doc"]
                got["iso"] = spec["iso"]
                got["url"] = f"{spec['url']}#{cs['anchor']}"
                out["clauses"][cs["key"]] = got
        else:
            out["limitations"].append(
                f"{tag}（{spec['doc']}）是 PDF，本环境无 PDF 解析库 ⇒ 只留下载留痕"
                f"（bytes={len(data)}、sha256={rec['sha256'][:16]}…），**未抽取原文、未核对条款号**。"
                f"人核命令：用任意 PDF 阅读器打开 {spec['url']} 并检索 C11 对应条款号。")
    out["n_clauses"] = len(out["clauses"])
    out["n_found"] = sum(1 for c in out["clauses"].values() if c["found"])
    return out


def write_report(res: dict[str, Any]) -> str:
    lines = ["# 648 · C 标准原文抓取（C11/C17/C23）", "",
             "| 标准 | 文档 | ISO | 形式 | 下载 | 字节 | sha256（前 16） |", "|---|---|---|---|---|---|---|"]
    for tag, d in res["docs"].items():
        if d.get("ok"):
            lines.append(f"| {tag} | {d['doc']} | {d['iso']} | {d['kind']} | ✅ | {d['bytes']} | "
                         f"`{d['sha256'][:16]}…` |")
        else:
            lines.append(f"| {tag} | {d['doc']} | — | — | ❌ {d.get('error','')} | — | — |")
    lines += ["", "## 抽取到的条款（**逐字来自 N1570**，带字节偏移可复核）", "",
              "| 卡 | 条款 | 主题 | 命中方式 | 偏移 | 原文（截断） |", "|---|---|---|---|---|---|"]
    for k, c in res["clauses"].items():
        q = c["quote"].replace("|", "\\|")[:180]
        lines.append(f"| {k} | {c['anchor']} | {c['topic']} | {c['via'] or '❌未命中'} | "
                     f"{c['offset']} | {q or '—'} |")
    lines += ["", f"**命中 {res['n_found']}/{res['n_clauses']}**。", "",
              "## 诚实登记", ""]
    for lim in res.get("limitations", []):
        lines.append(f"- {lim}")
    lines += ["- 卡的 `sources[]` 只写**能机器核对的** N1570（C11）条款；C17 与 C23 "
              "**不写条款号**（本批未核对），只登记在 `claim_boundary.standard` 的实测范围里。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2, sort_keys=True)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("三个标准源都有 URL", len(SOURCES) == 3)
    chk("十张卡各有一条条款规格", len(CLAUSE_SPECS) == 10)
    chk("条款 key 不重复",
        len({c["key"] for c in CLAUSE_SPECS}) == len(CLAUSE_SPECS))
    # 抽取逻辑自检（合成 HTML，不联网）
    html = ('<p>before</p>\n<p><a name="6.5.6p8" href="#6.5.6p8"><small>8</small></a>\n'
            ' When an expression that has integer type is added to a pointer, the result has\n'
            ' the type of the pointer operand.\n<p><a name="6.5.6p9" href="#6.5.6p9"><small>9</small></a>\n next')
    got = extract_clause(html, "6.5.6p8", "")
    chk("锚点抽取命中", got["found"] and got["via"] == "anchor")
    chk("抽取含条款正文", "pointer operand" in got["quote"])
    chk("不跨到下一段", "next" not in got["quote"])
    got2 = extract_clause(html, "9.9.9p1", "pointer operand")
    chk("锚点缺失时回退短语", got2["found"] and got2["via"] == "phrase")
    got3 = extract_clause(html, "9.9.9p1", "__不存在的串__")
    chk("都没有时如实报未命中", got3["found"] is False and got3["quote"] == "")
    chk("去标签", "<" not in _strip_tags("<b>a</b> &amp; b"))
    print(f"c-standard-fetch selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="648 C 标准原文抓取")
    ap.add_argument("--check", action="store_true", help="只读自检（不联网）")
    ap.add_argument("--fetch", action="store_true", help="抓取 + 抽取 + 写报告")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.fetch:
        res = run_fetch()
        print(f"written {write_report(res)}")
        print(f"[648 c-standard] 命中 {res['n_found']}/{res['n_clauses']}；"
              f"下载 {sum(1 for d in res['docs'].values() if d.get('ok'))}/3")
        return 0 if res["n_found"] == res["n_clauses"] else 1
    if a.json:
        if os.path.isfile(OUT_JSON):
            print(open(OUT_JSON, encoding="utf-8").read())
            return 0
        print("尚无 648_c_standard.json（先跑 --fetch）")
        return 1
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
