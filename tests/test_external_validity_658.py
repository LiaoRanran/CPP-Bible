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


def test_holdout_blind_by_default():
    m = _load("holdout_658", "tools/holdout_658.py")
    assert m.is_revealed() is False, "测试不得触发 reveal（不可逆）"
    h = m.load()
    assert h["blind"] is True
    assert h["count"] == len(h["seeds"]) == 5
