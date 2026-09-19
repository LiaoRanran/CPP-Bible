"""601 任务3 · 585 三攻击封堵回归（含**残余风险**的显式证伪）。

585 的三个 meta 攻击（600 调研复核）与本批防护的对应关系：

| 攻击 | 手法 | 本批防护层（哪一层检出） |
|---|---|---|
| **攻击1 规则供给链** | 改"什么算通过"的定义/信任根数据 | ① `tool_integrity --check` core（规则**内嵌** gate_engine.py）② supply_chain 节（台账/manifest）③ Merkle 根（atoms/evidence/…）④ manifest self_hash |
| **攻击2 毒样例自证** | 自写一条豁免 / 文本 grep 谎报覆盖 | ① supply_chain 节盖 `tools/poison_exemptions.yaml` ② Merkle（若台账在覆盖目录内）③ 行为级 covered 由 581 封堵（本文件不重复跑 slow） |
| **攻击3 人签文本自证** | 直接敲 `human:xxx` | ① 596 的 git 作者绑定（wrong author ⇒ 拒写）② 人审记录文件在 Merkle/供应链覆盖面内时被改 ⇒ 检出 |

**残余风险（600 明说，本文件用测试显式演示，不假装封住了）**：
  * **进程内篡改**（不改文件、只在内存里把规则表置空）：四层**文件级**防护全部无感 ⇒ 需运行时规则指纹，留 W 档；
  * **git 作者可自设**（`git config user.name`）：单用户阶段结构性上限，真正解决要密钥对/第三方身份；
  * `--update` 重签本身不需要身份 ⇒ 与 `.tool_checksums` 的信任边界同源。
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

import attack_edge_review as aer
import gate_engine as ge
import governance_doc_guard as gd
import merkle_integrity as mi
import pytest
import tool_integrity as ti

TOOLS = Path(__file__).resolve().parent.parent / "tools"


def _fake_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """假仓：atoms/evidence/Examples + 一份豁免台账 + 一份治理 manifest。"""
    fake = tmp_path / "repo"
    for rel, text in (("atoms/mem/A.md", "A\n"),
                      ("evidence/conc/E.md", "E\n"),
                      ("Examples/x.cpp", "int main(){}\n"),
                      ("tools/poison_exemptions.yaml", "exemptions:\n  - id: R1\n"),
                      ("data/governance_docs_manifest.json", '{"files": [], "self_hash": "x"}\n')):
        p = fake / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    monkeypatch.setattr(mi, "ROOT", fake)
    monkeypatch.setattr(ti, "ROOT", fake)
    monkeypatch.setattr(ti, "SUPPLY_CHAIN_FILES",
                        ("tools/poison_exemptions.yaml", "data/governance_docs_manifest.json"))
    return fake


def _build_baselines(fake: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    """在假仓里钉三层基准：core（空）+ supply_chain + Merkle 台账。

    返回 (checksums 路径, merkle 台账路径) —— 后者必须**显式**传给 `mi.check_all(roots)`，
    因为 `check_all` 的 `roots_path` 默认参数是导入时绑定的真实路径常量（`ROOTS_PATH`），
    monkeypatch `mi.ROOT` 不会改它；不显式传就会去读真实仓台账而对不上。
    """
    cs = fake / "tools" / ".tool_checksums"
    monkeypatch.setattr(ti, "CHECKSUMS", cs)
    roots = fake / "data" / "supply_chain" / "merkle_roots.json"
    monkeypatch.setattr(mi, "ROOTS_PATH", roots)
    roots.parent.mkdir(parents=True, exist_ok=True)
    roots.write_text(json.dumps(mi.build_all(roots), ensure_ascii=False), encoding="utf-8")
    cs.write_text("# supply_chain\n", encoding="utf-8")
    ti.write_supply_chain_baseline(cs, fake)
    return cs, roots


# ── 攻击1：规则/信任根供给链 ────────────────────────────────────────────────────
def test_attack1_core_layer_detects_tampered_rule_definition(tmp_path: Path):
    """规则**内嵌在 gate_engine.py** ⇒ 篡改它由 core 层检出（在仓副本里验，不动真仓）。"""
    dst = tmp_path / "tools"
    shutil.copytree(TOOLS, dst)
    g = dst / "gate_engine.py"
    g.write_text(g.read_text(encoding="utf-8") + "\n# 585 攻击1：把规则 check 置空\n",
                 encoding="utf-8")
    import subprocess
    import sys

    r = subprocess.run([sys.executable, str(dst / "tool_integrity.py"), "--check"],
                       cwd=str(tmp_path), capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    assert r.returncode == 1, (r.returncode, r.stdout[-300:])
    assert "gate_engine.py" in r.stdout, r.stdout


def test_attack1_merkle_layer_detects_tampered_covered_data(tmp_path: Path,
                                                            monkeypatch: pytest.MonkeyPatch):
    fake = _fake_repo(tmp_path, monkeypatch)
    _cs, roots = _build_baselines(fake, monkeypatch)
    problems, _skipped, code = mi.check_all(roots)
    assert problems == [] and code == 0, (problems, code)   # 假仓只有 3 目录，其余标 skipped 属预期
    (fake / "atoms" / "mem" / "A.md").write_text("A 被改：伪造一条'通过'\n", encoding="utf-8")
    problems, _skipped, code = mi.check_all(roots)
    assert code == 1 and any("atoms" in p for p in problems), problems


def test_attack1_supply_chain_layer_detects_tampered_ledger(tmp_path: Path,
                                                           monkeypatch: pytest.MonkeyPatch):
    """攻击2 的一半也在这里：**豁免台账**（攻击者的"自写自验"面）被改 ⇒ supply_chain 层红。"""
    fake = _fake_repo(tmp_path, monkeypatch)
    _build_baselines(fake, monkeypatch)
    assert ti.verify_supply_chain(root=fake)[2] == 0
    (fake / "tools" / "poison_exemptions.yaml").write_text(
        "exemptions:\n  - id: R1\n  - id: 假豁免\n", encoding="utf-8")
    changed, _warn, code = ti.verify_supply_chain(root=fake)
    assert code == 1 and any("poison_exemptions.yaml" in c[0] for c in changed), changed


def test_attack1_manifest_self_hash_layer(tmp_path: Path):
    """纵深第 4 层：manifest 内容被改而 hash 未同步 ⇒ self_hash 报错（即使没人跑 tool_integrity）。"""
    docs = tmp_path / "References" / "architecture_架构演进"
    docs.mkdir(parents=True)
    (docs / "x.md").write_text("正常\n", encoding="utf-8")
    man = tmp_path / "manifest.json"
    gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    assert gd.verify_self_hash(man)[0] is True
    m = json.loads(man.read_text(encoding="utf-8"))
    m["files"].append({"path": "凭空多出来的投喂词.md", "sha256": "0" * 64, "size": 1})
    man.write_text(json.dumps(m, ensure_ascii=False, indent=1), encoding="utf-8")
    ok, why = gd.verify_self_hash(man)
    assert ok is False and "self-hash mismatch" in why, why


def test_attack1_multi_layer_verifies_depth(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """纵深防御：**同时**改多个文件 ⇒ 多层同时检出（不是"只靠一层"）。"""
    fake = _fake_repo(tmp_path, monkeypatch)
    _cs, roots = _build_baselines(fake, monkeypatch)
    (fake / "atoms" / "mem" / "A.md").write_text("改 1\n", encoding="utf-8")
    (fake / "tools" / "poison_exemptions.yaml").write_text("改 2\n", encoding="utf-8")
    (fake / "data" / "governance_docs_manifest.json").write_text('{"files": []}\n',
                                                                encoding="utf-8")
    layers: list[str] = []
    if mi.check_all(roots)[2] == 1:
        layers.append("merkle")
    changed, _w, code = ti.verify_supply_chain(root=fake)
    if code == 1:
        layers.append("supply_chain")
    assert layers == ["merkle", "supply_chain"], layers
    assert len(changed) == 2, changed


def test_attack1_residual_risk_inmemory_tamper_escapes_file_layers(
        tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """**残余风险（显式证伪）**：进程内把规则表清空、盘上什么都不动 ⇒ 所有**文件级**防护全绿。

    这不是"测试写错了"，而是本批的**已知边界**：文件没变 ⇒ 文件 hash/Merkle/链都无感。
    封堵它需要"运行时规则指纹"（执行前校验规则函数的内存 hash），600 已列为 W 档、本包不做。
    """
    fake = _fake_repo(tmp_path, monkeypatch)
    _cs, roots = _build_baselines(fake, monkeypatch)
    monkeypatch.setattr(ge, "RULES", [])          # ← 攻击：进程内清空规则（不改文件）
    assert ti.main(["--check"]) == 0, "文件级校验对进程内篡改无感（**这正是残余风险**）"
    problems, _skipped, code = mi.check_all(roots)
    assert problems == [] and code == 0, (problems, code)
    assert ti.verify_supply_chain(root=fake)[2] == 0


# ── 攻击2：毒样例自证 ──────────────────────────────────────────────────────────
def test_attack2_exemption_ledger_is_pinned(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    fake = _fake_repo(tmp_path, monkeypatch)
    _build_baselines(fake, monkeypatch)
    base = ti.load_supply_chain_baseline()
    assert "tools/poison_exemptions.yaml" in base, "豁免台账必须进信任根哈希面"
    (fake / "tools" / "poison_exemptions.yaml").write_text("exemptions: []\n", encoding="utf-8")
    changed, _w, code = ti.verify_supply_chain(root=fake)
    assert code == 1 and any("poison_exemptions.yaml" in c[0] for c in changed)


def test_attack2_behavior_level_coverage_lives_in_581():
    """行为级 covered（判"真载荷有没有被 gate 真的拦到"）由 581 封堵 —— 本文件不重复跑 slow。

    显式点名那批测试，避免"以为这里管了"：
    """
    tests = Path(__file__).resolve().parent
    for name in ("test_poison_attack_type.py", "test_poison_exemptions_581.py",
                 "test_poison_coverage_581.py"):
        assert (tests / name).is_file(), f"581 的行为级覆盖测试不见了：{name}"


# ── 攻击3：人签文本自证 ────────────────────────────────────────────────────────
def test_attack3_wrong_git_author_is_refused(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """596 已封堵：人审写入必须过 git 作者绑定；冒名/无签名 ⇒ 拒绝落行。"""
    edges = aer.load_edges()
    edge_id = str(edges[0]["id"])
    p = tmp_path / "ann.jsonl"
    monkeypatch.setattr(aer, "git_user_name", lambda: "LiaoRanran")
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: ("SomebodyElse", "s@x"))
    with pytest.raises(ValueError, match="不是该误解卡"):
        aer.append_annotation(edge_id, "approve", "冒充人签", path=p,
                              edges_path=aer.DEFAULT_EDGES)
    assert not p.exists(), "被拒后不许落行（fail-closed）"


def test_attack3_impersonation_with_other_name_is_refused(tmp_path: Path):
    edges = aer.load_edges()
    p = tmp_path / "ann.jsonl"
    with pytest.raises(ValueError, match="不许冒名"):
        aer.append_annotation(str(edges[0]["id"]), "approve", "冒名", reviewer="NotMe",
                              path=p, edges_path=aer.DEFAULT_EDGES)
    assert not p.exists()


def test_attack3_human_review_step_is_authorized_in_layout():
    """链路层的人审步骤必须是**显式授权**的（layout 声明），不是"谁都能写"。"""
    import supply_chain as sc

    lay = sc.load_layout()
    step = next(s for s in lay["steps"] if s["name"] == "human_review")
    assert step["functionary"] == "human:*"
    assert "data/human_attack_edge_annotations.jsonl" in step["products"]
    assert step["depends_on"] == ["card_authoring"]


def test_attack3_residual_risk_git_author_is_self_settable():
    """**残余风险**：git 作者名可自设 ⇒ 绑定只能证"同名"，证不了"同一人"。

    这一条不测"能防住"，而是把边界写成断言，防止后来者误以为已经被密码学保护：
      * `ge._author_matches` 是**宽松匹配**（大小写/分隔符不敏感、包含即通过）；
      * 真正解决需要密钥对/第三方身份（600 结论），本包不做。
    """
    assert ge._author_matches("liaoranran", ("LiaoRanran", "x@y")) is True
    assert ge._author_matches("someone-else", ("LiaoRanran", "x@y")) is False
