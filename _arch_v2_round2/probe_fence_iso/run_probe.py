#!/usr/bin/env python3
"""533 任务2 实测：FENCE-001 阴面构造 + 编译/运行/翻转/diff 全部量真实数据。

沙箱纪律：只读正式夹具 Examples/atoms/_atom_fence_vs_atomic.cpp，
所有变体与产物只落在 _arch_v2_round2/probe_fence_iso/。
"""
from __future__ import annotations

import difflib
import json
import os
import re
import statistics
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROUND2 = HERE.parent
ROOT = ROUND2.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROUND2))

import atom_evidence_replay as R  # noqa: E402
import iso_judge as J  # noqa: E402

OFFICIAL = ROOT / "Examples" / "atoms" / "_atom_fence_vs_atomic.cpp"
ANCHOR = "spin_signal_fence"
PROBE_SYMBOL = "_Z17spin_signal_fencev"
REMOVE_TEXT = "__atomic_signal_fence(__ATOMIC_SEQ_CST);"
RETAIN = ["while (!s_sf_b)", "return s_sf_a;"]
RUN_KEYS = ["spin_plain_ret", "spin_fence_outside_ret", "functions_present"]

FENCE_LINE = "        __atomic_signal_fence(__ATOMIC_SEQ_CST);\n"


def gen_variants(yang: str) -> dict[str, str]:
    """所有变换都做前置断言，夹具漂移即 fail，不静默写错。"""
    v: dict[str, str] = {}

    # ① 真阴面：删掉 spin_signal_fence 循环体内的 fence（锚定函数，勿误删 writer 侧同名行）
    span = J.find_func_span(yang, ANCHOR)
    assert span, "anchor not found"
    lines = yang.split("\n")
    body_idx = [i for i in range(span[0], span[1]) if lines[i] == FENCE_LINE.rstrip("\n")]
    assert len(body_idx) == 1, f"anchor 内 fence 行数={len(body_idx)}"
    yin = lines[:body_idx[0]] + lines[body_idx[0] + 1:]
    v["yin_del_fence"] = "\n".join(yin)

    # ② 形式阴面攻击：42→43 式（改返回常量；替换形态+探针不翻转）
    src = yang.replace("    s_sf_a = 8;", "    s_sf_a = 9;", 1)
    assert src != yang and src.count("s_sf_a = 9;") == 1
    v["yin_formal_43"] = src

    # ③ 纯删除但删错位置（set_all_flags 里的赋值行）
    src = yang.replace("    s_sf_a = 8;\n", "", 1)
    assert "s_sf_a = 8" not in src
    v["yin_del_unrelated"] = src

    # ④ 连主体带机制一起删（anchor 内定点删 while+fence+} 三行；retain 必须抓住）
    ll = yang.split("\n")
    want = ["    while (!s_sf_b) {",
            "        __atomic_signal_fence(__ATOMIC_SEQ_CST);",
            "    }"]
    hit = [i for i in range(span[0], span[1]) if ll[i] in want]
    assert len(hit) == 3, f"loop_kill 定位 {len(hit)}"
    v["yin_loop_kill"] = "\n".join(x for i, x in enumerate(ll) if i not in hit)

    # ⑦ 诊断对（非候选阴面）：标志置 0 时，阳面挂死、阴面秒回——
    # 证明机制确有运行时后果，但翻转 run 读数必须改第二处（测试支架），故 v1 单变量阴面不含它。
    diag_patch = "    set_all_flags(1); s_sf_b = 0;  // DIAG: 只让 sf 标志保持 0"
    v["diag_yang_hang"] = yang.replace("    set_all_flags(1);", diag_patch, 1)
    v["diag_yin_hang"] = v["yin_del_fence"].replace("    set_all_flags(1);",
                                                    diag_patch, 1)

    # ⑤ 注释走私（零语义 diff）
    src = yang.replace("// ATOM-CONC-001 夹具：",
                       "// ATOM-CONC-001 夹具（阴面注释微调）：", 1)
    v["yin_smuggle_comment"] = src

    # ⑥ 冒名阴面：完全不同的程序
    v["yin_impostor"] = (
        '#include <cstdio>\n'
        'int main() { printf("spin_plain_ret=999|x\\n"); return 0; }\n')
    return v


def timed(cmd: list[str], *, cwd: Path, env: dict, timeout: float = 30.0,
          shell: bool = False) -> dict:
    t0 = time.perf_counter()
    r = subprocess.run(cmd if not shell else " ".join(cmd), cwd=str(cwd),
                       env=env, capture_output=True, text=True,
                       errors="replace", timeout=timeout, shell=shell)
    dt = time.perf_counter() - t0
    return {"dt": dt, "rc": r.returncode, "stdout": r.stdout,
            "stderr": r.stderr[:400]}


def median_runs(n: int, fn) -> float:
    return statistics.median([fn()["dt"] for _ in range(n)])


def symbol_count(asm_text: str, symbol: str, text: str) -> int | None:
    body = R._symbol_body(asm_text.replace("\t", " "), symbol)
    if body is None:
        return None
    return body.count(text)


def parse_kv(stdout: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for ln in stdout.replace("\r", "").split("\n"):
        if "=" in ln:
            k, _, val = ln.partition("=")
            out[k.strip()] = val.strip()
    return out


def main() -> int:
    from toolchain import resolve_gpp
    gpp = resolve_gpp()
    env = dict(os.environ)
    env["PATH"] = str(Path(gpp).parent) + os.pathsep + env["PATH"]

    yang = OFFICIAL.read_text(encoding="utf-8")
    (HERE / "yang.cpp").write_text(yang, encoding="utf-", newline="")
    variants = gen_variants(yang)
    for name, src in variants.items():
        (HERE / f"{name}.cpp").write_text(src, encoding="utf-8", newline="")

    bdir = HERE / "build"
    bdir.mkdir(exist_ok=True)

    def compile_asm(src: Path, out: Path):
        return timed([gpp, "-std=c++23", "-O2", "-S", "-masm=intel",
                      str(src), "-o", str(out)], cwd=HERE, env=env)

    def compile_exe(src: Path, out: Path):
        return timed([gpp, "-std=c++23", "-O2", str(src), "-o", str(out)],
                     cwd=HERE, env=env)

    def run_exe(exe: Path):
        return timed([str(exe)], cwd=HERE, env=env, timeout=10.0)

    report: dict = {"gpp": gpp, "cards": {}}

    def probe(name: str, src: str) -> dict:
        cpp = HERE / f"{name}.cpp"
        asm_p = bdir / f"{name}.s"
        exe_p = bdir / f"{name}.exe"
        asm_t = median_runs(3, lambda: compile_asm(cpp, asm_p))
        exe_t = median_runs(3, lambda: compile_exe(cpp, exe_p))
        asm_rc = compile_asm(cpp, asm_p)["rc"]
        exe_rc = compile_exe(cpp, exe_p)["rc"]
        run = run_exe(exe_p) if exe_rc == 0 else {"rc": None, "stdout": "", "dt": None}
        asm_text = asm_p.read_text(encoding="utf-8", errors="replace") if asm_p.exists() else ""
        counts = {t: symbol_count(asm_text, PROBE_SYMBOL, t)
                  for t in ("s_sf_b", "je", "lock")}
        diff_lines = list(difflib.unified_diff(
            yang.splitlines(), src.splitlines(), lineterm="", n=1))
        v = J.judge_min_diff(yang, src, anchor=ANCHOR,
                             remove_text=REMOVE_TEXT, retain=RETAIN,
                             probe_symbol=PROBE_SYMBOL)
        return {
            "compile_asm_rc": asm_rc, "compile_exe_rc": exe_rc,
            "asm_compile_s": round(asm_t, 4),
            "exe_compile_s": round(exe_t, 4),
            "run_dt_s": round(run["dt"], 4) if run.get("dt") else None,
            "run_rc": run["rc"],
            "stdout": run["stdout"],
            "probe_counts": counts,
            "unified_diff": "\n".join(diff_lines),
            "judge_ok": v.ok, "judge_reasons": v.reasons,
            "judge_metrics": v.metrics,
        }

    # 阳面基线
    report["cards"]["yang"] = probe("yang", yang)
    yang_kv = parse_kv(report["cards"]["yang"]["stdout"])
    # 阴面各变体（diag_* 只做挂死诊断：编译 exe + 限时运行，不走 diff 判据）
    for name, src in variants.items():
        if name.startswith("diag_"):
            cpp = HERE / f"{name}.cpp"
            exe_p = bdir / f"{name}.exe"
            cexe = compile_exe(cpp, exe_p)
            hung = False
            run_dt = None
            rstdout = ""
            if cexe["rc"] == 0:
                t0 = time.perf_counter()
                try:
                    rr = timed([str(exe_p)], cwd=HERE, env=env, timeout=4.0)
                    run_dt, rstdout = rr["dt"], rr["stdout"]
                except subprocess.TimeoutExpired:
                    hung = True
                    run_dt = time.perf_counter() - t0
            report["cards"][name] = {
                "compile_exe_rc": cexe["rc"], "run_rc": None,
                "run_dt_s": round(run_dt, 3) if run_dt else None,
                "stdout": rstdout, "hung_timeout4s": hung}
            continue
        c = probe(name, src)
        kv = parse_kv(c["stdout"])
        c["run_keys_flipped"] = {k: {"yang": yang_kv.get(k), "yin": kv.get(k)}
                                 for k in RUN_KEYS if yang_kv.get(k) != kv.get(k)}
        yc = report["cards"]["yang"]["probe_counts"]
        c["probe_flipped"] = {t: {"yang": yc[t], "yin": c["probe_counts"][t]}
                              for t in ("s_sf_b", "je", "lock")
                              if yc[t] != c["probe_counts"][t]}
        report["cards"][name] = c

    # 阴面边际成本：一次额外 asm 编译（V-iso 对该卡的真实新增工作量）
    extra = bdir / "yin_only_cost.s"
    report["yin_marginal_asm_compile_s"] = round(median_runs(
        5, lambda: timed([gpp, "-std=c++23", "-O2", "-S", "-masm=intel",
                          str(HERE / "yin_del_fence.cpp"), "-o", str(extra)],
                         cwd=HERE, env=env)), 4)
    extra_exe = bdir / "yin_only_cost.exe"
    report["yin_marginal_exe_compile_s"] = round(median_runs(
        5, lambda: timed([gpp, "-std=c++23", "-O2",
                          str(HERE / "yin_del_fence.cpp"), "-o", str(extra_exe)],
                         cwd=HERE, env=env)), 4)

    (HERE / "probe_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # 控制台摘要
    for name, c in report["cards"].items():
        if name.startswith("diag_"):
            print(f"\n== {name} ==  exe_rc={c['compile_exe_rc']} "
                  f"hung={c['hung_timeout4s']} dt={c['run_dt_s']}s stdout={c['stdout']!r}")
            continue
        print(f"\n== {name} ==")
        print(f"  asm_rc={c['compile_asm_rc']} exe_rc={c['compile_exe_rc']} "
              f"run_rc={c['run_rc']} | asm {c['asm_compile_s']}s exe "
              f"{c['exe_compile_s']}s run {c['run_dt_s']}s")
        print(f"  counts={c['probe_counts']} flipped={c.get('probe_flipped')}")
        print(f"  run_keys_flipped={c.get('run_keys_flipped')}")
        print(f"  judge_ok={c['judge_ok']} reasons={c['judge_reasons']}")
        m = c["judge_metrics"]
        print(f"  diff: hunks={m['hunks']} ins={m['inserted_lines']} "
              f"del_code={m['code_deleted_lines']} tok_chg={m['tokens_changed']} "
              f"ratio={m['token_change_ratio']} coverage={m['anchor_coverage']}")
    print(f"\nyin marginal: asm {report['yin_marginal_asm_compile_s']}s "
          f"exe {report['yin_marginal_exe_compile_s']}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
