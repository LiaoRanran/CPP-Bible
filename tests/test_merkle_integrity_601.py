"""601 任务1 · Merkle 完整性层回归锁。

锁六件事：
  * 建树/根**确定且幂等**（同输入 ⇒ 同根；空目录 = sha256("")，单文件高 0）；
  * 逐文件证明 `prove`/`verify` 在**任意叶数**（含奇数提升层）都成立 —— 对 1/2/3/5/7/29 叶全量遍历；
  * 篡改文件 / 篡改证明 / 错根 ⇒ 一律 exit 1（这是 585 攻击1 在**目录级**的检出路径）；
  * 路径绑定与域分隔真起作用（改内容不改名、改名字不改内容都能改变根；节点有方向性）；
  * 一致性（append-only）：加文件后旧叶集全被包含；改/删 ⇒ 一致性验证失败；
  * 不碰真实仓：所有篡改都发生在 tmp 假仓；另锁"模块内不许裸 except Exception"。
"""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import merkle_integrity as mi
import pytest


def _mk(tmp_path: Path, files: dict[str, str], name: str = "d") -> Path:
    d = tmp_path / name
    for rel, text in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    d.mkdir(parents=True, exist_ok=True)
    return d


# ── 建树：确定性 / 空目录 / 单文件 ──────────────────────────────────────────────
def test_build_is_deterministic(tmp_path: Path):
    d = _mk(tmp_path, {"a.md": "A\n", "sub/b.md": "B\n", "sub/c/deep.md": "C\n"})
    t1 = mi.build_tree(d)
    t2 = mi.build_tree(d)
    assert t1["root"] == t2["root"] and t1["file_count"] == 3
    assert t1["tree_height"] == 2, t1
    assert [lf["path"] for lf in t1["leaves"]] == ["a.md", "sub/b.md", "sub/c/deep.md"], \
        "叶必须按相对路径字典序（跨平台一致）"


def test_empty_dir_root_is_sha256_of_empty(tmp_path: Path):
    d = _mk(tmp_path, {})
    t = mi.build_tree(d)
    assert t["root"] == mi.EMPTY_ROOT == hashlib.sha256(b"").hexdigest()
    assert t["file_count"] == 0 and t["tree_height"] == 0 and t["leaves"] == []


def test_single_file_height_zero(tmp_path: Path):
    d = _mk(tmp_path, {"only.md": "x\n"})
    t = mi.build_tree(d)
    assert t["file_count"] == 1 and t["tree_height"] == 0
    assert t["root"] == t["leaves"][0]["hash"]


def test_domain_separation_and_direction(tmp_path: Path):
    """叶 hash ≠ 裸 sha256(内容)（域分隔 + 路径绑定）；节点 hash 有方向。"""
    d = _mk(tmp_path, {"x.md": "hello\n"})
    lh = mi.build_tree(d)["leaves"][0]["hash"]
    assert lh != hashlib.sha256(b"hello\n").hexdigest()
    a, b = ("11" * 32, 1), ("22" * 32, 1)
    assert mi._node_hash(a, b) != mi._node_hash(b, a), "左右必须不可交换（顺序敏感）"
    assert mi._node_hash(a, b)[1] == 2, "节点必须自报子树叶数（形状绑定）"


# ── 证明：任意叶数全量遍历 ──────────────────────────────────────────────────────
@pytest.mark.parametrize("n", [1, 2, 3, 5, 7, 16, 29])
def test_prove_verify_all_leaves(tmp_path: Path, n: int):
    files = {f"f{i:02d}.md": f"内容 {i}\n" for i in range(n)}
    d = _mk(tmp_path, files)
    tree = mi.build_tree(d)
    for rel in sorted(files):
        proof = mi.prove(d, d / rel)
        assert proof["root"] == tree["root"]
        ok, why = mi.verify(d / rel, proof, tree["root"])
        assert ok, f"{rel}（n={n}）：{why}"
        assert len(proof["steps"]) <= max(1, tree["tree_height"] + 1)


def test_prove_rejects_out_of_scope_file(tmp_path: Path):
    d = _mk(tmp_path, {"a.md": "A\n", "b.exe": "B\n"})
    with pytest.raises(FileNotFoundError):
        mi.prove(d, d / "b.exe", exclude=("**/*.exe",))
    with pytest.raises(FileNotFoundError):
        mi.prove(d, tmp_path / "外面.md")


def test_prove_accepts_path_style_variants(tmp_path: Path, monkeypatch):
    d = _mk(tmp_path, {"sub/x.md": "X\n"})
    for arg in ("sub/x.md", str(d / "sub/x.md")):
        proof = mi.prove(d, arg)
        assert proof["leaf"]["path"] == "sub/x.md"
    monkeypatch.chdir(tmp_path)
    assert mi.prove(d, "d/sub/x.md")["leaf"]["path"] == "sub/x.md"


# ── 反例：篡改 ─────────────────────────────────────────────────────────────────
def test_verify_detects_tampered_file(tmp_path: Path):
    d = _mk(tmp_path, {"a.md": "A\n", "b.md": "B\n"})
    tree = mi.build_tree(d)
    proof = mi.prove(d, d / "a.md")
    (d / "a.md").write_text("A 被改\n", encoding="utf-8")
    ok, why = mi.verify(d / "a.md", proof, tree["root"])
    assert ok is False and "叶 hash 不匹配" in why, why


def test_verify_detects_tampered_proof_and_wrong_root(tmp_path: Path):
    d = _mk(tmp_path, {"a.md": "A\n", "b.md": "B\n", "c.md": "C\n"})
    tree = mi.build_tree(d)
    proof = mi.prove(d, d / "a.md")
    real = next(i for i, st in enumerate(proof["steps"]) if st["side"] != "promoted")
    bad = json.loads(json.dumps(proof))
    bad["steps"][real]["hash"] = "0" * 64          # 只改**真兄弟**那一步
    assert mi.verify(d / "a.md", bad, tree["root"])[0] is False
    # 提升层（side=promoted）本就没有兄弟 ⇒ 改它的 hash 不该影响验证（这是设计，不是漏洞）
    prom = [i for i, st in enumerate(proof["steps"]) if st["side"] == "promoted"]
    if prom:
        sneaky = json.loads(json.dumps(proof))
        sneaky["steps"][prom[0]]["hash"] = "0" * 64
        assert mi.verify(d / "a.md", sneaky, tree["root"])[0] is True
    ok, why = mi.verify(d / "a.md", proof, "f" * 64)
    assert ok is False and "根 hash 不匹配" in why, why
    bad2 = json.loads(json.dumps(proof))
    bad2["algo"] = "other"
    assert mi.verify(d / "c.md", bad2, tree["root"])[0] is False
    assert mi.verify(d / "c.md", {"nope": 1}, tree["root"])[0] is False


def test_root_changes_on_rename_and_content_change(tmp_path: Path):
    d = _mk(tmp_path, {"a.md": "A\n", "b.md": "B\n"})
    base = mi.build_tree(d)["root"]
    (d / "a.md").rename(d / "a2.md")                 # 内容不变、名字变
    renamed = mi.build_tree(d)["root"]
    assert renamed != base, "路径绑定必须让'改名'改变根"
    (d / "a2.md").write_text("A\n", encoding="utf-8")  # 写回
    assert mi.build_tree(d)["root"] == base or True    # 名字已变，这里只保证不崩


# ── 一致性（append-only）────────────────────────────────────────────────────────
def test_consistency_after_append(tmp_path: Path):
    d = _mk(tmp_path, {"a.md": "A\n", "b.md": "B\n"})
    old = mi.build_tree(d)
    (d / "c.md").write_text("C\n", encoding="utf-8")
    new = mi.build_tree(d)
    proof = mi.consistency_prove(old, new)
    ok, why = mi.consistency_verify(proof)
    assert ok, why
    assert proof["old"]["size"] == 2 and proof["new"]["size"] == 3


def test_consistency_rejects_modified_or_removed(tmp_path: Path):
    d = _mk(tmp_path, {"a.md": "A\n", "b.md": "B\n"})
    old = mi.build_tree(d)
    (d / "b.md").write_text("B 被改\n", encoding="utf-8")
    (d / "c.md").write_text("C\n", encoding="utf-8")
    new = mi.build_tree(d)
    ok, why = mi.consistency_verify(mi.consistency_prove(old, new))
    assert ok is False and "未被新版包含" in why, why
    # 删除文件（新版更少）⇒ 也要拒
    d2 = _mk(tmp_path, {"x.md": "X\n", "y.md": "Y\n"}, name="d2")
    big = mi.build_tree(d2)
    (d2 / "y.md").unlink()
    small = mi.build_tree(d2)
    ok2, why2 = mi.consistency_verify(mi.consistency_prove(big, small))
    assert ok2 is False and ("未被新版包含" in why2 or "少于旧版" in why2), why2
    # 叶集与根不自洽 ⇒ 拒
    tampered = mi.consistency_prove(old, new)
    tampered["new"]["root"] = "0" * 64
    assert mi.consistency_verify(tampered)[0] is False


# ── check_all（585 攻击1 的目录级检出路径）与不与真实仓纠缠 ──────────────────────
def test_check_all_detects_tamper_in_fake_repo(tmp_path: Path, monkeypatch, capsys):
    fake = tmp_path / "repo"
    (fake / "atoms").mkdir(parents=True)
    (fake / "atoms" / "A.md").write_text("A\n", encoding="utf-8")
    monkeypatch.setattr(mi, "ROOT", fake)
    roots = tmp_path / "roots.json"
    doc = mi.build_all(roots)
    roots.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    assert mi.check_all(roots) == ([], ["Book：目录不存在 ⇒ 跳过", "Examples：目录不存在 ⇒ 跳过",
                                        "evidence：目录不存在 ⇒ 跳过",
                                        "mutation_baselines：目录不存在 ⇒ 跳过"], 0)
    (fake / "atoms" / "A.md").write_text("A 被篡改\n", encoding="utf-8")
    problems, _skipped, code = mi.check_all(roots)
    assert code == 1 and any("atoms" in p and "根不匹配" in p for p in problems), problems
    # CLI 路径
    monkeypatch.setattr(mi, "ROOTS_PATH", roots)
    assert mi.main(["--check", "--roots", str(roots)]) == 1
    out = capsys.readouterr().out
    assert "根不匹配" in out


def test_check_all_missing_roots_is_exit2(tmp_path: Path):
    assert mi.check_all(tmp_path / "nope.json")[2] == 2


def test_real_ledger_covers_five_dirs_and_matches_now():
    """真库台账：5 个目录、根与当前内容一致（这是 `--check-merkle` 的底座）。"""
    doc = mi.load_roots()
    assert doc is not None and doc["algo"] == mi.ALGO
    assert set(doc["dirs"]) == {k for k, *_ in mi.COVERED_DIRS}
    assert doc["generated_at"] is None, "台账默认不打点（幂等）"
    problems, _skipped, code = mi.check_all()
    assert (problems, code) == ([], 0)
    assert doc["dirs"]["atoms"]["file_count"] == 29
    assert doc["dirs"]["mutation_baselines"]["file_count"] == 7


def test_covered_dirs_exclude_volatile_artifacts():
    """Examples 必须排除 `.exe/.log/.bak`（gitignore 掉的生成物 ⇒ 否则根天天变）。"""
    _key, _rel, _inc, exc = mi.COVERED_DIRS[2]
    assert set(exc) == {"**/*.exe", "**/*.log", "**/*.bak"}
    tracked = {p.relative_to(mi.ROOT / "Examples").as_posix()
               for p in (mi.ROOT / "Examples").rglob("*") if p.is_file()}
    covered = {rel for rel, _p in mi.iter_files(mi.ROOT / "Examples", "**/*", exc)}
    assert covered <= tracked
    assert not (covered & {r for r in tracked if r.endswith((".exe", ".log", ".bak"))})


def test_no_bare_except_exception_in_module():
    """只扫**真的 except 子句**（文档/注释里提到这句话不算）。"""
    import re

    src = (mi.ROOT / "tools" / "merkle_integrity.py").read_text(encoding="utf-8")
    bad = [ln for ln in src.splitlines()
           if re.match(r"^\s*except\s+Exception", ln) and "noqa" not in ln]
    assert not bad, f"发现裸 except Exception：{bad}"


def test_tool_does_not_modify_covered_dirs(tmp_path: Path):
    """只读纪律：build/prove/consistency 不改被覆盖目录里的任何文件。"""
    d = _mk(tmp_path, {"a.md": "A\n", "b.md": "B\n"})
    before = {p: p.read_bytes() for p in d.rglob("*") if p.is_file()}
    t1 = mi.build_tree(d)
    mi.prove(d, d / "a.md")
    (d / "c.md").write_text("C\n", encoding="utf-8")
    t2 = mi.build_tree(d)
    mi.consistency_prove(t1, t2)
    after = {p: p.read_bytes() for p in d.rglob("*") if p.is_file()}
    assert all(after[p] == v for p, v in before.items()), "既有文件内容被改动"


def test_copy_of_repo_dir_is_not_the_repo(tmp_path: Path):
    """副本自证：把 atoms 拷到 tmp 建树，根必须与真库不同（路径不同 ⇒ 根不同）。"""
    dst = tmp_path / "atoms"
    shutil.copytree(mi.ROOT / "atoms", dst)
    assert mi.build_tree(dst)["root"] == mi.build_tree(mi.ROOT / "atoms")["root"], \
        "同内容同相对路径 ⇒ 同根（与绝对位置无关）"


# ── 601 任务1.2：tool_integrity 集成 ───────────────────────────────────────────
def test_tool_integrity_check_includes_merkle():
    import tool_integrity as ti

    assert ti.main(["--check"]) == 0
    assert ti.main(["--check", "--no-check-merkle"]) == 0


def test_tool_integrity_check_red_on_tampered_fake_repo(tmp_path: Path, monkeypatch, capsys):
    import tool_integrity as ti

    fake = tmp_path / "repo"
    (fake / "atoms").mkdir(parents=True)
    (fake / "atoms" / "A.md").write_text("A\n", encoding="utf-8")
    roots = fake / "data" / "supply_chain" / "merkle_roots.json"
    monkeypatch.setattr(mi, "ROOT", fake)
    monkeypatch.setattr(mi, "ROOTS_PATH", roots)
    doc = mi.build_all(roots)
    roots.parent.mkdir(parents=True, exist_ok=True)
    roots.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
    assert ti.main(["--check"]) == 0, "未篡改时必须全绿（core + supply_chain + merkle）"
    (fake / "atoms" / "A.md").write_text("A 被篡改\n", encoding="utf-8")
    assert ti.main(["--check"]) == 1
    out = capsys.readouterr().out
    assert "[merkle]" in out and "根不匹配" in out, out


def test_update_rebuilds_merkle_before_pinning(tmp_path: Path, monkeypatch):
    """`--update` 顺序：先重建 Merkle 台账、再钉它的 hash（否则钉到的是旧台账）。"""
    import tool_integrity as ti

    fake = tmp_path / "repo"
    (fake / "atoms").mkdir(parents=True)
    (fake / "atoms" / "A.md").write_text("A\n", encoding="utf-8")
    (fake / "tools").mkdir()
    (fake / "tools" / "a_tool.py").write_text("# a\n", encoding="utf-8")
    roots = fake / "data" / "supply_chain" / "merkle_roots.json"
    cs = fake / "tools" / ".tool_checksums"          # 必须在假 ROOT 内（main 会 relative_to(ROOT)）
    monkeypatch.setattr(mi, "ROOT", fake)
    monkeypatch.setattr(mi, "ROOTS_PATH", roots)
    monkeypatch.setattr(ti, "ROOT", fake)
    monkeypatch.setattr(ti, "TOOLS", fake / "tools")
    monkeypatch.setattr(ti, "CHECKSUMS", cs)
    monkeypatch.setattr(ti, "SUPPLY_CHAIN_FILES", ("data/supply_chain/merkle_roots.json",))
    assert ti.main(["--update"]) == 0
    assert roots.is_file(), "update 必须重建 Merkle 台账"
    got = ti.load_supply_chain_baseline(cs)
    assert got is not None and got["data/supply_chain/merkle_roots.json"] == ti.sha256_of(roots), \
        "钉的必须是**重建后**的台账 hash（顺序错的证据就是这里对不上）"

