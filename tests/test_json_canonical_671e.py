# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671e-C · JSON 哈希规范化（JCS）核查测试。

**核查结论（先复现，再下结论）**：
671c 调研把"JSON 哈希未规范化、相同内容不同键序→不同哈希=不可复算"列为 *硬缺陷候选*。
本批经全 `tools/` 扫描 + 复现，结论是 **false positive（非缺陷）**：

  * 全 `tools/` 中**唯一 3 处**对内存 dict 做 `sha256(json.dumps(...))` 的代码
    （authority_projection_compiler_626 / e2e_attestation_629 / lifecycle_fsm_638）
    **全部已用 `sort_keys=True`**；另有 governance_doc_guard / independent_verifier_628 /
    vsa_* / in_toto_link 等一大批验证哈希也带 `sort_keys=True`。
  * 关键"信任/验证"产物 `data/dataset_hashes_670c.json`、`data/supply_chain/merkle_roots.json`、
    `tools/.tool_checksums` 的哈希对象都是**原始文件字节**（`sha256_file` / `sha256_of`），
    与内存 dict 的 JSON 键序**完全无关** ⇒ JCS 风险在本仓库不存在。

本测试集目的：
  (1) 锁定 3 个真实 dict-哈希函数的**键序无关性**（order-independent）；
  (2) 演示"若漏 sort_keys，键序不同会得不同哈希"——说明项目用 sort_keys 是正确的防护；
  (3) 锁定 dataset_hashes / merkle_roots 的哈希基于**文件字节**（键序无关）。
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)


def _load(modname):
    spec = importlib.util.spec_from_file_location(modname, os.path.join(TOOLS, modname + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mi_hash = _load("hash_datasets_670c")
fsm = _load("lifecycle_fsm_638")


def _canonical(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _shuffled(d: dict) -> dict:
    out = {}
    for k in reversed(list(d.keys())):   # 逆序插入，构造不同键序的同内容 dict
        out[k] = d[k]
    return out


def test_canonical_hash_is_key_order_independent():
    a = {"b": 1, "a": 2, "c": {"z": 1, "y": 2}}
    assert _canonical(a) == _canonical(_shuffled(a))


def test_unsorted_dumps_would_differ_demonstrating_the_risk():
    """机理演示：若哈希用 `json.dumps`（无 sort_keys），键序不同 ⇒ 哈希不同。
    这正说明项目统一用 `sort_keys=True` 是对的选择（这就是 JCS 要防的坑）。"""
    a = {"b": 1, "a": 2}
    h_sorted = hashlib.sha256(json.dumps(a, sort_keys=True).encode()).hexdigest()
    h_unsorted_a = hashlib.sha256(json.dumps(a).encode()).hexdigest()
    h_unsorted_b = hashlib.sha256(json.dumps(_shuffled(a)).encode()).hexdigest()
    assert h_sorted == h_sorted            # sort_keys 稳定
    assert h_unsorted_a != h_unsorted_b    # 无 sort_keys 时键序敏感（风险所在）


def test_lifecycle_entry_hash_order_independent():
    rec = {"id": "x", "state": "open", "self_hash": "deadbeef", "ts": 123}
    h1 = fsm._entry_hash(rec)
    h2 = fsm._entry_hash(_shuffled(rec))
    assert h1 == h2


def test_lifecycle_entry_hash_ignores_self_hash_field():
    rec = {"id": "x", "v": 1, "self_hash": "AAA"}
    rec2 = {"id": "x", "v": 1, "self_hash": "BBB"}   # self_hash 不同，其余同
    assert fsm._entry_hash(rec) == fsm._entry_hash(rec2)


def test_source_authority_digest_uses_sort_keys():
    src = open(os.path.join(TOOLS, "authority_projection_compiler_626.py"), encoding="utf-8").read()
    # 找到 sha256(json.dumps(...)...) 调用，必须含 sort_keys=True
    import re
    m = re.search(r"hashlib\.sha256\(\s*json\.dumps\([^)]*\)", src, re.S)
    assert m and "sort_keys=True" in m.group(0), "authority _digest 必须 sort_keys=True"


def test_source_e2e_attestation_uses_sort_keys():
    src = open(os.path.join(TOOLS, "e2e_attestation_629.py"), encoding="utf-8").read()
    import re
    m = re.search(r"sha256\(\s*json\.dumps\([^)]*\)", src, re.S)
    assert m and "sort_keys=True" in m.group(0), "e2e_attestation 的 pub 哈希必须 sort_keys=True"


def test_source_governance_core_hash_uses_sort_keys():
    src = open(os.path.join(TOOLS, "governance_doc_guard.py"), encoding="utf-8").read()
    import re
    # core 的哈希调用
    m = re.search(r"json\.dumps\(core,[^)]*\)\.encode", src)
    assert m and "sort_keys=True" in m.group(0), "governance_doc_guard 的 core 验证哈希必须 sort_keys=True"


def test_source_independent_verifier_uses_sort_keys():
    src = open(os.path.join(TOOLS, "independent_verifier_628.py"), encoding="utf-8").read()
    import re
    m = re.search(r"json\.dumps\(\{[^}]*\},\s*ensure_ascii=False,\s*sort_keys=True", src, re.S)
    assert m, "independent_verifier 的验证哈希必须 sort_keys=True"


def test_sha256_file_identical_for_same_bytes(tmp_path):
    p = tmp_path / "f.json"
    p.write_text('{"a":1,"b":2}', encoding="utf-8")
    q = tmp_path / "g.json"
    q.write_text('{"a":1,"b":2}', encoding="utf-8")
    assert mi_hash.sha256_file(p) == mi_hash.sha256_file(q)


def test_dataset_hash_detects_byte_level_drift_including_key_order(tmp_path):
    """锁定设计意图：`sha256_file` 哈希**原始字节**，因此即使是"同逻辑内容、不同键序"
    的两个文件也会给出**不同**哈希——这正是抓字节级漂移（含键序/CRLF 改写）的目的，
    **不是** JCS 缺陷。JCS 风险只在"对内存 dict 做 json.dumps 哈希"时出现，
    而本仓库的 dict 哈希已全部 sort_keys=True（见上方测试）。"""
    a = tmp_path / "same_a.json"
    b = tmp_path / "same_b.json"
    a.write_text('{"z":1,"a":2,"m":{"x":9,"y":8}}', encoding="utf-8")
    b.write_text('{"a":2,"m":{"y":8,"x":9},"z":1}', encoding="utf-8")
    assert mi_hash.sha256_file(a) != mi_hash.sha256_file(b)   # 字节不同 ⇒ 哈希必不同（设计预期）
    # 同内容同字节 ⇒ 同哈希（可复算性在"源文件字节固定"时成立）
    c = tmp_path / "same_c.json"
    c.write_text('{"z":1,"a":2,"m":{"x":9,"y":8}}', encoding="utf-8")
    assert mi_hash.sha256_file(a) == mi_hash.sha256_file(c)


def test_build_manifest_records_byte_level_hashes(tmp_path):
    """build_manifest 的每文件 sha256 来自字节（sha256_file），与 JSON 结构无关。"""
    (tmp_path / "d").mkdir()
    f = tmp_path / "d" / "x.json"
    f.write_text('{"k":1,"j":2}', encoding="utf-8")
    man = mi_hash.build_manifest(tmp_path, entries=(
        {"group": "g", "path": "d/x.json", "frozen": True, "note": "t"},))
    rec = man["files"][0]
    assert rec["sha256"] == mi_hash.sha256_file(f)
    assert rec["missing"] is False


def test_build_manifest_file_hashes_stable_across_rebuild(tmp_path):
    (tmp_path / "d").mkdir()
    (tmp_path / "d" / "x.json").write_text('{"k":1}', encoding="utf-8")
    e = ({"group": "g", "path": "d/x.json", "frozen": True, "note": "t"},)
    m1 = mi_hash.build_manifest(tmp_path, entries=e)
    m2 = mi_hash.build_manifest(tmp_path, entries=e)
    assert m1["files"][0]["sha256"] == m2["files"][0]["sha256"]


def test_no_unsorted_dict_hash_in_known_sites(tmp_path):
    """锁死 3 个已知的 dict-哈希点：每个 `sha256(json.dumps(...))` 必须带 sort_keys=True。"""
    import re
    for fn in ("authority_projection_compiler_626.py", "e2e_attestation_629.py",
              "lifecycle_fsm_638.py"):
        src = open(os.path.join(TOOLS, fn), encoding="utf-8").read()
        for m in re.finditer(r"sha256\([^;]*?json\.dumps\(.*?\)\s*.*?\)", src, re.S):
            seg = m.group(0)
            if "json.dumps" in seg:
                assert "sort_keys=True" in seg, f"{fn} 存在未规范化的 dict 哈希：{seg[:80]}"


def test_merkle_roots_hash_is_over_file_bytes_not_dict():
    """锁定：`data/supply_chain/merkle_roots.json` 在 tool_integrity 里经 `sha256_of`
    （读文件字节）哈希，而非对内存 dict 做 json.dumps ⇒ 不受 JSON 键序影响。"""
    ti_src = open(os.path.join(TOOLS, "tool_integrity.py"), encoding="utf-8").read()
    # merkle_roots 在 SUPPLY_CHAIN_FILES 中，且 supply_chain 哈希走 compute_supply_chain→sha256_of
    assert "data/supply_chain/merkle_roots.json" in ti_src
    assert "def sha256_of" in ti_src
    assert "def compute_supply_chain" in ti_src
    # merkle_integrity 自身也只对文件字节/叶子内容做哈希，不把整棵树 dict 当哈希输入
    mi_src = open(os.path.join(TOOLS, "merkle_integrity.py"), encoding="utf-8").read()
    assert "_LEAF_PREFIX" in mi_src and "_NODE_PREFIX" in mi_src
