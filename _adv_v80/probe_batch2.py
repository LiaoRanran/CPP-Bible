"""v5 对抗复测（批量 v2）：修正探针（每行 command 含产出 artifact 的编译行）
+ ccache 面 + P0-A 构建脚本边界。
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
replay._REPLAY_LOCK = ROOT / "_adv_v80" / ".replay_lock"
GPP = Path(toolchain.resolve_gpp()).as_posix()


def line(tag: str, verdict: str, note: str = "") -> None:
    print(f"[{tag:<28}] {verdict}" + (f"  | {note}" if note else ""))


def mk(name: str, extra_cmd: str, fx_src: str, asserts: str = "", **kw) -> Path:
    """构造卡：command 第一行产出 artifact(asm)，其后为被测命令。"""
    fx = PROBE / f"{name}.cpp"
    fx.write_text(fx_src, encoding="utf-8")
    art = PROBE / f"{name}.asm"
    out = PROBE / f"{name}.out"
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
        "  run_match_keys: [k]\n")
    if asserts:
        body += "artifact_assert:\n" + asserts
    for k, v in kw.items():
        body += f"{k}: {v}\n"
    body += "---\n"
    p = PROBE / f"EV-ADV80-{name.upper()}.md"
    p.write_text(body, encoding="utf-8")
    return p


# ── N2：跨编译器 + 全局恒真断言（P0-C 不治 contains/contains_any）────────
c = mk("n2b", "", "int main(){return 0;}\n",
       "  - {kind: contains_any, texts: ['zzz_absent', '.file']}\n")
(PROBE / "n2b.out").write_text("k=1\n", encoding="utf-8")
v, log = replay.replay_card(c, do_sanitizer=False)
line("N2 全局恒真断言", v,
     "逃逸（零信息断言仍 confirm）" if v == "confirm" else "已拦")

# ── E10a：零诊断措辞在 expected，command 无 -Werror ─────────────────────
c = mk("e10a", f'  "{GPP}" -Wall -c "{PROBE}/e10a.cpp" -o "{PROBE}/e10a.o"\n',
       "int main(){return 0;}\n")
(PROBE / "e10a.out").write_text("k=1\n", encoding="utf-8")
c.write_text(c.read_text(encoding="utf-8").replace(
    "expected: any", "expected: 零诊断（编译无警告）"), encoding="utf-8")
v, _ = replay.replay_card(c, do_sanitizer=False)
tmpd = Path(tempfile.mkdtemp()); (tmpd / "evidence").mkdir()
orig_ev = ge.EVIDENCE
ge.EVIDENCE = tmpd / "evidence"
shutil.copy(c, tmpd / "evidence" / c.name)
w = bool([f for f in ge.check_evidence_zero_diag_werror() if f.severity == "warn"])
ge.EVIDENCE = orig_ev; shutil.rmtree(tmpd, ignore_errors=True)
line("E10a 零诊断字段位移", v,
     f"gate warn={w} → {'仍逃逸（卡 confirm）' if v == 'confirm' else '已拦'}")

# ── E10b：pragma 消音 + -Werror ────────────────────────────────────────
c = mk("e10b",
       f'  "{GPP}" -Wall -Wextra -Werror -c "{PROBE}/e10b.cpp" -o "{PROBE}/e10b.o"\n',
       '#pragma GCC diagnostic ignored "-Wunused-variable"\n'
       "int main(){ int unused_v = 1; return 0; }\n")
(PROBE / "e10b.out").write_text("k=1\n", encoding="utf-8")
v, _ = replay.replay_card(c, do_sanitizer=False)
tmpd = Path(tempfile.mkdtemp()); (tmpd / "evidence").mkdir()
ge.EVIDENCE = tmpd / "evidence"
shutil.copy(c, tmpd / "evidence" / c.name)
w = bool([f for f in ge.check_evidence_zero_diag_werror() if f.severity == "warn"])
ge.EVIDENCE = orig_ev; shutil.rmtree(tmpd, ignore_errors=True)
line("E10b pragma 消音", v,
     f"gate warn={w} → {'仍逃逸（卡 confirm）' if v == 'confirm' else '已拦'}")

# ── E05：cat 式证据（读仓库数据文件原样打印）────────────────────────────
(PROBE / "expected_data.txt").write_text("result=42\n", encoding="utf-8")
c = mk("e05",
       f'  "{GPP}" -std=c++17 "{PROBE}/e05.cpp" -o "{PROBE}/e05.exe"\n'
       f'  "{PROBE}/e05.exe"\n',
       '#include <cstdio>\n#include <fstream>\n#include <string>\n'
       'int main(){ std::ifstream f("_adv_v80/probes/expected_data.txt"); std::string l;\n'
       '  while (std::getline(f, l)) std::printf("%s\\n", l.c_str()); }\n')
(PROBE / "e05.out").write_text("result=42\n", encoding="utf-8")
v, _ = replay.replay_card(c, do_sanitizer=False)
hits = ge.check_fixture_no_echo_data([c])
line("E05 cat 式证据", v,
     f"exp-scan={bool(hits)} → {'仍逃逸（零输出，卡 confirm）' if v == 'confirm' else '已拦'}")

# ── P0-A 构建脚本边界：无直接编译行产出 artifact（应 fail-closed）───────
c = mk("bs", "", "int main(){return 0;}\n")
c.write_text(c.read_text(encoding="utf-8").replace(
    f'"{GPP}" -std=c++17 -S', f'python -c "print(1)"  # {GPP} -std=c++17 -S'),
    encoding="utf-8")
(PROBE / "bs.out").write_text("k=1\n", encoding="utf-8")
v, _ = replay.replay_card(c, do_sanitizer=False)
line("P0-A 构建脚本边界", v, "fail-closed=不静默放行（预期 infra/其它非 confirm）")

# ── ccache 面：g++ 是否被 ccache shim 包裹（影响重编译可信度）───────────
r = subprocess.run(["where", "g++"], capture_output=True, text=True,
                   shell=True)
first = (r.stdout or "").strip().split("\n")[0] if r.stdout else "?"
is_shim = "ccache" in first.lower()
print(f"[ccache 面] where g++ 首选 = {first!r} | ccache shim = {is_shim}")
print(f"[ccache 面] 防御 CCACHE_DISABLE=1 在 _recompile_invariant 内 = "
      f"{'CCACHE_DISABLE' in (ROOT / 'tools/atom_evidence_replay.py').read_text(encoding='utf-8')}")
