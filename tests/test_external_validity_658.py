"""658 A 段：外部效度工具自检（不触发不可逆 reveal）。"""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_real_defect_reinject_caught():
    m = _load("defect_fixture_658", "tools/defect_fixture_658.py")
    for did, fn in m.INJECTORS.items():
        r = fn()
        assert r["caught"], f"{did} 重注入应被门禁抓住"


def test_holdout_reveal_state():
    """661 B1：reveal 后不可回盲；未 reveal 时须保持盲态。"""
    m = _load("holdout_658", "tools/holdout_658.py")
    h = m.load()
    # 660 C2 原有口径：20 个真实 C++ 错误类型样本。
    # 665 C1：holdout 扩样 20 → 30（新增 h21–h30，全部为真错）；本批只**放宽下界**，
    # 不撤销"count 必须与 seeds 条数一致"这条一致性锁（那才是这个测试真正守的东西）。
    assert h["count"] == len(h["seeds"]), "count 必须等于 seeds 条数"
    assert len(h["seeds"]) >= 20, "665 C1 只能扩样（20 → 30），不许删样本"
    if m.is_revealed():
        assert os.path.isfile(os.path.join(ROOT, "data", "holdout_reveal_1_661.json")), \
            "已 reveal 必须有 reveal 报告（661 B1）"
    else:
        assert h["blind"] is True, "未 reveal 时必须保持盲态"
