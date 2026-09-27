#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""replay_probe_651.py — T5 reproduce manifest（651 W2，**信任资产**）。

为什么（651 W2-T5）：648 十张 C 卡的 L1 结论若不记"怎么复现"，一年后没人能重跑。
本工具把 648 的实测**固化成可执行 manifest**：每张卡一条 = 版本串 + 命令 + 输入哈希 +
期望输出哈希/kv；并给出**单命令验收** `replay_probe_651.py <ID>`（ID = decay/malloc/...）。

用法
====
    python tools/replay_probe_651.py --check              # 合成自检（不编译）
    python tools/replay_probe_651.py --build              # 从 648_c_probe.json 建 manifest → data/651_t5_manifest.json
    python tools/replay_probe_651.py decay                # 单命令验收：校验输入哈希 + 重跑 + 比对期望
    python tools/replay_probe_651.py --list

诚实边界：
- 真实探针需 gcc/clang 在 PATH；**缺编译器 ⇒ 报 `compiler_unavailable`，不伪造结果**。
- 只比对 648 已记录的主档位（优先 gcc -std=c11 -O2）；其它档位在 manifest 里保留但不在默认验收内。
- 产物写 `build/c651/`（构建产物，非受控文件）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "trust_asset", "name": "replay_probe_651", "entry": "probe",
                "description": "T5 648 十卡 reproduce manifest + 单命令验收"}

PROBE_648 = ROOT / "data" / "648_c_probe.json"
OUT = ROOT / "data" / "651_t5_manifest.json"
KV_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(-?\d+)$")


def _sha256_file(p: Path) -> str | None:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None


def choose_primary(fx: dict) -> tuple[str | None, dict]:
    """优先 gcc / clang × c11 × -O2；退化取第一个可用 run。"""
    runs = fx.get("runs", {})
    for comp in ("gcc", "clang"):
        for std in ("c11", "c17", "c23"):
            opt = runs.get(comp, {}).get(std, {}).get("-O2")
            if opt and opt.get("supported") and opt.get("compile_rc") == 0:
                return opt.get("cmd"), opt.get("kv", {})
    for comp, stds in runs.items():
        for std, opts in stds.items():
            for o, r in opts.items():
                if r.get("supported") and r.get("compile_rc") == 0:
                    return r.get("cmd"), r.get("kv", {})
    return None, {}


def build_manifest() -> dict:
    d = json.loads(PROBE_648.read_text(encoding="utf-8"))
    entries = []
    for name, fx in d.get("fixtures", {}).items():
        cmd, expected = choose_primary(fx)
        entries.append({
            "id": name,
            "fixture": fx.get("fixture"),
            "fixture_sha256": _sha256_file(ROOT / fx["fixture"]) if fx.get("fixture") else None,
            "cmd": cmd,
            "expected_kv": expected,
            "asm_path": fx.get("asm", {}).get("path"),
            "asm_sha256": fx.get("asm", {}).get("sha256"),
        })
    return {"source": str(PROBE_648.relative_to(ROOT)), "compilers": d.get("compilers", {}),
            "count": len(entries), "entries": entries}


def parse_kv(stdout: str) -> dict:
    out: dict[str, int] = {}
    for ln in stdout.splitlines():
        m = KV_RE.match(ln.strip())
        if m:
            out[m.group(1)] = int(m.group(2))
    return out


def probe(entry: dict, timeout: int = 60) -> dict:
    """校验输入哈希 + 重跑 + 比对期望（单条验收）。"""
    res = {"id": entry["id"], "accept": False}
    if not entry.get("cmd"):
        res["reason"] = "no_cmd_in_manifest"
        return res
    fx = ROOT / entry["fixture"]
    if not fx.is_file():
        res["reason"] = "fixture_missing"
        res["fixture"] = entry["fixture"]
        return res
    cur = _sha256_file(fx)
    if entry.get("fixture_sha256") and cur != entry["fixture_sha256"]:
        res["reason"] = "input_hash_mismatch"
        res["expected_sha256"], res["actual_sha256"] = entry["fixture_sha256"][:16], (cur or "")[:16]
        return res
    # 重定向输出到 build/c651
    cmd = entry["cmd"].replace("build/c648/", "build/c651/")
    try:
        argv = shlex.split(cmd)
    except ValueError:
        argv = cmd.split()
    # 确保 -o 输出目录存在（否则 ld 报 cannot open output file）
    if "-o" in argv:
        out_path = ROOT / argv[argv.index("-o") + 1]
        out_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        p = subprocess.run(argv, cwd=str(ROOT), capture_output=True, text=True, timeout=timeout, check=False)
    except FileNotFoundError:
        res["reason"] = "compiler_unavailable"
        return res
    except subprocess.TimeoutExpired:
        res["reason"] = "timeout"
        return res
    if p.returncode != 0:
        res["reason"] = "compile_failed"
        res["stderr"] = p.stderr[-300:]
        return res
    # 648 的 cmd 只负责**编译**；再运行生成的 exe 取 stdout
    if "-o" not in argv:
        res["reason"] = "no_output_exe"
        return res
    exe = ROOT / argv[argv.index("-o") + 1]
    try:
        rp = subprocess.run([str(exe)], cwd=str(ROOT), capture_output=True, text=True,
                            timeout=timeout, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:  # noqa: PERF203
        res["reason"] = "run_failed"
        res["stderr"] = str(e)[:200]
        return res
    got = parse_kv(rp.stdout)
    exp = {k: int(v) for k, v in entry.get("expected_kv", {}).items()}
    res["expected"] = exp
    res["actual"] = got
    res["accept"] = (got == exp)
    if not res["accept"]:
        res["reason"] = "output_mismatch"
    return res


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("解析 kv", parse_kv("a=1\nb=-2\nnoise\n") == {"a": 1, "b": -2})
    chk("忽略非 kv 行", parse_kv("bf_sizeof=4\n# x\n") == {"bf_sizeof": 4})
    fx = {"runs": {"clang": {"c11": {"-O2": {"supported": True, "compile_rc": 0, "cmd": "clang ...", "kv": {"a": 1}}}},
                   "gcc": {"c11": {"-O2": {"supported": True, "compile_rc": 0, "cmd": "gcc ...", "kv": {"a": 2}}}}}}
    cmd, kv = choose_primary(fx)
    chk("优先 gcc", cmd == "gcc ..." and kv == {"a": 2}, str(cmd))
    fx2: dict = {"runs": {}}
    chk("无可用 run ⇒ (None, {})", choose_primary(fx2) == (None, {}))
    print(f"replay_probe_651 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="651 T5 reproduce manifest + 单命令验收")
    ap.add_argument("probe_id", nargs="?", default=None, help="验收集 ID（decay/malloc/...）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.build:
        m = build_manifest()
        OUT.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"manifest {m['count']} 条 → {OUT.name}")
        return 0
    if a.list or not a.probe_id:
        m = build_manifest()
        print("\n".join(f"  {e['id']:10s} cmd={'有' if e['cmd'] else '无'} keys={len(e['expected_kv'])}" for e in m["entries"]))
        return 0
    m = build_manifest()
    entry = next((e for e in m["entries"] if e["id"] == a.probe_id), None)
    if entry is None:
        print(f"未知 ID: {a.probe_id}")
        return 2
    rep = probe(entry)
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0 if rep["accept"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
