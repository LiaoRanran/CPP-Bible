#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_655_gate.py — 655 收工门禁（两阶段 pytest + ruff/mypy + 许可证头 + 前端产物 +
门禁三杠杆自检 + 保护器联调 + 受控零污染 + 信任根）。

阶段：
1. fast pytest（本批文件，`-m "not slow"`）→ 2. full pytest（本批文件）
3. ruff（本批文件）→ 4. mypy（本批新工具）
5. **许可证头** `license_header_check_655 --check`（active 口径必须 0 缺）
6. **前端产物**：文件齐备 + JSON 可解析 + status.json 字段完备 + JS 语法（node，含 index.html 内联模块）
7. **门禁三杠杆**：test_selector / result_cache / pytest_shard 三个 `--check` + 缓存 `--verify`
8. **保护器联调**：queyi-core `protector_rollout_652 --verify`
9. 受控 atoms 指纹（零污染）→ 10. 信任根 `tool_integrity --check`

用法：python tools/run_655_gate.py [--fast-only] [--web-only]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
QUEYI = ROOT.parent.parent / "queyi-core"

NEW_TESTS = ["tests/test_655_tools.py", "tests/test_verdict_spec_v1_655.py"]
NEW_TOOLS = ["tools/license_header_check_655.py", "tools/test_selector_655.py",
             "tools/result_cache_655.py", "tools/pytest_shard_655.py",
             "tools/web_status_655.py", "tools/run_655_gate.py"]
WEB_FILES = ["web/index.html", "web/starmap.html", "web/verify.html", "web/app.js",
             "web/starmap.js", "web/verify.js", "web/verify_core.js", "web/graph_core.js",
             "web/style.css", "web/package.json",
             "web/data/graph.json", "web/data/manifest.json", "web/data/status.json"]
STATUS_KEYS = ("cards", "rules", "protectors", "escape", "w2", "generated_from", "unavailable")


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


def _inline_module(html: str) -> str | None:
    m = re.search(r'<script type="module">(.*?)</script>', html, re.DOTALL)
    return m.group(1) if m else None


def _check_web() -> bool:
    ok = True
    missing = [f for f in WEB_FILES if not (ROOT / f).is_file()]
    print(f"  文件齐备：{'PASS' if not missing else 'FAIL ' + str(missing)}")
    ok = ok and not missing

    for f in ("web/data/graph.json", "web/data/manifest.json", "web/data/status.json"):
        try:
            json.loads((ROOT / f).read_text(encoding="utf-8"))
            print(f"  {f} 可解析：PASS")
        except Exception as e:  # noqa: BLE001
            print(f"  {f} 可解析：FAIL {e}")
            ok = False

    try:
        st = json.loads((ROOT / "web/data/status.json").read_text(encoding="utf-8"))
        miss = [k for k in STATUS_KEYS if k not in st]
        cards_ok = int((st.get("cards") or {}).get("cards_real", 0)) > 0
        print(f"  status.json 字段：{'PASS' if not miss else 'FAIL ' + str(miss)}"
              f"（cards_real={cards_ok}）")
        ok = ok and not miss and cards_ok
    except Exception as e:  # noqa: BLE001
        print(f"  status.json 字段：FAIL {e}")
        ok = False

    node = shutil.which("node")
    if not node:
        print("  JS 语法：SKIP（无 node）")
        return ok
    jobs: list[tuple[str, str]] = []
    for f in [x for x in WEB_FILES if x.endswith(".js")]:
        jobs.append((f, (ROOT / f).read_text(encoding="utf-8")))
    inline = _inline_module((ROOT / "web/index.html").read_text(encoding="utf-8"))
    if inline:
        jobs.append(("web/index.html#inline", inline))
    for name, src in jobs:
        with tempfile.TemporaryDirectory() as td:
            base = name.split("/")[-1].split("#")[0].replace(".js", "")
            dst = Path(td) / (base + ".mjs")
            dst.write_text(src, encoding="utf-8")
            r = subprocess.run([node, "--check", str(dst)], check=False, capture_output=True, text=True)
            print(f"  JS 语法 {name}：{'PASS' if r.returncode == 0 else 'FAIL ' + r.stderr[:100]}")
            ok = ok and r.returncode == 0
    return ok


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="655 收工门禁")
    ap.add_argument("--fast-only", action="store_true")
    ap.add_argument("--web-only", action="store_true", help="只跑前端检查（调试用）")
    a = ap.parse_args(argv)
    py = sys.executable
    res: dict[str, bool] = {}

    if a.web_only:
        print("\n=== 前端产物检查（--web-only）===")
        res["web_assets"] = _check_web()
        print("\n===== 655 门禁汇总（web-only）=====")
        for k, v in res.items():
            print(f"  {k:22s}: {'PASS' if v else 'FAIL'}")
        return 0 if all(res.values()) else 1

    res["fast"] = _run("阶段1 fast pytest（本批文件）",
                       [py, "-m", "pytest", *NEW_TESTS, "-q", "-m", "not slow",
                        "-p", "no:cacheprovider"])
    if not a.fast_only:
        res["full"] = _run("阶段2 full pytest（本批文件）",
                           [py, "-m", "pytest", *NEW_TESTS, "-q", "-p", "no:cacheprovider"])
        res["ruff"] = _run("阶段3a ruff（本批文件）", [py, "-m", "ruff", "check", *NEW_TOOLS])
        res["mypy"] = _run("阶段3b mypy（本批新工具）",
                           [py, "-m", "mypy", "--ignore-missing-imports",
                            "--no-error-summary", *NEW_TOOLS])
        res["license_header"] = _run("阶段5 许可证头检查（active 口径）",
                                     [py, "tools/license_header_check_655.py", "--check"])
        print("\n=== 阶段6 前端产物 ===")
        res["web_assets"] = _check_web()
        node = shutil.which("node")
        if node:
            res["web_logic"] = _run("阶段6b 前端逻辑真求值（Node，无需 jsdom）",
                                    [node, "tools/web_logic_check_655.mjs"])
            res["web_smoke"] = _run("阶段6c 前端 DOM 冒烟（jsdom；环境缺则 SKIP 计 PASS）",
                                    [node, "tools/web_smoke_655.mjs"])
        else:
            print("  阶段6b/6c：SKIP（无 node）")
        res["lever_selftest"] = (_run("阶段7a 选择器自检",
                                      [py, "tools/test_selector_655.py", "--check"])
                                 and _run("阶段7b 结果缓存自检",
                                          [py, "tools/result_cache_655.py", "--check"])
                                 and _run("阶段7c 分片自检",
                                          [py, "tools/pytest_shard_655.py", "--check"]))
        res["cache_verify"] = _run("阶段7d 缓存条目体检（重算依赖哈希）",
                                   [py, "tools/result_cache_655.py", "--verify"])

        before = _atoms_fp()
        res["protector_integration"] = _run(
            "阶段8 保护器联调 queyi-core protector_rollout_652 --verify",
            [py, "tools/protector_rollout_652.py", "--verify"], cwd=QUEYI)
        after = _atoms_fp()
        res["zero_pollution"] = before == after
        print(f"\n--- 阶段9 受控 atoms 指纹: before={before[:16]} after={after[:16]} "
              f"{'一致(PASS)' if res['zero_pollution'] else '漂移(FAIL)'}")
        res["trust_root"] = _run("阶段10 信任根 tool_integrity --check",
                                 [py, "tools/tool_integrity.py", "--check"])

    print("\n===== 655 门禁汇总 =====")
    for k, v in res.items():
        print(f"  {k:22s}: {'PASS' if v else 'FAIL'}")
    allok = all(res.values())
    print(f"655 gate: {'PASS' if allok else 'FAIL'}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
