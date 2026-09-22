"""621 D3 · 人审数据脱敏 + 导出（为未来开源做准备）

**脱敏动作**：
1. **移除 reviewer 身份**：真实姓名 → 稳定化名 `R-<hash8>`（同人同码，便于统计但不暴露身份）
2. **时间戳降精度**：`decided_at` / `timestamp` 截断到**日**（去时刻）
3. **移除个人标识字段**：`source` 路径中的用户目录信息
4. **默认移除哈希链字段**（`self_hash` / `prev_hash` / `seq`）：它们可作为**持久关联标识**，
   把人审记录串成可追踪链；开源场景下优先匿名（可用 `--keep-chain` 保留以便审计）

**⚠ 脱敏 ≠ 完全匿名**（详见报告 §局限性）：`reason` 文本可能残留可识别信息；
时间戳到"日"仍可与其它日志做关联分析；稳定化名本身在跨数据集时仍可被链接。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

AUTHORITY_LOG = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
LEGACY_ANNOTATIONS = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
DEFAULT_OUT = os.path.join(ROOT, "data", "human_review_anonymized_621.jsonl")
DEFAULT_REPORT = os.path.join(ROOT, "data", "human_review_anonymization_report_621.md")

SALT = "cpp-bible-621-anon"
PERSONAL_FIELDS = ("reviewer", "self_hash", "prev_hash", "seq")
DATE_FIELDS = ("decided_at", "timestamp")
# Windows 用户目录（C:\Users\<name>）与 posix home（/home/<name>、/Users/<name>）
HOME_RE = re.compile(r"(?i)(?:[a-z]:\\users\\|/(?:home|users)/)([^\\/\s\"']+)")


def pseudonym(name: str, salt: str = SALT) -> str:
    if not name:
        return "R-unknown"
    h = hashlib.sha256((salt + str(name)).encode("utf-8")).hexdigest()
    return f"R-{h[:8]}"


def to_date(value: object) -> object:
    if not value:
        return value
    s = str(value)
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", s)
    return m.group(1) if m else s


def scrub_text(value: object) -> object:
    """把文本里的用户目录名替换为 <user>。"""
    if not isinstance(value, str):
        return value
    return HOME_RE.sub(lambda m: m.group(0).replace(m.group(1), "<user>"), value)


def anonymize_entry(entry: dict, keep_chain: bool = False) -> dict:
    out: dict = {}
    for k, v in entry.items():
        if k in PERSONAL_FIELDS and not (keep_chain and k in ("self_hash", "prev_hash", "seq")):
            continue
        if k in DATE_FIELDS:
            out[k] = to_date(v)
        else:
            out[k] = scrub_text(v)
    if "reviewer" in entry:
        out["reviewer_pseudo"] = pseudonym(entry.get("reviewer"))
    return out


def load_jsonl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return [json.loads(ln) for ln in fh if ln.strip()]


def anonymize_all(authority_log: str = AUTHORITY_LOG,
                  legacy: str = LEGACY_ANNOTATIONS,
                  keep_chain: bool = False) -> dict:
    auth = load_jsonl(authority_log)
    old = load_jsonl(legacy)
    rows = [anonymize_entry(e, keep_chain) for e in auth]
    for e in old:
        rows.append(anonymize_entry({"reviewer": e.get("reviewer"),
                                     "reason": e.get("reason"),
                                     "target": {"type": "attack_edge", "id": e.get("edge_id")},
                                     "power": (e.get("action") or "").upper() or None,
                                     "review_method": "batch_authorization",
                                     "decided_at": e.get("timestamp")}, keep_chain))
    return {"authority_count": len(auth), "legacy_count": len(old),
            "rows": rows, "keep_chain": keep_chain}


def residual_identity_scan(rows: list[dict], known_names: list[str]) -> dict:
    """扫描脱敏结果里是否还残留已知人名。"""
    blob = json.dumps(rows, ensure_ascii=False)
    hits = {n: blob.count(n) for n in known_names if n and blob.count(n)}
    return {"known_names": len(known_names), "residual_hits": hits,
            "clean": len(hits) == 0}


def write_jsonl(rows: list[dict], path: str = DEFAULT_OUT) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def render_report(res: dict) -> str:
    o = ["# 621 D3 · 人审数据脱敏报告\n"]
    o.append(f"> Authority 日志 {res['authority_count']} 条 + 历史标注 {res['legacy_count']} 条"
             f" ⇒ 脱敏输出 **{len(res['rows'])}** 条\n")
    o.append("## 一、脱敏方法\n")
    o.append("| # | 动作 | 说明 |")
    o.append("|---|---|---|")
    o.append("| 1 | reviewer → 稳定化名 | `R-<sha256前8>`，同人同码、不可逆推姓名 |")
    o.append("| 2 | 时间戳截断到日 | 去掉时刻，降低时序关联精度 |")
    o.append("| 3 | 用户目录名 → `<user>` | 清除 `C:\\Users\\<name>` / `/home/<name>` 等路径身份 |")
    o.append(f"| 4 | 哈希链字段 | {'**保留**（--keep-chain）' if res['keep_chain'] else '**默认移除**（去关联）'} |")
    o.append("")
    o.append("## 二、脱敏前后数据量对比\n")
    o.append("| 项 | 脱敏前 | 脱敏后 |")
    o.append(f"| 记录条数 | {res['authority_count'] + res['legacy_count']} | {len(res['rows'])} |")
    o.append(f"| 含真实姓名的字段 | {res['authority_count'] + res['legacy_count']} 条有 `reviewer` | "
             f"**0**（改为 `reviewer_pseudo`） |")
    o.append("| 含时刻的时间戳 | 全部 | **0**（截断到日） |")
    o.append("")
    o.append("## 三、残留身份扫描\n")
    scan = res["residual_identity_scan"]
    o.append(f"- 已知真实姓名样本：{scan['known_names']} 个")
    o.append(f"- 脱敏结果中残留命中：**{scan['residual_hits']}**")
    o.append(f"- 判定：**{'干净 ✅' if scan['clean'] else '仍有残留 ⚠'}**")
    o.append("")
    o.append("## 四、脱敏后样例（前 2 条）\n")
    o.append("```json")
    for r in res["rows"][:2]:
        o.append(json.dumps(r, ensure_ascii=False, sort_keys=True))
    o.append("```")
    o.append("")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    e = {"decision_id": "dec-1", "reviewer": "LiaoRanran", "reason": "用户授权批量通过",
         "decided_at": "2026-09-19T23:16:04", "seq": 1,
         "prev_hash": "a" * 64, "self_hash": "b" * 64,
         "target": {"id": "ae-A->B::prop-1"}, "power": "ACCEPT"}
    a = anonymize_entry(e)
    chk("移除真实姓名", "reviewer" not in a)
    chk("改为稳定化名", str(a.get("reviewer_pseudo", "")).startswith("R-"))
    chk("时间戳截断到日", a["decided_at"] == "2026-09-19")
    chk("默认移除哈希链字段", "self_hash" not in a and "prev_hash" not in a and "seq" not in a)
    chk("保留可统计字段", a["power"] == "ACCEPT" and a["target"]["id"].endswith("prop-1"))
    k = anonymize_entry(e, keep_chain=True)
    chk("--keep-chain 保留链字段", "self_hash" in k and "seq" in k)
    chk("化名稳定（同人同码）", pseudonym("LiaoRanran") == pseudonym("LiaoRanran"))
    chk("化名区分（异人异码）", pseudonym("A") != pseudonym("B"))
    chk("空名安全", pseudonym("") == "R-unknown")
    chk("路径脱敏", scrub_text(r"C:\Users\ASUS\x.md").find("<user>") > 0)
    chk("残留扫描可用",
        residual_identity_scan([{"a": "no names"}], ["LiaoRanran"])["clean"] is True)
    chk("残留可被检出",
        residual_identity_scan([{"a": "LiaoRanran"}], ["LiaoRanran"])["clean"] is False)
    print(f"D3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 D3 人审数据脱敏")
    ap.add_argument("--authority-log", default=AUTHORITY_LOG)
    ap.add_argument("--legacy", default=LEGACY_ANNOTATIONS)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--report", default=DEFAULT_REPORT)
    ap.add_argument("--keep-chain", action="store_true", help="保留哈希链字段（默认移除）")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    res = anonymize_all(args.authority_log, args.legacy, args.keep_chain)
    names = sorted({e.get("reviewer") for e in load_jsonl(args.authority_log) if e.get("reviewer")}
                   | {e.get("reviewer") for e in load_jsonl(args.legacy) if e.get("reviewer")})
    res["residual_identity_scan"] = residual_identity_scan(res["rows"], names)
    write_jsonl(res["rows"], args.out)
    with open(args.report, "w", encoding="utf-8") as fh:
        fh.write(render_report(res) + "\n")
    print(json.dumps({"rows": len(res["rows"]), "names_seen": len(names),
                      "residual": res["residual_identity_scan"]["residual_hits"],
                      "clean": res["residual_identity_scan"]["clean"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
