"""v5 对抗复测（核心）：E01/E03 现成探针 + 新逃逸 N1 + E07 变体 + E12 签收。

只信实跑结果。不修改任何工具/正式文件。
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge  # noqa: E402

PROBE = ROOT / "_adv_v80" / "probes"
PROBE.mkdir(parents=True, exist_ok=True)


def line(tag: str, verdict: str, note: str = "") -> None:
    print(f"[{tag:<36}] {verdict}" + (f"  | {note}" if note else ""))


# ── A. E01：编译后覆写（P0-A 声称已修）───────────────────────────────────
v, _ = replay.replay_card(ROOT / "_adv_v70/probes/EV-ADV70-H1.md", do_sanitizer=False)
line("E01 编译后覆写（H1 探针）", v, "refute=拦住 / confirm=仍逃逸")

# ── B. E03：恒真符号（P0-C 声称已修，探针含 contains_in）────────────────
v, _ = replay.replay_card(ROOT / "_adv_v70/probes/EV-ADV70-H3.md", do_sanitizer=False)
line("E03 恒真符号（H3 探针）", v)

# ── C. N1 新逃逸：跨编译器 + **全局**恒真断言（不含 contains_in）─────────
# 思路：P0-C 的判别力统计只作用于 contains_in（区间）；全局 contains/contains_any
# 上的恒真文本（.file/.text 任何 gcc -S 产物都有）不受约束 ⇒ 断言零信息仍 confirm。
fx = PROBE / "n1.cpp"
fx.write_text("int main(){return 0;}\n", encoding="utf-8")
art = PROBE / "n1.asm"
gpp = Path(replay.__file__).parent / "toolchain.py"
import importlib  # noqa: E402
tc = importlib.import_module("toolchain")
exe = ROOT / "build" / "_adv80_n1.exe"
subprocess.run([tc.resolve_gpp(), "-std=c++17", "-S", str(fx), "-o", str(art)],
               capture_output=True)
card = PROBE / "EV-ADV80-N1.md"
card.write_text(
    "---\nid: EV-ADV80-N1\nserves: []\nhypothesis: h\nkind: asm\n"
    f"command: |\n  \"{Path(tc.resolve_gpp()).as_posix()}\" -std=c++17 -S \"{fx.as_posix()}\""
    f" -o \"{art.as_posix()}\"\n"
    f"fixture: {fx.relative_to(ROOT).as_posix()}\n"
    f"artifact: {art.relative_to(ROOT).as_posix()}\n"
    "artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111\n"
    "artifact_compiler: Clang 19.0.0 (Linux)\n"
    "verdict: confirm\nfalsification: f\n"
    "expected: any\n"
    "actual:\n  run_match_file: _adv_v80/probes/n1.out\n  run_match_keys: [k]\n"
    "artifact_assert:\n"
    "  - {kind: contains_any, texts: [\".file\", \".text\", \"main\"]}\n"
    "---\n", encoding="utf-8")
(PROBE / "n1.out").write_text("k=1\n", encoding="utf-8")
v, log = replay.replay_card(card, do_sanitizer=False)
hit = [l for l in log if "artifact_assert" in l]
line("N1 跨编译器+全局恒真断言", v,
     "confirm=逃逸（断言零信息）" if v == "confirm" else "已拦")
for l in hit[:2]:
    print("      ", l.strip()[:100])

# ── D. E12：签收字符串自证（P0-G2 未做）─────────────────────────────────
tmp = Path(tempfile.mkdtemp())
atoms = tmp / "atoms" / "mem"
ev = tmp / "evidence" / "mem"
atoms.mkdir(parents=True)
ev.mkdir(parents=True)
orig_a, orig_e, orig_root = ge.ATOMS, ge.EVIDENCE, ge.ROOT
ge.ATOMS, ge.EVIDENCE, ge.ROOT = atoms.parent, ev.parent, tmp
try:
    (ev / "EV-C.md").write_text(
        "---\nid: EV-C\nserves: [ATOM-X]\nverdict: confirm\nhypothesis: h\n"
        "command: g++ a.cpp\nfixture: a.cpp\nartifact: a.asm\n"
        "artifact_sha256: " + "0" * 64 + "\nkind: asm\nfalsification: f\n---\n",
        encoding="utf-8")
    (atoms / "ATOM-X.md").write_text(
        "---\nid: ATOM-X\ntitle: t\ndomain: MEM\ntype: mechanism\nstatus: verified\n"
        "claim: c\nclaim_boundary: b\nrelations: []\nevidence: [EV-C]\n"
        "sources: '[{kind: iso, ref: X, independent: true}]'\nfirst_hand: 'false'\n"
        "superiority: s\ndepth: d\npedagogy: p\n"
        "verified_by: human:liaoranran\n"
        "status_history:\n  - {level: machine-verified, at: 2026-09-13, by: machine:gate}\n"
        "  - {level: human-verified, at: 2026-09-13, by: human:liaoranran}\n---\n",
        encoding="utf-8")
    blocks = [f.rule_id for f in ge.run(include_advice=False) if f.severity == "block"]
    line("E12 签收字符串自证", "逃逸（0 block）" if not blocks else f"已拦 {blocks}",
         "verified_by 写人名为字符串即可直推 verified")
finally:
    ge.ATOMS, ge.EVIDENCE, ge.ROOT = orig_a, orig_e, orig_root

# ── E. E07 变体：缩进走私（tab / 引号值 / 列表项后）─────────────────────
variants = {
    "空格缩进": "fixture: f.cpp &x\n  verdict: confirm\n",
    "tab 缩进": "fixture: f.cpp &x\n\tverdict: confirm\n",
    "引号值+缩进": 'fixture: "f.cpp"\n  verdict: confirm\n',
    "列表项后缩进": "tags:\n  - a\n  verdict: confirm\n",
}
orig_ev = ge.EVIDENCE
ge.EVIDENCE = tmp / "evidence"
(tmp / "evidence").mkdir(exist_ok=True)
try:
    for name, body in variants.items():
        p = tmp / "evidence" / "EV-S.md"
        p.write_text("---\nid: EV-S\nstatus: draft\n" + body + "hypothesis: h\n---\n",
                     encoding="utf-8")
        meta = replay.parse_frontmatter(p.read_text(encoding="utf-8"))
        lifted = meta.get("verdict")
        hits = [f for f in ge.check_frontmatter_hardening() if f.severity == "block"]
        detected = bool(hits)
        line(f"E07 变体·{name}",
             f"顶层verdict={lifted!r} 检测命中={detected}",
             "逃逸（提升未检出）" if (lifted == "confirm" and not detected)
             else ("无效载荷" if lifted != "confirm" else "已拦"))
finally:
    ge.EVIDENCE = orig_ev
