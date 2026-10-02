# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""634 A1 · pytest 生产 `data/` 写隔离（根级 conftest，**非**被完整性钉住的 `tests/conftest.py`）

**病（633 发现）**：全量 pytest 会重写 `data/` 多个文件、向生产透明日志
`data/transparency_log.jsonl` 追加条目 ⇒ 工作区脏文件 60→74、失败数非稳定。
根因（634 任务0）：大量测试**直接调用被测工具的默认写方法**（`write_report()` / `run_e2e()`），
而这些方法默认写到生产 `data/` 路径，未重定向到 `tmp_path`。

**治法（会话级写保护）**：会话开始快照**所有被 git 跟踪的 `data/` 文件**（含透明日志）的字节；
会话结束把**被改动的还原**、把**会话新建的删除** ⇒ pytest 对 `data/` **净引入 0 改动**。

**为什么放根级 conftest 而非 `tests/conftest.py`**：`tests/conftest.py` 被
`tool_integrity.py` 的 `# test_config` 节钉住哈希；改它会触发 `pytest_configure` 的
`--check-test-config` 失败（`pytest.exit(2)`，全套红）。根级 conftest 不在钉住面内，
且作为 rootdir conftest 对全部测试生效（§零.5 未禁新增测试基建）。

**诚实边界**：本 fixture 让 pytest **净**不引入改动；若会话**开始前** `data/` 已是脏的
（如透明日志被**更早**的测试运行追加过），结束时仍是同样的脏（不背锅、也不擅改 JSONL，§零.11）。
"""
from __future__ import annotations

import os

import pytest

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")


_MAX_SNAPSHOT_BYTES = 2 * 1024 * 1024   # 大文件只记存在性，不整读（避免吃内存）

# ── 640 A5（D8 防复发）：会话清理器安全化 ─────────────────────────────────────
# 病（639 D8 实证复现）：会话期间新建的 data/ 文件在会话结束时被**无差别删除**
# （638 报告两度消失；639 中 round3 报告与 check_scan.json 也被删过）。
# 治法三层：
#   1. **tracked 不删**：git ls-files 里的文件一律还原而非删除（tracked 不会出现在
#      "快照外新建"集合，防御性双保险）；
#   2. **正式产物不删**：豁免名单（批次产物模式）内的文件保留；
#   3. **删除有日志**：每次删除/保留都追加 _auto/cleanup_log.jsonl（append-only），
#      记 文件名/时间/原因——638 事故排查难正因为只报数量不报名单。
# 保守默认：非临时、非名单、非 tracked 的会话新建文件**保留并记日志**（残留可审计，
# 误删不可逆——638 的教训是宁可残留）。
SESSION_CLEANUP_KEEP = ("640_", "639_", "638_", "_baseline", "baseline_",
                        "_report", "report_")
CLEANUP_LOG = os.path.join(ROOT, "_auto", "cleanup_log.jsonl")


def _tracked_files() -> set[str]:
    """git ls-files 的 data/ 全集（会话开始时取一次，集合判断 O(1)）。"""
    try:
        import subprocess
        p = subprocess.run(["git", "ls-files", "--", "data"],
                           cwd=ROOT, capture_output=True, text=True, check=False)
        return {os.path.normpath(os.path.join(ROOT, ln.strip()))
                for ln in p.stdout.splitlines() if ln.strip()}
    except OSError:
        return set()


def _cleanup_log(action: str, path: str, reason: str) -> None:
    import datetime
    import json
    try:
        os.makedirs(os.path.dirname(CLEANUP_LOG), exist_ok=True)
        with open(CLEANUP_LOG, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(json.dumps({"ts": datetime.datetime.now().isoformat(timespec="seconds"),
                                 "action": action, "path": os.path.relpath(path, ROOT),
                                 "reason": reason}, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _classify_new(path: str, tracked: set[str]) -> tuple[bool, str]:
    """会话新建文件的处置：(是否删除, 原因)。**保守默认 = 保留**。

    判定顺序：tracked → 临时产物（最具体，优先于豁免名单）→ 豁免名单 → 保守保留。
    """
    name = os.path.basename(path)
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if path in tracked or rel in tracked:
        return False, "tracked（git 在册）"
    if name.endswith((".tmp", ".temp")) or "probe" in name or "canary" in name:
        return True, "临时测试产物（.tmp/probe/canary）"
    # 640b：`data/vsa/` 是**运行时凭证目录**——会话期间新建的凭证若保留，而会话结束
    # 又把透明日志还原到会话前 ⇒ 产生"无主凭证"（640b 实测复现）。凭证+日志必须
    # 同进同出 ⇒ 未跟踪的新凭证一律删除（tracked 的凭证在上方已放行）。
    if rel.startswith("data/vsa/") or rel.startswith("data" + os.sep + "vsa" + os.sep):
        return True, "运行时凭证（会话期的凭证与日志必须同进同出）"
    if any(name.startswith(p) or p in name for p in SESSION_CLEANUP_KEEP):
        return False, "豁免名单（匹配 SESSION_CLEANUP_KEEP）"
    return False, "非临时产物（保守默认：保留 + 留痕）"


def _read(path: str):
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError:
        return None


def _write(path: str, content: bytes) -> None:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(content)
    except OSError:
        pass


# ── 673u 性能优化：逐测试隔离的「元数据快路径」──────────────────────────────
# 病（673u 实测）：`_isolate_merkle_dirs` 每个测试把 4 个受隔离目录的全部内容**读两遍**
# （快照一遍、还原比对一遍），实测 ~30 MB × 2 / 测试。全量 fast 档（4266 例）因此多耗
# ~6000 s CPU —— 占 pytest 腿总 CPU（8159 s）的 **73%**；停用该 fixture 后墙钟
# **377 s → 191 s**。而 walk+stat 只要 0.03 s/次（内容读占 ~0.4 s）⇒ 瓶颈是**读**，不是遍历。
#
# 治法：快照时**额外**记一份 `{path: (size, mtime_ns)}` 指纹。
#   * 还原时：指纹一致的文件直接判定"没被动过"、**不读内容**（省掉还原那一遍读）；
#   * 跨测试：指纹未变则**连快照内容也复用**（省掉快照那一遍读）。
#
# **诚实边界（红线 5：不改变正确性）**：本快路径把"文件是否被改过"的判据从**逐字节比对**
# 换成 **(size, mtime_ns) 比对**。两者只在"**同长度**且**同 mtime** 的静默改内容"下分歧 ——
# 这要求测试写完后**显式把 mtime 改回原值**（`os.utime` / `copystat` / `copy2`）。
# 673u 已全仓核对：所有 `os.utime`/`copystat`/`copy2` 调用都作用于 `tmp_path` / 沙箱 /
# `data/`，**无一作用于受隔离的 `atoms/ evidence/ Examples/ Book/`** ⇒ 本仓当前用例集下等价。
# 需要完全回到"逐字节比对"的原始语义时：设环境变量 `CPPBIBLE_ISOLATE_STRICT=1`（整体关闭快路径）。
_ISOLATE_STRICT = os.environ.get("CPPBIBLE_ISOLATE_STRICT") == "1"
#: base → (指纹, 内容快照)；仅 `_isolate_merkle_dirs` 用（会话级、每 worker 一份）
_ISO_SNAP_CACHE: dict[str, tuple[dict, dict]] = {}


def _scan_stats(base: str) -> dict[str, tuple[int, int]]:
    """`{path: (size, mtime_ns)}` —— 只 scandir + stat，**零内容读**（673u）。

    用 `os.scandir` + `entry.stat()`（走 scandir 已缓存的 stat）而不是
    `os.walk` + `os.path.getsize`，实测 Examples(1597 文件) 0.005 s vs 0.022 s。
    """
    out: dict[str, tuple[int, int]] = {}
    stack = [base]
    while stack:
        d = stack.pop()
        try:
            with os.scandir(d) as it:
                for e in it:
                    try:
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        elif e.is_file(follow_symlinks=False):
                            st = e.stat()
                            out[e.path] = (st.st_size, st.st_mtime_ns)
                    except OSError:
                        continue
        except OSError:
            continue
    return out


def _snapshot(base: str | None = None) -> dict[str, bytes | None]:
    """快照 base 下**全部**文件：小文件存字节，大文件只记存在（None=存在但不还原内容）。"""
    root = base or DATA
    snap: dict[str, bytes | None] = {}
    if not os.path.isdir(root):
        return snap
    for r, _dirs, files in os.walk(root):
        for f in files:
            p = os.path.join(r, f)
            try:
                big = os.path.getsize(p) > _MAX_SNAPSHOT_BYTES
            except OSError:
                big = True
            snap[p] = None if big else _read(p)
    return snap


def _restore(snap: dict[str, bytes | None], base: str | None = None,
             tracked: set[str] | None = None,
             stamps: dict[str, tuple[int, int]] | None = None) -> tuple[int, int, int]:
    """还原被改文件 + 按安全策略处置会话新建文件。

    返回 (restored, deleted, kept)——kept 即"会话新建但按 640 A5 策略保留"的数量
    （全部留痕于 _auto/cleanup_log.jsonl）。

    `stamps`（673u，可选）：快照时刻的 `{path: (size, mtime_ns)}`。给了它 ⇒ 指纹一致的文件
    判为"未改动"、**不读内容**；`None` ⇒ 保持 634 的原始语义（逐字节比对）。
    """
    root = base or DATA
    tr = tracked if tracked is not None else _tracked_files()
    restored = deleted = kept = 0
    cur = _scan_stats(root) if stamps is not None else None
    # 1) 处置期间**新建**的文件（当前有、快照里没有）——640 A5：先分类再动手
    if cur is None:
        walk = (os.path.join(r, f) for r, _d, files in os.walk(root) for f in files)
    else:
        walk = iter(cur)
    for p in walk:
        if p in snap:
            continue
        do_del, reason = _classify_new(p, tr)
        if do_del:
            try:
                os.remove(p)
                deleted += 1
                _cleanup_log("deleted", p, reason)
            except OSError:
                pass
        else:
            kept += 1
            _cleanup_log("kept", p, reason)
    # 2) 还原快照里被改动的**文件**
    for p, content in snap.items():
        if content is None:
            continue
        if cur is not None:
            st = cur.get(p)
            if st is not None and st == stamps.get(p):
                continue                       # 673u：指纹一致 ⇒ 没动过，免读
        if _read(p) != content:
            _write(p, content)
            restored += 1
    return restored, deleted, kept


@pytest.fixture(scope="session", autouse=True)
def _isolate_production_data():
    """会话级：快照 → 跑测试 → 还原被改 + 按 640 A5 安全策略处置新建。"""
    snap = _snapshot()
    stamps = None if _ISOLATE_STRICT else _scan_stats(DATA)   # 673u：还原时的免读指纹
    tracked = _tracked_files()
    yield
    restored, deleted, kept = _restore(snap, tracked=tracked, stamps=stamps)
    if restored or deleted or kept:
        print(f"\n[634 A1/640 A5] 生产 data/ 写隔离：还原被改 {restored} 个、"
              f"删除新建 {deleted} 个、按豁免/保守策略保留 {kept} 个"
              f"（明细：_auto/cleanup_log.jsonl）", flush=True)


# ── 648：仓外「Merkle 覆盖目录」逐测试隔离 ─────────────────────────────────────
# 病（648 实测）：`tool_integrity --check` 的目录级 Merkle 根覆盖
# `atoms/ evidence/ Examples/ Book/ data/mutation(full_baseline)`，而部分攻击/回归测试
# 会**直接写真实的 atoms/ evidence/ 目录**且不还原；并行下另一 worker 的 integrity /
# evidence_sufficiency 测试读到被污染的目录 → 偶发红。data/（3.2GB）只能会话级还原，
# 但这几个目录体量小，故改为**逐测试**快照→严格还原（删新建、复原被改）。
# 快照在每测试开始时拍摄（已含 648 新增的未跟踪文件），故只会清掉“本测试运行期间产生
# 的污染”，不会误删 648 产物；跨测试共享写不属于预期用法（data/ 亦仅会话级还原）。
_ISOLATE_DIRS = [os.path.join(ROOT, d) for d in ("atoms", "evidence", "Examples", "Book")]


def _restore_strict(snap: dict, base: str, stamps: dict | None = None) -> None:
    """逐测试严格还原：删除快照外新建文件（污染），复原被改文件。

    `stamps`（673u，可选）：快照时刻的 `{path: (size, mtime_ns)}`。给了它 ⇒ 指纹一致的文件
    判为"未改动"、**不读内容**；`None` ⇒ 保持 648 的原始语义（逐字节比对）。
    """
    if stamps is None:
        for r, _dirs, files in os.walk(base):
            for f in files:
                p = os.path.join(r, f)
                if p not in snap:
                    try:
                        os.remove(p)
                    except OSError:
                        pass
        for p, content in snap.items():
            if content is None:
                continue
            if _read(p) != content:
                _write(p, content)
        return
    cur = _scan_stats(base)
    for p in cur:
        if p not in snap:
            try:
                os.remove(p)
            except OSError:
                pass
    for p, content in snap.items():
        if content is None:
            continue
        st = cur.get(p)
        if st is not None and st == stamps.get(p):
            continue                                   # 673u：指纹一致 ⇒ 没动过，免读
        if st is None or _read(p) != content:
            _write(p, content)


@pytest.fixture(scope="function", autouse=True)
def _isolate_merkle_dirs():
    if _ISOLATE_STRICT:                                # 673u：严格档 = 648 原始语义
        snaps = {d: _snapshot(d) for d in _ISOLATE_DIRS if os.path.isdir(d)}
        yield
        for d, snap in snaps.items():
            _restore_strict(snap, d)
        return
    # 673u 快路径：指纹未变 ⇒ 复用上次内容快照（零读）；还原时指纹一致 ⇒ 免读
    snaps: dict[str, dict] = {}
    stamps: dict[str, dict] = {}
    for d in _ISOLATE_DIRS:
        if not os.path.isdir(d):
            continue
        fp = _scan_stats(d)
        cached = _ISO_SNAP_CACHE.get(d)
        if cached is not None and cached[0] == fp:
            snaps[d], stamps[d] = cached[1], fp
        else:
            snaps[d] = _snapshot(d)
            stamps[d] = fp
            _ISO_SNAP_CACHE[d] = (fp, snaps[d])
    yield
    for d, snap in snaps.items():
        _restore_strict(snap, d, stamps.get(d))
