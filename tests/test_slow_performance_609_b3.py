"""609 B3 · 多瓶颈缓存回归锁（数据/规则/还原/编译/目录，8 例；与 B1 的 8 例累计 16）。

锁的核心不是"缓存命中"，而是**失效正确性**——缓存最危险的失败模式是"改了输入还返回旧值"：

  1. 数据缓存：同文件命中；**改文件（mtime/size 变）⇒ 必须失效**；
  2. 规则缓存：parser 只被调一次；文件一变 ⇒ 重新解析；
  3. 目录缓存：同目录命中；**目录里新增/改一张卡 ⇒ 签名变 ⇒ 失效**；
  4. 编译缓存：同源内容哈希只 build 一次；源码改 ⇒ 重新 build；
  5. 还原缓存：同指纹命中，不同指纹必须重新 build（不许把两个指纹混用）；
  6. 深拷贝：命中返回的对象被调用方改动，不得污染缓存里的副本；
  7. 接入 `attack_edge_generator`：`read_mis`/`atom_props` 命中缓存且**结果与无缓存版逐字段相同**，
     而"改了目录内容"能立刻反映（签名失效）；
  8. `--check` 自检 exit 0（内部同时验命中与失效两条路径）。
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import attack_edge_generator as aeg
import perf_cache as pc


def _touch(p: Path, text: str) -> None:
    time.sleep(0.01)                     # 保证 mtime_ns 真的变（NTFS 时间戳分辨率）
    p.write_text(text, encoding="utf-8")


# ── 1. 数据缓存 ───────────────────────────────────────────────────────────────
def test_data_cache_hit_and_invalidate(tmp_path: Path):
    f = tmp_path / "d.json"
    f.write_text('{"v": 1}', encoding="utf-8")
    pc.reset()
    assert pc.load_json(f)["v"] == 1
    assert pc.load_json(f)["v"] == 1
    assert pc.STATS["hits"] == 1 and pc.STATS["misses"] == 1
    _touch(f, '{"v": 2}')
    assert pc.load_json(f)["v"] == 2, "改了文件还返回旧值 ⇒ 失效口径破"
    assert pc.STATS["invalidations"] >= 1
    assert pc.read_text(f) == '{"v": 2}'


# ── 2. 规则缓存 ───────────────────────────────────────────────────────────────
def test_rule_cache_parses_once_and_reparses_on_change(tmp_path: Path):
    f = tmp_path / "rules.json"
    f.write_text('{"r": [1]}', encoding="utf-8")
    calls = {"n": 0}

    def parser(text: str):
        calls["n"] += 1
        return json.loads(text)

    pc.reset()
    assert pc.load_rules(f, parser)["r"] == [1]
    assert pc.load_rules(f, parser)["r"] == [1]
    assert calls["n"] == 1, f"解析被调 {calls['n']} 次（应只 1 次）"
    _touch(f, '{"r": [1, 2]}')
    assert pc.load_rules(f, parser)["r"] == [1, 2] and calls["n"] == 2


# ── 3. 目录缓存 ───────────────────────────────────────────────────────────────
def test_dir_cache_invalidates_on_new_file(tmp_path: Path):
    d = tmp_path / "cards"
    d.mkdir()
    (d / "a.md").write_text("a", encoding="utf-8")
    calls = {"n": 0}

    def builder() -> int:
        calls["n"] += 1
        return len(list(d.rglob("*.md")))

    pc.reset()
    assert pc.cached_dir(d, "*.md", builder) == 1
    assert pc.cached_dir(d, "*.md", builder) == 1
    assert calls["n"] == 1, "同目录应命中缓存"
    (d / "b.md").write_text("b", encoding="utf-8")
    assert pc.cached_dir(d, "*.md", builder) == 2, "目录新增文件未失效 ⇒ 拿到过期快照"
    assert calls["n"] == 2


# ── 4. 编译缓存 ───────────────────────────────────────────────────────────────
def test_compile_cache_keyed_by_source_hash(tmp_path: Path):
    src = tmp_path / "s.cpp"
    src.write_text("int main(){}", encoding="utf-8")
    calls = {"n": 0}

    def build() -> str:
        calls["n"] += 1
        return f"obj-{calls['n']}"

    pc.reset()
    assert pc.compile_once(src, build) == pc.compile_once(src, build) == "obj-1"
    assert calls["n"] == 1
    _touch(src, "int main(){return 0;}")
    assert pc.compile_once(src, build) == "obj-2", "源码改了仍在用旧产物"


# ── 5. 还原缓存按指纹隔离 ─────────────────────────────────────────────────────
def test_restore_cache_is_per_fingerprint():
    calls = {"n": 0}

    def build() -> int:
        calls["n"] += 1
        return calls["n"]

    pc.reset()
    assert pc.restore("fp-A", build) == pc.restore("fp-A", build) == 1
    assert pc.restore("fp-B", build) == 2, "不同指纹必须各自 build（不许混用）"
    assert calls["n"] == 2


# ── 6. 深拷贝隔离 ─────────────────────────────────────────────────────────────
def test_cache_returns_deep_copy(tmp_path: Path):
    f = tmp_path / "d.json"
    f.write_text('{"lst": [1, 2]}', encoding="utf-8")
    pc.reset()
    first = pc.load_json(f)
    first["lst"].append(999)                     # 调用方改坏返回值
    assert pc.load_json(f)["lst"] == [1, 2], "缓存副本被污染 ⇒ 命中会把脏数据传播出去"


# ── 7. 接入 attack_edge_generator ─────────────────────────────────────────────
def test_attack_edge_generator_uses_cache_without_changing_results():
    pc.reset()
    cached = aeg.read_mis()
    raw = aeg._read_mis_uncached()
    assert cached == raw, "缓存版与无缓存版结果必须逐字段相同（口径不许变）"
    hits_before = pc.STATS["hits"]
    assert aeg.read_mis() == raw
    assert pc.STATS["hits"] > hits_before, "第二次 read_mis 未命中缓存 ⇒ 接入没生效"
    assert aeg.atom_props() == aeg._atom_props_uncached()
    # 实测：`misconceptions/MIS-*.md` 共 79 张（不等于攻击图里的 42 个 MIS 节点，
    # 也不等于 v7 基线的 83 张**证据卡**——三个数各是各的口径，不许混用）
    assert len(raw) == 79, f"误区卡数变了：{len(raw)}（实测基线 79）"


def test_directory_change_invalidates_attack_edge_generator_cache(tmp_path: Path):
    d = tmp_path / "mis"
    d.mkdir()
    (d / "MIS-X-001.md").write_text(
        "---\nid: MIS-X-001\nrelated_atoms: [ATOM-X-001]\nrefutations: [测试卡]\n---\n正文\n",
        encoding="utf-8")
    pc.reset()
    assert set(aeg.read_mis(d)) == {"MIS-X-001"}
    (d / "MIS-X-002.md").write_text(
        "---\nid: MIS-X-002\nrelated_atoms: [ATOM-X-001]\nrefutations: [第二张]\n---\n正文\n",
        encoding="utf-8")
    assert set(aeg.read_mis(d)) == {"MIS-X-001", "MIS-X-002"}, "新增卡片未进缓存结果"


# ── 8. 自检 ───────────────────────────────────────────────────────────────────
def test_check_is_green():
    assert pc.check() == []
    assert pc.main(["--check"]) == 0
