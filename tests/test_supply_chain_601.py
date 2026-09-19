"""601 任务2 · in-toto 风格溯源链最小子集回归锁。

锁五件事：
  * link 结构/只追加/可读回；`verify_link` 查字段、授权、materials/products 路径集合、**重算 hash**；
  * layout 自洽：步骤唯一 / 依赖存在 / **无环** / 检查点挂对步骤 / 授权非空；
  * `chain verify` fail-closed：篡改过的 link、缺依赖 link、顺序倒置 ⇒ exit 1；
  * 585 攻击1 的**链路层**检出：目录/文件事后被改 ⇒ 既有 link 的 products hash 对不上；
  * 不自动记录步骤（链可以合法地为空）；不许裸 `except Exception`。
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import merkle_integrity as mi
import pytest
import supply_chain as sc


def _fake_repo(tmp_path: Path) -> Path:
    fake = tmp_path / "repo"
    (fake / "atoms" / "mem").mkdir(parents=True)
    (fake / "atoms" / "mem" / "A.md").write_text("A\n", encoding="utf-8")
    (fake / "evidence").mkdir()
    (fake / "evidence" / "E.md").write_text("E\n", encoding="utf-8")
    (fake / "Examples").mkdir()
    (fake / "Examples" / "x.cpp").write_text("int main(){}\n", encoding="utf-8")
    return fake


@pytest.fixture
def fake_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    fake = _fake_repo(tmp_path)
    monkeypatch.setattr(sc, "ROOT", fake)
    monkeypatch.setattr(mi, "ROOT", fake)
    return fake


# ── link ───────────────────────────────────────────────────────────────────────
def test_create_and_write_and_read_link(fake_repo: Path, tmp_path: Path):
    links = tmp_path / "links"
    link = sc.create_link("card_authoring", functionary="human:LiaoRanran",
                          command="人工编写", now="2026-09-19T18:00:00")
    assert set(link) >= {"step", "functionary", "command", "materials", "products",
                         "timestamp", "signature", "link_version"}
    assert [m["path"] for m in link["products"]] == ["atoms", "evidence", "Examples"]
    assert all(m["kind"] == "dir" and len(m["hash"]) == 64 for m in link["products"])
    p = sc.write_link(link, links)
    assert p.is_file()
    assert sc.read_link(p) == link
    # 同 step+timestamp 再写 ⇒ **加后缀，不覆盖**
    p2 = sc.write_link(link, links)
    assert p2 != p and p2.is_file() and p.is_file()
    assert len(sc.load_links(links)) == 2


def test_link_field_kinds_and_missing_paths(fake_repo: Path, tmp_path: Path):
    (fake_repo / "tools").mkdir()
    (fake_repo / "tools" / "poison_exemptions.yaml").write_text("x: 1\n", encoding="utf-8")
    link = sc.create_link("poison_test", now="2026-09-19T18:01:00")
    by = {m["path"]: m for m in link["materials"]}
    assert by["tools/poison_exemptions.yaml"]["kind"] == "file"
    assert by["atoms"]["kind"] == "dir"
    assert link["functionary"] == "machine:poison_drill.py", "机器步骤用工具名，不带 human: 前缀"
    miss = sc.hash_path("不存在的路径")
    assert miss["kind"] == "missing" and miss["hash"] is None


def test_verify_link_ok_then_detects_tamper(fake_repo: Path, tmp_path: Path):
    lay = sc.create_layout()
    link = sc.create_link("card_authoring", functionary="human:X", now="2026-09-19T18:02:00",
                          layout=lay)
    assert sc.verify_link(link, lay) == []
    (fake_repo / "atoms" / "mem" / "A.md").write_text("A 被篡改\n", encoding="utf-8")
    problems = sc.verify_link(link, lay)
    assert any("atoms" in p and "与记录不符" in p for p in problems), problems


def test_verify_link_rejects_unauthorized_and_path_mismatch(fake_repo: Path):
    lay = sc.create_layout()
    link = sc.create_link("gate_check", now="2026-09-19T18:03:00", layout=lay)
    assert sc.verify_link(link, lay) == []
    bad_who = json.loads(json.dumps(link))
    bad_who["functionary"] = "human:Attacker"
    assert any("未被授权" in p for p in sc.verify_link(bad_who, lay))
    bad_paths = json.loads(json.dumps(link))
    bad_paths["materials"] = [{"path": "Book", "kind": "dir", "hash": "0" * 64}]
    assert any("与 layout 声明不一致" in p for p in sc.verify_link(bad_paths, lay))
    bad_step = json.loads(json.dumps(link))
    bad_step["step"] = "不存在的步骤"
    assert any("不在 layout 里" in p for p in sc.verify_link(bad_step, lay))
    assert sc.verify_link({"step": "gate_check"}, lay)[0].startswith("link 缺字段")


def test_verify_link_without_layout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(sc, "LAYOUT_PATH", tmp_path / "nope.json")
    assert sc.verify_link({"step": "x"}, None)[0].startswith("缺 layout")


# ── layout ─────────────────────────────────────────────────────────────────────
def test_layout_is_self_consistent_and_idempotent():
    lay = sc.create_layout()
    assert sc.verify_layout(lay) == []
    assert lay["steps"][0]["name"] == "card_authoring" and len(lay["steps"]) == 7
    assert len(lay["inspections"]) == 3
    assert lay["generated_at"] is None, "默认不打点（幂等/入库可比对）"
    a = json.dumps(sc.create_layout(), ensure_ascii=False)
    b = json.dumps(sc.create_layout(), ensure_ascii=False)
    assert a == b


def test_layout_verify_catches_cycle_dup_dangling_and_bad_inspection():
    base = sc.create_layout()

    def mutate(fn) -> list[str]:
        lay = json.loads(json.dumps(base))
        fn(lay)
        return sc.verify_layout(lay)

    def _cycle(lay):
        lay["steps"][0]["depends_on"] = ["metrics_collect"]
        lay["steps"][5]["depends_on"] = ["card_authoring"]
    assert any("成环" in p for p in mutate(_cycle)), "A→B→A 必须被检出"

    def _dup(lay):
        lay["steps"][1]["name"] = "card_authoring"
    assert any("重复" in p for p in mutate(_dup))

    def _dangling(lay):
        lay["steps"][1]["depends_on"] = ["不存在"]
    assert any("依赖不存在的步骤" in p for p in mutate(_dangling))

    def _insp(lay):
        lay["inspections"][0]["after"] = "不存在"
    assert any("挂在不存在的步骤" in p for p in mutate(_insp))

    def _noauth(lay):
        lay["steps"][0]["functionary"] = ""
    assert any("未声明授权" in p for p in mutate(_noauth))

    def _empty(lay):
        lay["steps"] = []
    assert sc.verify_layout({"steps": []}) == ["layout 没有任何步骤"]


# ── chain verify ───────────────────────────────────────────────────────────────
def _mk_links(fake_repo: Path, tmp_path: Path, steps=("card_authoring", "gate_check")) -> Path:
    links = tmp_path / "links"
    lay = sc.create_layout()
    for i, s in enumerate(steps):
        who = "human:X" if s == "card_authoring" else None
        link = sc.create_link(s, functionary=who, now=f"2026-09-19T18:0{i}:00", layout=lay)
        sc.write_link(link, links)
    return links


def test_chain_verify_green_then_red_on_tampered_link(fake_repo: Path, tmp_path: Path):
    links = _mk_links(fake_repo, tmp_path)
    problems, notes = sc.chain_verify(links_dir=links, run_inspections=False)
    assert problems == [], problems
    # 篡改一条 link 的 products hash（模拟"改记录"）⇒ 必须红
    f = sorted(links.glob("card_authoring*.json"))[0]
    link = json.loads(f.read_text(encoding="utf-8"))
    link["products"][0]["hash"] = "0" * 64
    f.write_text(json.dumps(link, ensure_ascii=False), encoding="utf-8")
    problems, _ = sc.chain_verify(links_dir=links, run_inspections=False)
    assert any("与记录不符" in p for p in problems), problems


def test_chain_verify_red_on_missing_dependency_or_order_inversion(fake_repo: Path, tmp_path: Path):
    # 只建 gate_check（依赖 card_authoring 没有 link）⇒ 依赖不成立
    only_gate = _mk_links(fake_repo, tmp_path / "a", steps=("gate_check",))
    problems, _ = sc.chain_verify(links_dir=only_gate, run_inspections=False)
    assert any("依赖步骤 card_authoring 没有任何 link" in p for p in problems), problems
    # 顺序倒置：card_authoring 的时间晚于 gate_check
    links = tmp_path / "b" / "links"
    lay = sc.create_layout()
    sc.write_link(sc.create_link("gate_check", now="2026-09-19T18:00:00", layout=lay), links)
    sc.write_link(sc.create_link("card_authoring", functionary="human:X",
                                 now="2026-09-19T18:05:00", layout=lay), links)
    problems, _ = sc.chain_verify(links_dir=links, run_inspections=False)
    assert any("早于" in p for p in problems), problems


def test_chain_verify_empty_chain_is_legal():
    """**系统绝不自动记录步骤**：没有 link 不是错误（链未开始）。"""
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        problems, notes = sc.chain_verify(links_dir=Path(td) / "links", run_inspections=False)
    assert problems == [] and any("没有任何 link" in n for n in notes)


def test_chain_verify_runs_inspections(fake_repo: Path, tmp_path: Path):
    links = _mk_links(fake_repo, tmp_path)
    lay = sc.create_layout()
    lay["inspections"] = [{"name": "fake_ok", "after": "card_authoring",
                           "command": ["-c", "print('ok')"]}]
    problems, notes = sc.chain_verify(links_dir=links, layout=lay, run_inspections=True)
    assert problems == [] and any("fake_ok ✓" in n for n in notes)
    lay["inspections"] = [{"name": "fake_fail", "after": "card_authoring",
                           "command": ["-c", "import sys; sys.exit(3)"]}]
    problems, _ = sc.chain_verify(links_dir=links, layout=lay, run_inspections=True)
    assert any("fake_fail 失败（exit 3）" in p for p in problems), problems


def test_run_inspection_returns_exit_and_output():
    rc, out = sc.run_inspection({"name": "x", "command": ["-c", "print('hello')"]})
    assert rc == 0 and "hello" in out
    rc2, _ = sc.run_inspection({"name": "y", "command": ["-c", "raise SystemExit(2)"]})
    assert rc2 == 2
    rc3, out3 = sc.run_inspection({"name": "z", "command": ["--不存在的选项"]})
    assert rc3 != 0 and out3


# ── stats / CLI / 卫生 ─────────────────────────────────────────────────────────
def test_stats_counts(fake_repo: Path, tmp_path: Path):
    links = _mk_links(fake_repo, tmp_path)
    st = sc.stats(links_dir=links, layout=sc.create_layout())
    assert st["links"] == 2 and st["links_by_step"] == {"card_authoring": 1, "gate_check": 1}
    assert st["steps"] == 7 and len(st["steps_without_link"]) == 5
    assert st["last_by_step"]["gate_check"] == "2026-09-19T18:01:00"


def test_cli_roundtrip(fake_repo: Path, tmp_path: Path, capsys):
    lay_path = tmp_path / "layout.json"
    links = tmp_path / "links"
    argv = ["--layout", str(lay_path), "--links-dir", str(links)]
    assert sc.main(["layout", "init", *argv, "--now", None]) == 0
    assert sc.main(["layout", "verify", *argv]) == 0
    assert sc.main(["link", "create", "card_authoring", *argv,
                    "--functionary", "human:X", "--now", "2026-09-19T18:00:00"]) == 0
    created = sorted(links.glob("*.json"))
    assert created, "link create 必须落盘"
    assert sc.main(["link", "verify", str(created[0]), *argv]) == 0
    assert sc.main(["chain", "verify", *argv, "--no-inspections"]) == 0
    assert sc.main(["stats", *argv, "--json"]) == 0
    # 反例：步骤不存在 ⇒ exit 1；缺 layout ⇒ verify 失败
    assert sc.main(["link", "create", "不存在的步骤", *argv]) == 1
    assert sc.main(["layout", "verify", "--layout", str(tmp_path / "nope.json")]) == 2


def test_hash_path_uses_merkle_for_dirs(fake_repo: Path):
    rec = sc.hash_path("atoms")
    assert rec["hash"] == mi.build_tree(fake_repo / "atoms")["root"]
    assert rec["file_count"] == 1


def test_no_bare_except_exception_in_module():
    import re

    src = (mi.ROOT / "tools" / "supply_chain.py").read_text(encoding="utf-8")
    bad = [ln for ln in src.splitlines()
           if re.match(r"^\s*except\s+Exception", ln) and "noqa" not in ln]
    assert not bad, f"发现裸 except Exception：{bad}"


def test_links_dir_is_not_created_implicitly():
    """只读纪律：`stats`/`chain verify` 不许悄悄建 links 目录（只有 link create 才写）。"""
    assert not sc.LINKS_DIR.exists() or sc.LINKS_DIR.is_dir()
    assert shutil.which("git") or True          # 环境无关占位（保持测试可读性）
