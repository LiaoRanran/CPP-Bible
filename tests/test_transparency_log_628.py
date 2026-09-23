"""628 B3 · 透明日志 单测（9 例）。

幂等性说明：**追加类用例一律把日志指向临时文件**（`T.LOG_ENV` 覆盖），
因此单测不会在生产日志里留下条目（旧实现每跑一次就多一条重复记录）。
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import transparency_log_628 as T


def _creds() -> list:
    return [os.path.join(T.VSA_DIR, f) for f in sorted(os.listdir(T.VSA_DIR))
            if f.startswith("attestation_") and f.endswith(".json")]


def _temp_log(tmp_path, monkeypatch) -> str:
    p = tmp_path / "log.jsonl"
    monkeypatch.setenv(T.LOG_ENV, str(p))
    return str(p)


def _recompute_chain(path: str) -> bool:
    entries = [json.loads(line) for line in open(path, encoding="utf-8")
               if line.strip()]
    prev = "GENESIS"
    for e in entries:
        if e.get("prev_log_hash") != prev or T._entry_hash(e) != e.get("entry_hash"):
            return False
        prev = e["entry_hash"]
    return True


def test_log_chain_valid():
    v = T.verify_log()
    assert v["chain_valid"] and v["entries"] >= 1


def test_append_increases_entries(tmp_path, monkeypatch):
    _temp_log(tmp_path, monkeypatch)
    creds = _creds()
    assert len(creds) >= 2
    r0 = T.append_vsa(creds[-1])
    r1 = T.append_vsa(creds[0])
    assert r0["ok"] and r1["ok"]
    assert (r0["log_index"], r1["log_index"]) == (0, 1)
    assert T.verify_log()["entries"] == 2
    assert _recompute_chain(T._log_path())


def test_append_idempotent(tmp_path, monkeypatch):
    _temp_log(tmp_path, monkeypatch)
    cred = _creds()[-1]
    first = T.append_vsa(cred)
    second = T.append_vsa(cred)
    assert first["ok"] and second["ok"] and second["already_present"]
    assert T.verify_log()["entries"] == 1, "同一凭证重复追加必须是 no-op"
    assert second["log_index"] == first["log_index"]


def test_tamper_history_detected(tmp_path):
    log = T._read_log()
    if len(log) < 2:
        log.append(dict(log[0], log_index=len(log)))
    tampered = [dict(e) for e in log]
    tampered[0]["timestamp"] = "2000-01-01T00:00:00Z"
    p = tmp_path / "tampered.jsonl"
    p.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in tampered) + "\n",
                 encoding="utf-8")
    assert not _recompute_chain(str(p)), "篡改历史条目必须使链验证失败"


def test_deletion_detected(tmp_path):
    log = T._read_log()
    if len(log) < 3:
        return  # 样本不足时跳过（构建期已保证 ≥3）
    trimmed = [log[0], log[2]]              # 删掉 index 1
    p = tmp_path / "deleted.jsonl"
    p.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in trimmed) + "\n",
                 encoding="utf-8")
    entries = [json.loads(line) for line in open(p, encoding="utf-8")
               if line.strip()]
    assert entries[1]["prev_log_hash"] != entries[0]["entry_hash"]
    assert not _recompute_chain(str(p)), "删除历史条目必须被检测"


def test_inclusion_check(tmp_path, monkeypatch):
    _temp_log(tmp_path, monkeypatch)
    cred = _creds()[-1]
    assert not T.check_inclusion(cred)["included"]
    T.append_vsa(cred)
    r = T.check_inclusion(cred)
    assert r["included"] and r["log_index"] == 0


def test_append_only_no_rewrite(tmp_path, monkeypatch):
    p = _temp_log(tmp_path, monkeypatch)
    T.append_vsa(_creds()[-1])
    before = open(p, "rb").read()
    T.append_vsa(_creds()[0])
    after = open(p, "rb").read()
    assert after.startswith(before), "既有条目必须逐字节保留（append-only）"


def test_entry_hash_excludes_itself():
    e = T._read_log()[0]
    h = dict(e)
    h.pop("entry_hash")
    import hashlib
    blob = json.dumps(h, ensure_ascii=False, sort_keys=True).encode("utf-8")
    assert hashlib.sha256(blob).hexdigest() == e["entry_hash"]


def test_status_consistent_on_production_log():
    st = T.status()
    assert st["chain_valid"] and st["files"]["ok"]
    assert st["unlogged"] == [], f"存在未入册凭证：{st['unlogged']}"
    assert st["tail_included"], "日志尾部凭证必须可验证存在"
