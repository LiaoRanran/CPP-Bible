"""610 D4 · governance × supply chain 联动测试（**只加测试，不改生产代码**）。

验证"治理台账一变 ⇒ 必须重钉 supply chain"这条链真的存在，且**不污染真实仓库**：
  1. `data/governance_docs_manifest.json` 确实在 `tool_integrity.SUPPLY_CHAIN_FILES` 内，
     且 `tools/.tool_checksums` 的 `# supply_chain` 节里**有它的哈希行**（只读断言，不跑 --check）；
  2. tmp 目录里跑完整「生成 → 校验 → 新增文档 → 校验报红 → update --force → 校验转绿」闭环；
  3. **机械证明"必须重钉"**：真实 manifest 的 sha256 == 台账记录的哈希（当前钉住）；
     一旦内容变（tmp 模拟），同一哈希公式必然不匹配 ⇒ `tool_integrity --update` 不可省；
  4. `verify_self_hash` 在 update 后为真；篡改内容后为假（self_hash 拦得住）；
  5. supply chain 的 layout **含 governance inspection**；merkle 台账的 append-only 守卫
     （609 D3）证明"治理变更必须**追加**新快照，不得改写既有行"。
"""
from __future__ import annotations

import json
from pathlib import Path

import governance_doc_guard as gd
import supply_chain as sc
import supply_chain_verify as scv
import tool_integrity as ti

MANIFEST_REL = "data/governance_docs_manifest.json"


def test_governance_manifest_in_supply_chain():
    assert MANIFEST_REL in ti.SUPPLY_CHAIN_FILES, \
        f"治理台账必须被 supply chain 覆盖：{ti.SUPPLY_CHAIN_FILES}"
    text = ti.CHECKSUMS.read_text(encoding="utf-8")
    assert "# supply_chain" in text, "台账里应有 supply_chain 节标记"
    tail = text.split("# supply_chain", 1)[1]
    assert MANIFEST_REL in tail, "supply_chain 节里必须有治理台账的哈希行"
    assert ti.sha256_of(ti.ROOT / MANIFEST_REL) == _recorded_checksum(MANIFEST_REL), \
        "当前哈希必须与台账一致（这就是'钉住'的含义）"


def _recorded_checksum(rel: str) -> str:
    for ln in ti.CHECKSUMS.read_text(encoding="utf-8").splitlines():
        parts = ln.split()
        if len(parts) == 2 and parts[1] == rel:
            return parts[0]
    raise AssertionError(f"台账里没有 {rel}")


def _tmp_docs(tmp_path: Path) -> Path:
    docs = tmp_path / "References"
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "a.md").write_text("# A\n", encoding="utf-8")
    return docs


def test_governance_update_cycle_in_tmp(tmp_path: Path):
    docs = _tmp_docs(tmp_path)
    man = tmp_path / "manifest.json"
    ok, diffs = gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    assert ok and diffs, "首次生成应报告'新增'清单"
    assert gd.verify_manifest(man, docs_root=docs)[0] is True, "刚生成 ⇒ 必须一致"
    assert [f["path"].endswith("a.md") for f in json.loads(man.read_text(encoding="utf-8"))["files"]]

    (docs / "b.md").write_text("# B\n", encoding="utf-8")       # 台账外新增文档
    ok2, diffs2 = gd.verify_manifest(man, docs_root=docs)
    assert ok2 is False and any("新增" in d for d in diffs2), f"必须报红：{diffs2}"

    ok3, _ = gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    assert ok3 is True
    assert gd.verify_manifest(man, docs_root=docs)[0] is True, "重签后应转绿"


def test_governance_change_requires_checksum_repin(tmp_path: Path):
    """真实台账哈希 == 记录值；内容一变 ⇒ 同一哈希公式必然对不上 ⇒ 必须 --update 重钉。"""
    real = ti.ROOT / MANIFEST_REL
    assert ti.sha256_of(real) == _recorded_checksum(MANIFEST_REL)

    copy = tmp_path / "manifest.json"
    doc = json.loads(real.read_text(encoding="utf-8"))
    doc["files"] = doc.get("files", []) + [{"path": "References/新文档.md",
                                            "sha256": "0" * 64, "size": 1}]
    copy.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    assert ti.sha256_of(copy) != _recorded_checksum(MANIFEST_REL), \
        "治理台账一变，台账里的哈希立刻失配 ⇒ 重钉是机械必需而非习惯"


def test_verify_self_hash_after_update(tmp_path: Path):
    docs = _tmp_docs(tmp_path)
    man = tmp_path / "manifest.json"
    gd.update_manifest(force=True, manifest_path=man, docs_root=docs)
    ok, why = gd.verify_self_hash(man)
    assert ok is True and why == ""

    doc = json.loads(man.read_text(encoding="utf-8"))
    doc["files"][0]["sha256"] = "f" * 64                 # 内容被改而 self_hash 未同步
    man.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    ok2, why2 = gd.verify_self_hash(man)
    assert ok2 is False, "内容被改而 self_hash 未同步 ⇒ 必须报红"
    assert "self-hash mismatch" in why2 or "被改过" in why2, why2


def test_supply_chain_layout_covers_governance_and_append_only_guard():
    layout = sc.load_layout()
    inspections = layout.get("inspections") or []
    steps = layout.get("steps") or []
    names = {str(x.get("name")) for x in list(inspections) + list(steps)}
    assert any("governance" in n for n in names), f"链条里必须有 governance 检查：{sorted(names)}"

    raw = (ti.ROOT / "data" / "supply_chain" / "merkle_roots.json").read_text(encoding="utf-8")
    # ⚠️ 实测细节（登记）：609 D3 的 `verify_append_only` 是**行级**前缀检查
    #   —— 末行没有换行的文件无法被"行级追加"（末行会被判成改写）。故演示前先归一化结尾换行。
    ledger = raw if raw.endswith("\n") else raw + "\n"
    assert scv.verify_append_only(ledger, ledger)[0] is True
    appended = ledger + '{"snapshot": "610-repin-demo"}\n'   # 允许：追加新快照（只加不删）
    assert scv.verify_append_only(ledger, appended)[0] is True, "只追加应通过"
    rewritten = ledger.replace('"algo"', '"ALGO"', 1)     # 禁止：改写既有行
    assert scv.verify_append_only(ledger, rewritten)[0] is False, \
        "改写既有行必须被 append-only 守卫抓住（治理变更不得回改历史）"
    truncated = "".join(ledger.splitlines(keepends=True)[:5])
    assert scv.verify_append_only(ledger, truncated)[0] is False, "截断历史必须被抓"


def test_no_real_repo_mutation_by_these_tests():
    """本文件全程只用 tmp_path 写盘；真实 manifest / checksums 的哈希保持钉住状态。"""
    assert ti.sha256_of(ti.ROOT / MANIFEST_REL) == _recorded_checksum(MANIFEST_REL)
    assert "# supply_chain" in ti.CHECKSUMS.read_text(encoding="utf-8")
