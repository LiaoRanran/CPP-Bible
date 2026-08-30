#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C++ 示例缺陷静态扫描 (深度审计 #201 工具)。

目标：对 Book/**/ch*.md 中所有 ```cpp 代码块做静态启发式审查，按缺陷类别
产出可定位的报告。核心约束：**不把「故意演示错误/UB」的教学示例误判为缺陷**。

意图分类：
  * intent_error  —— 教学性错误示例（前置 3 行 prose 或块内注释含 错误/UB/
    undefined/ill-formed/编译失败/反例/should not/won't compile 等标记），仅统计，
    不列缺陷。
  * intent_ok     —— 普通可教学示例，进入缺陷检查。

缺陷类别（高置信、低误报优先）：
  * unsafe_c          : gets/sprintf/strcpy/strcat/scanf("%s") 等不安全 C 函数 (SECURITY)
  * raw_new_no_delete : 块内出现 `new` 但无 `delete` (潜在泄漏, REVIEW)
  * reinterpret_cast  : reinterpret_cast 跨类型别名 (潜在 UB, REVIEW)
  * missing_virtual_dtor : 含虚函数但析构非 virtual (REVIEW)
  * using_namespace_std  : 全局 `using namespace std;` (名称污染, STYLE)
  * endl_flush        : std::endl 频繁 flush (PERF, INFO)

输出：tools/audit_cpp_defects.json + 汇总打印。
用法：python tools/audit_cpp_defects.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BOOK = REPO / "Book"
OUT = REPO / "tools" / "audit_cpp_defects.json"

FENCE_RE = re.compile(r"^```(cpp|c\+\+)\s*(.*)$", re.MULTILINE)
END_RE = re.compile(r"^```\s*$", re.MULTILINE)

ERROR_MARKERS = re.compile(
    r"(错误|UB|undefined\s*behavior|ill[- ]?formed|编译失败|无法编译|反例|错误示范|"
    r"should\s+not|shouldn't|won't\s+compile|does\s+not\s+compile|this\s+is\s+(wrong|bad)|"
    r"bug|缺陷|未定义|悬垂|泄漏|越界)",
    re.IGNORECASE,
)
IN_BLOCK_ERROR = re.compile(r"//\s*(错误|UB|undefined|ill-formed|反例|bad|wrong)|/\*\s*(错误|UB|bad|wrong)")

UNSAFE_C = [
    (re.compile(r"\bgets\s*\("), "gets() 已被 C11 废除，无条件读入可缓冲区溢出"),
    (re.compile(r"\bsprintf\s*\("), "sprintf 不检查目标缓冲区长度，易溢出；改用 snprintf"),
    (re.compile(r"\bstrcpy\s*\("), "strcpy 不检查目标长度，易溢出；改用 strncpy/std::string"),
    (re.compile(r"\bstrcat\s*\("), "strcat 不检查目标长度，易溢出"),
    (re.compile(r'\bscanf\s*\(\s*"[^"]*%s'), 'scanf("%s") 无宽度限制，缓冲区溢出；改用 %Ns 或 std::string'),
    (re.compile(r"\bsystem\s*\("), "system() 执行 shell，存在命令注入与可移植性风险"),
]

RE_NEW = re.compile(r"\bnew\s+(?:[\w:]+|void)")
RE_DELETE = re.compile(r"\bdelete\s*(?:\[\s*|\b)")
RE_REINTERPRET = re.compile(r"reinterpret_cast\s*<")
RE_VIRTUAL_METHOD = re.compile(r"\bvirtual\s+(?:[\w:~<>\s*,]+?)\s*\(")
RE_CLASS = re.compile(r"\bclass\s+(\w+)")
RE_DTOR = re.compile(r"~(\w+)\s*\(")
RE_VIRTUAL_DTOR = re.compile(r"\bvirtual\s+~\w+\s*\(")
RE_USING_NS = re.compile(r"using\s+namespace\s+std\s*;")
RE_ENDL = re.compile(r"(std::endl|<<\s*endl)")


def extract_blocks(path: Path):
    """返回 [(line_no, code, preceding_prose_lines), ...]。"""
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        m = FENCE_RE.match(lines[i])
        if m:
            start = i + 1
            j = start
            while j < n and not END_RE.match(lines[j]):
                j += 1
            code = "\n".join(lines[start:j])
            pre = "\n".join(lines[max(0, i - 3):i])
            out.append((i + 1, code, pre))
            i = j + 1
        else:
            i += 1
    return out


def is_intent_error(code: str, pre: str) -> bool:
    if IN_BLOCK_ERROR.search(code):
        return True
    if ERROR_MARKERS.search(pre):
        return True
    return False


def check_virtual_dtor(code: str):
    findings = []
    for cm in RE_CLASS.finditer(code):
        cls = cm.group(1)
        # 类体范围：从 class 到下一个顶层 '};' 近似——这里仅在块内做存在性判断
        has_virtual = RE_VIRTUAL_METHOD.search(code) is not None
        dtor_m = RE_DTOR.search(code)
        has_virtual_dtor = RE_VIRTUAL_DTOR.search(code) is not None
        if has_virtual and dtor_m and not has_virtual_dtor:
            findings.append(f"class {cls}: 含虚函数但析构非 virtual（基类应 virtual ~{cls}()）")
    return findings


def main() -> int:
    files = sorted(BOOK.rglob("ch*.md"))
    if not files:
        print(f"ERROR: 未在 {BOOK} 找到章节文件", file=sys.stderr)
        return 2

    total = 0
    intent_error = 0
    cats = {
        "unsafe_c": [],
        "raw_new_no_delete": [],
        "reinterpret_cast": [],
        "missing_virtual_dtor": [],
        "using_namespace_std": [],
        "endl_flush": [],
    }
    by_part = {}

    for f in files:
        part = f.parent.name
        blocks = extract_blocks(f)
        for (ln, code, pre) in blocks:
            total += 1
            by_part.setdefault(part, {"blocks": 0, "intent_error": 0})
            by_part[part]["blocks"] += 1
            if is_intent_error(code, pre):
                intent_error += 1
                by_part[part]["intent_error"] += 1
                continue
            rel = f.relative_to(REPO).as_posix()
            # unsafe_c
            for rx, note in UNSAFE_C:
                if rx.search(code):
                    cats["unsafe_c"].append({"file": rel, "line": ln, "note": note})
                    break
            # raw new without delete
            if RE_NEW.search(code) and not RE_DELETE.search(code):
                cats["raw_new_no_delete"].append(
                    {"file": rel, "line": ln, "note": "块内出现 new 但无对应 delete（片段可能省略释放，需确认是否为教学意图）"}
                )
            # reinterpret_cast
            if RE_REINTERPRET.search(code):
                cats["reinterpret_cast"].append(
                    {"file": rel, "line": ln, "note": "reinterpret_cast 跨无关类型可能触发严格别名 UB"}
                )
            # virtual dtor
            for vd in check_virtual_dtor(code):
                cats["missing_virtual_dtor"].append({"file": rel, "line": ln, "note": vd})
            # using namespace std
            if RE_USING_NS.search(code):
                cats["using_namespace_std"].append(
                    {"file": rel, "line": ln, "note": "全局 using namespace std; 污染命名空间，头文件中尤应避免"}
                )
            # endl
            if RE_ENDL.search(code):
                cats["endl_flush"].append(
                    {"file": rel, "line": ln, "note": "std::endl 强制 flush，循环内使用应改 '\\n'"}
                )

    summary = {k: len(v) for k, v in cats.items()}
    OUT.write_text(
        json.dumps(
            {"total_blocks": total, "intent_error_blocks": intent_error,
             "by_part": by_part, "categories": cats, "summary": summary},
            ensure_ascii=False, indent=2,
        ),
        encoding="utf-8",
    )
    print(f"总 cpp 块={total}  教学性错误示例(已排除)={intent_error}")
    print("缺陷类别计数:")
    for k, v in summary.items():
        print(f"  {k:22s} {v}")
    print("\n按 part 统计块数:")
    for part, d in sorted(by_part.items()):
        print(f"  {part:22s} blocks={d['blocks']:4d} intent_error={d['intent_error']}")
    print(f"\n报告已写入 {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
