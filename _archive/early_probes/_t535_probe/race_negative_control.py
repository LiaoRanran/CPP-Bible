#!/usr/bin/env python3
"""C1 的阴性对照：把"朴素增量迁移"造出来，验证新 pytest 有牙齿。

朴素版 = d976170 的 PRAGMA 顺序（journal_mode 先于 busy_timeout）+ 逐列
`PRAGMA table_info` 检查后单条 `ALTER`（各自自动提交、无版本门、无单事务）。
沙箱（534 §5 坑①）实测该形态双进程冷启动 6/8 失败；本脚本在**真实仓库的正式代码**
上重现同一形态，跑 12 轮统计失败数。用完即删（临时探针，不入库）。
"""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = (REPO / "tools" / "task_queue.py").read_text(encoding="utf-8")

# ① 复原旧 PRAGMA 顺序（WAL 先、busy_timeout 后）且去掉 _set_wal 的显式重试
naive = SRC.replace(
    '    conn.execute("PRAGMA busy_timeout=10000")\n    _set_wal(conn)',
    '    conn.execute("PRAGMA journal_mode=WAL")\n    conn.execute("PRAGMA busy_timeout=10000")')
assert naive != SRC, "PRAGMA 顺序替换失败"

# ② 把 migrate 的"单事务 + 版本门"换成"逐列检查 + 各自提交"
start = naive.index("def migrate(")
end = naive.index("def init(")
NAIVE_MIGRATE = '''def migrate(db_path: Path | str | None = None) -> int:
    """朴素版：无版本门、无单事务（每句 ALTER 各自提交）。"""
    p = Path(db_path) if db_path else DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p), timeout=15.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=15000")
        conn.executescript(DDL)
        have = {r["name"] for r in conn.execute("PRAGMA table_info(tasks)")}
        for col, decl in NEW_COLS.items():
            if col not in have:
                conn.execute(f"ALTER TABLE tasks ADD COLUMN {col} {decl}")
        conn.executescript(EVENTS_DDL)
        return 0
    finally:
        conn.close()


'''
naive = naive[:start] + NAIVE_MIGRATE + naive[end:]
assert "user_version" not in naive.split("def migrate")[1].split("def init")[0]

tmp = Path(tempfile.mkdtemp(prefix="c1_naive_"))
naive_py = tmp / "naive_tq.py"
naive_py.write_text(naive, encoding="utf-8")

fails = 0
msgs: list[str] = []
for rnd in range(12):
    db = tmp / f"cold{rnd}" / "queue.db"
    procs = [subprocess.Popen(
        [sys.executable, str(naive_py), "--db", str(db), "enqueue",
         "--type", "redteam", "--payload-ref", f"cold/{rnd}/p{i}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", errors="replace") for i in range(2)]
    for i, p in enumerate(procs):
        o, e = p.communicate(timeout=180)
        if p.returncode != 0:
            fails += 1
            msgs.append(f"round{rnd} proc{i} rc={p.returncode}: {(e or o).strip().splitlines()[-1][:160]}")
print(f"[阴性对照] 朴素迁移：12 轮 × 2 进程，失败 {fails} 次")
for m in msgs:
    print("   -", m)
sys.exit(0 if fails > 0 else 1)
