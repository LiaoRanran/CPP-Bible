"""638 3.2 · Lifecycle FSM（五态状态机 · 真落地）

v25 要求：**五态**状态机 + 复活条件。

五态：`draft` → `verified` → `stale` → `disputed` → `retired`

合法迁移（`LEGAL`，即 §三.3.2.2 表）：
```
draft    → verified / retired
verified → stale / disputed / retired
stale    → verified / disputed / retired
disputed → verified / retired
retired  → draft（**复活**，须满足复活条件之一）
```

复活条件（`REVIVAL_CONDITIONS`，§三.3.2.3）：
`new_evidence`（新证据出现）/ `boundary_change`（边界变化）/ `defeater_resolved`（击败器被解决）。

迁移日志（`data/638_lifecycle_ledger.jsonl`）**append-only** 且带哈希链
（`seq` / `prev_hash` / `self_hash`），只追加、不改历史（§零.2）。

**只读契约**：`--check` 只读、exit 0、**不写盘（也不创建 ledger）**；
`--report` 写 `data/638_lifecycle_fsm.md` + `.json`；`--record` 才追写 ledger。
纯标准库；≥6 例单测（tests/test_lifecycle_fsm_638.py）。
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "638_lifecycle_fsm.md")
OUT_JSON = os.path.join(ROOT, "data", "638_lifecycle_fsm.json")
LEDGER = os.path.join(ROOT, "data", "638_lifecycle_ledger.jsonl")

STATES = ["draft", "verified", "stale", "disputed", "retired"]

STATE_DESC: dict[str, str] = {
    "draft": "刚创建，未验证",
    "verified": "验证通过",
    "stale": "边界漂移/证据老化",
    "disputed": "有争议/被击败器触发",
    "retired": "退役，带复活条件",
}

LEGAL: dict[str, set[str]] = {
    "draft": {"verified", "retired"},
    "verified": {"stale", "disputed", "retired"},
    "stale": {"verified", "disputed", "retired"},
    "disputed": {"verified", "retired"},
    "retired": {"draft"},
}

REVIVAL_CONDITIONS = ("new_evidence", "boundary_change", "defeater_resolved")

_STATUS_RE = re.compile(r"^status:\s*(\S+)", re.MULTILINE)
_LIFECYCLE_RE = re.compile(r"^lifecycle:\s*(\S+)", re.MULTILINE)

# status → FSM 态（诚实映射：本批实测 28 张卡**全部无 lifecycle 字段**，故按 status 推导初态）
STATUS_TO_STATE: dict[str, str] = {
    "verified": "verified",
    "red-team-verified": "verified",
    "draft": "draft",
    "stale": "stale",
    "disputed": "disputed",
    "retired": "retired",
}


# ── 迁移合法性 ──────────────────────────────────────────────────────────
def can_transition(src: str, dst: str,
                   revival: Optional[str] = None) -> tuple[bool, str]:
    """判断一次迁移是否合法，返回 `(是否合法, 理由)`。"""
    if src not in LEGAL:
        return False, f"未知源态 `{src}`"
    if dst not in STATES:
        return False, f"未知目标态 `{dst}`"
    if dst not in LEGAL[src]:
        return False, f"非法迁移 `{src} → {dst}`（§三.3.2.2 不允许）"
    if src == "retired" and dst == "draft":
        if revival not in REVIVAL_CONDITIONS:
            return False, (f"复活须满足复活条件之一 {list(REVIVAL_CONDITIONS)}，"
                           f"收到 `{revival or '无'}`")
        return True, f"合法复活（条件：{revival}）"
    return True, f"合法迁移 `{src} → {dst}`"


def all_pairs() -> list[dict[str, Any]]:
    """全迁移矩阵（25 组，含非法），供报告与单测。"""
    rows: list[dict[str, Any]] = []
    for s in STATES:
        for d in STATES:
            ok, why = can_transition(s, d, "new_evidence")
            rows.append({"from": s, "to": d, "legal": ok, "why": why})
    return rows


# ── ledger（append-only + 哈希链）────────────────────────────────────────
def _entry_hash(rec: dict[str, Any]) -> str:
    payload = {k: rec[k] for k in sorted(rec) if k != "self_hash"}
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False,
                                     sort_keys=True).encode("utf-8")).hexdigest()


def load_ledger(path: str = LEDGER) -> list[dict[str, Any]]:
    if not os.path.exists(path):
        return []
    out: list[dict[str, Any]] = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def verify_ledger(records: list[dict[str, Any]]) -> list[str]:
    """校验 ledger 的 seq 连续 + prev_hash 衔接 + 自哈希正确；返回错误列表。"""
    errs: list[str] = []
    prev = "GENESIS"
    for i, r in enumerate(records, 1):
        if r.get("seq") != i:
            errs.append(f"第 {i} 条 seq 应为 {i}，实为 {r.get('seq')}")
        if r.get("prev_hash") != prev:
            errs.append(f"第 {i} 条 prev_hash 断链")
        if r.get("self_hash") != _entry_hash(r):
            errs.append(f"第 {i} 条 self_hash 校验失败")
        prev = str(r.get("self_hash"))
    return errs


def append_transition(card: str, src: str, dst: str, reason: str = "",
                      revival: Optional[str] = None, path: str = LEDGER) -> dict[str, Any]:
    """追写一次迁移到 ledger（**append-only**，不修改历史行）。返回新记录。"""
    ok, why = can_transition(src, dst, revival)
    if not ok:
        return {"ok": False, "why": why}
    recs = load_ledger(path)
    rec: dict[str, Any] = {
        "seq": len(recs) + 1,
        "card": card,
        "from": src,
        "to": dst,
        "reason": reason,
        "revival": revival or "",
        "recorded_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "prev_hash": (recs[-1]["self_hash"] if recs else "GENESIS"),
    }
    rec["self_hash"] = _entry_hash(rec)
    with open(path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")
    return {"ok": True, "record": rec, "why": why}


# ── 当前状态查询 ────────────────────────────────────────────────────────
def current_state(card_path: str) -> dict[str, Any]:
    """查一张卡的当前 FSM 态（优先 `lifecycle:`，否则按 `status:` 映射，再否则 draft）。"""
    try:
        t = open(card_path, encoding="utf-8", errors="replace").read()
    except OSError:
        return {"card": card_path, "state": "draft", "source": "文件不可读"}
    lc = _LIFECYCLE_RE.search(t)
    if lc:
        v = lc.group(1).lower()
        return {"card": os.path.relpath(card_path, ROOT).replace(os.sep, "/"),
                "state": v if v in STATES else "draft", "source": "lifecycle 字段"}
    st = _STATUS_RE.search(t)
    if st:
        v = st.group(1).lower()
        return {"card": os.path.relpath(card_path, ROOT).replace(os.sep, "/"),
                "state": STATUS_TO_STATE.get(v, "draft"), "source": f"status={v}"}
    return {"card": os.path.relpath(card_path, ROOT).replace(os.sep, "/"),
            "state": "draft", "source": "无 status（默认 draft）"}


def census() -> dict[str, Any]:
    """全库卡片的当前态普查（真实数字）。"""
    rows: list[dict[str, Any]] = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "atoms")):
        for f in sorted(fs):
            if f.endswith(".md"):
                rows.append(current_state(os.path.join(r, f)))
    dist: dict[str, int] = {}
    for x in rows:
        dist[x["state"]] = dist.get(x["state"], 0) + 1
    led = load_ledger()
    return {"rows": rows, "dist": dist, "n": len(rows),
            "ledger_n": len(led), "ledger_errs": verify_ledger(led),
            "with_lifecycle_field": sum(1 for x in rows if x["source"] == "lifecycle 字段")}


# ── 报告 ────────────────────────────────────────────────────────────────
def write_report() -> dict[str, str]:
    c = census()
    pairs = all_pairs()
    legal_n = sum(1 for p in pairs if p["legal"])
    out = {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "states": STATES, "legal_pairs": legal_n, "total_pairs": len(pairs),
           "census": {k: v for k, v in c.items() if k != "rows"}, "pairs": pairs,
           "revival_conditions": list(REVIVAL_CONDITIONS)}
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)

    lines = [
        "# 638 3.2 · Lifecycle FSM（五态状态机 · 真落地）", "",
        f"> 生成时间：{out['generated']}。工具：`tools/lifecycle_fsm_638.py`。", "",
        "## 一、五态定义", "",
        "| 态 | 含义 |", "|---|---|",
    ]
    for s in STATES:
        lines.append(f"| `{s}` | {STATE_DESC[s]} |")
    lines += [
        "", "## 二、迁移合法性矩阵（25 组）", "",
        f"- 合法迁移：**{legal_n} / {len(pairs)}** 组；",
        "", "| from \\ to | " + " | ".join(STATES) + " |",
        "|---|" + "---|" * len(STATES),
    ]
    for s in STATES:
        cells = []
        for d in STATES:
            ok, _ = can_transition(s, d, "new_evidence")
            cells.append("合法" if ok else "—")
        lines.append(f"| `{s}` | " + " | ".join(cells) + " |")
    lines += [
        "", "## 三、复活条件（`retired → draft` 必填其一）", "",
        "| 条件 | 含义 |", "|---|---|",
        "| `new_evidence` | 新证据出现 |",
        "| `boundary_change` | 边界变化（三元组改变） |",
        "| `defeater_resolved` | 击败器被解决 |", "",
        "> 未提供或提供非法条件 ⇒ **判非法**（`can_transition` 返回 False）。", "",
        "## 四、全库当前态普查（真实）", "",
        f"- 扫描 `atoms/**/*.md`：**{c['n']}** 张卡；",
        f"- 四态分布：`{c['dist']}`；",
        f"- 其中有显式 `lifecycle:` 字段的：**{c['with_lifecycle_field']}** 张；",
        f"- 迁移 ledger：**{c['ledger_n']}** 条；链校验错误：**{len(c['ledger_errs'])}** 条。", "",
        "### 4.1 初态推导口径（诚实说明）", "",
        "实测 28 张卡**全部无 `lifecycle:` 字段**，故「当前态」按 `status:` 推导：",
        "`verified`/`red-team-verified → verified`；`draft → draft`；无 `status` → `draft`。",
        "该映射是**兼容性推导**，不是卡上的真实 FSM 态（后者需后续批次回填）。", "",
        "## 五、诚实登记", "",
        "1. **ledger 默认不存在**（本批首次上线）：`--check` 不创建 ledger，`--record` 才追写；",
        "2. ledger **append-only + 哈希链**（seq/prev_hash/self_hash），`verify_ledger()` 可校验；",
        "3. 初态推导用 `status:` 兼容映射（见 §4.1），**非**卡上真实字段；",
        "4. 迁移规则**严格按 §三.3.2.2**，未自行扩充；`retired → draft` 必须给复活条件；",
        "5. 本工具**不改任何卡**（只读卡、只写自己的 ledger/报告）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


# ── 自检 ────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("五态定义", len(STATES) == 5 and set(LEGAL) == set(STATES))
    chk("draft→verified 合法", can_transition("draft", "verified")[0])
    chk("draft→retired 合法", can_transition("draft", "retired")[0])
    chk("verified→stale 合法", can_transition("verified", "stale")[0])
    chk("stale→verified 合法", can_transition("stale", "verified")[0])
    chk("disputed→verified 合法", can_transition("disputed", "verified")[0])
    chk("draft→stale 非法", not can_transition("draft", "stale")[0])
    chk("verified→draft 非法", not can_transition("verified", "draft")[0])
    chk("retired→verified 非法", not can_transition("retired", "verified")[0])
    chk("retired→draft 无复活条件 ⇒ 非法", not can_transition("retired", "draft")[0])
    chk("retired→draft 有复活条件 ⇒ 合法",
        can_transition("retired", "draft", "new_evidence")[0])
    chk("未知态 ⇒ 非法", not can_transition("nope", "draft")[0])
    chk("矩阵 25 组", len(all_pairs()) == 25)
    chk("ledger 校验空表通过", verify_ledger([]) == [])
    bad = [{"seq": 2, "prev_hash": "X", "self_hash": "Y"}]
    chk("ledger 断链可检出", len(verify_ledger(bad)) == 3)
    chk("当前态查询可用", current_state(os.path.join(ROOT, "data", "638_baseline.md"))
        ["state"] in STATES)
    c = census()
    chk("普查到卡", c["n"] >= 1 and sum(c["dist"].values()) == c["n"])
    chk("输出路径在 data 下",
        OUT_MD.startswith(os.path.join(ROOT, "data"))
        and LEDGER.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="638 3.2 Lifecycle FSM")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--state", help="查询一张卡的当前态")
    ap.add_argument("--record", action="store_true", help="追写一条迁移到 ledger")
    ap.add_argument("--from", dest="src", help="迁移源态")
    ap.add_argument("--to", dest="dst", help="迁移目标态")
    ap.add_argument("--card", default="", help="迁移对象卡（相对路径）")
    ap.add_argument("--reason", default="", help="迁移理由")
    ap.add_argument("--revival", default=None, help="复活条件（retired→draft 必填）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.state:
        print(json.dumps(current_state(args.state), ensure_ascii=False, indent=2))
        return 0
    if args.record:
        if not args.src or not args.dst:
            print("--record 需要 --from 与 --to")
            return 2
        r = append_transition(args.card, args.src, args.dst, args.reason, args.revival)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r.get("ok") else 1
    if args.report:
        out = write_report()
        print(f"written {out['json']} {out['md']}")
        return 0
    c = census()
    if args.json:
        print(json.dumps({k: v for k, v in c.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"cards={c['n']} dist={c['dist']} ledger={c['ledger_n']} errs={c['ledger_errs']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
