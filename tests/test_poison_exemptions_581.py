"""581 hole B 回归锁：豁免二人锁 + legacy 单列 + reason 背书机器核验。

背景（_worklog_581.md 任务 2）：
- 存量豁免（date<=2026-09-18）全标 `redteam_seen: legacy`，单列、不计入"诚实覆盖率"；
- 新豁免（date>2026-09-18）缺 `redteam_seen` ⇒ fail-closed，规则回到 uncovered（不静默放行）；
- reason 里声称的 pytest 背书由 `verify_exemption_reason` 机器核验（backed/missing-test/weak-test），
  unverifiable 单列点名、不删；
- 同时给出"表观覆盖率"（含 legacy 虚高）与"诚实覆盖率"（legacy 不计入），防只报好看的那个。

测试（fast 走纯函数/台账解析，slow 走一次钻探做端到端 fail-closed 验证）：
- 反例 1：新豁免无 redteam_seen → 规则仍在 uncovered（fail-closed）。
- 反例 2：reason 点名不存在的测试 → 归 unverifiable 被点名。
- 正例：带合法 redteam_seen → 移出 uncovered。
- 锁：存量 27 全落 legacy、不静默删除；apparent/honest 双口径可算出。
"""
from __future__ import annotations

import gate_engine as ge
import poison_drill as pd

REAL_EXEMPTIONS = pd.EXEMPTIONS


def _write_tmp_exempt(tmp_path, body: str) -> None:
    (tmp_path / "poison_exemptions.yaml").write_text(
        "schema: cppbible-poison-exemptions/1.0\n"
        "updated: 2026-09-18\n\n"
        "exemptions:\n" + body,
        encoding="utf-8",
    )


# ---------- 纯函数：reason 背书机器核验 ----------

def test_verify_exemption_reason_backed():
    # 取一个真实 back 桶豁免的 reason 文本直接核验（不跑钻探）
    ex = pd.load_exemptions()
    backed = [i for i, d in ex.items() if d["reason_verified"] == "backed"]
    assert backed, "应存在机器核验为 backed 的存量豁免"
    rid = backed[0]
    assert pd.verify_exemption_reason(rid, ex[rid]["reason"]) == "backed"


def test_verify_exemption_reason_missing_test():
    # reason 点名不存在的测试 ⇒ missing-test
    assert pd.verify_exemption_reason(
        "ATOM-ANY", "pytest 任务X 已补证据，见 test_does_not_exist_581_xyz") == "missing-test"


def test_verify_exemption_reason_weak_test():
    # 测试函数存在但该文件未断言该 rule_id ⇒ weak-test
    # （用真实存在的测试函数名 test_build_surface_map_matches_measured_stats，
    #  传入不可能出现在该文件源码里的 rule_id）
    assert pd.verify_exemption_reason(
        "EV-NOSUCHRULE-FOR-TEST-581",
        "见 test_build_surface_map_matches_measured_stats") == "weak-test"


# ---------- 台账解析：fail-closed 与 legacy 归类 ----------

def test_load_exemptions_legacy_stock_all_legacy(tmp_path):
    ex = pd.load_exemptions()
    # 625 A3：624 B1 新增 4 条非 legacy 豁免（-HC 规则）⇒ 只核「存量 legacy 部分」= 27
    stock = {k: v for k, v in ex.items() if v["redteam_seen"] == "legacy"}
    assert len(stock) == 27, f"存量 legacy 豁免须 27 条，实际 {len(stock)}"
    assert all(d["redteam_seen"] == "legacy" for d in stock.values()), \
        "存量豁免必须全部标 legacy，严禁替异族签字"


def test_load_exemptions_fail_closed_new_unsigned(tmp_path):
    # 新豁免（晚于合入日）无 redteam_seen ⇒ 无效、不进豁免台账（fail-closed）
    _write_tmp_exempt(tmp_path,
        '  - {id: ATOM-FAKE-A, reason: "pytest 任务X 已补", date: 2026-09-19}\n')
    pd.EXEMPTIONS = tmp_path / "poison_exemptions.yaml"
    try:
        ex = pd.load_exemptions()
        assert "ATOM-FAKE-A" not in ex, "无签名新豁免须被 fail-closed 拒绝"
    finally:
        pd.EXEMPTIONS = REAL_EXEMPTIONS


def test_load_exemptions_signed_new_accepted(tmp_path):
    # 新豁免带合法 redteam_seen ⇒ 进入豁免台账（正例对照）
    _write_tmp_exempt(tmp_path,
        '  - {id: ATOM-FAKE-A, reason: "pytest 任务X 已补", date: 2026-09-19, '
        'redteam_seen: arch_v7/2026-09-17}\n')
    pd.EXEMPTIONS = tmp_path / "poison_exemptions.yaml"
    try:
        ex = pd.load_exemptions()
        assert "ATOM-FAKE-A" in ex and ex["ATOM-FAKE-A"]["redteam_seen"] == "arch_v7/2026-09-17"
    finally:
        pd.EXEMPTIONS = REAL_EXEMPTIONS


def test_reason_missing_test_is_unverifiable_pointed(tmp_path):
    # 反例 2：reason 点名不存在的测试 ⇒ 该豁免在台账中被标 unverifiable（点名不删）
    _write_tmp_exempt(tmp_path,
        '  - {id: ATOM-FAKE-B, reason: "pytest 任务X 已补，见 test_does_not_exist_581_xyz", '
        'date: 2026-09-12, redteam_seen: legacy}\n')
    pd.EXEMPTIONS = tmp_path / "poison_exemptions.yaml"
    try:
        ex = pd.load_exemptions()
        assert ex["ATOM-FAKE-B"]["reason_verified"] == "missing-test"
    finally:
        pd.EXEMPTIONS = REAL_EXEMPTIONS


# ---------- 双口径覆盖率可算出 ----------

def test_coverage_report_two_rates_computable():
    rep = pd.coverage_report()
    assert rep["total"] == 67   # 625 A3：624 B1 后规则数 63→67
    # 587 任务3：新增 P77/P78/P79（matrix 非法值）毒载荷 ⇒ EV-MATRIX 由"仅豁免"升为
    # **行为级覆盖**，行为覆盖 38 → 39（非回归，是新增毒样例带来的真实增量）。
    assert rep["behavioral_covered"] == 39
    assert rep["apparent_rule_coverage"] >= rep["honest_rule_coverage"], \
        "表观口径（含 legacy）应 ≥ 诚实口径（legacy 不计入）"
    assert rep["legacy_exempt"] and len(rep["legacy_exempt"]) == 27
    # 586 任务3 后：20 条"背书不可核验"债已清偿（12 missing + 8 weak 全部补到真测试/降级声明）⇒
    # missing/weak 归零（unverifiable=0）；其中人审象限（无 check 函数）3 条机器原理上无从触发，
    # 归 machine-untriggerable 单列、**不计入**诚实分子（防"声明当背书"虚高），其余 24 条 backed。
    ex = pd.load_exemptions()
    buckets = [d["reason_verified"] for d in ex.values()]
    # 625 A3：624 B1 新增 4 条 -HC 豁免（reason 引用 test_hc_rules_are_block_and_automated，核验 backed）
    # ⇒ backed 24 → 28；missing/weak 仍为 0。
    assert buckets.count("backed") == 28
    assert buckets.count("machine-untriggerable") == 3
    assert buckets.count("missing-test") == 0
    assert buckets.count("weak-test") == 0
    assert rep["machine_untriggerable"] == sorted(
        i for i, d in ex.items() if d["reason_verified"] == "machine-untriggerable")
    # 诚实分子 = 行为覆盖 ∪ 背书豁免（不含 machine-untriggerable）
    assert rep["honest_covered"] == len(set(rep["backed_exempt"]) | pd.behavioral_covered())


# ---------- 586 任务3：无 check 的人审象限规则不得伪称"pytest 背书" ----------

def test_verify_exemption_reason_machine_untriggerable():
    # 反例 3：规则在 gate_engine.RULES 里没有 check 函数（人审象限）⇒ 即便 reason 点名了
    # 真实存在的测试并断言了该 rule_id，也只归 machine-untriggerable，不算 backed。
    no_check = [r.id for r in ge.RULES if getattr(r, "check", None) is None]
    assert no_check, "应存在无 check 函数的人审象限规则"
    rid = no_check[0]
    # 用一条真实存在的、源码里确实出现该 rule_id 的测试名（正例对照用的 test 名称取自本仓）
    reason = "pytest test_human_quadrant_rules_not_machine_triggered 已确认"
    assert pd.verify_exemption_reason(rid, reason) == "machine-untriggerable", \
        "无 check 的规则不得被算作 pytest 背书（那会把人审声明伪装成机械覆盖）"


# ---------- 端到端：fail-closed 反映在 uncovered（走一次钻探） ----------

def test_unsigned_new_exemption_stays_uncovered_end_to_end(tmp_path):
    pd.behavioral_covered()  # 确保覆盖率已采集（同进程内只跑一次钻探）
    ex = pd.load_exemptions()
    only_exempt = [i for i in ex if i not in pd.behavioral_covered()]
    assert only_exempt, "需存在仅豁免未覆盖的规则，以验证 fail-closed 端到端"
    rid = only_exempt[0]

    # 反例 1：同规则改挂"新豁免且无 redteam_seen" ⇒ 须被 fail-closed，回到 uncovered
    _write_tmp_exempt(tmp_path,
        f'  - {{id: {rid}, reason: "pytest 任务X 已补", date: 2026-09-19}}\n')
    pd.EXEMPTIONS = tmp_path / "poison_exemptions.yaml"
    try:
        assert rid in pd.rule_coverage()[2], \
            "无签名新豁免须 fail-closed，规则回到 uncovered"
        # 正例：补合法 redteam_seen ⇒ 移出 uncovered
        _write_tmp_exempt(tmp_path,
            f'  - {{id: {rid}, reason: "pytest 任务X 已补", date: 2026-09-19, '
            f'redteam_seen: arch_v7/2026-09-17}}\n')
        assert rid not in pd.rule_coverage()[2], \
            "带合法 redteam_seen 的新豁免须移出 uncovered"
    finally:
        pd.EXEMPTIONS = REAL_EXEMPTIONS
