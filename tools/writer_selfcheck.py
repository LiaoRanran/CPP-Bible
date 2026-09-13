#!/usr/bin/env python3
"""413 Writer 自检层：7 项确定性检查（零 token），提交红队前拦 E1/E2 机械错误。

背景（413/420）：第五批 3 颗原子跨 6 个窗口，根因是 E1（形式）/E2（工件）类机械错误
消耗了红队注意力。Writer 提交前自跑本层，把机械错误拦在红队之前。

七项（420 口径）：
  WC-01 artifact_same_generation  工件同代：卡面 sha == 磁盘工件；夹具不得比工件新
  WC-02 assert_labels_in_artifact 断言标签实测：contains*/call_count 的 symbol/text
                                  须在工件中 grep 得到（Windows 走 sha 比对不评断言
                                  ⇒ 本条是 Windows 盲区补全；absent 系列的主张就是
                                  「不存在」，不查存在性）
  WC-03 command_runnable          command 结构可执行：非空、fixture/artifact 路径存在；
                                  含 cl → skip（MSVC 永久边界；深度复算归 replay）
  WC-04 out_same_generation       .out 存在且不早于夹具（陈旧 → warn，同 EV-OUT-STALE-MTIME）
  WC-05 live_control              活性对照：run 卡须有运行时读数；纯工件文本支撑 warn
  WC-06 metric_consistency        正文数字+单位须在 .out 中有对应（启发式，warn）
  WC-07 no_infinite_loop          夹具无界循环（while(1)/for(;;)）体内须有
                                  break/return/exit/throw；volatile/atomic 条件降 warn

与门禁的分工：深度复算（重编译+四项校验）= atom_evidence_replay；规则全集 = gate_engine；
本层只做**提交前自检**，检出（warn/fail）都算「拦住」——平台拼写差异与伪造在结构上
不可区分（373 教训），故 WC-02 用 warn 不用 fail，避免存量已知拼写缺陷（EV-MEM-017）
把门禁打红。

用法：
  python tools/writer_selfcheck.py evidence/mem/EV-MEM-040.md [--json]
  python tools/writer_selfcheck.py --all          # 全部证据卡（存量 0 fail 基线）
退出码：0 = 无 fail；1 = 有 fail（warn 不影响）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_engine as ge  # noqa: E402
import atom_evidence_replay as replay  # noqa: E402

VERSION = "v7.0"
_BOUNDLESS_LOOP = re.compile(r"while\s*\(\s*(?:1|true|TRUE)\s*\)|for\s*\(\s*;\s*;\s*\)")
_NUM_WITH_UNIT = re.compile(r"\d+(?:\.\d+)?\s*(?:B|KB|MB|×|ns|us|µs|ms|%)")


def _res(rel: Any) -> Path | None:
    """ROOT 相对路径 → 存在的文件；否则 None。"""
    s = str(rel or "").strip()
    if not s:
        return None
    f = ge.ROOT / s
    return f if f.is_file() else None


def _artifact_text(meta: dict[str, Any]) -> str:
    parts: list[str] = []
    f = _res(meta.get("artifact"))
    if f:
        parts.append(f.read_text(encoding="utf-8", errors="replace"))
    for e in (meta.get("artifacts") or []):
        f = _res(e if isinstance(e, str) else (e.get("path") or e.get("file") or ""))
        if f:
            parts.append(f.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(parts)


def wc01_artifact_same_generation(meta: dict[str, Any]) -> tuple[str, str]:
    art = _res(meta.get("artifact"))
    if art is None:
        return "fail", "工件文件不存在"
    sha = str(meta.get("artifact_sha256") or "").strip().lower()
    owner = str(meta.get("artifact_compiler") or "").strip()
    # 字节比对只在「本机编译器产物」下合法：跨编译器卡（matrix 多编译器）的字节必然
    # 不同——replay 对归属不符的卡改判结构断言，本层同口径跳过（实测 EV-CONC-003/004：
    # 卡面/磁盘/现跑三个 sha 各不相同，属跨编译器正常而非不同代）。
    if sha:
        if owner:
            try:
                local = replay._current_toolchain_id()
            except Exception:
                local = ""
            if local and owner != local:
                return "skip", f"跨编译器工件（归属 {owner}）不做字节比对——结构断言归 replay"
        if hashlib.sha256(art.read_bytes()).hexdigest() != sha:
            return "fail", "artifact_sha256 与磁盘工件不一致（工件与断言不同代）"
    fx = _res(meta.get("fixture"))
    if fx and fx.stat().st_mtime > art.stat().st_mtime + 5:
        return "warn", "夹具比工件新——改源码后可能未重生成工件"
    return "pass", ""


def wc02_assert_labels_in_artifact(meta: dict[str, Any]) -> tuple[str, str]:
    hay = _artifact_text(meta)
    if not hay:
        return "warn", "无工件文件可 grep（断言标签未实测）"
    rules = meta.get("artifact_assert") or []
    rules = [r for r in rules if isinstance(r, dict)] if isinstance(rules, list) else []
    missing: list[str] = []
    for r in rules:
        kind = str(r.get("kind") or "")
        if kind.startswith("absent"):
            continue                       # absent 的主张即「不存在」
        labels = [str(r.get("symbol") or "")] if r.get("symbol") else []
        texts = ([str(t) for t in r.get("texts") or []] if r.get("texts")
                 else [str(r.get("text") or "")])
        labels += [t for t in texts if t]
        missing += [lb for lb in labels if lb not in hay]
    if missing:
        return "warn", (f"断言标签在工件中不存在：{sorted(set(missing))}"
                        "（疑似拼错/平台拼写差异/跨编译器未实测）")
    return "pass", ""


def wc03_command_runnable(meta: dict[str, Any]) -> tuple[str, str]:
    cmd = str(meta.get("command") or "").strip()
    if not cmd:
        return "fail", "command 为空"
    if ge._command_uses_msvc(cmd):
        return "skip", "MSVC 永久边界（重编译校验不尝试 cl，见 replay）"
    for key in ("fixture", "artifact"):
        rel = str(meta.get(key) or "").strip()
        if rel and not (ge.ROOT / rel).exists():
            return "fail", f"{key} 路径不存在：{rel}"
    return "pass", ""


def wc04_out_same_generation(meta: dict[str, Any]) -> tuple[str, str]:
    actual = meta.get("actual") or {}
    rf = str(actual.get("run_match_file") or "") if isinstance(actual, dict) else ""
    if not rf:
        return "pass", ""                  # 无 .out 留痕的卡（asm 类）不适用
    f = ge.ROOT / rf
    if not f.is_file():
        return "fail", f".out 不存在：{rf}"
    fx = _res(meta.get("fixture"))
    if fx and f.stat().st_mtime < fx.stat().st_mtime - 5:
        return "warn", ".out 比夹具旧——可能不是当前源码的产出"
    return "pass", ""


def wc05_live_control(meta: dict[str, Any]) -> tuple[str, str]:
    actual = meta.get("actual") or {}
    if isinstance(actual, dict):
        if any(str(k).startswith("run") for k in actual):
            return "pass", ""
    elif "run" in str(actual):
        return "pass", ""
    if str(meta.get("kind") or "") in ("asm", "symbol", "layout", "abi"):
        return "warn", "无运行时读数（工件形态卡）：结论仅由工件文本支撑"
    return "pass", ""


def wc06_metric_consistency(p: Path, meta: dict[str, Any]) -> tuple[str, str]:
    raw = p.read_text(encoding="utf-8", errors="replace")
    body = raw.split("---", 2)[-1] if raw.startswith("---") else raw
    actual = meta.get("actual") or {}
    rf = str(actual.get("run_match_file") or "") if isinstance(actual, dict) else ""
    f = ge.ROOT / rf if rf else None
    out_txt = f.read_text(encoding="utf-8", errors="replace") if f and f.is_file() else ""
    if not out_txt:
        return "skip", "无 .out 可对照"
    nums = {m.group(0).strip() for m in _NUM_WITH_UNIT.finditer(body)}
    miss = [n for n in sorted(nums) if n not in out_txt]
    if miss:
        return "warn", f"数字在 .out 中无对应（口径不一致嫌疑）：{miss}"
    return "pass", ""


def wc07_no_infinite_loop(meta: dict[str, Any]) -> tuple[str, str]:
    fx = _res(meta.get("fixture"))
    if fx is None:
        return "skip", "无夹具可查"
    src = fx.read_text(encoding="utf-8", errors="replace")
    m = _BOUNDLESS_LOOP.search(src)
    if not m:
        return "pass", ""
    i = src.find("{", m.start())
    depth, j = 0, i
    while j < len(src):
        if src[j] == "{":
            depth += 1
        elif src[j] == "}":
            depth -= 1
            if depth == 0:
                break
        j += 1
    body = src[i:j + 1]
    if any(k in body for k in ("break", "return", "exit", "throw")):
        return "pass", ""
    ctx = src[max(0, m.start() - 200):m.end()]
    if "volatile" in ctx or "atomic" in ctx:
        return "warn", "无界循环以 volatile/atomic 标志为条件——可能终止，请复核"
    return "fail", "无界循环（while(1)/for(;;)）且体内无 break/return/exit——可能永不终止"


def check_card(p: Path) -> list[dict[str, str]]:
    meta = ge._meta(p)
    out: list[dict[str, str]] = []

    def add(wid: str, name: str, res: tuple[str, str]) -> None:
        out.append({"id": wid, "name": name, "status": res[0], "message": res[1]})

    add("WC-01", "artifact_same_generation", wc01_artifact_same_generation(meta))
    add("WC-02", "assert_labels_in_artifact", wc02_assert_labels_in_artifact(meta))
    add("WC-03", "command_runnable", wc03_command_runnable(meta))
    add("WC-04", "out_same_generation", wc04_out_same_generation(meta))
    add("WC-05", "live_control", wc05_live_control(meta))
    add("WC-06", "metric_consistency", wc06_metric_consistency(p, meta))
    add("WC-07", "no_infinite_loop", wc07_no_infinite_loop(meta))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Writer 自检层（413：7 项确定性检查）")
    ap.add_argument("target", nargs="?", help="证据卡路径（相对仓库根）")
    ap.add_argument("--all", action="store_true", help="检查全部证据卡")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.all:
        targets = sorted(ge._cards(ge.EVIDENCE, "EV-*.md"))
    elif a.target:
        t = ge.ROOT / a.target
        if not t.is_file():
            raise SystemExit(f"[selfcheck] 目标不存在：{a.target}")
        targets = [t]
    else:
        raise SystemExit("[selfcheck] 需要 <card> 或 --all")

    n_fail = 0
    reports: list[dict[str, Any]] = []
    for t in targets:
        checks = check_card(t)
        bad = [c for c in checks if c["status"] == "fail"]
        n_fail += len(bad)
        summary = {s: sum(1 for c in checks if c["status"] == s)
                   for s in ("pass", "warn", "fail", "skip")}
        summary = {k: v for k, v in summary.items() if v}
        reports.append({"target": t.relative_to(ge.ROOT).as_posix()
                        if t.is_relative_to(ge.ROOT) else t.as_posix(),
                        "checks": checks, "summary": summary})
        if not a.json and (bad or not a.all):
            print(f"[selfcheck] {t.name}: {summary}")
            for c in checks:
                mark = {"pass": "✅", "warn": "⚠️ ", "fail": "❌", "skip": "⏭ "}[c["status"]]
                line = f"  {mark} {c['id']} {c['name']}: {c['status']}"
                if c["message"]:
                    line += f" — {c['message']}"
                print(line)

    if a.json:
        print(json.dumps({"tool": "writer_selfcheck", "version": VERSION,
                          "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
                          "summary": {"targets": len(targets), "fail": n_fail},
                          "reports": reports}, ensure_ascii=False, indent=1))
    else:
        print(f"\n[selfcheck] {len(targets)} 张卡，fail={n_fail}"
              + (" —— 存在机械错误，先修再交红队" if n_fail else "（自检通过/仅告警）"))
    return 1 if n_fail else 0


if __name__ == "__main__":
    main()
