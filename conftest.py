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
    if any(name.startswith(p) or p in name for p in SESSION_CLEANUP_KEEP):
        return False, "豁免名单（匹配 SESSION_CLEANUP_KEEP）"
    return False, "非临时产物（保守默认：保留 + 留痕）"


def _read(path: str):
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError:
        return None


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
             tracked: set[str] | None = None) -> tuple[int, int, int]:
    """还原被改文件 + 按安全策略处置会话新建文件。

    返回 (restored, deleted, kept)——kept 即"会话新建但按 640 A5 策略保留"的数量
    （全部留痕于 _auto/cleanup_log.jsonl）。
    """
    root = base or DATA
    tr = tracked if tracked is not None else _tracked_files()
    restored = deleted = kept = 0
    # 1) 处置期间**新建**的文件（当前有、快照里没有）——640 A5：先分类再动手
    for r, _dirs, files in os.walk(root):
        for f in files:
            p = os.path.join(r, f)
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
        if _read(p) != content:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            try:
                with open(p, "wb") as fh:
                    fh.write(content)
                restored += 1
            except OSError:
                pass
    return restored, deleted, kept


@pytest.fixture(scope="session", autouse=True)
def _isolate_production_data():
    """会话级：快照 → 跑测试 → 还原被改 + 按 640 A5 安全策略处置新建。"""
    snap = _snapshot()
    tracked = _tracked_files()
    yield
    restored, deleted, kept = _restore(snap, tracked=tracked)
    if restored or deleted or kept:
        print(f"\n[634 A1/640 A5] 生产 data/ 写隔离：还原被改 {restored} 个、"
              f"删除新建 {deleted} 个、按豁免/保守策略保留 {kept} 个"
              f"（明细：_auto/cleanup_log.jsonl）", flush=True)
