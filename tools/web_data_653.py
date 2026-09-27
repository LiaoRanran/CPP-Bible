#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""web_data_653.py — 653 B · 前端数据生成（**真实台账 → web/data/*.json，不造数据**）。

数据来源（全部真实、可复核）：
1. `data/grounded_labels_w2.json`（W2 加权接地模型，weighted_af_solver v1.1）：
   - `nodes`（131 命题）每项含 `card / label(IN|OUT|UNDEC) / credibility / attackers /
     defenders / defeated_attackers` ⇒ **边由节点表物化**（`edges`/`defeating_edges` 在该文件里
     只是**计数**，不是列表）；
   - `summary`（IN/OUT/UNDEC 计数）。
2. `atoms/**/*.md` 前置元数据（卡 id / domain / status / title）。
3. `data/638_four_state_schema.json`（四态：`baseline_dist` 34 pass / 3 unknown；`boundary_ok`）。

四态派生口径（**显式登记，不编造**）：
- 命题节点：`label=IN ⇒ pass`；`OUT ⇒ fail`；`UNDEC ⇒ unknown`。
- 卡节点：子命题有 OUT ⇒ fail；有 UNDEC ⇒ unknown；全 IN 且 credibility<3 ⇒ pass_with_exception；
  全 IN 且 credibility==3 ⇒ pass。

用法：`--check` / `--build`（写 web/data/graph.json + web/data/manifest.json）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "adapter", "name": "web_data_653", "entry": "build",
                "description": "653 B 前端真实数据生成（W2 接地图 + 卡元数据 → web/data/*.json）"}

W2 = ROOT / "data" / "grounded_labels_w2.json"
FS = ROOT / "data" / "638_four_state_schema.json"
WEB = ROOT / "web"
GRAPH_OUT = WEB / "data" / "graph.json"
MANIFEST_OUT = WEB / "data" / "manifest.json"
PCK_DIR = ROOT / "data" / "pck" / "certificates"

_FM = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_ID = re.compile(r"^id:\s*(\S+)", re.MULTILINE)
_STATUS = re.compile(r"^status:\s*(\S+)", re.MULTILINE)
_DOMAIN = re.compile(r"^domain:\s*(\S+)", re.MULTILINE)
_TITLE = re.compile(r"^title:\s*(.+)$", re.MULTILINE)

LABEL_TO_STATE = {"IN": "pass", "OUT": "fail", "UNDEC": "unknown"}
STATES = ("pass", "pass_with_exception", "fail", "unknown")


def load_w2() -> dict:
    data: dict = json.loads(W2.read_text(encoding="utf-8"))
    return data


def load_cards() -> list[dict]:
    out = []
    for p in sorted((ROOT / "atoms").rglob("*.md")):
        if p.name.upper().startswith("README"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = _FM.match(text)
        if not fm:
            continue
        f = fm.group(1)
        im, sm_, dm, tm = _ID.search(f), _STATUS.search(f), _DOMAIN.search(f), _TITLE.search(f)
        if not im:
            continue
        out.append({"id": im.group(1).strip().strip('"'),
                    "status": (sm_.group(1).strip().strip('"') if sm_ else "unknown"),
                    "domain": (dm.group(1).strip().strip('"') if dm else "?"),
                    "title": (tm.group(1).strip().strip('"') if tm else "")[:80]})
    return out


def derive_card_state(props: list[dict]) -> str:
    labels = {p["label"] for p in props}
    if "OUT" in labels:
        return "fail"
    if "UNDEC" in labels:
        return "unknown"
    creds = [p.get("credibility", 3) for p in props]
    if creds and min(creds) < 3:
        return "pass_with_exception"
    return "pass"


def build_graph() -> dict:
    w2 = load_w2()
    nodes_raw: dict[str, dict] = w2["nodes"]
    cards = load_cards()

    props: dict[str, list[dict]] = {}
    for nid, n in nodes_raw.items():
        props.setdefault(n.get("card", "?"), []).append(n)

    nodes: list[dict] = []
    links: list[dict] = []
    seen_edges: set[tuple[str, str, str]] = set()

    def add_edge(s: str, t: str, kind: str, defeated: bool) -> None:
        key = (s, t, kind)
        if key in seen_edges:
            return
        seen_edges.add(key)
        links.append({"source": s, "target": t, "kind": kind, "defeated": defeated})

    # ① 卡节点（真实 atoms，47 张；含四态派生）
    for c in cards:
        cprops = props.get(c["id"], [])
        state = derive_card_state(cprops) if cprops else (
            "pass" if c["status"] == "verified" else "unknown")
        nodes.append({
            "id": c["id"], "kind": "card", "state": state, "domain": c["domain"],
            "status": c["status"], "title": c["title"], "credibility": 3,
            "props": len(cprops),
        })
        for p in cprops:
            add_edge(c["id"], p["id"], "asserts", False)

    # ② 命题节点 + 边（由 attackers/defenders/defeated_attackers 物化）
    for nid, n in nodes_raw.items():
        is_mis = nid.startswith("MIS-")          # 误解节点（攻击者）用「方」形编码
        nodes.append({
            "id": nid, "kind": "misconception" if is_mis else "prop",
            "state": LABEL_TO_STATE.get(n.get("label", ""), "unknown"),
            "domain": (n.get("card", "").split("-")[1].lower() if "-" in n.get("card", "") else "?"),
            "status": n.get("signoff_state", ""), "title": f"{n.get('claim_type', '')}",
            "credibility": int(n.get("credibility", 3)), "label": n.get("label"),
            "card": n.get("card"),
        })
        defeated = set(n.get("defeated_attackers", []) or [])
        for a in (n.get("attackers", []) or []):
            add_edge(a, nid, "attack", a in defeated)
        for d in (n.get("defenders", []) or []):
            add_edge(d, nid, "defend", False)

    # ③ 未在卡表里的攻击者（误解节点 MIS-*）补为节点
    known = {x["id"] for x in nodes}
    for ln in links:
        for end in (ln["source"], ln["target"]):
            if end not in known:
                known.add(end)
                nodes.append({"id": end, "kind": "misconception",
                              "state": "fail" if end.startswith("MIS-") else "unknown",
                              "domain": (end.split("-")[1].lower() if end.count("-") >= 1 else "?"),
                              "status": "attacker", "title": "", "credibility": 1})

    defeated_n = sum(1 for ln in links if ln["defeated"])
    kind_n: dict[str, int] = {}
    for ln in links:
        kind_n[ln["kind"]] = kind_n.get(ln["kind"], 0) + 1
    return {
        "meta": {
            "generated_from": [
                "data/grounded_labels_w2.json (W2 weighted_af_solver v1.1)",
                "atoms/**/*.md frontmatter",
                "data/638_four_state_schema.json",
            ],
            "w2_summary": w2.get("summary", {}),
            "w2_model": w2.get("model"), "w2_rounds": w2.get("rounds"),
            "counts": {"nodes": len(nodes), "links": len(links), "defeated_links": defeated_n,
                       "cards": sum(1 for x in nodes if x["kind"] == "card"),
                       "props": sum(1 for x in nodes if x["kind"] == "prop"),
                       "by_kind": dict(sorted(kind_n.items()))},
            "w2_declared": {"edges": w2.get("edges"), "defeating_edges": w2.get("defeating_edges")},
            "four_state_rule": "prop: IN→pass/OUT→fail/UNDEC→unknown；card: 有OUT→fail/有UNDEC→unknown/"
                               "全IN且cred<3→pass_with_exception/全IN且cred=3→pass",
            "states": list(STATES),
        },
        "nodes": nodes,
        "links": links,
    }


def build_manifest() -> dict:
    """B2 现场验哈希用的**真实工件清单**（sha256 由本机现算，浏览器可离线复核）。"""
    items = []
    for rel in ("data/grounded_labels_w2.json", "data/648_c_probe.json",
                "data/supply_chain/merkle_roots.json", "tools/.tool_checksums"):
        p = ROOT / rel
        if p.is_file():
            items.append({"path": rel, "bytes": p.stat().st_size,
                          "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    for p in sorted(PCK_DIR.glob("*.yaml"))[:12]:
        items.append({"path": str(p.relative_to(ROOT)).replace("\\", "/"),
                      "bytes": p.stat().st_size,
                      "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    return {"note": "sha256 为本机现算；浏览器用 Web Crypto 对同一文件重算即可离线复核（不联网、无后端）。",
            "count": len(items), "items": items}


def _write() -> dict:
    WEB.mkdir(parents=True, exist_ok=True)
    (WEB / "data").mkdir(parents=True, exist_ok=True)
    g = build_graph()
    GRAPH_OUT.write_text(json.dumps(g, ensure_ascii=False, indent=1), encoding="utf-8")
    m = build_manifest()
    MANIFEST_OUT.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"graph": g["meta"]["counts"], "manifest": m["count"],
            "declared_w2": g["meta"]["w2_declared"]}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    g = build_graph()
    c = g["meta"]["counts"]
    chk("有卡节点", c["cards"] > 0, str(c["cards"]))
    chk("有命题节点", c["props"] > 0, str(c["props"]))
    chk("边被物化（>0）", c["links"] > 0, str(c["links"]))
    attack_n = c["by_kind"].get("attack", 0)
    chk("声明 edges=388 与物化 attack 边一致",
        g["meta"]["w2_declared"]["edges"] == attack_n,
        f"declared={g['meta']['w2_declared']['edges']} attack={attack_n}")
    chk("击败边计数一致（defeating_edges）",
        g["meta"]["w2_declared"]["defeating_edges"] == c["defeated_links"],
        f"declared={g['meta']['w2_declared']['defeating_edges']} materialized={c['defeated_links']}")
    chk("四态取值合法", all(n["state"] in STATES for n in g["nodes"]))
    chk("manifest 有 sha256", build_manifest()["count"] > 0)
    print(f"web_data_653 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="653 B 前端真实数据生成")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--build", action="store_true")
    a = ap.parse_args()
    if a.check:
        raise SystemExit(selftest())
    rep = _write()
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    raise SystemExit(0)
