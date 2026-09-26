"""647 A3 · **信任根闭包扩展**（641 的 23 文件闭包 → 覆盖全部"能改判决"的面）。

现状（647 §一）：641 D 线的闭包（`verifier_closure_641`）只跟 `tools/*.py` 的 import 图 +
3 个配置信任根 glob + `data/supply_chain/*`，**不覆盖**：

| 面 | 为什么必须进闭包 | 647 补法 |
|---|---|---|
| **67 条规则** | 规则内嵌在 `gate_engine.py`（无独立规则文件）⇒ 规则改一行判决就变 | 记 `gate_engine.py` sha256 **+ 规则集指纹**（`sorted(rule_id)` 的 sha256，含条数） |
| **Authority schema** | `authority_schema_v2_626` / `decision_event_v2_626` 决定「一条人审事件是否算数」 | 沿 import 图纳入 + 显式列两个模块 |
| **透明日志 anchor** | 账本 anchor 落在这里；改它 = 改"历史是否可证" | 纳入 `data/transparency_log.jsonl` |
| **tool_integrity 基线** | 「什么算被改过」由 `tools/.tool_checksums` 定义 | 纳入（641 已含，647 再做**一致性交叉校验**） |
| **证据库索引** | 证据检索面（646 A4） | 纳入 `data/evidence_index.json` |
| **高复杂度 block 规则 yaml** | 623 E2 的 4 条 block 规则（独立文件） | 纳入 `data/gate_rules_high_complexity_block_623.yaml` |

设计原则（**不破坏历史**）：**新增文件、不修改 `verifier_closure_641.py`** ——
641 的 `closure_digest` 已经绑进 `VerificationRun.digests`，改它会让历史 run 的 digest 对不上。

- 缺失即 **FAIL**（不是 warning）：`status=FAIL` + `missing` 点名（`--simulate-missing` 可做攻击测试，
  **不真删任何文件**）。
- **与 tool_integrity 一致性**：闭包里 5 个 CORE_TOOLS 的 sha256 必须与 `.tool_checksums` core 节
  逐字相同；5 个信任根数据文件必须与 supply_chain 节逐字相同（不一致 ⇒ `consistent=False`）。

CLI：`--check`（只读自检）/ `--report`（写 `data/647_verifier_closure.md` + `.json`）/ `--json` /
`--simulate-missing a,b`。纯标准库。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Any, Iterable, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import calibration_tracker_636 as ruleset  # noqa: E402  （67 规则 id 单一真源，不复制）
import queyi_core_v10_641 as core  # noqa: E402  （digest/import 图复用）
import tool_integrity as ti  # noqa: E402      （一致性交叉校验）
import verifier_closure_641 as base  # noqa: E402  （641 闭包，**只读复用不改**）

OUT_MD = os.path.join(ROOT, "data", "647_verifier_closure.md")
OUT_JSON = os.path.join(ROOT, "data", "647_verifier_closure.json")

#: 647 新增进闭包的**显式**信任根（相对 repo 根）
EXTRA_FILES: tuple[str, ...] = (
    "tools/authority_schema_v2_626.py",                       # Authority schema
    "tools/decision_event_v2_626.py",                         # 事件结构与哈希口径
    "tools/verifier_closure_641.py",                          # 641 闭包实现本身
    "data/gate_rules_high_complexity_block_623.yaml",          # 4 条高复杂度 block 规则（独立文件）
    "data/transparency_log.jsonl",                            # 透明日志（anchor 载体）
    "data/evidence_index.json",                               # 证据库索引（646 A4）
) + tuple(ti.SUPPLY_CHAIN_FILES)   # tool_integrity 的 5 个信任根数据文件（一致性交叉校验的基准面）
#: 沿 import 图**额外**展开的起点（schema/事件层）
EXTRA_ROOTS: tuple[str, ...] = ("authority_schema_v2_626", "decision_event_v2_626")
#: 规则集指纹的**合成条目名**（不是磁盘文件，是"规则内容"的指纹）
RULESET_ID = "RULESET#gate_engine"


def _rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def _sha256_file(path: str) -> Optional[str]:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def rule_ids() -> list[str]:
    """67 条在册规则 id（gate_engine 单一真源，经 636 读取）。"""
    return sorted(r["id"] for r in ruleset.rules())


def ruleset_fingerprint() -> str:
    """规则集指纹 = sha256(sorted(rule_id) 拼接) —— 规则**增删改 id** 都会变。"""
    payload = "\n".join(rule_ids())
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def closure_files() -> list[str]:
    """647 全闭包：641 闭包 ∪ EXTRA_FILES ∪ (schema/事件层的 import 图)。排序去重。"""
    files: set[str] = set(base.closure_files())
    files |= set(EXTRA_FILES)
    stack = list(EXTRA_ROOTS)
    seen: set[str] = set()
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        p = base.module_path(name)
        if not p:
            continue
        files.add(_rel(p))
        for dep in core.module_imports(p):
            if dep not in seen and base.module_path(dep):
                stack.append(dep)
    return sorted(files)


def build_closure(missing: Iterable[str] = ()) -> dict[str, Any]:
    """构建全闭包。`missing` = 假装缺失的相对路径（**攻击测试用，不真删**）⇒ status=FAIL。"""
    miss = set(missing)
    entries: list[dict[str, str]] = []
    missing_list: list[str] = []
    for rel in closure_files():
        if rel in miss:
            missing_list.append(rel)
            continue
        d = _sha256_file(os.path.join(ROOT, rel))
        if d is None:
            missing_list.append(rel)
            continue
        entries.append({"path": rel, "sha256": d})
    # 规则集指纹（合成条目：不是文件，是"规则内容"的可比指纹）
    if RULESET_ID in miss:
        missing_list.append(RULESET_ID)
    else:
        entries.append({"path": RULESET_ID, "sha256": ruleset_fingerprint(),
                        "n_rules": str(len(rule_ids()))})  # type: ignore[dict-item]
    entries.sort(key=lambda e: e["path"])
    missing_list.sort()
    return {"schema": "verifier_closure/1.1-647",
            "status": "FAIL" if missing_list else "OK",
            "n_files": len(entries), "n_missing": len(missing_list),
            "missing": missing_list, "files": entries,
            "digest": core.digest_of(entries),
            "n_rules": len(rule_ids())}


def closure_digest() -> str:
    return str(build_closure()["digest"])


def consistency_with_tool_integrity(cl: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """**与 tool_integrity 一致**：闭包里 CORE_TOOLS / 信任根数据文件的 sha256 必须与基线逐字相同。

    不一致的四种来路都被点名：① 文件被改未重钉；② 基线缺该节；③ 闭包漏了该文件；④ 基线没钉该文件。
    """
    cl = cl or build_closure()
    got = {e["path"]: e["sha256"] for e in cl["files"]}
    core_base = ti.load_baseline() or {}
    sc_base = ti.load_supply_chain_baseline() or {}
    mismatches: list[dict[str, str]] = []
    for name, want in sorted(core_base.items()):
        rel = f"tools/{name}"
        if rel not in got:
            mismatches.append({"path": rel, "why": "闭包未覆盖该 CORE_TOOL"})
        elif got[rel] != want:
            mismatches.append({"path": rel, "why": f"sha256 与 core 节不一致（{got[rel][:12]}≠{want[:12]}）"})
    for name, want in sorted(sc_base.items()):
        if name not in got:
            mismatches.append({"path": name, "why": "闭包未覆盖该信任根数据文件"})
        elif got[name] != want:
            mismatches.append({"path": name, "why": f"sha256 与 supply_chain 节不一致（{got[name][:12]}≠{want[:12]}）"})
    covered = [n for n in ti.CORE_TOOLS if f"tools/{n}" in got]
    return {"consistent": not mismatches, "mismatches": mismatches,
            "core_tools_in_closure": len(covered), "core_tools_total": len(ti.CORE_TOOLS),
            "supply_chain_pinned": len(sc_base)}


def attack_missing_trust_root() -> dict[str, Any]:
    """攻击测试：假装删掉一个 CORE_TOOL 与一个信任根数据文件 ⇒ 必须 FAIL 并点名（不真删）。"""
    targets = ["tools/gate_engine.py", ti.SUPPLY_CHAIN_FILES[0]]
    r = build_closure(missing=targets)
    return {"targets": targets, "status": r["status"], "missing": r["missing"],
            "digest_changed": r["digest"] != closure_digest()}


def write_report(cl: Optional[dict[str, Any]] = None) -> str:
    cl = cl or build_closure()
    cons = consistency_with_tool_integrity(cl)
    att = attack_missing_trust_root()
    lines = [
        "# 647 A3 · 信任根闭包扩展（641 的 23 文件 → 全覆盖）", "",
        f"- 状态：**{cl['status']}** · 闭包文件 **{cl['n_files']}** 个（含规则集指纹）· 缺失 **{cl['n_missing']}**",
        f"- 规则数：**{cl['n_rules']}**；规则集指纹：`{ruleset_fingerprint()}`",
        f"- closure_digest（647 版）：`{cl['digest']}`",
        f"- 与 tool_integrity 一致：**{cons['consistent']}**"
        f"（CORE_TOOLS 覆盖 {cons['core_tools_in_closure']}/{cons['core_tools_total']}，"
        f"信任根数据 {cons['supply_chain_pinned']} 个已钉）", "",
        "## 一、相比 641 新增覆盖的面", "",
        "| 面 | 载体 | 为什么必须进闭包 |", "|---|---|---|",
        "| 67 条规则 | `gate_engine.py` + **规则集指纹** | 规则内嵌，改规则=改判决 |",
        "| Authority schema | `authority_schema_v2_626.py` / `decision_event_v2_626.py` | 决定「一条人审是否算数」 |",
        "| 透明日志 anchor | `data/transparency_log.jsonl` | 改了它 = 改「历史是否可证」 |",
        "| 基线自身 | `tools/.tool_checksums` | 「什么算被改过」的定义 |",
        "| 证据库索引 | `data/evidence_index.json` | 证据检索面 |",
        "| block 规则 yaml | `data/gate_rules_high_complexity_block_623.yaml` | 623 E2 的 4 条独立 block 规则 |", "",
        "## 二、缺失即 FAIL（不是 warning）", "",
        "```",
        f"attack（假装缺 {att['targets']}） ⇒ status={att['status']}",
        f"missing={att['missing']}",
        f"digest 改变：{att['digest_changed']}",
        "```", "",
        "**不真删任何文件**：`missing` 只是「假装磁盘上没有」，用于证明判定会 FAIL。", "",
        "## 三、与 tool_integrity 一致性（交叉校验）", "",
    ]
    if cons["consistent"]:
        lines.append("- ✅ 闭包内 5 个 CORE_TOOLS + 5 个信任根数据文件的 sha256 **与 `.tool_checksums` 逐字相同**。")
    else:
        lines.append("- ❌ 不一致项：")
        for m in cons["mismatches"]:
            lines.append(f"  - `{m['path']}`：{m['why']}")
    lines += ["", "## 四、闭包清单（每个文件的 sha256）", "",
              "| # | 文件 | sha256（前 16） |", "|---|---|---|"]
    for i, e in enumerate(cl["files"], 1):
        lines.append(f"| {i} | `{e['path']}` | `{e['sha256'][:16]}…` |")
    lines += ["", "## 诚实登记", "",
              "1. **闭包仍跟不到 site-packages**：第三方依赖以 `pyproject.toml` 声明进闭包，"
              "不递归进依赖树（同 641 口径）；",
              "2. **规则集指纹只覆盖规则 id**：规则**正文**改动由 `gate_engine.py` 的 sha256 覆盖，"
              "两者必须一起看（id 不变、正文变 ⇒ 只有 gate_engine 的 sha256 会变）；",
              "3. **未修改 `verifier_closure_641.py`**：641 的 digest 已绑进历史 run，改它会让历史对不上 ⇒ "
              "647 以**新文件**扩展（代价：两个闭包并存，交人裁决是否收编）；",
              "4. **闭包的「完整性」仍是相对的**：本机信任根未外移（外部 KMS/第三方签名留 A4 + 交人）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"closure": cl, "consistency": cons, "attack": att,
                   "ruleset_fingerprint": ruleset_fingerprint()},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    cl = build_closure()
    paths = [e["path"] for e in cl["files"]]
    chk("闭包状态 OK（真实仓库无缺失）", cl["status"] == "OK", str(cl["missing"]))
    chk("闭包 ≥ 641 的规模", cl["n_files"] > 30, str(cl["n_files"]))
    for t in ti.CORE_TOOLS:
        chk(f"含 CORE_TOOL {t}", f"tools/{t}" in paths, "" if f"tools/{t}" in paths else "缺失")
    for rel in EXTRA_FILES:
        chk(f"含新增信任根 {rel}", rel in paths, "" if rel in paths else "缺失")
    chk("含规则集指纹条目", RULESET_ID in paths)
    chk("规则集 67 条", cl["n_rules"] == 67, str(cl["n_rules"]))
    chk("digest 确定性", build_closure()["digest"] == cl["digest"])
    chk("sha256 长度 64", all(len(e["sha256"]) == 64 for e in cl["files"]))

    att = attack_missing_trust_root()
    chk("攻击：假删信任根 ⇒ FAIL", att["status"] == "FAIL")
    chk("攻击：点名缺失文件", att["missing"] == sorted(att["targets"]), str(att["missing"]))
    chk("攻击：digest 改变", att["digest_changed"] is True)

    cons = consistency_with_tool_integrity(cl)
    chk("与 tool_integrity 一致", cons["consistent"] is True, str(cons["mismatches"]))
    chk("CORE_TOOLS 全进闭包", cons["core_tools_in_closure"] == cons["core_tools_total"])
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"A3 closure selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 A3 信任根闭包扩展")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告 + JSON")
    ap.add_argument("--json", action="store_true", help="打印闭包（JSON）")
    ap.add_argument("--simulate-missing", default="", help="假装缺失（逗号分隔），验证缺失即 FAIL")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.simulate_missing:
        rels = [x.strip() for x in a.simulate_missing.split(",") if x.strip()]
        r = build_closure(missing=rels)
        print(json.dumps({"status": r["status"], "missing": r["missing"]}, ensure_ascii=False))
        return 0 if r["status"] == "FAIL" else 1
    cl = build_closure()
    if a.report:
        print(f"written {write_report(cl)}（{cl['status']}，{cl['n_files']} 条目）")
        return 0 if cl["status"] == "OK" else 1
    if a.json:
        print(json.dumps({k: v for k, v in cl.items() if k != "files"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[647 closure] status={cl['status']} n={cl['n_files']} rules={cl['n_rules']} "
          f"digest={cl['digest'][:16]}…")
    return 0 if cl["status"] == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
