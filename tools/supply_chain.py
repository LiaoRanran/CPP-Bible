#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""supply_chain.py — in-toto 风格溯源链最小子集（601 任务2；600 调研阶段2）。

为什么：Merkle 层回答"**文件有没有被换过**"，但不回答"**谁在什么时候、用什么输入、跑出什么**"。
in-toto 的核心是把每个构建步骤记成一条 **link**（materials 输入 hash + products 输出 hash + command +
functionary），再用 **layout** 声明"哪些步骤、什么顺序、谁被授权、事后跑哪些 inspection"。
本仓只实现需要的子集（不引第三方框架、纯标准库）：

  * **Step**：本项目的 7 个构建步骤（见 `STEPS`），每个有 functionary、materials、products、依赖；
  * **Link**：一次执行的记录，**只追加**（`data/supply_chain/links/<step>-<时间>.json`）；
  * **Layout**：`data/supply_chain/layout.json`，声明步骤/顺序/授权/检查点，**只增不减**（删步骤须人审显式做）；
  * **Inspection**：链验证时按顺序跑的检查命令（全是**只读**命令：tool_integrity / merkle / governance）。

签名替代（单用户阶段无密钥对，600 已说清这是**结构性上限**）：link/layout 的 `signature` =
生成时的 **git commit**（可追溯"对应哪个 commit"）。**它不是密码学签名**（git 作者可自设），
挡不住有 git 权限的攻击者 —— 真正的签名留阶段3/密钥对。诚实登记，不假装。

纪律：纯标准库；**不自动产生 link**（必须显式 `link create`）；`chain verify` fail-closed（任一 link
不一致/顺序错 ⇒ exit 1，不跳过）；目录的 hash 用 **Merkle 根**（与任务1 同一套口径）⇒ 链与 Merkle 层咬合。

用法：
    python tools/supply_chain.py layout init            # 生成/刷新 layout（幂等，默认不打点）
    python tools/supply_chain.py layout verify          # 校验 layout 自洽（唯一名/无环/检查点指向存在的步骤）
    python tools/supply_chain.py link create <step> [--functionary X] [--command "..."] [--now ISO]
    python tools/supply_chain.py link verify <link.json>
    python tools/supply_chain.py chain verify [--links-dir DIR] [--no-inspections]
    python tools/supply_chain.py stats [--json]
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import merkle_integrity as mi  # noqa: E402

VERSION = "1.0"
LAYOUT_PATH = ROOT / "data" / "supply_chain" / "layout.json"
LINKS_DIR = ROOT / "data" / "supply_chain" / "links"

#: 本项目的构建步骤（601 任务2；materials/products 用**仓根相对路径**；目录 ⇒ Merkle 根）。
#: `functionary` 支持 glob（`human:*` 表示"任一实名人类"，机器步骤写死工具名）。
STEPS: tuple[dict, ...] = (
    {"name": "card_authoring", "functionary": "human:*", "depends_on": [],
     "materials": [], "products": ["atoms", "evidence", "Examples"],
     "说明": "卡面编写（人/苦力）：产出原子卡、证据卡与夹具"},
    {"name": "gate_check", "functionary": "machine:gate_engine.py", "depends_on": ["card_authoring"],
     "materials": ["atoms", "evidence", "Examples"], "products": [],
     "说明": "门禁校验：结果在 stdout（不落文件 ⇒ products 空）"},
    {"name": "replay_verify", "functionary": "machine:atom_evidence_replay.py",
     "depends_on": ["card_authoring"],
     "materials": ["atoms", "evidence", "Examples"], "products": [],
     "说明": "复算验证：结果在 stdout；`build/replay_manifest.json` 是**易变缓存**，不入链（否则链天天过期）"},
    {"name": "poison_test", "functionary": "machine:poison_drill.py", "depends_on": ["card_authoring"],
     "materials": ["atoms", "evidence", "tools/poison_exemptions.yaml"], "products": [],
     "说明": "毒样例攻击测试：结果在 stdout"},
    {"name": "mutation_test", "functionary": "machine:mutation_fuzz.py", "depends_on": ["card_authoring"],
     "materials": ["atoms", "evidence", "data/mutation"], "products": [], "说明": "变异攻击测试：结果在报告文件（显式产出）"},
    {"name": "metrics_collect", "functionary": "machine:metrics_collector.py",
     "depends_on": ["gate_check", "replay_verify", "poison_test", "mutation_test"],
     "materials": ["atoms", "evidence"], "products": [], "说明": "度量采集：落 data/metrics.jsonl（gitignore，不入链）"},
    {"name": "human_review", "functionary": "human:*", "depends_on": ["card_authoring"],
     "materials": ["data/attack_edges_candidates.jsonl", "data/overturned_events.jsonl"],
     "products": ["data/human_attack_edge_annotations.jsonl"], "说明": "人审确认：候选边/推翻事件 → 人审标注"},
)
#: 检查点：链验证时按顺序执行（**只读**命令）。
INSPECTIONS: tuple[dict, ...] = (
    {"name": "integrity_check", "after": "card_authoring",
     "command": ["tools/tool_integrity.py", "--check"],
     "说明": "核心工具 + 信任根数据 + Merkle 根三层自检"},
    {"name": "merkle_check", "after": "card_authoring",
     "command": ["tools/merkle_integrity.py", "--check"], "说明": "目录级 Merkle 根 vs 当前内容"},
    {"name": "governance_check", "after": "card_authoring",
     "command": ["tools/governance_doc_guard.py", "verify"],
     "说明": "治理 manifest self_hash + 文档逐条一致"},
)
LINK_REQUIRED = ("step", "functionary", "command", "materials", "products", "timestamp",
                 "signature", "link_version")


# ── 基础 ───────────────────────────────────────────────────────────────────────
def step_by_name(name: str) -> dict | None:
    return next((s for s in STEPS if s["name"] == name), None)


def git_commit() -> str | None:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT),
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.strip() if r.returncode == 0 else None


def hash_path(rel_or_path: Path | str) -> dict:
    """给一个仓根相对路径算 hash：文件 ⇒ sha256(内容)；目录 ⇒ **Merkle 根**（与任务1 同口径）。"""
    p = Path(rel_or_path)
    full = p if p.is_absolute() else (ROOT / p)
    if full.is_dir():
        # 目录若是 Merkle 覆盖目录，用它的 include/exclude 配置（口径必须与台账一致）
        rel = full.resolve().relative_to(ROOT).as_posix()
        for key, path, inc, exc in mi.COVERED_DIRS:
            if path == rel:
                t = mi.build_tree(full, include=inc, exclude=exc)
                return {"path": rel, "kind": "dir", "hash": t["root"],
                        "file_count": t["file_count"], "algo": mi.ALGO}
        t = mi.build_tree(full)
        return {"path": rel, "kind": "dir", "hash": t["root"],
                "file_count": t["file_count"], "algo": mi.ALGO}
    if full.is_file():
        rel = full.resolve().relative_to(ROOT).as_posix() if full.is_absolute() else p.as_posix()
        return {"path": rel, "kind": "file", "hash": hashlib.sha256(full.read_bytes()).hexdigest()}
    return {"path": p.as_posix(), "kind": "missing", "hash": None}


# ── link ───────────────────────────────────────────────────────────────────────
def create_link(step_name: str, *, functionary: str | None = None, command: str = "",
                now: str | None = None, layout: dict | None = None) -> dict:
    """按 layout 声明生成一条 link（**不落盘**；落盘走 write_link）。"""
    lay = layout or load_layout() or create_layout()
    step = next((s for s in lay["steps"] if s["name"] == step_name), None)
    if step is None:
        raise ValueError(f"layout 里没有步骤 {step_name!r}（先 `layout init`/人审加步骤）")
    who = functionary or (step["functionary"] if "*" not in step["functionary"]
                          else f"human:{git_author_name() or 'unknown'}")
    return {"step": step_name, "functionary": who, "command": command,
            "materials": [hash_path(m) for m in step["materials"]],
            "products": [hash_path(p) for p in step["products"]],
            "timestamp": now or datetime.now().isoformat(timespec="seconds"),
            "signature": git_commit(), "link_version": VERSION,
            "note": "signature=生成时的 git commit（可追溯，**不是密码学签名**）"}


def git_author_name() -> str | None:
    try:
        r = subprocess.run(["git", "config", "user.name"], cwd=str(ROOT),
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    return (r.stdout or "").strip() or None


def write_link(link: dict, links_dir: Path | str = LINKS_DIR) -> Path:
    """写 link（**只追加**：同名冲突则加后缀，绝不覆盖历史）。"""
    d = Path(links_dir)
    d.mkdir(parents=True, exist_ok=True)
    base = f"{link['step']}-{str(link['timestamp']).replace(':', '').replace('-', '')}"
    p = d / f"{base}.json"
    n = 1
    while p.exists():
        n += 1
        p = d / f"{base}-{n}.json"
    p.write_text(json.dumps(link, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")
    return p


def read_link(path: Path | str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_links(links_dir: Path | str = LINKS_DIR) -> list[tuple[Path, dict]]:
    """读全部 link（按文件名排序 = 时间序），坏文件 ⇒ fail-loud。"""
    d = Path(links_dir)
    if not d.is_dir():
        return []
    out: list[tuple[Path, dict]] = []
    for f in sorted(d.glob("*.json")):
        try:
            out.append((f, json.loads(f.read_text(encoding="utf-8"))))
        except ValueError as exc:
            raise ValueError(f"link 不是合法 JSON：{f}（{exc}）") from exc
    return out


def verify_link(link: dict, layout: dict | None = None, *, check_disk: bool = True) -> list[str]:
    """验证一条 link；返回问题清单（空 = 通过）。

    查四件事：① 字段齐 + 步骤在 layout 里；② functionary 被授权（glob 匹配）；
    ③ materials/products 的**路径集合**与 layout 声明一致；④ 若 `check_disk`：重算 hash 与记录一致
    （不一致 = 「事后被换过」或「link 过期」—— 这正是 585 攻击1 在链路层的检出）。
    """
    lay = layout or load_layout()
    problems: list[str] = []
    if lay is None:
        return ["缺 layout（先 `layout init`）⇒ 无法验证"]
    miss = [k for k in LINK_REQUIRED if k not in link]
    if miss:
        return [f"link 缺字段 {miss}"]
    step = next((s for s in lay["steps"] if s["name"] == link["step"]), None)
    if step is None:
        return [f"link 的步骤 {link['step']!r} 不在 layout 里（layout 只增不减 ⇒ 需人审补步骤）"]
    who = str(link["functionary"])
    if not fnmatch.fnmatch(who, step["functionary"]):
        problems.append(f"functionary {who!r} 未被授权（layout 允许 {step['functionary']!r}）")
    for field in ("materials", "products"):
        got = sorted(str(x.get("path")) for x in link.get(field) or [])
        want = sorted(step[field])
        if got != want:
            problems.append(f"{field} 与 layout 声明不一致：link {got} vs layout {want}")
    if check_disk:
        for field in ("materials", "products"):
            for rec in link.get(field) or []:
                now = hash_path(str(rec.get("path")))
                if now.get("hash") != rec.get("hash"):
                    problems.append(
                        f"{field} `{rec.get('path')}` 与记录不符（记录 {str(rec.get('hash'))[:12]}… "
                        f"实际 {str(now.get('hash'))[:12]}…）⇒ 事后被改或 link 过期，需重建 link")
    return problems


def chain_verify(*, links_dir: Path | str = LINKS_DIR, layout: dict | None = None,
                 check_disk: bool = True, run_inspections: bool = True) -> tuple[list[str], list[str]]:
    """验证整条链：逐 link 校验 + **顺序**（依赖步骤必须先有 link）+ inspection。

    返回 (problems, notes)。**fail-closed**：任一 link 不通过 ⇒ problems 非空（调用方 exit 1），不跳过。
    """
    lay = layout or load_layout()
    if lay is None:
        return ["缺 layout（先 `layout init`）"], []
    problems: list[str] = []
    notes: list[str] = []
    links = load_links(links_dir)
    if not links:
        notes.append("链上没有任何 link（**系统绝不自动记录步骤**：链未开始，需显式 `link create`）")
    first_seen: dict[str, str] = {}
    for path, link in links:
        problems += [f"{path.name}：{p}" for p in verify_link(link, lay, check_disk=check_disk)]
        first_seen.setdefault(str(link.get("step")), str(link.get("timestamp")))
    for step in lay["steps"]:
        if step["name"] not in first_seen:
            continue
        for dep in step["depends_on"]:
            if dep not in first_seen:
                problems.append(f"步骤 {step['name']} 有 link，但依赖步骤 {dep} 没有任何 link "
                                f"（顺序/依赖不成立）")
            elif first_seen[dep] > first_seen[step["name"]]:
                problems.append(f"步骤 {step['name']} 的 link（{first_seen[step['name']]}）"
                                f"**早于**其依赖 {dep}（{first_seen[dep]}）⇒ 顺序倒置")
    if run_inspections and first_seen:
        for insp in lay.get("inspections", []):
            rc, out = run_inspection(insp)
            if rc != 0:
                problems.append(f"inspection {insp['name']} 失败（exit {rc}）：{out.strip()[:200]}")
            else:
                notes.append(f"inspection {insp['name']} ✓")
    return problems, notes


# ── layout ─────────────────────────────────────────────────────────────────────
def create_layout(steps: tuple[dict, ...] | None = None,
                  inspections: tuple[dict, ...] | None = None, *, now: str | None = None) -> dict:
    """生成本项目的 layout（**不含时间戳**，便于幂等与入库比对）。"""
    steps = steps if steps is not None else STEPS
    inspections = inspections if inspections is not None else INSPECTIONS
    return {"layout_version": VERSION, "tool": "supply_chain",
            "generated_at": now, "signature": None,
            "steps": [{"name": s["name"], "functionary": s["functionary"],
                       "depends_on": list(s["depends_on"]), "materials": list(s["materials"]),
                       "products": list(s["products"]), "说明": s.get("说明", "")} for s in steps],
            "inspections": [dict(i) for i in inspections],
            "note": ("in-toto 最小子集：layout 声明步骤/顺序/授权/检查点；**只增不减**"
                     "（删步骤须人审显式做并留 git 痕）；signature=生成时 git commit（非密码学签名）")}


def load_layout(path: Path | str | None = None) -> dict | None:
    # 注意：默认值**在调用时**读模块全局（写成 `path=LAYOUT_PATH` 会把默认值焊死在 def 时刻，
    # 测试里 monkeypatch `sc.LAYOUT_PATH` 就不生效了 —— 601 实测踩到）。
    p = Path(path) if path else LAYOUT_PATH
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def write_layout(layout: dict, path: Path | str | None = None) -> Path:
    p = Path(path) if path else LAYOUT_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(layout, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")
    return p


def verify_layout(layout: dict) -> list[str]:
    """layout 自洽性：步骤名唯一 / 依赖存在且**无环** / 检查点指向存在的步骤 / 授权非空。"""
    problems: list[str] = []
    steps = layout.get("steps") or []
    names = [str(s.get("name")) for s in steps]
    if not names:
        return ["layout 没有任何步骤"]
    dup = sorted({n for n in names if names.count(n) > 1})
    if dup:
        problems.append(f"步骤名重复：{dup}")
    known = set(names)
    graph = {}
    for s in steps:
        if not str(s.get("functionary") or "").strip():
            problems.append(f"步骤 {s.get('name')} 未声明授权 functionary")
        deps = [str(d) for d in (s.get("depends_on") or [])]
        for d in deps:
            if d not in known:
                problems.append(f"步骤 {s.get('name')} 依赖不存在的步骤 {d}")
        graph[str(s.get("name"))] = deps
    # 环检测（DFS 三色）
    color: dict[str, int] = {}

    def visit(n: str, stack: list[str]) -> list[str] | None:
        color[n] = 1
        for d in graph.get(n, []):
            if color.get(d) == 1:
                return stack + [n, d]
            if color.get(d, 0) == 0:
                got = visit(d, stack + [n])
                if got:
                    return got
        color[n] = 2
        return None

    for n in graph:
        if color.get(n, 0) == 0:
            cyc = visit(n, [])
            if cyc:
                problems.append("依赖成环：" + " → ".join(cyc))
                break
    for insp in layout.get("inspections") or []:
        if str(insp.get("after")) not in known:
            problems.append(f"检查点 {insp.get('name')} 挂在不存在的步骤 {insp.get('after')!r}")
        if not insp.get("command"):
            problems.append(f"检查点 {insp.get('name')} 没有命令")
    return problems


def run_inspection(inspection: dict, *, timeout: int = 900) -> tuple[int, str]:
    """跑检查命令（**只读**：全部是 `xxx.py --check/verify` 这类），返回 (exit, 输出)。"""
    cmd = [sys.executable, *[str(c) for c in inspection["command"]]]
    try:
        r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, f"{type(exc).__name__}: {exc}"
    return r.returncode, (r.stdout or "") + (r.stderr or "")


# ── stats ──────────────────────────────────────────────────────────────────────
def stats(*, links_dir: Path | str = LINKS_DIR, layout: dict | None = None) -> dict:
    lay = layout or load_layout()
    links = load_links(links_dir)
    per: dict[str, int] = {}
    last: dict[str, str] = {}
    for _p, link in links:
        s = str(link.get("step"))
        per[s] = per.get(s, 0) + 1
        last[s] = max(last.get(s, ""), str(link.get("timestamp")))
    steps = [s["name"] for s in (lay or {}).get("steps", [])]
    return {"tool": "supply_chain", "version": VERSION,
            "layout": bool(lay), "steps": len(steps), "links": len(links),
            "links_by_step": {k: per[k] for k in sorted(per)},
            "last_by_step": {k: last[k] for k in sorted(last)},
            "steps_without_link": [s for s in steps if s not in per],
            "inspections": len((lay or {}).get("inspections", []))}


def _extract_globals(argv: list[str]) -> tuple[list[str], str | None, str | None]:
    """把 `--layout/--links-dir` 从 argv 里**提到任意位置都能用**（argparse 默认只认子命令之前）。

    返回 (剩余 argv, layout, links_dir)。这两个开关不改变命令语义，只是把默认路径换掉。
    """
    rest: list[str] = []
    layout: str | None = None
    links: str | None = None
    i = 0
    while i < len(argv):
        if argv[i] in ("--layout", "--links-dir") and i + 1 < len(argv):
            if argv[i] == "--layout":
                layout = argv[i + 1]
            else:
                links = argv[i + 1]
            i += 2
            continue
        rest.append(argv[i])
        i += 1
    return rest, layout, links


def main(argv: list[str] | None = None) -> int:
    raw, g_layout, g_links = _extract_globals(list(argv if argv is not None else sys.argv[1:]))
    ap = argparse.ArgumentParser(description="in-toto 风格溯源链最小子集（只追加；不自动记录步骤）")
    ap.add_argument("--layout", default=str(LAYOUT_PATH), help="layout 路径（也可写在子命令之后）")
    ap.add_argument("--links-dir", default=str(LINKS_DIR), help="link 目录（也可写在子命令之后）")
    sub = ap.add_subparsers(dest="cmd")

    lay = sub.add_parser("layout")
    lay.add_argument("action", choices=["init", "verify", "show"])
    lay.add_argument("--now", default=None)

    ln = sub.add_parser("link")
    ln.add_argument("action", choices=["create", "verify"])
    ln.add_argument("step", nargs="?")
    ln.add_argument("--functionary", default=None)
    ln.add_argument("--command", default="")
    ln.add_argument("--now", default=None)
    ln.add_argument("--json", action="store_true")

    ch = sub.add_parser("chain")
    ch.add_argument("action", choices=["verify"])
    ch.add_argument("--no-inspections", action="store_true")
    ch.add_argument("--no-disk", action="store_true")

    st = sub.add_parser("stats")
    st.add_argument("--json", action="store_true")
    a = ap.parse_args(raw)
    if g_layout is not None:
        a.layout = g_layout
    if g_links is not None:
        a.links_dir = g_links

    if a.cmd == "layout":
        if a.action == "init":
            layout = create_layout(now=a.now)
            problems = verify_layout(layout)
            if problems:
                print(f"[sc] ❌ 生成的 layout 不自洽：{problems}", file=sys.stderr)
                return 1
            write_layout(layout, a.layout)
            print(f"[sc] layout 已写 {Path(a.layout).name}：{len(layout['steps'])} 步 · "
                  f"{len(layout['inspections'])} 检查点（自洽 ✓）")
            return 0
        layout = load_layout(a.layout)
        if layout is None:
            print(f"[sc] ❌ 缺 layout：{a.layout}（先 `layout init`）", file=sys.stderr)
            return 2
        problems = verify_layout(layout)
        if problems:
            print(f"[sc] ❌ layout 不自洽（{len(problems)} 项）：", file=sys.stderr)
            for p in problems[:20]:
                print(f"  - {p}", file=sys.stderr)
            return 1
        if a.action == "verify":
            print(f"[sc] ✓ layout 自洽：{len(layout['steps'])} 步 · "
                  f"{len(layout['inspections'])} 检查点")
        else:
            print(json.dumps(layout, ensure_ascii=False, indent=1))
        return 0

    if a.cmd == "link":
        if a.action == "create":
            if not a.step:
                print("[sc] ❌ link create 需要步骤名", file=sys.stderr)
                return 2
            try:
                link = create_link(a.step, functionary=a.functionary, command=a.command,
                                   now=a.now, layout=load_layout(a.layout))
            except ValueError as exc:
                print(f"[sc] ❌ {exc}", file=sys.stderr)
                return 1
            problems = verify_link(link, load_layout(a.layout))
            if problems:
                print(f"[sc] ❌ 生成的 link 未通过自校验：{problems}", file=sys.stderr)
                return 1
            p = write_link(link, a.links_dir)
            print(f"[sc] link 已写 {p.name}（{link['step']} · by {link['functionary']} · "
                  f"materials {len(link['materials'])} · products {len(link['products'])}）")
            return 0
        if not a.step:
            print("[sc] ❌ link verify 需要 link 文件路径", file=sys.stderr)
            return 2
        link = read_link(a.step)
        problems = verify_link(link, load_layout(a.layout))
        if a.json:
            print(json.dumps({"link": link, "problems": problems}, ensure_ascii=False, indent=1))
            return 0 if not problems else 1
        if problems:
            print(f"[sc] ❌ link 未通过（{len(problems)} 项）：", file=sys.stderr)
            for p in problems[:20]:
                print(f"  - {p}", file=sys.stderr)
            return 1
        print(f"[sc] ✓ link 通过：{link['step']} by {link['functionary']} @ {link['timestamp']}")
        return 0

    if a.cmd == "chain":
        problems, notes = chain_verify(links_dir=a.links_dir, layout=load_layout(a.layout),
                                       check_disk=not a.no_disk,
                                       run_inspections=not a.no_inspections)
        for n in notes:
            print(f"[sc] · {n}")
        if problems:
            print(f"[sc] ❌ 链验证失败（{len(problems)} 项）：", file=sys.stderr)
            for p in problems[:20]:
                print(f"  - {p}", file=sys.stderr)
            return 1
        print(f"[sc] ✓ 链验证通过（link 逐条一致 · 顺序/依赖成立"
              f"{'' if a.no_inspections else ' · inspection 全绿'}）")
        return 0

    if a.cmd == "stats":
        st2 = stats(links_dir=a.links_dir, layout=load_layout(a.layout))
        if a.json:
            print(json.dumps(st2, ensure_ascii=False, indent=1))
            return 0
        print(f"[sc] layout {'已就位' if st2['layout'] else '**缺失**'}（{st2['steps']} 步 · "
              f"{st2['inspections']} 检查点）· link **{st2['links']}** 条")
        if st2["links_by_step"]:
            print(f"[sc] 按步骤 {st2['links_by_step']}")
            print(f"[sc] 最后执行 {st2['last_by_step']}")
        if st2["steps_without_link"]:
            print(f"[sc] 尚无 link 的步骤（{len(st2['steps_without_link'])}）："
                  f"{', '.join(st2['steps_without_link'])}")
        print("[sc] 注：**系统绝不自动记录步骤** —— link 只能由显式 `link create` 产生")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
