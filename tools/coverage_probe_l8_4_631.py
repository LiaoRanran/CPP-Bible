"""631 D2 · 探针 #2：向量 **L8.4 透明日志伪造**（P0，此前无探针）

向量定义（629 B1）：攻击**他验链的最后一层**——伪造/篡改透明日志本身，
让"看起来已入册"的凭证实际不存在或被改过。

本探针在**临时目录的日志副本**上执行 5 种伪造攻击，用 628 的 `transparency_log_628`
（`CPPBIBLE_TRANSPARENCY_LOG` 环境变量指向副本）判定**是否被检出**：

| # | 攻击 | 期望 |
|---|---|---|
| 0 | 原样拷贝（基线） | 链完整（`chain_valid=True`） |
| 1 | 删中间条目 | 链断 |
| 2 | 篡改某条 `vsa_hash` | 链断 |
| 3 | 篡改某条 `entry_hash` | 链断 |
| 4 | 伪造追加（凭证文件不存在） | 追加被拒 |

**只读**：生产日志 `data/transparency_log.jsonl` **一个字节都不碰**
（所有攻击都在 `tempfile` 副本上进行，副本用完即删）。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
from typing import Any, Callable, Optional, cast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "coverage_probe_l8_4_631.md")
OUT_JSON = os.path.join(ROOT, "data", "coverage_probe_l8_4_631.json")
PROD_LOG = os.path.join(ROOT, "data", "transparency_log.jsonl")
ENV = "CPPBIBLE_TRANSPARENCY_LOG"


def _read(path: str) -> list[dict[str, Any]]:
    return [json.loads(ln) for ln in open(path, encoding="utf-8") if ln.strip()]


def _write(path: str, entries: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        for e in entries:
            fh.write(json.dumps(e, ensure_ascii=False) + "\n")


def _with_log(path: str, fn: Callable[[Any], dict[str, Any]]) -> dict[str, Any]:
    """把 628 的日志路径临时指向 `path` 并执行 fn（结束后还原环境变量）。"""
    import importlib

    old = os.environ.get(ENV)
    os.environ[ENV] = path
    try:
        import transparency_log_628 as T

        importlib.reload(T)
        return cast(dict, fn(T))
    finally:
        if old is None:
            os.environ.pop(ENV, None)
        else:
            os.environ[ENV] = old
        importlib.reload(T)


def scenario_baseline(path: str) -> dict[str, Any]:
    return _with_log(path, lambda T: {"chain_valid": bool(T.verify_log()["chain_valid"]),
                                      "entries": len(T._read_log())})


def scenario_delete(path: str, entries: list[dict[str, Any]]) -> dict[str, Any]:
    if len(entries) < 3:
        return {"skipped": "条目不足"}
    mid = len(entries) // 2
    kept = entries[:mid] + entries[mid + 1:]
    _write(path, kept)
    return _with_log(path, lambda T: {"chain_valid": bool(T.verify_log()["chain_valid"]),
                                      "removed_index": entries[mid].get("log_index")})


def scenario_tamper_vsa_hash(path: str,
                             entries: list[dict[str, Any]]) -> dict[str, Any]:
    if not entries:
        return {"skipped": "无条目"}
    e = dict(entries[len(entries) // 2])
    e["vsa_hash"] = "0" * 64
    mod = list(entries)
    mod[len(mod) // 2] = e
    _write(path, mod)
    return _with_log(path, lambda T: {"chain_valid": bool(T.verify_log()["chain_valid"]),
                                      "broken_at": T.verify_log().get("broken_at")})


def scenario_tamper_entry_hash(path: str,
                               entries: list[dict[str, Any]]) -> dict[str, Any]:
    if not entries:
        return {"skipped": "无条目"}
    mod = list(entries)
    e = dict(mod[len(mod) // 2])
    e["entry_hash"] = "f" * 64
    mod[len(mod) // 2] = e
    _write(path, mod)
    return _with_log(path, lambda T: {"chain_valid": bool(T.verify_log()["chain_valid"]),
                                      "broken_at": T.verify_log().get("broken_at")})


def scenario_forge_append(path: str, _entries: list[dict[str, Any]]) -> dict[str, Any]:
    def run(T):
        r = T.append_vsa(os.path.join(ROOT, "data", "vsa",
                                      "__does_not_exist__.json"))
        return {"ok": bool(r.get("ok")), "error": r.get("error"),
                "rejected": not r.get("ok")}

    return _with_log(path, run)


def measure() -> dict[str, Any]:
    if not os.path.exists(PROD_LOG):
        return {"vector": "L8.4", "error": "生产日志不存在"}
    entries = _read(PROD_LOG)
    out: dict[str, Any] = {"vector": "L8.4", "name": "透明日志伪造",
                           "prod_entries": len(entries), "scenarios": []}
    with tempfile.TemporaryDirectory() as td:
        # 0 基线
        p0 = os.path.join(td, "base.jsonl")
        shutil.copy2(PROD_LOG, p0)
        r0 = scenario_baseline(p0)
        out["scenarios"].append({"id": 0, "name": "原样拷贝（基线）",
                                 "expect_valid": True, **r0})
        # 1 删条目
        p1 = os.path.join(td, "del.jsonl")
        shutil.copy2(PROD_LOG, p1)
        r1 = scenario_delete(p1, entries)
        out["scenarios"].append({"id": 1, "name": "删中间条目",
                                 "expect_valid": False, **r1})
        # 2 改 vsa_hash
        p2 = os.path.join(td, "vh.jsonl")
        shutil.copy2(PROD_LOG, p2)
        r2 = scenario_tamper_vsa_hash(p2, entries)
        out["scenarios"].append({"id": 2, "name": "篡改 vsa_hash",
                                 "expect_valid": False, **r2})
        # 3 改 entry_hash
        p3 = os.path.join(td, "eh.jsonl")
        shutil.copy2(PROD_LOG, p3)
        r3 = scenario_tamper_entry_hash(p3, entries)
        out["scenarios"].append({"id": 3, "name": "篡改 entry_hash",
                                 "expect_valid": False, **r3})
        # 4 伪造追加（凭证不存在）
        p4 = os.path.join(td, "forge.jsonl")
        shutil.copy2(PROD_LOG, p4)
        r4 = scenario_forge_append(p4, entries)
        out["scenarios"].append({"id": 4, "name": "伪造追加（凭证不存在）",
                                 "expect_rejected": True, **r4})
    for s in out["scenarios"]:
        if "expect_valid" in s and "chain_valid" in s:
            s["as_expected"] = (s["chain_valid"] == s["expect_valid"])
        elif "expect_rejected" in s:
            s["as_expected"] = bool(s.get("rejected")) == s["expect_rejected"]
    out["detected_all"] = all(s.get("as_expected", False) for s in out["scenarios"])
    return out


def write_report() -> str:
    m = measure()
    lines = ["# 631 D2 · 探针 #2：L8.4 透明日志伪造", "",
             f"- 生产日志条目：**{m.get('prod_entries')}** 条（**副本攻击，生产日志零改动**）",
             "- 攻击与检出：", "",
             "| # | 攻击 | 期望 | 实际 | 判定 |", "|---|---|---|---|---|"]
    for s in m.get("scenarios", []):
        exp = ("链完整" if s.get("expect_valid") else
               ("链断" if "expect_valid" in s else "追加被拒"))
        act = ("链完整" if s.get("chain_valid") else
               ("链断" if "chain_valid" in s else
                ("被拒" if s.get("rejected") else "未拒")))
        lines.append(f"| {s['id']} | {s['name']} | {exp} | {act} | "
                     f"{'✅' if s.get('as_expected') else '❌'} |")
    lines += [
        "", f"**全部按预期检出：{m.get('detected_all')}**", "",
        "## 诚实登记", "",
        "1. 探针攻击的是**临时副本**；生产日志 `data/transparency_log.jsonl` 零改动"
        "（副本用完即删，`--check` 只读）；",
        "2. **检出的是「链断」这类结构性伪造**；"
        "若攻击者持有 HMAC 密钥并能重算整条链（同主体，能力相同），"
        "本探针**无法**检出——这是 628 B2 已登记的信任根局限（本探针不解决）；",
        "3. 场景 4 只验证「文件不存在导致拒绝追加」，不是「伪造凭证内容导致拒绝」；"
        "后者需要 HMAC 密钥，等价于场景 2/3。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    import hashlib

    before = hashlib.sha256(open(PROD_LOG, "rb").read()).hexdigest()
    m = measure()
    after = hashlib.sha256(open(PROD_LOG, "rb").read()).hexdigest()
    chk("生产日志零改动（副本攻击）", before == after)
    chk("5 个场景全部执行", len(m.get("scenarios", [])) == 5,
        f"({len(m.get('scenarios', []))})")
    chk("基线场景链完整",
        bool([s for s in m["scenarios"] if s["id"] == 0][0].get("chain_valid")))
    chk("三类伪造全部被检出（链断）",
        all(not s.get("chain_valid", True) for s in m["scenarios"]
            if s["id"] in (1, 2, 3)),
        f"({[(s['id'], s.get('chain_valid')) for s in m['scenarios']]})")
    chk("伪造追加被拒",
        bool([s for s in m["scenarios"] if s["id"] == 4][0].get("rejected")))
    chk("汇总 detected_all", bool(m.get("detected_all")))
    chk("报告存在", os.path.exists(OUT_MD))
    print(f"D2 probe L8.4 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 D2 探针 L8.4 透明日志伪造")
    ap.add_argument("--check", action="store_true", help="只读自检（副本攻击）")
    ap.add_argument("--report", action="store_true", help="写探针报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    print(f"scenarios={len(m.get('scenarios', []))} detected_all={m.get('detected_all')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
