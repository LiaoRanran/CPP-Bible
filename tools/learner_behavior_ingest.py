#!/usr/bin/env python3
"""613 任务C1 · 真实学习行为接入层（append-only，fail-closed）。

612 的学习者镜像只有 `simulate()` 造的模拟掌握度；本工具补上「真实行为 → 事件流」的第一公里。

数据源（`data/learner_behavior.jsonl`，一行一条 JSON）：
    {
      "timestamp": "2026-09-20T23:00:00",   # ISO8601
      "kc_id":     "ATOM-MEM-ALLOC-001",    # 必须是 KC 台账中的已知 KC
      "action_type": "answer" | "review" | "test",
      "correct":   true | false | null,     # answer/test 用；review 可为 null
      "duration_s": 12.5,                   # 可选，>=0
      "source":    "flashcard" | "exam" | ...
    }

纪律：
  * **append-only**：只追加，绝不改写/删除已有行（与 learner_state 同口径）。
  * **fail-closed**：批次内**任何**一条不合法 ⇒ 整批拒绝、一个字节都不写（绝不部分写入）。
  * **去重**：以 (timestamp, kc_id, action_type, correct) 为幂等键，重复行丢弃并计数。
  * **KC 白名单**：kc_id 必须在 `data/kc_inventory_612.json` 中，未知 KC 直接报错。

CLI：
  python tools/learner_behavior_ingest.py --init                # 建空数据文件
  python tools/learner_behavior_ingest.py --source X.jsonl      # 校验（dry-run，默认）
  python tools/learner_behavior_ingest.py --source X.jsonl --write
  python tools/learner_behavior_ingest.py --source X.csv --write
  python tools/learner_behavior_ingest.py --stats
  python tools/learner_behavior_ingest.py --check               # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

DATA = ROOT / "data" / "learner_behavior.jsonl"
KC_JSON = ROOT / "data" / "kc_inventory_612.json"

ACTION_TYPES = ("answer", "review", "test")
REQUIRED = ("timestamp", "kc_id", "action_type")
OPTIONAL = ("correct", "duration_s", "source")


def known_kcs() -> set[str]:
    if not KC_JSON.is_file():
        return set()
    d = json.loads(KC_JSON.read_text(encoding="utf-8"))
    return {k["id"] for k in d.get("kcs", [])}


def _valid_ts(s: str) -> bool:
    try:
        datetime.fromisoformat(s)
        return True
    except (ValueError, TypeError):
        return False


def validate(rec: dict, kcs: set[str] | None = None) -> list[str]:
    """返回错误列表；空列表 = 合法。kc_id 白名单只在传入 kcs 时校验。"""
    errs = []
    if not isinstance(rec, dict):
        return ["记录不是 JSON 对象"]
    for f in REQUIRED:
        if f not in rec or rec[f] in (None, ""):
            errs.append(f"缺必填字段 {f}")
    if "timestamp" in rec and not _valid_ts(str(rec.get("timestamp"))):
        errs.append(f"timestamp 非 ISO8601: {rec.get('timestamp')!r}")
    act = rec.get("action_type")
    if act is not None and act not in ACTION_TYPES:
        errs.append(f"action_type 非法: {act!r}（应为 {'/'.join(ACTION_TYPES)}）")
    cor = rec.get("correct")
    if cor is not None and not isinstance(cor, bool):
        errs.append(f"correct 应为 bool 或 null，实测 {cor!r}")
    if act in ("answer", "test") and cor is None:
        errs.append(f"action_type={act} 必须给 correct")
    dur = rec.get("duration_s")
    if dur is not None:
        try:
            if float(dur) < 0:
                errs.append(f"duration_s 不能为负: {dur}")
        except (TypeError, ValueError):
            errs.append(f"duration_s 非数值: {dur!r}")
    kid = rec.get("kc_id")
    if kcs is not None and kid is not None and kid not in kcs:
        errs.append(f"未知 kc_id（不在 KC 台账）: {kid}")
    return errs


def normalize(rec: dict) -> dict:
    out = {k: rec[k] for k in REQUIRED if k in rec}
    for k in OPTIONAL:
        if k in rec and rec[k] is not None:
            out[k] = rec[k]
    if out.get("duration_s") is not None:
        out["duration_s"] = float(out["duration_s"])
    return out


def dedup_key(rec: dict) -> tuple:
    return (str(rec.get("timestamp")), str(rec.get("kc_id")),
            str(rec.get("action_type")), str(rec.get("correct")))


def load_records(path: Path) -> list[dict]:
    """支持 .jsonl / .csv；CSV 需表头，correct 列的 true/false/"" 会转 bool/null。"""
    if path.suffix.lower() == ".csv":
        out = []
        with path.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                rec = dict(row)
                if "correct" in rec:
                    v = (rec["correct"] or "").strip().lower()
                    rec["correct"] = True if v == "true" else False if v == "false" else None
                if rec.get("duration_s") not in (None, ""):
                    rec["duration_s"] = float(rec["duration_s"])
                elif "duration_s" in rec:
                    rec["duration_s"] = None
                out.append(rec)
        return out
    out = []
    for i, ln in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except json.JSONDecodeError as e:
            out.append({"__parse_error__": f"第 {i} 行 JSON 解析失败: {e}"})
    return out


def ingest(records: list[dict], path: Path = DATA, write: bool = False,
           kcs: set[str] | None = None) -> dict:
    """fail-closed：任何一条不合法 ⇒ 整批拒绝（不写入任何字节）。"""
    parse_bad = [r["__parse_error__"] for r in records if "__parse_error__" in r]
    good_raw = [r for r in records if "__parse_error__" not in r]

    errors: list[tuple[int, str]] = []
    for i, r in enumerate(good_raw, 1):
        for e in validate(r, kcs):
            errors.append((i, e))

    existing: set[tuple] = set()
    if path.is_file():
        for ln in path.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if ln:
                try:
                    existing.add(dedup_key(json.loads(ln)))
                except json.JSONDecodeError:
                    pass

    if errors or parse_bad:
        return {"accepted": 0, "written": 0, "duplicates": 0, "rejected": len(errors) + len(parse_bad),
                "errors": [f"L{i}: {e}" for i, e in errors] + parse_bad, "aborted": True}

    seen: set[tuple] = set()
    batch: list[dict] = []
    dups = 0
    for r in good_raw:
        k = dedup_key(r)
        if k in existing or k in seen:
            dups += 1
            continue
        seen.add(k)
        batch.append(normalize(r))

    if write and batch:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as fh:
            for r in batch:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    return {"accepted": len(batch), "written": len(batch) if write else 0, "duplicates": dups,
            "rejected": 0, "errors": [], "aborted": False}


def stats(path: Path = DATA) -> dict:
    if not path.is_file():
        return {"exists": False, "n": 0}
    rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    by_act: dict[str, int] = {}
    kcs: set[str] = set()
    n_correct = 0
    for r in rows:
        by_act[r.get("action_type", "?")] = by_act.get(r.get("action_type", "?"), 0) + 1
        kcs.add(str(r.get("kc_id")))
        if r.get("correct") is True:
            n_correct += 1
    return {"exists": True, "n": len(rows), "by_action": by_act, "distinct_kc": len(kcs),
            "n_correct": n_correct}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 C1 · 真实学习行为接入（append-only / fail-closed）")
    ap.add_argument("--source", help="输入文件（.jsonl / .csv）")
    ap.add_argument("--write", action="store_true", help="真正追加写入（默认 dry-run）")
    ap.add_argument("--init", action="store_true", help="建空数据文件")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--no-kc-check", action="store_true", help="跳过 kc_id 白名单校验")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        kcs = known_kcs()
        ok = True
        good = {"timestamp": "2026-09-20T23:00:00", "kc_id": "ATOM-MEM-ALLOC-001",
                "action_type": "answer", "correct": True}
        if validate(good, kcs) != []:
            print(f"[C1] ✗ 合法样例被拒: {validate(good, kcs)}")
            ok = False
        bad_missing = {"timestamp": "2026-09-20T23:00:00"}
        if not validate(bad_missing, kcs):
            print("[C1] ✗ 缺字段记录未被拒")
            ok = False
        bad_act = {"timestamp": "2026-09-20T23:00:00", "kc_id": "X", "action_type": "sleep"}
        if not validate(bad_act, None):
            print("[C1] ✗ 非法 action_type 未被拒")
            ok = False
        # fail-closed：混入坏记录 ⇒ 整批拒绝、accepted=0
        res = ingest([good, bad_missing], path=DATA, write=False, kcs=None)
        if res["accepted"] != 0 or not res["aborted"]:
            print("[C1] ✗ fail-closed 失效（坏批次仍被接受）")
            ok = False
        # 去重：同键两条 ⇒ accepted=1, duplicates=1
        res2 = ingest([good, dict(good)], path=DATA, write=False, kcs=None)
        if res2["accepted"] != 1 or res2["duplicates"] != 1:
            print(f"[C1] ✗ 去重失效: {res2}")
            ok = False
        if not kcs:
            print("[C1] ✗ KC 台账为空")
            ok = False
        print("[C1] " + ("✅ 自验证通过" if ok else "❌ 自验证失败"))
        return 0 if ok else 1

    if a.init:
        DATA.parent.mkdir(parents=True, exist_ok=True)
        if not DATA.exists():
            DATA.write_text("", encoding="utf-8")
        print(f"[C1] 数据文件就绪 {DATA.relative_to(ROOT).as_posix()}（{len(DATA.read_text(encoding='utf-8').splitlines())} 行）")
        return 0

    if a.stats:
        s = stats()
        print(f"[C1] {DATA.name}: exists={s['exists']} n={s.get('n', 0)} "
              f"by_action={s.get('by_action', {})} distinct_kc={s.get('distinct_kc', 0)}")
        return 0

    if not a.source:
        print("[C1] 需要 --source 或 --init / --stats / --check")
        return 1

    src = Path(a.source)
    if not src.is_file():
        print(f"[C1] ✗ 源文件不存在: {src}")
        return 1
    records = load_records(src)
    kcs = None if a.no_kc_check else known_kcs()
    res = ingest(records, path=DATA, write=a.write, kcs=kcs)
    tag = "已写入" if a.write else "dry-run（未写入）"
    if res["aborted"]:
        print(f"[C1] ❌ 整批拒绝（fail-closed）：{res['rejected']} 条不合法，{tag}")
        for e in res["errors"][:10]:
            print(f"     - {e}")
        return 1
    print(f"[C1] ✅ 接受 {res['accepted']} 条 / 去重丢弃 {res['duplicates']} 条 / "
          f"写入 {res['written']} 条（{tag}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
