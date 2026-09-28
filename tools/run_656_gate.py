#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_656_gate.py — 656 收工门禁（核心 PBT/变异/性能 + 前端工程化 + 学习 MVP + 收尾）。

阶段：
1. fast pytest（本批文件）→ 2. full pytest（本批文件）
3. ruff → 4. mypy（本批工具）
5. **核心器械自检**：mutation_test_656 --check（含"放松边界正则必须被杀"的射程自检）
   + core_profile_656 --check
6. **前端工程化**：web_data_pipeline_656 --check（schema / 索引漂移 / **WCAG AA 对比度** / 组件接线 / 卡片契约）
   + web_logic_check_655（Node 真求值）+ web_smoke_655（jsdom DOM；环境缺则 SKIP 计 PASS）
   + teach_card_656 --check（学习卡数据 + 自测题 q/a/source）
7. 保护器联调（queyi-core `protector_rollout_652 --verify`）
8. 受控 atoms 指纹（零污染）→ 9. 信任根 `tool_integrity --check`

用法：python tools/run_656_gate.py [--fast-only] [--web-only]
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
QUEYI = ROOT.parent.parent / "queyi-core"

NEW_TESTS = ["tests/test_core_pbt_656.py", "tests/test_core_boundary_656.py"]
NEW_TOOLS = ["tools/mutation_test_656.py", "tools/core_profile_656.py",
             "tools/web_data_pipeline_656.py", "tools/teach_card_656.py",
             "tools/run_656_gate.py"]
WEB_FILES = ["web/index.html", "web/starmap.html", "web/verify.html", "web/card.html",
             "web/app.js", "web/starmap.js", "web/verify.js", "web/verify_core.js",
             "web/graph_core.js", "web/card.js", "web/style.css",
             "web/css/design-tokens.css", "web/package.json",
             "web/components/index.js", "web/components/qy-nav.js",
             "web/components/qy-card.js", "web/components/qy-panel.js",
             "web/components/qy-button.js", "web/components/qy-tag.js",
             "web/components/qy-status.js",
             "web/data/graph.json", "web/data/manifest.json", "web/data/status.json",
             "web/data/cards_index.json", "web/data/card.json", "web/data/cards.json"]


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


def _check_web_assets() -> bool:
    missing = [f for f in WEB_FILES if not (ROOT / f).is_file()]
    print(f"  文件齐备（{len(WEB_FILES)} 项）：{'PASS' if not missing else 'FAIL ' + str(missing)}")
    return not missing


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="656 收工门禁")
    ap.add_argument("--fast-only", action="store_true")
    ap.add_argument("--web-only", action="store_true")
    a = ap.parse_args(argv)
    py = sys.executable
    res: dict[str, bool] = {}

    if a.web_only:
        print("\n=== 前端工程化（--web-only）===")
        res["web_assets"] = _check_web_assets()
        res["pipeline"] = _run("前端数据管线 --check", [py, "tools/web_data_pipeline_656.py", "--check"])
        node = shutil.which("node")
        if node:
            res["web_logic"] = _run("Node 真求值", [node, "tools/web_logic_check_655.mjs"])
            res["web_smoke"] = _run("jsdom DOM 冒烟", [node, "tools/web_smoke_655.mjs"])
        res["teach"] = _run("学习卡数据 --check",
                            [py, "tools/teach_card_656.py", "--card", "ATOM-CONC-RACE-001", "--check"])
        print("\n===== 656 门禁汇总（web-only）=====")
        for k, v in res.items():
            print(f"  {k:20s}: {'PASS' if v else 'FAIL'}")
        return 0 if all(res.values()) else 1

    res["fast"] = _run("阶段1 fast pytest（本批文件）",
                       [py, "-m", "pytest", *NEW_TESTS, "-q", "-m", "not slow",
                        "-p", "no:cacheprovider"])
    if not a.fast_only:
        res["full"] = _run("阶段2 full pytest（本批文件）",
                           [py, "-m", "pytest", *NEW_TESTS, "-q", "-p", "no:cacheprovider"])
        res["ruff"] = _run("阶段3a ruff", [py, "-m", "ruff", "check", *NEW_TOOLS])
        res["mypy"] = _run("阶段3b mypy", [py, "-m", "mypy", "--ignore-missing-imports",
                                           "--no-error-summary", *NEW_TOOLS])
        res["core_instruments"] = (
            _run("阶段5a 变异器械自检（射程自检）",
                 [py, "tools/mutation_test_656.py", "--check"])
            and _run("阶段5b 性能器械自检",
                     [py, "tools/core_profile_656.py", "--check"])
        )
        print("\n=== 阶段6 前端工程化 ===")
        res["web_assets"] = _check_web_assets()
        res["pipeline"] = _run("阶段6a 数据管线 --check（含 WCAG AA 对比度）",
                               [py, "tools/web_data_pipeline_656.py", "--check"])
        node = shutil.which("node")
        if node:
            res["web_logic"] = _run("阶段6b Node 真求值", [node, "tools/web_logic_check_655.mjs"])
            res["web_smoke"] = _run("阶段6c jsdom DOM 冒烟（缺则 SKIP 计 PASS）",
                                    [node, "tools/web_smoke_655.mjs"])
        else:
            print("  阶段6b/6c：SKIP（无 node）")
        res["teach"] = _run("阶段6d 学习卡数据 + 自测题",
                            [py, "tools/teach_card_656.py", "--card", "ATOM-CONC-RACE-001", "--check"])

        before = _atoms_fp()
        res["protector_integration"] = _run(
            "阶段7 保护器联调 protector_rollout_652 --verify",
            [py, "tools/protector_rollout_652.py", "--verify"], cwd=QUEYI)
        after = _atoms_fp()
        res["zero_pollution"] = before == after
        print(f"\n--- 阶段8 受控 atoms 指纹：{'一致(PASS)' if res['zero_pollution'] else '漂移(FAIL)'}")
        res["trust_root"] = _run("阶段9 信任根 tool_integrity --check",
                                 [py, "tools/tool_integrity.py", "--check"])

    print("\n===== 656 门禁汇总 =====")
    for k, v in res.items():
        print(f"  {k:20s}: {'PASS' if v else 'FAIL'}")
    allok = all(res.values())
    print(f"656 gate: {'PASS' if allok else 'FAIL'}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
