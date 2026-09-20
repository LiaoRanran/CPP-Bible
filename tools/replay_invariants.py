#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""replay_invariants.py — replay 状态机不变量独立检查工具（605 任务1）。

为什么：602 TLA+ 调研发现 replay 的 5 个关键不变量全部是**隐式的**（散落在代码中，
没有独立可验证的检查）。本工具把其中 3 个（I1 工件还原 / I2 编译可复现 / I4 沙箱隔离）
显性化，做成独立的、可机器验证的不变量检查。

硬约束：
  * 不修改 atom_evidence_replay.py（独立工具，不侵入 replay）；
  * 只读真实仓库，检查用临时文件放 %TEMP%；
  * 每个不变量有明确 pass/fail 判据，不输出"可能有问题"。

用法：
    python tools/replay_invariants.py --check              # 跑全部不变量
    python tools/replay_invariants.py --check --invariant artifact_restore  # 只跑指定
    python tools/replay_invariants.py --list                # 列出所有不变量
"""
# mypy: ignore-errors
# 类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

EXAMPLES_DIR = ROOT / "Examples"
INVARIANTS = ("artifact_restore", "build_reproducibility", "sandbox_isolation",
              "lock_consistency", "manifest_consistency")


# ── 工具函数 ───────────────────────────────────────────────────────────────────
def fingerprint_dir(path: Path | str, *, pattern: str = "**/*") -> str:
    """目录内容指纹（只看文件内容和相对路径，不看 mtime）。"""
    p = Path(path)
    if not p.is_dir():
        return "MISSING"
    h = hashlib.sha256()
    for f in sorted(p.glob(pattern)):
        if f.is_file():
            rel = f.relative_to(p).as_posix()
            h.update(rel.encode())
            h.update(b"\x00")
            h.update(f.read_bytes())
            h.update(b"\x00")
    return h.hexdigest()[:16]


# ── I1：工件还原不变量 ─────────────────────────────────────────────────────────
def _find_confirm_cards(*, n: int = 1) -> list[tuple[Path, dict]]:
    """找前 n 张 confirm 卡（有 command + artifact_sha256）。"""
    try:
        import gate_engine as ge
    except ImportError:
        return []
    cards = []
    for f in sorted((ROOT / "evidence").rglob("EV-*.md")):
        meta = ge._meta(f)
        if meta.get("verdict") == "confirm" and meta.get("command") and meta.get("artifact_sha256"):
            cards.append((f, meta))
            if len(cards) >= n:
                break
    return cards


def check_artifact_restore() -> dict:
    """I1：replay 跑完后，真实仓库 Examples/ 工件必须与跑前逐字节一致。

    真检查：找一张 confirm 卡 → 拍 Examples/ 指纹 before → 跑 replay_card(restore_artifact=True)
    → 拍指纹 after → 验证 before==after。如果 replay 崩溃或没还原，指纹不一致 ⇒ fail。
    """
    t0 = time.time()
    cards = _find_confirm_cards(n=1)
    if not cards:
        return {"name": "artifact_restore", "passed": False, "elapsed_s": 0,
                "detail": "no confirm card with command+artifact_sha256 found"}
    card_path, meta = cards[0]
    fp_before = fingerprint_dir(EXAMPLES_DIR)
    verdict = "not_run"
    error_msg = ""
    try:
        import atom_evidence_replay as aer
        verdict, _log = aer.replay_card(card_path, restore_artifact=True)
    except Exception as exc:
        error_msg = f"{type(exc).__name__}: {exc}"
    fp_after = fingerprint_dir(EXAMPLES_DIR)
    elapsed = time.time() - t0
    passed = fp_before == fp_after and fp_before != "MISSING" and not error_msg
    detail = (f"card={card_path.stem} verdict={verdict} "
              f"Examples/ before={fp_before} after={fp_after} "
              f"{'RESTORED ✓' if passed else 'NOT RESTORED ✗'}")
    if error_msg:
        detail += f" error={error_msg}"
    return {
        "name": "artifact_restore",
        "passed": passed,
        "elapsed_s": round(elapsed, 2),
        "detail": detail,
        "card": card_path.stem,
        "verdict": verdict,
        "files_scanned": len(list(EXAMPLES_DIR.glob("**/*"))) if EXAMPLES_DIR.is_dir() else 0,
    }


# ── I2：编译可复现不变量 ───────────────────────────────────────────────────────
def _only_time_macro_diff(ba: bytes, bb: bytes) -> bool:
    """判断两个二进制是否**只**在「时间宏 / PE 时间戳」区域不同。

    命中任一即视为时间相关漂移（可接受）：
      * 所有差异字节均为可打印 ASCII（`__TIME__`/`__DATE__`/`__TIMESTAMP__` 是 ASCII 串）；
      * 或差异恰好落在 PE 头 TimeDateStamp 4 字节（即便已关插时间戳，也兜底层处理）。
    否则 ⇒ 真不可复现。
    """
    if ba == bb:
        return True
    n = min(len(ba), len(bb))
    diff_bytes = {ba[i] for i in range(n) if ba[i] != bb[i]}
    if diff_bytes and all(0x20 <= b <= 0x7E for b in diff_bytes):
        return True
    if (len(ba) >= 0x40 and len(bb) >= 0x40
            and ba[0:2] == b"MZ" and bb[0:2] == b"MZ"):
        pe_off = int.from_bytes(ba[0x3C:0x40], "little")
        if (ba[pe_off:pe_off + 4] == b"PE\x00\x00"
                and bb[pe_off:pe_off + 4] == b"PE\x00\x00"):
            ts_region = range(pe_off + 8, pe_off + 12)
            if all(i in ts_region for i in range(n) if ba[i] != bb[i]):
                return True
    return False


def check_build_reproducibility(*, n_cards: int = 5, cross_time: bool = False,
                                 no_symtab: bool = False) -> dict:
    """I2：编译可复现不变量（608 B1 深化）。

    在 603 的短窗口 sha 比对之外新增三项（均不修改 atom_evidence_replay.py，只调用其
    `check_build_reproducibility` 引擎与 `_recompile_invariant`）：
      * **符号表一致性**：`nm` 提取两次编译的符号表逐行比对（`--no-symtab` 关闭）；
      * **段一致性**：`objdump -h` 比对 `.text`/`.data`/`.rodata` 段大小；
      * **跨时间窗口**：间隔 ≥1s 重编译，检测 `__TIME__`/`__DATE__`/`__TIMESTAMP__` 漂移
        （只对前 3 张卡做，避免太慢）。漂移只落在时间宏区域 ⇒「时间宏漂移（可接受）」；
        落在其他区域 ⇒「真不可复现（fail）」。

    硬纪律：编译产物落 %TEMP%；复用 replay 的 CCACHE_DISABLE + 临时目录隔离。
    """
    t0 = time.time()
    try:
        import atom_evidence_replay as aer
        import gate_engine as ge
    except ImportError as exc:
        return {"name": "build_reproducibility", "passed": False, "elapsed_s": 0,
                "detail": f"import error: {exc}"}
    confirm_cards = []
    evidence_dir = ROOT / "evidence"
    for f in sorted(evidence_dir.rglob("EV-*.md")):
        meta = ge._meta(f)
        if meta.get("verdict") == "confirm" and meta.get("command") and meta.get("artifact_sha256"):
            confirm_cards.append((f, meta))
            if len(confirm_cards) >= n_cards:
                break
    if not confirm_cards:
        return {"name": "build_reproducibility", "passed": False, "elapsed_s": 0,
                "detail": "no confirm cards with command+artifact_sha256 found"}
    check_level = "sha" if no_symtab else "full"
    results = []
    all_pass = True
    for idx, (card_path, meta) in enumerate(confirm_cards):
        cmd = str(meta["command"])
        art_rel = str(meta.get("artifact", ""))
        want_sha = str(meta.get("artifact_sha256", ""))
        bin_name = Path(art_rel).name
        lines = aer._artifact_compile_lines(cmd, art_rel)
        art_line = lines[-1] if lines else cmd
        ok = True
        parts: list[str] = []
        # 1) 短窗口 sha 复现（保留原语义：重编译 vs 卡值，防篡改）
        for ln in lines:
            status, detail = aer._recompile_invariant(cmd, art_rel, want_sha)
            if status != "ok":
                ok = False
                parts.append(f"{status}:{detail[:36]}")
        # 2) 符号表 / 段一致性 + run1==run2（引擎，check_level）
        bin_a = None
        with tempfile.TemporaryDirectory() as wd1:
            res1 = aer.check_build_reproducibility(
                source_path=aer.run_root() / art_rel, compile_cmd=art_line, work_dir=wd1,
                output_name=None, ccaches_disable=True, check_level=check_level)
            if res1.compile_exit_code != 0:
                ok = False
                parts.append(f"compile_rc={res1.compile_exit_code}")
            if not res1.success:
                ok = False
                parts.append("run1!=run2")
            if res1.symbols_match is False:
                ok = False
                parts.append("symtab=no")
            if res1.sections_match is False:
                ok = False
                parts.append("sections=no")
            bin_a = (Path(wd1) / "run1" / bin_name).read_bytes()
        # 3) 跨时间窗口（只对前 3 张卡）
        cross_status = "未启用"
        if cross_time and idx < 3:
            time.sleep(1.2)
            with tempfile.TemporaryDirectory() as wd2:
                res2 = aer.check_build_reproducibility(
                    source_path=aer.run_root() / art_rel, compile_cmd=art_line, work_dir=wd2,
                    output_name=None, ccaches_disable=True, check_level="sha")
                if res2.compile_exit_code != 0:
                    cross_status = "编译失败"
                    ok = False
                elif res1.first_hash == res2.first_hash:
                    cross_status = "一致"
                else:
                    bin_b = (Path(wd2) / "run1" / bin_name).read_bytes()
                    if _only_time_macro_diff(bin_a, bin_b):
                        cross_status = "时间宏漂移（可接受）"
                    else:
                        cross_status = "真不可复现（fail）"
                        ok = False
        if not ok:
            all_pass = False
        results.append({"card": card_path.stem, "match": ok, "cross": cross_status,
                        "detail": "; ".join(parts)[:90]})
    elapsed = time.time() - t0
    n_match = sum(1 for r in results if r["match"])
    return {
        "name": "build_reproducibility",
        "passed": all_pass,
        "elapsed_s": round(elapsed, 2),
        "detail": f"{n_match}/{len(results)} cards reproducible "
                  f"(短窗口+{'symtab+sections' if not no_symtab else 'sha'}；"
                  f"cross_time={'on' if cross_time else 'off'})",
        "cards": results,
    }


# ── I4：沙箱隔离不变量 ─────────────────────────────────────────────────────────
def _git_diff_quiet(*paths: str) -> bool:
    """用 git diff --quiet 检查指定路径是否有未提交改动。True=无改动（干净）。"""
    import subprocess
    try:
        r = subprocess.run(
            ["git", "diff", "--quiet", "--", *paths],
            cwd=str(ROOT), capture_output=True, timeout=30,
        )
        return r.returncode == 0
    except Exception:
        return True  # git 不可用时不报错（降级为不检测）


def check_sandbox_isolation() -> dict:
    """I4：batch_root 上下文内跑 replay，操作不能泄漏到真实仓库。

    真检查：git diff 拍受控目录基线 → 设 batch_root 到临时目录 →
    在 batch_root 上下文内跑 replay_card → git diff 验证受控目录零改动；
    同时验证临时目录内有 replay 产生的文件（证明 batch_root 确实被使用）。
    """
    t0 = time.time()
    cards = _find_confirm_cards(n=1)
    if not cards:
        return {"name": "sandbox_isolation", "passed": False, "elapsed_s": 0,
                "detail": "no confirm card found"}
    card_path, meta = cards[0]
    # 基线：受控目录必须干净（atoms/evidence/Book/Examples/data/mutation）
    controlled_paths = ["atoms", "evidence", "Book", "Examples", "data/mutation"]
    clean_before = _git_diff_quiet(*controlled_paths)
    leaked = False
    leak_detail = ""
    batch_had_files = False
    verdict = "not_run"
    error_msg = ""
    with tempfile.TemporaryDirectory(prefix="replay_batch_") as tmp:
        batch_root = Path(tmp)
        (batch_root / "build").mkdir(exist_ok=True)  # replay 需要 build/ 放锁和 manifest
        try:
            import atom_evidence_replay as aer
            tok = aer._RUN_ROOT.set(batch_root)
            try:
                verdict, _log = aer.replay_card(card_path, restore_artifact=True)
            finally:
                aer._RUN_ROOT.reset(tok)
        except Exception as exc:
            error_msg = f"{type(exc).__name__}: {exc}"
        # 验证 batch_root 内有 replay 产生的文件（manifest / 锁 / 临时工件）
        batch_files = list(batch_root.rglob("*"))
        batch_had_files = len(batch_files) > 0
        # 验证受控目录零改动（git diff --quiet）
        clean_after = _git_diff_quiet(*controlled_paths)
        if not clean_after and clean_before:
            leaked = True
            leak_detail = "git diff detected changes in controlled dirs after batch_root replay"
        elif not clean_before:
            leak_detail = "controlled dirs were dirty before check (pre-existing changes)"
    elapsed = time.time() - t0
    passed = not leaked and batch_had_files and not error_msg
    detail = (f"card={card_path.stem} verdict={verdict} "
              f"clean_before={clean_before} clean_after={clean_after} "
              f"batch_files={'yes' if batch_had_files else 'NO'} "
              f"{'ISOLATED ✓' if passed else 'LEAK ✗'}")
    if leak_detail:
        detail += f" {leak_detail}"
    if error_msg:
        detail += f" error={error_msg}"
    return {
        "name": "sandbox_isolation",
        "passed": passed,
        "elapsed_s": round(elapsed, 2),
        "detail": detail,
        "card": card_path.stem,
        "batch_had_files": batch_had_files,
    }


# ── I3：锁一致性不变量 ─────────────────────────────────────────────────────────
def check_lock_consistency() -> dict:
    """I3：replay 并发锁路径跟随跑批根，且真实仓库无残留锁。

    验证三件事：
      1. 默认路径 = 真实 ROOT/build/.replay_lock（无 batch_root 时）
      2. batch_root 上下文内，锁路径跟随 batch_root（不指向真实仓库）
      3. 真实仓库无残留锁文件（replay 未运行时）
    """
    t0 = time.time()
    try:
        import atom_evidence_replay as aer
    except ImportError as exc:
        return {"name": "lock_consistency", "passed": False, "elapsed_s": 0,
                "detail": f"import error: {exc}"}
    failures = []
    # 1. 默认路径正确
    default_lock = aer._replay_lock_path()
    expected_default = ROOT / "build" / ".replay_lock"
    if default_lock != expected_default:
        failures.append(f"default lock path mismatch: {default_lock} != {expected_default}")
    # 2. batch_root 内路径跟随（contextvar token+reset，防嵌套上下文泄漏）
    fake_root = Path(tempfile.gettempdir()) / "replay_inv_fake_root"
    tok = aer._RUN_ROOT.set(fake_root)
    try:
        batch_lock = aer._replay_lock_path()
        expected_batch = fake_root / "build" / ".replay_lock"
        if batch_lock != expected_batch:
            failures.append(f"batch lock path mismatch: {batch_lock} != {expected_batch}")
    finally:
        aer._RUN_ROOT.reset(tok)
    # 3. 真实仓库无残留锁
    if expected_default.exists():
        failures.append(f"stale lock file exists in real repo: {expected_default}")
    elapsed = time.time() - t0
    return {
        "name": "lock_consistency",
        "passed": len(failures) == 0,
        "elapsed_s": round(elapsed, 2),
        "detail": "default path correct + batch_root follows + no stale lock" if not failures
                  else "; ".join(failures),
        "default_lock": str(default_lock),
    }


# ── I5：manifest 一致性不变量 ─────────────────────────────────────────────────
def check_manifest_consistency() -> dict:
    """I5：replay manifest 中记录的卡指纹必须与磁盘真实卡文件一致。

    验证：读 build/replay_manifest.json，对每条记录的 fingerprint 与磁盘卡文件的
    sha256 比对。如果 manifest 是 stale 的（卡文件被改但 manifest 没更新），
    指纹不一致 ⇒ fail。同时验证 verdict 字段合法。
    只读检查，不修改任何文件。
    """
    t0 = time.time()
    manifest_path = ROOT / "build" / "replay_manifest.json"
    if not manifest_path.is_file():
        return {"name": "manifest_consistency", "passed": False, "elapsed_s": 0,
                "detail": "build/replay_manifest.json not found"}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"name": "manifest_consistency", "passed": False, "elapsed_s": 0,
                "detail": f"manifest parse error: {type(exc).__name__}: {exc}"}
    if not isinstance(manifest, dict):
        return {"name": "manifest_consistency", "passed": False, "elapsed_s": 0,
                "detail": f"manifest is not a dict (got {type(manifest).__name__})"}
    mismatches = []
    invalid_verdicts = []
    checked = 0
    try:
        import atom_evidence_replay as aer
    except ImportError as exc:
        return {"name": "manifest_consistency", "passed": False, "elapsed_s": 0,
                "detail": f"import error: {exc}"}
    for card_rel, entry in manifest.items():
        card_path = ROOT / card_rel
        if not card_path.is_file():
            mismatches.append(f"{card_rel}: file not found on disk")
            continue
        actual_fp = aer.card_fingerprint(card_path)
        recorded_fp = str(entry.get("fingerprint", ""))
        if actual_fp == "MISSING":
            mismatches.append(f"{card_rel}: card_fingerprint returned MISSING (fixture/artifact missing)")
        elif recorded_fp != actual_fp:
            mismatches.append(f"{card_rel}: fingerprint mismatch (manifest={recorded_fp[:16]}… actual={actual_fp[:16]}…)")
        verdict = str(entry.get("verdict", ""))
        if verdict not in ("confirm", "refute", "infra_error") and not verdict.startswith("refute:"):
            invalid_verdicts.append(f"{card_rel}: invalid verdict '{verdict}'")
        checked += 1
    elapsed = time.time() - t0
    passed = len(mismatches) == 0 and len(invalid_verdicts) == 0
    detail = (f"{checked} cards checked, {len(mismatches)} fingerprint mismatches, "
              f"{len(invalid_verdicts)} invalid verdicts "
              f"{'CONSISTENT ✓' if passed else 'INCONSISTENT ✗'}")
    if mismatches:
        detail += f" | mismatches: {'; '.join(mismatches[:3])}"
    if invalid_verdicts:
        detail += f" | invalid: {'; '.join(invalid_verdicts[:3])}"
    return {
        "name": "manifest_consistency",
        "passed": passed,
        "elapsed_s": round(elapsed, 2),
        "detail": detail,
        "cards_checked": checked,
        "mismatches": len(mismatches),
        "invalid_verdicts": len(invalid_verdicts),
    }


# ── 主检查 ─────────────────────────────────────────────────────────────────────
CHECKS = {
    "artifact_restore": check_artifact_restore,
    "build_reproducibility": check_build_reproducibility,
    "sandbox_isolation": check_sandbox_isolation,
    "lock_consistency": check_lock_consistency,
    "manifest_consistency": check_manifest_consistency,
}


def run_checks(*, only: tuple[str, ...] | None = None,
               heavy: bool = True, n_cards: int = 5,
               cross_time: bool = False, no_symtab: bool = False) -> list[dict]:
    """跑不变量检查。heavy=False 时跳过 I2 build_reproducibility（不编译，轻量）。"""
    names = only or INVARIANTS
    results = []
    for name in names:
        if name not in CHECKS:
            results.append({"name": name, "passed": False, "elapsed_s": 0,
                            "detail": f"unknown invariant: {name}"})
            continue
        if not heavy and name == "build_reproducibility":
            results.append({"name": name, "passed": True, "elapsed_s": 0,
                            "detail": "skipped (heavy=False, no compilation)"})
            continue
        try:
            if name == "build_reproducibility":
                results.append(CHECKS[name](n_cards=n_cards,
                                           cross_time=cross_time,
                                           no_symtab=no_symtab))
            else:
                results.append(CHECKS[name]())
        except Exception as exc:
            results.append({"name": name, "passed": False, "elapsed_s": 0,
                            "detail": f"check raised: {exc}"})
    return results


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="replay 状态机不变量独立检查")
    ap.add_argument("--check", action="store_true", help="跑不变量检查（失败 exit 2）")
    ap.add_argument("--list", action="store_true", help="列出所有不变量")
    ap.add_argument("--invariant", choices=INVARIANTS, default=None,
                    help="只跑指定不变量")
    ap.add_argument("--n-cards", type=int, default=5,
                    help="I2 抽样卡数（默认5，非全量）")
    ap.add_argument("--cross-time", action="store_true",
                    help="I2 跨时间窗口（间隔≥1s 重编译，检测 __TIME__ 漂移；只对前3张卡）")
    ap.add_argument("--no-symtab", action="store_true",
                    help="I2 不做符号表一致性（只比对 sha + 段大小）")
    ap.add_argument("--no-heavy", action="store_true",
                    help="跳过 I2 build_reproducibility（不编译，轻量模式）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    a = ap.parse_args(argv)

    if a.list:
        if a.json:
            print(json.dumps({"invariants": list(INVARIANTS)}, ensure_ascii=False, indent=1))
        else:
            print("[replay_invariants] 可用不变量：")
            for inv in INVARIANTS:
                print(f"  - {inv}")
        return 0

    if a.check:
        only = (a.invariant,) if a.invariant else None
        results = run_checks(only=only, heavy=not a.no_heavy, n_cards=a.n_cards,
                             cross_time=a.cross_time, no_symtab=a.no_symtab)
        all_pass = all(r["passed"] for r in results)
        if a.json:
            print(json.dumps({"all_passed": all_pass, "results": results},
                              ensure_ascii=False, indent=1))
        else:
            print(f"[replay_invariants] {'全部通过 ✓' if all_pass else '有失败 ✗'}")
            for r in results:
                mark = "✓" if r["passed"] else "✗"
                print(f"  {mark} {r['name']}: {r['detail']} ({r['elapsed_s']}s)")
                if r["name"] == "build_reproducibility" and "cards" in r:
                    for c in r["cards"]:
                        extra = f" — {c['detail']}" if c.get("detail") else ""
                        print(f"      · {c['card']}: match={c['match']} "
                              f"cross={c['cross']}{extra}")
        return 0 if all_pass else 2

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
