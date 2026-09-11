#!/usr/bin/env python3
"""S6 变异测试：向制衡层**注入毒样例**，门禁必须全部拦截且理由正确；阴性对照必须放行。

这就是 G3 验收门「3 个毒样例现场攻击制衡层」的机器化自证（不采信自报，跑给监工看）：
    P1 假论断    —— status=verified 但证据空、无人工签收 → S1 + ATOM-VERIFIED-BOUND
    P2 过期工件  —— 证据卡 sha256 与重新生成的工件不符     → replay refute:sha256_mismatch
    P3 缺反例    —— 证据卡无 falsification                → EV-FALSIFICATION
    P4 自证断言  —— 夹具自定义 operator new/delete，而断言只做存在性匹配（命中定义处即通过）
                   → EV-SELF-SATISFIED-ASSERT（第三批实例：`contains_any ["_ZdaPv","_ZdaPvy"]`）
    P5 伪证伪    —— falsification 是纯假设句、无任何量化对照值 → EV-FALSIFICATION-QUANT
    P6 恒真观测  —— actual 里是存在性判断（对关键变量零响应）  → EV-TRIVIAL-OBSERVATION
                   （第三批实例：`use_count after join=1`）
    P7 无留痕矩阵—— matrix 声明多编译器但只有一个工件、无外部留痕说明 → EV-MATRIX-UNBACKED
    阴性对照     —— 干净原子 + 干净证据卡                 → 0 block 且 replay confirm

实现要点：
    * 每个样例用**独立沙箱**（contextmanager 替换 `gate_engine.ATOMS/EVIDENCE`，finally 还原），
      互不污染、也不污染真实仓库——阴性对照若与毒卡同沙箱，会被毒卡的违规假性拉红。
    * 多行值（command）写 YAML block scalar（`|`），不能用普通标量拼接——两条命令会被
      plain-scalar 续行逻辑拼成一行（实测：生成 asm 的命令从此消失 → missing_artifact_command）。
    * P2 走真编译（与 replay 契约一致）。
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge               # noqa: E402
from toolchain import resolve_gpp      # noqa: E402


def _write(path: Path, fields: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = ""
    for k, v in fields.items():
        s = str(v)
        if s.startswith("\n"):                          # 显式嵌套块（优先于 block scalar）
            body += f"{k}:{s}\n"
        elif "\n" in s:                                 # 多行标量 → block scalar
            body += f"{k}: |\n" + "".join(f"  {ln}\n" for ln in s.split("\n"))
        else:
            body += f"{k}: {s}\n"
    path.write_text("---\n" + body + "---\n", encoding="utf-8")


@contextmanager
def sandbox() -> Iterator[Path]:
    tmp = Path(tempfile.mkdtemp(prefix="poison_"))
    (tmp / "atoms").mkdir()
    (tmp / "evidence").mkdir()
    orig_a, orig_e = ge.ATOMS, ge.EVIDENCE
    ge.ATOMS, ge.EVIDENCE = tmp / "atoms", tmp / "evidence"
    try:
        yield tmp
    finally:
        ge.ATOMS, ge.EVIDENCE = orig_a, orig_e
        shutil.rmtree(tmp, ignore_errors=True)


def drill() -> int:
    gpp_posix = Path(resolve_gpp()).as_posix()
    results: list[tuple[str, bool, str]] = []

    # ── P1 假论断：verified 但证据空、无人工签收 ─────────────────────────────
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-MEM-MOVE-001.md", {
            "id": "ATOM-MEM-MOVE-001", "title": "t", "domain": "MEM",
            "type": "mechanism", "status": "verified", "claim": "c",
            "claim_boundary": "b", "relations": "[]", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "true", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p",
        })
        who = sorted({f.rule_id for f in ge.check_verified_bound()}
                     | {f.rule_id for f in ge.check_s1_human_signoff()})
        ok = ("ATOM-VERIFIED-BOUND" in who) and ("S1-AUTHOR-SELF-VERIFY" in who)
        results.append(("P1 假论断（verified 无证据+无人工签收）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P2 过期工件：卡里 sha256 与重生成产物不符（真编译）───────────────────
    with sandbox() as tmp:
        fx = ge.EVIDENCE / "_fx.cpp"
        fx.parent.mkdir(parents=True, exist_ok=True)
        fx.write_text('#include <cstdio>\nint main(){ std::printf("A\\nB\\n"); }\n',
                      encoding="utf-8")
        exe = tmp / "fx.exe"
        asm = ge.EVIDENCE / "fx.asm"
        command = (f'"{gpp_posix}" -std=c++17 -O2 "{fx.as_posix()}" -o "{exe.as_posix()}" '
                   f'&& "{exe.as_posix()}"\n'
                   f'"{gpp_posix}" -std=c++17 -O2 -S "{fx.as_posix()}" -o "{asm.as_posix()}"')
        card = ge.EVIDENCE / "mem" / "EV-MEM-POISON.md"
        _write(card, {
            "id": "EV-MEM-POISON", "serves": "[ATOM-MEM-MOVE-001]",
            "hypothesis": "h", "command": command, "fixture": fx.as_posix(),
            "artifact": asm.as_posix(), "artifact_sha256": "0" * 64,   # ← 毒点
            "actual": "{run_case: A | B}", "kind": "run", "verdict": "confirm",
            "falsification": "对照输出 1",
            "matrix": "\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]",
        })
        verdict, log = replay.replay_card(card, do_sanitizer=False)
        ok = verdict == "refute:sha256_mismatch"
        detail = verdict
        for ln in log:
            if "期望" in ln or "实际" in ln:
                detail += f" · {ln.strip()[:88]}"
        results.append(("P2 过期工件（sha256 与重生成不符）", ok, detail))

    # ── P3 缺反例：证据卡无 falsification ────────────────────────────────────
    with sandbox() as tmp:
        fx = ge.EVIDENCE / "_fx.cpp"
        fx.parent.mkdir(parents=True, exist_ok=True)
        fx.write_text('#include <cstdio>\nint main(){ std::printf("A\\n"); }\n',
                      encoding="utf-8")
        asm = ge.EVIDENCE / "fx.asm"
        subprocess_done = subprocess.run(
            [resolve_gpp(), "-std=c++17", "-O2", "-S", str(fx), "-o", str(asm)],
            capture_output=True, text=True, errors="replace", timeout=300)
        card = ge.EVIDENCE / "mem" / "EV-MEM-NOFALS.md"
        _write(card, {
            "id": "EV-MEM-NOFALS", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": (f'"{gpp_posix}" -std=c++17 -O2 -S "{fx.as_posix()}" '
                        f'-o "{asm.as_posix()}"'),
            "fixture": fx.as_posix(), "artifact": asm.as_posix(),
            "artifact_sha256": hashlib.sha256(asm.read_bytes()).hexdigest(),
            "actual": "{run_case: A}", "kind": "run", "verdict": "confirm",
            "falsification": "",                                     # ← 毒点
            "matrix": "\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]",
        })
        who = sorted({h.rule_id for h in ge.check_evidence_falsification()})
        ok = "EV-FALSIFICATION" in who
        results.append(("P3 缺反例（无证伪对照）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"
                        + ("" if subprocess_done.returncode == 0 else " · 夹具生成失败")))

    # ── P4 自证断言：夹具自定义 operator delete[]，而断言只做存在性匹配 ───────
    # 第三批真实案例（UNIQUE-002 初版）：`contains_any ["_ZdaPv","_ZdaPvy"]` 被夹具自身的
    # `operator delete[]` **定义**满足——工件里既没有 call 点也照样通过 ⇒ 断言恒真。
    with sandbox() as tmp:
        fx4 = ge.EVIDENCE / "_fx_selfsat.cpp"
        fx4.parent.mkdir(parents=True, exist_ok=True)
        fx4.write_text(
            "#include <cstdio>\n#include <cstdlib>\n"
            "void* operator new[](std::size_t n) { return std::malloc(n); }\n"
            "void  operator delete[](void* p) noexcept { std::free(p); }\n"
            "void  operator delete[](void*, std::size_t) noexcept {}\n"
            "int main() { auto p = new int[4]; delete[] p; std::printf(\"A\\n\"); return 0; }\n",
            encoding="utf-8")
        asm4 = ge.EVIDENCE / "fx_selfsat.asm"
        subprocess.run([resolve_gpp(), "-std=c++17", "-O2", "-S", str(fx4), "-o", str(asm4)],
                       capture_output=True, text=True, errors="replace", timeout=300)
        subprocess_done = subprocess.run(
            [resolve_gpp(), "-std=c++17", "-O2", "-S", str(fx4), "-o", str(asm4)],
            capture_output=True, text=True, errors="replace", timeout=300)
        _write(ge.EVIDENCE / "mem" / "EV-MEM-SELFSAT.md", {
            "id": "EV-MEM-SELFSAT", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": (f'"{gpp_posix}" -std=c++17 -O2 -S "{fx4.as_posix()}" '
                        f'-o "{asm4.as_posix()}"'),
            "fixture": fx4.as_posix(), "artifact": asm4.as_posix(),
            "artifact_sha256": hashlib.sha256(asm4.read_bytes()).hexdigest(),
            "actual": "{run_case: A}", "kind": "asm", "verdict": "confirm",
            "falsification": "对照输出 1",
            # ← 毒点：夹具自带 operator delete[] 定义，此断言在零调用点下也恒真
            "artifact_assert": '\n  - {kind: contains_any, texts: ["_ZdaPvy", "_ZdaPv"]}',
            "matrix": "\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_self_satisfied_assert()})
        ok = "EV-SELF-SATISFIED-ASSERT" in who
        results.append(("P4 自证断言（断言被夹具自身定义满足）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"
                        + ("" if subprocess_done.returncode == 0 else " · 夹具生成失败")))

    # ── P5 伪证伪：falsification 是纯假设句、无任何量化对照值 ────────────────
    with sandbox() as tmp:
        fx5 = ge.EVIDENCE / "_fx_weak.cpp"
        fx5.parent.mkdir(parents=True, exist_ok=True)
        fx5.write_text('#include <cstdio>\nint main(){ std::printf("A\\n"); }\n',
                       encoding="utf-8")
        asm5 = ge.EVIDENCE / "fx_weak.asm"
        subprocess.run([resolve_gpp(), "-std=c++17", "-O2", "-S", str(fx5), "-o", str(asm5)],
                       capture_output=True, text=True, errors="replace", timeout=300)
        _write(ge.EVIDENCE / "mem" / "EV-MEM-WEAKFALS.md", {
            "id": "EV-MEM-WEAKFALS", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": (f'"{gpp_posix}" -std=c++17 -O2 -S "{fx5.as_posix()}" '
                        f'-o "{asm5.as_posix()}"'),
            "fixture": fx5.as_posix(), "artifact": asm5.as_posix(),
            "artifact_sha256": hashlib.sha256(asm5.read_bytes()).hexdigest(),
            "actual": "{run_case: A}", "kind": "run", "verdict": "confirm",
            # ← 毒点：只有"若…则应…"的假设句，读者无法复核"结论错了会怎样"
            "falsification": "若结论不成立，则对照组的输出会与实验组不同",
            "matrix": "\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_falsification_quantified()})
        ok = "EV-FALSIFICATION-QUANT" in who
        results.append(("P5 伪证伪（无量化对照值，不可复核）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P6 恒真观测：actual 里的存在性判断对 claim 关键变量零响应 ─────────────
    # 第三批真实案例（SHARED-002 初版）：`use_count after join=1`——join 之后任何实现都读到 1。
    with sandbox() as tmp:
        fx6 = ge.EVIDENCE / "_fx_trivial.cpp"
        fx6.parent.mkdir(parents=True, exist_ok=True)
        fx6.write_text('#include <cstdio>\nint main(){ std::printf("A\\n"); }\n',
                       encoding="utf-8")
        asm6 = ge.EVIDENCE / "fx_trivial.asm"
        subprocess.run([resolve_gpp(), "-std=c++17", "-O2", "-S", str(fx6), "-o", str(asm6)],
                       capture_output=True, text=True, errors="replace", timeout=300)
        _write(ge.EVIDENCE / "mem" / "EV-MEM-TRIVIAL.md", {
            "id": "EV-MEM-TRIVIAL", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": (f'"{gpp_posix}" -std=c++17 -O2 -S "{fx6.as_posix()}" '
                        f'-o "{asm6.as_posix()}"'),
            "fixture": fx6.as_posix(), "artifact": asm6.as_posix(),
            "artifact_sha256": hashlib.sha256(asm6.read_bytes()).hexdigest(),
            # ← 毒点：存在性判断（指针非空）——无论被测机制是否成立都恒为该值
            "actual": "{run_case: observer != nullptr}",
            "kind": "run", "verdict": "confirm",
            "falsification": "对照输出 1",
            "matrix": "\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_trivial_observation()})
        ok = "EV-TRIVIAL-OBSERVATION" in who
        results.append(("P6 恒真观测（存在性判断无判别力）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P7 无留痕矩阵：声明多编译器但只有一个工件、且无外部留痕说明 ──────────
    with sandbox() as tmp:
        fx7 = ge.EVIDENCE / "_fx_matrix.cpp"
        fx7.parent.mkdir(parents=True, exist_ok=True)
        fx7.write_text('#include <cstdio>\nint main(){ std::printf("A\\n"); }\n',
                       encoding="utf-8")
        asm7 = ge.EVIDENCE / "fx_matrix.asm"
        subprocess.run([resolve_gpp(), "-std=c++17", "-O2", "-S", str(fx7), "-o", str(asm7)],
                       capture_output=True, text=True, errors="replace", timeout=300)
        _write(ge.EVIDENCE / "mem" / "EV-MEM-MATRIX.md", {
            "id": "EV-MEM-MATRIX", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": (f'"{gpp_posix}" -std=c++17 -O2 -S "{fx7.as_posix()}" '
                        f'-o "{asm7.as_posix()}"'),
            "fixture": fx7.as_posix(), "artifact": asm7.as_posix(),
            "artifact_sha256": hashlib.sha256(asm7.read_bytes()).hexdigest(),
            "actual": "{run_case: A}", "kind": "run", "verdict": "confirm",
            "falsification": "对照输出 1",
            # ← 毒点：声明三个编译器，但仓内只有一个工件、卡内也无"外部留痕"说明
            "matrix": "\n  compiler: [GCC 15.3.0, Clang 19.1.0, MSVC 19.4]"
                      "\n  std: [c++17]\n  opt: [-O2]",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_matrix_backed()})
        ok = "EV-MATRIX-UNBACKED" in who
        results.append(("P7 无留痕矩阵（多编译器声明无工件支撑）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── 阴性对照：干净原子 + 干净证据卡必须放行（门禁不得恒红）───────────────
    with sandbox() as tmp:
        fx = ge.EVIDENCE / "_fx.cpp"
        fx.parent.mkdir(parents=True, exist_ok=True)
        fx.write_text('#include <cstdio>\nint main(){ std::printf("A\\nB\\n"); }\n',
                      encoding="utf-8")
        exe = tmp / "fx.exe"
        asm = ge.EVIDENCE / "fx.asm"
        command = (f'"{gpp_posix}" -std=c++17 -O2 "{fx.as_posix()}" -o "{exe.as_posix()}" '
                   f'&& "{exe.as_posix()}"\n'
                   f'"{gpp_posix}" -std=c++17 -O2 -S "{fx.as_posix()}" -o "{asm.as_posix()}"')
        subprocess.run([resolve_gpp(), "-std=c++17", "-O2", "-S", str(fx), "-o", str(asm)],
                       capture_output=True, text=True, errors="replace", timeout=300)
        _write(ge.ATOMS / "mem" / "ATOM-MEM-CLEAN-001.md", {
            "id": "ATOM-MEM-CLEAN-001", "title": "t", "domain": "MEM",
            "type": "mechanism", "status": "draft", "claim": "c",
            "claim_boundary": "b", "relations": "[]", "evidence": "[EV-MEM-CLEAN]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p",
        })
        _write(ge.EVIDENCE / "mem" / "EV-MEM-CLEAN.md", {
            "id": "EV-MEM-CLEAN", "serves": "[ATOM-MEM-CLEAN-001]", "hypothesis": "h",
            "command": command, "fixture": fx.as_posix(), "artifact": asm.as_posix(),
            "artifact_sha256": hashlib.sha256(asm.read_bytes()).hexdigest(),
            "actual": "{run_case: A | B}", "kind": "run", "verdict": "confirm",
            "falsification": "对照输出 1",
            "matrix": "\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]",
        })
        blocks = [f for f in ge.run(include_advice=False) if f.severity == "block"]
        clean_verdict, clean_log = replay.replay_card(
            ge.EVIDENCE / "mem" / "EV-MEM-CLEAN.md", do_sanitizer=False)
        ok = not blocks and clean_verdict == "confirm"
        detail = f"gate block={len(blocks)} · replay={clean_verdict}"
        if not ok:
            for f in blocks:
                detail += f"\n         [{f.rule_id}] {f.message[:80]}"
            for ln in clean_log:
                if "❌" in ln:
                    detail += f"\n         {ln.strip()[:88]}"
        results.append(("阴性对照（干净原子+干净卡）", ok, detail))

    for name, ok, detail in results:
        print(f"[poison] {name}: {detail} {'✅' if ok else '❌'}")
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"\n[poison] {passed}/{len(results)} —— "
          + ("制衡层有效（全部拦截 + 阴性放行）" if passed == len(results)
             else "制衡层有漏网，先修制衡！"))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(drill())
