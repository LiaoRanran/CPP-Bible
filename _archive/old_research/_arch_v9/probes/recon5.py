"""582 只读侦察⑤：写作所需的静态计数（零写；只读卡面与 db）。"""
import json
import pathlib
import re
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "tools"))
import atom_evidence_replay as replay   # frontmatter 解析（只读）

atoms = sorted(p for p in (ROOT / "atoms").rglob("ATOM-*.md") if "README" not in p.name)
evs = sorted(p for p in (ROOT / "evidence").rglob("EV-*.md") if "README" not in p.name)
print(f"原子卡 {len(atoms)} · 证据卡 {len(evs)}")

no_oracle = []
has_oracle = 0
for p in atoms + evs:
    m = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    if m.get("verified_by_oracle"):
        has_oracle += 1
    else:
        no_oracle.append(p.stem)
print(f"带 verified_by_oracle 的卡: {has_oracle}；缺: {len(no_oracle)}（示例 {no_oracle[:4]}）")

# 命题统计（不 build，直接读卡）
nprop = 0
nobs = ninf = 0
nlive = 0
for p in atoms:
    m = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    for pr in (m.get("claim_structured") or []):
        if not isinstance(pr, dict):
            continue
        nprop += 1
        ct = str(pr.get("claim_type") or "")
        nobs += ct == "observation"
        ninf += ct == "inference"
        nlive += bool(pr.get("liveness"))
print(f"命题（读卡面）: {nprop}（observation {nobs} / inference {ninf}）· 带命题级 liveness 锚: {nlive}")

# MIS 的 source 字段形态（注意：目录里有非卡文件 ⇒ 解析失败要跳过，不能整批崩）
srcs = []
skipped = []
for p in sorted((ROOT / "misconceptions").rglob("*.md")):
    try:
        m = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        skipped.append(p.name)
        continue
    if not str(m.get("id") or "").startswith("MIS-"):
        skipped.append(p.name)
        continue
    srcs.append(str(m.get("source") or ""))
print(f"  （跳过非 MIS 卡文件 {len(skipped)} 个：{skipped[:4]}）")
pat_ch = sum(1 for s in srcs if re.search(r"ch\d+_", s))
pat_sec = sum(1 for s in srcs if re.search(r"[①-⑳]", s))
print(f"MIS {len(srcs)} 条：source 含 chNN_ 的 {pat_ch} 条、含圈码小节号（①②…）的 {pat_sec} 条")
from collections import Counter
print("  source 形态分布:", Counter(
    ("含ch+圈码" if (re.search(r'ch\d+_', s) and re.search(r'[①-⑳]', s))
     else "仅ch" if re.search(r'ch\d+_', s) else "仅圈码" if re.search(r'[①-⑳]', s)
     else "其它") for s in srcs))

# 知识图谱规模
con = sqlite3.connect(f"file:{ROOT/'data/knowledge_graph.db'}?mode=ro", uri=True)
for tbl in ("nodes", "edges"):
    n = con.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
    print(f"knowledge_graph.{tbl}: {n} 行")
try:
    print("  edge 类型分布:", con.execute(
        "SELECT type, COUNT(*) FROM edges GROUP BY type ORDER BY 2 DESC LIMIT 8").fetchall())
except Exception as e:
    print("  (无 type 列:", e, ")")
con.close()

# metrics.jsonl 条数 + 三曲线字段
lines = [json.loads(x) for x in (ROOT / "data/metrics.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
print(f"metrics.jsonl 条数 {len(lines)}；含 curves 的条数 {sum(1 for o in lines if 'curves' in o)}")
if lines and "curves" in lines[-1]:
    print("  末条 curves 键:", list(lines[-1]["curves"]))

# 门禁规则数（静态读注册表，不跑 gate）
t = (ROOT / "tools/gate_engine.py").read_text(encoding="utf-8")
ids = set(re.findall(r'Finding\(\s*"([A-Z][A-Z0-9\-]{3,})"', t))
print(f"gate_engine 源码中出现的规则 id 字面量: {len(ids)} 个（非运行时真值）")
