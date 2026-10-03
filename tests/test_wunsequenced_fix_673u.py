#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_wunsequenced_fix_673u.py — 673u：`holdout_reveal_661.detect` 的 wunsequenced 恒 catch 修复。

病（673u 修复前）
=================
本机 MinGW g++ 13.1 **不认** `-Wunsequenced`，编译输出
    g++.exe: error: unrecognized command-line option '-Wunsequenced'
而命中判定是 `"unsequenced" in out.lower()` ⇒ 把**选项报错**里的 "unsequenced" 当成命中
⇒ 该资产对**任何**样本恒返回 catch（常量资产）。

后果（已在 673r 报告 §4.2 登记，673u 修复）：
  * 673r 的 840 次真实矩阵里 wunsequenced = holdout 41/41、corpus 64/64 全 catch；
  * A5 主分析被天花板压死（Δ≡0、p≡1，判「不可解释」）；
  * holdout 对照样本 h3 / h35 被记成假阳性（control false_positive 2/11）。

本文件锁住三件事：
  1. 修复后的行为：`-Wunsequenced` 不被编译器认 ⇒ **unknown**（不是 catch，也不是 miss）；
  2. 红线：修复只动 wunsequenced 分支——其他资产的命中判定原样（源码级 + 行为级各一道）；
  3. 诚实边界：unknown 的 note 必须说明根因（编译器不认该选项），不许静默。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / rel))
    if spec is None or spec.loader is None:
        raise ImportError(rel)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


RV = _load("rv661_673u", "tools/holdout_reveal_661.py")

# h3 的夹具（Examples/atoms 下，661 PLAN 里指派给 wunsequenced 的样本）
EVAL_ORDER = "_atom_eval_order.cpp"


# ── 1. 修复后的行为：unknown，不是 catch / miss ─────────────────────────────
def test_wunsequenced_is_unknown_not_catch():
    verdict, note = RV.detect("wunsequenced", [EVAL_ORDER])
    assert verdict == "unknown", f"修复失败：仍是 {verdict}（note={note[:80]}）"


def test_wunsequenced_note_names_the_root_cause():
    """诚实边界：unknown 的 note 必须说清是"检测器不可用"，不许静默。"""
    _, note = RV.detect("wunsequenced", [EVAL_ORDER])
    assert "不可用" in note, note
    assert "-Wunsequenced" in note, note


def test_wunsequenced_unknown_is_not_counted_as_miss_or_catch():
    """unknown 不得被四态逻辑吞掉：三种 verdict 互斥且各归各类。"""
    v, _ = RV.detect("wunsequenced", [EVAL_ORDER])
    assert v in ("catch", "miss", "unknown")
    assert v != "catch" and v != "miss"


# ── 2. 红线：其他资产的命中判定一行未动 ─────────────────────────────────────
def test_source_keeps_both_unrecognized_variants():
    """`unrecognized command-line option` 与 `unrecognized option` 两个变体都要认
    （前者是 gcc 的完整报错，后者是缩写形态；只认其一会在别的工具链上漏判）。"""
    src = (TOOLS / "holdout_reveal_661.py").read_text(encoding="utf-8")
    assert "unrecognized command-line option" in src
    assert '"unrecognized option"' in src


def test_source_keeps_original_hit_predicate_after_the_guard():
    """修复是**前置**一道 unknown 拦截，原命中判定必须原样保留（不许顺手改语义）。"""
    src = (TOOLS / "holdout_reveal_661.py").read_text(encoding="utf-8")
    assert '"unsequenced" in low' in src, "原命中判定被改掉 ⇒ 越权改动"
    assert "无 unsequenced 告警" in src


def test_source_keeps_two_tier_opt_levels_and_setarch():
    """红线：-O0/-O2 双档、setarch -R、TSan 不可用判定全部原样。"""
    assert tuple(RV.OPT_LEVELS) == ("-O0", "-O2")
    assert RV.SAN == {"tsan": "thread", "asan": "address", "ubsan": "undefined"}
    src = (TOOLS / "holdout_reveal_661.py").read_text(encoding="utf-8")
    assert "setarch -R" in src and "FATAL: ThreadSanitizer" in src


def test_other_local_assets_verdicts_unchanged():
    """行为级：compiler-warn / linker 的判定与修复前一致（真编译，秒级）。"""
    assert RV.detect("compiler-warn", ["_atom_auto_ptr.cpp"])[0] == "catch"
    assert RV.detect("linker", ["_atom_inline_odr_a.cpp", "_atom_inline_odr_b.cpp",
                                "_atom_inline_odr_main.cpp"])[0] == "catch"


def test_detect_signature_unchanged():
    """673r 的守卫同款：detect 仍是 2 元签名（kind, files）。"""
    assert RV.detect.__code__.co_argcount == 2
    assert RV.detect.__code__.co_varnames[:2] == ("kind", "files")
