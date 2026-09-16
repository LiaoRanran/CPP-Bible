#!/usr/bin/env python3
"""547 B 面探针：V-iso 阴阳同构（545 未饱和）。

纯函数 / schema 层为主，不编译、不改正式文件。每项一行 `[PASS|FAIL|ESCAPE|INFO]`。
ESCAPE = 发现该假设描述的洞；PASS = 工具行为诚实；INFO = 需真实编译，超便宜范围。
"""
from __future__ import annotations

import re
import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import atom_evidence_replay as replay   # noqa: E402
import viso_diff as viso                 # noqa: E402
import gate_engine as ge                 # noqa: E402

NC1 = "Examples/atoms/_atom_fence_vs_atomic.nc1.cpp"


# ── B2：阳面断言恒真 ⇒ 阴面翻转不被当 negative_control_passed ──────────────────
def t_b2_const_yang_rejected() -> str:
    # 恒真 text（如 .file）在阳/阴都出现 ⇒ 不是翻转 ⇒ 系统应判"该卡无判别力"
    ok, wrong = replay._nc_flip_ok("becomes_present", 5, 5)
    if ok or wrong:
        return f"FAIL (恒真 text 被当翻转 ok={ok} wrong={wrong})"
    # 真翻转：becomes_absent 语义 = 阳有(yang>0)、阴无(yin==0) ⇒ 应判翻转
    ok2, _ = replay._nc_flip_ok("becomes_absent", 3, 0)
    return "PASS" if ok2 else "FAIL (真翻转未被识别)"


# ── B3：阴面 fixture 不锚定到本卡（可借别卡/别优化级产物冒充） ─────────────────
def t_b3_yin_not_bound_to_card() -> str:
    # 选一个真实存在、且不是阳夹具自身的"借来"fixture
    cands = [p for p in (ROOT / "Examples" / "atoms").rglob("*.cpp")]
    borrowed = next((str(p.relative_to(ROOT)).replace("\\", "/")
                     for p in cands if str(p).replace("\\", "/") != NC1
                     and p.name.endswith(".cpp")), None)
    if not borrowed:
        return "INFO (找不到可借的 .cpp)"
    nc = {"id": "nc9", "variant": "v1", "mutation": "delete_mechanism",
          "fixture": borrowed, "anchor": "spin_plain", "remove": "while",
          "retain": ["while"],
          "probe": {"channel": "artifact", "symbol": "_Z10spin_plainv",
                    "op": "becomes_absent", "text": "s_p_b"}}
    verdict = viso.validate_nc_schema(
        nc, fixture_exists=lambda p: (ROOT / p).is_file(),
        anchor_def_count=1, declared_run_keys=set(), yang_fixture=NC1)
    errs = list(verdict.errors)
    if errs:
        # 547 B3 修复后：借品阴面被升 block 拒收 ⇒ 洞已闭
        return "PASS (借品阴面被 schema 升 block 拒收：" + "; ".join(errs) + ")"
    warns = list(verdict.warnings)
    # 若仍只命名告警、未升 block ⇒ 洞未闭
    return ("ESCAPE" if warns else "PASS") + \
        f" (借来 fixture={borrowed}；若仅命名告警={warns} 则洞未闭)"


# ── B4：阴面编译失败归类（纯函数） ───────────────────────────────────────────
def t_b4_compile_failure_classified() -> str:
    # 注：本纯函数只管 infra vs content（compiler_missing / compile_timeout /
    # compile_error / confirm）；unsupported_shell 由 _split_argv（另路径）产出，不在此。
    cases = [
        (("g++ -c x.cpp", 127, "", "g++"), "infra_error:compiler_missing"),
        (("g++ -c x.cpp", 1, "err", "g++"), "refute:compile_error"),
        (("g++ -c x.cpp", 124, "", "g++"), "infra_error:compile_timeout"),
        (("g++ -c x.cpp", 0, "", "g++"), "confirm"),
    ]
    bad = [(c, exp) for c, exp in cases
           if replay.classify_command_failure([c]) != exp]
    return "PASS" if not bad else f"FAIL {bad}"


# ── B5：negative_controls 用 flow 写法，自定义 frontmatter 解析器收不收 ────────
def t_b5_flow_style_nc_parsed() -> str:
    # flow 式 negative_controls 写进临时卡，跑门禁硬化层（547 B5 修复点）。
    # 注：自定义 parse_frontmatter 仍收下 flow 式（replay 路径另要求 block），
    # 本探针专测"硬化层是否拦 flow 式 nc"——修复后须 [nc-flow] block。
    tmp = Path(tempfile.mkdtemp(prefix="b5_"))
    orig_ev = ge.EVIDENCE
    ge.EVIDENCE = tmp
    try:
        (tmp / "mem").mkdir(exist_ok=True)
        (tmp / "mem" / "EV-X.md").write_text(
            "---\nid: EV-X\nnegative_controls: [{id: nc1, variant: delete, "
            "mutation: fence, fixture: a.cpp, anchor: f, remove: 'x', "
            "retain: [y], probe: {channel: artifact, symbol: s, "
            "op: becomes_absent, text: t}}]\n---\n",
            encoding="utf-8")
        hits = ge.check_frontmatter_hardening()
    finally:
        ge.EVIDENCE = orig_ev
        shutil.rmtree(tmp, ignore_errors=True)
    blocks = [f for f in hits if f.severity == "block" and "nc-flow" in f.message]
    if blocks:
        return "PASS (flow 式 nc 被硬化层 [nc-flow] block 拦下)"
    return "ESCAPE (flow 式 negative_controls 未被硬化层拦下：仍可沉默通过)"


# ── B6：nc1 诚实性（换 -O2 / 换符号名翻转是否仍只对 fence 敏感） ───────────────
def t_b6_nc1_honesty() -> str:
    # 需真实编译（g++ 多优化级），超本探针的便宜范围；列为 INCONCLUSIVE 待真跑
    return ("INFO (需真实编译 ATOM-CONC-001 在 -O0/-O2/-Os 三侧比对读数，"
            "超纯函数探针范围；留待真跑，不在此伪造结论)")


DEFS = [t_b2_const_yang_rejected, t_b3_yin_not_bound_to_card,
        t_b4_compile_failure_classified, t_b5_flow_style_nc_parsed, t_b6_nc1_honesty]


def main() -> int:
    print("=== B 面：V-iso 阴阳同构 ===")
    esc = 0
    for f in DEFS:
        try:
            res = f()
        except Exception as e:  # noqa: BLE001
            res = f"FAIL (抛异常 {type(e).__name__}: {e})"
        tag = res.split(" ")[0]
        if tag == "ESCAPE":
            esc += 1
        print(f"[{tag}] {f.__name__}: {res}")
    print(f"B 面：{esc} 个 ESCAPE" + ("（重点）" if esc else ""))
    return 1 if esc else 0


if __name__ == "__main__":
    raise SystemExit(main())
