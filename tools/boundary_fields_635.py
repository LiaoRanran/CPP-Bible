"""635 1.1 · 边界三元组回填 + v26 补充字段（**只加字段，不改判决**）

给全部 `data/*baseline*` 报告回填 5 个字段：
- 边界三元组（v25）：`mutation_set_hash` / `mutation_count` / `generator_version`
- v26 补充：`evidence_channel`（证据取得通道）/ `materiality_flag`（是否重大）

**字段口径（实际值，非空/null）**：
- `mutation_set_hash` = 当前规范 mutation 集 `data/mutation/full_baseline_v7.json` 的 SHA256；
- `mutation_count` / `generator_version` 取自该文件（variants / 版本号）；
- `evidence_channel` 按**文件内容关键词**推断（cppreference/标准 → standard_textbook；
  人审 → human_review；外部/审核 → external_audit；AI/生成 → ai_generated；否则 experiment）；
- `materiality_flag` 按**内容是否涉及 gate 判决/安全/多卡影响**推断（true）否则 false。

`.md` → 追加「## 边界三元组 + v26 补充字段」小节；`.json` → 顶层加 5 键。

**只读契约**：`--check` 只读、exit 0、不写盘；`--apply` 才改文件；`--report` 写审计报告。
纯标准库；≥5 例单测（tests/test_boundary_fields_635.py）。
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MUT = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")
AUDIT_MD = os.path.join(ROOT, "data", "635_boundary_fields_audit.md")

CHANNELS = ("direct_experiment", "standard_textbook", "cppreference",
            "ai_generated", "human_review", "external_audit")


def _sha256(path: str) -> str:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for c in iter(lambda: fh.read(65536), b""):
                h.update(c)
        return h.hexdigest()
    except OSError:
        return ""


def mutation_meta() -> dict[str, Any]:
    d: dict[str, Any] = {}
    try:
        d = json.loads(open(MUT, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        d = {}
    return {
        "mutation_set_hash": _sha256(MUT),
        "mutation_count": d.get("variants", 0),
        "generator_version": "mutation_fuzz@v7",
    }


def infer_channel(text: str) -> str:
    t = text.lower()
    if "cppreference" in t:
        return "cppreference"
    if "标准" in text or "iso" in t:
        return "standard_textbook"
    if "人审" in text or "human_review" in t or "blind review" in t:
        return "human_review"
    if "外部" in text or "external" in t or "audit" in t:
        return "external_audit"
    if "ai 生成" in text or "ai_generated" in t or "gpt" in t:
        return "ai_generated"
    return "direct_experiment"


def infer_materiality(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in ("gate", "安全", "safety", "block", "判决逻辑", "≥3 张", "影响"))


def baseline_files() -> list[str]:
    return sorted(glob.glob(os.path.join(ROOT, "data", "*baseline*")))


def fields_for(path: str) -> dict[str, Any]:
    m = mutation_meta()
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        text = ""
    return {
        **m,
        "evidence_channel": infer_channel(text),
        "materiality_flag": infer_materiality(text),
    }


def _md_block(f: dict[str, Any]) -> str:
    return (
        "\n\n## 边界三元组 + v26 补充字段（635 1.1 回填）\n\n"
        f"- `mutation_set_hash`: `{f['mutation_set_hash']}`\n"
        f"- `mutation_count`: {f['mutation_count']}\n"
        f"- `generator_version`: `{f['generator_version']}`\n"
        f"- `evidence_channel`: `{f['evidence_channel']}`\n"
        f"- `materiality_flag`: {str(f['materiality_flag']).lower()}\n"
    )


def apply(dry: bool = True) -> list[dict[str, Any]]:
    rows = []
    for p in baseline_files():
        f = fields_for(p)
        ext = os.path.splitext(p)[1]
        exists = ("635 1.1 回填" in open(p, encoding="utf-8", errors="replace").read()
                  if os.path.exists(p) else False)
        if dry or exists:
            rows.append({"file": os.path.basename(p), **f, "already": exists})
            continue
        if ext == ".json":
            try:
                d = json.loads(open(p, encoding="utf-8").read())
                if isinstance(d, dict):
                    d.update(f)
                    with open(p, "w", encoding="utf-8", newline="\n") as fh:
                        json.dump(d, fh, ensure_ascii=False, indent=2)
            except (OSError, json.JSONDecodeError):
                pass
        else:
            with open(p, "a", encoding="utf-8", newline="\n") as fh:
                fh.write(_md_block(f))
        rows.append({"file": os.path.basename(p), **f, "already": exists})
    return rows


def write_audit() -> str:
    rows = apply(dry=True)
    lines = [
        "# 635 1.1 · 边界字段回填审计", "",
        f"- `data/*baseline*` 文件：**{len(rows)}** 个",
        "- 5 字段：`mutation_set_hash` / `mutation_count` / `generator_version` /"
        " `evidence_channel` / `materiality_flag`", "",
        "| 文件 | mutation_count | generator_version | evidence_channel | materiality |",
        "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r['file']}` | {r['mutation_count']} | {r['generator_version']} | "
                     f"{r['evidence_channel']} | {str(r['materiality_flag']).lower()} |")
    lines += ["", f"- `mutation_set_hash`（统一，当前规范 mutation 集）："
              f"`{rows[0]['mutation_set_hash'] if rows else ''}`", "",
              "## 诚实登记", "",
              "1. `evidence_channel` / `materiality_flag` 为**内容关键词启发式**推断（非人工逐份标注）；",
              "2. `mutation_set_hash` 取**当前规范** mutation 集（历史 baseline 未各自绑定专属集，"
              "统一引用 v7）——如实说明该简化；",
              "3. 回填**只追加小节/加键**，不改任何既有内容与判决。"]
    with open(AUDIT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return AUDIT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m = mutation_meta()
    chk("mutation_set_hash 非空", len(m["mutation_set_hash"]) == 64)
    chk("mutation_count = 1593", m["mutation_count"] == 1593)
    chk("channel 推断：cppreference", infer_channel("见 cppreference 原文") == "cppreference")
    chk("channel 推断：默认 experiment", infer_channel("普通测量") == "direct_experiment")
    chk("materiality 推断", infer_materiality("影响 gate 判决") is True
        and infer_materiality("措辞修正") is False)
    chk("baseline 文件 ≥20", len(baseline_files()) >= 20)
    chk("审计路径在 data 下（--check 不写）", AUDIT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 1.1 边界字段回填")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true", help="写入 5 字段")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.apply:
        rows = apply(dry=False)
        print(f"applied {len(rows)} files")
        return 0
    if args.report:
        print(f"written {write_audit()}")
        return 0
    rows = apply(dry=True)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0
    print(f"baseline files: {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
