"""629 B2 · 历史攻击映射（纯标准库，只读）

把 603–629 各批次报告中**已经真实发生**的攻击/漏洞事件，逐条映射到 B1 的攻击面向量编号，
并标注修复批次与当前状态。目的：把「分类学」变成「有历史命中的地图」——
零命中的向量 = 未验证的假设面（B3 据此排优先级）。

数据来源（人工摘录，逐条给证据）：各批验收报告（`data/*_acceptance_report*.md`）、
`_arch_v19/`–`_arch_v22/` 调研（只读引用，不修改）、629 任务0 基线台账。

状态口径：`已修`（有工具/测试锁住）/ `部分修`（有处置但未闭合）/ `未修`（仅登记，待裁决）。
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "attack_mapping_629.md")
VALID_STATUS = ("已修", "部分修", "未修")

# (事件 id, 名称, 攻击面向量, 修复批次, 状态, 证据来源)
EVENTS: list[tuple[str, str, str, str, str, str]] = [
    ("EV-01", "EV-MATRIX 规则隐性预处理（判据藏在预处理里，绕过条件不可见）",
     "L4.1", "619-620", "已修", "619 A 线 / 620 A 线（EV-MATRIX 显式化）"),
    ("EV-02", "置信序列被连续偷看（CP 用于序贯决策 ⇒ 置信度失效）",
     "L6.2", "616", "已修", "616 A 线（e-process 修正）"),
    ("EV-03", "warn 成为优化目标（Goodhart 漂移）",
     "L6.1", "616", "部分修", "616 warn 治理 + Goodhart 登记"),
    ("EV-04", "388 条一次性批量授权（人审名存实亡）",
     "L7.1", "622 D1 → 626 A3", "已修", "626 A3（review_method 五级 + decision_origin 四级）"),
    ("EV-05", "194 条镜像边 symmetry_proof_id=null（把镜像当独立证据）",
     "L7.3", "627 A4 → 628 A3", "部分修", "628 A3（76 自动证明入账 + 118 sidecar 待治理）"),
    ("EV-06", "VSA 验证端 import 签发端（同源耦合 ⇒ 签发写错验证也错）",
     "L5.2", "628 → 629 C3", "已修", "628 E1 前置修复 + 629 C3 静态证明"),
    ("EV-07", "83 张 PCK hash 与证据文件不匹配（内容漂移）",
     "L2.1", "627 A3 → 628 A2", "已修", "628 A2（82 张重算/补 hash + 1 张需人审）"),
    ("EV-08", "CI 中 gate 先于 replay 完成（读方先于写方 ⇒ 假红/假绿）",
     "L4.5", "622 B2 → 624 C2", "已修", "ci.yml needs:[replay] 强制序 + 622 B2 实测"),
    ("EV-09", "PE 时间戳口径不可复现（同一产物两次生成不同时间戳）",
     "L8.1", "611", "部分修", "611 专项（PE 时间戳口径冻结）"),
    ("EV-10", "W2 求解器归一化缺陷（519 节点 vs 正确 121 节点，双实现同错）",
     "L5.1", "627 A1", "已修", "627 A1（W2 归一化 519→121，diff=0）"),
    ("EV-11", "51 条 REPLACE 事件引用旧式 decision id（无法溯源到被替代事件）",
     "L8.5", "626 C2 → 627 A2", "已修", "627 A2（supersedes ID 重映射 legacy34+dec17）"),
    ("EV-12", "PCK 严格/宽松双策略都是 0 authorized（验证范围与口径缺口）",
     "L5.4", "626 D2/E1", "已修", "626 D2 投影双策略 + E1 四层验证"),
    ("EV-13", "治理 manifest 未同步（CI pytest 假红）",
     "L6.4", "623 B1", "已修", "623 B1（manifest 重签 + tool_integrity 重钉）"),
    ("EV-14", "626 报告四处数值错误（median 75→67.5、110→93 等）",
     "L6.4", "626 A1", "已修", "626 A1（数值按实测更正）"),
    ("EV-15", "622 23/50 条 infra_error（生成器不查卡实际字段 ⇒ 探针覆盖缺口）",
     "L5.4", "622 A4", "已修", "622 A4（生成器 v2 schema-aware，可施加率 54%→83%）"),
    ("EV-16", "先验预测口径不可靠（v7 预测与真跑一致率 51.85%）",
     "L6.3", "622 A2", "部分修", "622 A2（改为真跑 gate，不再依赖预测）"),
    ("EV-17", "Verification Horizon 指标不敏感（恒 60-80，检出 0% 断崖）",
     "L6.1", "622 E1", "部分修", "622 E1（改用最低桶检出率）"),
    ("EV-18", "56 张 evidence.hash 与当前文件不匹配（626 首次发现）",
     "L2.1", "626 E1", "已修", "626 E1 只验证不修改 → 628 A2 处置"),
    ("EV-19", "warn 层 100% 命中已验证卡（warn 不可当质量评级）",
     "L6.3", "629 A1", "未修", "629 A1 实测（23/23 被 warn，分桶 1 硬缺陷 + 22 口径）"),
    ("EV-20", "1 张 verified 卡存在悬空 relation 目标（ATOM-UB-GRAY-001）",
     "L2.2", "629 A1", "未修", "629 A1 报告（ATOM-REL-TARGET×2：ATOM-UB-ALIAS-001 / ATOM-UB-DEF-001）"),
    ("EV-21", "规则触达盲区 31/67（沙箱六轮累计触达 36/67）",
     "L5.4", "623-624", "部分修", "623/624 A 线触达矩阵 + 629 D2 继续"),
    ("EV-22", "19 项全量测试断言过期（状态快照型断言被 628 数据处置打破）",
     "L6.4", "629 任务0", "未修", "629 基线台账 BASELINE_FAILURES（19 项冻结）"),
    ("EV-23", "62 commit 本地领先远程（无法验证 CI 真实绿灯）",
     "L8.5", "629 E1", "未修", "629 E1 push 裁决（不自动 push）"),
]


def events() -> list[dict[str, Any]]:
    import attack_surface_taxonomy as T

    known = {v["id"]: v for v in T.vectors()}
    out = []
    for eid, name, vec, batch, status, src in EVENTS:
        v = known.get(vec, {})
        out.append({"id": eid, "name": name, "vector": vec, "batch": batch,
                    "status": status, "source": src,
                    "layer": vec.split(".")[0], "layer_name": v.get("layer_name", ""),
                    "risk": v.get("risk", ""), "has_probe": bool(v.get("probe"))})
    return out


def stats() -> dict[str, Any]:
    import attack_surface_taxonomy as T

    ev = events()
    by_layer = collections.Counter(e["layer"] for e in ev)
    by_status = collections.Counter(e["status"] for e in ev)
    hit_vectors = {e["vector"] for e in ev}
    vs = T.vectors()
    per_layer = {}
    for layer in T.LAYERS:
        lv = [v for v in vs if v["layer"] == layer]
        per_layer[layer] = {
            "vectors": len(lv),
            "hit_vectors": len({v["id"] for v in lv} & hit_vectors),
            "no_probe": sum(1 for v in lv if not v["covered"]),
            "events": by_layer.get(layer, 0),
        }
    return {"events": len(ev), "by_layer": dict(by_layer),
            "by_status": dict(by_status), "per_layer": per_layer,
            "hit_vectors": len(hit_vectors), "zero_hit_vectors":
            sorted(v["id"] for v in vs if v["id"] not in hit_vectors)}


def write_report() -> str:
    import attack_surface_taxonomy as T

    ev, st = events(), stats()
    lines = [
        "# 629 B2 · 历史攻击映射（分类学 × 真实命中）", "",
        "> 工具：`tools/attack_mapping_629.py`（纯标准库，只读；数据为人工摘录 + 逐条证据）",
        f"> 事件：**{st['events']} 条**（603–629）· 命中向量 {st['hit_vectors']}/{len(T.vectors())} · "
        f"状态分布 {st['by_status']}", "",
        "## 一、事件 → 攻击面向量 → 修复批次 → 状态", "",
        "| 事件 | 描述 | 向量 | 层 | risk | 修复批次 | 状态 | 证据 |",
        "|---|---|---|---|---|---|---|---|",
        *[f"| {e['id']} | {e['name']} | `{e['vector']}` | {e['layer']} | {e['risk']} | "
          f"{e['batch']} | {e['status']} | {e['source']} |" for e in ev], "",
        "## 二、按层统计", "",
        "| 层 | 向量数 | 有事件的向量 | 零命中向量 | 零探针向量 | 事件数 |",
        "|---|---|---|---|---|---|",
        *[f"| {k} {T.LAYERS[k].split('（')[0]} | {v['vectors']} | {v['hit_vectors']} | "
          f"{v['vectors'] - v['hit_vectors']} | {v['no_probe']} | {v['events']} |"
          for k, v in st["per_layer"].items()], "",
        "## 三、结论", "",
        f"- **历史命中集中在 {sorted(st['by_layer'], key=lambda x: -st['by_layer'][x])[:3]}**"
        "：说明阙疑过去的攻击与修复主要围绕这几层展开。",
        f"- **零命中向量 {len(st['zero_hit_vectors'])} 个**："
        f"{'、'.join('`' + x + '`' for x in st['zero_hit_vectors'])}",
        "  零命中 ≠ 无风险，而是**从未被主动攻击过**（未验证的假设面）⇒ B3 排优先级。",
        f"- 状态：{st['by_status'].get('已修', 0)} 已修 / {st['by_status'].get('部分修', 0)} "
        f"部分修 / {st['by_status'].get('未修', 0)} 未修。未修项已进交人清单。", "",
        "## 四、局限", "",
        "- 事件清单是**人工摘录**（来自验收报告与调研），不做穷尽保证；漏摘会导致某向量"
        "被误判为「零命中」。",
        "- 一个事件只映射到一个向量（最贴切的那个），因此层内事件数会被**低估**"
        "（真实攻击常跨层，如 EV-05 同时涉 L7.3 与 L8.5）。",
        "- 事件在 629 之后仍会增加，本表是**时点快照**。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    import attack_surface_taxonomy as T

    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    ev, st = events(), stats()
    known = {v["id"] for v in T.vectors()}
    chk(f"事件 ≥ 15 条（实测 {len(ev)}）", len(ev) >= 15)
    chk("事件 id 唯一", len({e["id"] for e in ev}) == len(ev))
    chk("全部映射到 B1 已知向量", all(e["vector"] in known for e in ev),
        f"({[e['vector'] for e in ev if e['vector'] not in known]})")
    chk("状态取值合法", all(e["status"] in VALID_STATUS for e in ev),
        f"({set(e['status'] for e in ev) - set(VALID_STATUS)})")
    chk("每条都有修复批次与证据", all(e["batch"] and e["source"] for e in ev))
    chk("覆盖 ≥ 5 层（映射不集中于单层）", len(st["by_layer"]) >= 5,
        f"({sorted(st['by_layer'])})")
    chk("报告存在且含按层统计", os.path.exists(OUT_MD)
        and "按层统计" in open(OUT_MD, encoding="utf-8").read())
    print(f"B2 attack mapping check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 B2 历史攻击映射（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写 data/attack_mapping_629.md")
    ap.add_argument("--json", action="store_true", help="打印事件 JSON")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.json:
        print(json.dumps({"events": events(), "stats": stats()},
                         ensure_ascii=False, indent=2))
        return 0
    if args.report:
        print(f"written {write_report()}")
        return 0
    st = stats()
    print(f"events={st['events']} hit_vectors={st['hit_vectors']} "
          f"zero_hit={len(st['zero_hit_vectors'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
