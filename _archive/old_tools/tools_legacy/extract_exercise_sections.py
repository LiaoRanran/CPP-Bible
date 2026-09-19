#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_exercise_sections.py — 抽取全书各章习题/面试题/思考题区块

为 A-priority 「习题主题匹配度」审计提供结构化输入。输出 JSON：
- chapter: 文件路径
- title: 章标题（# 第N章 ...）
- body_summary: 正文摘要（首 1200 字符 + 所有 ## 小标题）
- exercise_sections: 命中 ⑮/⑳/面试题/练习题/思考题 的节列表

用法：python3 tools/extract_exercise_sections.py
输出：build/exercise_sections.json
"""
import json
import pathlib
import re

ROOT = pathlib.Path("Book")
OUT = pathlib.Path("build/exercise_sections.json")

# 命中习题/面试/思考类区块的标题正则
# 1) ⑮/⑳ 等带"题/练习/思考/FAQ"的节
# 2) 附录 X：...面试/习题/练习/工业与面试...
# 3) 自测练习（Exercises）
EXERCISE_RE = re.compile(
    r"^##\s*(?:"
    r"([⑮⑯⑰⑱⑲⑳]\s*)?.*?(?:面试题|练习题|思考题|应用题|习题|源码阅读路线|FAQ)"
    r"|附录\s+[A-Z]：.*?(?:面试|习题|练习|工业与面试)"
    r"|自测练习(?:（Exercises）)?"
    r")$",
    re.MULTILINE,
)
H2_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def extract(file: pathlib.Path) -> dict:
    text = file.read_text(encoding="utf-8", errors="ignore")
    title_m = TITLE_RE.search(text)
    title = title_m.group(1).strip() if title_m else file.stem

    # 正文摘要：标题后到第一个 ## ⑮/⑯... 之前的片段，截断到 1200 字符
    body_start = title_m.end() if title_m else 0
    first_ex = EXERCISE_RE.search(text)
    body_end = first_ex.start() if first_ex else body_start + 1200
    body_summary = text[body_start:body_end].strip()[:1200]

    # 收集所有二级标题作为主题骨架
    h2s = [m.group(1).strip() for m in H2_RE.finditer(text)]

    # 抽取习题类节：从标题到下一个同级或更高级标题
    sections = []
    for m in EXERCISE_RE.finditer(text):
        sec_title = m.group(0).replace("##", "").strip()
        start = m.end()
        # 下一个以 ## 或 # 开头的行
        nxt = re.search(r"\n(?=##\s|#\s)", text[start:])
        end = start + nxt.start() if nxt else len(text)
        sec_text = text[start:end].strip()
        sections.append({
            "section_title": sec_title,
            "offset": m.start(),
            "text": sec_text[:2500],  # 截断，防超大节
        })

    return {
        "chapter": str(file).replace("\\", "/"),
        "title": title,
        "body_summary": body_summary,
        "h2_titles": h2s,
        "exercise_sections": sections,
    }


def main():
    files = sorted(
        f for f in ROOT.rglob("ch*.md")
        if "_legacy_" not in str(f) and f.name.startswith("ch")
    )
    data = [extract(f) for f in files]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[*] 抽取 {len(data)} 章习题/面试题区块 → {OUT}")
    print(f"[*] 含至少一个 exercise 节的章数: {sum(1 for d in data if d['exercise_sections'])}")


if __name__ == "__main__":
    main()
