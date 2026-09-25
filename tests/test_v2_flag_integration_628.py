"""628 A1 · V2 flag 真接入 单测（8 例）。"""
import importlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import authority_projection_compiler_626 as C
import v2_flag_integration_verify_628 as V

ENV = C.ENV_FLAG
GROUNDED = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        "data", "grounded_labels_w2.json")


def _set(val):
    os.environ[ENV] = val


def _unset():
    os.environ.pop(ENV, None)


def _compiler():
    importlib.reload(C)
    return C.AuthorityProjectionCompiler()


def _expect_w2_or_dynamic() -> dict:
    """640b A1：期望 W2 取单一权威源（不写死 114/7）。"""
    from w2_authority_640b import current as _w2
    return _w2()


def setup_function(fn):
    _unset()


def teardown_function(fn):
    _unset()


def test_flag_unset_defaults_v1():
    _unset()
    c = _compiler()
    assert c.v2_mode is False


def test_flag_0_is_v1():
    _set("0")
    c = _compiler()
    assert c.v2_mode is False


def test_flag_1_is_v2():
    _set("1")
    c = _compiler()
    assert c.v2_mode is True


def test_v1_uses_legacy_grounded_labels():
    _set("0")
    w2 = _compiler().compile_w2()
    g = json.load(open(GROUNDED, encoding="utf-8"))
    expected = {k: v["label"] for k, v in g["nodes"].items()}
    assert w2 == expected
    assert len(w2) == 121


def test_v2_uses_normalized_121_nodes():
    _set("1")
    w2 = _compiler().compile_w2()
    assert len(w2) == 121          # 归一化后 121，非 ledger edge 粒度 519


def test_v1_v2_numbers_identical():
    _set("0")
    w1 = _compiler().compile_w2()
    _set("1")
    w2 = _compiler().compile_w2()
    assert w1 == w2
    _exp = _expect_w2_or_dynamic()
    assert list(_compiler().w2_summary().items()) == [("IN", _exp["IN"]),
                                                      ("OUT", _exp["OUT"]),
                                                      ("UNDEC", _exp["UNDEC"])]


def test_schema_identical_both_modes():
    _set("0")
    s1 = _compiler().w2_summary()
    _set("1")
    s2 = _compiler().w2_summary()
    assert list(s1.keys()) == list(s2.keys()) == ["IN", "OUT", "UNDEC"]


def test_core_tools_do_not_read_flag():
    here = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tools")
    for ct in V.CORE_TOOLS:
        txt = open(os.path.join(here, ct), encoding="utf-8", errors="ignore").read()
        assert ENV not in txt, f"{ct} 不应读取 flag"
