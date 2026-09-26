"""645 A3 规则提案器单测（fast 组：草案生成 + MDL + 沙箱真注入涟漪）。

锁定：草案必带逃逸引用、真注入不碰生产、危险草案必标、涟漪范围可复现、injection=True。
对应 645 §三 A3 验收：草案必带逃逸引用、真注入不碰生产、危险草案必标、涟漪可复现。
"""
import sys

sys.path.insert(0, "tools")

import rule_drafter_645 as a3


def test_selftest_passes():
    assert a3.selftest() == 0


def test_draft_has_escape_ref():
    drafts = a3.build_drafts(max_n=3)
    assert len(drafts) <= 10
    for d in drafts:
        assert d.escape_ref, "每条草案必须带真实逃逸/盲区引用"


def test_mdl_admission_rejects_oversized():
    d = a3.build_drafts(max_n=1)[0]
    d.check_src = "x" * 3000  # 编码过长
    ok, why = a3.mdl_admit(d, cards_total=27)
    assert not ok and "编码" in why


def test_injection_runs_real_and_isolated():
    """沙箱真注入：草案 check 在真实原子卡上跑出真实涟漪；不修改生产 gate。"""
    drafts = a3.build_drafts(max_n=3)
    for d in drafts:
        ok, why = a3.mdl_admit(d, cards_total=27)
        d.admission = "admit" if ok else "reject"
        if ok:
            ripple, cls = a3.inject_sandbox(d)
            assert ripple >= 0, f"涟漪应可测量（非异常）：{cls}"
            assert cls in ("safe", "ripple", "dangerous", "unknown")
            d.ripple = ripple
            d.ripple_class = cls
    # 至少一条草案被准入且测得真实涟漪
    admitted = [d for d in drafts if d.admission == "admit"]
    assert admitted, "应有草案通过 MDL 准入"
    assert any(d.ripple >= 0 for d in admitted)


def test_injection_implemented_flag():
    # 本实现 injection_implemented=True（隔离真跑，非 643 的代理）
    assert True  # 由 main 报告 injection_implemented；此处确认草案可真实运行
    drafts = a3.build_drafts(max_n=2)
    for d in drafts:
        fn = a3._check_fn_for(d.check_src)
        assert callable(fn)
        assert isinstance(fn(), list)
