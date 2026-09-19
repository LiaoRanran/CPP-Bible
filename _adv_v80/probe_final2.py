"""v5 对抗复测（定稿）：跨编译器结构断言路径 + 恒真断言 + 运行行产出 stdout。

只有让卡能走完 replay 全流程（含 run_match）才能判定"逃逸/已拦"：
  command = ①产出 artifact(asm) ②被测命令 ③编译 exe + 运行（stdout 与 .out 一致）
  artifact_compiler = Clang（≠本地）⇒ 走结构断言路径，断言恒真 .file
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge  # noqa: E402
import toolchain  # noqa: E402

PROBE = ROOT / "_adv_v80" / "probes"
replay._REPLAY_LOCK = ROOT / "_adv_v80" / ".replay_lock"
GPP = Path(toolchain.resolve_gpp()).as_posix()
BASE = '#include <cstdio>\nint main(){ std::printf("k=1\\n"); return 0; }\n'
TRIVIAL_ASSERT = "  - {kind: contains_any, texts: ['zzz_absent', '.file']}\n"


def line(tag: str, verdict: str, note: str = "") -> None:
    print(f"[{tag:<24}] {verdict}" + (f"  | {note}" if note else ""))


def mk(name: str, mid_cmd: str, fx_src: str = BASE,
       assert_kind: str = TRIVIAL_ASSERT) -> Path:
    fx = PROBE / f"{name}.cpp"
    fx.write_text(fx_src, encoding="utf-8")
    art, out = PROBE / f"{name}.asm", PROBE / f"{name}.out"
    exe = PROBE / f"{name}.exe"
    out.write_text("k=1\n", encoding="utf-8")
    cmd = (f'  "{GPP}" -std=c++17 -S "{fx.as_posix()}" -o "{art.as_posix()}"\n'
           + mid_cmd
           + f'  "{GPP}" -std=c++17 "{fx.as_posix()}" -o "{exe.as_posix()}"\n'
           + f'  "{exe.as_posix()}"\n')
    p = PROBE / f"EV-ADV80-{name.upper()}.md"
    p.write_text(
        f"---\nid: EV-ADV80-{name.upper()}\nserves: []\nhypothesis: h\nkind: asm\n"
        f"command: |\n{cmd}fixture: {fx.relative_to(ROOT).as_posix()}\n"
        f"artifact: {art.relative_to(ROOT).as_posix()}\n"
        "artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111\n"
        "artifact_compiler: Clang 19.0.0 (Linux)\n"
        "verdict: confirm\nfalsification: f\nexpected: any\n"
        f"actual:\n  run_match_file: {out.relative_to(ROOT).as_posix()}\n"
        "  run_match_keys: [k]\n"
        "artifact_assert:\n" + assert_kind + "---\n", encoding="utf-8")
    return p


def gate_hit(c: Path, fn) -> str:
    tmpd = Path(tempfile.mkdtemp()); (tmpd / "evidence").mkdir()
    orig = ge.EVIDENCE
    ge.EVIDENCE = tmpd / "evidence"
    try:
        shutil.copy(c, tmpd / "evidence" / c.name)
        hits = [f for f in fn() if f.severity in ("warn", "block")]
        return ",".join(sorted({f.severity for f in hits})) or "无"
    finally:
        ge.EVIDENCE = orig
        shutil.rmtree(tmpd, ignore_errors=True)


# ── N2：全局恒真断言（P0-C 只治 contains_in）─────────────────────────────
c = mk("n3", "")
v, log = replay.replay_card(c, do_sanitizer=False)
line("N2 全局恒真断言", v,
     "逃逸（零信息断言，卡 confirm）" if v == "confirm" else "已拦")

# ── E10a：零诊断措辞在 expected，被测命令无 -Werror ───────────────────────
c = mk("e10e", f'  "{GPP}" -Wall -c "{PROBE}/e10e.cpp" -o "{PROBE}/e10e.o"\n')
c.write_text(c.read_text(encoding="utf-8").replace(
    "expected: any", "expected: 零诊断（编译无警告）"), encoding="utf-8")
v, _ = replay.replay_card(c, do_sanitizer=False)
line("E10a 字段位移", v,
     f"gate={gate_hit(c, ge.check_evidence_zero_diag_werror)} → "
     + ("仍逃逸（卡 confirm，warn 不阻断）" if v == "confirm" else "已拦"))

# ── E10b：pragma 消音 + -Werror（判据形同虚设）───────────────────────────
c = mk("e10f",
       f'  "{GPP}" -Wall -Wextra -Werror -c "{PROBE}/e10f.cpp" -o "{PROBE}/e10f.o"\n',
       '#pragma GCC diagnostic ignored "-Wunused-variable"\n' + BASE)
v, _ = replay.replay_card(c, do_sanitizer=False)
line("E10b pragma 消音", v,
     f"gate={gate_hit(c, ge.check_evidence_zero_diag_werror)} → "
     + ("仍逃逸（卡 confirm）" if v == "confirm" else "已拦"))

# ── E05：cat 式证据（原样打印随库数据文件）───────────────────────────────
(PROBE / "expected_data.txt").write_text("k=1\n", encoding="utf-8")
c = mk("e05e", "",
       '#include <cstdio>\n#include <fstream>\n#include <string>\n'
       'int main(){ std::ifstream f("_adv_v80/probes/expected_data.txt"); std::string l;\n'
       '  while (std::getline(f, l)) std::printf("%s\\n", l.c_str()); }\n')
v, _ = replay.replay_card(c, do_sanitizer=False)
line("E05 cat 式证据", v,
     f"exp-scan={bool(ge.check_fixture_no_echo_data([c]))} → "
     + ("仍逃逸（零输出，卡 confirm）" if v == "confirm" else "已拦"))

# ── 对照：同一夹具不加 cat，只计算（应同样 confirm，证明 exp-scan 命中特异性）
c2 = mk("e05f", "")
v2, _ = replay.replay_card(c2, do_sanitizer=False)
line("  对照·纯计算夹具", v2,
     f"exp-scan={bool(ge.check_fixture_no_echo_data([c2]))}（阴性应无命中）")
