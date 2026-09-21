#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 E2 · 人审待办清单生成工具（从 evidence 卡生成 30 条逐条复核清单）

- 扫描 evidence/ 下 EV-*.md（只读），取前 30（按路径排序）生成逐条复核 TODO。
- 每条：序号 / 证据卡 / 复核类型（默认"逐项语义审查"——填补 615 缺口）/ 状态 pending / 裁决选项 / 镜像边标记（按卡内容检测"镜像|mirror|对称边"）。
- 纯标准库；只读 evidence/，不改受控目录、不代签裁决。
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = os.path.join(ROOT, "evidence")


def collect_ev_cards(ev_dir=EVIDENCE, limit=30):
    base = os.path.dirname(ev_dir)
    cards = []
    for root, _dirs, files in os.walk(ev_dir):
        for f in files:
            if f.startswith("EV-") and f.endswith(".md"):
                rel = os.path.relpath(os.path.join(root, f), base).replace(os.sep, "/")
                cards.append(rel)
    return sorted(cards)[:limit]


def detect_mirror_edge(card_relpath, ev_dir=EVIDENCE):
    abs_p = os.path.join(os.path.dirname(ev_dir), card_relpath)
    try:
        with open(abs_p, encoding="utf-8", errors="ignore") as f:
            head = f.read(2000)
    except OSError:
        head = ""
    return bool(re.search(r"镜像|mirror|对称边|symmetric", head, re.IGNORECASE))


def build(limit=30, ev_dir=EVIDENCE):
    cards = collect_ev_cards(ev_dir, limit=limit)
    items = []
    for i, c in enumerate(cards, 1):
        items.append({
            "no": i,
            "card": c,
            "review_type": "逐项语义审查（填补 615 缺口：原 388 条中此项为 0）",
            "status": "pending",
            "decision_options": ["approve", "modify", "reject"],
            "mirror_edge": detect_mirror_edge(c, ev_dir),
        })
    return items


def render_markdown(items):
    L = []
    L.append("# 人审逐条复核待办清单（618 E2 · 30 条）\n")
    L.append("> 由 `tools/human_review_todo_generator_618.py` 从 evidence/ EV 卡生成（只读，前 30 张，按路径排序）。\n")
    L.append("> 615 诚实发现：原 388 条人审中**逐条独立语义审查 = 0**（仅 194 镜像边 + 354 批量授权）。本清单即补齐该缺口的 TODO。\n")
    L.append("> 本工具**只生成清单，不代签任何裁决**（approve/modify/reject 权唯人）。\n")
    L.append("\n| 序号 | 证据卡 | 复核类型 | 镜像边 | 状态 | 裁决选项 |")
    L.append("|---|---|---|---|---|---|")
    for it in items:
        L.append("| %d | `%s` | %s | %s | %s | %s |" % (
            it["no"], it["card"], it["review_type"],
            "是" if it["mirror_edge"] else "否", it["status"],
            "/".join(it["decision_options"])))
    L.append("\n## 使用说明\n")
    L.append("- 人工对每张卡执行“逐项语义审查”，在“状态/裁决”列填写结果（approve/modify/reject 并附理由）。")
    L.append("- 镜像边标记仅作提示（卡内容含“镜像/mirror/对称边”），不替代人工判定。")
    L.append("- 清单为 TODO 模板；最终裁决与统计由人审执行，本批不代签。")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="618 E2 人审待办清单生成")
    ap.add_argument("--evidence", default=EVIDENCE)
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "human_review_todo_30_618.md"))
    args = ap.parse_args()
    items = build(args.limit, args.evidence)
    txt = render_markdown(items)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(txt)
    print("generated %d items -> %s" % (len(items), args.out))


if __name__ == "__main__":
    main()
