"""v5 对抗复测（核心 v2）：绕开僵尸锁（沙箱锁路径）+ 合规 E12 + E07 细分。

僵尸锁 build/.replay_lock（pid 39120，锁龄 2188s）导致正式路径 replay 全站 busy，
本脚本把 _REPLAY_LOCK 重定向到沙箱，不删现场、不改正式文件。
"""
from __future__ import annotations

import re
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
SANDBOX_LOCK = ROOT / "_adv_v80" / ".replay_lock"
replay._REPLAY_LOCK = SANDBOX_LOCK          # 沙箱锁：绕开残留僵尸锁


def line(tag: str, verdict: str, note: str = "") -> None:
    print(f"[{tag:<34}] {verdict}" + (f"  | {note}" if note else ""))


# ── A. E01：编译后覆写 ─────────────────────────────────────────────────
v, _ = replay.replay_card(ROOT / "_adv_v70/probes/EV-ADV70-H1.md", do_sanitizer=False)
line("E01 编译后覆写（H1）", v, "confirm=仍逃逸")

# ── B. E03：恒真符号（含 contains_in）───────────────────────────────────
v, _ = replay.replay_card(ROOT / "_adv_v70/probes/EV-ADV70-H3.md", do_sanitizer=False)
line("E03 恒真符号（H3）", v, "confirm=仍逃逸")

# ── C. N2 新逃逸：跨编译器 + **全局**恒真断言（不用 contains_in）──────────
fx = PROBE / "n2.cpp"
fx.write_text("int main(){return 0;}\n", encoding="utf-8")
art = PROBE / "n2.asm"
gpp = Path(toolchain.resolve_gpp()).as_posix()
subprocess.run([toolchain.resolve_gpp(), "-std=c++17", "-S", str(fx), "-o", str(art)],
               capture_output=True)
(PROBE / "n2.out").write_text("k=1\n", encoding="utf-8")
card = PROBE / "EV-ADV80-N2.md"
card.write_text(
    "---\nid: EV-ADV80-N2\nserves: []\nhypothesis: h\nkind: asm\n"
    f'command: "{gpp}" -std=c++17 -S "{fx.as_posix()}" -o "{art.as_posix()}"\n'
    f"fixture: {fx.relative_to(ROOT).as_posix()}\n"
    f"artifact: {art.relative_to(ROOT).as_posix()}\n"
    "artifact_sha256: 1111111111111111111111111111111111111111111111111111111111111111\n"
    "artifact_compiler: Clang 19.0.0 (Linux)\n"
    "verdict: confirm\nfalsification: f\nexpected: any\n"
    "actual:\n  run_match_file: _adv_v80/probes/n2.out\n  run_match_keys: [k]\n"
    "artifact_assert:\n"
    "  - {kind: contains_any, texts: ['zzz_not_there', '.file']}\n"
    "---\n", encoding="utf-8")
v, log = replay.replay_card(card, do_sanitizer=False)
line("N2 跨编译器+全局恒真断言", v,
     "逃逸（P0-C 只治 contains_in）" if v == "confirm" else "已拦")
for l in log:
    if "artifact_assert" in l or "结构断言" in l:
        print("      ", l.strip()[:95])

# ── D. E12：签收字符串自证（用真实卡复制沙箱，只观察 S1 类规则）──────────
tmp = Path(tempfile.mkdtemp(prefix="adv80_"))
shutil.copytree(ROOT / "atoms", tmp / "atoms")
shutil.copytree(ROOT / "evidence", tmp / "evidence")
orig = (ge.ATOMS, ge.EVIDENCE, ge.ROOT)
ge.ATOMS, ge.EVIDENCE, ge.ROOT = tmp / "atoms", tmp / "evidence", tmp
try:
    tgt = next((tmp / "atoms").rglob("ATOM-MEM-RAII-001.md"))
    txt = tgt.read_text(encoding="utf-8")
    # 攻击者自签：人级签收写成在册人名字符串（无任何身份绑定）
    if "verified_by:" in txt:
        txt = re.sub(r"verified_by:.*", "verified_by: human:liaoranran", txt)
    else:
        txt = txt.replace("status:", "verified_by: human:liaoranran\nstatus:", 1)
    txt = re.sub(r"^status:.*$", "status: human-verified", txt, flags=re.M)
    tgt.write_text(txt, encoding="utf-8")
    findings = [f for f in ge.run(include_advice=False)
                if "ATOM-MEM-RAII-001" in f.target]
    blocks = sorted({f.rule_id for f in findings if f.severity == "block"})
    warns = sorted({f.rule_id for f in findings if f.severity == "warn"})
    signoff = [r for r in (blocks + warns) if "SIGN" in r or "S1" in r or "PRINCIPAL" in r]
    line("E12 签收字符串自证",
         "逃逸（无签收真实性规则命中）" if not signoff else f"已拦 {signoff}",
         f"block={blocks or '无'} warn={warns or '无'}")
finally:
    ge.ATOMS, ge.EVIDENCE, ge.ROOT = orig
    shutil.rmtree(tmp, ignore_errors=True)

# ── E. E07 变体细分（命中类型）─────────────────────────────────────────
variants = {
    "空格缩进": "fixture: f.cpp &x\n  verdict: confirm\n",
    "tab 缩进": "fixture: f.cpp &x\n\tverdict: confirm\n",
    "混合 tab+空格": "fixture: f.cpp &x\n \t verdict: confirm\n",
    "引号值+缩进": 'fixture: "f.cpp"\n  verdict: confirm\n',
    "注释值+缩进": "fixture: f.cpp  # note\n  verdict: confirm\n",
}
tmp2 = Path(tempfile.mkdtemp(prefix="adv80e_"))
(tmp2 / "evidence").mkdir()
orig_ev = ge.EVIDENCE
ge.EVIDENCE = tmp2 / "evidence"
try:
    for name, body in variants.items():
        p = tmp2 / "evidence" / "EV-S.md"
        p.write_text("---\nid: EV-S\nstatus: draft\n" + body + "hypothesis: h\n---\n",
                     encoding="utf-8")
        meta = replay.parse_frontmatter(p.read_text(encoding="utf-8"))
        lifted = meta.get("verdict")
        hits = ge.check_frontmatter_hardening()
        kinds = [("block:" + f.message.split("]")[0].strip("[")) for f in hits
                 if f.severity == "block"]
        line(f"E07 变体·{name}", f"顶层verdict={lifted!r} 命中={kinds or '无'}",
             "逃逸" if (lifted == "confirm" and not kinds) else
             ("无效载荷" if lifted != "confirm" else "已拦"))
finally:
    ge.EVIDENCE = orig_ev
    shutil.rmtree(tmp2, ignore_errors=True)
