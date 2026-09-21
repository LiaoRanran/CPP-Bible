#!/usr/bin/env python3
"""615 A1 · 人审诚实化标签（**只读** annotations，新建独立标签文件，绝不修改原记录）。

背景（_arch_v19 调研 `05_人审即内容.md`）：388 条"全量人审"实为 **1 名审阅者、5 个理由模板**的
**批量授权**——镜像边（对称边）194、抽样外推 177、**逐条独立判断 0**。本工具把每条的真实
**审核方式**打标，供 W2/报告诚实区分「独立票 / 镜像票 / 授权票」。

分类规则（可复算）：
  * `is_mirror`：理由含「对称边」（命题→MIS 对称推断，一次判断算两条）。
  * `template_match`：匹配 5 个理由模板之一（T1..T5），非模板 ⇒ null。
  * `review_method`：`item_by_item`（非模板 ∧ 非镜像 ∧ 理由>50 字符，独立判断）
    / `batch_authorization`（其余）。
  * `batch_group_id`：批量授权按模板分组（`BATCH-T1`..），逐条判断为 null。

产物：`data/human_review_honesty_labels.jsonl`（每行对应一条 annotations）+ `data/human_review_honesty_615.md`。

CLI：`--write`（写标签）/ `--report`（写报告）/ `--check`（自验证，exit 0=通过）。
铁律：**绝不修改** `data/human_attack_edge_annotations.jsonl`；不改受控目录。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

ANNOTATIONS = ROOT / "data" / "human_attack_edge_annotations.jsonl"
LABELS = ROOT / "data" / "human_review_honesty_labels.jsonl"
REPORT = ROOT / "data" / "human_review_honesty_615.md"

#: 原 annotations 的 sha256 基线（防误改的对照锚；由任务0 实测）
ANNOTATIONS_SHA256 = "027dff3aaaa6247f04541968b988fc90325363b75314b1c54fa8a9a346f9f3c4"

MIRROR_MARK = "对称边"
TEMPLATE_SIGNATURES = (
    ("T3", "AI预标注modify"),                 # 批量 adjust
    ("T2", "抽样验证准确率100%(20/20)"),        # 抽样外推
    ("T1", "对称边"),                          # 镜像（approve）
)   # 依序匹配；未命中者再看 action 细分


def load_annotations() -> list[dict]:
    if not ANNOTATIONS.is_file():
        return []
    out: list[dict] = []
    for line in ANNOTATIONS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(cast("dict[str, Any]", json.loads(line)))
    return out


def classify(rec: dict) -> dict:
    reason = str(rec.get("reason") or "")
    action = str(rec.get("action") or "")
    is_mirror = MIRROR_MARK in reason
    template: str | None = None
    for tid, sig in TEMPLATE_SIGNATURES:
        if sig in reason:
            template = tid
            break
    if template == "T1" and action == "modify":
        template = "T4"                          # 镜像边(modify)
    if template == "T2" and not is_mirror and "即授权批量通过" not in reason:
        template = "T5"                          # T2 的措辞变体（1 条）
    item_by_item = (template is None) and (not is_mirror) and (len(reason) > 50)
    return {
        "edge_id": rec.get("edge_id"),
        "review_method": "item_by_item" if item_by_item else "batch_authorization",
        "is_mirror": is_mirror,
        "batch_group_id": None if item_by_item else f"BATCH-{template or 'OTHER'}",
        "reason_length": len(reason),
        "template_match": template,
    }


def build() -> list[dict]:
    return [classify(r) for r in load_annotations()]


def write_labels(labels: list[dict]) -> int:
    LABELS.parent.mkdir(parents=True, exist_ok=True)
    with LABELS.open("w", encoding="utf-8", newline="\n") as fh:
        for x in labels:
            fh.write(json.dumps(x, ensure_ascii=False) + "\n")
    return len(labels)


def summarize(labels: list[dict]) -> dict:
    methods = Counter(x["review_method"] for x in labels)
    tmpl = Counter(x["template_match"] for x in labels)
    lens = sorted(x["reason_length"] for x in labels)
    hist: dict[str, int] = {}
    for L in lens:
        b = f"{(L // 10) * 10}-{(L // 10) * 10 + 9}"
        hist[b] = hist.get(b, 0) + 1
    return {
        "total": len(labels),
        "item_by_item": methods.get("item_by_item", 0),
        "batch_authorization": methods.get("batch_authorization", 0),
        "mirror": sum(1 for x in labels if x["is_mirror"]),
        "templates": dict(tmpl),
        "reason_len": {"min": lens[0] if lens else 0, "max": lens[-1] if lens else 0,
                       "median": lens[len(lens) // 2] if lens else 0},
        "hist": hist,
    }


def render(s: dict) -> str:
    return "\n".join([
        "# 615 A1 · 人审诚实化（388 条真实审核方式重述）", "",
        "> **只读** annotations；标签为独立文件，**不改**任何人审结果。", "",
        "## 一、诚实声明（核心）", "",
        f"- 388 条「人审」中，**{s['item_by_item']} 条为逐条独立判断**，"
        f"**{s['batch_authorization']} 条为批量授权**（非逐条复核）；",
        f"- 其中 **{s['mirror']} 条为镜像边**（命题↔MIS 对称推断，一次判断算两条，不提供独立信息）。",
        "- ⇒ 独立人类确认强度 = **0 条**（不含镜像票、不含抽样外推票）。", "",
        "## 二、审核方式对比", "",
        "| 方式 | 条数 |", "|---|---|",
        f"| 逐条独立判断 item_by_item | {s['item_by_item']} |",
        f"| 批量授权 batch_authorization | {s['batch_authorization']} |",
        f"| 其中镜像边 is_mirror | {s['mirror']} |", "",
        "## 三、模板化理由分布（5 模板）", "",
        "| 模板 | 条数 | 特征 |", "|---|---|---|",
        f"| T1 | {s['templates'].get('T1', 0)} | 镜像(approve) |",
        f"| T2 | {s['templates'].get('T2', 0)} | 抽样外推 |",
        f"| T3 | {s['templates'].get('T3', 0)} | 批量 adjust |",
        f"| T4 | {s['templates'].get('T4', 0)} | 镜像(modify) |",
        f"| T5 | {s['templates'].get('T5', 0)} | T2 变体 |", "",
        "## 四、理由长度分布", "",
        f"- min/max/median = {s['reason_len']['min']}/{s['reason_len']['max']}/{s['reason_len']['median']}",
        "", "| 区间(字符) | 条数 |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in sorted(s["hist"].items())],
        "", "## 五、边界", "",
        "- 原 `data/human_attack_edge_annotations.jsonl` **未被修改**（sha256 对照锚）。",
        "- 标签只描述「审核方式」，**不改变**任何 approve/modify 结论。", "",
    ]) + "\n"


def check() -> list[str]:
    problems: list[str] = []
    ann = load_annotations()
    labels = build()
    # 原文件未被修改
    if ANNOTATIONS.is_file():
        cur = hashlib.sha256(ANNOTATIONS.read_bytes()).hexdigest()
        if cur != ANNOTATIONS_SHA256:
            problems.append(f"annotations 已被修改（sha256 {cur[:16]}… ≠ 基线）")
    # 行数匹配 + edge_id 一一对应
    if len(labels) != len(ann):
        problems.append(f"标签行数 {len(labels)} ≠ annotations {len(ann)}")
    if [x["edge_id"] for x in labels] != [r.get("edge_id") for r in ann]:
        problems.append("edge_id 未与 annotations 一一对应")
    s = summarize(labels)
    # 统计闭环
    if s["mirror"] != 194:
        problems.append(f"镜像边应为 194（实测 {s['mirror']}）")
    if s["item_by_item"] != 0:
        problems.append(f"逐条独立判断应为 0（实测 {s['item_by_item']}）")
    if s["batch_authorization"] != len(ann):
        problems.append("批量授权数应等于 annotations 总数")
    for x in labels:
        if x["is_mirror"] and not str(x["batch_group_id"]).startswith("BATCH-"):
            problems.append("镜像边应属批量授权组")
            break
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="human_review_honesty_615",
                                 description="615 A1 人审诚实化标签（只读 annotations）")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    labels = build()
    s = summarize(labels)
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[A1] ❌ {p}", file=sys.stderr)
            return 1
        print(f"[A1] ✅ 自验证通过：388 标签 / edge_id 一一对应 / 镜像 {s['mirror']} / "
              f"逐条 {s['item_by_item']} / annotations 未改")
        return 0
    if a.write:
        n = write_labels(labels)
        print(f"[A1] 已写 {LABELS.relative_to(ROOT).as_posix()}（{n} 行）")
        return 0
    if a.report:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(render(s), encoding="utf-8", newline="\n")
        print(f"[A1] 已写 {REPORT.relative_to(ROOT).as_posix()}")
        return 0
    print(json.dumps(s, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
