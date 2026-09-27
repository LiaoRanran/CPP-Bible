#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_653_gate.py — 653 收工门禁（两阶段 pytest + ruff/mypy + 保护器联调 + 前端产物 + 信任根 + 零污染）。

阶段：
1. fast pytest（-m 'not slow'）→ 2. full pytest
3. ruff / mypy（653 文件）→ 4. web_data_653 --check
5. **前端产物**：web/ 文件齐备 + graph.json/manifest.json 可解析 + JS 语法（node --check，若有 node）
6. **保护器联调**：queyi-core `protector_rollout_652 --verify`（B7-B10 四保护器真上岗）
7. 受控 atoms 指纹（零污染）→ 8. 信任根 `tool_integrity --check`

用法：python tools/run_653_gate.py [--fast-only]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
QUEYI = ROOT.parent.parent / "queyi-core"

NEW_TESTS = ["tests/test_653_tools.py", "tests/test_652_tools.py", "tests/test_core_pbt_651.py"]
NEW_TOOLS = ["tools/web_data_653.py", "tools/run_653_gate.py"]
WEB_FILES = ["web/index.html", "web/starmap.html", "web/verify.html", "web/app.js",
             "web/starmap.js", "web/verify.js", "web/style.css",
             "web/data/graph.json", "web/data/manifest.json"]


def _run(label: str, cmd: list[str], cwd: Path = ROOT) -> bool:
    print(f"\n=== {label} ===\n$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(cwd), check=False)
    print(f"--- {label}: {'PASS' if r.returncode == 0 else 'FAIL'} (exit={r.returncode})")
    return r.returncode == 0


def _atoms_fp() -> str:
    h = hashlib.sha256()
    for p in sorted((ROOT / "atoms").rglob("*.md")):
        h.update(str(p.relative_to(ROOT)).encode())
        h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def _check_web() -> bool:
    ok = True
    missing = [f for f in WEB_FILES if not (ROOT / f).is_file()]
    print(f"  文件齐备：{'PASS' if not missing else 'FAIL ' + str(missing)}")
    ok = ok and not missing
    for f in ("web/data/graph.json", "web/data/manifest.json"):
        try:
            json.loads((ROOT / f).read_text(encoding="utf-8"))
            print(f"  {f} 可解析：PASS")
        except Exception as e:  # noqa: BLE001
            print(f"  {f} 可解析：FAIL {e}")
            ok = False
    jss = [f for f in WEB_FILES if f.endswith(".js")]
    node = _node_path()
    if node:
        import tempfile
        for f in jss:
            with tempfile.TemporaryDirectory() as td:
                dst = Path(td) / (Path(f).stem + ".mjs")
                dst.write_text((ROOT / f).read_text(encoding="utf-8"), encoding="utf-8")
                r = subprocess.run([node, "--check", str(dst)], check=False,
                                   capture_output=True, text=True)
                print(f"  JS 语法 {f}：{'PASS' if r.returncode == 0 else 'FAIL ' + r.stderr[:80]}")
                ok = ok and r.returncode == 0
    else:
        print("  JS 语法：SKIP（无 node）")
    return ok


def _node_path() -> str | None:
    import shutil
    return shutil.which("node")


def _has_node() -> bool:
    return _node_path() is not None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="653 收工门禁")
    ap.add_argument("--fast-only", action="store_true")
    a = ap.parse_args(argv)
    py = sys.executable
    res: dict[str, bool] = {}

    res["fast"] = _run("阶段1 fast pytest(-m 'not slow')",
                       [py, "-m", "pytest", *NEW_TESTS, "-q", "-m", "not slow", "-p", "no:cacheprovider"])
    if not a.fast_only:
        res["full"] = _run("阶段2 full pytest",
                           [py, "-m", "pytest", *NEW_TESTS, "-q", "-p", "no:cacheprovider"])
        res["ruff"] = _run("阶段3a ruff（653 文件）", [py, "-m", "ruff", "check", *NEW_TOOLS])
        res["mypy"] = _run("阶段3b mypy（653 文件）",
                           [py, "-m", "mypy", "--ignore-missing-imports", "--no-error-summary", *NEW_TOOLS])
        res["web_data_selftest"] = _run("阶段4 web_data_653 --check", [py, "tools/web_data_653.py", "--check"])
        print("\n=== 阶段5 前端产物 ===")
        res["web_assets"] = _check_web()

        before = _atoms_fp()
        res["protector_integration"] = _run(
            "阶段6 保护器联调 queyi-core protector_rollout_652 --verify",
            [py, "tools/protector_rollout_652.py", "--verify"], cwd=QUEYI)
        after = _atoms_fp()
        res["zero_pollution"] = before == after
        print(f"\n--- 阶段7 受控 atoms 指纹: before={before[:16]} after={after[:16]} "
              f"{'一致(PASS)' if res['zero_pollution'] else '漂移(FAIL)'}")
        res["trust_root"] = _run("阶段8 信任根 tool_integrity --check",
                                 [py, "tools/tool_integrity.py", "--check"])

    print("\n===== 653 门禁汇总 =====")
    for k, v in res.items():
        print(f"  {k:22s}: {'PASS' if v else 'FAIL'}")
    allok = all(res.values())
    print(f"653 gate: {'PASS' if allok else 'FAIL'}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
