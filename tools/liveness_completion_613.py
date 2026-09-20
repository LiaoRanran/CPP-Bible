#!/usr/bin/env python3
"""613 任务A2 · 活性锚批量补全（低成本部分）—— **只产出补丁集，不落卡**。

铁律：atoms/ 是受控目录，本批**不写入**。本工具计算「低成本 + 高置信」命题的**精确补全补丁**
（卡 / 命题 / 锚类型 / 锚符号），并用 612 B3 的 `liveness_impact.analyze()` 投影 warn 下降效果，
供人审裁决后授权落卡（交人项）。

补全标准（与 607 规则一致）：
    liveness:
      kind: fixture_symbol
      symbol: <证据卡工件中的真实符号>
  锚必须：① 真实存在于该命题引用证据卡的工件中；② 非 universal 通配符号；
  ③ 出现在 artifact_assert 目标内（否则 OBSERVATION-LIVENESS 仍 warn）。

只补 **cost=low** 档（class A，或 class B 且 confidence=high）——即 A1 排序的前 9 条。
medium/high 档留作人审，绝不自动补。

CLI：
  python tools/liveness_completion_613.py            # 生成 data/liveness_completed_613.md
  python tools/liveness_completion_613.py --json     # 同时输出机器可读补丁 data/liveness_patch_613.json
  python tools/liveness_completion_613.py --check    # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

OUT = ROOT / "data" / "liveness_completed_613.md"
JSON_OUT = ROOT / "data" / "liveness_patch_613.json"

# universal 通配符号（gate 判为无效锚）
UNIVERSAL = {"main", "_start", "__libc_start_main", "_ZSt", "operator"}
SYMBOL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_:]*$")


def load_low_cost() -> list[dict]:
    """取 A1 排序中 cost=low 的命题（class A，或 class B+high）。"""
    import liveness_priority_613 as a1  # noqa: E402
    return [r for r in a1.build() if r["cost"] == "low"]


def validate_anchor(row: dict) -> list[str]:
    """校验单条锚是否满足 OBSERVATION-LIVENESS 的锚要求（静态可判部分）。"""
    errs = []
    sym = (row.get("best_symbol") or "").strip()
    if not sym:
        errs.append("锚符号为空")
    elif not SYMBOL_RE.match(sym):
        errs.append(f"锚符号形态非法: {sym!r}")
    elif sym in UNIVERSAL or sym.startswith("_ZSt"):
        errs.append(f"锚符号是 universal 通配: {sym}")
    if row.get("best_kind") != "fixture_symbol":
        errs.append(f"锚类型应为 fixture_symbol，实测 {row.get('best_kind')!r}")
    if not row.get("source_file"):
        errs.append("缺来源证据卡")
    return errs


def patch_of(row: dict) -> dict:
    return {
        "proposition_id": row["proposition_id"],
        "card": row["card"],
        "card_path": row.get("path", ""),
        "claim_type": "observation",
        "liveness": {"kind": "fixture_symbol", "symbol": row["best_symbol"]},
        "anchor_source": row["source_file"],
        "class": row["class"],
        "confidence": row["confidence"],
        "priority": row["priority"],
    }


def yaml_fragment(p: dict) -> str:
    return (f"    liveness:\n"
            f"      kind: {p['liveness']['kind']}\n"
            f"      symbol: {p['liveness']['symbol']}")


def projection(n: int) -> dict:
    import liveness_impact as li  # noqa: E402
    return li.analyze(partial=n)


def render(patches: list[dict], errs: dict[str, list[str]], proj: dict, total: int) -> str:
    L = ["# 613 · 活性锚补全补丁集（A2）", "",
         f"> 生成：`python tools/liveness_completion_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         "> **状态：补丁已算出，尚未落卡**——atoms/ 为受控目录，落卡需人审授权（交人项）。",
         "> 只补 cost=low 档（class A / B+high）；medium/high 档留作人审。", "",
         "## 一、规模与投影", "",
         "| 项 | 值 |", "|---|---|",
         f"| 缺锚命题总数 | {total} |",
         f"| 本次低成本补全 | **{len(patches)}** |",
         f"| 投影 warn（前） | {proj['warn_before']} |",
         f"| 投影 warn（后） | **{proj['warn_after']}** |",
         f"| 剩余待补（medium/high） | {total - len(patches)} |", "",
         "## 二、补全补丁（精确锚点）", "",
         "| # | 命题 | 卡 | 锚类型 | 锚符号 | 来源证据卡 | 校验 |",
         "|---|---|---|---|---|---|---|"]
    for i, p in enumerate(patches, 1):
        ok = "✅" if not errs.get(p["proposition_id"]) else "❌ " + "；".join(errs[p["proposition_id"]])
        L.append(f"| {i} | `{p['proposition_id']}` | {p['card']} | {p['liveness']['kind']} "
                 f"| `{p['liveness']['symbol']}` | {p['anchor_source']} | {ok} |")
    L += ["", "## 三、待插入 YAML 片段（按命题）", ""]
    for p in patches:
        L += [f"### `{p['proposition_id']}`（{p['card']}）", "", "```yaml", yaml_fragment(p), "```", ""]
    L += ["> 落卡位置：对应原子卡 frontmatter 的 `claim_structured[]` 中该 proposition 条目下。",
          "> 落卡后 `OBSERVATION-LIVENESS` 该条不再 warn（规则要求 kind=fixture_symbol 且符号真实可断言）。",
          "", "## 四、未补部分（交人）", "",
          "- medium 档（class B + confidence=medium）：需人审复核锚符号后补。",
          "- high 档（class C，无候选锚）：建议改标 `inference` 或人工指定锚，需人审裁决。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 A2 · 活性锚低成本补全补丁集（不落卡）")
    ap.add_argument("--json", action="store_true", help="同时输出机器可读补丁")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    rows = load_low_cost()
    patches = [patch_of(r) for r in rows]
    errs = {r["proposition_id"]: validate_anchor(r) for r in rows}
    import liveness_priority_613 as a1  # noqa: E402
    total = len(a1.build())

    if a.check:
        bad = [f"{k}: {v}" for k, v in errs.items() if v]
        for b in bad:
            print(f"[A2] ✗ {b}")
        if len(patches) != 9:
            print(f"[A2] ✗ low 档应为 9 条，实测 {len(patches)}")
            bad.append("count")
        proj = projection(len(patches))
        if proj["warn_after"] != proj["warn_before"] - len(patches):
            print(f"[A2] ✗ 投影不一致：{proj}")
            bad.append("projection")
        print("[A2] " + ("✅ 自验证通过" if not bad else f"❌ {len(bad)} 项失败"))
        return 0 if not bad else 1

    proj = projection(len(patches))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(patches, errs, proj, total), encoding="utf-8", newline="\n")
    print(f"[A2] 写入 {OUT.relative_to(ROOT).as_posix()}（{len(patches)} 条补丁；"
          f"投影 warn {proj['warn_before']} ⇒ {proj['warn_after']}）")
    if a.json:
        JSON_OUT.write_text(json.dumps({"generated_at": datetime.now().isoformat(timespec="seconds"),
                                        "patches": patches, "projection": proj},
                                       ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[A2] 写入 {JSON_OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
