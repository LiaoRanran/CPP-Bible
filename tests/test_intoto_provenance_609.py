"""609 D2 · in-toto 溯源回归锁（link/layout schema + 4 关键步骤 + **缺签名即 fail-closed**）。

锁五件事（任务书 5 例）：
  1. `gen_link` 产出字段齐全且 `signatures == []`（**未签名件**，不是证据）；
  2. `check_link` / `check_layout` 字段级 schema：缺字段即报错（不补全、不猜）；
  3. ① 命令一致性：把 link 的 command 改成别的 ⇒ **fail**（封 A1 伪造 link）；
  4. ③ 签名覆盖：未签名 ⇒ **fail-closed**（不许因为"没签就先放过"）；
  5. ④ 顺序/quorum：跳过某一步 ⇒ fail（封 A3 跳步骤）；
  +. ② material→product：产物被偷换/缺 ⇒ fail（封 A2）。
"""
from __future__ import annotations

import json
from pathlib import Path

import intoto_provenance as iip

LAYOUT = iip.gen_layout()
STEP0 = LAYOUT["steps"][0]


def _link(name: str, **kw) -> dict:
    return iip.gen_link(name, materials=kw.get("materials", []),
                        products=kw.get("products", []),
                        command=kw.get("command", STEP0["expected_command"]),
                        return_value=kw.get("return_value", 0))


def _all_links() -> list[dict]:
    return [iip.gen_link(s["name"], materials=s["expected_materials"],
                         products=s["expected_products"],
                         command=s["expected_command"]) for s in LAYOUT["steps"]]


def test_gen_link_schema_and_unsigned():
    link = _link("generate", materials=["data/attack_edges_candidates.jsonl"])
    assert iip.check_link(link) == []
    assert link["_type"] == "link" and link["signatures"] == []
    assert {"stdout", "stderr", "return-value"} <= set(link["byproducts"])
    # 已存在的 material 必须记 sha256；不存在的必须标 missing（**不许伪造哈希**）
    assert "sha256" in link["materials"]["data/attack_edges_candidates.jsonl"]
    missing = _link("x", materials=["nope/at/all.md"])["materials"]["nope/at/all.md"]
    assert missing == {"missing": "all.md"}


def test_layout_schema_flags_missing_fields():
    assert iip.check_layout(LAYOUT) == []
    bad = {"_type": "layout", "steps": [{"name": "s"}]}
    problems = iip.check_layout(bad)
    assert any("expected_command" in p for p in problems)
    assert any("expected_products" in p for p in problems)
    assert iip.check_link({"_type": "link", "name": "n"}) != []


def test_attack_a1_command_mismatch_fails():
    links = _all_links()
    assert iip.verify(LAYOUT, links)["verdict"] in ("pass", "fail")
    links[0]["command"] = ["tools/rm", "-rf", "/"]       # 伪造：声称跑了别的东西
    res = iip.verify(LAYOUT, links)
    assert res["verdict"] == "fail" and any("[①]" in p for p in res["problems"])


def test_missing_signature_is_fail_closed():
    links = _all_links()
    res = iip.verify(LAYOUT, links)
    assert res["fail_closed"] is True
    assert res["verdict"] == "fail", "未签名的 link 竟然判 pass ⇒ 不是证据却成了证据"
    assert any("[③]" in p for p in res["problems"])
    links[0]["signatures"] = [{"keyid": "k1", "sig": "deadbeef"}]
    assert any("[③]" in p for p in iip.verify(LAYOUT, links)["problems"]), \
        "只签一条仍不足以覆盖全部步骤 ⇒ 必须继续 fail"


def test_attack_a3_skipped_step_fails():
    links = _all_links()[:-1]                              # 跳过最后一步
    res = iip.verify(LAYOUT, links)
    assert res["verdict"] == "fail" and any("[④]" in p for p in res["problems"])


def test_attack_a2_missing_product_fails(tmp_path: Path):
    links = _all_links()
    # 把 solve 步的产物换成一个不相干文件 ⇒ 偷换产物必须被 ② 抓到
    links[1]["products"] = {str(tmp_path / "unrelated.json"): {"sha256": "0" * 64}}
    res = iip.verify(LAYOUT, links)
    assert any("[②]" in p for p in res["problems"])


def test_cli_roundtrip_exit_codes(tmp_path: Path):
    layout_p = tmp_path / "layout.json"
    layout_p.write_text(json.dumps(LAYOUT, ensure_ascii=False), encoding="utf-8")
    link_p = tmp_path / "generate.link"
    assert iip.main(["gen-link", "generate",
                     "--command", "tools/attack_edge_generator.py", "generate",
                     "--products", "data/attack_edges_candidates.jsonl",
                     "--out", str(link_p)]) == 0
    link = json.loads(link_p.read_text(encoding="utf-8"))
    assert link["signatures"] == []
    assert iip.main(["verify", "--layout", str(layout_p), "--links", str(link_p)]) == 1
    assert iip.main(["--check"]) == 0
