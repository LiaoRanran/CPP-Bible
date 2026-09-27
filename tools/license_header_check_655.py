#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""license_header_check_655.py — Apache-2.0 许可证头检查 / 批量补齐（655 A）。

背景（655 A 开源准备）
======================
本仓库 655 从 MIT 切换到 **Apache-2.0**。Apache-2.0 第 4(c) 条要求再分发时
**保留版权与许可声明**，因此源码文件需要可见的许可证头。本工具把这件事变成
可跑、可判、可幂等补齐的机器检查，而不是靠人记。

头的规范形态（追加在 shebang / coding 行之后，不动正文）
======================================================
``# SPDX-License-Identifier: Apache-2.0``
``# Copyright 2026 LiaoRanran (阿信)``

作用域（重要：本工具**默认只强制活跃源码**）
============================================
- ``active``（默认，``--check`` 判红的口径）：``tools/`` ``tests/`` ``web/`` ``Scripts/``
  以及根 ``conftest.py`` —— 即"会被 CI / 发布 / 用户直接执行"的代码；
- ``all``：仓库内**全部被 git 跟踪**的 ``.py``（含 ``_archive/``、``_adv_*``、``_arch_v*``
  等历史与调研目录）。``--report`` 会分别给出两个口径的覆盖率，便于分批偿还。

为什么不默认全仓强制
====================
历史目录（``_archive/`` 等）与调研沙箱不是产品代码，给它们补头只产生噪声 diff；
本工具把"未强制"**显式登记为报告里的缺口数字**，而不是假装全绿。想全量强制：
``--scope all``（或 ``--apply --scope all``）。

用法
====
    python tools/license_header_check_655.py                # 默认 = --check（active）
    python tools/license_header_check_655.py --scope all     # 全仓口径检查
    python tools/license_header_check_655.py --report        # 只报告：写 data/655_license_header_report.{md,json}
    python tools/license_header_check_655.py --apply --dry-run   # 预览要补哪些文件
    python tools/license_header_check_655.py --apply             # 幂等补头（保留 CRLF/BOM）
    python tools/license_header_check_655.py --selftest      # 本工具自检（不读仓库）

诚实边界
========
1. 检查只看**文件头 6 行**是否出现 SPDX 标识与版权行，不做完整 Apache-2.0 合规审查；
2. ``--apply`` 只**插入两行注释**，绝不改动任何既存字节（diff 只应包含新增行）；
3. 文件清单以 ``git ls-files`` 为准（生成物 / 忽略目录天然被排除）；无 git 时退化为
   目录遍历并跳过 ``__pycache__`` / ``.venv`` / ``build`` / ``.pytest_tmp``。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

sys.path.insert(0, str(HERE))
try:  # 与全仓一致的 UTF-8 控制台
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

SPDX_LINE = "# SPDX-License-Identifier: Apache-2.0"
COPYRIGHT_LINE = "# Copyright 2026 LiaoRanran (阿信)"
HEAD_PREFIX = "# SPDX-License-Identifier:"
HEAD_SCAN_LINES = 6

ACTIVE_PREFIXES = ("tools/", "tests/", "web/", "Scripts/")
ACTIVE_EXACT = ("conftest.py",)

SKIP_DIRS = {"__pycache__", ".venv", "venv", "build", ".pytest_tmp", ".git", "node_modules"}
_CODING_RE = re.compile(r"^#.*?coding[:=]\s*[-\w.]+")
_SPDX_RE = re.compile(r"^#\s*SPDX-License-Identifier:\s*Apache-2\.0\s*$")
_COPY_RE = re.compile(r"^#\s*Copyright\s+\d{4}\s+\S")

OUT_MD = ROOT / "data" / "655_license_header_report.md"
OUT_JSON = ROOT / "data" / "655_license_header_report.json"


# ── 文件清单 ────────────────────────────────────────────────────────────────
def tracked_py_files() -> list[Path]:
    """全部被 git 跟踪的 .py（相对路径排序）。无 git 时退化为目录遍历。"""
    try:
        proc = subprocess.run(["git", "ls-files", "*.py"], cwd=str(ROOT),
                              capture_output=True, text=True, check=True)
        files = [ROOT / ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
        files = [p for p in files if p.is_file()]
        if files:
            return sorted(set(files))
    except Exception:  # noqa: BLE001
        pass
    out: list[Path] = []
    for p in ROOT.rglob("*.py"):
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        out.append(p)
    return sorted(set(out))


def _rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def in_scope(p: Path, scope: str) -> bool:
    rel = _rel(p)
    if scope == "all":
        return True
    return rel.startswith(ACTIVE_PREFIXES) or rel in ACTIVE_EXACT


# ── 头检测 / 插入 ───────────────────────────────────────────────────────────
def header_status(text: str) -> tuple[bool, bool, int]:
    """返回 (有 SPDX, 有版权行, 插入下标)。行序按 ``\\n`` 切；CRLF 的 ``\\r`` 保留在行尾。"""
    body = text[1:] if text.startswith("\ufeff") else text
    lines = body.split("\n")
    head = [ln.rstrip("\r") for ln in lines[:HEAD_SCAN_LINES]]
    has_spdx = any(_SPDX_RE.match(ln) for ln in head)
    has_copy = any(_COPY_RE.match(ln) for ln in head)
    idx = 0
    if idx < len(lines) and lines[idx].lstrip("\ufeff").startswith("#!"):
        idx += 1
    if idx < 2 and idx < len(lines) and _CODING_RE.match(lines[idx].rstrip("\r")):
        idx += 1
    return has_spdx, has_copy, idx


def insert_header(text: str) -> str:
    """插入两行头注释；保留 BOM 与行尾风格；已带头则原样返回（幂等）。"""
    if header_status(text)[0]:
        return text
    bom = "\ufeff" if text.startswith("\ufeff") else ""
    body = text[1:] if bom else text
    cr = "\r" if "\r\n" in body[:200] else ""
    _, _, idx = header_status(body)
    lines = body.split("\n")
    lines.insert(idx, f"{SPDX_LINE}{cr}")
    lines.insert(idx + 1, f"{COPYRIGHT_LINE}{cr}")
    return bom + "\n".join(lines)


def _scan_files(files: list[Path]) -> tuple[list[str], list[str]]:
    """返回 (缺 SPDX 的, 有 SPDX 但缺版权行的)。"""
    miss: list[str] = []
    nocopy: list[str] = []
    for p in files:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            miss.append(_rel(p))
            continue
        has_spdx, has_copy, _ = header_status(text)
        if not has_spdx:
            miss.append(_rel(p))
        elif not has_copy:
            nocopy.append(_rel(p))
    return sorted(miss), sorted(nocopy)


def scan(scope: str) -> dict[str, Any]:
    """按口径统计（active/all 均给出，active 用于判红）。"""
    files = tracked_py_files()
    active = [p for p in files if in_scope(p, "active")]
    allf = [p for p in files if in_scope(p, "all")]
    missing, no_copy = _scan_files(active if scope == "active" else allf)
    return {
        "scope": scope,
        "tracked_py_total": len(files),
        "active_total": len(active),
        "all_total": len(allf),
        "checked": len(active) if scope == "active" else len(allf),
        "missing": missing,
        "missing_count": len(missing),
        "no_copyright": no_copy,
        "no_copyright_count": len(no_copy),
    }


def apply_headers(scope: str, dry_run: bool) -> dict[str, Any]:
    rep = scan(scope)
    changed: list[str] = []
    for rel in rep["missing"]:
        p = ROOT / rel
        text = p.read_text(encoding="utf-8", errors="replace")
        new = insert_header(text)
        if new == text:
            continue
        if not dry_run:
            p.write_text(new, encoding="utf-8", newline="")
        changed.append(rel)
    return {"scope": scope, "dry_run": dry_run, "changed_count": len(changed), "changed": changed}


# ── 报告 ────────────────────────────────────────────────────────────────────
def write_report() -> tuple[Path, Path]:
    act, allr = scan("active"), scan("all")
    lines = [
        "# 655 A · 许可证头覆盖报告（Apache-2.0）",
        "",
        "- 口径：`active` = `tools/ tests/ web/ Scripts/ conftest.py`；`all` = git 跟踪的全部 `.py`。",
        f"- 被跟踪 `.py` 总数：**{act['tracked_py_total']}**（`all` 口径检查 {allr['checked']}）",
        "",
        "| 口径 | 文件数 | 已带头 | 缺头 | 覆盖率 | 判红 |",
        "|---|---|---|---|---|---|",
        f"| active | {act['active_total']} | {act['active_total'] - act['missing_count']} | "
        f"{act['missing_count']} | {_pct(act['active_total'] - act['missing_count'], act['active_total'])} | 是 |",
        f"| all | {allr['all_total']} | {allr['all_total'] - allr['missing_count']} | "
        f"{allr['missing_count']} | {_pct(allr['all_total'] - allr['missing_count'], allr['all_total'])} | 否（登记） |",
        "",
        "## 一、active 口径缺头文件（`--check` 会判红的全部清单）",
        "",
    ]
    lines += [f"- `{m}`" for m in act["missing"]] or ["- （无）"]
    lines += ["", "## 二、all 口径额外缺头（历史 / 调研目录，未强制）", ""]
    extra = [m for m in allr["missing"] if m not in set(act["missing"])]
    lines += [f"- `{m}`" for m in extra[:400]]
    if len(extra) > 400:
        lines.append(f"- …（其余 {len(extra) - 400} 个见同名 `.json`）")
    lines += ["", "## 三、有 SPDX 但缺版权行", ""]
    lines += [f"- `{m}`" for m in act["no_copyright"]] or ["- （无）"]
    lines += ["", "---", "_本报告由 `tools/license_header_check_655.py --report` 生成；数字现算，不手写。_", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    OUT_JSON.write_text(json.dumps({"active": act, "all": allr}, ensure_ascii=False, indent=2),
                        encoding="utf-8", newline="\n")
    return OUT_MD, OUT_JSON


def _pct(n: int, d: int) -> str:
    return f"{(100.0 * n / d):.1f}%" if d else "—"


# ── 自检 ────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    plain = '"""doc."""\nX = 1\n'
    out = insert_header(plain)
    chk("无 shebang：头插在最前", out.splitlines()[0] == SPDX_LINE)
    chk("插入后 idempotent", insert_header(out) == out)
    chk("原正文未动", plain.splitlines()[-1] in out)

    she = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nX = 1\n"
    o2 = insert_header(she)
    l2 = o2.splitlines()
    chk("shebang 仍在第 1 行", l2[0].startswith("#!"))
    chk("coding 仍在第 2 行", "coding" in l2[1])
    chk("头在 coding 之后", l2[2] == SPDX_LINE and l2[3] == COPYRIGHT_LINE)

    crlf = "#!/usr/bin/env python3\r\nX = 1\r\n"
    o3 = insert_header(crlf)
    chk("CRLF 行尾保留", "\r\n" in o3 and o3.count(SPDX_LINE + "\r") == 1)

    bom = "\ufeffX = 1\n"
    o4 = insert_header(bom)
    chk("BOM 仍在第 1 字节", o4.startswith("\ufeff"))

    chk("检测已有头", header_status(out)[0] is True)
    chk("检测无头", header_status(plain)[0] is False)
    chk("scope=all 含历史目录", in_scope(ROOT / "_archive" / "x.py", "all") is True)
    chk("scope=active 排除历史目录", in_scope(ROOT / "_archive" / "x.py", "active") is False)
    chk("scope=active 含 tools/", in_scope(ROOT / "tools" / "x.py", "active") is True)
    print(f"license_header_check_655 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


# ── CLI ─────────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Apache-2.0 许可证头检查 / 补齐（655 A）")
    ap.add_argument("--check", action="store_true", help="严格检查（默认动作）")
    ap.add_argument("--scope", choices=("active", "all"), default="active")
    ap.add_argument("--report", action="store_true", help="写 data/655_license_header_report.*")
    ap.add_argument("--apply", action="store_true", help="批量补头（幂等）")
    ap.add_argument("--dry-run", action="store_true", help="配合 --apply：只预览不改文件")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    if a.apply:
        rep = apply_headers(a.scope, a.dry_run)
        print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else
              f"[license-header] scope={rep['scope']} dry_run={rep['dry_run']} "
              f"待补/已补 {rep['changed_count']} 个文件")
        return 0

    if a.report:
        md, js = write_report()
        print(f"[license-header] 报告已写：{_rel(md)} / {_rel(js)}")
        if not a.check:
            return 0

    rep = scan(a.scope)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(f"[license-header] 口径={rep['scope']} 检查 {rep['checked']} 个 .py "
              f"（active {rep['active_total']} / all {rep['all_total']}）")
        print(f"[license-header] 缺 SPDX 头：{rep['missing_count']} 个")
        for rel in rep["missing"][:20]:
            print(f"  - {rel}")
        if rep["missing_count"] > 20:
            print(f"  …（其余 {rep['missing_count'] - 20} 个）")
        if rep["no_copyright_count"]:
            print(f"[license-header] 有 SPDX 缺版权行：{rep['no_copyright_count']} 个（不判红，提示）")
    return 0 if rep["missing_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
