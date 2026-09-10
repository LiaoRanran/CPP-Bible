#!/usr/bin/env python3
"""S6 变异测试：向制衡层**注入毒样例**，门禁必须全部拦截且理由正确；阴性对照必须放行。

这就是 G3 验收门「3 个毒样例现场攻击制衡层」的机器化自证（不采信自报，跑给监工看）：
    P1 假论断    —— status=verified 但证据空、无人工签收 → S1 + ATOM-VERIFIED-BOUND
    P2 过期工件  —— 证据卡 sha256 与重新生成的工件不符     → replay refute:sha256_mismatch
    P3 缺反例    —— 证据卡无 falsification                → EV-FALSIFICATION
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
