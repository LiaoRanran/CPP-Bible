# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_master_gate_670c.py — 670c D1 主门禁的回归测试（>=10 断言）。

覆盖任务书点名的六件事：分层解析、overall 判定（PASS/FAIL 组合）、未登记 BLOCK 计数、
--check 只读语义、json 输出 schema、门禁名清单非空且与 669d 一致。
另外三条是「防假绿」的射程自检：镜像 fail-closed、L1 不阻断、D2 守卫真的并进了主门禁。

658 子进程用 monkeypatch 的假 runner（用例只验证编排/分层/汇总语义，不重跑重活）；
669d/D2/D3 走真实 in-process 复用（那正是被测对象）。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import gate_rules_669d as G  # noqa: E402
import guard_rerun_670c as Guard  # noqa: E402
import run_master_gate_670c as MG  # noqa: E402

REAL_658_SRC = (ROOT / "tools" / "run_658_gate.py").read_text(encoding="utf-8")
RESEARCH_FILES = ("PROTOCOL_v0.1.md", "00_problem.md", "01_research_questions.md",
                  "02_hypotheses.md", "03_system_boundary.md", "04_threat_model.md",
                  "05_evaluation_protocol.md", "06_datasets.md", "07_baselines.md",
                  "08_metrics.md", "09_ablations.md", "10_analysis_plan.md",
                  "11_reproducibility.md", "12_threats_to_validity.md",
                  "13_ai_use_and_authorship.md", "CHANGELOG.md")


# ─────────────────────────────────────────────────────────────────────────────
# helper
# ─────────────────────────────────────────────────────────────────────────────

def wt(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def wj(p: Path, obj) -> None:
    wt(p, json.dumps(obj, ensure_ascii=False) + "\n")


def mk_root(tmp: Path) -> Path:
    """最小仓库：658 源副本 + 658 测试 + research 骨架 + 受控目录样例 + 五个核心工具。"""
    wt(tmp / "tools" / "run_658_gate.py", REAL_658_SRC)
    wt(tmp / "tests" / "test_x658.py", "def test_x():\n    assert True\n")
    for f in RESEARCH_FILES:
        wt(tmp / "research" / f, "# 骨架\n")
    wt(tmp / "atoms" / "conc" / "ATOM-A.md", "---\nid: A\nstatus: draft\n---\n")
    wt(tmp / "evidence" / "conc" / "EV-A.md", "---\nid: E\n---\n")
    wt(tmp / "Examples" / "atoms" / "x.asm", "main:\n\tret\n")
    wt(tmp / "Book" / "part00" / "ch01.md", "# ch01\n")
    for name, spec in Guard.CORE_TOOLS.items():
        wt(tmp / spec["src"], f"def {name}_fn():\n    return 1\n")
        for rel in spec["products"]:
            wj(tmp / rel, {"v": 1})
    (tmp / "data").mkdir(parents=True, exist_ok=True)
    return tmp


def fake_runner(exit_map: dict | None = None):
    """替换 MG.run_stage：不真跑子进程。"""
    def _run(argv, root, timeout=600):
        return (exit_map or {}).get(argv[0], 0), f"fake:{argv[0]}"
    return _run


def register_all_blocks(root: Path) -> int:
    """把当前全部 BLOCK 登记进 known_gaps（模拟 669d 的「只降级已登记项」机制）。"""
    blocks = [f for f in G.run_all(root) if f["severity"] == G.BLOCK]
    seen, gaps = set(), []
    for f in blocks:
        key = (f["rule"], f["target"])
        if key in seen:
            continue
        seen.add(key)
        gaps.append({"rule": f["rule"], "target": f["target"], "message": f["message"],
                     "reason": "用例登记（真实原因）", "owner": "test"})
    wj(root / "data" / "669d_known_gaps.json", {"schema": "queyi-known-gaps/v1", "gaps": gaps})
    return len(gaps)


# ─────────────────────────────────────────────────────────────────────────────
# ① 658 镜像：复用 + fail-closed
# ─────────────────────────────────────────────────────────────────────────────

def test_mirror_658_matches_real_repo():
    m = MG.mirror_658(ROOT)
    assert m["ok"] is True, f"镜像与 run_658_gate.py 不一致：{m['problems']}"
    assert m["extracted"] == len(MG.STAGES_658) == 6
    assert m["has_research"] is True


def test_mirror_658_fail_closed_on_unparsable(tmp_path):
    wt(tmp_path / "tools" / "run_658_gate.py", "def f():\n    return 1\n")
    m = MG.mirror_658(tmp_path)
    assert m["ok"] is False, "解析不出 stage() 必须判红（fail-closed），不得静默少跑"
    assert m["extracted"] == 0 and m["problems"]


def test_mirror_658_detects_added_stage(tmp_path):
    wt(tmp_path / "tools" / "run_658_gate.py",
       REAL_658_SRC + '    stage("S9 新增阶段", "L0", [PY, "tools/x658_new.py"])\n')
    m = MG.mirror_658(tmp_path)
    assert m["ok"] is False and any("条数" in p for p in m["problems"]), \
        "658 源多了一条阶段而镜像不自知 ⇒ 必须报出来"


# ─────────────────────────────────────────────────────────────────────────────
# ② 门禁名清单：非空且与 669d 注册表一致；分层取值正确
# ─────────────────────────────────────────────────────────────────────────────

def test_gate_names_match_669d_registry():
    gates, findings = MG.gates_669d(ROOT)
    ids = [g["id"] for g in gates]
    rule_ids = [str(r["id"]) for r in G.RULES669D]
    assert len(rule_ids) == 6, "669d 应为六条规则"
    assert all(f"669d/{rid}" in ids for rid in rule_ids), "主门禁必须逐条列出 669d 六条门禁"
    tiers = {g["id"]: g["tier"] for g in gates}
    assert tiers["669d/G-RATE-CONSISTENCY"] == "L0" and tiers["669d/G-IRR"] == "L1", \
        "分层必须与 669d 注册表一致（G-IRR 只 WARN）"
    assert isinstance(findings["unregistered_blocks"], list)


# ─────────────────────────────────────────────────────────────────────────────
# ③ overall 判定：PASS / FAIL 组合 + 未登记 BLOCK 计数
# ─────────────────────────────────────────────────────────────────────────────

def test_overall_pass_when_l0_all_pass(tmp_path, monkeypatch):
    root = mk_root(tmp_path)
    n = register_all_blocks(root)
    monkeypatch.setattr(MG, "run_stage", fake_runner())
    st = MG.collect(root)
    assert n >= 1 and st["registered_gaps"] == n
    assert st["unregistered_blocks"] == 0
    assert st["overall"] == "PASS" and st["fail_l0"] == []
    assert st["l0_pass"] == st["l0_total"] >= 8


def test_unregistered_block_fails_overall(tmp_path, monkeypatch):
    root = mk_root(tmp_path)                      # 刻意不登记 known_gaps
    monkeypatch.setattr(MG, "run_stage", fake_runner())
    st = MG.collect(root)
    assert st["unregistered_blocks"] >= 1, "未登记 BLOCK 必须被数出来"
    assert st["overall"] == "FAIL"
    assert any(g.startswith("669d/") for g in st["fail_l0"])
    assert st["findings"]["unregistered_blocks"], "未登记 BLOCK 明细必须随状态输出"


def test_registered_gaps_downgrade_blocks(tmp_path, monkeypatch):
    root = mk_root(tmp_path)
    register_all_blocks(root)
    monkeypatch.setattr(MG, "run_stage", fake_runner())
    st = MG.collect(root)
    assert st["unregistered_blocks"] == 0 and st["overall"] == "PASS"
    assert len(st["findings"]["registered_gaps"]) >= 1, "已登记缺口要显形，不得静默"


def test_l0_failure_fails_overall(tmp_path, monkeypatch):
    root = mk_root(tmp_path)
    register_all_blocks(root)
    monkeypatch.setattr(MG, "run_stage",
                        fake_runner({"tools/status_reconciler_658.py": 1}))
    st = MG.collect(root)
    assert "658/S0" in st["fail_l0"]
    assert st["overall"] == "FAIL"
    assert st["l0_pass"] == st["l0_total"] - 1


def test_l1_failure_does_not_block(tmp_path, monkeypatch):
    root = mk_root(tmp_path)
    register_all_blocks(root)
    (root / "research" / "CHANGELOG.md").unlink()      # S5 是 L1，缺一件即失败
    monkeypatch.setattr(MG, "run_stage", fake_runner())
    st = MG.collect(root)
    assert "658/S5" in st["fail_l1"], "缺 research 骨架应让 L1 失败"
    assert st["l1_pass"] < st["l1_total"]
    assert st["overall"] == "PASS", "L1 只出报告，绝不阻断"


# ─────────────────────────────────────────────────────────────────────────────
# ④ --check 只读语义 + 受控目录零写
# ─────────────────────────────────────────────────────────────────────────────

def test_check_mode_is_read_only(tmp_path, monkeypatch, capsys):
    root = mk_root(tmp_path)
    register_all_blocks(root)
    monkeypatch.setattr(MG, "run_stage", fake_runner())
    before = MG.snapshot_controlled(root)
    capsys.readouterr()
    rc = MG.main(["--root", str(root), "--check", "--json"])
    st = json.loads(capsys.readouterr().out)
    after = MG.snapshot_controlled(root)
    assert rc == 0 and st["overall"] == "PASS"
    assert st["controlled_dirs"]["checked"] is True
    assert st["controlled_dirs"]["write_detected"] == 0
    assert MG.diff_controlled(before, after) == {"added": [], "removed": [], "modified": []}, \
        "--check 不得写受控目录"
    assert not (root / "data" / "guard_rerun_baseline_670c.json").is_file(), \
        "主门禁不得偷偷标定基线（那是 D2 --update 的事）"
    assert not (root / "data" / "drift_report_670c.json").is_file(), \
        "主门禁不得写 D3 的报告（drift_watch 自己写）"


def test_check_mode_detects_controlled_write(tmp_path, monkeypatch):
    root = mk_root(tmp_path)
    register_all_blocks(root)

    def evil(argv, root_, timeout=600):
        (root_ / "atoms" / "conc" / "EVIL.md").write_text("x", encoding="utf-8")
        return 0, "evil"

    monkeypatch.setattr(MG, "run_stage", evil)
    st = MG.collect(root, check_mode=True)
    assert st["controlled_dirs"]["write_detected"] == 1
    assert "670c/controlled-dirs" in st["fail_l0"]
    assert st["overall"] == "FAIL", "受控目录被写必须判红（红线）"


# ─────────────────────────────────────────────────────────────────────────────
# ⑤ json schema + D2 集成 + 自检
# ─────────────────────────────────────────────────────────────────────────────

def test_json_output_schema(tmp_path, monkeypatch, capsys):
    root = mk_root(tmp_path)
    register_all_blocks(root)
    monkeypatch.setattr(MG, "run_stage", fake_runner())
    capsys.readouterr()
    MG.main(["--root", str(root), "--json"])
    st = json.loads(capsys.readouterr().out)
    for k in ("schema", "gate", "generated_at", "overall", "l0_pass", "l0_total",
              "l1_pass", "l1_total", "unregistered_blocks", "registered_gaps", "warns",
              "fail_l0", "fail_l1", "gates", "findings", "guard", "drift", "controlled_dirs"):
        assert k in st, f"json 缺字段 {k}"
    assert st["schema"] == MG.SCHEMA and st["gate"] == MG.GATE_ID
    assert all({"id", "tier", "pass"} <= set(g) for g in st["gates"])
    assert all(g["tier"] in ("L0", "L1") for g in st["gates"])


def test_d2_guard_is_integrated_into_master_gate(tmp_path, monkeypatch):
    root = mk_root(tmp_path)
    register_all_blocks(root)
    monkeypatch.setattr(MG, "run_stage", fake_runner())
    bp = root / "data" / "guard_rerun_baseline_670c.json"
    assert Guard.main(["--root", str(root), "--baseline", str(bp), "--update"]) == 0
    src = root / Guard.CORE_TOOLS["gate_engine"]["src"]
    wt(src, "def gate_engine_fn():\n    return 42\n")      # 改代码，不重跑产物
    st = MG.collect(root)
    assert st["guard"]["overall"] == "RED"
    assert "670c/D2-guard" in st["fail_l0"], "D2 的结论必须并进主门禁的 L0"
    assert st["overall"] == "FAIL"


def test_guard_unarmed_is_l1_not_l0(tmp_path, monkeypatch):
    root = mk_root(tmp_path)                       # 没有基线
    register_all_blocks(root)
    monkeypatch.setattr(MG, "run_stage", fake_runner())
    st = MG.collect(root)
    assert st["guard"]["baseline_found"] is False
    assert "670c/D2-guard" not in st["fail_l0"], "无基线是「未进射程」，不是「改了没重跑」"
    assert "670c/D2-guard-armed" in st["fail_l1"]


def test_selftest_passes(capsys):
    assert MG.selftest() == 0
    out = capsys.readouterr().out
    assert "658 镜像一致" in out
