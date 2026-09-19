"""v5 对抗复测（最终）：夹具输出与 .out 严格一致，取真实 verdict。"""
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
replay._REPLAY_LOCK = ROOT / "_adv_v80" / ".replay_lock"
GPP = Path(toolchain.resolve_gpp()).as_posix()
BASE = '#include <cstdio>\nint main(){ std::printf("k=1\\n"); return 0; }\n'


def line(tag: str, verdict: str, note: str = "") -> None:
    print(f"[{tag:<26}] {verdict}" + (f"  | {note}" if note else ""))


def mk(name: str, extra_cmd: str, fx_src: str = BASE, asserts: str = "",
       out_text: str = "k=1\n", key: str = "k") -> Path:
    fx = PROBE / f"{name}.cpp"
    fx.write_text(fx_src, encoding="utf-8")
    art, out = PROBE / f"{name}.asm", PROBE / f"{name}.out"
    out.write_text(out_text, encoding="utf-8")
    cmd = (f'  "{GPP}" -std=c++17 -S "{fx.as_posix()}" -o "{art.as_posix()}"\n'
           + extra_cmd)
    body = (
        f"---\nid: EV-ADV80-{name.upper()}\nserves: []\nhypothesis: h\nkind: asm\n"
        f"command: |\n{cmd}\nfixture: {fx.relative_to(ROOT).as_posix()}\n"
        f"artifact: {art.relative_to(ROOT).as_posix()}\n"
        "artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111\n"
        "artifact_compiler: Clang 19.0.0 (Linux)\n"
        "verdict: confirm\nfalsification: f\nexpected: any\n"
        f"actual:\n  run_match_file: {out.relative_to(ROOT).as_posix()}\n"
        f"  run_match_keys: [{key}]\n")
    if asserts:
        body += "artifact_assert:\n" + asserts
    p = PROBE / f"EV-ADV80-{name.upper()}.md"
    p.write_text(body + "---\n", encoding="utf-8")
    return p


def gate_warn(c: Path, fn) -> bool:
    tmpd = Path(tempfile.mkdtemp()); (tmpd / "evidence").mkdir()
    orig = ge.EVIDENCE
    ge.EVIDENCE = tmpd / "evidence"
    try:
        shutil.copy(c, tmpd / "evidence" / c.name)
        return bool([f for f in fn() if f.severity in ("warn", "block")])
    finally:
        ge.EVIDENCE = orig
        shutil.rmtree(tmpd, ignore_errors=True)


# N2：跨编译器 + 全局恒真断言（P0-C 不治 contains/contains_any）
c = mk("n2c", "", asserts="  - {kind: contains_any, texts: ['zzz_absent', '.file']}\n")
v, _ = replay.replay_card(c, do_sanitizer=False)
line("N2 全局恒真断言", v, "逃逸（零信息断言 confirm）" if v == "confirm" else "已拦")

# E10a：零诊断措辞在 expected，无 -Werror
c = mk("e10c", f'  "{GPP}" -Wall -c "{PROBE}/e10c.cpp" -o "{PROBE}/e10c.o"\n')
c.write_text(c.read_text(encoding="utf-8").replace(
    "expected: any", "expected: 零诊断（编译无警告）"), encoding="utf-8")
v, _ = replay.replay_card(c, do_sanitizer=False)
line("E10a 字段位移", v,
     f"gate={gate_warn(c, ge.check_evidence_zero_diag_werror)} → "
     + ("仍逃逸（卡 confirm）" if v == "confirm" else "已拦"))

# E10b：pragma 消音 + -Werror（判据形同虚设）
c = mk("e10d",
       f'  "{GPP}" -Wall -Wextra -Werror -c "{PROBE}/e10d.cpp" -o "{PROBE}/e10d.o"\n',
       '#pragma GCC diagnostic ignored "-Wunused-variable"\n' + BASE)
v, _ = replay.replay_card(c, do_sanitizer=False)
line("E10b pragma 消音", v,
     f"gate={gate_warn(c, ge.check_evidence_zero_diag_werror)} → "
     + ("仍逃逸（卡 confirm）" if v == "confirm" else "已拦"))

# E05：cat 式证据（原样打印随库数据文件）
(PROBE / "expected_data.txt").write_text("result=42\n", encoding="utf-8")
c = mk("e05c",
       f'  "{GPP}" -std=c++17 "{PROBE}/e05c.cpp" -o "{PROBE}/e05c.exe"\n'
       f'  "{PROBE}/e05c.exe"\n',
       '#include <cstdio>\n#include <fstream>\n#include <string>\n'
       'int main(){ std::ifstream f("_adv_v80/probes/expected_data.txt"); std::string l;\n'
       '  while (std::getline(f, l)) std::printf("%s\\n", l.c_str()); }\n',
       out_text="result=42\n", key="result")
v, _ = replay.replay_card(c, do_sanitizer=False)
line("E05 cat 式证据", v,
     f"exp-scan={bool(ge.check_fixture_no_echo_data([c]))} → "
     + ("仍逃逸（零输出，卡 confirm）" if v == "confirm" else "已拦"))

# P0-A 构建脚本边界（无直接编译行产出 artifact）
c = mk("bsc", "")
txt = c.read_text(encoding="utf-8")
txt = txt.replace(f'"{GPP}" -std=c++17 -S', f'python -c "print(1)"  # {GPP} -std=c++17 -S')
c.write_text(txt, encoding="utf-8")
v, _ = replay.replay_card(c, do_sanitizer=False)
line("P0-A 构建脚本边界", v, "fail-closed" if v != "confirm" else "静默放行=逃逸")
