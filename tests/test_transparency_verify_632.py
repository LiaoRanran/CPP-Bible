"""632 B2 · transparency_verify_632 单测（≥5 例，全只读/纯标准库）。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import transparency_verify_632 as tv  # noqa: E402


def _chain():
    return [
        {"log_index": 0, "prev_log_hash": "GENESIS", "entry_hash": "a" * 64},
        {"log_index": 1, "prev_log_hash": "a" * 64, "entry_hash": "b" * 64},
        {"log_index": 2, "prev_log_hash": "b" * 64, "entry_hash": "c" * 64},
    ]


def test_load_entries(tmp_path):
    p = tmp_path / "log.jsonl"
    p.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in _chain()) + "\n",
                 encoding="utf-8")
    assert len(tv.load_entries(p)) == 3


def test_verify_chain_ok():
    assert tv.verify_chain(_chain()) == []


def test_verify_chain_detects_broken_prev_hash():
    bad = _chain()
    bad[2]["prev_log_hash"] = "x" * 64
    errs = tv.verify_chain(bad)
    assert any("prev_log_hash" in e for e in errs)


def test_verify_chain_detects_gap_in_index():
    bad = _chain()
    bad[2]["log_index"] = 5
    errs = tv.verify_chain(bad)
    assert any("log_index" in e for e in errs)


def test_verify_chain_detects_bad_genesis():
    bad = _chain()
    bad[0]["prev_log_hash"] = "not-genesis"
    errs = tv.verify_chain(bad)
    assert any("GENESIS" in e for e in errs)


def test_verify_detects_nonhex_entry_hash():
    bad = _chain()
    bad[1]["entry_hash"] = "zzz"
    errs = tv.verify_chain(bad)
    assert any("entry_hash" in e for e in errs)


def test_main_check_exit_codes(tmp_path):
    log = tmp_path / "log.jsonl"
    log.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in _chain()) + "\n",
                   encoding="utf-8")
    vsa = tmp_path / "vsa"
    vsa.mkdir()
    # 先写锚（B1 逻辑），再校验应全绿
    sys.path.insert(0, str(ROOT / "tools"))
    import transparency_anchor_632 as ta
    ta.write_anchor(log, vsa)
    assert tv.main(["--check", "--log", str(log), "--vsa-dir", str(vsa)]) == 0
    # 篡改日志 → 链/锚不一致
    log.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in _chain()[:-1]) + "\n",
                   encoding="utf-8")
    assert tv.main(["--check", "--log", str(log), "--vsa-dir", str(vsa)]) == 1
