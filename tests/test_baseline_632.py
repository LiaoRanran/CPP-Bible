"""632 任务0 · 基线台账单测（≥5 例，全只读、纯标准库）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import baseline_632 as B  # noqa: E402


def test_baseline_has_required_keys():
    for k in ("gate 规则数", "CI pytest", "自身免疫率", "coverage", "雷1 触发标准"):
        assert k in B.BASELINE, k


def test_ci_remaining_items_extracts_five(tmp_path):
    md = tmp_path / "ci.md"
    md.write_text(
        "# t\n- `test_a.py::test_x`\n- `test_b.py::test_y`\n"
        "- `test_a.py::test_x`\n- `test_c.py::test_z`\n- `test_d.py::test_w`\n"
        "- `test_e.py::test_v`\n", encoding="utf-8")
    items = B.ci_remaining_items(md)
    assert len(items) == 5, items  # 去重后 5


def test_ci_remaining_items_missing_file_returns_empty():
    assert B.ci_remaining_items(Path("/nope/not_here.md")) == []


def test_proxy_up_closed_port_is_false():
    # 端口 1 几乎必然关闭 ⇒ 返回 False（验证函数逻辑与返回类型）
    assert B.proxy_up(port=1) is False


def test_proxy_up_returns_bool():
    assert isinstance(B.proxy_up(port=1), bool)


def test_vsa_secret_key_detection(tmp_path):
    d = tmp_path / "vsa"
    d.mkdir()
    assert B.vsa_secret_key_exists(d) is False
    (d / "vsa_secret.key").write_text("x", encoding="utf-8")
    assert B.vsa_secret_key_exists(d) is True


def test_write_baseline_md(tmp_path):
    out = tmp_path / "632_baseline.md"
    B.write_baseline_md(out)
    txt = out.read_text(encoding="utf-8")
    assert "§一 Standing Baseline" in txt
    assert "代理 7990 端口" in txt
    assert str(B.PROXY_PORT) in txt
