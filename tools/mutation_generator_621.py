"""621 A1 · 对抗性 mutation 生成器（雷2 第三阶段）

**为什么需要它**：620 的闭环候选空间**钉死**在 v7 既有 1593 条，
⇒ VFDR 恒 0 是"只考旧题"的结构必然，不是"系统无盲区"。
本工具**生成新 mutation**，让闭环真正有可能发现新逃逸。

三种对抗策略（对应 619 A1 的三个可计算子目标）：

| 策略 | 对应子目标 | 手法 |
|---|---|---|
| `rule_blind_spot` | rule_blind_spot | 针对 gate 规则的检查边界，构造**刚好绕过**的变异（删必需字段 / 键名大小写变形 / 空值占位） |
| `evidence_ambiguity` | evidence_ambiguity | 针对 `artifact_sha256` / `actual` 字段，构造**语义相同但表示不同**的变异（大小写 / 空白 / 换行归一） |
| `provenance_inconsistency` | provenance_inconsistency | 针对卡面引用的工件/证据，构造**引用存在但内容不匹配**的变异（路径大小写 / 同目录兄弟文件替换） |

**安全护栏（硬边界）**：
- 生成的 mutation **只写** `data/mutation/` 或临时目录；写其它路径（尤其受控目录）**直接拒绝**
- **不修改**原始卡、`gate_engine.py`、任何 CORE_TOOLS
- **不自动运行验证**（验证是 A2 的职责，本工具只生成）

**确定性**：不引入随机/时间（除 `generated_at` 可注入），同输入同输出 ⇒ 可复现。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

STRATEGIES = ("rule_blind_spot", "evidence_ambiguity", "provenance_inconsistency")

# 写入白名单：只允许落到这些前缀（相对仓库根，posix）
SAFE_WRITE_PREFIXES = ("data/mutation/",)
CONTROLLED_PREFIXES = ("atoms/", "evidence/", "Examples/", "Book/")

# 目标规则（取自 gate 规则集；本工具只读其名字，不改规则实现）
TARGET_RULES = (
    "EV-FM-REQUIRED", "EV-FM-DUP-KEY", "EV-ARTIFACT-FILE-EXISTS",
    "EV-ARTIFACT-PRODUCER", "EV-FALSIFICATION", "EV-FALSIFICATION-QUANT",
    "EV-MATRIX-UNBACKED", "ATOM-CLAIM-STRUCTURED", "ATOM-ID-UNIQUE",
    "ATOM-FM-REQUIRED", "CARD-PATH-NOT-CANONICAL", "OBSERVATION-LIVENESS",
)

# 各策略的变异模板库（确定性循环取用）
_RULE_TEMPLATES = (
    {"op": "M1", "point": "删 {rule} 所依赖的必需字段", "detail": "删除 frontmatter 中该规则校验的字段"},
    {"op": "M6", "point": "{rule} 键名大小写变形", "detail": "把字段键名改为同义但大小写不同的写法"},
    {"op": "M5", "point": "{rule} 字段置空值占位", "detail": "字段保留但值为空串，规避'缺失'判定"},
)
_EVIDENCE_TEMPLATES = (
    {"op": "M7", "point": "artifact_sha256 大小写归一", "detail": "sha256 改大写，语义等价但逐字不同"},
    {"op": "M6", "point": "actual 块引号风格切换", "detail": "YAML 单引号↔双引号，语义等价"},
    {"op": "M7", "point": "run_match_keys 前后空白注入", "detail": "键名尾部加空格，语义等价"},
    {"op": "M4", "point": "注入恒真断言键", "detail": "追加一个恒为真的断言以稀释判别力"},
)
_PROVENANCE_TEMPLATES = (
    {"op": "M2", "point": "引用路径大小写变形", "detail": "指向同一文件但大小写不同，Windows 可解析、Linux 不可"},
    {"op": "M2", "point": "替换为同目录兄弟工件", "detail": "引用存在但内容不匹配"},
    {"op": "M7", "point": "artifact 与 command -o 目标解耦", "detail": "声明工件与编译产物不是同一文件"},
    {"op": "M3", "point": "弱化 run_match 断言键", "detail": "删掉最具判别力的读数键"},
)


def _templates(strategy: str) -> tuple[dict, ...]:
    return {
        "rule_blind_spot": _RULE_TEMPLATES,
        "evidence_ambiguity": _EVIDENCE_TEMPLATES,
        "provenance_inconsistency": _PROVENANCE_TEMPLATES,
    }[strategy]


def is_safe_path(path: str) -> bool:
    """写入路径必须在白名单内，且绝不能是受控目录。"""
    norm = os.path.normpath(os.path.abspath(path)).replace(os.sep, "/")
    root_norm = os.path.normpath(ROOT).replace(os.sep, "/")
    rel = norm[len(root_norm):].lstrip("/") if norm.startswith(root_norm) else None
    if rel is None:  # 仓库外 ⇒ 只允许临时目录
        tmp = os.path.normpath(os.path.abspath(os.sep + "tmp")).replace(os.sep, "/")
        return norm.startswith(tmp) or "temp" in norm.lower()
    if any(rel.startswith(p) for p in CONTROLLED_PREFIXES):
        return False
    return any(rel.startswith(p) for p in SAFE_WRITE_PREFIXES)


def mutation_id(target_card: str, attack_type: str, content: str) -> str:
    h = hashlib.sha256(f"{target_card}|{attack_type}|{content}".encode("utf-8")).hexdigest()
    return f"MUT-621-{h[:12]}"


def now_iso(now: datetime | None = None) -> str:
    return (now or datetime.now(timezone.utc)).isoformat()


def generate(cards: list[str], rules: tuple[str, ...] = TARGET_RULES,
             count: int = 50, strategy: str = "all",
             now: datetime | None = None) -> list[dict]:
    """确定性生成 mutation 列表（同输入同输出）。"""
    if count <= 0 or not cards:
        return []
    wanted = STRATEGIES if strategy == "all" else (strategy,)
    if strategy not in ("all", *STRATEGIES):
        raise ValueError(f"未知策略：{strategy}（允许 all 或 {STRATEGIES}）")

    ts = now_iso(now)
    out: list[dict] = []
    seen: set[str] = set()
    i = 0
    # 确定性遍历：卡 × 策略 × 模板 轮转，直到凑够 count 或穷尽组合
    max_iter = len(cards) * len(wanted) * 8 + 8
    while len(out) < count and i < max_iter:
        card = cards[i % len(cards)]
        # 策略按 i 轮转（而非「每轮完所有卡才换」），否则 count < 卡数时会只剩第一种策略
        strat = wanted[i % len(wanted)]
        tpls = _templates(strat)
        tmpl = tpls[(i // len(wanted)) % len(tpls)]
        rule = rules[i % len(rules)]
        point = tmpl["point"].format(rule=rule)
        content = json.dumps({"op": tmpl["op"], "point": point, "detail": tmpl["detail"],
                              "target_rule": rule, "target_card": card},
                             ensure_ascii=False, sort_keys=True)
        mid = mutation_id(card, strat, content)
        if mid not in seen:
            seen.add(mid)
            out.append({
                "mutation_id": mid,
                "attack_type": strat,
                "target_rule": rule,
                "target_card": card,
                "content": content,
                "generated_at": ts,
            })
        i += 1
    return out[:count]


def write_jsonl(items: list[dict], path: str) -> str:
    """写 JSONL；路径不安全则拒绝（fail-closed）。"""
    if not is_safe_path(path):
        raise ValueError(f"拒绝写入非白名单路径：{path}（只允许 {SAFE_WRITE_PREFIXES} 或临时目录）")
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for it in items:
            fh.write(json.dumps(it, ensure_ascii=False, sort_keys=True) + "\n")
    return path


def validate_record(rec: dict) -> list[str]:
    """格式校验（空列表 = 合法）。"""
    errs = []
    for f in ("mutation_id", "attack_type", "target_rule", "target_card", "content", "generated_at"):
        if not str(rec.get(f, "")).strip():
            errs.append(f"缺字段 {f}")
    if rec.get("attack_type") not in STRATEGIES:
        errs.append(f"attack_type 非法：{rec.get('attack_type')}")
    try:
        json.loads(rec.get("content") or "null")
    except (TypeError, ValueError):
        errs.append("content 非合法 JSON")
    return errs


# ── 622 A4：生成器 v2（schema-aware + v7 排除 + 新算子 M8/M9）──────────────────
# 依据 622 A3 的改进建议：
#   ① schema-aware：先读目标卡 frontmatter 的真实字段，再决定算子（消除 46% 不适用）
#   ② 排除 v7 已有 (卡, 算子) 对，并引入 v7 没有的算子 ⇒ 把 novelty 从 0.5 档拉到 1.0 档
NEW_STRATEGIES = ("boundary_value", "cross_reference")

# 算子 → 该算子能施加所需的 frontmatter 字段（任一命中即可）
OP_REQUIRED_FIELDS = {
    "M1": ("__any__",), "M6": ("__any__",),
    "M7": ("artifact_sha256",), "M2": ("artifact", "fixture"),
    "M3": ("run_match_keys",), "M4": ("artifact_assert",),
    "M5": ("status",),
    "M8": ("artifact_version", "status"),           # 边界值：版本号/枚举越界
    "M9": ("serves", "relations"),                  # 交叉引用：指向不存在的目标
}
_M8_TEMPLATES = (
    {"op": "M8", "point": "artifact_version 置 0（越界版本号）",
     "detail": "把版本号改成 0，测试版本合法性校验的边界"},
    {"op": "M8", "point": "status 置非法枚举值",
     "detail": "把 status 改成未登记枚举，测试枚举白名单"},
)
_M9_TEMPLATES = (
    {"op": "M9", "point": "serves 指向不存在的原子卡",
     "detail": "把跨卡引用改成不存在的目标，测试引用完整性"},
    {"op": "M9", "point": "relations 指向不存在的目标",
     "detail": "把关系目标改成不存在的卡，测试 DAG/目标存在性"},
)


def card_fields(card_rel: str) -> list[str]:
    """读目标卡 frontmatter 的真实字段名（schema-aware 的基础）。"""
    path = os.path.join(ROOT, card_rel.replace(os.sep, "/"))
    if not os.path.exists(path):
        return []
    sys.path.insert(0, HERE)
    try:
        import pck_batch_migrator_620 as M  # noqa: PLC0415
        fm = M.read_frontmatter(path)
        return sorted(str(k) for k in (fm or {}))
    except Exception:  # noqa: BLE001
        return []


def _op_applicable(op: str, fields: list[str]) -> bool:
    need = OP_REQUIRED_FIELDS.get(op, ())
    if "__any__" in need:
        return bool(fields)
    return any(f in fields for f in need)


def _templates_v2(strategy: str) -> tuple[dict, ...]:
    if strategy == "boundary_value":
        return _M8_TEMPLATES
    if strategy == "cross_reference":
        return _M9_TEMPLATES
    return _templates(strategy)


def generate_v2(cards: list[str], v7: list[dict], count: int = 30,
                include_classic: bool = True, now: datetime | None = None) -> list[dict]:
    """schema-aware + v7 排除 的生成器 v2（确定性）。"""
    v7_pairs = {(str(r.get("card")), str(r.get("op"))) for r in v7}
    strategies = list(NEW_STRATEGIES) + (list(STRATEGIES) if include_classic else [])
    ts = now_iso(now)
    out: list[dict] = []
    seen: set[str] = set()

    # 先按卡读一次字段（缓存），避免重复 IO
    field_cache: dict[str, list[str]] = {}

    def fields_of(card: str) -> list[str]:
        if card not in field_cache:
            field_cache[card] = card_fields(card)
        return field_cache[card]

    i = 0
    guard = len(cards) * len(strategies) * 8 + 64
    while len(out) < count and i < guard:
        card = cards[i % len(cards)]
        # 策略按 i 轮转（不能按 i//len(cards)，否则 count < 卡数时只会用到第一种策略）
        strat = strategies[i % len(strategies)]
        tpls = _templates_v2(strat)
        tmpl = tpls[(i // len(strategies)) % len(tpls)]
        op = tmpl["op"]
        flds = fields_of(card)
        if not _op_applicable(op, flds):
            i += 1
            continue
        if (card, op) in v7_pairs:          # 排除 v7 已有组合（提高新颖性）
            i += 1
            continue
        rule = TARGET_RULES[i % len(TARGET_RULES)]
        point = tmpl["point"].format(rule=rule)
        content = json.dumps({"op": op, "point": point, "detail": tmpl["detail"],
                              "target_rule": rule, "target_card": card},
                             ensure_ascii=False, sort_keys=True)
        mid = mutation_id(card, strat, content)
        if mid not in seen:
            seen.add(mid)
            out.append({"mutation_id": mid, "attack_type": strat,
                        "target_rule": rule, "target_card": card,
                        "content": content, "generated_at": ts,
                        "generator": "v2"})
        i += 1
    return out[:count]


# ── 判决预测（621 A2）─────────────────────────────────────────────────────────
# 诚实声明：这里是**预测**，不是真实 gate 判决。原因有二：
#   1) 621 §六.3 硬边界：不跑监工门禁（含 gate --check），仅 ci.yml 语法验证例外；
#   2) 没有「把 mutation 施加到沙箱副本」的 API（620 §九.8 已登记为根本瓶颈），
#      要跑真实 gate 就得改原始卡，而这是硬边界禁止的。
# 预测依据全部来自 v7 既有实测数据（同 card+op → 同 op → 策略先验），可复现、可审计。
V7_PATH = os.path.join(ROOT, "data", "mutation", "full_baseline_v7.json")
STRATEGY_PRIOR = {
    "rule_blind_spot": "blocked",
    "evidence_ambiguity": "blocked",
    "provenance_inconsistency": "blocked",
}


def load_v7(path: str = V7_PATH) -> list[dict]:
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return list((json.load(fh).get("results")) or [])


def _majority(records: list[dict]) -> str | None:
    if not records:
        return None
    counts: dict[str, int] = {}
    for r in records:
        v = str(r.get("verdict"))
        counts[v] = counts.get(v, 0) + 1
    return max(sorted(counts), key=lambda k: counts[k])


def predict_verdict(mutation: dict, v7: list[dict]) -> dict:
    """基于 v7 实测数据的判决预测（确定性）。返回 verdict + basis + confidence。"""
    content = json.loads(mutation["content"])
    card, op = content.get("target_card"), content.get("op")
    strat = mutation.get("attack_type")

    same_card_op = [r for r in v7 if r.get("card") == card and r.get("op") == op]
    v = _majority(same_card_op)
    if v:
        return {"verdict": v, "basis": f"v7 同卡同算子 {card}×{op}（{len(same_card_op)} 条）",
                "confidence": "high"}
    same_op = [r for r in v7 if r.get("op") == op]
    v = _majority(same_op)
    if v:
        return {"verdict": v, "basis": f"v7 同算子 {op}（{len(same_op)} 条）",
                "confidence": "medium"}
    if strat in STRATEGY_PRIOR:
        return {"verdict": STRATEGY_PRIOR[strat], "basis": f"策略先验 {strat}",
                "confidence": "low"}
    return {"verdict": "infra_error", "basis": "无任何 v7 依据", "confidence": "none"}


def verify_batch(mutations: list[dict], v7: list[dict]) -> dict:
    """对一批 mutation 做判决预测并汇总。"""
    rows = []
    for m in mutations:
        p = predict_verdict(m, v7)
        rows.append({**m, "predicted_verdict": p["verdict"],
                     "basis": p["basis"], "confidence": p["confidence"]})
    dist: dict[str, int] = {}
    for r in rows:
        dist[r["predicted_verdict"]] = dist.get(r["predicted_verdict"], 0) + 1
    return {
        "rows": rows,
        "distribution": dict(sorted(dist.items())),
        "total": len(rows),
        # 真逃逸 = predicted escaped（本工具不做 equivalent 判定，如实为 0）
        "new_escapes": [r["mutation_id"] for r in rows if r["predicted_verdict"] == "escaped"],
        "note": "预测值，非真实 gate 判决（621 §六.3 不跑门禁 + 无沙箱施加 API）",
    }


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    cards = ["atoms/mem/ATOM-MEM-LEAK-001.md", "evidence/conc/EV-CONC-001.md"]
    chk("空输入返回空", generate([], count=10) == [])
    chk("count<=0 返回空", generate(cards, count=0) == [])
    single = generate(cards, count=6, strategy="rule_blind_spot")
    chk("单策略可生成", len(single) == 6 and all(x["attack_type"] == "rule_blind_spot" for x in single))
    # generated_at 是唯一非确定性字段（默认取当前时间）；幂等性用固定 now 验证
    ts = datetime(2026, 9, 22, tzinfo=timezone.utc)
    multi = generate(cards, count=9, strategy="all", now=ts)
    chk("多策略覆盖 3 种", {x["attack_type"] for x in multi} == set(STRATEGIES))
    chk("去重：mutation_id 唯一", len({x["mutation_id"] for x in multi}) == len(multi))
    chk("格式全部合法", all(validate_record(x) == [] for x in multi))
    chk("确定性/幂等：同输入同输出（固定 now）", generate(cards, count=9, now=ts) == multi)
    chk("generated_at 为 ISO 时间戳", all(x["generated_at"].startswith("2026-09-22") for x in multi))
    chk("记录字段齐全",
        all(set(x) >= {"mutation_id", "attack_type", "target_rule",
                       "target_card", "content", "generated_at"} for x in multi))
    chk("安全护栏：受控目录写入被拒", not is_safe_path(os.path.join(ROOT, "atoms/x.jsonl")))
    chk("安全护栏：data/mutation 允许", is_safe_path(os.path.join(ROOT, "data/mutation/a.jsonl")))
    try:
        write_jsonl(multi, os.path.join(ROOT, "evidence/bad.jsonl"))
        chk("写入受控目录抛错", False)
    except ValueError:
        chk("写入受控目录抛错", True)
    chk("未知策略抛错", _raises(lambda: generate(cards, count=1, strategy="bogus")))

    v7 = [{"card": cards[0], "op": "M1", "verdict": "blocked"},
          {"card": cards[0], "op": "M1", "verdict": "escaped"},
          {"card": "other.md", "op": "M6", "verdict": "blocked"}]
    vb = verify_batch(multi, v7)
    chk("verify_batch 条数一致", vb["total"] == len(multi))
    chk("预测分布键合法",
        set(vb["distribution"]) <= {"blocked", "escaped", "n_a", "infra_error"})
    chk("预测含依据与置信度", all(r["basis"] and r["confidence"] for r in vb["rows"]))
    print(f"A1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _raises(fn) -> bool:
    try:
        fn()
        return False
    except ValueError:
        return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 A1 对抗性 mutation 生成器（只生成，不验证）")
    ap.add_argument("--strategy", default="all", choices=("all", *STRATEGIES))
    ap.add_argument("--count", type=int, default=50)
    ap.add_argument("--output", help="输出 JSONL（只允许 data/mutation/ 或临时目录）")
    ap.add_argument("--cards", help="卡清单文件（每行一个相对路径）；不给则自动发现全量 83 张")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    if args.cards:
        with open(args.cards, encoding="utf-8") as fh:
            cards = [ln.strip() for ln in fh if ln.strip()]
    else:
        sys.path.insert(0, HERE)
        import pck_batch_migrator_620 as M  # noqa: PLC0415
        cards = M.discover_cards()

    items = generate(cards, count=args.count, strategy=args.strategy)
    if args.output:
        write_jsonl(items, args.output)
        print(json.dumps({"generated": len(items), "strategy": args.strategy,
                          "output": args.output}, ensure_ascii=False))
    else:
        for it in items:
            print(json.dumps(it, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
