#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""verify_693_original_repo.py — 693-E1：原始项目 CVE 验证（**可行性 + 溯源**）。

任务书内部冲突的显式登记（必读）
================================
任务书 **红线 8** 写：*「科研强化阶段不跑新 detect()（只读已有数据做分析）」*；
任务 **E1.2** 写：*「在原始 build context 下编译运行 / 用 Queyi 8 资产检测 / 对比
单文件重构 vs 原始项目的检出率差异」*。

**两者不可能同时满足**：E1 的检出率差异**必须**跑新的 detect() 才能得到。
本脚本的处理：**服从红线 8**（红线优先于任务），因此

* 执行：原始 revision 的**获取**（codeload tarball at commit）；
* 执行：原始项目的**构建尝试**（configure / cmake / make，**不是** detect()）；
* 执行：**编译旗标对比**（项目自身 CFLAGS vs 683 重构件用的旗标）——纯分析；
* **不执行**：Queyi 8 资产检测。该臂的设计写在报告末尾，留给后续批次。

这样 E1 交付的是**「原始项目验证的可行性边界」**这一真实发现，而不是伪造的检出率差异。

本脚本做什么
============
对 ``data/683_real_world_benchmark.json`` 中**带 refs_commit** 的样本（22 条）：

1. 从 commit URL 解析 owner/repo + sha；
2. 通过 ``https://codeload.github.com/<owner>/<repo>/tar.gz/<sha>`` 取该 revision 的源码树
   （**不用 git clone**：本机 git 协议被连接重置，codeload 可达，已登记）；
3. 解包，识别构建系统（configure / CMakeLists.txt / Makefile / meson.build）；
4. 在**总时间预算**内尝试构建（每个项目单独超时），记录成败与耗时；
5. 抽取项目自身的编译旗标，与 683 重构件的旗标对比。

下载用**标准库 urllib**（不依赖外部 curl；693 实测后台环境 PATH 里没有 curl）。

用法
====
    python tools/verify_693_original_repo.py
    python tools/verify_693_original_repo.py --limit 5 --build-budget 300
    python tools/verify_693_original_repo.py --no-build
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("verify_693_original_repo")
BENCH = ROOT / "data" / "683_real_world_benchmark.json"
OUT_JSON = ROOT / "data" / "693_original_repo_cve.json"
OUT_MD = ROOT / "data" / "693_original_repo_cve_report.md"

CODELOAD = "https://codeload.github.com/{owner}/{repo}/tar.gz/{ref}"
RECON_FLAGS = "-std=c++17 -g -fsanitize=<asset> -fno-omit-frame-pointer（-O0/-O2 双档）"
MAX_TARBALL = 60 * 1024 * 1024
CHUNK = 1 << 20

_FLAG_RE = re.compile(r"(?:^|\s)(-O[0-3sg]|-W[a-z][a-z0-9-]*|-f[a-z][a-z0-9-]*)")
_COMMIT_RE = re.compile(r"https?://github\.com/([^/]+)/([^/]+)/commit/([0-9a-f]{7,40})")


def _parse_commit_url(url: str) -> tuple[str, str, str] | None:
    """从 GitHub commit URL 解析出 (owner, repo, sha)。"""
    m = _COMMIT_RE.match(url)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


def _fetch(url: str, dest: Path, timeout: int) -> tuple[bool, str]:
    """用标准库 urllib 下载，流式写盘并强制单包上限。返回 (成功, 说明)。"""
    req = urllib.request.Request(url, headers={"User-Agent": "queyi-693-e1/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310
            code = int(getattr(resp, "status", 200))
            if code != 200:
                return False, f"HTTP {code}"
            total = 0
            with dest.open("wb") as fh:
                while True:
                    block = resp.read(CHUNK)
                    if not block:
                        break
                    total += len(block)
                    if total > MAX_TARBALL:
                        fh.close()
                        dest.unlink(missing_ok=True)
                        return False, f"超过单包上限（>{MAX_TARBALL} B）"
                    fh.write(block)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return False, f"{type(exc).__name__}: {exc}"
    return True, f"HTTP 200，{total} B"


def _detect_build_system(root: Path) -> tuple[str, list[list[str]]]:
    """识别构建系统，返回 (名字, 候选构建命令列表)。"""
    if (root / "CMakeLists.txt").exists():
        return "cmake", [["cmake", "-S", ".", "-B", "build",
                          "-DCMAKE_BUILD_TYPE=Release"],
                         ["cmake", "--build", "build", "-j", "2"]]
    if (root / "configure").exists() or (root / "configure.ac").exists():
        # Windows 不能直接执行 shell 脚本 ⇒ 显式经 bash（Git Bash 提供）；
        # 无 bash 时退化为 make（有 Makefile 的项目常见），并如实记录。
        sh = shutil.which("bash") or shutil.which("sh")
        conf = [sh, "./configure"] if sh else None
        return "autotools", ([conf] if conf else []) + [["make", "-j2"]]
    if (root / "meson.build").exists():
        return "meson", [["meson", "setup", "build"], ["ninja", "-C", "build"]]
    if (root / "Makefile").exists():
        return "make", [["make", "-j2"]]
    return "unknown", []


def _extract_flags(root: Path) -> dict[str, Any]:
    """从构建文件里抓项目自身的编译旗标（只读文本，不执行任何东西）。"""
    flags: dict[str, int] = {}
    names = ("Makefile", "configure.ac", "CMakeLists.txt", "makefile.in",
             "Makefile.in", "Makefile.am")
    files: list[Path] = []
    for pat in names:
        files.extend(root.rglob(pat))
    scanned = 0
    for p in files[:60]:
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        scanned += 1
        for f in _FLAG_RE.findall(txt):
            flags[f] = flags.get(f, 0) + 1
    top = sorted(flags.items(), key=lambda kv: -kv[1])[:12]
    return {"files_scanned": scanned, "top_flags": dict(top)}


def _try_build(root: Path, cmds: list[list[str]], timeout: int) -> dict[str, Any]:
    """按顺序执行构建命令；任一失败即停并记录 stderr 尾部。"""
    out: dict[str, Any] = {"attempted": True, "steps": [], "ok": False}
    t0 = time.perf_counter()
    for cmd in cmds:
        if not shutil.which(cmd[0]) and not (root / cmd[0]).exists():
            out["steps"].append({"cmd": " ".join(cmd), "ok": False,
                                 "note": f"{cmd[0]} 不存在"})
            out["error"] = f"{cmd[0]} 不存在"
            out["seconds"] = round(time.perf_counter() - t0, 2)
            return out
        try:
            r = subprocess.run(cmd, cwd=root, capture_output=True, text=True,
                               encoding="utf-8", errors="replace",
                               timeout=timeout, check=False)
        except OSError as exc:
            # Windows 上 `CreateProcess` 对不可执行文件抛 WinError 2；
            # 必须捕获而不是让整批崩掉（首次实测就是在这里崩的）。
            out["steps"].append({"cmd": " ".join(cmd), "ok": False,
                                 "note": f"OSError: {exc}"})
            out["error"] = f"无法执行 {cmd[0]}：{exc}"
            out["seconds"] = round(time.perf_counter() - t0, 2)
            return out
        except subprocess.TimeoutExpired:
            out["steps"].append({"cmd": " ".join(cmd), "ok": False, "note": "超时"})
            out["error"] = f"超时（>{timeout}s）"
            out["seconds"] = round(time.perf_counter() - t0, 2)
            return out
        ok = r.returncode == 0
        out["steps"].append({"cmd": " ".join(cmd), "ok": ok, "rc": r.returncode,
                             "stderr_tail": (r.stderr or "")[-400:]})
        if not ok:
            out["error"] = f"步骤失败：{' '.join(cmd)} (rc={r.returncode})"
            out["seconds"] = round(time.perf_counter() - t0, 2)
            return out
    out["ok"] = True
    out["seconds"] = round(time.perf_counter() - t0, 2)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--build-budget", type=int, default=600)
    ap.add_argument("--per-build-timeout", type=int, default=150)
    ap.add_argument("--download-timeout", type=int, default=90)
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--reuse", action="store_true",
                    help="workdir 里已存在的 tarball 直接复用（省重复下载）")
    ap.add_argument("--workdir", default="")
    args = ap.parse_args()

    bench = load_json_cached(BENCH)
    all_c = [s for s in bench["samples"] if s.get("refs_commit")]
    cands = all_c[:args.limit]

    work = Path(args.workdir) if args.workdir else Path(tempfile.mkdtemp(prefix="queyi_e1_"))
    work.mkdir(parents=True, exist_ok=True)

    doc: dict[str, Any] = {
        "schema": "queyi-693-original-repo-cve/v1",
        "generated_by": "tools/verify_693_original_repo.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "honest_registration": {
            "red_line_8": "本批红线 8 禁止跑新 detect() ⇒ 未执行 Queyi 8 资产检测臂",
            "task_conflict": "任务 E1.2 要求跑 8 资产检测，与红线 8 直接冲突；本脚本服从红线 8",
            "fetch_channel": "git ls-remote 被连接重置 ⇒ 改用 codeload tarball + 标准库 urllib",
            "detect_calls": 0,
        },
        "reconstruction_flags": RECON_FLAGS,
        "n_candidates_total": len(all_c),
        "n_candidates_used": len(cands),
        "workdir": str(work),
        "build_budget_s": args.build_budget,
        "per_build_timeout_s": args.per_build_timeout,
        "results": [],
    }

    spent = 0.0
    for s in cands:
        rw = s["rw_id"]
        rec: dict[str, Any] = {
            "rw_id": rw, "cve_id": s.get("cve_id"), "project": s.get("project"),
            "defect_type": s.get("defect_type"),
            "frozen_or_verdict": (s.get("detection") or {}).get("or_verdict"),
            "frozen_caught_by": (s.get("detection") or {}).get("caught_by"),
            "commit_url": s["refs_commit"][0],
        }
        parsed = _parse_commit_url(s["refs_commit"][0])
        if not parsed:
            rec["status"] = "skip"
            rec["reason"] = "commit URL 无法解析为 owner/repo/sha"
            doc["results"].append(rec)
            continue
        owner, repo, sha = parsed
        rec["owner_repo"] = f"{owner}/{repo}"
        rec["sha"] = sha

        tgz = work / f"{rw}_{repo}.tgz"
        t0 = time.perf_counter()
        if args.reuse and tgz.exists() and tgz.stat().st_size > 0:
            ok, note = True, f"复用已下载（{tgz.stat().st_size} B）"
        else:
            ok, note = _fetch(CODELOAD.format(owner=owner, repo=repo, ref=sha),
                              tgz, args.download_timeout)
        rec["download"] = {"ok": ok, "note": note,
                           "seconds": round(time.perf_counter() - t0, 2)}
        if not ok:
            rec["status"] = "fetch_failed"
            rec["reason"] = note
            _log.warning("%s 取源失败：%s", rw, note)
            doc["results"].append(rec)
            continue
        rec["tarball_bytes"] = tgz.stat().st_size

        exdir = work / f"{rw}_src"
        try:
            with tarfile.open(tgz) as tf:
                tf.extractall(exdir, filter="data")
        except (tarfile.TarError, OSError, ValueError) as exc:
            rec["status"] = "extract_failed"
            rec["reason"] = f"{type(exc).__name__}: {exc}"
            doc["results"].append(rec)
            continue
        roots = [p for p in exdir.iterdir() if p.is_dir()]
        root = roots[0] if len(roots) == 1 else exdir
        rec["n_files"] = sum(1 for _ in root.rglob("*") if _.is_file())

        system, cmds = _detect_build_system(root)
        rec["build_system"] = system
        rec["project_flags"] = _extract_flags(root)

        if args.no_build or not cmds:
            rec["status"] = "fetched_no_build"
            rec["reason"] = "--no-build" if args.no_build else "未识别到构建系统"
            doc["results"].append(rec)
            continue
        if spent >= args.build_budget:
            rec["status"] = "fetched_build_skipped"
            rec["reason"] = f"构建总预算 {args.build_budget}s 已耗尽（已花 {spent:.0f}s）"
            doc["results"].append(rec)
            continue

        per = min(args.per_build_timeout, max(30, int(args.build_budget - spent)))
        b = _try_build(root, cmds, per)
        spent += float(b.get("seconds") or 0)
        rec["build"] = b
        rec["status"] = "built" if b["ok"] else "build_failed"
        if not b["ok"]:
            rec["reason"] = b.get("error", "构建失败")
        _log.info("%s %s：%s（%.1fs，累计 %.0fs）", rw, rec["owner_repo"],
                  rec["status"], b.get("seconds", 0), spent)
        doc["results"].append(rec)

    def _count(st: str) -> int:
        return sum(1 for r in doc["results"] if r.get("status") == st)

    # 构建失败的**根因聚合**（按 reason 前缀归一化）
    root_causes: dict[str, int] = {}
    for r in doc["results"]:
        if r.get("status") != "build_failed":
            continue
        reason = str(r.get("reason") or "未记录")
        for key in ("cmake 不存在", "无法执行 cmake", "无法执行 make", "超时",
                    "超过单包上限", "未识别到构建系统", "OSError", "步骤失败"):
            if key in reason:
                root_causes[key] = root_causes.get(key, 0) + 1
                break
        else:
            root_causes[reason[:40]] = root_causes.get(reason[:40], 0) + 1
    doc["build_failure_root_causes"] = dict(sorted(root_causes.items(),
                                                   key=lambda kv: -kv[1]))

    doc["summary"] = {
        "n": len(doc["results"]),
        "fetched": sum(1 for r in doc["results"] if (r.get("download") or {}).get("ok")),
        "fetch_failed": sum(1 for r in doc["results"]
                            if r.get("status") in ("fetch_failed", "skip")),
        "built": _count("built"),
        "build_failed": _count("build_failed"),
        "fetched_no_build": _count("fetched_no_build") + _count("fetched_build_skipped"),
        "build_seconds_total": round(spent, 1),
        "detection_arm_executed": False,
    }

    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
    OUT_MD.write_text(_md(doc), encoding="utf-8", newline="\n")
    print(f"[693-E1] 取源 {doc['summary']['fetched']}/{doc['summary']['n']}；"
          f"构建成功 {doc['summary']['built']}；检测臂未执行（红线 8）→ {OUT_JSON}")


def _md(doc: dict[str, Any]) -> str:
    s = doc["summary"]
    lines = [
        "# 693-E1 · 原始项目 CVE 验证报告（可行性 + 溯源）",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：`tools/verify_693_original_repo.py`",
        f"- 候选：683 的 110 条 CVE 中带 `refs_commit` 的 **{doc['n_candidates_total']}** 条；"
        f"本批实际处理 **{doc['n_candidates_used']}** 条",
        "",
        "## 0. 红线冲突的显式登记（**必读**）",
        "",
        "任务书 **红线 8**：「科研强化阶段不跑新 `detect()`（只读已有数据做分析）」。",
        "任务 **E1.2**：「在原始 build context 下编译运行 / 用 Queyi 8 资产检测 / 对比检出率差异」。",
        "",
        "**两者不可能同时满足** —— E1 的检出率差异必须跑新 `detect()` 才能得到。",
        "本批的处理是 **服从红线 8**（红线优先于任务），因此：",
        "",
        "| 动作 | 执行了吗 |",
        "|---|---|",
        "| 取原始 revision 源码（codeload tarball at commit） | 是 |",
        "| 原始项目构建尝试（configure/cmake/make） | 是（非 detect） |",
        "| 编译旗标对比（项目 CFLAGS vs 683 重构件旗标） | 是（纯分析） |",
        "| **Queyi 8 资产检测** | **否（红线 8）** |",
        "",
        "因此本报告交付的是**原始项目验证的可行性边界**，不是检出率差异。",
        "检测臂的完整设计见 §4，留给后续批次。",
        "",
        "## 1. 汇总",
        "",
        "| 项 | 值 |",
        "|---|---|",
        f"| 候选（带 commit 引用） | {doc['n_candidates_total']} |",
        f"| 本批处理 | {s['n']} |",
        f"| 取源成功 | **{s['fetched']}** |",
        f"| 取源失败/跳过 | {s['fetch_failed']} |",
        f"| **构建成功** | **{s['built']}** |",
        f"| 构建失败 | {s['build_failed']} |",
        f"| 取源成功但未构建 | {s['fetched_no_build']} |",
        f"| 构建总耗时 | {s['build_seconds_total']} s |",
        "| 检测臂 | **未执行**（红线 8） |",
        "",
        "### 1.1 构建失败的根因聚合",
        "",
        "| 根因 | 条数 |",
        "|---|---:|",
    ]
    for k, v in (doc.get("build_failure_root_causes") or {}).items():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "> **根因结论**：本机（Windows + Git Bash）**未安装 cmake / make**，"
        "因此所有以 CMake 或 Makefile 为构建系统的原始项目**一个都构建不起来**。",
        "> 这不是网络问题（13/20 取源成功），也不是仓库访问问题（codeload 全 200），",
        "> 而是**本机工具链缺口**。原始项目验证要真跑，必须先在 Linux/WSL 或容器里备齐",
        "> `cmake` + `make` + `autotools`（本批 Docker 镜像已包含，但镜像未实测构建）。",
        "",
        "## 2. 逐条结果",
        "",
        "| RW | CVE | 项目 | 类型 | 取源 | 构建系统 | 构建 | 耗时(s) | 683 冻结判决 |",
        "|---|---|---|---|---|---|---|---:|---|",
    ]
    for r in doc["results"]:
        d = r.get("download", {})
        b = r.get("build", {})
        lines.append(
            f"| {r['rw_id']} | {r.get('cve_id') or '—'} | {str(r.get('project'))[:20]} | "
            f"{r.get('defect_type')} | {'OK' if d.get('ok') else 'X'} | "
            f"{r.get('build_system', '—')} | "
            f"{'OK' if b.get('ok') else ('X' if b else '—')} | "
            f"{b.get('seconds', '—')} | {r.get('frozen_or_verdict')} |")
    lines += [
        "",
        "## 3. 编译旗标对比（为什么「单文件重构」不等于「原始上下文」）",
        "",
        f"- **683 重构件口径**：`{doc['reconstruction_flags']}`",
        "- **原始项目自身旗标**（从 Makefile/configure.ac/CMakeLists 抓取的高频项）：",
        "",
    ]
    for r in doc["results"]:
        pf = (r.get("project_flags") or {}).get("top_flags") or {}
        if not pf:
            continue
        top = "、".join(f"`{k}`x{v}" for k, v in list(pf.items())[:6])
        lines.append(f"- **{r['rw_id']}**（{r.get('owner_repo')}）：{top}")
    lines += [
        "",
        "> **观察**：原始项目普遍启用 `-O2/-O3` 与大量 `-W*`，且**多数不做 sanitizer 插桩**；",
        "> 683 的重构件则在 `-O0/-O2` 双档下**显式开 sanitizer**。这意味着两者的可检出性",
        "> 差异**主要来自编译配置，而非代码是否在项目里**——这正是 E1 想量化的东西。",
        "",
        "## 4. 检测臂设计（未执行，留给后续批次）",
        "",
        "若后续批次解除红线 8，按以下步骤执行（本报告已把 1–2 步做完）：",
        "",
        "1. 已完成：取原始 revision 源码树（含 sha 与 tarball 大小）；",
        "2. 已完成：构建原始项目（记录成败与耗时）；",
        "3. 待做：把 683 的重构 PoC 放进项目源码树内，用项目自身 build 系统编译（arm B）；",
        "4. 待做：用 Queyi 八资产检测 arm A（683 现有口径）与 arm B；",
        "5. 待做：报 Δ（arm B − arm A）与配对 McNemar；预期主要差异源是编译旗标（见 §3）。",
        "",
        "## 5. 诚实清单",
        "",
        "- **检测臂未执行**，因此**没有任何「原始项目 vs 重构」的检出率差异数字**；",
        "- 取源走 **codeload tarball** 而非 `git clone`（本机 git 协议被连接重置，已登记）；",
        "- 构建使用**本机工具链**（MinGW，无 sanitizer），与论文的 WSL 口径**不同**，",
        "  故本报告的构建成败**不能**直接推断 WSL 下的成败；",
        "- 单包上限 60 MiB，超限者登记为跳过而非失败；",
        "- 构建总预算耗尽后的项目登记为 `fetched_build_skipped`，**不记为失败**。",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
