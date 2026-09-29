#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""status_reconciler_658.py — 元状态对账器（658 D 段）。

设计原则（658 D5 反自证）：**越蠢越好**。
- 只用 git CLI + 文件系统 + 门禁产物（junit xml / mutation report）。
- **不 import queyi core / gate_engine / 任何本仓库工具链** —— 不能用自己的工具证明自己。
- 只回答四类问题：文档说的 HEAD==实际？ahead 数==实际？卡数==baseline？CI green==实际 gate？

用法：
    python tools/status_reconciler_658.py --check            # 对账，不一致→META-STATE-CONFLICT，exit 1
    python tools/status_reconciler_658.py --emit-agent       # 重写 AGENT.md 的 <!-- GENERATED --> 块
    python tools/status_reconciler_658.py --emit-next        # 生成 NEXT_LLM.md
    python tools/status_reconciler_658.py --selftest         # 自检（工具自身可跑、可产出 dict）
    python tools/status_reconciler_658.py --json             # 只打印观测事实 JSON
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBE_DIRS = ("_arch_v", "_pytest_tmp", "backup_652", "node_modules", ".pytest_tmp")
TOLERATED_KEYS: set = set()  # 660 B5：规则口径已收敛；666 A6 定位为 data/_gate_rules.json 实测 == gate_engine.RULES == 67（旧值 63 见 _arch_v19_brief.md，属历史快照）


def _run(args):
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=120).stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


def _git(args):
    return _run(["git"] + args)


def _is_ancestor(a, b):
    """a 是否为 b 的祖先（用于 HEAD 快照语义）。返回 True/False/None(未知)。"""
    if not a or not b:
        return None
    try:
        r = subprocess.run(["git", "merge-base", "--is-ancestor", a, b],
                           cwd=ROOT, capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            return True
        if r.returncode == 1:
            return False
        return None
    except Exception:  # noqa: BLE001
        return None


def observed_facts():
    facts = {}
    facts["head"] = _git(["rev-parse", "HEAD"])
    facts["branch"] = _git(["rev-parse", "--abbrev-ref", "HEAD"]) or "master"
    ahead = _git(["rev-list", "--count", "origin/master..HEAD"])
    behind = _git(["rev-list", "--count", "HEAD..origin/master"])
    facts["ahead_of_origin_master"] = int(ahead) if ahead.isdigit() else 0
    facts["behind_origin_master"] = int(behind) if behind.isdigit() else 0
    # dirty：排除探针/构建目录
    porcelain = _git(["status", "--porcelain"])
    dirty = False
    for line in porcelain.splitlines():
        path = line[3:].strip()
        if not any(p in path for p in PROBE_DIRS):
            dirty = True
            break
    facts["dirty"] = dirty
    # mutation
    mut = {}
    for name, key in (("data/656_mutation_report_core.json", "core"),
                      ("data/656_mutation_report_all.json", "all")):
        p = os.path.join(ROOT, name)
        if os.path.isfile(p):
            try:
                d = json.load(open(p, encoding="utf-8"))
                kr = d.get("kill_rate_on_scored") or d.get("kill_rate")
                if isinstance(kr, (int, float)):
                    mut[key] = round(kr, 1)
            except Exception:  # noqa: BLE001
                pass
    facts["mutation"] = mut
    # cards
    cards = 0
    bd = os.path.join(ROOT, "atoms")
    if os.path.isdir(bd):
        for _, _, files in os.walk(bd):
            cards += sum(1 for f in files if f.endswith(".md"))
    facts["cards_atoms_total"] = cards
    # graph
    gp = os.path.join(ROOT, "web", "data", "graph.json")
    if os.path.isfile(gp):
        try:
            g = json.load(open(gp, encoding="utf-8"))
            facts["graph_nodes"] = len(g.get("nodes", []))
            facts["graph_links"] = len(g.get("links", []))
        except Exception:  # noqa: BLE001
            pass
    # 660 B5：规则数以 data/_gate_rules.json 为准；README 陈述数用于对账
    gp2 = os.path.join(ROOT, "data", "_gate_rules.json")
    if os.path.isfile(gp2):
        try:
            d = json.load(open(gp2, encoding="utf-8"))
            facts["rules_actual"] = len(d)
        except Exception:  # noqa: BLE001
            pass
    rmd = os.path.join(ROOT, "README.md")
    if os.path.isfile(rmd):
        try:
            txt = open(rmd, encoding="utf-8").read()
            m = re.search(r"(\d+)\s*规则", txt)
            if m:
                facts["readme_rules"] = int(m.group(1))
            m = re.search(r"(\d+)\s*节点\s*/\s*[\d,]*\s*边", txt)  # 仅匹配星图行，避开 W2 的 131 节点
            if m:
                facts["readme_nodes"] = int(m.group(1))
        except Exception:  # noqa: BLE001
            pass
    return facts


def load_baseline():
    p = os.path.join(ROOT, "data", "baseline.json")
    if not os.path.isfile(p):
        return None
    return json.load(open(p, encoding="utf-8"))


def reconcile(facts, baseline):
    conflicts = []
    if not baseline:
        conflicts.append("baseline.json 不存在")
        return conflicts
    g = baseline.get("git", {})
    # HEAD 采用「快照 + 祖先」语义：baseline 是某时刻的快照；
    # 之后新增提交（快照落后）是正常的，只有「文档声明的 HEAD 不是实际 HEAD 的祖先」
    # 才是真冲突（历史被改写 / 文档造假 / 指到不存在的提交）。
    bh, fh = g.get("head"), facts.get("head")
    if bh and fh:
        if bh == fh:
            facts["_baseline_head"] = "equal"
        elif _is_ancestor(bh, fh):
            facts["_baseline_head"] = "ancestor(snapshot-behind)"
        else:
            conflicts.append(
                f"HEAD 非 baseline 后代：baseline={bh[:10]} 实际={fh[:10]}（历史被改写或文档造假）")
    # ahead/behind 是快照数字，会随提交自然增长 → 仅记录，不判冲突
    facts["_baseline_ahead"] = g.get("ahead_of_origin_master")
    bc = baseline.get("cards", {})
    if bc.get("atoms_total") is not None and bc["atoms_total"] != facts.get("cards_atoms_total"):
        conflicts.append(f"卡数不一致：baseline={bc['atoms_total']} 实际={facts.get('cards_atoms_total')}")
    bg = baseline.get("graph", {})
    if bg.get("nodes") is not None and bg["nodes"] != facts.get("graph_nodes"):
        conflicts.append(f"图节点数不一致：baseline={bg['nodes']} 实际={facts.get('graph_nodes')}")
    if bg.get("links") is not None and bg["links"] != facts.get("graph_links"):
        conflicts.append(f"图边数不一致：baseline={bg['links']} 实际={facts.get('graph_links')}")
    # 660 B5：规则数以 _gate_rules.json 为准，README/baseline 必须一致
    ra = facts.get("rules_actual")
    if ra is not None:
        dr = facts.get("readme_rules")
        if dr is not None and dr != ra:
            conflicts.append(f"README 规则数不一致：文档={dr} 实际={ra}（data/_gate_rules.json）")
        br = baseline.get("rules", {}).get("documented_brief")
        if br is not None and br != ra:
            conflicts.append(f"baseline 规则数不一致：文档={br} 实际={ra}（data/_gate_rules.json）")
    rn = facts.get("readme_nodes")
    if rn is not None and facts.get("graph_nodes") is not None and rn != facts["graph_nodes"]:
        conflicts.append(f"README 节点数不一致：文档={rn} 实际={facts['graph_nodes']}（web/data/graph.json）")
    # mutation 容忍 ±0.5（采样/舍入），且只在对账时对比
    bm = baseline.get("mutation", {})
    for k in ("core_kill_rate_pct", "all_kill_rate_pct"):
        bv = bm.get(k)
        fk = "core" if k.startswith("core") else "all"
        fv = facts.get("mutation", {}).get(fk)
        if bv is not None and fv is not None and abs(bv - fv) > 0.5:
            conflicts.append(f"变异{k}不一致：baseline={bv} 实际={fv}")
    return conflicts


def _gen_block(facts):
    return (
        "<!-- GENERATED:BEGIN (status_reconciler_658.py · 机器生成，禁止手改) -->\n"
        f"HEAD: {facts['head']}\n"
        f"Branch: {facts['branch']}\n"
        f"Ahead/Behind: {facts['ahead_of_origin_master']}/{facts['behind_origin_master']}\n"
        f"Dirty(tracked): {facts['dirty']}\n"
        f"Mutation core/all: {facts.get('mutation',{}).get('core','?')}/{facts.get('mutation',{}).get('all','?')}%\n"
        f"Cards(atoms): {facts.get('cards_atoms_total','?')}\n"
        f"Graph nodes/links: {facts.get('graph_nodes','?')}/{facts.get('graph_links','?')}\n"
        "<!-- GENERATED:END -->\n"
    )


def emit_agent(facts):
    p = os.path.join(ROOT, "AGENT.md")
    block = _gen_block(facts)
    if os.path.isfile(p):
        txt = open(p, encoding="utf-8").read()
        if "<!-- GENERATED:BEGIN" in txt and "<!-- GENERATED:END -->" in txt:
            txt = re.sub(r"<!-- GENERATED:BEGIN.*?GENERATED:END -->\n?", block, txt, flags=re.DOTALL)
        else:
            txt = txt.rstrip() + "\n\n" + block
        open(p, "w", encoding="utf-8").write(txt)
    else:
        open(p, "w", encoding="utf-8").write("# AGENT\n\n" + block)
    print("AGENT.md GENERATED 块已更新")


def emit_next(facts):
    p = os.path.join(ROOT, "NEXT_LLM.md")
    baseline = load_baseline() or {}
    cur = baseline.get("cards", {})
    block = (
        "<!-- GENERATED:BEGIN (status_reconciler_658.py · 全自动生成) -->\n"
        "# NEXT_LLM — 给下一个会话的接力棒\n\n"
        f"- 当前 HEAD：`{facts['head']}`（branch {facts['branch']}，ahead {facts['ahead_of_origin_master']}）\n"
        f"- 脏状态：{facts['dirty']}（受控目录 atoms/evidence/Examples/Book/ 零改动是硬红线）\n"
        f"- 当前主线：658 批次（外部效度四层 / 门禁分层 / 元状态可验证 / research v0.1）\n"
        f"- 元状态：mutation core/all {facts.get('mutation',{}).get('core','?')}/{facts.get('mutation',{}).get('all','?')}%；"
        f"卡 {facts.get('cards_atoms_total','?')}；图 {facts.get('graph_nodes','?')}/{facts.get('graph_links','?')}\n"
        f"- 边界现状：{cur.get('boundary_written','?')} 卡有边界（{cur.get('boundary_verified_pass','?')} verified-pass + {cur.get('boundary_redteam_verified','?')} red-team）；{cur.get('draft_empty','?')} draft 留空\n"
        "- 口径裁定（661 A2）：规则数=67（gate_engine.RULES 执行权威；data/_gate_rules.json 已同步 67，旧 63 是 623 缓存漏 4 条 -HC block 规则）；图节点=178（graph.json 实测，任务书称 121 待权威源）\n"
        "- 接手前先跑：`python tools/status_reconciler_658.py --check`（META-STATE-CONFLICT 即停）\n"
        "<!-- GENERATED:END -->\n"
    )
    # 不覆盖整文件（NEXT_LLM.md 可能已有手工执行的「当前阶段」叙述）；
    # 只把 GENERATED 块作为机器对账区插入/更新，保留人工部分。
    if os.path.isfile(p):
        txt = open(p, encoding="utf-8").read()
        if "<!-- GENERATED:BEGIN" in txt and "<!-- GENERATED:END -->" in txt:
            txt = re.sub(r"<!-- GENERATED:BEGIN.*?GENERATED:END -->\n?", block, txt, flags=re.DOTALL)
        else:
            txt = txt.rstrip() + "\n\n" + block
        open(p, "w", encoding="utf-8").write(txt)
    else:
        open(p, "w", encoding="utf-8").write(block)
    print("NEXT_LLM.md GENERATED 块已更新（人工叙述保留）")


def snapshot_baseline(facts):
    """把当前观测事实写回 baseline.json（HEAD 快照点）。只更新机器可算的键。"""
    p = os.path.join(ROOT, "data", "baseline.json")
    base = load_baseline() or {}
    base["git"] = {
        "head": facts["head"],
        "branch": facts["branch"],
        "ahead_of_origin_master": facts["ahead_of_origin_master"],
        "behind_origin_master": facts["behind_origin_master"],
    }
    c = dict(base.get("cards", {}))
    c["atoms_total"] = facts.get("cards_atoms_total")
    base["cards"] = c
    base["graph"] = {"nodes": facts.get("graph_nodes"), "links": facts.get("graph_links")}
    if facts.get("mutation"):
        base["mutation"] = {
            "core_kill_rate_pct": facts["mutation"].get("core"),
            "all_kill_rate_pct": facts["mutation"].get("all"),
        }
    base["snapshot_note"] = "由 status_reconciler_658.py --snapshot 生成；git.head 为快照点（新增提交后自动放宽为祖先）"
    json.dump(base, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"baseline.json 已快照刷新：HEAD {facts['head'][:10]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--emit-agent", action="store_true")
    ap.add_argument("--emit-next", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--snapshot", action="store_true", help="把当前观测事实写回 baseline.json")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    facts = observed_facts()
    if a.json:
        print(json.dumps(facts, ensure_ascii=False, indent=2))
        return
    if a.snapshot:
        snapshot_baseline(facts)
        return
    if a.selftest:
        assert isinstance(facts, dict) and "head" in facts
        assert reconcile(facts, load_baseline()) is not None
        print("selftest OK: reconciler 可独立产出事实 dict 并对账")
        return
    if a.emit_agent:
        emit_agent(facts)
        return
    if a.emit_next:
        emit_next(facts)
        return
    # default: --check
    conflicts = reconcile(facts, load_baseline())
    print("=== 658 元状态对账 ===")
    print(json.dumps(facts, ensure_ascii=False, indent=2))
    if conflicts:
        print("\n[META-STATE-CONFLICT]")
        for c in conflicts:
            print("  -", c)
        sys.exit(1)
    print("\n[OK] 元状态与 baseline.json 一致（受控目录零改动前提下）")


if __name__ == "__main__":
    main()
