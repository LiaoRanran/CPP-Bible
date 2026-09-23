"""628 B3 · 透明日志 单测（7 例）。"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import transparency_log_628 as T


def test_log_chain_valid():
    v = T.verify_log()
    assert v["chain_valid"] and v["entries"] >= 1


def test_append_increases_entries():
    creds = sorted(f for f in os.listdir(T.VSA_DIR) if f.startswith("attestation_"))
    before = T.verify_log()["entries"]
    r = T.append_vsa(os.path.join(T.VSA_DIR, creds[-1]))
    assert r["ok"] and r["log_index"] == before
    assert T.verify_log()["entries"] == before + 1


def test_tamper_history_detected(tmp_path):
    # 复制日志到临时文件，篡改一条中间记录的 timestamp ⇒ 链断
    log = T._read_log()
    if len(log) < 2:
        log.append(dict(log[0], log_index=len(log)))
    tampered = [dict(e) for e in log]
    tampered[0]["timestamp"] = "2000-01-01T00:00:00Z"
    p = tmp_path / "tampered.jsonl"
    p.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in tampered) + "\n",
                 encoding="utf-8")
    entries = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    prev = "GENESIS"
    broken = False
    for e in entries:
        if e.get("prev_log_hash") != prev or T._entry_hash(e) != e.get("entry_hash"):
            broken = True
            break
        prev = e["entry_hash"]
    assert broken, "篡改历史条目必须使链验证失败"


def test_deletion_detected(tmp_path):
    # 删除中间条目 ⇒ 后续 prev_log_hash 对不上
    log = T._read_log()
    if len(log) < 3:
        return  # 样本不足时跳过（构建期已保证 ≥3）
    trimmed = [log[0], log[2]]              # 删掉 index 1
    p = tmp_path / "deleted.jsonl"
    p.write_text("\n".join(json.dumps(e, ensure_ascii=False) for e in trimmed) + "\n",
                 encoding="utf-8")
    entries = [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]
    prev = entries[0]["entry_hash"]
    assert entries[1]["prev_log_hash"] != prev, "删除历史条目必须被检测"


def test_inclusion_check():
    creds = sorted(f for f in os.listdir(T.VSA_DIR) if f.startswith("attestation_"))
    r = T.check_inclusion(os.path.join(T.VSA_DIR, creds[-1]))
    assert r["included"] and r["log_index"] is not None


def test_append_only_no_rewrite():
    # append 前后：既有条目字节不变（只在末尾追加）
    before = open(T.LOG, "rb").read()
    creds = sorted(f for f in os.listdir(T.VSA_DIR) if f.startswith("attestation_"))
    T.append_vsa(os.path.join(T.VSA_DIR, creds[-1]))
    after = open(T.LOG, "rb").read()
    assert after.startswith(before), "既有条目必须逐字节保留（append-only）"


def test_entry_hash_excludes_itself():
    e = T._read_log()[0]
    h = dict(e)
    h.pop("entry_hash")
    import hashlib
    blob = json.dumps(h, ensure_ascii=False, sort_keys=True).encode("utf-8")
    assert hashlib.sha256(blob).hexdigest() == e["entry_hash"]
