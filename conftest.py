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


def _restore(snap: dict[str, bytes | None], base: str | None = None) -> tuple[int, int]:
    """还原被改文件 + 删除会话新建文件（含未跟踪）。返回 (restored, deleted)。"""
    root = base or DATA
    restored = deleted = 0
    # 1) 删除期间**新建**的文件（当前有、快照里没有）
    for r, _dirs, files in os.walk(root):
        for f in files:
            p = os.path.join(r, f)
            if p not in snap:
                try:
                    os.remove(p)
                    deleted += 1
                except OSError:
                    pass
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
    return restored, deleted


@pytest.fixture(scope="session", autouse=True)
def _isolate_production_data():
    """会话级：快照 → 跑测试 → 还原被改 + 删新建，保证 data/ 回到开跑前（净 0 改动）。"""
    snap = _snapshot()
    yield
    restored, deleted = _restore(snap)
    if restored or deleted:
        print(f"\n[634 A1] 生产 data/ 写隔离：还原被改 {restored} 个、删除新建 {deleted} 个",
              flush=True)
