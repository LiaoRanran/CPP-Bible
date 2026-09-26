"""641 E1 · 收工门禁

八项检查：
1. 641 新工具 `--check` 全绿（内核 / C++ 插件 / toy 插件 / 闭包）
2. 整目录 ruff（tools/ + tests/）全绿
3. mypy tools/ = 0 errors
4. 受控目录（atoms/evidence/Examples/Book）零污染
5. 内核**零领域 import**（AST 机械证明，§四.2）
6. C++ 对账：内核编排的 run 与 legacy 规则清单/W2 一致，run 自校验通过
7. 通用性：C++ 与 toy 两个 run 的 `kernel_digest` **相同**（内核零改动跨领域）
8. 信任根闭包：状态 OK + **缺失即 FAIL**（攻击测试）

铁律：不跑监工门禁；`--check` 只读（除报告外不写任何文件）。
产物：`--report` 写 `data/641_gate_result.md`。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import queyi_core_v10_641 as core  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "641_gate_result.md")
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
CONTROLLED = ("atoms", "evidence", "Examples", "Book")

#: 本批 641 新工具（均带 --check）
NEW_TOOLS = ("queyi_core_v10_641", "queyi_core_cpp_641",
             "queyi_core_toy_641", "verifier_closure_641")


def _run(args: list[str], timeout: int = 600) -> tuple[int, str]:
    try:
        p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, f"{type(exc).__name__}: {exc}"


def check_new_tools() -> dict[str, Any]:
    bad = []
    for name in NEW_TOOLS:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), "--check"])
        if rc != 0:
            bad.append(f"{name}: {out[-200:]}")
    return {"ok": not bad, "n_tools": len(NEW_TOOLS), "detail": "; ".join(bad) or f"{len(NEW_TOOLS)}/{len(NEW_TOOLS)} --check 绿"}


def check_ruff() -> dict[str, Any]:
    rc, out = _run([PY, "-m", "ruff", "check", "tools/", "tests/"])
    return {"ok": rc == 0, "detail": out.splitlines()[-1] if out else ""}


def check_mypy() -> dict[str, Any]:
    rc, out = _run([PY, "-m", "mypy", "tools/"], timeout=900)
    n = out.count(": error:")
    return {"ok": rc == 0 and n == 0, "detail": f"{n} errors"}


def check_controlled() -> dict[str, Any]:
    rc, out = _run(["git", "diff", "--quiet", "--", *CONTROLLED])
    return {"ok": rc == 0, "detail": out or "受控目录零改动"}


def check_kernel_purity() -> dict[str, Any]:
    hits = core.verify_no_domain_imports(os.path.join(HERE, "queyi_core_v10_641.py"))
    return {"ok": hits == [], "detail": f"领域 import：{hits or '零'}"}


def check_cpp_reconcile() -> dict[str, Any]:
    try:
        import queyi_core_cpp_641 as cpp
        run = cpp.run_verification()
        rec = cpp.reconcile(run)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "detail": f"{type(exc).__name__}: {exc}"}
    by = {r["metric"]: r for r in rec["rows"]}
    ok = (run.verify_integrity()
          and by["规则条数"]["kernel"] == by["规则条数"]["legacy"]
          and by["规则 ID 集合"]["kernel"] == "same"
          and by["W2 节点数"]["kernel"] == by["W2 节点数"]["legacy"])
    return {"ok": bool(ok), "detail": f"run={run.run_id[:12]}… 差异 {rec['n_diff']} 项"
            f"（规则/W2 口径一致={ok}）", "n_diff": rec["n_diff"]}


def check_generality() -> dict[str, Any]:
    try:
        import queyi_core_cpp_641 as cpp
        import queyi_core_toy_641 as toy
        kr = cpp.run_verification(limit=5).digests.get("kernel_digest", "")
        tr = toy.run_verification().digests.get("kernel_digest", "")
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "detail": f"{type(exc).__name__}: {exc}"}
    ok = bool(kr) and kr == tr == core.kernel_self_digest()
    return {"ok": ok, "detail": f"cpp={kr[:12]}… toy={tr[:12]}… 相同={ok}"}


def check_closure() -> dict[str, Any]:
    try:
        import verifier_closure_641 as vc
        cl = vc.build_closure()
        att = vc.simulate_missing(["pyproject.toml"])
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "detail": f"{type(exc).__name__}: {exc}"}
    ok = cl["status"] == "OK" and att["status"] == "FAIL"
    return {"ok": ok, "detail": f"闭包 {cl['n_files']} 文件 status={cl['status']}；"
                                f"缺失攻击 ⇒ {att['status']}"}


def build() -> dict[str, Any]:
    checks = {
        "641 新工具 --check": check_new_tools(),
        "ruff 全绿": check_ruff(),
        "mypy 0 errors": check_mypy(),
        "受控目录零污染": check_controlled(),
        "内核零领域 import（AST）": check_kernel_purity(),
        "C++ 端到端对账": check_cpp_reconcile(),
        "通用性（kernel_digest 两域相同）": check_generality(),
        "信任根闭包（缺失即 FAIL）": check_closure(),
    }
    return {"checks": checks, "all_ok": all(v["ok"] for v in checks.values())}


def write_report(r: dict[str, Any]) -> str:
    c = r["checks"]
    lines = ["# 641 E1 · 收工门禁结果", "",
             "| # | 检查 | 结果 | 详情 |", "|---|---|---|---|"]
    for i, (k, v) in enumerate(c.items(), 1):
        lines.append(f"| {i} | {k} | {'✅' if v['ok'] else '❌'} | {v['detail']} |")
    lines += ["", f"**总判定**：{'全部通过 ✅' if r['all_ok'] else '存在未过项 ❌'}"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="641 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写门禁结果报告")
    a = ap.parse_args(argv)
    r = build()
    for k, v in r["checks"].items():
        print(f"  [{'ok' if v['ok'] else 'FAIL'}] {k} — {v['detail']}")
    print(f"E1 gate: {'PASS' if r['all_ok'] else 'FAIL'}")
    if a.report:
        print(f"written {write_report(r)}")
    return 0 if r["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
