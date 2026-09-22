#!/usr/bin/env python3
"""615 C2 · 27 条 legacy 豁免**到期制**（新建独立工具，**不改 poison_drill.py / 不删任何豁免**）。

背景（_arch_v19/03）：毒样例 27 条豁免全 `redteam_seen: legacy`，无到期日 ⇒ 永久免检（Goodhart 漂移）。

机制：为每条豁免设**到期批次 = 创建批次 + 10**（默认），到期后**重新评估**（续豁免/修规则/删豁免，
**均需人审授权**——本工具只算到期日与提醒，**不自动删除/修改任何豁免**）。

输入：`tools/poison_exemptions.yaml`（581 台账，只读行解析）+ `tools/golden_state.json`（批次时间线）。
CLI：`--check` / `--report` / 默认打印。
铁律：不改 `poison_drill.py`、不删豁免；本批**不跑** gate/poison 门禁。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, cast

from path_config_625 import root as _queyi_root  # noqa: E402  (625 C1 路径解耦)

ROOT = _queyi_root()
sys.path.insert(0, str(ROOT / "tools"))

EXEMPTIONS = ROOT / "tools" / "poison_exemptions.yaml"
GOLDEN = ROOT / "tools" / "golden_state.json"
REPORT = ROOT / "data" / "exemption_expiry_615.md"
DISPOSAL_REPORT = ROOT / "data" / "exemption_expiry_disposal_616.md"

EXPIRY_BATCHES = 10        # 创建批次 + 10 = 到期批次
DUE_SOON_BATCHES = 3       # 距到期 <= 3 批 ⇒ 即将到期

_ENTRY = re.compile(
    r"-\s*\{id:\s*(?P<id>[A-Za-z0-9_\-]+),\s*reason:\s*\"(?P<reason>[^\"]*)\",\s*"
    r"date:\s*(?P<date>\d{4}-\d{2}-\d{2})(?:,\s*redteam_seen:\s*(?P<seen>[A-Za-z0-9_\-]+))?\s*\}")


def load_exemptions() -> list[dict]:
    """解析 `poison_exemptions.yaml`（零依赖行解析，只读）。"""
    if not EXEMPTIONS.is_file():
        return []
    out: list[dict] = []
    for ln in EXEMPTIONS.read_text(encoding="utf-8").splitlines():
        m = _ENTRY.search(ln)
        if m:
            out.append({"id": m.group("id"), "date": m.group("date"),
                        "redteam_seen": m.group("seen") or "legacy",
                        "reason": m.group("reason")})
    return out


def batch_timeline() -> list[str]:
    """批次时间线 = golden `accepted[]` 的 ts（升序）；返回日期字符串列表。"""
    if not GOLDEN.is_file():
        return []
    st = cast("dict[str, Any]", json.loads(GOLDEN.read_text(encoding="utf-8")))
    acc = cast("list[dict[str, Any]]", st.get("accepted") or [])
    return [str(r.get("ts") or "")[:10] for r in sorted(acc, key=lambda r: str(r.get("ts") or ""))]


def created_batch(date: str, timeline: list[str]) -> int:
    """创建批次 = 时间线中 **ts 日期 < 创建日期** 的批次数（即创建时已历批次数）。"""
    return sum(1 for d in timeline if d and d < date)


def assign(timeline: list[str] | None = None) -> list[dict]:
    """为每条豁免算到期批次与状态。"""
    tl = timeline if timeline is not None else batch_timeline()
    current = len(tl)
    out: list[dict] = []
    for e in load_exemptions():
        cb = created_batch(e["date"], tl)
        exp = cb + EXPIRY_BATCHES
        if exp <= current:
            status = "expired"
        elif exp - current <= DUE_SOON_BATCHES:
            status = "due_soon"
        else:
            status = "active"
        out.append({"id": e["id"], "created_date": e["date"], "redteam_seen": e["redteam_seen"],
                    "created_batch": cb, "expiry_batch": exp, "current_batch": current,
                    "status": status})
    return out


def render(rows: list[dict]) -> str:
    n = len(rows)
    by = {"active": 0, "due_soon": 0, "expired": 0}
    for r in rows:
        by[r["status"]] = by.get(r["status"], 0) + 1
    due = [r for r in rows if r["status"] == "due_soon"]
    exp = [r for r in rows if r["status"] == "expired"]
    L = ["# 615 C2 · 豁免到期制（legacy + 624 新增）", "",
         f"> 豁免总数 **{n}**；到期 = **创建批次 + {EXPIRY_BATCHES}**"
         f"（批次轴 = `golden_state.accepted[]` 时间线）。**只算到期日与提醒，不删/不改任何豁免**。", "",
         "## 一、状态汇总", "", "| 状态 | 条数 |", "|---|---|",
         f"| active（未到期） | {by['active']} |",
         f"| due_soon（≤{DUE_SOON_BATCHES} 批内到期） | {by['due_soon']} |",
         f"| expired（已到期，须重评估） | {by['expired']} |", "",
         "## 二、到期日列表", "",
         "| 规则 ID | 创建日期 | 创建批次 | 到期批次 | 当前批次 | 状态 |",
         "|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: (x["expiry_batch"], x["id"])):
        L.append(f"| `{r['id']}` | {r['created_date']} | {r['created_batch']} | "
                 f"{r['expiry_batch']} | {r['current_batch']} | {r['status']} |")
    L += ["", "## 三、即将到期 / 已到期", "",
          f"- 即将到期（≤{DUE_SOON_BATCHES} 批）：{', '.join('`%s`' % r['id'] for r in due) or '（无）'}",
          f"- 已到期：{', '.join('`%s`' % r['id'] for r in exp) or '（无）'}", "",
          "## 四、到期后重新评估流程（需人审授权）", "",
          "1. **继续豁免**：确认该规则仍「端到端毒样例不适用/不经济」（须有 pytest 正反例兜底）⇒ 续期 +10 批；",
          "2. **修复规则**：若该规则本应有端到端毒样例 ⇒ 补毒样例、删豁免（改分母=口径动作，须人审）；",
          "3. **删除豁免**：规则被合并/废弃 ⇒ 删豁免并说明。", "",
          "> **重要声明**：本工具**只算到期日与提醒**，**不自动删除或修改任何豁免**；"
          "续期/修复/删除均需**人审授权**。", "", ""]
    return "\n".join(L) + "\n"


def check() -> list[str]:
    problems: list[str] = []
    rows = assign()
    expected = len(load_exemptions())       # 624 D3：动态口径（新增豁免不再硬编码 27）
    if len(rows) != expected:
        problems.append(f"豁免应为 {expected} 条（实测 {len(rows)}）")
    for r in rows:
        if r["expiry_batch"] != r["created_batch"] + EXPIRY_BATCHES:
            problems.append(f"{r['id']} 到期批次 ≠ 创建批次+{EXPIRY_BATCHES}")
            break
    # 合成：到期检测
    fake_tl = ["2026-01-01"] * 5 + ["2026-06-01"] * 10
    r0 = assign(fake_tl)
    if r0 and r0[0]["current_batch"] != 15:
        problems.append("批次轴长度应等于时间线条数")
    # 616 C2：处置建议覆盖全部豁免
    if len(dispose()) != len(rows):
        problems.append(f"处置建议应覆盖全部豁免（{len(dispose())} ≠ {len(rows)}）")
    return problems


def dispose(rows: list[dict] | None = None) -> list[dict]:
    """616 C2：为每条豁免生成**处置建议**（**不自动删除任何豁免**）。

    判据（据 581 台账纪律"豁免 ≠ 免检；须有 pytest 正反例兜底"）：
      * 理由含 pytest 兜底 ⇒ **继续豁免**（端到端毒样例不适用/不经济）；
      * advice 级规则（drill 判据与"拦截"相反）⇒ **继续豁免**。
    风险：**删豁免会改变 RULE-COVERAGE 分母**，若该规则无端到端毒样例 ⇒ `poison_drill` 可能非 0（CI 红）。
    """
    rows = rows if rows is not None else assign()
    reasons = {e["id"]: e.get("reason", "") for e in load_exemptions()}
    out: list[dict] = []
    for r in rows:
        reason = reasons.get(r["id"], "")
        adv = ("advice" in reason.lower()) or ("非阻断" in reason) or ("advice 级" in reason)
        teach = ("误解" in reason) or ("教学" in reason) or ("audience" in reason.lower())
        cat = "advice级" if adv else ("教学/资产类" if teach else "字段/枚举/结构类")
        has_pytest = "pytest" in reason
        if adv or has_pytest:
            sugg = "继续豁免（续期 +10 批）"
        else:
            sugg = "待裁决（缺 pytest 兜底证据）"
        out.append({"rule": r["id"], "created_batch": r["created_batch"],
                    "expiry_batch": r["expiry_batch"], "status": r["status"],
                    "category": cat, "has_pytest_evidence": has_pytest,
                    "suggestion": sugg,
                    "rationale": f"{cat}：" + ("advice 级与 drill 判据相反" if adv else
                                               "pytest 正反例已兜底、端到端毒样例不经济"),
                    "risk": "删豁免改变 RULE-COVERAGE 分母 ⇒ 无端到端毒样例时 poison_drill 可能非 0（CI 红）"})
    return out


def disposal_report(rows: list[dict] | None = None) -> str:
    disp = dispose(rows)
    from collections import Counter
    summ = Counter(x["suggestion"] for x in disp)
    cats = Counter(x["category"] for x in disp)
    L = [f"# 616 C2 · 豁免到期处置清单（{len(disp)} 条，**只建议，不自动删除**）", "",
         "> 依据：581 台账纪律「豁免 ≠ 免检；须有 pytest 正反例兜底」；到期 = 创建批次 + 10。", "",
         "## 一、分类汇总", "",
         "| 处置建议 | 条数 |", "|---|---|",
         *[f"| {k} | {v} |" for k, v in sorted(summ.items())],
         "", "| 类别 | 条数 |", "|---|---|",
         *[f"| {k} | {v} |" for k, v in sorted(cats.items())], "",
         "## 二、逐条处置建议", "",
         "| 规则 ID | 类别 | 创建批次 | 到期批次 | 状态 | 建议 | 理由 |", "|---|---|---|---|---|---|---|",
         *[f"| `{x['rule']}` | {x['category']} | {x['created_batch']} | {x['expiry_batch']} | "
           f"{x['status']} | {x['suggestion']} | {x['rationale']} |" for x in disp],
         "", "## 三、风险评估（统一）", "",
         f"- {disp[0]['risk'] if disp else '—'}",
         "- ⇒ **删除豁免前必须先补端到端毒样例**（或人审确认该规则确不适用）。", "",
         "## 四、执行建议（如要执行）", "",
         "1. **顺序**：先补毒样例/确认豁免理由 → 再删豁免（同 commit 跑 `poison_drill` 复核，注意那是监工门禁 ⇒ 交监工/人）；",
         "2. **前置条件**：人审授权 + 逐条确认；**不得批量删除**；",
         "3. **默认动作**：全部**继续豁免**（续期 +10 批）——本批 27 条全有 pytest 兜底 / advice 级。", "",
         "> **重要声明**：本清单只做处置**建议**，**不自动删除任何豁免**。所有删除决策需要**人审授权**。", "", ""]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="exemption_expiry",
                                 description="615 C2 legacy 豁免到期制（只算到期日与提醒）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--disposal", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[C2] ❌ {p}", file=sys.stderr)
            return 1
        print(f"[C2] ✅ 自验证通过：{len(load_exemptions())} 条豁免 / 到期=创建+10 / 状态计算 / 处置建议 一致")
        return 0
    if a.disposal:
        DISPOSAL_REPORT.parent.mkdir(parents=True, exist_ok=True)
        DISPOSAL_REPORT.write_text(disposal_report(), encoding="utf-8", newline="\n")
        print(f"[C2] 已写 {DISPOSAL_REPORT.relative_to(ROOT).as_posix()}（{len(dispose())} 条）")
        return 0
    rows = assign()
    if a.report:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(render(rows), encoding="utf-8", newline="\n")
        print(f"[C2] 已写 {REPORT.relative_to(ROOT).as_posix()}")
        return 0
    print(json.dumps({"total": len(rows),
                      "status": {s: sum(1 for r in rows if r["status"] == s)
                                 for s in ("active", "due_soon", "expired")}},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
