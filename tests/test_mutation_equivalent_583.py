"""583 任务 1（N5）回归锁：规范化等价变异体字段（**只加字段，判决零改**）。

规格 `_arch_v9/05_攻击生成系统化.md` §四：
    equivalent ⟺ P1 视角相同 ∧ P2 视角相同 ∧ 缩进信号相同 ∧ 正文逐字不变 ∧ op ∉ {M1,M7}

本文件锁四件事：
① 真形态判别力：M6 的"块式→flow（matrix）"⇒ **等价**；重复 id 键 / 缩进提升(id) / 全角键名 ⇒ **不等价**；
② 双解析器缺一不可（P1 相同而 P2 分叉的形态必须判**不**等价）；
③ 保守面：M1/M7 恒不判等价；正文被改恒不判等价；
④ 不改判决：等价记录必为 `escaped` 且 new_* 为空（自检可证伪）；小批 5 字段与 v5 逐条一致（路径归一后）。
"""
from __future__ import annotations

import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge  # noqa: E402
import mutation_fuzz as mf  # noqa: E402

# 一条带 matrix 块式的真卡（M6 的 flow 变异体在 v5 里是"逃逸"）
_CARD = ROOT / "evidence/mem/EV-MEM-032.md"
_ORIG = (
    "---\n"
    "id: EV-X\n"
    "matrix:\n"
    "  compiler: [GCC]\n"
    "---\n"
    "正文\n"
)
_SANDBOX_RE = re.compile(r"[A-Za-z]:\\.*?mutfuzz_[0-9a-z_]+\\")


def _norm(s: str) -> str:
    """归一化 finding 字符串里的**沙箱绝对路径**（578b 教训：不归一会 100% 假阳性）。

    注意**不要加 `^` 锚**：沙箱路径常出现在 `规则名:路径` 的冒号**之后**（v5 报告里就是这样）。
    """
    return _SANDBOX_RE.sub("", s or "")


def _variant(card: pathlib.Path, key_sub: str) -> str:
    text = card.read_text(encoding="utf-8")
    for point, vtext in mf.mut_m6(text):
        if key_sub in point:
            return vtext
    pytest.skip(f"该卡当前无 {key_sub!r} 形态的 M6 变体（卡面已变）")


# ── ① 真形态判别力 ───────────────────────────────────────────────────────────
def test_583_matrix_flow_is_equivalent_but_other_forms_are_not():
    """M6 在真卡上的四种形态：只有"块式→flow（matrix）"是等价变异体。"""
    text = _CARD.read_text(encoding="utf-8")
    got = {point: mf.equivalent_variant("M6", text, vt) for point, vt in mf.mut_m6(text)}
    assert got, "该卡应至少有一个 M6 变体"
    assert got.get("块式 → flow 写法（matrix）") is True, got
    # 三种"会改变判决可见面"的形态必须**不**被判等价（逐名断言，不用"其余全否"的强假设）
    for prefix in ("重复 id 键", "缩进提升", "全角键名"):
        hit = [pt for pt in got if pt.startswith(prefix)]
        assert hit, f"该卡应含 {prefix} 形态"
        assert all(got[pt] is False for pt in hit), {pt: got[pt] for pt in hit}


def test_583_block_to_flow_roundtrip_is_equivalent():
    """块式 ↔ flow 互转：两解析器视角都相同 ⇒ 等价（这是判据的**主要用途**）。"""
    flow = _ORIG.replace("matrix:\n  compiler: [GCC]\n", "matrix: {compiler: [GCC]}\n")
    assert mf.equivalent_variant("M6", _ORIG, flow) is True
    assert mf.equivalent_variant("M6", flow, _ORIG) is True


# ── ② 双解析器缺一不可 ───────────────────────────────────────────────────────
def test_583_duplicate_key_same_value_p1_same_p2_diverge_is_not_equivalent():
    """**规格 1.3-3 的正例**：重复键（同值）——P1（仓内子集解析器）两遍相同，
    但 P2（硬化 loader）因重复键**抛错** ⇒ 必须判**不**等价（否则等于给走私发放免检）。"""
    dup = _ORIG.replace("id: EV-X", "id: EV-X\nid: EV-X")
    assert mf._canon(replay.parse_frontmatter(_ORIG)) == mf._canon(replay.parse_frontmatter(dup))
    assert mf._p2_view(_ORIG) != mf._p2_view(dup)
    assert mf._p2_view(dup).startswith("<error:"), mf._p2_view(dup)
    assert mf.equivalent_variant("M6", _ORIG, dup) is False


def test_583_fullwidth_key_is_not_equivalent():
    """全角键名：两解析器**都**看不到 `id` ⇒ 判不等价（它是 EV-FM 系列的拦截面）。"""
    fw = _ORIG.replace("id: EV-X", "ｉｄ: EV-X")
    assert mf.equivalent_variant("M6", _ORIG, fw) is False


# ── ③ 保守面 ─────────────────────────────────────────────────────────────────
def test_583_replay_ops_never_equivalent():
    """M1/M7 的判决还读工件与命令 ⇒ 硬边界：恒不判等价（需 TCE，冻结项）。"""
    flow = _ORIG.replace("matrix:\n  compiler: [GCC]\n", "matrix: {compiler: [GCC]}\n")
    assert mf.equivalent_variant("M1", _ORIG, flow) is False
    assert mf.equivalent_variant("M7", _ORIG, flow) is False


def test_583_body_change_blocks_equivalence():
    """正文被改 ⇒ 有规则读正文 ⇒ 保守判不等价（防 M6 的 flow 正则命中正文行）。"""
    body = _ORIG.replace("正文", "正文改")
    assert mf.equivalent_variant("M6", _ORIG, body) is False


def test_583_same_text_and_broken_yaml_are_not_equivalent():
    """空操作 / 无 frontmatter / P1 抛错：一律不判等价（保守）。"""
    assert mf.equivalent_variant("M6", _ORIG, _ORIG) is False
    assert mf.equivalent_variant("M6", _ORIG, "id: EV-X\n") is False


# ── ④ 不改判决 + 自检可证伪 ───────────────────────────────────────────────────
def test_583_equivalent_records_are_escaped_with_no_new_findings():
    """跑一小批：所有 equivalent 记录必须是 escaped 且 new_* 为空（= classify 语意自洽）。"""
    cards = [_CARD, ROOT / "evidence/ub/EV-UB-002.md"]
    rep = mf._run_jobs(cards, ["M6"], len(cards), jobs=1)
    eq = [r for r in rep["results"] if r.get("equivalent")]
    assert eq, "EV-MEM-032/EV-UB-002 上应至少各出一条等价变异体"
    for r in eq:
        assert r["verdict"] == "escaped", r
        assert not r.get("new_block") and not r.get("new_warn"), r
    assert rep.get("equivalent") == len(eq), "计数必须与逐条标记一致"
    assert len(rep.get("equivalent_keys") or []) == len(eq)
    ok, bad = mf.selfcheck_equivalent(rep)
    assert ok and bad == [], bad


def test_583_equivalent_flag_does_not_change_blocked_set(monkeypatch):
    """586：equivalent 字段**只**把等价变体从 `escaped` 挪到 `equivalent_invalid`（不进可判分母），
    **不影响**任何变体的 blocked 判定。A/B 同输入：开/关 `equivalent_variant`，blocked 与 n_a 相等，
    `equivalent_invalid` 与 `escaped` 互补（开：escaped=0、equivalent_invalid=N；关：escaped=N、equivalent_invalid=0）。
    判决 5 字段逐条一致。"""
    cards = [_CARD, ROOT / "evidence/ub/EV-UB-002.md"]
    on = mf._run_jobs(cards, ["M6"], len(cards), jobs=1)
    monkeypatch.setattr(mf, "equivalent_variant", lambda *a, **k: False)
    off = mf._run_jobs(cards, ["M6"], len(cards), jobs=1)
    assert _order_of(on) == _order_of(off)
    assert mf._variant_index(on) == mf._variant_index(off), "开关 equivalent 不得改变任何判决字段"
    # blocked / n_a 不受 equivalent 影响（真实拦截集合不变）
    assert (on["blocked"], on["n_a"]) == (off["blocked"], off["n_a"])
    eqn = sum(1 for r in on["results"] if r["equivalent"])
    assert eqn > 0, "打开时应有等价变体（否则本 A/B 无意义）"
    assert on["equivalent_invalid"] == eqn and on["escaped"] == 0
    assert off["equivalent_invalid"] == 0 and off["escaped"] == eqn
    assert all(r["equivalent"] is False for r in off["results"])


def _order_of(rep: dict) -> list[tuple[str, str, str]]:
    return [(r["card"], r["op"], r["point"]) for r in rep["results"]]


def test_583_selfcheck_detects_false_positive():
    """**反例（可证伪）**：伪造一条"标了 equivalent 却有新 finding"的记录 ⇒ 自检必须报错。"""
    fake = {"results": [{"card": "c", "op": "M6", "point": "p", "equivalent": True,
                         "verdict": "blocked", "new_block": ["EV-MATRIX:c"], "new_warn": []}]}
    ok, bad = mf.selfcheck_equivalent(fake)
    assert not ok and bad and "EV-MATRIX" in bad[0], bad


def test_583_variant_index_carries_no_equivalent_field():
    """**只加不改（单元面）**：`_variant_index()` 的 5 字段里**不含** equivalent ⇒ 加字段不影响它。

    为什么不在单元测试里比 v5 子集：**子集跑的判决与全量跑不同源**——门禁有跨卡规则，且
    同一变体在不同"同批卡集合"下的 finding 差集本就可以不同（实测：EV-MEM-032 的"全角键名"
    在 2 卡子集里 strict、在 v5 全量里 warn_only）。⇒ "与 v5 逐条相等"这条验收必须在**全量**
    上做（见 `_worklog_583.md` 的收工对账），不在单元测试里用子集替代。
    """
    cards = [_CARD, ROOT / "evidence/ub/EV-UB-002.md"]
    rep = mf._run_jobs(cards, ["M6"], len(cards), jobs=1)
    for r in rep["results"]:
        assert isinstance(r.get("equivalent"), bool), r     # 每条记录都带字段
    idx = mf._variant_index(rep)
    assert idx, "索引不应为空"
    for key, val in idx.items():
        assert len(val) == 5, (key, val)                    # 仍是 5 字段，未被 equivalent 污染
    # 586：四分类总和 = 变体数（equivalent 不进 blocked/escaped，单列 equivalent_invalid）
    assert (rep["blocked"] + rep["escaped"] + rep["n_a"]
            + rep["equivalent_invalid"] == rep["variants"])
    # 等价记录必须是 escaped 且无新 finding（保守性：宁可漏标，不许错标）
    for r in rep["results"]:
        if r.get("equivalent"):
            assert r["verdict"] == "escaped" and not r.get("new_block") and not r.get("new_warn")


def test_583_p2_view_agrees_with_gate_real_entry(tmp_path, monkeypatch):
    """**漂移护栏**：拿 gate 的**真实入口** `check_frontmatter_hardening()` 交叉核对——
    "块式→flow"必须**零信号**（我与 gate 都说等价），"重复键"必须出 `[dup-key]`（都说分叉）。
    gate 若改硬化语义，本用例会红（不许静默漂移）。"""
    atoms, evidence = tmp_path / "atoms", tmp_path / "evidence"
    (atoms / "mem").mkdir(parents=True)
    (evidence / "mem").mkdir(parents=True)
    monkeypatch.setattr(ge, "ATOMS", atoms)
    monkeypatch.setattr(ge, "EVIDENCE", evidence)
    if hasattr(ge, "clear_meta_cache"):          # 清掉真卡的 meta 缓存（沙箱路径不同，避免误命中）
        ge.clear_meta_cache()

    def _p(name: str, body: str) -> pathlib.Path:
        p = evidence / "mem" / name
        p.write_text(body, encoding="utf-8")
        return p

    _p("EV-FLOW-001.md",
       _ORIG.replace("matrix:\n  compiler: [GCC]\n", "matrix: {compiler: [GCC]}\n"))
    _p("EV-DUP-001.md", _ORIG.replace("id: EV-X", "id: EV-X\nid: EV-X"))
    _p("EV-BLOCK-001.md", _ORIG)

    got: dict[str, list[str]] = {}
    for f in ge.check_frontmatter_hardening():
        got.setdefault(pathlib.PurePath(f.target).name, []).append(f.message)

    flow_msgs = " ".join(got.get("EV-FLOW-001.md", []))
    dup_msgs = " ".join(got.get("EV-DUP-001.md", []))
    blk_msgs = " ".join(got.get("EV-BLOCK-001.md", []))
    assert "dup-key" in dup_msgs, got
    assert "[parse-diverge]" not in flow_msgs and "dup-key" not in flow_msgs, got
    assert not blk_msgs, got                       # 正对照：块式原文零信号
    # 与我的 P2 视角判定一致：flow 形态两解析器同、dup 形态分叉
    assert mf._p2_view(_ORIG) == mf._p2_view(_ORIG.replace(
        "matrix:\n  compiler: [GCC]\n", "matrix: {compiler: [GCC]}\n"))
    assert mf._p2_view(_ORIG) != mf._p2_view(_ORIG.replace("id: EV-X", "id: EV-X\nid: EV-X"))
