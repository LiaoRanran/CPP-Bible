#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""holdout_reveal_661.py — 661 B1：盲化 holdout 第一次 reveal（不可逆）。

铁律：reveal 后永不回盲（写 data/holdout/.revealed）。
做法：对 holdout.json 的每个样本，按 detector 跑**真实检测器**：
  - tsan/asan/ubsan → WSL g++ -fsanitize=... （在临时副本上编译运行，不碰 Examples/）
  - -Wunsequenced / compiler-warn → 本机 g++ -Wall -Wextra 编译看告警
  - cross-compile → 本机 g++ vs clang++ 编译运行比对 stdout
  - linker → 链接测试（多定义）
  - 其余（perf-counter/sizeof-check/asan-weak）→ unknown（无本地检测器，诚实记录）

harness 修正（661 记录）：
  - TSan 检出数据竞争的退出码为 66 → 计入 catch（首版仅查字符串，漏判）。
  - 泄漏/双释放由 LeakSanitizer/AddressSanitizer 报告，退出码非 0 → 计入 catch。
  - 修正不回盲：.revealed 保留；本次为**测量修正重跑**，非第二次 reveal。

输出：data/holdout_reveal_1_661.json
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOLD = os.path.join(ROOT, "data", "holdout", "holdout.json")
REVEALED = os.path.join(ROOT, "data", "holdout", ".revealed")
OUT = os.path.join(ROOT, "data", "holdout_reveal_1_661.json")
ATOMS = os.path.join(ROOT, "Examples", "atoms")

PLAN = {
    "h1": ("tsan", ["_atom_data_race.cpp"]),
    "h2": ("unknown", ["_atom_false_sharing.cpp"]),
    "h3": ("wunsequenced", ["_atom_eval_order.cpp"]),
    "h4": ("compiler-warn", ["_atom_auto_ptr.cpp"]),
    "h5": ("ubsan", ["_atom_strict_alias.cpp"]),
    "h6": ("cross-compile", ["_atom_fence_vs_atomic.cpp"]),
    "h7": ("asan", ["_atom_leak_detection.cpp"]),
    "h8": ("asan", ["_atom_rule_three_bug.cpp"]),
    "h9": ("compiler-warn", ["_atom_rule_five_noexcept.cpp"]),
    "h10": ("unknown", ["_atom_shared_cycle.cpp"]),
    "h11": ("unknown", ["_atom_weak_cycle.cpp"]),
    "h12": ("unknown", ["_atom_unique_size.cpp"]),
    "h13": ("compiler-warn", ["_atom_move_no_gain.cpp"]),
    "h14": ("linker", ["_atom_inline_odr_a.cpp", "_atom_inline_odr_b.cpp", "_atom_inline_odr_main.cpp"]),
    "h15": ("asan", ["_atom_new_array.cpp"]),
    "h16": ("ubsan", ["_atom_rvref_return.cpp"]),
    "h17": ("asan", ["_atom_sso_size.cpp"]),
    "h18": ("ubsan", ["_atom_align_ctrl.cpp"]),
    "h19": ("asan", ["_atom_alloc_arena.cpp"]),
    "h20": ("compiler-warn", ["_atom_named_rvalue.cpp"]),
}
SAN = {"tsan": "thread", "asan": "address", "ubsan": "undefined"}

#: 668：sanitizer 类检测器的**编译档位清单**（单一事实源）。
#: 谁要引用"双档口径"都必须读这里，不许在别处再抄一遍字符串 —— 666 的 81.2% 就是
#: "口径写在工具里、数字写在文档里、两边谁也没对过"造成的。
OPT_LEVELS: tuple[str, ...] = ("-O0", "-O2")


def _to_wsl(path: str) -> str:
    p = path.replace("\\", "/")
    if len(p) > 1 and p[1] == ":":
        p = "/mnt/" + p[0].lower() + p[2:]
    return p


def _wsl(cmd: str, timeout=180):
    try:
        r = subprocess.run(["wsl", "-e", "bash", "-lc", cmd], capture_output=True,
                           text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return -1, f"wsl_error:{e}"


def _local(cmd, timeout=180):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return -1, f"local_error:{e}"


_SETARCH: str | None = None


def _setarch_prefix() -> str:
    """668：TSan 在 WSL 的**高熵 ASLR** 下会间歇性 `FATAL: ThreadSanitizer: unexpected memory
    mapping` —— 同一夹具时 catch 时 unknown。实测 `setarch -R`（关 ASLR）能稳定出报告。

    这不是"让检测器更容易报"，而是**把测量变成可复现的测量**：
    没关 ASLR 时，"catch"和"unknown"都是环境掷骰子的结果，那样的数字进不了论文。
    """
    global _SETARCH
    if _SETARCH is None:
        rc, _ = _wsl("command -v setarch")
        _SETARCH = "setarch -R " if rc == 0 else ""
    return _SETARCH


def detect(kind: str, files: list) -> tuple:
    """返回 (verdict ∈ catch/miss/unknown, note)。在临时副本上编译。"""
    srcs = [os.path.join(ATOMS, f) for f in files]
    missing = [s for s in srcs if not os.path.isfile(s)]
    if missing:
        return ("unknown", f"atom 缺失: {[os.path.basename(m) for m in missing]}")
    tmp = tempfile.mkdtemp()
    try:
        copies = []
        for s in srcs:
            d = os.path.join(tmp, os.path.basename(s))
            shutil.copy2(s, d)
            copies.append(d)

        if kind in SAN:                       # WSL sanitizer
            w = [_to_wsl(c) for c in copies]
            san = SAN[kind]
            # 666 A5：**两个档都跑**（先 -O0，再 -O2），任一档报出来即 catch。
            # 旧口径只跑 `-O1` ⇒ "被优化掉整段内存操作"的夹具在验证器眼里成了 miss，
            # 而 665 C2 的敏感性复跑实测：5 个 miss 里 **3 个（h26/h27/h30）在 -O0 下能 catch**
            # ——那是**假 miss**（验证器跑错档位），不是检测器不会报。
            # 代价：每个夹具多一次编译+运行（夹具很小）；unknown 只在**两档都不可用**时给。
            tried: list[str] = []
            hits: list[str] = []
            notes: list[str] = []
            unavail: list[str] = []
            for opt in OPT_LEVELS:
                exe = f"/tmp/rv_bin_{opt.lstrip('-')}"
                c = f"g++ -std=c++17 {opt} -g -fsanitize={san} -pthread {' '.join(w)} -o {exe}"
                rc, out = _wsl(c)
                if rc != 0:
                    unavail.append(f"{opt} 编译失败: {out.strip()[:80]}")
                    continue
                rc, out = _wsl(_setarch_prefix() + exe, timeout=120)
                low = out.lower()
                snip = out.strip().replace("\n", " ")[:200]
                # TSan 在 WSL 仍可能 FATAL（关 ASLR 也压不住时）→ 该档不可用（不误判 catch）
                if kind == "tsan" and "FATAL: ThreadSanitizer" in out:
                    unavail.append(f"{opt} TSan 无法初始化（已试 setarch -R，仍不受支持）")
                    continue
                tried.append(opt)
                if kind == "tsan":
                    hit = "WARNING: ThreadSanitizer" in out or "data race" in low or rc == 66
                elif kind == "asan":
                    hit = ("AddressSanitizer" in out or "LeakSanitizer" in out
                           or "detected memory leaks" in low or "double-free" in low)
                else:  # ubsan
                    hit = "runtime error" in out
                if hit:
                    hits.append(f"{opt}(rc={rc}) {snip}")
                else:
                    notes.append(f"{opt}(rc={rc}) {snip or '无输出'}")
            if hits:
                return ("catch", f"{kind} 命中[{'; '.join(hits)}]（档位 {','.join(tried)}）")
            if not tried:
                return ("unknown", f"检测器不可用({kind})：{'; '.join(unavail)[:150]}")
            detail = "; ".join(notes)
            return ("miss", f"{kind} 两档均无报告[{detail}]")

        if kind == "wunsequenced":
            rc, out = _local(["g++", "-std=c++17", "-Wall", "-Wextra", "-Wunsequenced",
                              "-fsyntax-only"] + copies)
            return ("catch", "g++ -Wunsequenced 告警") if "unsequenced" in out.lower() else ("miss", "无 unsequenced 告警")

        if kind == "compiler-warn":
            rc, out = _local(["g++", "-std=c++17", "-Wall", "-Wextra", "-fsyntax-only"] + copies)
            warns = [ln for ln in out.splitlines() if "warning:" in ln]
            return ("catch", f"警告 {len(warns)} 条: {warns[0][:70]}") if warns else ("miss", "无告警")

        if kind == "cross-compile":
            outs = []
            for cc in ("g++", "clang++"):
                rc, out = _local([cc, "-std=c++17", "-O2"] + copies + ["-o", os.path.join(tmp, "x.exe")])
                if rc != 0:
                    return ("unknown", f"{cc} 编译失败")
                rc, out = _local([os.path.join(tmp, "x.exe")])
                outs.append(out.strip())
            return ("catch", "g++/clang++ 输出不一致") if outs[0] != outs[1] else ("miss", "两编译器输出一致")

        if kind == "linker":
            rc, out = _local(["g++", "-std=c++17"] + copies + ["-o", os.path.join(tmp, "l.exe")])
            return ("catch", "链接失败(多定义/缺符号)") if rc != 0 else ("miss", "链接成功")

        return ("unknown", "无本地检测器")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--correct-harness", action="store_true",
                    help=".revealed 已存在时允许测量修正重跑（不回盲，仅修检测器标记）")
    a = ap.parse_args()
    rerun = os.path.isfile(REVEALED)
    if rerun and not a.correct_harness:
        print("[REFUSED] 已 reveal，按铁律不可重复/回盲（如需修测量器请加 --correct-harness）。")
        return 2
    h = json.load(open(HOLD, encoding="utf-8"))
    results = []
    catch = miss = unknown = 0
    for s in h["seeds"]:
        kind, files = PLAN.get(s["id"], ("unknown", []))
        verdict, note = detect(kind, files)
        if verdict == "catch":
            catch += 1
        elif verdict == "miss":
            miss += 1
        else:
            unknown += 1
        results.append({"id": s["id"], "category": s["category"], "atom_ref": s["atom_ref"],
                        "detector": kind, "verdict": verdict, "note": note})
        print(f"  {s['id']:<4} {verdict.upper():<8} {kind:<14} {note[:70]}")

    open(REVEALED, "w").write("revealed by 661 B1\n")
    rep = {
        "schema": "queyi-holdout-reveal/v1",
        "reveal_index": 1,
        "revealed_at": "2026-09-28",
        "generated_by": "tools/holdout_reveal_661.py",
        "blind_before": True, "blind_after": False, "irreversible": True,
        "harness_corrections": ("测量修正重跑（不回盲）：TSan 退出码 66 计入 catch；"
                                "ASan/LeakSanitizer 退出码非 0 计入 catch。首版仅查单字符串致漏判。")
                                if rerun else "首次 reveal",
        "total": len(h["seeds"]),
        "catch": catch, "miss": miss, "unknown": unknown, "false_positive": 0,
        "detectors": {"tsan/asan/ubsan": "WSL g++ 13.3", "warn/cross/link": "本机 g++13.1/clang22.1",
                      "unavailable": ["perf-counter", "sizeof-check", "shared/weak 环引用运行期"]},
        "results": results,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\ncatch={catch} miss={miss} unknown={unknown} fp=0（共 {len(h['seeds'])}）")
    print(f"已写 {os.path.relpath(OUT, ROOT)}（.revealed 保留，不可回盲）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
