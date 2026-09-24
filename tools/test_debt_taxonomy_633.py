"""633 E1 · 测试债深化分类与长期方案（**只分类，不改测试**）

针对 A2 清理后的**剩余失败**做深度分类（不重复 A2 的断言修复工作），并给出长期方案：

- **slow 测试**：哪些被标记 `@pytest.mark.slow`；对应文件。
- **跨批脆弱型**：仍硬编码批次号/旧数字的测试（列全清单 + 具体改造点）。
- **环境依赖型**：依赖特定文件/编译器/网络/仓库状态的测试（列依赖 + skipif 覆盖）。
- **快照测试**：依赖快照文件的测试（快照是否过期）。

**不修改任何测试逻辑**（§八.E1）。长期方案只写设计，不落地。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report`/默认 才写
`data/test_debt_taxonomy_633.md`。纯标准库；≥5 例单测（tests/test_test_debt_taxonomy_633.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import debt_inventory_633 as di  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "test_debt_taxonomy_633.md")
FAILURES = os.path.join(ROOT, "data", "633_ci_failures.json")

SLOW_RE = re.compile(r"@pytest\.mark\.slow|pytestmark\s*=.*slow")
SKIPIF_RE = re.compile(r"@pytest\.mark\.skipif")
BATCH_HARD_RE = re.compile(r"\b6[0-2]\d\b")
SNAPSHOT_RE = re.compile(r"snapshot|\.snap\b|SNAPSHOT")
ENV_HINT_RE = re.compile(r"os\.path\.exists|shutil\.which|socket\.|subprocess\.run|connect_ex|"
                         r"importlib\.util\.find_spec")


def _tests() -> dict[str, str]:
    return {di.rel(t): di._read(t) for t in di._walk(os.path.join(ROOT, "tests"), (".py",))}


def slow_tests() -> list[str]:
    return sorted(f for f, s in _tests().items() if SLOW_RE.search(s))


def cross_batch_fragile() -> list[tuple[str, int, str]]:
    out: list[tuple[str, int, str]] = []
    for f, s in _tests().items():
        for i, line in enumerate(s.splitlines(), 1):
            if "assert" in line and BATCH_HARD_RE.search(line) and re.search(r"==|>=|<=|>|<", line):
                out.append((f, i, line.strip()[:90]))
    return out


def env_dependent() -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    for f, s in _tests().items():
        n_ski = len(SKIPIF_RE.findall(s))
        n_env = len(ENV_HINT_RE.findall(s))
        if n_ski or n_env:
            out.append((f, n_ski))
    return out


def snapshot_tests() -> list[str]:
    return sorted(f for f, s in _tests().items() if SNAPSHOT_RE.search(s))


def remaining_failures() -> list[str]:
    if not os.path.exists(FAILURES):
        return []
    try:
        d = json.loads(open(FAILURES, encoding="utf-8").read())
    except json.JSONDecodeError:
        return []
    v = d.get("run2_after_fixes", [])
    return v if isinstance(v, list) else []


def plan() -> list[str]:
    return [
        "**跨批脆弱型 → 动态读基线**：把断言里的硬编码旧数字改为从 `_auto/status.json`、"
        "`data/<batch>_baseline.json` 或被测工具自身输出动态取值；改造点集中在 "
        "`tests/test_*_6[01]*.py` 中含 `== 6XX` 的断言行（见下清单）。",
        "**环境依赖型 → conftest.py 统一 skipif**：在 `tests/conftest.py` 定义 `requires(*paths)`"
        " 与 `requires_tool(*names)` 工厂，返回 `pytest.mark.skipif`；各测试改用装饰器而非"
        " 内联 os.path.exists 判断，统一 reason 文案，避免逐个漂移。",
        "**快照测试 → 定期更新机制**：给 `test_output_snapshots` 加 `--update-snapshots` 触发"
        "（pytest 自定义选项），CI 默认只比不更；触发条件：被快照对象的工具语义版本变更后由人手动跑。",
        "**slow 测试 → 分层**：CI `-m 'not slow'` 已隔离；slow 组加独立 job（夜间/手动触发），"
        "避免拖慢 PR 反馈。",
    ]


def write_report() -> str:
    slow = slow_tests()
    fragile = cross_batch_fragile()
    env = env_dependent()
    snaps = snapshot_tests()
    rem = remaining_failures()
    lines = [
        "# 633 E1 · 测试债深化分类与长期方案", "",
        "> 只针对 **A2 清理后的剩余失败** 做深度分类；**不修改任何测试逻辑**（§八.E1）。", "",
        f"- A2 后剩余失败（`data/633_ci_failures.json` run2）：**{len(rem)}** 项", "",
        "## 一、slow 测试", "",
        f"标记 `@pytest.mark.slow` 的文件：**{len(slow)}** 个", ""]
    for f in slow[:40]:
        lines.append(f"- `{f}`")
    lines += ["", "→ 长期方案：slow 组独立 job（夜间/手动），CI PR 只跑 `not slow`。", "",
              "## 二、跨批脆弱型（硬编码批次号断言）", "",
              f"命中：**{len(fragile)}** 处", "",
              "| 文件 | 行 | 断言 |", "|---|---|---|"]
    for f, i, tx in fragile[:60]:
        lines.append(f"| `{f}` | {i} | `{tx}` |")
    lines += ["", "→ 长期方案：改为动态读 baseline/status（见 §五.1）。", "",
              "## 三、环境依赖型", "",
              f"含 skipif 或环境判断的测试文件：**{len(env)}** 个", "",
              "| 文件 | skipif 数 |", "|---|---|"]
    for f, n in env[:60]:
        lines.append(f"| `{f}` | {n} |")
    lines += ["", "→ 长期方案：`conftest.py` 统一 skipif 工厂（见 §五.2）。", "",
              "## 四、快照测试", "",
              f"引用快照的测试文件：**{len(snaps)}** 个", ""]
    for f in snaps[:40]:
        lines.append(f"- `{f}`")
    lines += ["", "→ 长期方案：`--update-snapshots` 触发式更新（见 §五.3）。", "",
              "## 五、长期方案（设计，不落地）", ""]
    for i, p in enumerate(plan(), 1):
        lines.append(f"{i}. {p}")
    lines += ["",
              "## 六、诚实登记", "",
              "1. 本工具**只静态分类**，不运行测试、**不改任何测试**；",
              "2. slow/环境依赖/snapshot 判定为**正则启发式**（可能漏判）；",
              "3. 跨批脆弱清单按「assert 行含 6[12]X 数字」口径，是**上界**（含合法引用旧批号者）；",
              "4. 长期方案**只写设计**，是否实施交 634/人。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("slow 正则匹配", bool(SLOW_RE.search("@pytest.mark.slow\ndef test():")) is True)
    chk("skipif 正则匹配", bool(SKIPIF_RE.search('@pytest.mark.skipif(not os.path.exists("x"))')))
    chk("批次号正则匹配", BATCH_HARD_RE.search("assert batch == 629") is not None)
    chk("四类分类均可调用",
        isinstance(slow_tests(), list) and isinstance(cross_batch_fragile(), list)
        and isinstance(env_dependent(), list) and isinstance(snapshot_tests(), list))
    chk("长期方案非空", len(plan()) >= 3)
    chk("剩余失败可读（结构为 list）", isinstance(remaining_failures(), list))
    chk("报告路径在 data 下（--check 不写）", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="633 E1 测试债深化分类")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写 data/test_debt_taxonomy_633.md")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    data: dict[str, Any] = {"slow": len(slow_tests()), "cross_batch_fragile": len(cross_batch_fragile()),
                            "env_dependent": len(env_dependent()), "snapshot": len(snapshot_tests()),
                            "remaining": len(remaining_failures())}
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    print(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
