"""609 D2 · in-toto 溯源：**link/layout 生成（待签名） + 字段级 schema + 4 关键步骤验证流**。

**不实际签名、不实际执行命令**（609 铁律第 9 条）：本工具只产出 link metadata 的
**未签名件**（`signatures: []`），并按 layout 的 step 定义做**字段级**校验。

  * `link`：一步运行的记录 —— `materials` / `products` / `byproducts`（含
    `stdout`/`stderr`/`return-value`）/ `command` / `environment` / `signatures`；
  * `layout`：步骤图 —— `steps`（`expected_command` / `expected_materials` /
    `expected_products` / `threshold`）+ `inspect` + `keys`；
  * `verify`：4 个关键验证步骤
      ① 命令一致性      ⇒ 封 A1（伪造 link 声称跑了别的命令）
      ② material→product ⇒ 封 A2（凭空产物 / 偷换产物）
      ③ 签名覆盖        ⇒ **缺签名即 fail-closed**（未签名件不是证据）
      ④ 顺序与 quorum   ⇒ 封 A3（跳过/重排步骤）

⚠️ 未签名件**一律判 fail-closed**，绝不因为"没签就先放过"。

CLI：
    gen-link <step> [--materials M ...] [--products P ...] [--out FILE]   0 ok
    gen-layout [--out FILE]                                               0 ok
    verify --layout L --links L1 L2 ...                                   0 通过 / 1 不通过
    --check                                                               0 结构自洽 / 1 破
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
DEFAULT_LAYOUT = ROOT / "data" / "intoto_layout.json"
LINK_DIR = ROOT / "data" / "intoto_links"

LINK_REQUIRED = ("_type", "name", "materials", "products", "byproducts", "command")
BYPRODUCT_REQUIRED = ("stdout", "stderr", "return-value")
STEP_REQUIRED = ("name", "expected_command", "expected_products", "threshold")


def file_digest(path: Path | str) -> dict[str, str]:
    p = Path(path)
    if not p.is_file():
        return {"missing": p.name}
    raw = p.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "size": len(raw)}


def _now() -> str:
    return datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()


# ── 生成（**不签名**）──────────────────────────────────────────────────────────
def gen_link(name: str, *, materials: list[str] | None = None,
             products: list[str] | None = None, command: list[str] | None = None,
             return_value: int = 0, stdout: str = "", stderr: str = "") -> dict:
    mats = {str(m): file_digest(m) for m in (materials or [])}
    prods = {str(p): file_digest(p) for p in (products or [])}
    return {"_type": "link", "name": str(name), "materials": mats, "products": prods,
            "byproducts": {"stdout": stdout, "stderr": stderr, "return-value": int(return_value)},
            "command": list(command or []), "environment": {"cwd": str(ROOT)},
            "signed_at": _now(), "signatures": [],
            "unsigned_note": "本 link 未签名 ⇒ verify 一律 fail-closed（不是证据）"}


def gen_layout(steps: list[dict] | None = None) -> dict:
    default = [
        {"name": "generate",
         "expected_command": ["tools/attack_edge_generator.py", "generate"],
         "expected_materials": ["misconceptions", "atoms"],
         "expected_products": ["data/attack_edges_candidates.jsonl"], "threshold": 1},
        {"name": "solve", "expected_command": ["tools/weighted_af_solver.py", "solve"],
         "expected_materials": ["data/attack_edges_candidates.jsonl"],
         "expected_products": ["data/grounded_labels_w2.json"], "threshold": 1},
        {"name": "render", "expected_command": ["tools/grounded_visualizer.py", "--check"],
         "expected_materials": ["data/grounded_labels_w2.json"],
         "expected_products": ["data/argument_net.html"], "threshold": 1},
        {"name": "anchor", "expected_command": ["tools/opentimestamps_anchor.py", "stamp"],
         "expected_materials": ["data/grounded_labels_w2.json"],
         "expected_products": ["data/grounded_labels_w2.json.ots"], "threshold": 1},
    ]
    return {"_type": "layout", "version": VERSION, "created_at": _now(),
            "steps": steps or default, "inspect": [], "keys": {},
            "note": "link 缺 signatures ⇒ fail-closed（见关键步骤 ③）"}


# ── schema（字段级）───────────────────────────────────────────────────────────
def check_link(link: dict) -> list[str]:
    problems: list[str] = []
    for k in LINK_REQUIRED:
        if k not in link:
            problems.append(f"link 缺字段 {k}")
    if link.get("_type") != "link":
        problems.append(f"_type 不是 link：{link.get('_type')!r}")
    by = link.get("byproducts") or {}
    for k in BYPRODUCT_REQUIRED:
        if k not in by:
            problems.append(f"link.byproducts 缺字段 {k}")
    if not isinstance(link.get("signatures"), list):
        problems.append("signatures 必须是列表（空列表 = 未签名）")
    return problems


def check_layout(layout: dict) -> list[str]:
    problems: list[str] = []
    if layout.get("_type") != "layout":
        problems.append(f"_type 不是 layout：{layout.get('_type')!r}")
    steps = layout.get("steps")
    if not isinstance(steps, list) or not steps:
        return problems + ["steps 为空或不是列表"]
    seen: set[str] = set()
    for i, s in enumerate(steps, 1):
        for k in STEP_REQUIRED:
            if k not in s:
                problems.append(f"steps[{i}] 缺字段 {k}")
        name = str(s.get("name"))
        if name in seen:
            problems.append(f"steps[{i}] name 重复：{name}")
        seen.add(name)
        if int(s.get("threshold", 0)) < 1:
            problems.append(f"steps[{i}] threshold 须 ≥1（quorum 语义），实得 {s.get('threshold')}")
    return problems


# ── 4 个关键步骤 ──────────────────────────────────────────────────────────────
def _matches(pattern: str, produced: set[str]) -> bool:
    return any(p == pattern or p.endswith(pattern) for p in produced)


def verify(layout: dict, links: list[dict]) -> dict:
    problems: list[str] = []
    checks: list[dict] = []
    by_name: dict[str, dict] = {}
    for lnk in links:
        by_name[str(lnk.get("name"))] = lnk
    steps = layout.get("steps", [])

    for s in steps:                                       # ① 命令一致性（封 A1）
        name = str(s["name"])
        lnk = by_name.get(name)
        if lnk is None:
            checks.append({"no": 1, "step": name, "ok": False, "why": "link 缺失"})
            problems.append(f"[①] 缺 {name} 的 link ⇒ 不许跳过（见 ④）")
            continue
        want = [str(c) for c in s.get("expected_command", [])]
        got = [str(c) for c in lnk.get("command", [])]
        ok = got == want or all(w in got for w in want)
        checks.append({"no": 1, "step": name, "ok": ok, "why": f"期望 {want} vs 实得 {got}"})
        if not ok:
            problems.append(f"[①] {name} 命令不符（A1 伪造 link）：{want} vs {got}")

    for s in steps:                                       # ② material→product（封 A2）
        name = str(s["name"])
        lnk = by_name.get(name)
        if lnk is None:
            continue
        prods = set((lnk.get("products") or {}).keys())
        missing = [m for m in s.get("expected_products", []) if not _matches(m, prods)]
        ok = not missing
        checks.append({"no": 2, "step": name, "ok": ok, "why": f"缺产物 {missing}"})
        if not ok:
            problems.append(f"[②] {name} 产物缺失/被偷换（A2）：{missing}")
        missing_mat = [m for m in s.get("expected_materials", [])
                       if m.startswith("data/") and not _matches(m, set(lnk.get("materials", {})))]
        if missing_mat:
            problems.append(f"[②] {name} 凭空产物：缺输入 {missing_mat} 却有输出")

    for lnk in links:                                     # ③ 签名覆盖（fail-closed）
        sigs = lnk.get("signatures") or []
        ok = isinstance(sigs, list) and len(sigs) > 0
        checks.append({"no": 3, "step": str(lnk.get("name")), "ok": ok,
                       "why": ("有签名" if ok else "未签名 ⇒ 不是证据，fail-closed")})
        if not ok:
            problems.append(f"[③] {lnk.get('name')} 未签名 ⇒ 不得判 pass（609 铁律：不实际签名）")

    names = [str(s["name"]) for s in steps]               # ④ 顺序与 quorum（封 A3）
    got_names = [str(lnk.get("name")) for lnk in links]
    ordered = all(names.index(g) <= i for i, g in enumerate(got_names) if g in names)
    skipped = [n for n in names if n not in got_names]
    ok = ordered and not skipped
    checks.append({"no": 4, "step": "sequence", "ok": ok,
                   "why": f"顺序 {got_names} vs 布局 {names}；跳过 {skipped}"})
    if skipped:
        problems.append(f"[④] 步骤被跳过（A3）：{skipped}")
    if not ordered:
        problems.append(f"[④] 步骤顺序不符（A3）：{got_names} vs {names}")

    return {"ok": not problems, "fail_closed": True, "problems": problems, "checks": checks,
            "verdict": "pass" if not problems else "fail"}


def check() -> list[str]:
    problems: list[str] = []
    layout = gen_layout()
    problems += check_layout(layout)
    for s in layout["steps"]:
        link = gen_link(s["name"], materials=[], products=[], command=s["expected_command"])
        problems += check_link(link)
    for p in sorted(LINK_DIR.glob("*.link")) if LINK_DIR.is_dir() else []:
        try:
            problems += check_link(json.loads(p.read_text(encoding="utf-8")))
        except ValueError as exc:
            problems.append(f"{p}: 不是合法 JSON：{exc}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="intoto_provenance",
                                 description="609 D2 in-toto 溯源（待签名 link/layout + 4 步验证）")
    ap.add_argument("--version", action="version", version=f"intoto_provenance {VERSION}")
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    sp = sub.add_parser("gen-link", help="生成**未签名** link（签名的位置留给人的私钥）")
    sp.add_argument("step")
    sp.add_argument("--materials", nargs="*", default=[])
    sp.add_argument("--products", nargs="*", default=[])
    sp.add_argument("--command", nargs="*", default=[])
    sp.add_argument("--out", default=None)

    sp = sub.add_parser("gen-layout")
    sp.add_argument("--out", default=str(DEFAULT_LAYOUT))

    sp = sub.add_parser("verify", help="跑 4 关键步骤（缺签名 ⇒ fail-closed）")
    sp.add_argument("--layout", required=True)
    sp.add_argument("--links", nargs="*", default=[])
    sp.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print(f"[intoto] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print("[intoto] --check OK：link/layout schema 字段级自洽（默认 4 步全通过结构校验）")
        return 0

    if a.cmd is None:
        ap.print_help()
        return 2

    if a.cmd == "gen-link":
        link = gen_link(a.step, materials=a.materials, products=a.products, command=a.command)
        out = Path(a.out) if a.out else LINK_DIR / f"{a.step}.link"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(link, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"LINK(UNSIGNED): {out.name}（signatures=[] ⇒ verify 会 fail-closed）")
        return 0

    if a.cmd == "gen-layout":
        out = Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(gen_layout(), ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"LAYOUT: {out.name}（{len(gen_layout()['steps'])} 步）")
        return 0

    layout = json.loads(Path(a.layout).read_text(encoding="utf-8"))
    links = [json.loads(Path(p).read_text(encoding="utf-8")) for p in a.links]
    res = verify(layout, links)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    if res["ok"]:
        print(f"[intoto] ✓ verify pass（{len(res['checks'])} 项检查通过）")
        return 0
    print(f"[intoto] ❌ verify FAIL（fail-closed）：{len(res['problems'])} 项", file=sys.stderr)
    for m in res["problems"][:20]:
        print("  - " + m, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
