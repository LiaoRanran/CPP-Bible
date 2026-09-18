#!/usr/bin/env python3
"""prop_asof.py — 只读「四轴快照」视图（583 任务 2 / 调研包 `_arch_v9/01` 的 N1）。

回答的问题：**每条命题——何时被断言、在哪个验证者版本下被判过、何时被谁推翻、引用锚在哪。**

四轴的**唯一来源**（不引入新账本，只把散装事实汇成视图）：
  ① 何时被断言  ← **近似**：卡的 git 提交时间 `git log -1 --format=%cI -- <card_path>`
                  ⇒ 字段名硬约束为 `asserted_at_approx_from_card_commit`（**不许**叫 asserted_at：
                  git 时间可被 rebase/amend 重写，属 **B 级证据**）
  ② 哪个验证者判过 ← 卡面可选字段 `verified_by_oracle`（与 `data/oracle_registry.json` 比对）
  ③ 何时被谁推翻   ← `data/overturned_events.jsonl`（**可缺**：缺 = 0 事件，不是错误——
                     本仓"系统绝不自动产生推翻"，无数据是设计上的常态）
  ④ 引用锚        ← `data/propositions.db` 的 `anchor_source` 列（card / evidence / none）

硬纪律（583 §任务 2）：
  * **只读**：本文件不含任何写调用（无 `open(...,'w')`/`write_text`/`mkdir`/`subprocess`）；
  * 与 `prop_graph.query()` 同源（sqlite `mode=ro`，派生库不存在时 **fail-loud**，不返回空表）；
  * `--json` 输出**逐字确定**（键排序、无时间戳），可两次跑比对；
  * git 不可用 ⇒ exit 2（不静默降级）；overturned 缺失 ⇒ 按 0 事件且**不报错**。

用法::

    python tools/prop_asof.py                 # 人读：表 + 三张清单
    python tools/prop_asof.py --json          # 机器读（stdout 直接 JSON）
    python tools/prop_asof.py --limit 5       # 只看前 5 条命题
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "data" / "propositions.db"
REGISTRY = ROOT / "data" / "oracle_registry.json"
OVERTURNED = ROOT / "data" / "overturned_events.jsonl"
VERSION = "v1.0"


def _die(msg: str, code: int = 2) -> None:
    print(f"[prop_asof] ❌ {msg}", file=sys.stderr)
    raise SystemExit(code)


def _git_commit_iso(path: Path) -> str:
    """卡的**最后提交时间**（ISO8601，B 级证据）。git 不可用/仓库外 ⇒ 抛错（fail-loud）。"""
    try:
        r = subprocess.run(["git", "log", "-1", "--format=%cI", "--", str(path)],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        raise RuntimeError(f"git 调用失败：{type(exc).__name__}: {exc}") from exc
    if r.returncode != 0:
        raise RuntimeError(f"git 返回 {r.returncode}：{(r.stderr or '').strip()[:120]}")
    return (r.stdout or "").strip() or "<untracked>"


def _load_registry() -> dict:
    if not REGISTRY.is_file():
        return {}
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8")) or {}
    except ValueError as exc:
        raise RuntimeError(f"registry 解析失败：{exc}") from exc


def _load_overturned() -> list[dict]:
    """推翻事件（可缺 ⇒ 0 条，**不报错**：无数据是设计常态）。坏行跳过但要计数。"""
    if not OVERTURNED.is_file():
        return []
    out: list[dict] = []
    for ln in OVERTURNED.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except ValueError:
            continue
    return out


def _props(db: Path) -> list[dict]:
    """只读读命题表（与 `prop_graph` 同 schema；库缺失即 fail-loud）。"""
    if not db.is_file():
        _die(f"命题库不存在：{db}（先跑 `python tools/prop_graph.py build`；本工具**不代建**）")
    con = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
    try:
        cols = [r[1] for r in con.execute("PRAGMA table_info(props)")]
        rows = con.execute(
            "SELECT prop_key, card, card_path, claim_type, anchor_source, signoff_state "
            "FROM props ORDER BY prop_key").fetchall()
    finally:
        con.close()
    need = {"prop_key", "card", "card_path", "anchor_source"}
    if not need.issubset(set(cols)):
        _die(f"命题库 schema 不含所需列（缺 {sorted(need - set(cols))}）——库版本过旧，先 rebuild")
    return [dict(zip(("prop_key", "card", "card_path", "claim_type",
                      "anchor_source", "signoff_state"), r)) for r in rows]


def _card_oracle(card_path: str) -> dict | None:
    """卡面 `verified_by_oracle`（读**卡文本**的 frontmatter；纯只读）。"""
    p = ROOT / card_path
    if not p.is_file():
        return None
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import atom_evidence_replay as replay
        meta = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    except (ValueError, OSError):
        return None
    vo = meta.get("verified_by_oracle")
    if not vo:
        return None
    if isinstance(vo, dict):
        return {"name": str(vo.get("oracle") or vo.get("name") or ""),
                "version": str(vo.get("version") or "")}
    return {"name": str(vo), "version": ""}


def _overturned_for(prop_key: str, card: str, events: list[dict]) -> list[dict]:
    """把推翻事件挂到命题上：`target` 命中 prop_key、或（无 prop 粒度时）命中卡 id。"""
    hit = []
    for e in events:
        tgt = str(e.get("target") or "")
        e_card = str(e.get("card") or "")
        if tgt in (prop_key, card) or e_card == card or tgt.startswith(f"{card}/"):
            hit.append({"ts": e.get("ts"), "by": e.get("by"), "reason": e.get("reason")})
    return hit


def _library_missing_oracle() -> tuple[list[str], int]:
    """全库（atoms + evidence）缺 `verified_by_oracle` 的**卡清单**与总卡数（只读扫描）。

    与"命题所属卡"分开报：任务书口径是**全库 83 张**（27 原子 + 56 证据）——换代影响面看的是
    全库，而四轴表只覆盖有命题的卡。清单本身是交付物（**机器只列缺，不代填**）。
    """
    cards = sorted(p for base, pat in ((ROOT / "atoms", "ATOM-*.md"),
                                       (ROOT / "evidence", "EV-*.md"))
                   for p in base.rglob(pat) if p.is_file())
    miss = [p.relative_to(ROOT).as_posix() for p in cards
            if _card_oracle(p.relative_to(ROOT).as_posix()) is None]
    return miss, len(cards)


def build_rows(limit: int | None = None) -> dict:
    reg = _load_registry()
    oracles = (reg.get("oracles") or {}) if isinstance(reg, dict) else {}
    events = _load_overturned()
    props = _props(DEFAULT_DB)
    if limit:
        props = props[:limit]
    rows: list[dict] = []
    miss_oracle: list[str] = []
    stale: list[dict] = []
    for pr in props:
        vo = _card_oracle(pr["card_path"])
        try:
            ts = _git_commit_iso(ROOT / pr["card_path"])
        except RuntimeError as exc:
            _die(f"git 时间轴不可用（{exc}）——四轴视图**拒绝降级返回**，"
                 "请确认在 git 仓库内且 git 可用")
        ov = _overturned_for(pr["prop_key"], pr["card"], events)
        row = {"prop_key": pr["prop_key"],
               "card": pr["card"],
               "claim_type": pr["claim_type"],
               "asserted_at_approx_from_card_commit": ts,
               "oracle": vo or "missing",
               "overturned": 1 if ov else 0,
               "overturned_events": ov,
               "anchor_source": pr["anchor_source"],
               "signoff_state": pr["signoff_state"]}
        if vo is None:
            miss_oracle.append(pr["card"])
        else:
            want = str((oracles.get(vo["name"]) or {}).get("version") or "")
            if vo["name"] not in oracles or (want and vo["version"] and vo["version"] != want):
                stale.append({"card": pr["card"], "prop_key": pr["prop_key"],
                              "have": vo, "registry": want or "<未登记>"})
        rows.append(row)
    cards = sorted({pr["card"] for pr in props})
    lib_miss, lib_total = _library_missing_oracle()     # lib_miss = 卡清单
    return {
        "version": VERSION,
        "evidence_grade": "asserted_at_approx_from_card_commit 是 **B 级证据**："
                          "git 历史可被 rebase/amend 重写；本字段**不是**权威断言时间。",
        "registry_current_oracles": sorted(oracles),
        "counts": {"propositions": len(rows), "cards": len(cards),
                   "missing_oracle_cards": len(sorted(set(miss_oracle))),
                   "library_cards": lib_total,
                   "library_missing_oracle_cards": len(lib_miss),
                   "stale": len(stale),
                   "overturned_events": len(events)},
        "rows": rows,
        "lists": {
            "missing_oracle_cards": sorted(set(miss_oracle)),
            "library_missing_oracle_cards": lib_miss,
            "stale": sorted(stale, key=lambda d: d["card"]),
        },
    }


def _print_human(payload: dict, limit: int | None) -> None:
    c = payload["counts"]
    print(f"[prop_asof] {VERSION} · 命题 {c['propositions']} 条 / 命题所属卡 {c['cards']} 张 · "
          f"**全库缺 oracle 字段 {c['library_missing_oracle_cards']}/{c['library_cards']} 张**"
          f"（其中命题所属卡 {c['missing_oracle_cards']} 张）· stale {c['stale']} · "
          f"推翻事件 {c['overturned_events']} 条")
    print(f"[prop_asof] ⚠ {payload['evidence_grade']}")
    print()
    print(f"{'prop_key':44s} {'claim_type':12s} {'asserted(≈卡提交)':22s} {'oracle':22s} "
          f"{'被推翻':6s} {'锚':9s}")
    for r in payload["rows"]:
        o = r["oracle"]
        o_s = "missing" if o == "missing" else f"{o['name']}={o['version'] or '?'}"
        print(f"{r['prop_key']:44s} {r['claim_type']:12s} "
              f"{r['asserted_at_approx_from_card_commit'][:19]:22s} {o_s:22s} "
              f"{r['overturned']:<6d} {r['anchor_source']:9s}")
    print()
    libmiss = payload["lists"]["library_missing_oracle_cards"]
    print(f"[清单①] 全库缺 `verified_by_oracle` 的卡（{len(libmiss)} 张）"
          "——**机器只列缺，不代填**（这是人/强模型的活）：")
    print("   " + (", ".join(libmiss[:12]) + (" …" if len(libmiss) > 12 else "")
                   if libmiss else "（无）"))
    print(f"        （其中**有命题**的卡 {len(set(payload['lists']['missing_oracle_cards']))} 张）")
    st = payload["lists"]["stale"]
    print(f"[清单②] 被 registry 判 stale 的命题（{len(st)} 条）：")
    if not st:
        print("   （无——**注意**：这不是「版本齐备」，而是「无归属 ⇒ 全体保守」，见清单①）")
    for d in st[:20]:
        print(f"   {d['prop_key']} · 卡面 {d['have']} vs registry {d['registry']}")
    print("[清单③] 无 liveness 锚的 observation 命题：见 `data/prop_liveness_todo.md`（不在本工具口径内）")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="583 N1：命题四轴只读快照（同输入两次跑逐字相同）")
    ap.add_argument("--json", action="store_true", help="输出 JSON（stdout，确定性）")
    ap.add_argument("--limit", type=int, default=None, help="只看前 N 条命题（默认全部）")
    a = ap.parse_args(argv)
    payload = build_rows(a.limit)
    if a.json:
        print(json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True))
    else:
        _print_human(payload, a.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
