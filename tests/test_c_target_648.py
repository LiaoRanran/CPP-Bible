"""648 A · C 语言打靶回归锁（编号 A-1..A-8）。

分两档：
* **快档**（默认）：自检 + 工件存在性 + sha256 对账 + `.out` 键与卡声明一致 + 新卡零 block；
* **慢档**（`-m slow`）：**真的重编重跑** 10 个夹具（gcc/clang × c11/c17/c23 × -O0/-O2），
  并锁住几个"反直觉读数"（如 `i_after=2`、gcc/clang 在 UB 上答案相反）。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys

import c_target_648 as T
import pytest
import yaml

GATE = os.path.join(T.HERE, "gate_engine.py")


def _frontmatter(path: str) -> dict:
    txt = open(path, encoding="utf-8").read()
    got = yaml.safe_load(txt.split("---")[1])
    assert isinstance(got, dict), path
    return got


def _card_paths() -> list[str]:
    out = []
    for fx in T.FIXTURES:
        out.append(os.path.join(T.ROOT, "evidence", fx["dir"], f"EV-{fx['domain']}-{T.EV_NO[fx['key']]:03d}.md"))
        out.append(os.path.join(T.ROOT, "atoms", fx["dir"], f"ATOM-{fx['domain']}-{fx['topic']}-001.md"))
    return out


# ------------------------------- 快档 -------------------------------
def test_a1_selftest_and_generator_yaml_selfcheck_pass():
    assert T.selftest() == 0


def test_a2_generated_cards_yaml_parses_and_ids_unique():
    ids = []
    for fx in T.FIXTURES:
        p = os.path.join(T.ROOT, "atoms", fx["dir"], f"ATOM-{fx['domain']}-{fx['topic']}-001.md")
        d = _frontmatter(p)
        assert d["id"] == f"ATOM-{fx['domain']}-{fx['topic']}-001"
        assert d["domain"] == fx["domain"]
        ids.append(d["id"])
    assert len(set(ids)) == 10
    assert T.verify_yaml([os.path.relpath(p, T.ROOT).replace("\\", "/") for p in _card_paths()]) == []


def test_a3_artifacts_exist_and_sha256_matches_card():
    """卡的 `artifact_sha256` 必须与磁盘上工件逐字节一致（防止卡/工件漂移）。"""
    for fx in T.FIXTURES:
        ev = os.path.join(T.ROOT, "evidence", fx["dir"],
                          f"EV-{fx['domain']}-{T.EV_NO[fx['key']]:03d}.md")
        d = _frontmatter(ev)
        art = os.path.join(T.ROOT, d["artifact"])
        assert os.path.isfile(art), d["artifact"]
        got = hashlib.sha256(open(art, "rb").read()).hexdigest()
        assert got == d["artifact_sha256"], f"{d['id']} sha 漂移"


def test_a4_out_keys_match_declared_run_match_keys():
    """`.out` 里出现的每个键都必须在卡里声明（EV-OUT-UNDECLARED-KEY 的反向锁）。"""
    for fx in T.FIXTURES:
        ev = os.path.join(T.ROOT, "evidence", fx["dir"],
                          f"EV-{fx['domain']}-{T.EV_NO[fx['key']]:03d}.md")
        d = _frontmatter(ev)
        outp = os.path.join(T.ROOT, d["run_match_file"])
        assert os.path.isfile(outp)
        keys = re.findall(r"^([A-Za-z0-9_]+)=", open(outp, encoding="utf-8").read(), re.MULTILINE)
        assert keys, outp
        assert set(keys) == set(d["run_match_keys"]), (d["id"], keys, d["run_match_keys"])
        # 夹具源码必须存在，且断言符号真实出现在源码里
        src = open(os.path.join(T.ROOT, d["fixture"]), encoding="utf-8").read()
        for a in d["artifact_assert"]:
            assert a["text"] in src, (d["id"], a["text"])


def test_a5_atom_cards_declare_draft_and_are_honest_about_signing():
    """不代签：新卡必须是 draft，且正文写明"唯人签"。"""
    for fx in T.FIXTURES:
        p = os.path.join(T.ROOT, "atoms", fx["dir"], f"ATOM-{fx['domain']}-{fx['topic']}-001.md")
        d = _frontmatter(p)
        assert d["status"] == "draft", d["id"]
        assert d["status_history"][-1]["level"] == "draft"
        assert d["evidence"], d["id"]
        assert d["first_hand"] is True
        body = open(p, encoding="utf-8").read()
        assert "唯人签" in body and "反例" in body, d["id"]
        assert not re.search(r"TODO|TBD|FIXME|placeholder|占位", body)


def test_a6_new_cards_have_zero_block_in_gate():
    """只针对本批 20 张卡：`gate_engine --check` 不得给出 block（warn 允许，已登记）。"""
    out = os.path.join(T.ROOT, "build", "gate648_test.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    r = subprocess.run([sys.executable, GATE, "--check", "--json", out],
                       cwd=T.ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=600)
    data = json.load(open(out, encoding="utf-8"))
    findings = data["findings"] if isinstance(data, dict) else data
    mine = [f for f in findings
            if re.search(r"(ATOM-(LANG|MEM|UB)-(DECAY|FNPTR|VOLATILE|SETJMP|INTPROMO|"
                         r"BITFIELD|MACRO|MALLOC|STRBOUND|SIGNEDOVF))|"
                         r"(EV-(LANG-00[3-9]|MEM-04[67]|UB-003))", str(f.get("file", "")))]
    blocks = [f for f in mine if f["severity"] == "block"]
    assert blocks == [], blocks
    assert r.returncode == 0 or not blocks


def test_a7_gray_zone_declared_for_ub_card():
    """UB 域的卡必须带 gray_zone（ATOM-GRAY-ZONE 的正向锁）。"""
    p = os.path.join(T.ROOT, "atoms", "ub", "ATOM-UB-SIGNEDOVF-001.md")
    d = _frontmatter(p)
    assert d["domain"] == "UB" and d["gray_zone"] == "ub"


# ------------------------------- 慢档 -------------------------------
@pytest.mark.slow
def test_a8_real_recompile_all_combinations_green():
    """真重编重跑 10 夹具（120 组），失败组合必须为 0，并锁住反直觉读数。"""
    res = T.probe()
    assert res["n_failed"] == 0, res["failed"]
    fx = res["fixtures"]
    assert fx["decay"]["out"]["kv"]["decay_len_wrong_inside"] == "2"
    assert fx["decay"]["out"]["kv"]["decay_len_true"] == "10"
    assert fx["macro"]["out"]["kv"]["i_after"] == "2", "宏双求值必须被实测到"
    assert fx["signedovf"]["runs"]["gcc"]["c11"]["-O2"]["kv"]["signed_plus1_gt"] == "1"
    assert fx["signedovf"]["runs"]["clang"]["c11"]["-O2"]["kv"]["signed_plus1_gt"] == "0"
    assert fx["setjmp"]["runs"]["gcc"]["c11"]["-O0"]["kv"]["after_longjmp_plain"] == "5"
    assert fx["setjmp"]["runs"]["gcc"]["c11"]["-O2"]["kv"]["after_longjmp_plain"] == "0"
    assert fx["volatile"]["asm_refs"]["vol_flag"] > fx["volatile"]["asm_refs"]["plain_flag"]
