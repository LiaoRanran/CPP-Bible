"""634 A2 · 给 79 个无 --check 的老工具批量补只读 `--check`

范式（承 633 B2）：在工具**主逻辑之前**插入一个拦截守卫——

```python
if "--check" in sys.argv:
    print("OK: <name> --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)
```

放在 `if __name__ == "__main__":` **之前** ⇒ 跑 `tool --check` 时：先执行全部**顶层代码**
（import / 常量 / 函数定义）⇒ 这一步**真在校验"工具能否无错加载"**，然后命中守卫、
**exit 0、不进入业务逻辑、不写盘**。

- 幂等：已含 `--check` 的跳过；
- 需 `import sys`：缺失则在文件头补一行；
- 无 `__main__` 守卫的纯库/无 main 者 → 登记为例外（不强行加）。

**只读契约**：`--check` 只做自检、exit 0、不写盘。纯标准库；≥5 例单测
（tests/test_add_check_batch_634.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import tool_debt_audit_633 as tda  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "add_check_batch_634.md")
_MAIN_RE = re.compile(r"^if\s+__name__\s*==\s*['\"]__main__['\"]\s*:", re.MULTILINE)


def _tool_path(loc: str) -> str:
    return os.path.join(ROOT, loc)


def all_targets() -> list[str]:
    """无 --check 的 CLI 老工具（相对路径，升序）。"""
    try:
        items = tda.categorize()["no_check_cli"]
    except Exception:  # noqa: BLE001
        items = []
    return sorted(it["loc"] for it in items)


def groups(n: int = 4) -> list[list[str]]:
    t = all_targets()
    if not t:
        return [[]]
    size = (len(t) + n - 1) // n
    return [t[i:i + size] for i in range(0, len(t), size)]


def _guard(name: str) -> str:
    return ("\n\nif \"--check\" in sys.argv:\n"
            f"    print(\"OK: {name} --check（只读：加载即校验，不执行任何业务逻辑）\")\n"
            "    sys.exit(0)\n")


def add_check(loc: str) -> str:
    """给单个工具加 --check 守卫。返回 'added' / 'skip' / 'no_main'。"""
    p = _tool_path(loc)
    src = open(p, encoding="utf-8", errors="replace").read()
    if '"--check"' in src or "'--check'" in src:
        return "skip"
    m = _MAIN_RE.search(src)
    if not m:
        return "no_main"          # 无 __main__ 守卫 ⇒ 登记为例外，不强行加
    new = src
    if not re.search(r"^\s*import sys\b", src, re.MULTILINE):
        # `from __future__` 必须最靠前 ⇒ 有则插其**之后**，否则插首个 import 之前
        fut = list(re.finditer(r"^from __future__ import .*$", new, re.MULTILINE))
        if fut:
            pos = fut[-1].end()
            new = new[:pos] + "\nimport sys" + new[pos:]
        else:
            im = re.search(r"^(import |from )", new, re.MULTILINE)
            if im:
                new = new[:im.start()] + "import sys\n" + new[im.start():]
            else:
                new = "import sys\n" + new
    m2 = _MAIN_RE.search(new)
    guard = _guard(os.path.basename(loc)[:-3])
    new = new[:m2.start()].rstrip("\n") + guard + "\n" + new[m2.start():]
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(new)
    return "added"


def apply_group(idx: int) -> dict[str, list[str]]:
    gs = groups()
    res: dict[str, list[str]] = {"added": [], "skip": [], "no_main": []}
    if not (0 <= idx < len(gs)):
        return res
    for loc in gs[idx]:
        res[add_check(loc)].append(loc)
    return res


def verify(tools: list[str]) -> dict[str, Any]:
    ok = bad = 0
    bad_list = []
    for loc in tools:
        p = _tool_path(loc)
        r = subprocess.run([sys.executable, p, "--check"], cwd=ROOT,
                           capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            ok += 1
        else:
            bad += 1
            bad_list.append(loc)
    return {"ok": ok, "bad": bad, "bad_list": bad_list[:20]}


def write_report() -> str:
    t = all_targets()
    frozen = os.path.join(ROOT, "data", "add_check_targets_634.json")
    if not t and os.path.exists(frozen):
        t = json.loads(open(frozen, encoding="utf-8").read()).get("targets", [])
    gs = groups() if len(t) == len(all_targets()) else [t[i:i + 20] for i in range(0, len(t), 20)]
    rows = []
    for i, g in enumerate(gs):
        rows.append(f"| {i} | {len(g)} | {', '.join(os.path.basename(x) for x in g[:3])} … |")
    lines = ["# 634 A2 · 79 个无 --check 老工具批补", "",
             f"- 目标工具数：**{len(t)}**（来自 633 B2 登记口径，复算）",
             f"- 分组：**{len(gs)}** 组（每组 ~{len(gs[0]) if gs and gs[0] else 0}）", "",
             "| 组 | 数量 | 示例 |", "|---|---|---|", *rows, "",
             "## 守卫范式", "",
             "```python", _guard("<name>").strip(), "```", "",
             "## 诚实登记", "",
             "1. `--check` 语义为「**加载即校验**」：跑工具时先执行全部顶层代码（import/常量/",
             "   函数定义），能无错到达守卫 ⇒ 证明工具可加载；**不跑业务逻辑、不写盘**；",
             "2. **无 `__main__` 守卫**的工具（纯库/无 CLI）→ 登记例外，不强行加；",
             "3. 守卫在**顶层**拦截，对以 `import` 方式调用该工具的测试无影响（仅 `__main__` 时生效）；",
             "4. 本批**只加守卫**，不改任何业务逻辑（§零.5）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    t = all_targets()
    gs = groups()
    chk("目标列表可读（打完可为 0）", isinstance(t, list))
    chk("分组覆盖全部目标", sum(len(g) for g in gs) == len(t))
    chk("守卫文本含 --check", "--check" in _guard("x") and "sys.exit(0)" in _guard("x"))
    chk("无 __main__ 时返回 no_main",
        _MAIN_RE.search("import os\nprint(1)\n") is None)
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="634 A2 批量补 --check")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--apply", action="store_true", help="对 --group 指定的组打补丁")
    ap.add_argument("--group", type=int, default=0)
    ap.add_argument("--verify", action="store_true", help="校验目标工具的 --check")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.apply:
        print(json.dumps(apply_group(args.group), ensure_ascii=False, indent=2))
        return 0
    if args.verify:
        print(json.dumps(verify(all_targets()), ensure_ascii=False, indent=2))
        return 0
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.json:
        print(json.dumps({"targets": len(all_targets()), "groups": [len(g) for g in groups()]},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"targets={len(all_targets())} groups={[len(g) for g in groups()]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
