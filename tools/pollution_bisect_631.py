"""631 C1 · ATOM-CONC-FENCE-001 污染根因二分定位（纯标准库）

背景（630 发现）：跑完一次非 slow 全量后，受控文件 `atoms/conc/ATOM-CONC-FENCE-001.md`
的 `id:` 行被删除——这是 **M1「删字段」变异**的残留，即某条沙箱测试**未还原**。
已排除 619/620/621/622 组。本工具：

1. **静态候选**：扫 `tests/` 里疑似会写受控目录的测试（import 沙箱/变异工具、
   或字面量提到该卡）；
2. **真实二分**（`--run-group`，会跑 pytest）：对候选/分组跑测试，跑后查污染标记；
3. **二分逻辑** `bisect()` 是**纯函数**（注入 checker），可用模拟污染做单测；
4. `--check` **只读**（不跑 pytest、不写盘、exit 0）。

**不修复**（§七 C1.4），只定位。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, Callable, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

TARGET = os.path.join("atoms", "conc", "ATOM-CONC-FENCE-001.md")
OUT_MD = os.path.join(ROOT, "data", "pollution_bisect_631.md")
OUT_JSON = os.path.join(ROOT, "data", "pollution_bisect_631.json")

# 疑似会写受控目录的工具（**真正 import** 这些 ⇒ 该测试可能改 atoms/evidence）
# 注意：不能用"文本包含"判定（`gate_engine` 之类常出现在 docstring 里 ⇒ 90 个假阳性）；
# 改为解析 import 语句的模块名。
RISKY_IMPORTS = ("sandbox_apply_622", "mutation_batch_623", "high_complexity_mutator_623",
                 "adversarial_loop_620", "round3_mutator_623", "escape_root_cause_622",
                 "high_complexity_sandbox_run_623")
IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([A-Za-z_]\w*)", re.MULTILINE)


def is_polluted() -> bool:
    """污染标记：目标卡的 frontmatter 里 `id:` 行是否存在（缺失=被 M1 删字段）。"""
    p = os.path.join(ROOT, TARGET)
    if not os.path.exists(p):
        return True
    head = open(p, encoding="utf-8", errors="replace").read()[:400]
    return bool(head) and not re.search(r"^id:\s*\S", head, re.MULTILINE)


def candidate_files() -> list[str]:
    """静态疑似候选：`tests/` 下 import 沙箱/变异工具，或字面量提到目标卡。"""
    d = os.path.join(ROOT, "tests")
    out = []
    for f in sorted(os.listdir(d)):
        if not (f.startswith("test_") and f.endswith(".py")):
            continue
        txt = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
        imported = set(IMPORT_RE.findall(txt))
        risky = bool(imported & set(RISKY_IMPORTS))
        mentions = "ATOM-CONC-FENCE-001" in txt
        if risky or mentions:
            out.append(os.path.join("tests", f))
    return out


# 631 C1 真实执行记录（逐组跑后查污染标记；`polluted=false` 表示该组不含/未触发污染源）
EXECUTED_STEPS: list[dict[str, Any]] = [
    {"group": "623/624 沙箱候选",
     "files": ["tests/test_cross_card_attack_624.py",
               "tests/test_high_complexity_mutator_623.py",
               "tests/test_high_complexity_sandbox_run_623.py"],
     "rc": 0, "polluted": False,
     "note": "24 例全过，跑后 `id:` 行仍在"},
    {"group": "613/588/601 候选",
     "files": ["tests/test_bridge_edge_proposal_613.py",
               "tests/test_mutation_shape_588.py",
               "tests/test_supply_chain_601.py"],
     "rc": 0, "polluted": False,
     "note": "44 例全过，跑后 `id:` 行仍在"},
    {"group": "622 组复核（630 曾排除，本批再验）",
     "files": ["tests/test_622_a1.py", "tests/test_622_a2.py", "tests/test_622_a4.py"],
     "rc": 0, "polluted": False,
     "note": "34 例全过，跑后 `id:` 行仍在"},
    {"group": "631 两次**全量**非 slow 复跑（任务0 采集 + A4 复跑）",
     "files": ["<tests -m not slow>"],
     "rc": None, "polluted": False,
     "note": "两次全量结束受控目录均**零污染**（`git status -- atoms evidence` 空）"},
]


def executed_steps() -> list[dict[str, Any]]:
    """已真实执行过的分组检查（供报告与自检读取）。"""
    return list(EXECUTED_STEPS)


def bisect(items: list[Any], check: Callable[[list[Any]], bool]) -> dict[str, Any]:
    """二分定位：返回**最小可疑集合**与每一步的检查记录。

    纯函数：`check(子集)` 返回"该子集是否含污染源"。做法=每次把当前集合对半，
    先测左半；左半命中则收缩到左半，否则收缩到右半（右半不命中 ⇒ 返回空）。

    **注意边界**：若污染源是**间歇性**的（不是每次跑都复现），二分会给出空集——
    这种情况由 `inconclusive` 标出，不谎报结果。
    """
    steps: list[dict[str, Any]] = []
    cur = list(items)
    while len(cur) > 1:
        mid = len(cur) // 2
        left, right = cur[:mid], cur[mid:]
        hit = bool(check(left))
        steps.append({"size": len(cur), "left_size": len(left),
                      "left_hit": hit})
        cur = left if hit else right
    if not cur:
        return {"found": [], "steps": steps, "inconclusive": True}
    hit = bool(check(cur))
    steps.append({"size": len(cur), "left_size": len(cur), "left_hit": hit})
    return {"found": cur if hit else [], "steps": steps,
            "inconclusive": not hit}


def run_group(files: list[str], timeout: int = 1800) -> dict[str, Any]:
    """真实跑一组测试，跑后查污染标记（**会执行 pytest**，仅供 --run-group）。"""
    if not files:
        return {"ran": 0, "polluted": False}
    p = subprocess.run([sys.executable, "-m", "pytest", *files, "-n0", "-q",
                        "--tb=no"], cwd=ROOT, capture_output=True, text=True,
                       timeout=timeout, check=False)
    tail = (p.stdout or "").strip().splitlines()[-1] if p.stdout else ""
    return {"ran": len(files), "rc": p.returncode, "polluted": is_polluted(),
            "summary": tail[:160]}


def write_report() -> str:
    cands = candidate_files()
    data: dict[str, Any] = {"target": TARGET, "candidates": cands,
                            "currently_polluted": is_polluted(),
                            "steps": [], "found": [], "inconclusive": None}
    if os.path.exists(OUT_JSON):
        try:
            saved = json.load(open(OUT_JSON, encoding="utf-8"))
            data.update({k: saved[k] for k in ("steps", "found", "inconclusive")
                         if k in saved})
        except ValueError:
            pass
    lines = [
        "# 631 C1 · ATOM-CONC-FENCE-001 污染根因二分定位", "",
        f"- 污染目标：`{TARGET}`（M1「删字段」变异残留：`id:` 行缺失）",
        f"- 当前是否已污染：**{data['currently_polluted']}**",
        f"- 静态疑似候选：**{len(cands)}** 个测试文件", "",
        "## 一、静态候选（import 沙箱/变异工具 或 字面量提到该卡）", "",
        "| # | 测试文件 |", "|---|---|",
        *[f"| {i} | `{c}` |" for i, c in enumerate(cands, 1)], "",
        "## 二、二分过程", "",
    ]
    if not data["steps"]:
        lines += ["> 未执行**自动二分**（`bisect()` 需要每次跑组都稳定复现；"
                  "本批实测污染**不可复现**，见 §二 执行记录）。", ""]
    else:
        lines += ["| 步 | 当前集合大小 | 左半大小 | 左半命中 |", "|---|---|---|---|",
                  *[f"| {i} | {s['size']} | {s['left_size']} | {s['left_hit']} |"
                    for i, s in enumerate(data["steps"], 1)], "",
                  f"**定位结果**：{data['found'] or '（未定位到）'} · "
                  f"inconclusive={data['inconclusive']}", ""]
    lines += ["### 真实执行记录（逐组跑后查污染标记）", "",
              "| 组 | 文件 | rc | 污染 | 备注 |", "|---|---|---|---|---|"]
    for s in executed_steps():
        files = "、".join(f"`{f}`" for f in s["files"])
        lines.append(f"| {s['group']} | {files} | {s['rc']} | **{s['polluted']}** |"
                     f" {s['note']} |")
    lines += [
        "", "## 三、结论：未能复现，未定位到具体测试函数（§十二.2 诚实登记）", "",
        "1. **已排除**：619/620/621/622 组（630）、623/624 沙箱候选组、613/588/601 组"
        "（本批逐组实跑），**均不污染**；631 的**两次全量**跑完受控目录也都**零污染**；",
        "2. **因此自动二分不适用**：`bisect()` 依赖「每组跑完都能稳定判定」，"
        "而污染不可复现 ⇒ 二分会在某一步误收缩。工具对此显式返回 `inconclusive`，"
        "不谎报定位结果；",
        "3. **最可能的根因假设（有证据支撑，未证实）**：污染源是一个"
        "「**在沙箱 apply 之后、restore 之前失败**」的测试。依据三条：",
        "   - 污染形态 = M1 删字段，正是沙箱 `plan_edit` 的算子；",
        "   - 630 那次全量里**有 11-14 项测试失败**（其中既有失败会打断用例流程）；",
        "   - 631 A2/A3 修掉 8 项失败后，**两次全量都不再出现污染**。",
        "   若该假设成立，则修法不是「找某个文件」，而是**结构上保证 restore 不被跳过**"
        "（见 C2 防护设计）；",
        "4. 最小范围交付：静态候选 **{n}** 个文件（§一），其中「真正 import 沙箱/变异工具"
        "或 subprocess 驱动它们」的窄集为 `test_622_a1/a2`、`test_622_a4`、"
        "`test_cross_card_attack_624`、`test_high_complexity_mutator_623`、"
        "`test_high_complexity_sandbox_run_623`、`test_bridge_edge_proposal_613`、"
        "`test_mutation_shape_588` —— 逐组实跑**均未复现**。".replace(
            "{n}", str(len(data["candidates"]))), "",
        "## 四、诚实登记", "",
        "- 本工具**不修复**（§七 C1.4）；",
        "- `--check` 只读：不跑 pytest、不写任何文件（除报告由 `--report` 显式生成）；",
        "- 静态候选是**启发式**（按 import 模块名/字面量），可能漏（如动态 import）；",
        "- 根因假设**未证实**：要证实需人为让候选沙箱测试在 apply 后失败并观察残留"
        "（本批不做——那需要有目的地破坏测试，属下一批/C2 验证范畴）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    def mk(items: list[str], polluter: str) -> Callable[[list[str]], bool]:
        return lambda sub: polluter in sub

    # 模拟污染：二分逻辑必须把 8 个候选收缩到唯一的污染源
    items = [f"tests/t{i}.py" for i in range(8)]
    r = bisect(items, mk(items, "tests/t5.py"))
    chk("二分能定位到唯一污染源", r["found"] == ["tests/t5.py"] and not r["inconclusive"],
        f"({r['found']})")
    r0 = bisect(items, mk(items, "tests/t0.py"))
    chk("边界：污染源在首位也能定位", r0["found"] == ["tests/t0.py"])
    r7 = bisect(items, mk(items, "tests/t7.py"))
    chk("边界：污染源在末位也能定位", r7["found"] == ["tests/t7.py"])
    r_none = bisect(items, lambda sub: False)
    chk("间歇性/不复现 ⇒ 显式 inconclusive（不谎报）",
        r_none["found"] == [] and r_none["inconclusive"] is True)
    chk("空集合与单元素集合安全",
        bisect([], lambda s: False)["found"] == []
        and bisect(["a"], lambda s: True)["found"] == ["a"])
    chk("污染标记函数可用（读目标卡 id 行）", isinstance(is_polluted(), bool))
    chk("静态候选非空且都是 tests/ 下的测试文件",
        len(candidate_files()) >= 1
        and all(c.startswith("tests" + os.sep) and c.endswith(".py")
                for c in candidate_files()), f"({len(candidate_files())})")

    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    candidate_files()
    is_polluted()
    chk("只读：不跑 pytest、不改工作区", snap() == before)
    chk("报告存在", os.path.exists(OUT_MD))
    print(f"C1 pollution bisect check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 C1 污染根因二分（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--candidates", action="store_true", help="打印静态候选")
    ap.add_argument("--run-group", nargs="*", metavar="TESTFILE",
                    help="真实跑一组测试并查污染（会执行 pytest）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.candidates:
        print("\n".join(candidate_files()))
        return 0
    if args.run_group is not None:
        files = args.run_group or candidate_files()
        res = run_group(files)
        print(json.dumps(res, ensure_ascii=False))
        return 0
    print(f"candidates={len(candidate_files())} polluted={is_polluted()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
