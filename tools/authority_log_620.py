"""620 C2 · Authority 日志（append-only + 哈希链防篡改）

记录所有人审决策（620 C1 定义的四权力：ACCEPT / REJECT / OVERRIDE / ABSTAIN）。

**安全护栏**：
- 只有 `append`，**没有 update / delete**（撤销 = 追加一条 `OVERRIDE` 指向旧 decision_id）
- append 必须含 `reviewer`（含实名，空名无效）与 `reason`（非空）
- 每条含 `prev_hash` + `self_hash`，`verify()` 校验整条链

**硬边界**：
- 不修改现有人审通道（只读导入）
- 日志 append-only
- **不代签任何决策**——本工具只记录人已做出的决策，不自动生成决策

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOG = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
DEFAULT_HISTORY = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")

POWERS = ("ACCEPT", "REJECT", "OVERRIDE", "ABSTAIN")
GENESIS = "0" * 64


def _canonical(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _compute_self_hash(payload: dict, prev_hash: str) -> str:
    return hashlib.sha256((prev_hash + _canonical(payload)).encode("utf-8")).hexdigest()


def load_entries(path: str = DEFAULT_LOG) -> list[dict]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def validate_decision(d: dict) -> list[str]:
    """返回错误列表（空 = 合法）。"""
    errs: list[str] = []
    if d.get("power") not in POWERS:
        errs.append(f"power 必须是 {POWERS}，实际 {d.get('power')!r}")
    reviewer = str(d.get("reviewer") or "").strip()
    if not reviewer:
        errs.append("reviewer 缺失")
    elif reviewer.startswith("human:") and not reviewer[len("human:"):].strip():
        errs.append("空名签收：'human:' 后必须有实名（619 poison P13 教训）")
    if not str(d.get("reason") or "").strip():
        errs.append("reason 缺失或空")
    tid = ((d.get("target") or {}).get("id")) if isinstance(d.get("target"), dict) else None
    if not tid:
        errs.append("target.id 缺失")
    if d.get("power") == "OVERRIDE" and not d.get("overrides"):
        errs.append("power=OVERRIDE 必须指名 overrides（被推翻的 decision_id）")
    return errs


def append(path: str, decision: dict) -> dict:
    """追加一条决策（append-only）。非法决策抛 ValueError（fail-closed）。"""
    errs = validate_decision(decision)
    if errs:
        raise ValueError("非法决策：" + "; ".join(errs))

    entries = load_entries(path)
    prev_hash = entries[-1]["self_hash"] if entries else GENESIS

    payload = {k: v for k, v in decision.items() if k not in ("prev_hash", "self_hash")}
    if "decision_id" not in payload:
        payload["decision_id"] = f"dec-{len(entries) + 1:06d}"

    entry = dict(payload)
    entry["seq"] = len(entries) + 1
    entry["prev_hash"] = prev_hash
    # 哈希必须覆盖「除 self_hash 外的全部字段」（含 seq / prev_hash），
    # 否则与 verify() 重算的 body 不一致 ⇒ 恒定校验失败
    body = {k: v for k, v in entry.items() if k != "self_hash"}
    entry["self_hash"] = _compute_self_hash(body, prev_hash)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(_canonical(entry) + "\n")
    return entry


def query(path: str = DEFAULT_LOG, target_id: str | None = None,
          power: str | None = None) -> list[dict]:
    out = load_entries(path)
    if target_id:
        out = [e for e in out
               if ((e.get("target") or {}).get("id") == target_id)]
    if power:
        out = [e for e in out if e.get("power") == power]
    return out


def list_all(path: str = DEFAULT_LOG) -> list[dict]:
    return load_entries(path)


def verify(path: str = DEFAULT_LOG) -> tuple[bool, list[str]]:
    """校验哈希链完整性（prev_hash 衔接 + self_hash 自洽）。"""
    entries = load_entries(path)
    errs: list[str] = []
    if not entries:
        return True, []
    prev = GENESIS
    for i, e in enumerate(entries, 1):
        if e.get("prev_hash") != prev:
            errs.append(f"第 {i} 条 prev_hash 断裂（期望 {prev[:8]}… 实际 {str(e.get('prev_hash'))[:8]}…）")
        body = {k: v for k, v in e.items() if k != "self_hash"}
        expect = _compute_self_hash(body, e.get("prev_hash", GENESIS))
        if e.get("self_hash") != expect:
            errs.append(f"第 {i} 条 self_hash 不符（内容被篡改）")
        prev = e.get("self_hash", GENESIS)
    return (len(errs) == 0), errs


# ── 历史决策导入 ──────────────────────────────────────────────────────────────
ACTION_TO_POWER = {"approve": "ACCEPT", "modify": "OVERRIDE", "reject": "REJECT"}


def import_history(path: str = DEFAULT_LOG, src: str = DEFAULT_HISTORY) -> int:
    """从现有人审通道只读导入历史决策（不修改源文件）。返回导入条数。"""
    if not os.path.exists(src):
        return 0
    n = 0
    with open(src, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            power = ACTION_TO_POWER.get(str(raw.get("action", "")).lower())
            if power is None:
                continue
            dec = {
                "target": {"type": "attack_edge", "id": raw.get("edge_id")},
                "power": power,
                "reviewer": f"human:{raw.get('reviewer')}".rstrip(":"),
                "reason": raw.get("reason") or "",
                "review_method": "batch_authorization",
                "decided_at": raw.get("timestamp"),
                "source": "import:data/human_attack_edge_annotations.jsonl",
            }
            if not dec["reason"] or not raw.get("reviewer"):
                continue  # 缺 reason/reviewer 的历史条目如实跳过，不编造
            if power == "OVERRIDE":
                # 历史 modify = 人改了 AI 预标注，但导入前**不存在**可指名的 decision_id。
                # 如实指向 legacy 锚点（而非编造一个 dec-000xxx），保持 OVERRIDE 必填 overrides 的约束。
                dec["overrides"] = f"legacy:pre_annotation:{raw.get('edge_id')}"
                dec["note"] = "历史导入：被推翻的是 AI 预标注，非已入链决策"
            append(path, dec)
            n += 1
    return n


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    import tempfile

    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    with tempfile.TemporaryDirectory() as td:
        log = os.path.join(td, "authority_log.jsonl")
        # 空日志
        chk("空日志 verify 通过", verify(log)[0] is True)
        chk("空日志 list 为空", list_all(log) == [])

        d1 = {"target": {"type": "certificate", "id": "ATOM-CONC-FENCE-001"},
              "power": "ACCEPT", "reviewer": "human:LiaoRanran",
              "reason": "逐条核对断言"}
        e1 = append(log, d1)
        chk("append 生成 decision_id", e1["decision_id"] == "dec-000001")
        chk("首条 prev_hash = genesis", e1["prev_hash"] == GENESIS)
        chk("append 后 verify 通过", verify(log)[0] is True)
        chk("query by target 命中", len(query(log, target_id="ATOM-CONC-FENCE-001")) == 1)
        chk("query by power 命中", len(query(log, power="ACCEPT")) == 1)

        d2 = {"target": {"type": "certificate", "id": "ATOM-CONC-FENCE-001"},
              "power": "OVERRIDE", "reviewer": "human:LiaoRanran",
              "reason": "推翻前述决定", "overrides": e1["decision_id"]}
        e2 = append(log, d2)
        chk("OVERRIDE 追加而非删除（仍 2 条）", len(list_all(log)) == 2)
        chk("第二条 prev_hash 接第一条", e2["prev_hash"] == e1["self_hash"])

        # 篡改检测
        entries = load_entries(log)
        entries[1]["reason"] = "被偷偷改了"
        with open(log, "w", encoding="utf-8") as fh:
            for e in entries:
                fh.write(_canonical(e) + "\n")
        good, errs = verify(log)
        chk("篡改可被检测", (not good) and any("self_hash" in x for x in errs))

        # 非法决策 fail-closed
        for bad, label in (
            ({"power": "ACCEPT", "reviewer": "human:", "reason": "x",
              "target": {"id": "A"}}, "空名签收被拒"),
            ({"power": "BOGUS", "reviewer": "human:Bob", "reason": "x",
              "target": {"id": "A"}}, "非法 power 被拒"),
            ({"power": "ACCEPT", "reviewer": "human:Bob", "reason": "",
              "target": {"id": "A"}}, "空 reason 被拒"),
            ({"power": "OVERRIDE", "reviewer": "human:Bob", "reason": "x",
              "target": {"id": "A"}}, "OVERRIDE 缺 overrides 被拒"),
        ):
            try:
                append(log, bad)
                chk(label, False)
            except ValueError:
                chk(label, True)

    print(f"C2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="620 C2 Authority 日志（append-only + 哈希链）")
    ap.add_argument("--log", default=DEFAULT_LOG)
    ap.add_argument("--append", help="追加一条决策（JSON 字符串）")
    ap.add_argument("--query-target", help="按 target.id 查询")
    ap.add_argument("--power", choices=POWERS, help="按权力过滤（配合 --query-target）")
    ap.add_argument("--list", action="store_true", help="列出全部决策")
    ap.add_argument("--verify", action="store_true", help="校验哈希链")
    ap.add_argument("--import-history", action="store_true",
                    help=f"从 {os.path.basename(DEFAULT_HISTORY)} 只读导入历史决策")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    if args.append:
        entry = append(args.log, json.loads(args.append))
        print(_canonical(entry))
        return 0

    if args.import_history:
        n = import_history(args.log)
        good, errs = verify(args.log)
        print(json.dumps({"imported": n, "chain_ok": good, "errors": errs[:5]},
                         ensure_ascii=False))
        return 0 if good else 1

    if args.verify:
        good, errs = verify(args.log)
        for e in errs:
            print("FAIL:", e)
        print(f"chain_ok={good}  entries={len(load_entries(args.log))}")
        return 0 if good else 1

    if args.query_target or args.power:
        for rec in query(args.log, target_id=args.query_target, power=args.power):
            print(_canonical(rec))
        return 0

    if args.list:
        for rec in list_all(args.log):
            print(_canonical(rec))
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
