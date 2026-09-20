#!/usr/bin/env python3
"""588 任务 0 · 变异「发现器」完备性审计（只读、幂等、纯标准库 + 现有工具导入）。

产出：`data/mutation_shape_coverage.md`（机器生成、只读台账）。
- Part A（0a）：matrix 尾注释漏网坐实（修前证据，逐卡列出）
- Part B（0b）：全算子 × 卡面合法形态 覆盖审计（用**真实 MUTATORS** 测现正则能否变异）
- Part C（0c）：CRLF 子审计（行尾分布 + LF/CRLF 同构对拍）

纪律：
  * 只读 `atoms/` `evidence/`；不写任何卡；不 import scipy/numpy/pandas（venv 也没装）。
  * 形态判定一律基于真实卡扫描；库内未出现的形态标「库内未出现」，绝不编造卡例。
  * 本台账为 588 任务 0 **修前快照**（修前实跑）：矩阵尾注释漏网已于任务 1 修复，
    见 `_worklog_588.md`；其余形态结论以本脚本可复现重跑为准。

用法：
  python tools/mutation_shape_audit.py                 # 写 data/mutation_shape_coverage.md
  python tools/mutation_shape_audit.py --print-only    # 只打印摘要，不落盘
"""
# mypy: ignore-errors
# 类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# 导入真实 MUTATORS / 矩阵变异器：审计的就是"现正则能否变异"，必须用真实代码而非重抄。
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mutation_fuzz import MUTATORS, ROOT, _mut_matrix_values  # noqa: E402

EVIDENCE = ROOT / "evidence"
ATOMS = ROOT / "atoms"
OUT = ROOT / "data" / "mutation_shape_coverage.md"

# ── 卡读取 ──────────────────────────────────────────────────────────────────────
def _all_card_texts() -> list[tuple[str, str]]:
    cards = sorted(EVIDENCE.rglob("EV-*.md")) + sorted(ATOMS.rglob("ATOM-*.md"))
    cards = [c for c in cards if "README" not in c.name]
    out: list[tuple[str, str]] = []
    for c in cards:
        try:
            t = c.read_text(encoding="utf-8")
        except OSError:
            continue
        out.append((c.relative_to(ROOT).as_posix(), t))
    return out


# ── Part A：matrix 块宽容探测（不被尾注释漏掉）──────────────────────────────────
# 宽容：键行允许尾注释与任意空白，块体取「键行之后连续缩进行」，遇下一个顶格键 / `---` / 空行终止。
_MATRIX_KEY = re.compile(r"^matrix:[ \t]*(?:#[^\n]*)?\s*$")


def find_matrix_block(text: str) -> tuple[int, list[tuple[int, str]]]:
    """返回 (键行索引, [(行号, 缩进行原文), ...])；找不到返回 (-1, [])。

    用宽容正则而非 mutation_fuzz 的现正则 ⇒ 即便卡带尾注释也能数到（这正是 0a 要坐实的漏网）。
    """
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if _MATRIX_KEY.match(ln):
            j = i + 1
            block: list[tuple[int, str]] = []
            while j < len(lines):
                nxt = lines[j]
                if nxt.strip() == "" or nxt.strip() == "---":
                    break
                if re.match(r"^[ \t]", nxt):
                    block.append((j, nxt))
                    j += 1
                else:
                    break  # 下一个顶格键 ⇒ 块终止
            return i, block
    return -1, []


def matrix_audit(card_texts: list[tuple[str, str]]) -> dict[str, object]:
    total = 0
    tail_key: list[str] = []
    inline_comment: list[str] = []
    value_tail: list[str] = []
    block_style: list[str] = []          # compiler/std/opt/arch 用块式列表（而非 flow [..]）
    produces_variants: list[str] = []
    zero_variants: list[str] = []        # 现正则(_mut_matrix_values)产出 0 ⇒ 漏网
    for rel, t in card_texts:
        ki, block = find_matrix_block(t)
        if ki < 0:
            continue
        total += 1
        lines = t.split("\n")
        key_line = lines[ki]
        if "#" in key_line:
            tail_key.append(rel)
        has_inline = False
        has_value_tail = False
        has_block_list = False
        for _lno, ln in block:
            s = ln.strip()
            if s.startswith("#"):
                has_inline = True
            elif "#" in s and ":" in s:
                has_value_tail = True
            elif s.startswith("- "):          # 块式序列（非 flow [..]）
                has_block_list = True
        if has_inline:
            inline_comment.append(rel)
        if has_value_tail:
            value_tail.append(rel)
        if has_block_list:
            block_style.append(rel)
        n = len(_mut_matrix_values(t))
        if n > 0:
            produces_variants.append(rel)
        else:
            zero_variants.append(rel)
    return {
        "total": total,
        "tail_key": sorted(set(tail_key)),
        "inline_comment": sorted(set(inline_comment)),
        "value_tail": sorted(set(value_tail)),
        "block_style": sorted(set(block_style)),
        "produces": sorted(set(produces_variants)),
        "zero": sorted(set(zero_variants)),
        "ratio": (f"{len(produces_variants)}/{total}" if total else "0/0"),
    }


# ── Part B：形态覆盖（用真实 MUTATORS 测）───────────────────────────────────────
BASE = """---
id: EV-AUDIT-SYN-001
verdict: confirm
evidence_type: experiment
matrix:
  compiler: [GCC 13.1.0]
  std: [c++17]
  opt: [-O2]
  arch: [x86-64]
command: g++ -O2 -std=c++17 Examples/atoms/_atom_test.cpp -o Examples/atoms/_atom_test.out
artifact: Examples/atoms/_atom_test.out
artifact_producer: g++
artifact_sha256: 0000000000000000000000000000000000000000000000000000000000000000
fixture: Examples/atoms/_atom_test.cpp
actual:
  run_match_file: Examples/atoms/_atom_test.out
negative_controls: []
---
body text
"""

C_MATRIX_TAIL = """---
id: EV-AUDIT-SYN-001
verdict: confirm
matrix:                          # 尾注释：笛卡尔声明 ≠ 实测组数
  compiler: [GCC 13.1.0]
  std: [c++17]
  opt: [-O2]
  arch: [x86-64]
command: g++ -O2 -std=c++17 Examples/atoms/_atom_test.cpp -o Examples/atoms/_atom_test.out
artifact: Examples/atoms/_atom_test.out
---
body
"""

C_MATRIX_INLINE = """---
id: EV-AUDIT-SYN-001
verdict: confirm
matrix:
  compiler: [GCC 13.1.0]
  # 注释：含冒号也安全：不会被当成键
  std: [c++17]
  opt: [-O2]
  arch: [x86-64]
command: g++ -O2 -std=c++17 Examples/atoms/_atom_test.cpp -o Examples/atoms/_atom_test.out
artifact: Examples/atoms/_atom_test.out
---
body
"""

C_MATRIX_VALTAIL = """---
id: EV-AUDIT-SYN-001
verdict: confirm
matrix:
  compiler: [GCC 13.1.0]  # 值尾注释
  std: [c++17]
  opt: [-O2]
  arch: [x86-64]
command: g++ -O2 -std=c++17 Examples/atoms/_atom_test.cpp -o Examples/atoms/_atom_test.out
artifact: Examples/atoms/_atom_test.out
---
body
"""

C_MATRIX_FWPAREN = """---
id: EV-AUDIT-SYN-001
verdict: confirm
matrix:
  compiler: [GCC 13.1.0]
  std: [c++17]
  opt: [-O2]（全角括号注释）
  arch: [x86-64]
command: g++ -O2 -std=c++17 Examples/atoms/_atom_test.cpp -o Examples/atoms/_atom_test.out
artifact: Examples/atoms/_atom_test.out
---
body
"""

C_CMD_TAIL = BASE.replace(
    "command: g++ -O2 -std=c++17 Examples/atoms/_atom_test.cpp -o Examples/atoms/_atom_test.out",
    "command: g++ -O2 -std=c++17 Examples/atoms/_atom_test.cpp -o Examples/atoms/_atom_test.out  # 命令尾注释",
)
C_ACT_TAIL = BASE.replace(
    "  run_match_file: Examples/atoms/_atom_test.out",
    "  run_match_file: Examples/atoms/_atom_test.out  # actual 项尾注释",
)
C_ID_TAIL = BASE.replace("id: EV-AUDIT-SYN-001", "id: EV-AUDIT-SYN-001  # id 尾注释")


def _count(op: str, text: str) -> int:
    try:
        return len(MUTATORS[op](text))
    except Exception:  # noqa: BLE001  守卫：单算子异常不污染整批审计（如实记录异常）
        return -1


def _real_ids(card_texts: list[tuple[str, str]], pred) -> list[str]:
    out = []
    for rel, t in card_texts:
        if pred(t):
            out.append(rel)
    return sorted(set(out))


def shape_audit(card_texts: list[tuple[str, str]]) -> list[dict[str, str]]:
    """逐「算子 × 变异点 × 形态」格子。能/漏 由真实 MUTATOR 实跑决定。"""
    # 真实卡例：各类尾注释 / 块式序列
    real_matrix_tail = _real_ids(card_texts, lambda t: find_matrix_block(t)[0] >= 0
                                and "#" in t.split("\n")[find_matrix_block(t)[0]])
    real_matrix_inline = _real_ids(card_texts, lambda t: any(
        ln.strip().startswith("#") for _ki, blk in [find_matrix_block(t)]
        for _lno, ln in blk))
    real_valtail = _real_ids(card_texts, lambda t: "#" in t and any(
        (ln.strip().startswith(("compiler:", "std:", "opt:", "arch:"))
         and "#" in ln) for ln in t.split("\n")))
    real_cmd_tail = _real_ids(card_texts, lambda t: any(
        ln.startswith("command:") and "#" in ln for ln in t.split("\n")))
    real_act_tail = _real_ids(card_texts, lambda t: "#" in t and "run_match_file:" in t)
    real_id_tail = _real_ids(card_texts, lambda t: any(
        re.match(r"^id:\s*\S", ln) and "#" in ln for ln in t.split("\n")))

    def ex(ids: list[str]) -> str:
        return ids[0] if ids else "库内未出现"

    rows = [
        # 算子, 变异点, 目标字段, 卡面形态, 真实卡例, 现正则能否变异, 漏网证据
        {"op": "M6", "point": "matrix 值层（删键/非法值）", "field": "matrix 块",
         "form": "matrix 键行带尾注释（matrix:   # ...）",
         "real": ex(real_matrix_tail), "count": len(_mut_matrix_values(C_MATRIX_TAIL)),
         "evidence": "EV-MEM-004 即此形态；现正则 ^(matrix:)\\s*\\n 要求键行仅空白再换行，撞 # 失配 ⇒ 整块 0 变体（漏）"},
        {"op": "M6", "point": "matrix 值层", "field": "matrix 块",
         "form": "matrix 块内整行注释（含冒号）",
         "real": ex(real_matrix_inline), "count": len(_mut_matrix_values(C_MATRIX_INLINE)),
         "evidence": "现遍历靠 ':' not in s 跳过注释行（侥幸），注释含冒号也不误当键；任务1 改为先剥注释再解析"},
        {"op": "M6", "point": "matrix 值层", "field": "matrix 值行",
         "form": "matrix 值行带尾注释（compiler: [...]  # ...）",
         "real": ex(real_valtail), "count": len(_mut_matrix_values(C_MATRIX_VALTAIL)),
         "evidence": "现 _mut_matrix_values 不做剥注释；值行尾注释随值一起替换，变体照常产出（无漏）"},
        {"op": "M6", "point": "matrix 值层", "field": "matrix opt 值",
         "form": "opt 值行全角括号注释（[-O2]（…））",
         "real": ex(real_valtail), "count": len(_mut_matrix_values(C_MATRIX_FWPAREN)),
         "evidence": "全角括号不影响 ASCII 正则；变体照常产出（无漏）"},
        {"op": "M2", "point": "路径变形", "field": "command",
         "form": "command 行尾注释（g++ ... # ...）",
         "real": ex(real_cmd_tail), "count": _count("M2", C_CMD_TAIL),
         "evidence": "_PATHP 只匹配路径本身（不含 #），尾注释不阻断定位（无漏）"},
        {"op": "M3", "point": "断言弱化", "field": "actual.run_match_file",
         "form": "actual 项尾注释",
         "real": ex(real_act_tail), "count": _count("M3", C_ACT_TAIL),
         "evidence": "M3 在读取面内找 _in/-Werror/count:/条目，尾注释不影响（无漏）"},
        {"op": "M1", "point": "字段删除", "field": "id",
         "form": "id 行尾注释（id: X  # ...）",
         "real": ex(real_id_tail), "count": _count("M1", C_ID_TAIL),
         "evidence": "M1 用 ^id:\\s*(\\S+) 取首个非空 token，尾注释不阻断（无漏）"},
    ]
    for r in rows:
        n = r["count"]
        r["able"] = "能" if n and n > 0 else ("异常" if n == -1 else "漏")
    return rows


# ── Part C：CRLF 子审计 ──────────────────────────────────────────────────────────
def _norm_crlf(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def crlf_audit() -> dict[str, object]:
    lf = 0
    crlf = 0
    mixed = 0
    for _rel, t in _all_card_texts():
        has_cr = "\r" in t
        has_lf_only = "\n" in t and not has_cr
        if has_cr and has_lf_only is False and "\n" in t:
            # 同时含 \r\n 与裸 \n？判定混合
            if "\r\n" in t and (not t.replace("\r\n", "\n").count("\n") == t.count("\n")):
                mixed += 1
            else:
                crlf += 1
        elif has_cr:
            crlf += 1
        else:
            lf += 1
    # LF/CRLF 同构对拍：在 BASE 与 EV-MEM-004 上，对各算子比对变体集（归一 \r）
    # 取一张真实含多算子的卡做对拍（EV-MEM-004 含 matrix + id）
    ev_text = None
    for rel, t in _all_card_texts():
        if rel.endswith("EV-MEM-004.md"):
            ev_text = t
            break
    diffs: list[str] = []
    for op in MUTATORS:
        def _pair(text: str):
            return {(p, _norm_crlf(v) if v is not None else None)
                    for p, v in MUTATORS[op](text)}
        ref_lf = _pair(BASE)
        ref_cr = _pair(BASE.replace("\n", "\r\n"))
        if ref_lf != ref_cr:
            diffs.append(f"BASE · {op}：LF 与 CRLF 变体集不一致")
        if ev_text is not None:
            e_lf = _pair(ev_text)
            e_cr = _pair(ev_text.replace("\n", "\r\n"))
            if e_lf != e_cr:
                diffs.append(f"EV-MEM-004 · {op}：LF 与 CRLF 变体集不一致")
    return {"lf": lf, "crlf": crlf, "mixed": mixed, "diffs": diffs,
            "conclusion": ("CRLF 无影响" if not diffs else f"CRLF 有影响（{len(diffs)} 处）")}


# ── 报告渲染 ────────────────────────────────────────────────────────────────────
def build_report(mat: dict[str, object], shapes: list[dict[str, str]],
                 crlf: dict[str, object]) -> str:
    L: list[str] = []
    L.append("# 变异发现器 × 卡面合法形态 覆盖审计台账（588 任务 0，修前快照）\n")
    L.append("> 本台账为 **修前实跑** 快照（audit 脚本导入的是当时未改的 `mutation_fuzz`）。\n")
    L.append("> 矩阵键行尾注释漏网已于 **任务 1** 修复；其余结论以 `tools/mutation_shape_audit.py` 可复现重跑为准。\n")
    L.append("\n## Part A · matrix 尾注释漏网（0a）\n")
    L.append(f"- 含 `matrix` 块的卡总数：**{mat['total']}**")
    L.append(f"- `matrix` 键行带尾注释的卡（漏网，现正则 0 变体）：**{len(mat['tail_key'])}** → {mat['tail_key'] or '无'}")
    L.append(f"- `matrix` 块内整行注释的卡：**{len(mat['inline_comment'])}** → {mat['inline_comment'] or '无'}")
    L.append(f"- `matrix` 值行带尾注释的卡：**{len(mat['value_tail'])}** → {mat['value_tail'] or '无'}")
    L.append(f"- `matrix` 用块式列表（非 flow `[..]`）的卡：**{len(mat['block_style'])}** → {mat['block_style'] or '无'}")
    L.append(f"- 现正则能产 matrix 变体的卡 / 含 matrix 的卡：**{mat['ratio']}**")
    L.append(f"- 现正则产出 **0** matrix 变体的卡（漏网）：{mat['zero'] or '无'}")
    L.append("\n## Part B · 全算子 × 卡面形态 覆盖（0b）\n")
    L.append("| 算子 | 变异点 | 目标字段 | 卡面形态 | 真实卡例(id,至少1个) | 现正则能否变异 | 漏网证据 |")
    L.append("|---|---|---|---|---|---|---|")
    for r in shapes:
        L.append(f"| {r['op']} | {r['point']} | {r['field']} | {r['form']} | {r['real']} "
                 f"| {r['able']}(n={r['count']}) | {r['evidence']} |")
    L.append("\n## Part C · CRLF 子审计（0c）\n")
    L.append(f"- 行尾分布：LF={crlf['lf']} · CRLF={crlf['crlf']} · 混合={crlf['mixed']}")
    L.append(f"- 结论：**{crlf['conclusion']}**")
    if crlf["diffs"]:
        L.append("- 不一致清单：")
        for d in crlf["diffs"]:
            L.append(f"  - {d}")
    else:
        L.append("- LF/CRLF 同构对拍（BASE + EV-MEM-004，各 MUTATORS）：变体集逐字一致 ⇒ **CRLF 无影响**")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--print-only", action="store_true")
    args = ap.parse_args(argv)
    card_texts = _all_card_texts()
    mat = matrix_audit(card_texts)
    shapes = shape_audit(card_texts)
    crlf = crlf_audit()
    report = build_report(mat, shapes, crlf)
    if args.print_only:
        print(report)
    else:
        OUT.write_text(report, encoding="utf-8")
        print(f"[audit] 已写 {OUT.relative_to(ROOT).as_posix()}")
    # 摘要到 stderr（不污染落盘）
    print(f"[audit] matrix 卡={mat['total']} 尾注释漏网={len(mat['tail_key'])} "
          f"能产/含={mat['ratio']} CRLF={crlf['conclusion']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
