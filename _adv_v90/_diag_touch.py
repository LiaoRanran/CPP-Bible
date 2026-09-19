# -*- coding: utf-8 -*-
import sys, tempfile, json, sqlite3
from pathlib import Path
sys.path.insert(0, "tools")
import task_queue as tq

db = Path(tempfile.mkdtemp(prefix="pchk_")) / "q.db"
tq.init(db)
tq.enqueue("probe", "pay.md", touch=["tools/task_queue.py"], db_path=db)
tq.claim("wA", db_path=db)
b = tq.enqueue("probe", "pay.md", touch=["TOOLS/TASK_QUEUE.PY"], db_path=db)
print("enqueue B 返回:", json.dumps(b, ensure_ascii=False, default=str)[:400])

con = sqlite3.connect(db); con.row_factory = sqlite3.Row
print("--- 库中所有任务 touch_set ---")
for r in con.execute("select id,touch_set,status from tasks"):
    print(" ", dict(r))

r = tq.claim("wBx", db_path=db)
print("wBx claim claimed=", bool(r.get("claimed")), " blocked=", r.get("blocked_by_touch"))
print("wBx 完整:", json.dumps(r, ensure_ascii=False, default=str)[:600])
