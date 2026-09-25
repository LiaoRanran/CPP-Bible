"""625 F1 · 收工门禁回归测试（≥4 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import run_625_gate as G  # noqa: E402


def test_new_tools_registered():
    names = [n for n, _ in G.NEW_TOOLS]
    for must in ("loop_stability_metrics_625", "vfdr_convergence_625", "path_config_625",
                 "queyi_core_interface_design_625", "queyi_core_trigger_check_625",
                 "round7_mutator_625", "human_review_dashboard_625",
                 "human_review_executor_625", "pck_upgrade_strategy_625"):
        assert must in names
    assert len(names) == 9


def test_each_new_tool_has_check_flag():
    for _name, extra in G.NEW_TOOLS:
        assert "--check" in extra


def test_gate_logic_fails_when_a_step_fails(monkeypatch):
    """640c B1：门禁**逻辑**本身的回归（与仓库当前是否绿无关）。

    历史门禁容易变成"跨批脆弱"——它断言的是"当时仓库全绿"，仓库一演进就红。
    真正该锁的是机制：**任一步骤失败 ⇒ exit 1**（否则门禁恒绿 == 没有门禁）。
    """
    monkeypatch.setattr(G, "_run", lambda _args: (1, "boom"))
    assert G.check() == 1


def test_gate_logic_passes_when_all_steps_ok(monkeypatch):
    monkeypatch.setattr(G, "_run", lambda _args: (0, ""))
    assert G.check() == 0


def test_full_gate_passes():
    """真实仓库全绿（受控不变量；失败时按 `_run` 输出定位是真红还是基准未重钉）。"""
    assert G.check() == 0


def test_gate_runs_no_modification():
    before = os.path.getsize(os.path.join(ROOT, "data", "authority", "authority_log.jsonl"))
    G.check()
    after = os.path.getsize(os.path.join(ROOT, "data", "authority", "authority_log.jsonl"))
    assert before == after
