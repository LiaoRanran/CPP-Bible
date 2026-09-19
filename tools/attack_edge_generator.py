#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""attack_edge_generator.py — 候选攻击边自动生成（596 任务1；594 W2 模型的**数据地基**）。

为什么：593 异族调研在本仓 79 命题图上手搓 grounded 求解器，三种自然攻击构造**全部退化**
（零攻击全接受 / 单向语义倒置 / 对称全不确定）——瓶颈不是算法，是**没有可信的攻击关系数据**。
594 的 W2 只差一件事：把"误解库 ↔ 原子卡/命题"的**既有书面关联**变成有方向的攻击边。本工具就是
那一步：从误区库的 `related_atoms`（MIS → 原子卡）与卡面 `claim_structured`（原子卡 → 命题）
**纯标准库**推导出：

  * `mis_to_prop`（MIS 攻击命题）：误解指出"这个命题所断言的用法是错的"；
  * `prop_to_mis`（命题反驳误解，**对称边**）：命题反过来把误解判出局。
    594 实证：**没有对称边就会退化**（单向 ⇒ MIS 无入边 ⇒ 永远 IN ⇒ 语义倒置），所以对称边
    不是"锦上添花"，是模型成立的必要条件。

可信度分级（任务书 596 任务1.5；取值 high=3 / medium=2 / low=1，见 `CONFIDENCE_WEIGHT`）：
  * `high`：MIS 卡面有非空 `verified_by`（人审过）；
  * `medium`：MIS 卡面 `machine_verified` 为真（或等效字段）；
  * `low`：无任何可信度字段（默认）。

幂等纪律：**同输入 ⇒ 逐字节同输出**。因此 `generated_at` 默认 `null`（时间戳会破坏幂等，
而对账靠内容本身）；需要打点时显式 `--now <ISO8601>`。排序确定（方向 → source → target → kind）。

只读纪律：不写卡、不写命题库；唯一写动作是 `generate` 覆盖写**派生数据**
`data/attack_edges_candidates.jsonl`（入库，便于对账）。

用法：
    python tools/attack_edge_generator.py generate [--out PATH] [--now ISO]
    python tools/attack_edge_generator.py stats [--json]
    python tools/attack_edge_generator.py --check        # 独立复算 + 字段/存在性/去重校验（失败 exit 2）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_engine as ge  # noqa: E402

VERSION = "1.0"
DEFAULT_MIS_DIR = ROOT / "misconceptions"
DEFAULT_ATOMS_DIR = ROOT / "atoms"
DEFAULT_OUT = ROOT / "data" / "attack_edges_candidates.jsonl"

#: 可信度三级（任务书口径：严格大于才构成"击败"，见 weighted_af_solver）
CONFIDENCE_WEIGHT = {"high": 3, "medium": 2, "low": 1}
#: 命题 id 在**本批数据文件**里的写法（任务书 596 任务1：`卡id::prop-N`）。
#: 注意：`prop_graph.py` 内部用 `卡id/prop-N`（斜杠）——本批不改它，只在本工具边界做映射。
PROP_SEP = "::"
KINDS = ("related_atom", "misconception", "misconception_refutation")
EVIDENCE_MAX = 200


# ── 读取面（只读）──────────────────────────────────────────────────────────────
def _as_list(v: object) -> list[str]:
    if isinstance(v, list):
        return [str(x).strip() for x in v if str(x).strip()]
    if isinstance(v, str):
        return [x.strip() for x in v.replace(",", " ").split() if x.strip()]
    return []


def read_mis(mis_dir: Path | str = DEFAULT_MIS_DIR) -> dict[str, dict]:
    """读误区库：`{mis_id: {related_atoms, misconceptions, refutations, confidence}}`（排序确定）。"""
    out: dict[str, dict] = {}
    for f in sorted(Path(mis_dir).rglob("MIS-*.md")):
        if "README" in f.name:
            continue
        m = ge._meta(f)
        mid = str(m.get("id") or f.stem)
        out[mid] = {
            "path": f,
            "related_atoms": _as_list(m.get("related_atoms")),
            "misconceptions": _as_list(m.get("misconceptions")),
            "refutations": _as_list(m.get("refutations")),
            "confidence": confidence_of(m),
        }
    return out


def confidence_of(meta: dict) -> str:
    """可信度分级（任务书 596 任务1.5）。实测：MIS 卡面 **0 张**有 `verified_by`/`machine_verified`
    ⇒ 当前全部落在 `low`（这条事实写进 `stats` 与 worklog，不假装有分级）。"""
    if str(meta.get("verified_by") or "").strip():
        return "high"
    if meta.get("machine_verified") in (True, 1, "true", "True"):
        return "medium"
    return "low"


def atom_props(atoms_dir: Path | str = DEFAULT_ATOMS_DIR) -> dict[str, list[str]]:
    """原子卡 → 它声明的命题 id 列表（`卡id::prop-N`，按 prop id 排序）。"""
    out: dict[str, list[str]] = {}
    for p in sorted(Path(atoms_dir).rglob("ATOM-*.md")):
        if "README" in p.name:
            continue
        m = ge._meta(p)
        cid = str(m.get("id") or p.stem)
        pids = []
        for it in (m.get("claim_structured") or []):
            if isinstance(it, dict) and str(it.get("id") or "").strip():
                pids.append(f"{cid}{PROP_SEP}{str(it['id']).strip()}")
        out[cid] = sorted(pids)
    return out


def _evidence_snippet(refs: list[str]) -> str:
    """证据 = 该 MIS 的 `refutations` 文本片段（前 200 字；多条以 ` / ` 连接后截断）。"""
    text = " / ".join(refs)
    return text[:EVIDENCE_MAX]


# ── 生成 ───────────────────────────────────────────────────────────────────────
def generate_edges(mis_dir: Path | str = DEFAULT_MIS_DIR,
                   atoms_dir: Path | str = DEFAULT_ATOMS_DIR,
                   *, now: str | None = None) -> tuple[list[dict], list[str]]:
    """生成候选攻击边（排序确定的列表）+ 跳过告警列表。

    规则（严格按 596 任务1）：
      1. 每个 MIS 的 `related_atoms` 指向原子卡 → 该卡**所有**命题 ⇒ 每条 `mis_to_prop`（kind `related_atom`）；
      2. 每个 MIS 的 `misconceptions` 字段同样解析为卡 id（0 张目前有该字段）⇒ kind `misconception`；
      3. 每条 `mis_to_prop` **再配一条对称边** `prop_to_mis`（kind `misconception_refutation`）——W2 的必要条件；
      4. 去重：同 `(source, target, kind)` 只留**可信度最高**的一条。
    """
    mis = read_mis(mis_dir)
    props = atom_props(atoms_dir)
    warn: list[str] = []
    seen: dict[tuple[str, str, str], dict] = {}

    def put(source: str, target: str, kind: str, confidence: str, evidence: str,
            direction: str) -> None:
        key = (source, target, kind)
        rec = {"id": f"ae-{source}->{target}", "source": source, "target": target,
               "kind": kind, "evidence": evidence, "confidence": confidence,
               "direction": direction, "generated_at": now,
               "generator_version": VERSION}
        old = seen.get(key)
        if old is None or CONFIDENCE_WEIGHT[confidence] > CONFIDENCE_WEIGHT[old["confidence"]]:
            seen[key] = rec

    for mid in sorted(mis):
        info = mis[mid]
        snip = _evidence_snippet(info["refutations"])
        for field, kind in (("related_atoms", "related_atom"),
                            ("misconceptions", "misconception")):
            for cid in info[field]:
                if cid not in props:
                    warn.append(f"{mid}.{field} 指向不存在的原子卡 {cid} ⇒ 跳过（不生成边）")
                    continue
                for pid in props[cid]:
                    put(mid, pid, kind, info["confidence"], snip, "mis_to_prop")
                    put(pid, mid, "misconception_refutation", info["confidence"], snip,
                        "prop_to_mis")
    edges = [seen[k] for k in sorted(seen)]
    return edges, warn


def write_edges(edges: list[dict], out: Path | str = DEFAULT_OUT) -> Path:
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="\n") as f:
        for e in edges:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    return p


def load_edges(path: Path | str = DEFAULT_OUT) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if ln.strip():
            out.append(json.loads(ln))
    return out


# ── 统计 / 校验 ────────────────────────────────────────────────────────────────
def stats(edges: list[dict]) -> dict:
    def hist(key: str) -> dict[str, int]:
        d: dict[str, int] = {}
        for e in edges:
            d[str(e.get(key))] = d.get(str(e.get(key)), 0) + 1
        return dict(sorted(d.items()))
    return {"total": len(edges), "by_kind": hist("kind"), "by_confidence": hist("confidence"),
            "by_direction": hist("direction"), "by_source": hist("source"),
            "by_target": hist("target"),
            "distinct_sources": len({e["source"] for e in edges}),
            "distinct_targets": len({e["target"] for e in edges})}


def check(edges: list[dict], *, mis_dir: Path | str = DEFAULT_MIS_DIR,
          atoms_dir: Path | str = DEFAULT_ATOMS_DIR) -> list[str]:
    """独立复算 + 结构校验；返回问题清单（空 = 通过）。"""
    problems: list[str] = []
    fresh, _warn = generate_edges(mis_dir, atoms_dir, now=None)
    if len(fresh) != len(edges):
        problems.append(f"边数与独立复算不一致：文件 {len(edges)} vs 复算 {len(fresh)}")
    fresh_ids = {e["id"] for e in fresh}
    file_ids = {e["id"] for e in edges}
    if fresh_ids != file_ids:
        problems.append(f"边集与独立复算不一致：仅文件 {sorted(file_ids - fresh_ids)[:5]} / "
                        f"仅复算 {sorted(fresh_ids - file_ids)[:5]}")
    if len(file_ids) != len(edges):
        problems.append(f"存在重复 id（{len(edges) - len(file_ids)} 条）")
    mis, props = read_mis(mis_dir), atom_props(atoms_dir)
    all_props = {p for ps in props.values() for p in ps}
    required = ("id", "source", "target", "kind", "evidence", "confidence", "direction",
                "generated_at", "generator_version")
    for i, e in enumerate(edges, 1):
        miss = [k for k in required if k not in e]
        if miss:
            problems.append(f"第 {i} 条缺字段 {miss}")
            continue
        if e["kind"] not in KINDS:
            problems.append(f"第 {i} 条 kind 非法：{e['kind']}")
        if e["confidence"] not in CONFIDENCE_WEIGHT:
            problems.append(f"第 {i} 条 confidence 非法：{e['confidence']}")
        if e["direction"] == "mis_to_prop":
            if e["source"] not in mis:
                problems.append(f"第 {i} 条 source MIS 不存在：{e['source']}")
            if e["target"] not in all_props:
                problems.append(f"第 {i} 条 target 命题不存在：{e['target']}")
        elif e["direction"] == "prop_to_mis":
            if e["source"] not in all_props:
                problems.append(f"第 {i} 条 source 命题不存在：{e['source']}")
            if e["target"] not in mis:
                problems.append(f"第 {i} 条 target MIS 不存在：{e['target']}")
        else:
            problems.append(f"第 {i} 条 direction 非法：{e['direction']}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="候选攻击边自动生成（只读卡面；派生数据入库）")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("generate", "stats"):
        sp = sub.add_parser(name)
        sp.add_argument("--mis-dir", default=str(DEFAULT_MIS_DIR))
        sp.add_argument("--atoms-dir", default=str(DEFAULT_ATOMS_DIR))
        sp.add_argument("--out", default=str(DEFAULT_OUT))
        sp.add_argument("--json", action="store_true")
        if name == "generate":
            sp.add_argument("--now", default=None,
                            help="打点时间（ISO8601）。默认不打点 —— 时间戳会破坏逐字节幂等")
    ap.add_argument("--check", action="store_true", help="独立复算 + 结构校验（失败 exit 2）")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--mis-dir", default=str(DEFAULT_MIS_DIR))
    ap.add_argument("--atoms-dir", default=str(DEFAULT_ATOMS_DIR))
    a = ap.parse_args(argv)

    if a.check:
        edges = load_edges(a.out)
        if not edges:
            print(f"[attack] ❌ 候选边文件为空或不存在：{a.out}（先跑 generate）", file=sys.stderr)
            return 2
        problems = check(edges, mis_dir=a.mis_dir, atoms_dir=a.atoms_dir)
        if problems:
            print(f"[attack] ❌ 校验失败（{len(problems)} 项）：", file=sys.stderr)
            for p in problems[:20]:
                print(f"  - {p}", file=sys.stderr)
            return 2
        print(f"[attack] ✓ 校验通过：{len(edges)} 条候选边（独立复算一致 · 字段完整 · "
              f"source/target 存在 · 无重复）")
        return 0

    if a.cmd == "stats":
        st = stats(load_edges(a.out))
        if a.json:
            print(json.dumps(st, ensure_ascii=False, indent=1))
            return 0
        print(f"[attack] 候选边 {st['total']} 条 · source MIS {st['distinct_sources']} 个 · "
              f"target {st['distinct_targets']} 个")
        print(f"[attack] 按 kind {st['by_kind']}")
        print(f"[attack] 按 confidence {st['by_confidence']}（实测：MIS 卡面无可信度字段 ⇒ 当前全 low）")
        print(f"[attack] 按 direction {st['by_direction']}")
        top = dict(sorted(st["by_source"].items(), key=lambda kv: -kv[1])[:5])
        print(f"[attack] source 分布 Top5 {top}（共 {len(st['by_source'])} 个 MIS）")
        return 0

    # generate（默认子命令）
    edges, warn = generate_edges(a.mis_dir, a.atoms_dir, now=a.now)
    out = write_edges(edges, a.out)
    st = stats(edges)
    print(f"[attack] 已写 {Path(out).relative_to(ROOT).as_posix() if str(out).startswith(str(ROOT)) else out}"
          f"：{st['total']} 条（kind {st['by_kind']}）")
    print(f"[attack] source MIS {st['distinct_sources']} 个 · target {st['distinct_targets']} 个 · "
          f"confidence {st['by_confidence']}")
    for w in warn:
        print(f"[attack] ⚠ {w}", file=sys.stderr)
    if warn:
        print(f"[attack] 跳过告警 {len(warn)} 条（见 stderr；不崩溃、不静默）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
