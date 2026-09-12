"""S4/S5/S6 机器判定回归（S1/S2/S3 规则由 test_gate_engine.py 覆盖）。

覆盖（红绿成对，正例触发 + 反例不触发）：
  S4 黄金锁：无漂移放行 · block 上升红 · verified 下降红 · --accept 留痕后放行
  S5 债务台账：到期红 · 超 90 天红 · Agent 自批红 · 负债率超限红 · 干净台账绿
  S6 毒样例演练：3 毒样例全拦截 + 阴性放行（真编译）
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import debt_ledger as dl
import golden_lock as gl
import poison_drill as pd

METRICS = {"block_findings": 0, "warn_findings": 1, "atoms_total": 0,
           "evidence_total": 1, "verified_atoms": 0, "replay_confirm": 1}


# ── S6 毒样例 P4–P7 的判定规则（2026-09-11 第四批）──────────────────────────
# 与 poison_drill 的端到端演练互补：这里直接锁**规则函数**的判定边界
# （正例触发 + 反例不触发），使契约在无编译器的环境下也可测。
def _poison_arena(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """把 gate_engine 的 EVIDENCE 指向临时 arena，返回该目录。"""
    import gate_engine as ge
    ev = tmp_path / "evidence"
    (ev / "mem").mkdir(parents=True)
    monkeypatch.setattr(ge, "EVIDENCE", ev)
    return ev


def _poison_card(ev: Path, name: str, fields: dict) -> Path:
    import gate_engine as ge                                   # noqa: F401
    p = ev / "mem" / name
    body = ""
    for k, v in fields.items():
        s = str(v)
        body += f"{k}:{s}\n" if s.startswith("\n") else f"{k}: {s}\n"
    p.write_text("---\n" + body + "---\n", encoding="utf-8")
    return p


BASE = {"serves": "[ATOM-MEM-CLEAN-001]", "hypothesis": "h", "kind": "run",
        "verdict": "confirm", "actual": "{run_case: A}"}


def test_p4_self_satisfied_assert(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """P4：夹具自定义 operator delete[] + 断言只做存在性匹配 ⇒ 命中；注明调用点则豁免。"""
    import gate_engine as ge
    ev = _poison_arena(tmp_path, monkeypatch)
    fx = ev / "_fx.cpp"
    fx.write_text("void operator delete[](void* p) noexcept { (void)p; }\nint main(){}\n",
                  encoding="utf-8")
    _poison_card(ev, "EV-MEM-T1.md", dict(
        BASE, fixture=str(fx),
        artifact_assert='\n  - {kind: contains_any, texts: ["_ZdaPvy"]}'))
    who = {f.rule_id for f in ge.check_evidence_self_satisfied_assert()}
    assert "EV-SELF-SATISFIED-ASSERT" in who, "夹具自定义符号 + 存在性断言必须命中"
    # 反例：卡内已注明调用点口径 → 视为已处置，不报
    _poison_card(ev, "EV-MEM-T1.md", dict(
        BASE, fixture=str(fx),
        hypothesis="调用点真实存在（本工件 3 处）",
        artifact_assert='\n  - {kind: contains_any, texts: ["_ZdaPvy"]}'))
    assert not [f for f in ge.check_evidence_self_satisfied_assert()
                if f.path.endswith("EV-MEM-T1.md")], "已注明调用点口径的卡不该再报"


def test_p5_falsification_must_be_quantified(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """P5：falsification 无任何数字 ⇒ 命中；含量化取值 ⇒ 不报。"""
    import gate_engine as ge
    ev = _poison_arena(tmp_path, monkeypatch)
    _poison_card(ev, "EV-MEM-T2.md", dict(BASE, falsification="若结论不成立则输出会不同"))
    assert {f.rule_id for f in ge.check_evidence_falsification_quantified()} \
        == {"EV-FALSIFICATION-QUANT"}
    _poison_card(ev, "EV-MEM-T2.md", dict(BASE, falsification="对照读数应为 3，实测 0"))
    assert not ge.check_evidence_falsification_quantified(), "含量化对照值不该报"


def test_p6_trivial_observation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """P6：actual 里的存在性判断无判别力 ⇒ 命中；跨类型比对值（equal=1）不算。"""
    import gate_engine as ge
    ev = _poison_arena(tmp_path, monkeypatch)
    _poison_card(ev, "EV-MEM-T3.md", dict(BASE, actual="{run_case: observer != nullptr}"))
    assert {f.rule_id for f in ge.check_evidence_trivial_observation()} \
        == {"EV-TRIVIAL-OBSERVATION"}
    # 反例：'sizes equal=1' 是跨类型比对（对"是否擦除"有响应），不得误报
    _poison_card(ev, "EV-MEM-T3.md", dict(BASE, actual="{run_case: sizes equal=1}"))
    assert not ge.check_evidence_trivial_observation(), "跨类型比对不应误报"


def test_p7_matrix_needs_backing_note(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """P7：声明多编译器却无可核对留痕锚 ⇒ 命中。

    v2 收紧（2026-09-12）：旧口径只做关键词匹配，写一句"外部复跑留痕"即可自证通过；
    新口径要求**可核对锚**（.out 路径 / CI run 号 / ::notice:: / 完整编译器命令行 / 标准条文）。
    """
    import gate_engine as ge
    ev = _poison_arena(tmp_path, monkeypatch)
    matrix = "\n  compiler: [GCC 15.3.0, Clang 19.1.0]\n  std: [c++17]"
    _poison_card(ev, "EV-MEM-T4.md", dict(BASE, matrix=matrix))
    assert {f.rule_id for f in ge.check_evidence_matrix_backed()} == {"EV-MATRIX-UNBACKED"}
    # 关键词自证（旧口径会放行）：v2 必须仍命中，否则"写明留痕"又成逃生舱
    _poison_card(ev, "EV-MEM-T4.md", dict(
        BASE, hypothesis="Clang 列为外部复跑留痕（仓内无工件）", matrix=matrix))
    assert {f.rule_id for f in ge.check_evidence_matrix_backed()} == {"EV-MATRIX-UNBACKED"}, \
        "光写关键词不算留痕锚"
    # 给出可核对锚（CI run 号）⇒ 不报（门禁不得恒红）
    _poison_card(ev, "EV-MEM-T4.md", dict(
        BASE, hypothesis="Clang 列为外部复跑留痕（CI run 34595609458，仓内无工件）", matrix=matrix))
    assert not ge.check_evidence_matrix_backed(), "写明可核对锚后不该再报"


# ── S4 黄金锁 ──────────────────────────────────────────────────────────────
def _gold(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, measure: dict) -> None:
    monkeypatch.setattr(gl, "STATE", tmp_path / "golden_state.json")
    monkeypatch.setattr(gl, "measure", lambda: dict(measure))
    assert gl.cmd_sync() == 0


def test_golden_no_drift_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _gold(tmp_path, monkeypatch, METRICS)
    assert gl.cmd_check(None) == 0


def test_golden_block_increase_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _gold(tmp_path, monkeypatch, METRICS)
    monkeypatch.setattr(gl, "measure", lambda: dict(METRICS, block_findings=2))
    assert gl.cmd_check(None) == 1, "block 0→2 必须红"


def test_golden_verified_drop_fails(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    base = dict(METRICS, verified_atoms=1)
    _gold(tmp_path, monkeypatch, base)
    monkeypatch.setattr(gl, "measure", lambda: dict(METRICS))     # verified 1→0
    assert gl.cmd_check(None) == 1, "verified 数下降必须红"


def test_golden_accept_leaves_audit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _gold(tmp_path, monkeypatch, METRICS)
    monkeypatch.setattr(gl, "measure", lambda: dict(METRICS, warn_findings=3))
    rc = gl.cmd_check("口径变更：新增 2 条 warn 级规则")
    state = json.loads(gl.STATE.read_text(encoding="utf-8"))
    assert rc == 0 and len(state["accepted"]) == 1
    assert "口径变更" in state["accepted"][0]["reason"]


# ── S5 债务台账 ────────────────────────────────────────────────────────────
def _debt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, tickets: list[dict]) -> None:
    p = tmp_path / "debt_ledger.json"
    p.write_text(json.dumps({"schema": dl.SCHEMA, "tickets": tickets}, ensure_ascii=False),
                 encoding="utf-8")
    monkeypatch.setattr(dl, "LEDGER", p)


def _tk(**over: str) -> dict:
    t = {"id": "DEBT-001", "cause": "c", "risk": "r", "compensation": "cp",
         "owner": "human:liaoranran", "opened": "2026-09-10", "due": "2026-09-20"}
    t.update(over)
    return t


def test_clean_ledger_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _debt(tmp_path, monkeypatch, [_tk()])
    assert dl.cmd_check() == 0


def test_expired_ticket_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _debt(tmp_path, monkeypatch, [_tk(due="2026-08-01")])
    assert dl.cmd_check() == 1, "到期未清必须停线"


def test_over_90_days_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _debt(tmp_path, monkeypatch, [_tk(opened="2026-01-01", due="2026-06-01")])
    assert dl.cmd_check() == 1, "超 90 天 = 永久豁免，必须停线"


def test_agent_owner_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _debt(tmp_path, monkeypatch, [_tk(owner="agent:claude")])
    assert dl.cmd_check() == 1, "Agent 自批豁免必须停线"


def test_ratio_over_limit_blocks(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    many = [_tk(id=f"DEBT-{i:03d}") for i in range(1, 6)]       # 5/20 = 25% > 15%
    _debt(tmp_path, monkeypatch, many)
    assert dl.cmd_check() == 1, "负债率超限必须停线"


def test_add_rejects_agent_owner(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(dl, "LEDGER", tmp_path / "debt_ledger.json")
    argv = ["add", "--cause", "c", "--risk", "r", "--compensation", "cp",
            "--owner", "agent:x", "--days", "30"]
    assert dl.main(argv) == 2, "Agent 不得自批（S1 同源）"


# ── S6 毒样例演练（真编译，含阴性对照）────────────────────────────────────
@pytest.mark.skipif(not (Path("C:/Qt/Tools/mingw1530_64/bin/g++.exe").exists()
                         or __import__("shutil").which("g++")),
                    reason="本机无 g++")
def test_poison_drill_all_caught_and_negative_passes():
    assert pd.drill() == 0, "毒样例必须全部拦截且阴性对照放行（G3 验收门自证）"
