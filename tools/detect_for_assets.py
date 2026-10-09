#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""detect_for_assets.py — 673r：把 `holdout_reveal_661.detect` 从「样本 → 单个 detector」
提升为「样本 × 资产子集」的**真实逐资产判定**。

为什么需要这一层
================
`tools/holdout_reveal_661.py::detect(kind, files)` 本身**已经是单资产接口**
（`kind` 就是资产 id：asan / tsan / ubsan / compiler-warn / cross-compile / linker /
wunsequenced）。661 的 `main()` 只是用 `PLAN` 给每个样本**固定指派一个** detector，
于是落盘的逐样本明细是「这条样本被哪个资产判成什么」——**一对一**。

673p 的 A5 因此卡死：重放层只能表达「detector ∈ 选中集才 catch」（**单归属假设**），
无法回答「若只跑子集 S，这条样本会怎样」。673r 的解法不是改 detect，而是：

    对每条样本、每个资产**各调一次**既有 detect ⇒ 得到 N × 8 的真实判定矩阵
    ⇒ 子集 S 的判定 = S 中资产的 **OR**（任一资产抓到即抓到）。

这样 A5 的「同预算选哪些资产」第一次成为**可计算的量**，而不是事后记账。

红线（本文件严格遵守）
======================
* **不修改** `holdout_reveal_661.py::detect` —— 双档 -O0/-O2、TSan 不可用判定、
  `setarch -R` 都是 666/668 调出来的判据；已落盘 reveal 记录的可复现性依赖它。
* **不修改** `holdout_reveal_661.py::main` —— 触发 `[REFUSED]` 盲区铁律。
* 本文件只做「外层」：加载模块 → 按样本切 `ATOMS`（沿用 672h 既有做法）→ 逐资产调用 → 聚合。

三层解码兜底适配层（WSL 横幅污染，见下）
========================================
本机 WSL 2.7.10 在 Windows 系统代理开启（ProxyEnable=1）时，每次 `wsl.exe` 调用都会向
**stderr** 写一条警告横幅，且是 **UTF-16LE** 字节。Python `subprocess.run(text=True)`
用 UTF-8 strict 解码 ⇒ 抛 `UnicodeDecodeError` ⇒ `CompletedProcess.stderr` 变 **None**
⇒ ASan/UBSan 的报告（走 stderr）**全部丢失** ⇒ **系统性假 miss**。

实测证据：`h41`（`Appendix/ub/ub_use_after_free.cpp`）在 672h 冻结记录里 asan = **catch**；
未装适配层时本环境判 **miss**，装了才回到 catch。

三层处置（按治本到下兜排序，**都不改 detect 的代码**）：

1. `WSL_UTF8=1` + `WSLENV=WSL_UTF8/u`（环境变量，detect 的 subprocess 会继承）
   ⇒ 实测横幅变成**合法 UTF-8** 中文，解码不再失败。**治本。**
2. 文本模式解码用 `errors="replace"` ⇒ 任何残余非法字节不再让整条流变 None。
3. 过滤含 NUL 的行、以及 `wsl:` 开头的行 ⇒ 去掉 UTF-16 残留与横幅噪声。

适配层只在 `decode_safety()` 上下文内存活，退出即卸载，并在产物 `environment` 块里
**显式登记**装了什么、探测到什么。绝不静默。

聚合口径（写死，可测）
======================
    catch     —— 选中资产中**任一**返回 catch
    unknown   —— 选中资产**全部**返回 unknown（绝不许把 unknown 当 miss）
    miss      —— 其余（至少一个资产给了确定的 miss，且无人 catch）

用法
====
    python tools/detect_for_assets.py --check                  # 自检（含 h41 asan 保真断言）
    python tools/detect_for_assets.py --probe                  # 只探测 WSL 横幅/环境
    python tools/detect_for_assets.py --dataset holdout --limit 3 --no-write
    python tools/detect_for_assets.py --dataset both           # 全量跑 + 落盘（约 25 分钟）
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import asset_capabilities as _ac  # noqa: E402  707-B：聚合规则/声明的单一事实源（700-F P1/P3）

VERSION = "1.0"
OUT_DEFAULT = ROOT / "data" / "experiments" / "asset_attribution_673r.json"

H_DETAIL = ROOT / "data" / "holdout" / "reveal_5_detail_672h.json"
C_DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_672h.json"
CORPUS_CODE_FILES = (
    "data/external_corpus/external_corpus_662.json",
    "data/external_corpus/external_corpus_665.json",
    "data/external_corpus/external_corpus_669d.json",
    "data/external_corpus/external_corpus_672h.json",
)
NEW_SOURCE = "measured_672h"

_BANNER_RE = re.compile(r"^\s*wsl\s*:", re.IGNORECASE)


# ─────────────────────────────────────────────────────────────────────────────
# 第 0 层：加载 661（沿用 672h 的 importlib 装载器，不 import 成包）
# ─────────────────────────────────────────────────────────────────────────────
def load_rv661():
    """按文件路径加载 `tools/holdout_reveal_661.py`（不执行 main，不改一行代码）。"""
    spec = importlib.util.spec_from_file_location("rv661", str(HERE / "holdout_reveal_661.py"))
    if spec is None or spec.loader is None:
        raise ImportError("无法构造 holdout_reveal_661 的模块规格")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["rv661"] = mod
    spec.loader.exec_module(mod)
    return mod


# ─────────────────────────────────────────────────────────────────────────────
# 第 1–3 层：解码兜底适配层
# ─────────────────────────────────────────────────────────────────────────────
_ORIG_RUN = subprocess.run
_ADAPTER_INSTALLED = False


def _strip_banner(text: str) -> str:
    """去掉 wsl 横幅行与 UTF-16 残留行（含 NUL 的行不可能是编译器/程序输出）。"""
    return "\n".join(ln for ln in text.splitlines()
                     if "\x00" not in ln and not _BANNER_RE.match(ln))


def _decode_safe_run(*args: Any, **kwargs: Any):
    """`subprocess.run` 的兜底包装：文本模式用 errors=replace，并剥掉横幅行。"""
    wants_text = kwargs.get("text") or kwargs.get("universal_newlines")
    if not wants_text:
        return _ORIG_RUN(*args, **kwargs)
    kw = dict(kwargs)
    kw.pop("errors", None)
    kw["errors"] = "replace"
    cp = _ORIG_RUN(*args, **kw)
    if isinstance(cp.stdout, str):
        cp.stdout = _strip_banner(cp.stdout)
    if isinstance(cp.stderr, str):
        cp.stderr = _strip_banner(cp.stderr)
    return cp


def probe_wsl_banner() -> dict[str, Any]:
    """探测本机 wsl.exe 是否向 stderr 写非 UTF-8 横幅。只读，不改任何状态。"""
    try:
        cp = _ORIG_RUN(["wsl", "-e", "bash", "-lc", "true"], capture_output=True, timeout=60)
    except Exception as e:  # noqa: BLE001
        return {"wsl_available": False, "error": f"{type(e).__name__}: {e}"}
    err = cp.stderr or b""
    utf16 = b"\x00" in err
    try:
        err.decode("utf-8")
        decodable = True
    except UnicodeDecodeError:
        decodable = False
    return {
        "wsl_available": cp.returncode == 0,
        "stderr_bytes": len(err),
        "stderr_has_nul": utf16,
        "stderr_utf8_decodable": decodable,
        "banner_present": err.startswith(b"w") or b"wsl" in err[:16].lower(),
        "stderr_head_latin1": err[:80].decode("latin-1"),
    }


@contextlib.contextmanager
def decode_safety() -> Iterator[dict[str, Any]]:
    """装/卸三层解码兜底（退出时**必须**还原，绝不残留全局改动）。"""
    global _ADAPTER_INSTALLED
    env_before = {k: os.environ.get(k) for k in ("WSL_UTF8", "WSLENV")}
    probe_before = probe_wsl_banner()

    os.environ["WSL_UTF8"] = "1"          # 第 1 层：强制 wsl 输出 UTF-8（治本）
    os.environ["WSLENV"] = "WSL_UTF8/u"
    subprocess.run = _decode_safe_run     # 第 2+3 层：解码兜底 + 横幅剥离
    _ADAPTER_INSTALLED = True
    probe_after = probe_wsl_banner()
    info = {
        "installed": True,
        "layers": [
            "L1 env WSL_UTF8=1 + WSLENV=WSL_UTF8/u（强制 wsl 输出 UTF-8，治本）",
            "L2 subprocess 文本模式 errors=replace（不抛异常 ⇒ stderr 不变 None）",
            "L3 剥离含 NUL 的行与 wsl: 开头的行（去 UTF-16 残留与横幅噪声）",
        ],
        "probe_before": probe_before,
        "probe_after": probe_after,
        "L1_effect": probe_after.get("stderr_utf8_decodable") is True,
    }
    try:
        yield info
    finally:
        subprocess.run = _ORIG_RUN
        _ADAPTER_INSTALLED = False
        for k, v in env_before.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def adapter_installed() -> bool:
    return _ADAPTER_INSTALLED


# ─────────────────────────────────────────────────────────────────────────────
# 样本规格
# ─────────────────────────────────────────────────────────────────────────────
@dataclass(frozen=True)
class SampleSpec:
    """一条待判样本。**要么**有磁盘夹具（dir+files），**要么**有内联代码。"""

    id: str
    dataset: str
    dir: str = ""                       # 相对仓库根；磁盘夹具模式
    files: tuple[str, ...] = ()         # 文件名（相对 dir）
    code: str | None = None             # 内联源码（corpus 模式）
    recorded_detector: str = ""         # 672h 冻结记录里的 detector（保真对照用）
    recorded_verdict: str = ""          # 672h 冻结记录里的 verdict
    source: str = ""                    # 派生集/评估集切分用
    category: str = ""

    @property
    def input_mode(self) -> str:
        return "code_materialized" if self.code is not None else "disk_fixtures"

    def as_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"id": self.id, "source": self.source, "category": self.category,
                             "input_mode": self.input_mode,
                             "recorded_detector": self.recorded_detector,
                             "recorded_verdict": self.recorded_verdict}
        if self.code is not None:
            d["code_sha256"] = _sha256_text(self.code)
        else:
            d["dir"] = self.dir
            d["files"] = list(self.files)
        return d


def _sha256_text(t: str) -> str:
    import hashlib

    return hashlib.sha256(t.encode("utf-8")).hexdigest()


def corpus_code_map() -> dict[str, str]:
    """corpus 样本 id → 内联源码（四个历史 json 并集，先到先得）。"""
    out: dict[str, str] = {}
    for rel in CORPUS_CODE_FILES:
        p = ROOT / rel
        if not p.is_file():
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        for s in doc.get("samples", []):
            out.setdefault(str(s["id"]), str(s.get("code", "")))
    return out


def measurable_specs(dataset: str) -> list[SampleSpec]:
    """可测样本规格（口径与 673p 一致：catch+miss；holdout 另加 planted=true）。"""
    if dataset == "holdout":
        rows = json.loads(H_DETAIL.read_text(encoding="utf-8"))["per_sample"]
        rows = [r for r in rows if r.get("planted") is True]
    elif dataset == "corpus":
        rows = json.loads(C_DETAIL.read_text(encoding="utf-8"))["per_sample"]
        cmap = corpus_code_map()
    else:
        raise ValueError(f"未知 dataset={dataset!r}（应为 holdout / corpus）")

    rows = [r for r in rows if r.get("verdict") in ("catch", "miss")]
    specs: list[SampleSpec] = []
    for r in rows:
        if dataset == "holdout":
            specs.append(SampleSpec(
                id=str(r["id"]), dataset="holdout",
                dir=str(r.get("dir", "")), files=tuple(str(f) for f in (r.get("files") or [])),
                recorded_detector=str(r.get("detector", "")),
                recorded_verdict=str(r.get("verdict", "")),
                source=str(r.get("source", "")), category=str(r.get("category", "")),
            ))
        else:
            code = cmap.get(str(r["id"]))
            if code is None:
                raise KeyError(f"corpus 样本 {r['id']} 在历史 json 里没有 code ⇒ 无法实测")
            specs.append(SampleSpec(
                id=str(r["id"]), dataset="corpus", code=code,
                recorded_detector=str(r.get("detector", "")),
                recorded_verdict=str(r.get("verdict", "")),
                source=str(r.get("source", "")), category=str(r.get("category", "")),
            ))
    return specs


# ─────────────────────────────────────────────────────────────────────────────
# 核心：逐资产调用既有 detect
# ─────────────────────────────────────────────────────────────────────────────
def detect_one_asset(rv: Any, spec: SampleSpec, asset_id: str, *, atoms_root: str) -> dict[str, Any]:
    """对**单个资产**调一次既有 `detect`。返回 {verdict, note, wall_seconds}。

    `ATOMS` 的临时切换沿用 672h 的既有做法（`rv.ATOMS = <该样本目录>`，finally 还原）；
    这不是改判据，只是告诉 detect 去哪儿取夹具。
    """
    old = rv.ATOMS
    t0 = time.perf_counter()
    try:
        rv.ATOMS = atoms_root
        verdict, note = rv.detect(asset_id, list(spec.files) if spec.files else [])
    finally:
        rv.ATOMS = old
    return {"verdict": str(verdict), "note": str(note),
            "wall_seconds": round(time.perf_counter() - t0, 4)}


def aggregate(by_asset: dict[str, dict[str, Any]], rule: str = "or") -> dict[str, Any]:
    """聚合。**unknown 绝不许当 miss**。

    科研依据（707-B / 700-F P3）：聚合规则必须**显式声明**。默认 ``rule="or"``
    （旧行为，与冻结矩阵逐字一致，**对零产资产免疫**）；``mean`` 会被零产资产稀释
    （8 资产 vs 6 资产稀释因子 1.3333）。非 ``or`` 规则交给单一事实源
    ``asset_capabilities.aggregate_one`` 处理。
    """
    if rule != "or":
        v = _ac.aggregate_one({a: vv.get("verdict") for a, vv in by_asset.items()},
                              tuple(by_asset), rule=rule)
        caught = [a for a, vv in by_asset.items() if str(vv.get("verdict")) == "catch"]
        return {"verdict": v, "caught_by": (sorted(caught)[0] if caught else None),
                "caught_by_all": sorted(caught)}
    verdicts = {a: str(v.get("verdict")) for a, v in by_asset.items()}
    caught = [a for a, v in verdicts.items() if v == "catch"]
    if caught:
        return {"verdict": "catch", "caught_by": sorted(caught)[0], "caught_by_all": sorted(caught)}
    if verdicts and all(v == "unknown" for v in verdicts.values()):
        return {"verdict": "unknown", "caught_by": None, "caught_by_all": []}
    return {"verdict": "miss", "caught_by": None, "caught_by_all": []}


def detect_for_assets(spec: SampleSpec, selected: list[str] | tuple[str, ...], *,
                      rv: Any | None = None, pool_ids: list[str] | None = None,
                      rule: str = "or") -> dict[str, Any]:
    """样本 × 资产子集 的真实判定。

    参数
    ----
    spec      : 样本规格（磁盘夹具或内联代码）。
    selected  : 本次要跑的资产 id（预算 k 个子集）。
    rv        : 已加载的 661 模块（None ⇒ 现加载）。
    pool_ids  : 合法资产 id 白名单（None ⇒ `verifier_pool_673p.selectable_ids()`）。

    Raises
    ------
    ValueError : `selected` 含不在白名单里的资产（fail-loud，绝不静默跳过）。
    """
    import verifier_pool_673p as vp

    rv = rv if rv is not None else load_rv661()
    allowed = list(pool_ids) if pool_ids is not None else vp.selectable_ids(vp.ASSET_POOL)
    sel = list(selected)
    bad = [a for a in sel if a not in allowed]
    if bad:
        raise ValueError(f"选中的资产不在可选池中（fail-loud）：{bad}；可选={allowed}")

    tmpdir: str | None = None
    try:
        if spec.code is not None:
            # corpus：内联 code ⇒ 落临时目录，文件名 s.cpp（与 671a 同形）
            tmpdir = tempfile.mkdtemp(prefix=f"{spec.id}_")
            (Path(tmpdir) / "s.cpp").write_text(spec.code, encoding="utf-8")
            atoms_root = tmpdir
            files_for_detect = ["s.cpp"]
        else:
            atoms_root = str(ROOT / spec.dir) if spec.dir else str(ROOT)
            files_for_detect = list(spec.files)

        work = SampleSpec(id=spec.id, dataset=spec.dataset, dir=spec.dir,
                          files=tuple(files_for_detect), code=None,
                          recorded_detector=spec.recorded_detector,
                          recorded_verdict=spec.recorded_verdict)
        by_asset: dict[str, dict[str, Any]] = {}
        for a in sel:
            by_asset[a] = detect_one_asset(rv, work, a, atoms_root=atoms_root)
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)

    agg = aggregate(by_asset, rule=rule)
    unknown_reasons = {a: v["note"] for a, v in by_asset.items() if v["verdict"] == "unknown"}
    return {
        "id": spec.id,
        "dataset": spec.dataset,
        "input_mode": spec.input_mode,
        "selected": sel,
        "per_asset": by_asset,
        "unknown_reasons": unknown_reasons,
        **agg,
    }


# ─────────────────────────────────────────────────────────────────────────────
# 全量归属
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class AttributionResult:
    dataset: str
    samples: list[dict[str, Any]] = field(default_factory=list)
    wall_by_asset: dict[str, float] = field(default_factory=dict)
    wall_total: float = 0.0

    def as_dict(self) -> dict[str, Any]:
        return {"n": len(self.samples), "samples": self.samples,
                "wall_seconds_by_asset": {k: round(v, 3) for k, v in self.wall_by_asset.items()},
                "wall_seconds_total": round(self.wall_total, 3)}


def build_attribution(dataset: str, *, assets: list[str] | None = None, limit: int | None = None,
                      rv: Any | None = None, verbose: bool = True, rule: str = "or") -> dict[str, Any]:
    """对一个数据集跑 **全资产**：每条样本 × 每个可选资产各一次真实 detect。"""
    import verifier_pool_673p as vp

    rv = rv if rv is not None else load_rv661()
    asset_ids = list(assets) if assets is not None else vp.selectable_ids(vp.ASSET_POOL)
    specs = measurable_specs(dataset)
    if limit is not None:
        specs = specs[:limit]

    with decode_safety() as env_info:
        res = AttributionResult(dataset=dataset)
        t_all = time.perf_counter()
        for i, sp in enumerate(specs, 1):
            out = detect_for_assets(sp, asset_ids, rv=rv, pool_ids=asset_ids, rule=rule)
            row = sp.as_dict()
            row["per_asset"] = {a: {"verdict": v["verdict"], "note": v["note"][:300],
                                    "wall_seconds": v["wall_seconds"]}
                                for a, v in out["per_asset"].items()}
            row["or_verdict"] = out["verdict"]
            row["caught_by_all"] = out["caught_by_all"]
            row["unknown_reasons"] = out["unknown_reasons"]
            res.samples.append(row)
            for a, v in out["per_asset"].items():
                res.wall_by_asset[a] = res.wall_by_asset.get(a, 0.0) + v["wall_seconds"]
            if verbose:
                print(f"  [{dataset} {i}/{len(specs)}] {sp.id:<8} OR={out['verdict']:<7} "
                      f"caught_by={out['caught_by_all']}", flush=True)
        res.wall_total = time.perf_counter() - t_all

    return {
        "dataset": dataset,
        "n_measurable": len(specs),
        "asset_ids": asset_ids,
        "input_mode": specs[0].input_mode if specs else "",
        "source_of_record": (H_DETAIL if dataset == "holdout" else C_DETAIL).relative_to(ROOT).as_posix(),
        "environment": env_info,
        **res.as_dict(),
    }


def attribution_doc(datasets: list[str], *, limit: int | None = None, verbose: bool = True,
                    out_path: Path | None = None, rule: str = "or") -> dict[str, Any]:
    """跑多个数据集。**每跑完一个就增量落盘**（840 次真跑很贵，中途崩了也不该全丢）。"""
    import verifier_pool_673p as vp

    rv = load_rv661()
    t0 = time.perf_counter()
    parts: dict[str, Any] = {}

    def _snapshot() -> dict[str, Any]:
        return _doc_shell(vp, parts, time.perf_counter() - t0)

    for d in datasets:
        parts[d] = build_attribution(d, limit=limit, rv=rv, verbose=verbose, rule=rule)
        if out_path is not None:            # 增量落盘
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(_snapshot(), ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8", newline="\n")
            print(f"  [673r] 增量落盘 {d} → {out_path.name}", flush=True)
    return _snapshot()


def _doc_shell(vp: Any, parts: dict[str, Any], wall: float) -> dict[str, Any]:
    return {
        "schema": "queyi-asset-attribution/673r",
        "version": VERSION,
        "generated_by": "tools/detect_for_assets.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "prereg": "data/673r_a5_preregistration.json",
        "detector_owner": "tools/holdout_reveal_661.py::detect（**未修改**；双档 -O0/-O2 + "
                          "TSan 不可用判定 + setarch -R 全部沿用）",
        "execution_model": "real_per_asset_detect（每个样本 × 每个资产各一次真实 detect）",
        "aggregation": "OR：任一资产 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss（unknown 不当 miss）",
        "rounds": 1,
        "rounds_note": "672h 冻结记录为 3 回合『任一回合 catch ⇒ catch』；本批 1 回合 ⇒ 与 82.9%/62.5% 不同口径，不得相减。",
        "asset_pool": [a.as_dict() for a in vp.ASSET_POOL],
        "selectable_ids": vp.selectable_ids(vp.ASSET_POOL),
        "adapter_installed_during_run": True,
        "datasets": parts,
        "wall_seconds_total_all": round(wall, 3),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 保真自评（本批判定 vs 672h 冻结记录）
# ─────────────────────────────────────────────────────────────────────────────
def fidelity_report(doc: dict[str, Any]) -> dict[str, Any]:
    """逐样本：本批 `per_asset[recorded_detector]` 是否等于冻结记录的 verdict。

    注意这不是「对错」判定 —— 冻结记录是 3 回合口径、本批 1 回合，且环境已漂移。
    它衡量的是**测量链是否还认得同一批样本**，是适配层与环境的体检指标。
    """
    out: dict[str, Any] = {}
    for ds, part in doc["datasets"].items():
        rows = part["samples"]
        same = 0
        diffs: list[dict[str, str]] = []
        for r in rows:
            det = r.get("recorded_detector", "")
            rec = r.get("recorded_verdict", "")
            got = (r.get("per_asset", {}).get(det, {}) or {}).get("verdict")
            if got == rec:
                same += 1
            else:
                diffs.append({"id": r["id"], "detector": det, "frozen": rec, "this_run": str(got)})
        out[ds] = {"n": len(rows), "agree": same,
                   "agree_pct": round(same / len(rows) * 100, 4) if rows else None,
                   "disagreements": diffs}
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 自检
# ─────────────────────────────────────────────────────────────────────────────
def _raises(fn) -> bool:
    try:
        fn()
    except (ValueError, TypeError, KeyError):
        return True
    return False


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    import verifier_pool_673p as vp

    # 纯逻辑：聚合口径（不需要编译器）
    chk("OR：任一 catch ⇒ catch",
        aggregate({"asan": {"verdict": "miss"}, "ubsan": {"verdict": "catch"}})["verdict"] == "catch")
    chk("OR：全 miss ⇒ miss",
        aggregate({"asan": {"verdict": "miss"}, "ubsan": {"verdict": "miss"}})["verdict"] == "miss")
    chk("OR：全 unknown ⇒ unknown（不当 miss）",
        aggregate({"asan": {"verdict": "unknown"}, "ubsan": {"verdict": "unknown"}})["verdict"] == "unknown")
    chk("OR：unknown + miss ⇒ miss",
        aggregate({"asan": {"verdict": "unknown"}, "ubsan": {"verdict": "miss"}})["verdict"] == "miss")
    chk("OR：空集 ⇒ miss 且 caught_by=None",
        aggregate({})["verdict"] == "miss" and aggregate({})["caught_by"] is None)
    chk("caught_by_all 列出全部命中的资产",
        aggregate({"asan": {"verdict": "catch"}, "tsan": {"verdict": "catch"}})["caught_by_all"]
        == ["asan", "tsan"])

    # 纯逻辑：fail-loud 与规格
    specs = measurable_specs("holdout")
    chk("holdout 可测样本 = 41", len(specs) == 41, f"({len(specs)})")
    chk("corpus 可测样本 = 64", len(measurable_specs("corpus")) == 64)
    chk("样本规格带冻结 detector/verdict",
        all(s.recorded_detector and s.recorded_verdict for s in specs))
    chk("holdout 样本走磁盘夹具", all(s.input_mode == "disk_fixtures" for s in specs))
    chk("corpus 样本走内联 code",
        all(s.input_mode == "code_materialized" for s in measurable_specs("corpus")))
    chk("未知 dataset ⇒ ValueError", _raises(lambda: measurable_specs("nope")))
    rv = load_rv661()
    chk("661 detect 未被改动（仍是 2 元签名）",
        rv.detect.__code__.co_argcount == 2, f"({rv.detect.__code__.co_varnames[:2]})")
    chk("661 OPT_LEVELS 仍是双档", tuple(rv.OPT_LEVELS) == ("-O0", "-O2"))
    chk("661 的 SAN 映射未变", rv.SAN == {"tsan": "thread", "asan": "address", "ubsan": "undefined"})
    chk("未装适配层时 adapter_installed=False", adapter_installed() is False)
    chk("选中池外资产 ⇒ ValueError（fail-loud）",
        _raises(lambda: detect_for_assets(specs[0], ["valgrind"], rv=rv,
                                          pool_ids=vp.selectable_ids(vp.ASSET_POOL))))

    # 环境探测
    probe = probe_wsl_banner()
    chk("wsl 可用", probe.get("wsl_available") is True, f"({probe})")
    print(f"  [info] WSL 横幅探测：utf8_decodable={probe.get('stderr_utf8_decodable')} "
          f"has_nul={probe.get('stderr_has_nul')}")

    # 真实调用（慢，但这是本文件唯一的价值所在）
    with decode_safety() as info:
        chk("适配层第 1 层生效（stderr 可 UTF-8 解码）", info.get("L1_effect") is True)
        h41 = next(s for s in specs if s.id == "h41")
        asan = detect_one_asset(rv, h41, "asan", atoms_root=str(ROOT / h41.dir))
        chk("h41 × asan = catch（冻结记录保真断言）", asan["verdict"] == "catch",
            f"({asan['verdict']} / {asan['note'][:60]})")
        ct = detect_one_asset(rv, h41, "compile-time", atoms_root=str(ROOT / h41.dir))
        chk("compile-time 无本地检测器 ⇒ unknown（不是 miss）", ct["verdict"] == "unknown")
        sub = detect_for_assets(h41, ["asan", "compile-time"], rv=rv)
        chk("子集 OR 含 catch ⇒ 整条 catch", sub["verdict"] == "catch")
        chk("子集结果含逐资产判定", set(sub["per_asset"]) == {"asan", "compile-time"})
        chk("compile-time 的 unknown 进了 unknown_reasons", "compile-time" in sub["unknown_reasons"])
        ct_only = detect_for_assets(h41, ["compile-time"], rv=rv)
        chk("只选 compile-time ⇒ unknown（不当 miss）", ct_only["verdict"] == "unknown")
        # 适配层卸载后全局 subprocess 必须还原
    chk("适配层已卸载（subprocess.run 还原）", subprocess.run is _ORIG_RUN)
    chk("适配层卸载后 env 已还原", os.environ.get("WSL_UTF8") is None)

    print(f"detect_for_assets selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="673r：样本 × 资产子集 的真实逐资产判定")
    ap.add_argument("--dataset", choices=("holdout", "corpus", "both"), default=None)
    ap.add_argument("--limit", type=int, default=None, help="只跑前 N 条样本（冒烟用）")
    ap.add_argument("--out", default=str(OUT_DEFAULT))
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--probe", action="store_true", help="只探测 WSL 横幅/环境")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--aggregation", choices=tuple(_ac.AGGREGATION_RULES),
                    default=_ac.DEFAULT_AGGREGATION,
                    help="707-B / 700-F P3：聚合规则**显式声明**（默认 or，对零产资产免疫；mean 会被稀释）")
    a = ap.parse_args(argv)

    if a.aggregation == "mean":
        print("[707-B / 700-F P3] 警告：mean 聚合会被零产资产稀释"
              "（8 vs 6 资产稀释因子 1.3333）；报告须显式声明聚合规则。", flush=True)

    if a.probe:
        print(json.dumps(probe_wsl_banner(), ensure_ascii=False, indent=2))
        return 0
    if a.check:
        return selftest()
    if not a.dataset:
        ap.print_help()
        return 0

    datasets = ["holdout", "corpus"] if a.dataset == "both" else [a.dataset]
    out = Path(a.out)
    if not out.is_absolute():                 # 相对路径按仓库根解析（673r 首次运行在此崩过）
        out = ROOT / out
    doc = attribution_doc(datasets, limit=a.limit, out_path=None if a.no_write else out,
                          rule=a.aggregation)
    doc["fidelity_vs_frozen"] = fidelity_report(doc)

    if a.json:
        print(json.dumps(doc, ensure_ascii=False, indent=1))
    else:
        for ds, part in doc["datasets"].items():
            from collections import Counter
            c = Counter(r["or_verdict"] for r in part["samples"])
            print(f"[673r] {ds}: n={part['n_measurable']} OR 判定 {dict(c)} "
                  f"| 墙钟 {part['wall_seconds_total']:.1f}s")
        for ds, f in doc["fidelity_vs_frozen"].items():
            print(f"[673r] 保真 {ds}: {f['agree']}/{f['n']} = {f['agree_pct']}%")

    if not a.no_write:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"[673r] 写入 {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
