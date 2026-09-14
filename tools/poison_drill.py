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
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parent.parent
EXEMPTIONS = ROOT / "tools" / "poison_exemptions.yaml"
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

    # ── P8 身份漂移：stem≠id / id 重复（复制卡不改 id 会产生双份 verified）─────
    # 369 任务3（P1-5）：下游按 id 建 dict，重复时静默覆盖——其余规则各自看单卡，
    # 谁都不报；本样例同时验证两个毒点（stem≠id 与 id 撞车）都被同一规则拦下。
    with sandbox() as tmp:
        base = {
            "title": "t", "domain": "MEM", "type": "mechanism", "status": "draft",
            "claim": "c", "claim_boundary": "b", "relations": "[]", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p",
        }
        _write(ge.ATOMS / "mem" / "ATOM-ZZ-TMP-001.md",
               {"id": "ATOM-MEM-RAII-001", **base})          # ← 毒点1：stem≠id
        _write(ge.ATOMS / "mem" / "ATOM-MEM-RAII-001.md",
               {"id": "ATOM-MEM-RAII-001", **base})          # ← 毒点2：同 id 第二份
        who = sorted({f.rule_id for f in ge.check_atom_id_unique()})
        ok = "ATOM-ID-UNIQUE" in who and len(who) == 1
        results.append(("P8 身份漂移（stem≠id / id 重复）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P9 证据失配：verified 原子引用 verdict=refute 的证据卡（S2）────────────
    # 369 任务4：S2 此前无毒样例——"被反驳的证据仍撑着 verified"是最高危失配。
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-MEM-S2.md", {
            "id": "ATOM-MEM-S2", "title": "t", "domain": "MEM", "type": "mechanism",
            "status": "verified", "claim": "c", "claim_boundary": "b",
            "relations": "[]", "evidence": "[EV-MEM-REFUTED]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "true", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p",
        })
        _write(ge.EVIDENCE / "mem" / "EV-MEM-REFUTED.md", {
            "id": "EV-MEM-REFUTED", "serves": "[ATOM-MEM-S2]", "hypothesis": "h",
            "command": "true", "fixture": "x.cpp", "artifact": "x.asm",
            "artifact_sha256": "0" * 64, "actual": "{run_case: A}",
            "kind": "run", "verdict": "refute",                       # ← 毒点
            "falsification": "对照输出 1",
            "matrix": "\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]",
        })
        who = sorted({f.rule_id for f in ge.check_s2_evidence_verdict()})
        ok = "S2-EVIDENCE-VERDICT" in who
        results.append(("P9 证据失配（verified 绑 refute 证据）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P10 伪证据：期望值被硬编码进夹具字面量（S3）───────────────────────────
    # 369 任务4：S3 此前无毒样例——"打印常量冒充观测"是伪证据的最短路径。
    with sandbox() as tmp:
        fx = ge.EVIDENCE / "_fx_s3.cpp"
        fx.parent.mkdir(parents=True, exist_ok=True)
        fx.write_text('#include <cstdio>\n'
                      'int main(){ std::printf("single_total=100000\\n"); }\n',
                      encoding="utf-8")
        _write(ge.EVIDENCE / "mem" / "EV-MEM-S3.md", {
            "id": "EV-MEM-S3", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": "true", "fixture": fx.as_posix(), "artifact": "x.asm",
            "artifact_sha256": "0" * 64,
            "actual": "{single_total: 100000}",                        # ← 毒点
            "kind": "run", "verdict": "confirm",
            "falsification": "对照输出 1",
            "matrix": "\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]",
        })
        who = sorted({f.rule_id for f in ge.check_s3_hardcoded_expected()})
        ok = "S3-EXPECTED-HARDCODED" in who
        results.append(("P10 伪证据（期望值硬编码进夹具字面量）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P11 零诊断判据无 -Werror（W3）─────────────────────────────────────────
    # 371 报告 W3：compile_rc 只看退出码，警告不影响 rc ⇒「无警告/零诊断」类判据
    # 不加 -Werror 时**不可机器判定**（判据漂亮但机器看不见）。本样例验证新规则能拦下。
    with sandbox() as tmp:
        _write(ge.EVIDENCE / "mem" / "EV-MEM-ZD.md", {
            "id": "EV-MEM-ZD", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": "g++ -std=c++17 -Wall -c x.cpp -o x.o",          # ← 毒点：无 -Werror
            "fixture": "x.cpp", "artifact": "x.o",
            "artifact_sha256": "0" * 64, "actual": "{k: 1}",
            "kind": "run", "verdict": "confirm",
            "falsification": "若编译产生任何警告（非零诊断）→ 判 refute",
            "matrix": "\n  compiler: [GCC 15.3.0]\n  std: [c++17]\n  opt: [-O2]",
        })
        _fs = ge.check_evidence_zero_diag_werror()
        who = sorted({f.rule_id for f in _fs})
        _lvl = {f.rule_id: f.severity for f in _fs}
        ok = "EV-ZERO-DIAG-WERROR" in who and _lvl.get("EV-ZERO-DIAG-WERROR") == "block"
        results.append(("P11 零诊断判据缺 -Werror（须 block，472 P1-1）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"
                        f" · 级别 {_lvl.get('EV-ZERO-DIAG-WERROR', '—')}"))

    # ── P12 留痕锚自证：锚只出现在 actual 段（A3①）─────────────────────────────
    # 371 报告 A3①：P7 原对**整卡**搜索留痕锚，而 `actual.run_match_file` 自带 `.out`
    # 路径 ⇒ 对所有 run_match_file 形态的卡**结构上恒命中**（声明即留痕，规则永久失效）。
    # 本样例验证剥离 actual 段后："仅 actual 提到 .out" 必报。
    with sandbox() as tmp:
        _write(ge.EVIDENCE / "mem" / "EV-MEM-MB.md", {
            "id": "EV-MEM-MB", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": "g++ -c x.cpp", "fixture": "x.cpp", "artifact": "a.asm",
            "artifact_sha256": "0" * 64,
            "actual": "\n  run_match_file: Examples/atoms/_self_proving.out\n"
                      "  run_match_keys:\n    - k1",          # ← 毒点：锚仅在此处
            "kind": "run", "verdict": "confirm",
            "falsification": "对照输出 1",
            "matrix": "\n  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]\n"
                      "  std: [c++17]\n  opt: [-O2]",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_matrix_backed()})
        ok = "EV-MATRIX-UNBACKED" in who
        results.append(("P12 留痕锚自证（锚仅在 actual 段）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P13 空名签收：`human:` 前缀命中但**无实名**（373-P0-B9）──────────────────
    # 373 独立对抗渗透实测逃逸：三处签署判定原先只做 `startswith("human:")`，
    # `by: human:`（空名）、`by: human:   `（纯空格）、`verified_by: human:attacker`
    # 全部放行 ⇒ 任意方（含 Writer）可一步伪造「人已复核」，而人级是放权体系里唯一
    # 的真人授权来源。本样例验证实名制修法在**三处**同时生效（任一处漏 = 又一条逃生舱）。
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-MEM-EMPTYSIGN.md", {
            "id": "ATOM-MEM-EMPTYSIGN", "title": "t", "domain": "MEM",
            "type": "mechanism", "status": "human-verified", "claim": "c",
            "claim_boundary": "b", "relations": "[]", "evidence": "[EV-MEM-X]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "true", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p", "dal": "B", "human_review": "required",
            "status_history": ("\n  - {level: draft, at: legacy, by: writer:agent}"
                               "\n  - {level: machine-verified, at: 2026-09-12, by: machine:gate}"
                               "\n  - {level: human-verified, at: 2026-09-12, by: human:}"),
            "verified_by": "human:",                                # ← 毒点（空名）
        })
        _write(ge.ATOMS / "mem" / "ATOM-MEM-EMPTYDAL.md", {
            "id": "ATOM-MEM-EMPTYDAL", "title": "t", "domain": "MEM",
            "type": "mechanism", "status": "machine-verified", "claim": "c",
            "claim_boundary": "b", "relations": "[]", "evidence": "[EV-MEM-X]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "true", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p", "dal": "C", "human_review": "optional",
            "status_history": ("\n  - {level: draft, at: legacy, by: writer:agent}"
                               "\n  - {level: machine-verified, at: 2026-09-12, by: machine:gate}"),
            "verified_by": "machine:gate",
            "dal_reviewed_by": "human:",                            # ← 毒点（空名）
        })
        who = sorted({f.rule_id for f in ge.check_s1_human_signoff()}
                     | {f.rule_id for f in ge.check_status_transition()}
                     | {f.rule_id for f in ge.check_dal_match()})
        want = ["ATOM-DAL-MATCH", "ATOM-STATUS-TRANSITION", "S1-AUTHOR-SELF-VERIFY"]
        ok = who == want
        results.append(("P13 空名签收（human: 前缀无实名，三处）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"
                        + ("" if ok else f" · 期望 {', '.join(want)}")))

    # ── P14 .out 未声明读数键（373-B3 窄化，阴阳配对）──────────────────────────
    # 373 独立渗透 B3：往 `.out` 加一行 `fabricated_leak=64`，卡散文再引用它 ⇒
    # 该读数不在 `run_match_keys` 中 ⇒ 门禁视野外（S3/恒真观测都不扫、expected 约束不到），
    # 全库零告警。修复后：未声明的**结构化读数行** → `EV-OUT-UNDECLARED-KEY`。
    # 阴例：键已声明（含注释行/散文行）必须放行，否则规则恒红即失效。
    with sandbox() as tmp:
        of = tmp / "x.out"

        def _uk(name: str, keys: str, content: str) -> set[str]:
            of.write_text(content, encoding="utf-8")
            _write(ge.EVIDENCE / "mem" / f"{name}.md", {
                "id": name, "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
                "command": "echo hi", "fixture": "Examples/x.cpp", "artifact": "a.asm",
                "artifact_sha256": "0" * 64,
                "actual": f"\n  run_match_file: {of.as_posix()}\n"
                          f"  run_match_keys: [{keys}]",
                "kind": "run", "verdict": "confirm", "falsification": "对照输出 1",
            })
            return {f.rule_id for f in ge.check_evidence_out_undeclared_key()}

        who = _uk("EV-MEM-UK", "total", "total=100000\nfabricated_leak=64\n")
        ok = "EV-OUT-UNDECLARED-KEY" in who
        results.append(("P14 .out 未声明读数键（373-B3 编造载荷）", ok,
                        f"拦截者 {', '.join(sorted(who)) or '（漏网！）'}"))
        who2 = _uk("EV-MEM-UKOK", "total", "total=100000\n# 注释行\n散文行没有等号\n")
        ok2 = not who2
        results.append(("P14-阴 声明完整的 .out 必须放行", ok2,
                        f"误报 {', '.join(sorted(who2)) or '无'}"))

    # ── P15 断言文本须可定位（373-B2 窄化，阴阳各二）───────────────────────────
    # 373 独立渗透 B2-R1：断言 `contains "main"` —— 任何工件里都有 main ⇒ **恒真断言**，
    # 读者以为有校验、实际零判别力。裁决 §2.2 的映射判据把它挡在"夹具/工件/symbol_map"
    # 三处之外；拼错/平台专属拼写（无出处）同样不许蒙混。
    # 阴例①：符号在工件里有出处 → 放行。阴例②：卡内**显式** symbol_map 声明 → 放行
    # （工具**不做**"spin_plain → _Z10spin_plainv"的模糊匹配，只认显式声明）。
    with sandbox() as tmp:
        fx = tmp / "_fx.cpp"
        fx.write_text("void spin_plain(){ }\n", encoding="utf-8")
        art = tmp / "_art.asm"
        art.write_text("spin_other:\n\tret\n", encoding="utf-8")

        def _sev(name: str, asserts: str, extra: str = "") -> list[str]:
            _write(ge.EVIDENCE / "mem" / f"{name}.md", {
                "id": name, "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
                "command": "g++ -S x.cpp -o a.asm", "fixture": fx.as_posix(),
                "artifact": art.as_posix(), "artifact_sha256": "0" * 64,
                "artifact_assert": "\n" + asserts + extra,
                "actual": "{run_case: A}", "kind": "run", "verdict": "confirm",
                "falsification": "对照输出 1",
            })
            return sorted({f.severity for f in ge.check_evidence_assert_symbol_mapped()
                           if name in f.target})

        sev = _sev("EV-MEM-ASM1", '  - {kind: contains, text: "main"}')
        who = {f.rule_id for f in ge.check_evidence_assert_symbol_mapped()}
        ok = "EV-ASSERT-SYMBOL-MAPPED" in who and "block" in sev
        results.append(("P15 通用符号断言（373-B2 恒真载荷）", ok,
                        f"级别 {sev or '（漏网！）'}"))
        sev2 = _sev("EV-MEM-ASM2", '  - {kind: contains, text: "_Znotexist"}')
        results.append(("P15 断言符号无出处（拼错/平台专属拼写）", "warn" in sev2,
                        f"级别 {sev2 or '（漏网！）'}"))
        art.write_text("_Znwy:\n\tret\n", encoding="utf-8")
        sev3 = _sev("EV-MEM-ASM3", '  - {kind: contains, text: "_Znwy"}')
        results.append(("P15-阴 工件内有出处的断言必须放行", not sev3,
                        f"误报 {sev3 or '无'}"))
        art.write_text("spin_other:\n\tret\n", encoding="utf-8")
        sev4 = _sev("EV-MEM-ASM4", '  - {kind: contains, text: "_Z10spin_plainv"}',
                    "\nsymbol_map:\n  spin_plain: _Z10spin_plainv")
        results.append(("P15-阴 symbol_map 显式声明必须放行", not sev4,
                        f"误报 {sev4 or '无'}"))

    # ── P16 工件产出命令须显式声明（373-N4 窄化，阴阳各二）─────────────────────
    # 373 独立渗透 N4-R5：卡**不自己编译**，`cp other.asm mine.asm` 借一份别人的工件
    # ⇒ sha 与真实编译产物逐字一致、replay 全绿，而这张卡从未跑过自己的实验。
    # 阳例①：**新卡缺字段也必须拦**——否则攻击者不写这个字段就绕过了（豁免按 id 枚举的原因）。
    # 阴例②：迁移名单内的存量卡缺字段 → 放行（名单 = 可审计的迁移积压）。
    with sandbox() as tmp:

        def _prod(name: str, producer: str | None) -> list[str]:
            fields = {
                "id": name, "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
                "command": "g++ -S x.cpp -o a.asm", "fixture": "Examples/x.cpp",
                "artifact": "a.asm", "artifact_sha256": "0" * 64,
                "actual": "{run_case: A}", "kind": "run", "verdict": "confirm",
                "falsification": "对照输出 1",
            }
            if producer is not None:
                fields["artifact_producer"] = producer
            _write(ge.EVIDENCE / "mem" / f"{name}.md", fields)
            return sorted({f.severity for f in ge.check_evidence_artifact_producer()
                           if name in f.target})

        sev = _prod("EV-MEM-NEWPROD", None)                     # 新卡缺字段
        who = {f.rule_id for f in ge.check_evidence_artifact_producer()}
        ok = "EV-ARTIFACT-PRODUCER" in who and "block" in sev
        results.append(("P16 新卡缺 artifact_producer（不写字段即绕过）", ok,
                        f"级别 {sev or '（漏网！）'}"))
        sev2 = _prod("EV-MEM-COPYPROD", "cp Examples/atoms/other.asm a.asm")
        results.append(("P16 借工件（cp 复制，非编译产出）", "block" in sev2,
                        f"级别 {sev2 or '（漏网！）'}"))
        sev3 = _prod("EV-MEM-OKPROD", "g++ -S x.cpp -o a.asm")
        results.append(("P16-阴 编译器产出声明必须放行", not sev3, f"误报 {sev3 or '无'}"))
        sev4 = _prod("EV-MEM-001", None)                        # 迁移名单内的存量卡
        results.append(("P16-阴 迁移名单内存量卡缺字段放行", not sev4, f"误报 {sev4 or '无'}"))

    # ── P17 证据 id 唯一（373-N2）─────────────────────────────────────────────
    # 373 独立渗透 N2：同 id 的两张卡（一张 confirm、一张 refute）⇒ 按 id 建 dict 的下游
    # **后者覆盖前者**，门禁取到 confirm 那张即放行。
    with sandbox() as tmp:
        base = {
            "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h", "command": "echo hi",
            "fixture": "Examples/x.cpp", "artifact": "a.asm", "artifact_sha256": "0" * 64,
            "actual": "{run_case: A}", "kind": "run", "verdict": "confirm",
            "falsification": "对照输出 1",
        }
        _write(ge.EVIDENCE / "mem" / "EV-MEM-DUP1.md", {**base, "id": "EV-MEM-DUP"})
        _write(ge.EVIDENCE / "mem" / "EV-MEM-DUP2.md", {**base, "id": "EV-MEM-DUP"})
        who = {f.rule_id for f in ge.check_evidence_id_unique()}
        dup = [f for f in ge.check_evidence_id_unique() if "重复" in f.message]
        ok = "EV-ID-UNIQUE" in who and bool(dup)
        results.append(("P17 证据 id 重复（373-N2 同 id 双卡）", ok,
                        (f"拦截者 {', '.join(sorted(who)) or '（漏网！）'}"
                         f" · 重复判定 {len(dup)} 条")))
    with sandbox() as tmp:
        _write(ge.EVIDENCE / "mem" / "EV-MEM-UNIQ.md", {**base, "id": "EV-MEM-UNIQ"})
        results.append(("P17-阴 唯一且 stem==id 必须放行",
                        ge.check_evidence_id_unique() == [], "不得误伤"))

    # ── P18 relations 双写法归一（373-N1）──────────────────────────────────────
    # 373 独立渗透 N1：mapping 写法 `- prerequisite: X` 没有 type/target 键 ⇒
    # REL-TARGET / REL-DAG / PREREQ-READABLE 三条**静默跳过**（不报错、不计边、不查环）。
    # 归一本应让"环"立刻可见——修复前这两颗原子的环是隐形的。
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-MEM-001.md", {
            "id": "ATOM-MEM-001", "title": "t", "domain": "MEM", "type": "mechanism",
            "status": "draft", "claim": "c", "claim_boundary": "b",
            "relations": "\n  - prerequisite: ATOM-MEM-002",     # ← mapping-form
            "evidence": "[]", "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "s", "depth": "d", "pedagogy": "p",
        })
        _write(ge.ATOMS / "mem" / "ATOM-MEM-002.md", {
            "id": "ATOM-MEM-002", "title": "t", "domain": "MEM", "type": "mechanism",
            "status": "draft", "claim": "c", "claim_boundary": "b",
            "relations": "\n  - prerequisite: ATOM-MEM-001",     # ← 环
            "evidence": "[]", "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "s", "depth": "d", "pedagogy": "p",
        })
        who = {f.rule_id for f in ge.check_relations_dag()}
        ok = "ATOM-REL-DAG" in who
        results.append(("P18 mapping-form 环必须可见（373-N1）", ok,
                        f"拦截者 {', '.join(sorted(who)) or '（漏网！）'}"))
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-MEM-001.md", {
            "id": "ATOM-MEM-001", "title": "t", "domain": "MEM", "type": "mechanism",
            "status": "draft", "claim": "c", "claim_boundary": "b",
            "relations": "\n  - prerequisite: ATOM-MEM-002",
            "evidence": "[]", "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "s", "depth": "d", "pedagogy": "p",
        })
        _write(ge.ATOMS / "mem" / "ATOM-MEM-002.md", {
            "id": "ATOM-MEM-002", "title": "t", "domain": "MEM", "type": "mechanism",
            "status": "draft", "claim": "c", "claim_boundary": "b", "relations": "[]",
            "evidence": "[]", "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "s", "depth": "d", "pedagogy": "p",
        })
        res = [f.rule_id for f in ge.check_relations_dag() + ge.check_relations_target_exists()]
        results.append(("P18-阴 mapping-form 指向已存在目标必须放行", not res,
                        f"误报 {', '.join(res) or '无'}"))

    # ── P19 P7 留痕锚去自证（373-N3）──────────────────────────────────────────
    # 373 独立渗透 N3：旧锚含 `g++ … -o`（命令文本）⇒ 任何卡写了编译命令就算"留痕"，
    # 多编译器矩阵声明**结构上恒绿**。修复后：须两处可核对留痕（双平台 .out / 双 run / 各一）。
    with sandbox() as tmp:

        def _mx(name: str, falsification: str) -> list[str]:
            _write(ge.EVIDENCE / "mem" / f"{name}.md", {
                "id": name, "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
                "command": "g++ -O2 x.cpp -o x.exe && g++ -O2 -S x.cpp -o x.asm",
                "fixture": "Examples/x.cpp", "artifact": "x.asm",
                "artifact_sha256": "0" * 64,
                "actual": "{run_case: A}", "kind": "run", "verdict": "confirm",
                "falsification": falsification,
                "matrix": "\n  compiler: [GCC 15.3.0 (MinGW-w64), GCC 13.3.0 (WSL)]\n"
                          "  std: [c++17]\n  opt: [-O2]",
            })
            return sorted({f.rule_id for f in ge.check_evidence_matrix_backed()
                           if name in f.target})

        who = _mx("EV-MEM-MX1", "对照输出 1（命令本身不算留痕）")
        ok = "EV-MATRIX-UNBACKED" in who
        results.append(("P19 命令自证不再算留痕（373-N3）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))
        who2 = _mx("EV-MEM-MX2", "对照见 Examples/atoms/a.out 与 build/b.out 两处 1")
        results.append(("P19-阴 两处可核对留痕必须放行", not who2,
                        f"误报 {', '.join(who2) or '无'}"))

    # ── P20 声明-实现脱钩（373 绕过测试 3d，最核心）：producer 须逐字在 command 且 -o==artifact ──
    # 373 绕过测试 3d：仅查"声明文本"时，写 `artifact_producer: g++ -S x.cpp -o a.asm` 却让
    # `command: cp other.asm a.asm`，sha 与真编译产物一致、replay 全绿——卡从未跑自己的实验。
    # 修复后新增**声明-实现一致性**硬约束：producer 段须逐字出现在 command，且 -o 目标==artifact。
    with sandbox() as tmp:
        def _dec(name: str, producer: str, command: str) -> list[str]:
            _write(ge.EVIDENCE / "mem" / f"{name}.md", {
                "id": name, "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
                "command": command, "fixture": "Examples/x.cpp", "artifact": "a.asm",
                "artifact_sha256": "0" * 64, "actual": "{run_case: A}", "kind": "run",
                "verdict": "confirm", "falsification": "对照输出 1",
                "artifact_producer": producer,
            })
            return sorted({f.severity for f in ge.check_evidence_artifact_producer()
                           if name in f.target})

        # 阳例①：声明编译、实际 command 是 cp 借工件 → 段不在 command 中 → block
        sev = _dec("EV-MEM-DECOUPLE1", "g++ -S x.cpp -o a.asm",
                   "cp Examples/atoms/other.asm a.asm")
        who = {f.rule_id for f in ge.check_evidence_artifact_producer()}
        ok = "EV-ARTIFACT-PRODUCER" in who and "block" in sev
        results.append(("P20 声明-实现脱钩（producer 不在 command，cp 借工件）", ok,
                        f"级别 {sev or '（漏网！）'}"))
        # 阳例②：段在 command 中但 -o 目标≠artifact（编译产物非本工件）→ block
        sev2 = _dec("EV-MEM-DECOUPLE2", "g++ -S x.cpp -o b.asm", "g++ -S x.cpp -o b.asm")
        results.append(("P20 -o 目标≠artifact（编译产物非本工件）", "block" in sev2,
                        f"级别 {sev2 or '（漏网！）'}"))
        # 阴例：段逐字在 command 且 -o==artifact → 放行（声明与实现一致）
        sev3 = _dec("EV-MEM-DECOUPLE3", "g++ -S x.cpp -o a.asm", "g++ -S x.cpp -o a.asm")
        results.append(("P20-阴 声明与 command 一致且 -o==artifact 必须放行", not sev3,
                        f"误报 {sev3 or '无'}"))

    # ── P21 通用符号无论在哪都 block + 出处排除注释（373 绕过测试 2a/2b/2c）────────────
    # 373 绕过测试：2a `contains "main"`（任何工件都有 main ⇒ 恒真）；2b `contains_any ["main","call"]`
    # （any-of 只要一个通用符号即过）；2c `absent "_Znwm"` 配夹具注释 `/* _Znwm */`（注释伪造出处）。
    with sandbox() as tmp:
        fx = tmp / "_fx.cpp"
        art = tmp / "_art.asm"
        art.write_text("main:\n\tcall foo\n\tret\n", encoding="utf-8")   # 工件里真有 main:

        def _asv(name: str, asserts: str, fx_text: str = "", extra: str = "") -> list[str]:
            if fx_text:
                fx.write_text(fx_text, encoding="utf-8")
            _write(ge.EVIDENCE / "mem" / f"{name}.md", {
                "id": name, "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
                "command": "g++ -S x.cpp -o a.asm", "fixture": fx.as_posix(),
                "artifact": art.as_posix(), "artifact_sha256": "0" * 64,
                "artifact_assert": "\n" + asserts + extra,
                "actual": "{run_case: A}", "kind": "run", "verdict": "confirm",
                "falsification": "对照输出 1",
            })
            return sorted({f.severity for f in ge.check_evidence_assert_symbol_mapped()
                           if name in f.target})

        # 阳例①：通用符号 `main` 即便在工件里也 block（零判别力，恒真断言）
        sev = _asv("EV-MEM-UNIV1", '  - {kind: contains, text: "main"}')
        who = {f.rule_id for f in ge.check_evidence_assert_symbol_mapped()}
        ok = "EV-ASSERT-SYMBOL-MAPPED" in who and "block" in sev
        results.append(("P21 通用符号无论在哪都 block（工件含 main 仍拦）", ok,
                        f"级别 {sev or '（漏网！）'}"))
        # 阳例②：注释伪造出处 —— `absent "_Znwm"` 配夹具注释 `// _Znwm`
        #          剥注释后符号无出处 → 不再被"注释里有"蒙混放行
        sev2 = _asv("EV-MEM-COMM1", '  - {kind: absent, text: "_Znwm"}',
                    fx_text="// _Znwm\nint main(){ return 0; }\n")
        who2 = {f.rule_id for f in ge.check_evidence_assert_symbol_mapped()
                if "EV-MEM-COMM1" in f.target}
        ok2 = "EV-ASSERT-SYMBOL-MAPPED" in who2
        results.append(("P21 注释伪造出处（absent 配注释）必须被拦", ok2,
                        f"级别 {sev2 or '（漏网！）'}"))
        # 阴例：符号在工件真实代码里有出处 → 放行
        art.write_text("_Znwy:\n\tret\n", encoding="utf-8")
        sev3 = _asv("EV-MEM-UNIV3", '  - {kind: contains, text: "_Znwy"}',
                    fx_text="void spin_plain(){}\n")
        results.append(("P21-阴 工件真实代码里有出处须放行", not sev3, f"误报 {sev3 or '无'}"))

    # ── P29 relations 矛盾（415 D1）：A 依赖 B 且 B 声明 contradicts A ──────────
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-TEST-CONFLICT-001.md", {
            "id": "ATOM-TEST-CONFLICT-001", "title": "t", "domain": "MEM",
            "type": "mechanism", "status": "draft", "claim": "c",
            "claim_boundary": "b", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p",
            "relations": "\n  - prerequisite: ATOM-TEST-CONFLICT-002",
        })
        _write(ge.ATOMS / "mem" / "ATOM-TEST-CONFLICT-002.md", {
            "id": "ATOM-TEST-CONFLICT-002", "title": "t", "domain": "MEM",
            "type": "mechanism", "status": "draft", "claim": "c",
            "claim_boundary": "b", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p",
            "relations": "\n  - contradicts: ATOM-TEST-CONFLICT-001",
        })
        who = sorted({f.rule_id for f in ge.check_atom_rel_conflict()})
        ok = "ATOM-REL-CONFLICT" in who
        results.append(("P29 relations 矛盾（A 依赖 B 且 B contradicts A）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P30 自相矛盾（415 D1）：A 声明 contradicts 自身 ────────────────────────
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-TEST-SELFCONFLICT-001.md", {
            "id": "ATOM-TEST-SELFCONFLICT-001", "title": "t", "domain": "MEM",
            "type": "mechanism", "status": "draft", "claim": "c",
            "claim_boundary": "b", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p",
            "relations": "\n  - contradicts: ATOM-TEST-SELFCONFLICT-001",
        })
        who = sorted({f.rule_id for f in ge.check_atom_rel_conflict()})
        ok = "ATOM-REL-CONFLICT" in who
        results.append(("P30 自相矛盾（A contradicts 自身）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P31-阴 合法对比（415 D1）：contrasts 不是矛盾关系，不得 block ──────────
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-TEST-LEGAL-001.md", {
            "id": "ATOM-TEST-LEGAL-001", "title": "t", "domain": "MEM",
            "type": "mechanism", "status": "draft", "claim": "c",
            "claim_boundary": "b", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p",
            "relations": "\n  - prerequisite: ATOM-TEST-LEGAL-002\n  - contrasts: ATOM-TEST-LEGAL-003",
        })
        _write(ge.ATOMS / "mem" / "ATOM-TEST-LEGAL-002.md", {
            "id": "ATOM-TEST-LEGAL-002", "title": "t", "domain": "MEM",
            "type": "mechanism", "status": "draft", "claim": "c",
            "claim_boundary": "b", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]",
            "first_hand": "false", "superiority": "真实增量", "depth": "asm",
            "pedagogy": "p",
            "relations": "\n  - contrasts: ATOM-TEST-LEGAL-001",
        })
        who = sorted({f.rule_id for f in ge.check_atom_rel_conflict()})
        ok = "ATOM-REL-CONFLICT" not in who
        results.append(("P31-阴 合法对比（contrasts 非矛盾）必须放行", ok,
                        f"误报 {', '.join(who) or '无'}"))

    # ── P32 cl 卡标 confirm（414 P0-2 F01）：MSVC 卡不可复算，禁止宣称已验证 ──
    with sandbox() as tmp:
        _write(ge.EVIDENCE / "mem" / "EV-MEM-CLFAKE.md", {
            "id": "EV-MEM-CLFAKE", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": "cl /std:c++17 /c fx.cpp",        # ← 毒点：MSVC 卡
            "verdict": "confirm",                        # ← 毒点：不可复算却宣称已验证
            "falsification": "对照输出 1",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_msvc_no_verify()})
        ok = "EV-MSCV-NO-VERIFY" in who
        results.append(("P32 cl卡标confirm（不可复算卡宣称已验证）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P33 编译后覆写（414 P0-3 F02）：python 在编译行之后改写工件 ───────────
    with sandbox() as tmp:
        prod = f'"{gpp_posix}" -std=c++17 -O2 -S fx.cpp -o fx.asm'
        cmd = prod + " && python -c \"shutil.copy('other.asm', 'fx.asm')\""
        _write(ge.EVIDENCE / "mem" / "EV-MEM-POSTPY.md", {
            "id": "EV-MEM-POSTPY", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": cmd, "artifact_producer": prod, "artifact": "fx.asm",
            "verdict": "confirm", "falsification": "对照输出 1",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_artifact_producer()})
        ok = "EV-ARTIFACT-PRODUCER" in who
        results.append(("P33 编译后python覆写（时序约束）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P34 编译后覆写·powershell（414 P0-3 F02）：Copy-Item 换工件 ───────────
    with sandbox() as tmp:
        prod = f'"{gpp_posix}" -std=c++17 -O2 -S fx.cpp -o fx.asm'
        cmd = prod + " && powershell -Command Copy-Item other.asm fx.asm"
        _write(ge.EVIDENCE / "mem" / "EV-MEM-POSTPS.md", {
            "id": "EV-MEM-POSTPS", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": cmd, "artifact_producer": prod, "artifact": "fx.asm",
            "verdict": "confirm", "falsification": "对照输出 1",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_artifact_producer()})
        ok = "EV-ARTIFACT-PRODUCER" in who
        results.append(("P34 编译后powershell覆写（时序约束）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P35 contains_in 无判别力 text（414 P1-4 F03）：通用助记符恒有 ⇒ 恒真 ──
    with sandbox() as tmp:
        _write(ge.EVIDENCE / "mem" / "EV-MEM-CINTEXT.md", {
            "id": "EV-MEM-CINTEXT", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": "g++ -S fx.cpp", "verdict": "confirm",
            "falsification": "对照输出 1",
            "artifact_assert": "\n  - {kind: contains_in, symbol: asm, text: ret}",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_assert_symbol_mapped()})
        ok = "EV-ASSERT-SYMBOL-MAPPED" in who
        results.append(("P35 contains_in text=通用助记符（F03）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P36 重复 YAML 键（414 P1-5 F09）：双 verdict after-wins 遮蔽 S2 ───────
    with sandbox() as tmp:
        card = ge.EVIDENCE / "mem" / "EV-MEM-DUPKEY.md"
        card.parent.mkdir(parents=True, exist_ok=True)
        card.write_text(
            "---\nid: EV-MEM-DUPKEY\nverdict: refute\nverdict: confirm\n"
            "hypothesis: h\nfalsification: 对照输出 1\n---\n", encoding="utf-8")
        who = sorted({f.rule_id for f in ge.check_frontmatter_duplicate_key()})
        ok = "EV-FM-DUP-KEY" in who
        results.append(("P36 重复 verdict 键（F09 after-wins 遮蔽）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P37 全角 .out 键（414 P1-6 F04）：非 ASCII 键漏网 → 未声明键 warn ─────
    with sandbox() as tmp:
        outp = ROOT / "build" / "_poison_out_f04.out"
        outp.parent.mkdir(exist_ok=True)
        outp.write_text("ｎｐｒｏｃ=1\n", encoding="utf-8")
        _write(ge.EVIDENCE / "mem" / "EV-MEM-UNIKEY.md", {
            "id": "EV-MEM-UNIKEY", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": "g++ -S fx.cpp", "verdict": "confirm",
            "falsification": "对照输出 1",
            "actual": "\n  run_match_file: build/_poison_out_f04.out\n  run_match_keys: []",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_out_undeclared_key()})
        ok = "EV-OUT-UNDECLARED-KEY" in who
        results.append(("P37 全角键 .out 未声明（F04）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))
        outp.unlink(missing_ok=True)

    # ── P38 .out 陈旧留痕（414 P1-7 F06）：.out 比 .cpp 旧 → warn ─────────────
    with sandbox() as tmp:
        outp = ROOT / "build" / "_poison_out_f06.out"
        fxp = ROOT / "build" / "_poison_fx_f06.cpp"
        outp.parent.mkdir(exist_ok=True)
        fxp.write_text("int main(){return 0;}\n", encoding="utf-8")
        outp.write_text("x=1\n", encoding="utf-8")
        past = time.time() - 600
        os.utime(outp, (past, past))
        _write(ge.EVIDENCE / "mem" / "EV-MEM-STALE.md", {
            "id": "EV-MEM-STALE", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": "g++ -S fx.cpp", "fixture": "build/_poison_fx_f06.cpp",
            "verdict": "confirm", "falsification": "对照输出 1",
            "actual": "\n  run_match_file: build/_poison_out_f06.out\n  run_match_keys: []",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_out_stale_mtime()})
        ok = "EV-OUT-STALE-MTIME" in who
        results.append(("P38 .out 比夹具旧（F06 陈旧留痕）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))
        outp.unlink(missing_ok=True)
        fxp.unlink(missing_ok=True)

    # ── P39 注释伪造符号出处（424 A8）：出处空间剥注释后无此符号 → 无出处 ─────
    with sandbox() as tmp:
        fx = ROOT / "build" / "_poison_fx_a8.cpp"
        asm = ROOT / "build" / "_poison_fx_a8.asm"
        fx.parent.mkdir(exist_ok=True)
        # 毒点：符号只出现在**注释**里——出处空间若不剥注释，断言就有假出处
        fx.write_text("// 出处伪造注释：_Z10fake_symv\nint main(){return 0;}\n",
                      encoding="utf-8")
        subprocess.run([resolve_gpp(), "-std=c++17", "-S", str(fx), "-o", str(asm)],
                       capture_output=True, text=True, errors="replace", timeout=300)
        _write(ge.EVIDENCE / "mem" / "EV-MEM-A8COMM.md", {
            "id": "EV-MEM-A8COMM", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "kind": "asm", "fixture": fx.as_posix(), "artifact": asm.as_posix(),
            "command": f'"{gpp_posix}" -std=c++17 -S "{fx.as_posix()}" -o "{asm.as_posix()}"',
            "artifact_sha256": hashlib.sha256(asm.read_bytes()).hexdigest(),
            "verdict": "confirm", "falsification": "对照输出 1",
            "artifact_assert": "\n  - {kind: contains, text: _Z10fake_symv}",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_assert_symbol_mapped()})
        ok = "EV-ASSERT-SYMBOL-MAPPED" in who
        results.append(("P39 注释伪造符号出处（A8 间接注入）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))
        asm.unlink(missing_ok=True)
        fx.unlink(missing_ok=True)

    # ── P40 工具冒充（424 A10 供应链）：producer 声明 clang++，实际 command 用 g++ ─
    with sandbox() as tmp:
        prod = "clang++ -std=c++17 -S fx.cpp -o fx.asm"
        _write(ge.EVIDENCE / "mem" / "EV-MEM-A10IMPO.md", {
            "id": "EV-MEM-A10IMPO", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "kind": "asm",
            "command": "g++ -std=c++17 -S fx.cpp -o fx.asm",
            "artifact_producer": prod, "artifact": "fx.asm",
            "verdict": "confirm", "falsification": "对照输出 1",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_artifact_producer()})
        ok = "EV-ARTIFACT-PRODUCER" in who
        results.append(("P40 工具冒充（producer 声明≠实际编译器，A10）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P41 非编译器产出工件（424 A10 供应链）：argv[0] 不在编译器白名单 ───────
    with sandbox() as tmp:
        _write(ge.EVIDENCE / "mem" / "EV-MEM-A10GEN.md", {
            "id": "EV-MEM-A10GEN", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "kind": "asm",
            "command": "python gen_asm.py -o fx.asm",
            "artifact_producer": "python gen_asm.py -o fx.asm", "artifact": "fx.asm",
            "verdict": "confirm", "falsification": "对照输出 1",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_artifact_producer()})
        ok = "EV-ARTIFACT-PRODUCER" in who
        results.append(("P41 非编译器产出工件（生成脚本冒充编译，A10）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P42 环境值进读数键（424 A5 环境依赖）：nproc 类键未声明 → warn ─────────
    with sandbox() as tmp:
        outp = ROOT / "build" / "_poison_out_a5.out"
        outp.parent.mkdir(exist_ok=True)
        # 毒点：环境相关读数（nproc）进了 .out——换机器即碎，且不在 run_match_keys
        outp.write_text("nproc_used=16\n", encoding="utf-8")
        _write(ge.EVIDENCE / "mem" / "EV-MEM-A5ENV.md", {
            "id": "EV-MEM-A5ENV", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": "g++ -O2 fx.cpp -o fx.exe && ./fx.exe", "verdict": "confirm",
            "falsification": "对照输出 1",
            "actual": "\n  run_match_file: build/_poison_out_a5.out\n  run_match_keys: []",
        })
        who = sorted({f.rule_id for f in ge.check_evidence_out_undeclared_key()})
        ok = "EV-OUT-UNDECLARED-KEY" in who
        results.append(("P42 环境值进读数键（nproc 未声明，A5）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))
        outp.unlink(missing_ok=True)

    # ── P43 缩进走私（470 P0-D / 452 E07）：缩进 verdict 被提升为顶层键 ────────
    with sandbox() as tmp:
        card = ge.EVIDENCE / "mem" / "EV-MEM-SMUG.md"
        card.parent.mkdir(parents=True, exist_ok=True)
        card.write_text(
            "---\nid: EV-MEM-SMUG\nstatus: draft\nfixture: f.cpp &x\n"
            "  verdict: confirm\nhypothesis: h\ncommand: g++ -S f.cpp -o f.asm\n"
            "artifact: f.asm\nartifact_sha256: " + "0" * 64 + "\n---\n",
            encoding="utf-8")
        who = sorted({f.rule_id for f in ge.check_frontmatter_hardening()
                      if f.severity == "block"})
        ok = "EV-FM-YAML-HARDENING" in who
        results.append(("P43 缩进走私（E07 缩进 verdict 提升顶层键）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P44 环境量进断言键（470 P0-E / 452 E06）：nproc 声明为比对目标 ────────
    with sandbox() as tmp:
        outp = ROOT / "build" / "_poison_out_e06.out"
        outp.parent.mkdir(exist_ok=True)
        outp.write_text("nproc=32\nresult=7\n", encoding="utf-8")
        _write(ge.EVIDENCE / "mem" / "EV-MEM-ENVKEY.md", {
            "id": "EV-MEM-ENVKEY", "serves": "[ATOM-MEM-MOVE-001]", "hypothesis": "h",
            "command": "g++ fx.cpp -o a.exe && ./a.exe", "verdict": "confirm",
            "falsification": "对照输出 1",
            "actual": "\n  run_match_file: build/_poison_out_e06.out\n"
                      "  run_match_keys: [nproc, result]",
        })
        who = sorted({f.rule_id for f in ge.check_env_dependent_key()
                      if f.severity == "block"})
        ok = "EV-ENV-DEPENDENT-KEY" in who
        results.append(("P44 环境量进断言键（nproc 声明为比对目标，A5）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))
        outp.unlink(missing_ok=True)

    # ── P45 僵尸锁必须被立即接管（472 P0-1 / N1）───────────────────────────
    # 逃逸面：锁内 pid 已死（进程被杀）时，只按 mtime 判陈旧的实现会阻塞到
    # wait_timeout 才失败 ⇒ 整条 replay 长时间不可用（实测 600s）。
    _tmpd = Path(tempfile.mkdtemp(prefix="p45_"))
    _orig_lock = replay._REPLAY_LOCK
    replay._REPLAY_LOCK = _tmpd / ".replay_lock"
    try:
        replay._REPLAY_LOCK.write_text("999999\n", encoding="utf-8")   # 不存在 pid
        _t0 = time.time()
        try:
            replay._acquire_replay_lock(wait_timeout=5, stale_after=300)
            _took = time.time() - _t0
            _ok45 = _took < 3.0            # 应立即接管（pid 已死）
            replay._release_replay_lock()
        except TimeoutError:
            _took = time.time() - _t0
            _ok45 = False                  # 阻塞到超时 = 僵尸锁未被接管
        results.append(("P45 僵尸锁(pid已死)须立即接管", _ok45,
                        f"耗时 {_took:.1f}s（>3s 即仍逃逸）"))
    finally:
        replay._REPLAY_LOCK = _orig_lock
        shutil.rmtree(_tmpd, ignore_errors=True)

    # ── P46 阴性：活锁不得被抢（互斥必须成立）──────────────────────────────
    _tmpd2 = Path(tempfile.mkdtemp(prefix="p46_"))
    replay._REPLAY_LOCK = _tmpd2 / ".replay_lock"
    try:
        replay._acquire_replay_lock(wait_timeout=5, stale_after=300)
        _raised = False
        try:
            replay._acquire_replay_lock(wait_timeout=1, stale_after=3600)
        except TimeoutError:
            _raised = True
        results.append(("P46 活锁(当前pid)不得被接管", _raised,
                        "活锁时二次取锁须超时而非抢锁"))
        replay._release_replay_lock()
    finally:
        replay._REPLAY_LOCK = _orig_lock
        shutil.rmtree(_tmpd2, ignore_errors=True)

    # ── P51 工件快照：中断后须能幂等还原（472 P0-4 / N4）─────────────────────
    _tmpd3 = Path(tempfile.mkdtemp(prefix="p51_"))
    try:
        _art = _tmpd3 / "a.asm"
        _art.write_text("ORIGINAL-BYTES", encoding="utf-8")
        _bak = replay._snapshot_artifact(_art)
        _art.unlink()                                  # 模拟进程被杀：工件丢失
        _ok51 = (not _art.is_file()) and replay._restore_artifact(_art, _bak) \
            and _art.read_text(encoding="utf-8") == "ORIGINAL-BYTES"
        results.append(("P51 工件快照须能幂等还原（中断不丢工件）", _ok51,
                        f"还原后={_art.read_text(encoding='utf-8') if _art.is_file() else '丢失'}"))
        replay._drop_snapshot(_bak)
        results.append(("P52 阴性·正常路径不留 .bak 残留", not _bak.exists(),
                        f"bak 存在={_bak.exists()}"))
    finally:
        shutil.rmtree(_tmpd3, ignore_errors=True)

    # ── P55 refutes 同义词归一后须参与冲突检测（472 P1-4 / N3）────────────────
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-P.md", {
            "id": "ATOM-P", "title": "t", "domain": "MEM", "type": "mechanism",
            "status": "draft", "claim": "c", "claim_boundary": "b", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]", "first_hand": "false",
            "superiority": "s", "depth": "d", "pedagogy": "p",
            "relations": "\n  - prerequisite: ATOM-Q",
        })
        _write(ge.ATOMS / "mem" / "ATOM-Q.md", {
            "id": "ATOM-Q", "title": "t", "domain": "MEM", "type": "mechanism",
            "status": "draft", "claim": "c", "claim_boundary": "b", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]", "first_hand": "false",
            "superiority": "s", "depth": "d", "pedagogy": "p",
            "relations": "\n  - refutes: ATOM-P",
        })
        _who55 = sorted({f.rule_id for f in ge.check_atom_rel_conflict()})
        ok = "ATOM-REL-CONFLICT" in _who55
        results.append(("P55 refutes 同义词归一时须检出矛盾", ok,
                        f"拦截者 {', '.join(_who55) or '（漏网！）'}"))

    # ── P56 未知关系类型必须可见（结束同义词枚举）─────────────────────────────
    with sandbox() as tmp:
        _write(ge.ATOMS / "mem" / "ATOM-U1.md", {
            "id": "ATOM-U1", "title": "t", "domain": "MEM", "type": "mechanism",
            "status": "draft", "claim": "c", "claim_boundary": "b", "evidence": "[]",
            "sources": "[{kind: iso, ref: X, independent: true}]", "first_hand": "false",
            "superiority": "s", "depth": "d", "pedagogy": "p",
            "relations": "\n  - some_future_relation: ATOM-U2",
        })
        # RULE-COVERAGE 的正则只认 `"RULE_ID" in who`（变量名必须恰好是 who）
        who = sorted({f.rule_id for f in ge.check_relations_unknown_type()})
        ok = "ATOM-REL-UNKNOWN" in who
        results.append(("P56 未知 relations 类型须可见（不静默丢弃）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P57 cat 式证据须被拦（472 P1-2：experimental→warn）───────────────────
    with sandbox() as tmp:
        _fx = ROOT / "_adv_v80" / "probes" / "p57.cpp"
        _fx.parent.mkdir(parents=True, exist_ok=True)
        _fx.write_text(
            '#include <cstdio>\n#include <fstream>\n#include <string>\n'
            'int main(){ std::ifstream f("_adv_v80/probes/expected_data.txt");\n'
            '  std::string l;\n'
            '  while (std::getline(f, l)) std::printf("%s\\n", l.c_str()); }\n',
            encoding="utf-8")
        _write(ge.EVIDENCE / "mem" / "EV-MEM-CAT.md", {
            "id": "EV-MEM-CAT", "serves": "[]", "hypothesis": "h", "kind": "run",
            "command": "g++ _adv_v80/probes/p57.cpp -o build/_p57.exe && ./build/_p57.exe",
            "fixture": "_adv_v80/probes/p57.cpp", "artifact": "a.asm",
            "artifact_sha256": "0" * 64, "verdict": "confirm", "falsification": "f",
        })
        who = sorted({f.rule_id for f in ge.check_fixture_no_echo_findings()})
        ok = "EV-FIXTURE-NO-ECHO-DATA" in who
        results.append(("P57 cat 式证据须被拦（升 warn 后）", ok,
                        f"拦截者 {', '.join(who) or '（漏网！）'}"))

    # ── P47/P48 恒真断言（472 P0-2 / N2）：函数级探针（不真编译，避免与 replay 抢锁）──
    with sandbox() as tmp:
        _art = tmp / "a.asm"
        _art.write_text('\t.text\n\t.file\t"a.cpp"\nmain:\n\tret\n', encoding="utf-8")
        _ok47, _l47 = replay.check_artifact_assert(
            {"artifact_assert": [{"kind": "contains_any", "texts": [".file", ".text"]}]},
            _art)
        ok = (not _ok47) and any("判别力不足" in l for l in _l47)
        results.append(("P47 contains_any 全样板须判无判别力", ok,
                        "命中候选全为工件样板（.file/.text）⇒ 断言零信息"))
        _ok48, _l48 = replay.check_artifact_assert(
            {"artifact_assert": [{"kind": "contains_any", "texts": ["ret", ".file"]}]},
            _art)
        results.append(("P48 阴性·命中含非样板须放行", _ok48,
                        "命中候选含 ret（非伪指令）⇒ 按原语义放行"))

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
            # 373-N4：阴性对照代表**完全合规**的卡 ⇒ 必须声明产出命令（新卡强制项）
            "artifact_producer": f'"{gpp_posix}" -std=c++17 -O2 -S "{fx.as_posix()}" '
                                 f'-o "{asm.as_posix()}"',
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

    _LAST_RESULTS.clear()
    _LAST_RESULTS.extend(results)
    failures = []
    for name, ok, detail in results:
        print(f"[poison] {name}: {detail} {'✅' if ok else '❌'}")
        if not ok:
            failures.append({"rule": "poison", "severity": "block",
                             "file": name, "message": detail})
    passed = sum(1 for _, ok, _ in results if ok)
    print(f"\n[poison] {passed}/{len(results)} —— "
          + ("制衡层有效（全部拦截 + 阴性放行）" if passed == len(results)
             else "制衡层有漏网，先修制衡！"))
    stats = attack_type_stats(results)
    uncovered = [a for a in ALL_ATTACK_TYPES if stats.get(a, 0) == 0]
    unknown = unknown_attack_types(stats)
    print(f"[poison] 攻击面分类（424 A1-A{len(ALL_ATTACK_TYPES)}，实测载荷）：{stats}")
    if unknown:
        print(f"[poison] ⚠ 未登记攻击面 {unknown} —— 在 ATTACK_TYPES 补映射，"
              "否则「零覆盖」判定不可信")
    print(f"[poison] 零覆盖攻击面：{uncovered or '无'}"
          + ("" if not uncovered else " —— 攻击者可从这些面无样本预警地打进来"))
    return passed, len(results), failures


# ── 424：攻击面分类（A1-A11，409 分类学 + 472 扩面）────────────────────────
# 毒样例名前缀 → 主攻击类（阴性对照不分类）。P21 两条异类，具体前缀优先匹配。
#
# **口径声明（472 实测发现，勿默认本表==409 原表）**：本表并非 409 分类表的逐字落地——
# A8（间接注入）/A9（规则逃逸）与 409 一致，但 A1/A2/A3/A4/A6/A7/A10 的语义相对 409
# 发生迁移（例：409 `A4=注释伪造`、`A10=门禁假阳性`；本表 `A4=时序穿链`、`A10=供应链与工件完整性`）。
# A11 为 472 新增（并发/可用性）——409 原文授权「全新攻击面则更新分类学（A11…）」。
# 下表的 LABELS 由成员样例**归纳**，仅作人类可读；是否回改为 409 原义属人裁决（见 _worklog_472.md）。
ATTACK_TYPES: list[tuple[str, str]] = [
    ("P1 ", "A1"), ("P2 ", "A2"), ("P3 ", "A3"), ("P4 ", "A3"), ("P5 ", "A3"),
    ("P6 ", "A3"), ("P7 ", "A1"), ("P8 ", "A1"), ("P9 ", "A1"), ("P10 ", "A3"),
    ("P11 ", "A9"), ("P12 ", "A3"), ("P13 ", "A1"), ("P14 ", "A1"),
    ("P15 ", "A3"), ("P16 ", "A2"), ("P17 ", "A1"), ("P18 ", "A7"), ("P19 ", "A3"),
    ("P20 ", "A2"), ("P21 注释伪造", "A8"), ("P21 ", "A3"),
    ("P29 ", "A7"), ("P30 ", "A7"), ("P32 ", "A1"), ("P33 ", "A4"), ("P34 ", "A4"),
    ("P35 ", "A3"), ("P36 ", "A6"), ("P37 ", "A6"), ("P38 ", "A4"),
    ("P39 ", "A8"), ("P40 ", "A10"), ("P41 ", "A10"), ("P42 ", "A5"),
    ("P43 ", "A6"), ("P44 ", "A5"), ("P45 ", "A11"), ("P46 ", "A11"),
    ("P51 ", "A10"), ("P52 ", "A10"), ("P55 ", "A7"), ("P56 ", "A7"),
    ("P57 ", "A2"), ("P47 ", "A3"), ("P48 ", "A3"),
]
ALL_ATTACK_TYPES = [f"A{i}" for i in range(1, 12)]   # A11 = 并发/可用性（472 新增）

# 每类的人类可读标签（由成员样例归纳，非 409 原表逐字；见 ATTACK_TYPES 上方口径声明）。
ATTACK_TYPE_LABELS: dict[str, str] = {
    "A1": "记录层伪造：状态/身份/绑定不实（无证据 verified、留痕不足、id 漂移、空名签收）",
    "A2": "声明-实现脱钩：工件/证据与声明不符（借用、陈旧、cat 式证据）",
    "A3": "断言无判别力：恒真/自证/通用符号/全样板（contains·contains_in·absent）",
    "A4": "时序穿链：编译后覆写、留痕比夹具旧",
    "A5": "环境量污染：机器/时钟量进入读数键或断言键",
    "A6": "解析走私：缩进/重复键/全角键绕过 YAML 语义",
    "A7": "关系图失配：环、矛盾、未知关系类型",
    "A8": "间接注入：注释/知识库内容伪造出处",
    "A9": "编译器配置逃逸：零诊断判据未配 -Werror",
    "A10": "供应链与工件完整性：工具冒充、非编译器产出、快照幂等",
    "A11": "并发与可用性：僵尸锁 DoS、活锁误接管",
}
assert set(ATTACK_TYPE_LABELS) == set(ALL_ATTACK_TYPES), "标签表与攻击面清单不同源"

# 最近一次 drill 的实测载荷明细（424 台账用；保持 drill() 三元组返回契约不变）。
_LAST_RESULTS: list[tuple[str, bool, str]] = []


def attack_type_stats(results: list[tuple[str, bool, str]]) -> dict[str, int]:
    """按 A1-A11 统计攻击载荷覆盖（**实测口径**：同前缀多载荷各计一条）。

    阴性对照排除——它们验证「不误伤」，不计入攻击面覆盖。
    未登记前缀 → `A?`（会出现在返回值里，供调用方 fail-loud，勿静默丢弃）。
    """
    by: dict[str, int] = {}
    for name, _ok, _detail in results:
        head = name.split(" ")[0]
        if name.startswith("阴性") or "-阴" in head:
            continue
        t = next((t for pfx, t in ATTACK_TYPES if name.startswith(pfx)), "A?")
        by[t] = by.get(t, 0) + 1
    return dict(sorted(by.items()))


def unknown_attack_types(stats: dict[str, int]) -> list[str]:
    """未登记攻击面（含 `A?`）—— 非空即覆盖面不可信，调用方须红。"""
    return sorted(t for t in stats if t not in ALL_ATTACK_TYPES)


_EXEMPT_LINE = re.compile(
    r'^\s*-\s*\{\s*id:\s*([A-Z][A-Z0-9-]+)\s*,\s*reason:\s*"?(.*?)"?\s*,\s*'
    r'date:\s*(\d{4}-\d{2}-\d{2})\s*\}\s*$')


def load_exemptions() -> dict[str, str]:
    """S6 毒样例豁免台账 `tools/poison_exemptions.yaml` → {规则 ID: "日期 · 原因"}。

    **零依赖解析**（不引 PyYAML，与 gate_engine 复用 replay 解析器的零依赖口径一致）：
    台账只允许单行 flow 映射 `- {id: X, reason: "...", date: YYYY-MM-DD}`。

    fail-closed：台账缺失/解析不到 → 返回空 dict —— 未覆盖规则**一律算欠账**，
    不因台账丢失而静默放行（368 P1-2 的反面：旧实现只打印、永不红）。
    """
    if not EXEMPTIONS.is_file():
        return {}
    out: dict[str, str] = {}
    for ln in EXEMPTIONS.read_text(encoding="utf-8", errors="replace").split("\n"):
        m = _EXEMPT_LINE.match(ln)
        if m:
            out[m.group(1)] = f"{m.group(3)} · {m.group(2).strip()}"
    return out


def rule_coverage() -> tuple[int, int, list[str]]:
    """RULE-COVERAGE: 已覆盖 / **注册规则数**（分母单点化为 `gate_engine.RULES`）。

    旧口径（368 P1-2）：分母取 gate 源码 `Finding("...")` 正则去重数，与注册规则数
    互不认账（实测 32 vs 37），且未覆盖只打印、不影响退出码——台账不存在＝永久免检。
    新口径：分母取注册规则；未覆盖且未登记豁免 → 返回非空，`__main__` 据此 exit 1。
    """
    all_rules = {r.id for r in ge.RULES}
    drill_src = Path(__file__).read_text(encoding="utf-8")
    covered = set(re.findall(r'"([A-Z][A-Z0-9-]+)" in who', drill_src))
    exempt = set(load_exemptions())
    uncovered = sorted(all_rules - covered - exempt)
    return len(covered), len(all_rules), uncovered


def gate_exit_code(passed: int, total_d: int, uncovered: list[str]) -> int:
    """414 P0-1：全过且无未覆盖规则 → 0，否则 1。

    修复前 `0 if passed == total_d else 1 or (1 if uncovered else 0)`：
    `1 or x` 恒为 1（短路），且 passed==total 时忽略 uncovered ⇒ 未覆盖规则时 CI 不红。
    """
    all_passed = (passed == total_d)
    no_uncovered = (len(uncovered) == 0)
    return 0 if (all_passed and no_uncovered) else 1


# ── 424 产物：攻击面台账 `tools/poison_surface_map.json` ─────────────────────
# 设计取舍：**只有显式 `--write-surface-map` 才落盘**（主流程/CI 不自动写）。
# 理由：台账含 generated_at/source_commit，自动写会让每次门禁运行都把工作区搞脏
# （违「门禁只读仓」惯例）；而 `--by-type` 读台账，保证「查得快」与「数据真」两者兼得——
# 数据源单点化为**实测 results**，杜绝静态前缀表与实测各说各话（472 修）。
SURFACE_MAP = ROOT / "tools" / "poison_surface_map.json"


def build_surface_map(passed: int, total_d: int,
                      results: list[tuple[str, bool, str]],
                      rule_cov: tuple[int, int, list[str]]) -> dict:
    """把一次**实测**钻探固化为攻击面台账（逐条载荷 + 分类计数 + 覆盖率 + 规则覆盖）。"""
    covered_rules, total_rules, _ = rule_cov
    payloads = []
    negatives = []
    for name, ok, _detail in results:
        head = name.split(" ")[0]
        neg = name.startswith("阴性") or "-阴" in head
        entry = {"name": name, "pass": bool(ok)}
        if neg:
            entry["type"] = None
            negatives.append(entry)
        else:
            entry["type"] = next(
                (t for pfx, t in ATTACK_TYPES if name.startswith(pfx)), "A?")
            payloads.append(entry)
    stats = attack_type_stats(results)
    uncovered = [a for a in ALL_ATTACK_TYPES if stats.get(a, 0) == 0]
    try:
        src = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                             capture_output=True, text=True, timeout=10)
        commit = src.stdout.strip() or "unknown"
    except Exception:                                   # git 不可用不该阻断台账生成
        commit = "unknown"
    return {
        "schema": 1, "tool": "poison_drill.py", "task": "424",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source_commit": commit,
        "drill": {"passed": passed, "total": total_d},
        "attack_types": {a: {"label": ATTACK_TYPE_LABELS[a], "count": stats.get(a, 0)}
                         for a in ALL_ATTACK_TYPES},
        "coverage": {"covered": len(ALL_ATTACK_TYPES) - len(uncovered),
                     "total": len(ALL_ATTACK_TYPES), "uncovered": uncovered},
        "rule_coverage": {"covered": covered_rules, "total": total_rules,
                          "exempt": len(load_exemptions())},
        "payloads": payloads,
        "negative_controls": negatives,
        "note": ("A1-A11 = 代码实际口径（标签由成员样例归纳），非 409 原表逐字；"
                 "A11 为 472 新增（并发/可用性）。口径差异与裁决见 _worklog_472.md。"),
    }


def write_surface_map(payload: dict) -> Path:
    SURFACE_MAP.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8")
    return SURFACE_MAP


def load_surface_map() -> dict | None:
    """读台账；缺失/损坏 → None（调用方须 fail-loud，不得静默当「无覆盖问题」）。"""
    if not SURFACE_MAP.is_file():
        return None
    try:
        return json.loads(SURFACE_MAP.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


if __name__ == "__main__":
    import argparse as _ap, datetime as _dt
    _p = _ap.ArgumentParser(description="门禁毒样例钻探（对抗回归）")
    _p.add_argument("--json", nargs="?", const=True, default=False,
                   help="结构化 JSON 输出到 stdout")
    _p.add_argument("--by-type", action="store_true",
                    help="读 tools/poison_surface_map.json 打印攻击面覆盖（424，不跑钻探）")
    _p.add_argument("--write-surface-map", action="store_true",
                    help="跑完整钻探并把**实测**结果写成攻击面台账（424 产物，入库）")
    _a = _p.parse_args()
    if _a.by_type:
        _m = load_surface_map()
        if _m is None:
            print("[poison] 攻击面台账不存在/损坏：先跑 "
                  "`python tools/poison_drill.py --write-surface-map`"
                  "（不可用静态前缀表冒充实测数字）", file=sys.stderr)
            raise SystemExit(1)
        _at = _m.get("attack_types", {})
        _cov = _m.get("coverage", {})
        _rc = _m.get("rule_coverage", {})
        print(f"[poison] 攻击面覆盖 A1-A{len(ALL_ATTACK_TYPES)}"
              f"（实测口径 · 采集 {_m.get('generated_at', '?')}"
              f" @ {_m.get('source_commit', '?')}）")
        for _a11 in ALL_ATTACK_TYPES:
            _info = _at.get(_a11, {})
            _n = _info.get("count", 0)
            print(f"  {_a11:>3} {_n:>2} 条 {'✅' if _n else '❌ 零覆盖'}"
                  f"  {_info.get('label', '')}")
        _unc = _cov.get("uncovered") or []
        print(f"[poison] 覆盖率 {_cov.get('covered', 0)}/{_cov.get('total', len(ALL_ATTACK_TYPES))}"
              + (f" · 零覆盖 {_unc}" if _unc else " · 零覆盖：无"))
        print(f"[poison] RULE-COVERAGE（台账快照）：{_rc.get('covered', '?')}/{_rc.get('total', '?')}"
              f" + 豁免 {_rc.get('exempt', '?')}")
        raise SystemExit(0 if not _unc else 1)
    real_out = sys.stdout
    if _a.json:
        sys.stdout = sys.stderr          # 普通报告走 stderr，stdout 只留 JSON
    covered, total, uncovered = rule_coverage()
    print(f"[poison] RULE-COVERAGE: {covered}/{total} 注册规则被毒样例覆盖"
          f"（另登记豁免 {len(load_exemptions())} 条）")
    if uncovered:
        print(f"[poison] 未覆盖且未豁免（{len(uncovered)}）: {', '.join(uncovered)}")
        print("[poison] 二选一：补毒样例，或在 tools/poison_exemptions.yaml 登记"
              "（规则 ID + 原因 + 日期）——本项为硬门禁（CI 红）")
    passed, total_d, failures = drill()
    surface = build_surface_map(passed, total_d, _LAST_RESULTS,
                                (covered, total, uncovered))
    if _a.write_surface_map:
        _path = write_surface_map(surface)
        print(f"[poison] 攻击面台账已落盘：{_path.relative_to(ROOT).as_posix()}"
              f"（{surface['coverage']['covered']}/{surface['coverage']['total']} 覆盖）")
    if _a.json:
        payload = {
            "tool": "poison_drill", "version": "v6.1",
            "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
            "status": "pass" if passed == total_d else "fail",
            "summary": {"passed": passed, "total": total_d},
            "attack_surface": {
                "counts": {a: surface["attack_types"][a]["count"]
                           for a in ALL_ATTACK_TYPES},
                "coverage": surface["coverage"],
                "unknown": unknown_attack_types(attack_type_stats(_LAST_RESULTS)),
            },
            "findings": failures, "infra_errors": [],
        }
        real_out.write(json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
    raise SystemExit(gate_exit_code(passed, total_d, uncovered))

