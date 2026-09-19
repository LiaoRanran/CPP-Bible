#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_exercise_theme_reports.py — 合并各 part 的习题主题匹配度审计报告

读取 build/exercise_theme_part*.json，输出统一 Markdown 报告：
build/exercise_theme_report.md

用法：python3 tools/merge_exercise_theme_reports.py
"""
import json
import pathlib

BUILD = pathlib.Path("build")
OUT_MD = BUILD / "exercise_theme_report.md"
OUT_JSON = BUILD / "exercise_theme_report.json"


def main():
    parts = sorted(BUILD.glob("exercise_theme_part*.json"))
    if not parts:
        print("[*] 未找到 build/exercise_theme_part*.json，跳过合并")
        return

    all_items = []
    for p in parts:
        items = json.loads(p.read_text(encoding="utf-8"))
        for it in items:
            it["_source"] = p.name
        all_items.extend(items)

    # 按章节路径排序
    all_items.sort(key=lambda x: x.get("chapter", ""))

    mismatch = [it for it in all_items if it.get("score") == "MISMATCH"]
    weak = [it for it in all_items if it.get("score") == "WEAK"]

    lines = [
        "# 习题/面试题主题匹配度审计报告",
        "",
        "- 生成时间：见文件修改时间",
        f"- 数据来源：{len(parts)} 个 part 报告",
        f"- 可疑章节总数：{len(all_items)}（MISMATCH {len(mismatch)} / WEAK {len(weak)}）",
        "",
        "## 严重跑题（MISMATCH）",
        "",
    ]
    if mismatch:
        for it in mismatch:
            lines.append(f"### {it['title']} — `{it['chapter']}`")
            lines.append(f"- **判定**：{it['score']}")
            lines.append(f"- **原因**：{it['reason']}")
            lines.append(f"- **可疑节**：{', '.join(it.get('suspicious_sections', []))}")
            for ex in it.get("suspicious_excerpts", []):
                lines.append(f"> {ex}")
            lines.append("")
    else:
        lines.append("未发现严重跑题章节。\n")

    lines.extend([
        "## 轻度偏离（WEAK）",
        "",
    ])
    if weak:
        for it in weak:
            lines.append(f"### {it['title']} — `{it['chapter']}`")
            lines.append(f"- **判定**：{it['score']}")
            lines.append(f"- **原因**：{it['reason']}")
            lines.append(f"- **可疑节**：{', '.join(it.get('suspicious_sections', []))}")
            for ex in it.get("suspicious_excerpts", []):
                lines.append(f"> {ex}")
            lines.append("")
    else:
        lines.append("未发现轻度偏离章节。\n")

    lines.extend([
        "## 原始 JSON 汇总",
        "",
        "合并后的机器可读数据见 `build/exercise_theme_report.json`。",
        "",
    ])

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    OUT_JSON.write_text(json.dumps(all_items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[*] 合并 {len(parts)} 个报告 → {OUT_MD} ({len(all_items)} 条可疑记录)")
    print(f"    MISMATCH: {len(mismatch)}, WEAK: {len(weak)}")


if __name__ == "__main__":
    main()
