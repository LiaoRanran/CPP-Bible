#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""false_positive_thymus_671g.py — 671g D3：新规则发布前的误报率"胸腺"阴性选择门禁。

生物学隐喻（671f #117）
========================
胸腺对 T 细胞做**阴性选择**：攻击自身正常组织的细胞不许出胸腺。本项目每条**会对
C++ 代码判错的规则**发布前，必须先过"正确代码库"（已知无缺陷 C++ 集合）这道胸腺：
在正确代码上误报率 **< 阈值（默认 5%）** 才准发布；≥阈值 **block**；
样本不足（< min_samples）判 **inconclusive（warn，不许带过）**——样本太少不能放行。

框架边界（诚实登记）
====================
* 本工具是**框架**：它不自带 67 条规则的 C++ 检查器（gate_engine 的 67 条是**卡内容/
  治理规则**，不是可对 .cpp 运行的静态检查）。规则→检查器在 config 里以
  ``"tools/<mod>.py::<function>"`` 注册；新增**带代码检查器**的规则时必须一并注册胸腺。
* 正确代码库目录：``data/671g/thymus/clean/``（只放人工确认无缺陷的 .cpp）。

用法
====
    python tools/false_positive_thymus_671g.py --check           # 跑胸腺（exit 1=block）
    python tools/false_positive_thymus_671g.py --register-rule R-ID --checker tools/x.py::f
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SCHEMA = "queyi-thymus/671g"
CONFIG_PATH = Path("data/671g/thymus/config.json")
CLEAN_DIR = Path("data/671g/thymus/clean")
DEFAULT_THRESHOLD = 0.05
DEFAULT_MIN_SAMPLES = 10


def default_config() -> dict[str, Any]:
    return {"schema": SCHEMA,
            "clean_dir": CLEAN_DIR.as_posix(),
            "threshold_pct": DEFAULT_THRESHOLD * 100,
            "min_samples": DEFAULT_MIN_SAMPLES,
            "rules": {},
            "note": "rules: {rule_id: {checker: tools/mod.py::fn, files_glob: '*.cpp'}}；"
                    "fn(path)->bool，True=判缺陷（正确代码上 True 即误报）"}


def load_config(root: Path) -> dict[str, Any]:
    p = root / CONFIG_PATH
    if not p.is_file():
        return default_config()
    d = json.loads(p.read_text(encoding="utf-8"))
    return {**default_config(), **d}


def load_checker(root: Path, spec: str) -> Callable[[Path], bool]:
    """``tools/mod.py::fn`` 形式装载检查器。"""
    mod_s, _, fn = spec.partition("::")
    path = root / mod_s
    specm = importlib.util.spec_from_file_location(
        f"_thymus_{path.stem}_{abs(hash(str(path))) & 0xffffff:x}", path)
    mod = importlib.util.module_from_spec(specm)
    specm.loader.exec_module(mod)           # type: ignore[union-attr]
    fn_obj = getattr(mod, fn)
    return lambda p: bool(fn_obj(str(p)))


def evaluate_rule(root: Path, rule_id: str, spec: dict[str, Any],
                 checker: Callable[[Path], bool] | None = None,
                 clean_files: list[Path] | None = None,
                 threshold: float = DEFAULT_THRESHOLD,
                 min_samples: int = DEFAULT_MIN_SAMPLES) -> dict[str, Any]:
    files = clean_files if clean_files is not None else sorted(
        (root / spec.get("clean_dir", CLEAN_DIR.as_posix())).glob(
            spec.get("files_glob", "*.cpp")))
    n = len(files)
    fps: list[str] = []
    if checker is not None:
        for f in files:
            try:
                if checker(f):
                    fps.append(f.name)
            except Exception as e:               # noqa: BLE001  检查器崩在正确代码上也算误报（不可用检查器不许发布）
                fps.append(f"{f.name}（检查器异常 {type(e).__name__}）")
    res: dict[str, Any] = {"rule_id": rule_id, "n_clean": n, "false_positive": len(fps),
                             "fp_files": fps}
    if n < min_samples:
        res.update(status="inconclusive", severity="warn",
                  why=f"正确代码样本 {n}<{min_samples}，不足以发布（不许带过）")
    elif len(fps) / n > threshold + 1e-12:
        res.update(status="block", severity="block",
                  why=f"误报率 {len(fps)}/{n}={len(fps)/n*100:.1f}% > 阈值 {threshold*100:.0f}%")
    else:
        res.update(status="pass", severity="ok",
                  why=f"误报率 {len(fps)}/{n} ≤ {threshold*100:.0f}%，通过阴性选择")
    return res


def evaluate(root: Path = ROOT, checkers: dict[str, Callable[[Path], bool]] | None = None,
           ) -> list[dict[str, Any]]:
    cfg = load_config(root)
    th = float(cfg["threshold_pct"]) / 100.0
    mins = int(cfg["min_samples"])
    out: list[dict[str, Any]] = []
    rules = cfg.get("rules") or {}
    if not rules:
        # 没有任何带代码检查器的规则注册 ⇒ 胸腺未进射程（不判红，如实登记）
        return [{"note": "config.rules 为空：67 条现行规则是卡内容/治理规则，无 C++ 检查器；"
                          "新增带代码检查器的规则时必须在此注册，否则该规则发布不受胸腺约束",
                 "status": "unarmed", "severity": "warn"}]
    checkers = checkers or {}
    for rule_id, spec in rules.items():
        chk = checkers.get(rule_id)
        if chk is None and spec.get("checker"):
            try:
                chk = load_checker(root, spec["checker"])
            except Exception as e:                  # noqa: BLE001
                out.append({"rule_id": rule_id, "status": "block", "severity": "block",
                           "why": f"检查器装载失败：{type(e).__name__}: {e}"})
                continue
        if chk is None:
            out.append({"rule_id": rule_id, "status": "block", "severity": "block",
                         "why": "注册了规则但无 checker"})
            continue
        out.append(evaluate_rule(root, rule_id, spec, chk, threshold=th, min_samples=mins))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g D3：误报率胸腺（阴性选择）")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--register-rule", default=None)
    ap.add_argument("--checker", default=None)
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    if a.register_rule:
        cfg = load_config(root)
        cfg.setdefault("rules", {})[a.register_rule] = {"checker": a.checker or "",
                                                           "files_glob": "*.cpp"}
        p = root / CONFIG_PATH
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[thymus] 已注册 {a.register_rule} -> {a.checker}")
        return 0
    res = evaluate(root)
    print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else
          "\n".join(f"  [{r.get('status')}] {r.get('rule_id', '-')}: {r.get('why', r.get('note', ''))}"
                    for r in res))
    return 1 if any(r.get("severity") == "block" for r in res) else 0


if __name__ == "__main__":
    raise SystemExit(main())
