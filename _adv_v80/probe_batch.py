"""v5 对抗复测（批量）：N2 修正 + E10 两变种 + E05 + E11 + E04 + E06。

关键口径：拦住 = 卡无法直推 confirm/verified（block 或 refute）；
warn/advice/experimental 只"可见"，卡仍能 confirm ⇒ 计为**仍逃逸（严格口径）**。
"""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge  # noqa: E402
import toolchain  # noqa: E402

PROBE = ROOT / "_adv_v80" / "probes"
PROBE.mkdir(parents=True, exist_ok=True)
replay._REPLAY_LOCK = ROOT / "_adv_v80" / ".replay_lock"
GPP = Path(toolchain.resolve_gpp()).as_posix()


def line(tag: str, verdict: str, note: str = "") -> None:
    print(f"[{tag:<30}] {verdict}" + (f"  | {note}" if note else ""))


def mk(name: str, cmd: str, fx_src: str, asserts: str = "", **extra) -> Path:
    fx = PROBE / f"{name}.cpp"
    fx.write_text(fx_src, encoding="utf-8")
    (PROBE / f"{name}.out").write_text("k=1\n", encoding="utf-8")
    body = (
        f"---\nid: EV-ADV80-{name.upper()}\nserves: []\nhypothesis: h\nkind: asm\n"
        f"command: |\n{cmd}\nfixture: {fx.relative_to(ROOT).as_posix()}\n"
        f"artifact: {(PROBE / (name + '.asm')).relative_to(ROOT).as_posix()}\n"
        "artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111\n"
        "artifact_compiler: Clang 19.0.0 (Linux)\n"
        "verdict: confirm\nfalsification: f\nexpected: any\n"
        f"actual:\n  run_match_file: {(PROBE / (name + '.out')).relative_to(ROOT).as_posix()}\n"
        "  run_match_keys: [k]\n")
    if asserts:
        body += "artifact_assert:\n" + asserts
    for k, v in extra.items():
        body += f"{k}: {v}\n"
    body += "---\n"
    p = PROBE / f"EV-ADV80-{name.upper()}.md"
    p.write_text(body, encoding="utf-8")
    return p


# ── N2：跨编译器 + 全局恒真断言（P0-C 只治 contains_in）────────────────
c = mk("n2", f'  "{GPP}" -std=c++17 -S "{PROBE}/n2.cpp" -o "{PROBE}/n2.asm"',
       "int main(){return 0;}\n",
       "  - {kind: contains_any, texts: ['zzz_absent', '.file']}\n")
v, log = replay.replay_card(c, do_sanitizer=False)
line("N2 跨编译器+全局恒真", v,
     "逃逸（断言零信息仍 confirm）" if v == "confirm" else "已拦")

# ── E10a：零诊断措辞在 expected（无 -Werror）───────────────────────────
c = mk("e10a", f'  "{GPP}" -Wall -c "{PROBE}/e10a.cpp" -o "{PROBE}/e10a.o"',
       "int main(){return 0;}\n")
txt = c.read_text(encoding="utf-8").replace("expected: any", "expected: 零诊断（编译无警告）")
c.write_text(txt, encoding="utf-8")
v, _ = replay.replay_card(c, do_sanitizer=False)
tmpd = Path(tempfile.mkdtemp())
(tmpd / "evidence").mkdir()
orig_ev = ge.EVIDENCE
ge.EVIDENCE = tmpd / "evidence"
shutil.copy(c, tmpd / "evidence" / c.name)
warns = [f.message[:60] for f in ge.check_evidence_zero_diag_werror()
         if f.severity == "warn"]
ge.EVIDENCE = orig_ev
shutil.rmtree(tmpd, ignore_errors=True)
line("E10a 零诊断字段位移", v,
     f"gate warn={bool(warns)} → {'仍逃逸（卡 confirm，warn 不阻断）' if v == 'confirm' else '已拦'}")

# ── E10b：pragma 消音 + -Werror ────────────────────────────────────────
c = mk("e10b", f'  "{GPP}" -Wall -Wextra -Werror -c "{PROBE}/e10b.cpp" -o "{PROBE}/e10b.o"',
       '#pragma GCC diagnostic ignored "-Wunused-variable"\n'
       "int main(){ int unused_v = 1; return 0; }\n")
v, _ = replay.replay_card(c, do_sanitizer=False)
tmpd = Path(tempfile.mkdtemp())
(tmpd / "evidence").mkdir()
ge.EVIDENCE = tmpd / "evidence"
shutil.copy(c, tmpd / "evidence" / c.name)
warns = [f.message[:60] for f in ge.check_evidence_zero_diag_werror()
         if f.severity == "warn"]
ge.EVIDENCE = orig_ev
shutil.rmtree(tmpd, ignore_errors=True)
line("E10b pragma 消音+-Werror", v,
     f"gate warn={bool(warns)} → {'仍逃逸（卡 confirm）' if v == 'confirm' else '已拦'}")

# ── E05：cat 式证据（读文件原样打印）───────────────────────────────────
data = PROBE / "expected_data.txt"
data.write_text("result=42\n", encoding="utf-8")
c = mk("e05", f'  "{GPP}" -std=c++17 "{PROBE}/e05.cpp" -o "{PROBE}/e05.exe" && "{PROBE}/e05.exe"',
       '#include <cstdio>\n#include <fstream>\n#include <string>\n'
       'int main(){ std::ifstream f("_adv_v80/probes/expected_data.txt"); std::string l;\n'
       '  while (std::getline(f, l)) std::printf("%s\\n", l.c_str()); }\n')
(PROBE / "e05.out").write_text("result=42\n", encoding="utf-8")
v, _ = replay.replay_card(c, do_sanitizer=False)
hits = ge.check_fixture_no_echo_data([c])
line("E05 cat 式证据", v,
     f"exp-scan 命中={bool(hits)} → {'仍逃逸（experimental 零输出，卡 confirm）' if v == 'confirm' else '已拦'}")

# ── E11：冲突同义词（cancels，470 归一后）──────────────────────────────
tmpd = Path(tempfile.mkdtemp())
(tmpd / "atoms" / "mem").mkdir(parents=True)
orig = (ge.ATOMS, ge.ROOT)
ge.ATOMS, ge.ROOT = tmpd / "atoms", tmpd
try:
    def atom(aid: str, rel: str) -> None:
        (tmpd / "atoms" / "mem" / f"{aid}.md").write_text(
            f"---\nid: {aid}\ntitle: t\ndomain: MEM\ntype: mechanism\nstatus: draft\n"
            "claim: c\nclaim_boundary: b\nevidence: []\n"
            "sources: '[{kind: iso, ref: X, independent: true}]'\nfirst_hand: 'false'\n"
            f"superiority: s\ndepth: d\npedagogy: p\nrelations:\n  - {rel}\n---\n",
            encoding="utf-8")
    atom("ATOM-P", "prerequisite: ATOM-Q")
    atom("ATOM-Q", "cancels: ATOM-P")     # 同义词（470 归一前静默）
    hits = ge.check_atom_rel_conflict()
    line("E11 冲突同义词(归一后)", "已拦" if hits else "仍逃逸（静默共存）",
         hits[0].message[:50] if hits else "")
    # 未归一的第 5 种：refutes
    atom("ATOM-Q", "refutes: ATOM-P")
    hits2 = ge.check_atom_rel_conflict()
    line("E11b 同义词 refutes(未归一)", "已拦" if hits2 else "仍逃逸（新同义词仍静默）")
finally:
    ge.ATOMS, ge.ROOT = orig
    shutil.rmtree(tmpd, ignore_errors=True)

# ── E04：全角/中文 .out 键 ─────────────────────────────────────────────
tmpd = Path(tempfile.mkdtemp())
(tmpd / "evidence").mkdir()
(tmpd / "e.out").write_text("ｎｐｒｏｃ=32\n", encoding="utf-8")   # 全角键
(tmpd / "evidence" / "EV-U.md").write_text(
    "---\nid: EV-U\nserves: []\nhypothesis: h\nkind: run\ncommand: g++ a.cpp\n"
    "fixture: a.cpp\nartifact: a.asm\nartifact_sha256: " + "0" * 64 + "\n"
    "verdict: confirm\nfalsification: f\n"
    "actual:\n  run_match_file: e.out\n  run_match_keys: []\n---\n", encoding="utf-8")
ge.EVIDENCE, ge.ROOT = tmpd / "evidence", tmpd
try:
    hits = ge.check_evidence_out_undeclared_key()
    line("E04 全角键 .out", f"{hits[0].severity if hits else '无命中'}",
         "已拦" if hits and hits[0].severity == "block" else
         ("仍逃逸（仅 warn，卡可 confirm）" if hits else "漏检"))
finally:
    ge.EVIDENCE, ge.ROOT = orig_ev, ROOT
    shutil.rmtree(tmpd, ignore_errors=True)

# ── E06：.out 虚构留痕（mtime 陈旧）────────────────────────────────────
tmpd = Path(tempfile.mkdtemp())
(tmpd / "evidence").mkdir()
(tmpd / "fx.cpp").write_text("int main(){return 0;}\n", encoding="utf-8")
(tmpd / "s.out").write_text("k=1\n", encoding="utf-8")
import os, time  # noqa: E402
past = time.time() - 6000
os.utime(tmpd / "s.out", (past, past))
(tmpd / "evidence" / "EV-S.md").write_text(
    "---\nid: EV-S\nserves: []\nhypothesis: h\nkind: run\ncommand: g++ fx.cpp\n"
    "fixture: fx.cpp\nartifact: a.asm\nartifact_sha256: " + "0" * 64 + "\n"
    "verdict: confirm\nfalsification: f\n"
    "actual:\n  run_match_file: s.out\n  run_match_keys: [k]\n---\n", encoding="utf-8")
ge.EVIDENCE, ge.ROOT = tmpd / "evidence", tmpd
try:
    hits = ge.check_evidence_out_stale_mtime()
    line("E06 .out 陈旧留痕", hits[0].severity if hits else "无命中",
         "仍逃逸（advice 不阻断）" if hits and hits[0].severity == "advice" else
         ("已拦" if hits else "漏检"))
finally:
    ge.EVIDENCE, ge.ROOT = orig_ev, ROOT
    shutil.rmtree(tmpd, ignore_errors=True)
