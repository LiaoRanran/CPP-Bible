"""609 A4 · 人审反馈闭环：拒绝原因分类 ⇒ 反馈规则 ⇒（**人确认后**）提升下一轮候选边质量。

闭环的第四段也是最后一段，但这一段**到"建议"为止**：

  * `analyze` 扫人审通道里的 **reject** 记录，把 reason 按 4 类枚举归类，生成反馈规则
    （写入 `data/human_review_feedback_rules.json`，`applied` 默认 **false**）；
  * `apply` 只是把某条规则标记为已确认（still doesn't touch `attack_edge_generator.py`）；
  * 什么时候真的改生成器/下一轮候选边 ⇒ **人说了算**（不均自动发生，这条线就此截断）。

分类规则（**精确到触发词**，命中即归类，取第一个命中的类别）：

  misconception_invalid → downgrade_weight   词：误解不成立 / 误解错误 / MIS 内容有误
  target_mapping_error  → force_mapping      词：目标命题错误 / 映射错误 / 驳斥的不是这条
  duplicate_edge        → deduplicate        词：重复 / 已存在 / 与 XX 重复
  other                 → none               以上都不命中 ⇒ 需人进一步分类（不猜）

规则 schema（`data/human_review_feedback_rules.json`）：
  rule_id FB-XXX · mis_id · category · action · param · source_edge_id ·
  source_reason · applied(bool, 默认 false) · timestamp

CLI：
    analyze                      0 ok（打印分类统计）
    list [--category C] [--applied|--pending]
    apply <rule_id>              0 ok / 1 rule_id 不存在
    report                       0 ok（分布 + 预计下一轮质量提升）
    --check                      0 合法 / 1 非法
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import human_review_cli as hrc  # noqa: E402

VERSION = "1.0"
DEFAULT_ANN = hrc.DEFAULT_ANN
DEFAULT_EDGES = hrc.DEFAULT_EDGES
DEFAULT_RULES = ROOT / "data" / "human_review_feedback_rules.json"

CATEGORIES = ("misconception_invalid", "target_mapping_error", "duplicate_edge", "other")
ACTIONS = ("downgrade_weight", "force_mapping", "deduplicate", "none")

#: (category, action, 触发词, 动作参数)
CLASSIFIERS: tuple[tuple[str, str, tuple[str, ...], dict], ...] = (
    ("misconception_invalid", "downgrade_weight",
     ("误解不成立", "误解错误", "MIS 内容有误", "MIS内容有误"),
     {"from": "low", "to": "very_low"}),
    ("target_mapping_error", "force_mapping",
     ("目标命题错误", "映射错误", "驳斥的不是这条"),
     {"mapping": "strict", "allow_fuzzy": False}),
    ("duplicate_edge", "deduplicate",
     ("重复", "已存在"),
     {"dedupe_key": "source+target"}),
)
_MIS_RE = re.compile(r"MIS-[A-Za-z0-9-]+")


# ── 分类 ──────────────────────────────────────────────────────────────────────
def classify_reason(reason: str) -> tuple[str, str, dict]:
    """reason ⇒ (category, action, param)。不命中任何触发词 ⇒ `other`/`none`。"""
    text = str(reason or "")
    for cat, act, words, param in CLASSIFIERS:
        if any(w in text for w in words):
            return cat, act, dict(param)
    return "other", "none", {}


def mis_of(edge_id: str) -> str:
    """从 `ae-<source>-><target>` 里取 MIS 侧节点；取不到 ⇒ 原样回落 '*'。"""
    m = _MIS_RE.findall(str(edge_id))
    return m[0] if m else "*"


# ── 规则生成 ──────────────────────────────────────────────────────────────────
def load_rules(path: Path | str = DEFAULT_RULES) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        return []
    try:
        doc = json.loads(p.read_text(encoding="utf-8") or "[]")
    except ValueError as exc:
        raise ValueError(f"反馈规则文件 {p} 不是合法 JSON：{exc}") from exc
    if isinstance(doc, dict):
        doc = doc.get("rules", [])
    return list(doc)


def save_rules(rules: list[dict], path: Path | str = DEFAULT_RULES) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rules, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                 encoding="utf-8", newline="\n")
    return p


def _next_id(rules: list[dict]) -> str:
    used = [int(m.group(1)) for r in rules
            if (m := re.fullmatch(r"FB-(\d+)", str(r.get("rule_id", ""))))]
    return f"FB-{max(used) + 1 if used else 1:03d}"


def build_rules(records: list[dict]) -> list[dict]:
    """由人审记录（任意来源，测试可注入）生成规则列表；纯函数。"""
    out: list[dict] = []
    now = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
    for rec in records:
        if hrc.kind_of(rec) != "reject":
            continue
        reason = str(rec.get("reason", ""))
        cat, act, param = classify_reason(reason)
        out.append({"rule_id": "",        # 与既有规则对齐后再编号（见 analyze）
                    "mis_id": mis_of(str(rec.get("edge_id", ""))),
                    "category": cat, "action": act, "param": param,
                    "source_edge_id": str(rec.get("edge_id", "")),
                    "source_reason": reason, "applied": False, "timestamp": now})
    return out


def analyze(*, annotations_path: Path | str = DEFAULT_ANN,
            rules_path: Path | str = DEFAULT_RULES) -> list[dict]:
    """扫 reject 记录 ⇒ 生成/更新反馈规则；**已确认过的 applied 保留**（不因重跑被静默撤销）。"""
    recs = hrc.load_annotations(annotations_path)
    latest = hrc.latest_by_edge(recs)
    new = build_rules(list(latest.values()))
    old = load_rules(rules_path)
    confirmed = {(str(r.get("source_edge_id")), str(r.get("category"))): bool(r.get("applied"))
                 for r in old}
    stable_ts = {str(r.get("source_edge_id")): str(r.get("timestamp") or "") for r in old}
    rules: list[dict] = []
    for r in new:
        key = (r["source_edge_id"], r["category"])
        r["applied"] = confirmed.get(key, False)
        r["timestamp"] = stable_ts.get(r["source_edge_id"], r["timestamp"])
        r["rule_id"] = _next_id(rules + old)
        rules.append(r)
    save_rules(rules, rules_path)
    return rules


# ── 报表 ──────────────────────────────────────────────────────────────────────
def summarize(rules: list[dict]) -> dict:
    dist = {c: sum(1 for r in rules if r.get("category") == c) for c in CATEGORIES}
    expected = {
        "downgrade_weight": sum(1 for r in rules if r.get("action") == "downgrade_weight"),
        "force_mapping": sum(1 for r in rules if r.get("action") == "force_mapping"),
        "deduplicate": sum(1 for r in rules if r.get("action") == "deduplicate"),
        "none": sum(1 for r in rules if r.get("action") == "none"),
    }
    return {"rules": len(rules), "category_distribution": dist, "expected_actions": expected,
            "applied": sum(1 for r in rules if r.get("applied")),
            "pending": sum(1 for r in rules if not r.get("applied")),
            "affected_mis": sorted({str(r.get("mis_id")) for r in rules if r.get("mis_id") != "*"})}


def render_report(s: dict) -> str:
    return "\n".join([
        f"[feedback] 反馈报告 · 规则 {s['rules']} 条"
        f"（已确认 applied {s['applied']} / 待确认 {s['pending']}）",
        "  拒绝原因分布：" + " ".join(f"{k}={s['category_distribution'][k]}" for k in CATEGORIES),
        "  预计下一轮质量提升：降权 "
        f"{s['expected_actions']['downgrade_weight']} · 强制映射 "
        f"{s['expected_actions']['force_mapping']} · 去重 "
        f"{s['expected_actions']['deduplicate']} · 需人再分类 "
        f"{s['expected_actions']['none']}",
        f"  受影响 MIS 组 {len(s['affected_mis'])} 个"
        + (f"：{', '.join(s['affected_mis'][:8])}" if s["affected_mis"] else ""),
        "  ⚠️ 以上均为**建议**：applied 默认 false，落到 attack_edge_generator 需人显式确认",
    ])


def render_table(rules: list[dict]) -> str:
    head = f"{'rule_id':<8} {'category':<22} {'action':<17} {'applied':<8} {'mis_id':<16} source_edge_id"
    lines = [head, "-" * len(head)]
    for r in rules:
        lines.append(f"{str(r.get('rule_id', '')):<8} {str(r.get('category', '')):<22} "
                     f"{str(r.get('action', '')):<17} {str(bool(r.get('applied'))):<8} "
                     f"{str(r.get('mis_id', '')):<16} {str(r.get('source_edge_id', ''))}")
    return "\n".join(lines) if rules else "（无反馈规则）"


# ── 校验 ──────────────────────────────────────────────────────────────────────
def check(path: Path | str = DEFAULT_RULES) -> list[str]:
    problems: list[str] = []
    p = Path(path)
    if not p.is_file():
        return problems
    try:
        rules = load_rules(p)
    except ValueError as exc:
        return [str(exc)]
    seen: set[str] = set()
    for i, r in enumerate(rules, 1):
        if not isinstance(r, dict):
            problems.append(f"第 {i} 条不是 JSON 对象")
            continue
        rid = str(r.get("rule_id", ""))
        if not re.fullmatch(r"FB-\d{3}", rid):
            problems.append(f"第 {i} 条 rule_id 非法：{rid!r}（须 FB-XXX）")
        elif rid in seen:
            problems.append(f"第 {i} 条 rule_id 重复：{rid}")
        seen.add(rid)
        for k in ("mis_id", "category", "action", "source_edge_id", "source_reason"):
            if k not in r:
                problems.append(f"第 {i} 条缺字段 {k}")
        if "category" in r and r["category"] not in CATEGORIES:
            problems.append(f"第 {i} 条 category 非法：{r['category']!r}")
        if "action" in r and r["action"] not in ACTIONS:
            problems.append(f"第 {i} 条 action 非法：{r['action']!r}")
        if "applied" in r and not isinstance(r["applied"], bool):
            problems.append(f"第 {i} 条 applied 非 bool：{r['applied']!r}")
    return problems


# ── CLI ───────────────────────────────────────────────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="human_review_feedback",
                                description="609 A4 人审反馈闭环（拒绝原因分类 ⇒ 反馈规则，到人确认为止）")
    p.add_argument("--version", action="version", version=f"human_review_feedback {VERSION}")
    p.add_argument("--annotations", default=str(DEFAULT_ANN))
    p.add_argument("--rules", default=str(DEFAULT_RULES))
    p.add_argument("--check", action="store_true")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("analyze", help="扫 reject 记录生成反馈规则（applied=false）")

    sp = sub.add_parser("list", help="列出反馈规则")
    sp.add_argument("--category", choices=list(CATEGORIES), default=None)
    g = sp.add_mutually_exclusive_group()
    g.add_argument("--applied", dest="only", action="store_const", const=True)
    g.add_argument("--pending", dest="only", action="store_const", const=False)

    sp = sub.add_parser("apply", help="把某条规则标记为已确认（仍需人手才能真正影响生成器）")
    sp.add_argument("rule_id")

    sub.add_parser("report", help="反馈报告")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.check:
        problems = check(args.rules)
        if problems:
            print(f"[feedback] --check FAIL：{len(problems)} 处非法", file=sys.stderr)
            for m in problems[:200]:
                print("  - " + m, file=sys.stderr)
            return 1
        print(f"[feedback] --check OK：规则文件 {args.rules} 共 {len(load_rules(args.rules))} 条全合法")
        return 0

    if args.cmd is None:
        build_parser().print_help()
        return 2

    if args.cmd == "analyze":
        rules = analyze(annotations_path=args.annotations, rules_path=args.rules)
        s = summarize(rules)
        print(f"[feedback] analyze OK：{len(rules)} 条规则（未确认 {s['pending']} 条）→ {args.rules}")
        print("  分类分布：" + " ".join(f"{k}={s['category_distribution'][k]}" for k in CATEGORIES))
        return 0

    if args.cmd == "list":
        rules = load_rules(args.rules)
        if args.category:
            rules = [r for r in rules if r.get("category") == args.category]
        if args.only is not None:
            rules = [r for r in rules if bool(r.get("applied")) is args.only]
        print(render_table(rules))
        return 0

    if args.cmd == "apply":
        rules = load_rules(args.rules)
        hit = [r for r in rules if str(r.get("rule_id")) == str(args.rule_id)]
        if not hit:
            print(f"[feedback] rule_id 不存在：{args.rule_id!r}（当前 {len(rules)} 条规则）",
                  file=sys.stderr)
            return 1
        for r in hit:
            r["applied"] = True
        save_rules(rules, args.rules)
        print(f"APPLIED: {args.rule_id}（已确认；真正改生成器仍需人动手）")
        return 0

    print(render_report(summarize(load_rules(args.rules))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
