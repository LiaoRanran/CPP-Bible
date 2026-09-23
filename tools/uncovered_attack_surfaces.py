"""629 B3 · 未覆盖攻击面清单与优先级（纯标准库，只读）

基于 B1（分类学，35 向量）+ B2（历史命中，23 事件），挑出**零历史事件的向量**，
并按「风险 + 是否已有探针」打分排序，给出**建议探针设计**（只写设计，不实现）。

优先级打分（显式定义，可复核）：
    score = risk_weight(high=3/medium=2/low=1) + (2 if 无探针) + (2 if 零事件)
    P0: score ≥ 7（高危 + 零探针 + 零命中）· P1: 5-6 · P2: ≤ 4

`--check` 只读：重算清单、校验优先级与打分一致、校验 P0 确为高危零探针、报告存在。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "uncovered_attack_surfaces.md")
RISK_WEIGHT = {"high": 3, "medium": 2, "low": 1}

# 建议探针设计（只写设计，不实现）：vector_id -> (设计, 模式)
# 模式：可自动化 / 人机结合 / 需人审
DESIGN: dict[str, tuple[str, str]] = {
    "L1.2": ("收 30 条含模糊指代的命题，让两个独立复核者（或两次独立 LLM 抽取）各自填"
             "「命题指向的对象」，统计指向不一致率；不一致率 > 20% ⇒ 命题不合格，"
             "应在写入侧强制消解指代", "人机结合"),
    "L1.1": ("对每条命题做「语义等价改写」双向测试：改写后判据应给出同一判决；"
             "不一致即判据依赖表面形式（可复用 mutation_fuzz 的等价算子，加断言）", "可自动化"),
    "L1.3": ("命题↔卡标题/证据范围一致性静态检查：claim 的量词（单核/多核、∀/∃）"
             "与 evidence 的测量条件比对", "可自动化"),
    "L1.4": ("建「命题→证据」双射表，凡一个证据卡服务多于 1 个命题（或反之）即列"
             "待核查清单；对 OBSERVATION-LIVENESS 的命题级活性锚做覆盖率统计", "可自动化"),
    "L2.3": ("给每条 evidence 引用加「有效期/上游版本」字段，做一个陈旧度扫描器："
             "上游卡 revision 变化但引用未更新即告警", "可自动化"),
    "L2.4": ("造 20 份「格式完全合规但内容编造」的证据（如不存在的测量、伪造的实验日志），"
             "看 gate 能否区分「格式合规」与「事实可核」——预期不能，用于量化内容层盲区",
             "人机结合"),
    "L3.1": ("对同一文本生成合法 YAML 的多种等价写法（引号/折行/flow/锚点），"
             "断言解析结果与 gate 判决一致（629 A2 已覆盖 5 类，可扩展到锚点/多文档）",
             "可自动化"),
    "L3.2": ("直接用 629 A2 的格式微扰探针（20 次实测零假阳性，结论已在册）；"
             "后续每批新规则上线时复跑，防止新正则引入误伤", "可自动化"),
    "L3.3": ("字段注入用例集：控制字符 / 超长值 / 嵌套深度 / Unicode 同形字，"
             "验证解析与展示一致（626 A2 已清洗 339 控制字符，需常态化探针）", "可自动化"),
    "L3.4": ("YAML 锚点/别名/多文档/标签（!!python）绕过探针：构造 10 类特性文件，"
             "断言解析器与真实 PyYAML 结果一致（gate 已有 EV-FM-YAML-HARDENING，"
             "可做反向用例）", "可自动化"),
    "L4.2": ("边界值差分：对每条含阈值/计数的规则，取 n-1/n/n+1 三个样本跑判决，"
             "断言判决单调且边界写明（> 还是 ≥）", "可自动化"),
    "L4.3": ("同义异形词表扩张：为每条关键词规则准备 10 个同义替换，测绕过率；"
             "绕过率 > 30% ⇒ 规则应改为结构化判据而非关键词", "可自动化"),
    "L4.4": ("规则冲突检测：两两规则在同一输入上给出矛盾判决时列冲突对清单，"
             "并要求写明优先级", "可自动化"),
    "L5.3": ("工具完整性攻击演练：临时改一个尺子覆盖的工具体，断言 tool_integrity --check "
             "能捕获；同时统计「哪些工具未被任何尺子覆盖」（覆盖缺口清单）", "人机结合"),
    "L7.2": ("人审理由的文本相似度扫描：批量授权条目中理由互相高度相似（> 0.9）即告警，"
             "作为模板化人审的代理指标", "可自动化"),
    "L7.4": ("Blind Review 的 rubber-stamp 检测：统计每位人审者的「平均耗时 / 决策分布 / "
             "与 AI 推荐一致率」，异常一致或异常快即标记（627 C1 已有 Pass A 盲性基础）",
             "人机结合"),
    "L7.5": ("抽查覆盖率审计：按歧义度分层抽样，检查「低歧义」组的实际人审覆盖率——"
             "若为 0 则该层从未被检查", "可自动化"),
    "L8.2": ("密钥泄露演练：模拟密钥丢失/被替换，断言（a）历史凭证不被误判为篡改"
             "（628 B2 已修）；（b）伪造凭证可被检测；（c）密钥轮换有审计轨迹",
             "人机结合"),
    "L8.3": ("透明日志攻击集：删除中段条目 / 重放旧条目 / 替换整段链，断言 verify_log "
             "与 inclusion 全部检出（628 B3 已有篡改/删除检测，重放未测）", "可自动化"),
    "L8.4": ("替身日志检测：用第二份自建日志冒充「已入册」证据，检查现有流程是否会发现"
             "「同一凭证存在两份不同日志」——预期发现不了（无外部见证者）⇒ 需人裁决"
             "是否接外部锚（OTS/Rekor）", "需人审"),
}


def score(v: dict[str, Any], zero_event: bool) -> int:
    return (RISK_WEIGHT[v["risk"]] + (2 if not v["covered"] else 0)
            + (2 if zero_event else 0))


def priority(s: int) -> str:
    return "P0" if s >= 7 else ("P1" if s >= 5 else "P2")


def uncovered() -> list[dict[str, Any]]:
    import attack_mapping_629 as M
    import attack_surface_taxonomy as T

    zero = set(M.stats()["zero_hit_vectors"])
    out = []
    for v in T.vectors():
        if v["id"] not in zero:
            continue
        s = score(v, True)
        design, mode = DESIGN.get(v["id"], ("（未登记设计——需补）", "需人审"))
        out.append({**v, "zero_event": True, "score": s, "priority": priority(s),
                    "design": design, "mode": mode})
    return sorted(out, key=lambda x: (-x["score"], x["id"]))


def write_report() -> str:
    import attack_surface_taxonomy as T

    items = uncovered()
    by_p: dict[str, list[dict[str, Any]]] = {"P0": [], "P1": [], "P2": []}
    for it in items:
        by_p[it["priority"]].append(it)
    lines = [
        "# 629 B3 · 未覆盖攻击面清单与优先级", "",
        "> 工具：`tools/uncovered_attack_surfaces.py`（纯标准库，只读；**只写设计不实现**）",
        f"> 依据：B1 分类学 {len(T.vectors())} 向量 × B2 历史命中 23 事件 ⇒ "
        f"**零事件向量 {len(items)} 个**", "",
        "## 一、优先级打分口径", "",
        "```",
        "score = risk_weight(high=3/medium=2/low=1) + (无探针 +2) + (零事件 +2)",
        "P0: score ≥ 7（高危 + 零探针 + 零命中）· P1: 5-6 · P2: ≤ 4",
        "```", "",
        "零事件 ≠ 无风险，而是**从未被主动攻击过**（未验证的假设面）。"
        "P0 = 高危且连探针都没有——这些是「已知的未知」。", "",
    ]
    for p in ("P0", "P1", "P2"):
        lines += [f"## 二{'一二三'[('P0', 'P1', 'P2').index(p)]}、{p}（{len(by_p[p])} 个）", ""]
        if not by_p[p]:
            lines += ["（空）", ""]
            continue
        lines += ["| 向量 | 层 | 名称 | risk | 有探针 | score | 建议探针设计 | 模式 |",
                  "|---|---|---|---|---|---|---|---|",
                  *[f"| `{i['id']}` | {i['layer']} | {i['name']} | {i['risk']} | "
                    f"{'✔' if i['covered'] else '✘'} | {i['score']} | {i['design']} | "
                    f"{i['mode']} |" for i in by_p[p]], ""]
    auto = sum(1 for i in items if i["mode"] == "可自动化")
    lines += [
        "## 三、模式统计与建议", "",
        f"- 可自动化 {auto} 个 · 人机结合 {sum(1 for i in items if i['mode'] == '人机结合')} 个 · "
        f"需人审 {sum(1 for i in items if i['mode'] == '需人审')} 个",
        f"- **P0 优先落地建议**：{'、'.join('`' + i['id'] + '`' for i in by_p['P0']) or '无'}"
        "（高危且零探针，建议下一批直接实现）",
        "- 需人审项（如 `L8.4` 透明日志外部锚）涉及信任根选择，机器不能自行决定，"
        "已进交人清单。", "",
        "## 四、局限", "",
        "- 优先级基于**主观 risk 分级 + 探针有无**，不含利用难度/后果的定量估计；",
        "- 「零事件」依赖 B2 的人工摘录完整性（漏摘会误判为未覆盖）；",
        "- 本工具只给设计，不实现——按 §三 的建议实现需下一批排期。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    import attack_mapping_629 as M
    import attack_surface_taxonomy as T

    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    items, zero = uncovered(), set(M.stats()["zero_hit_vectors"])
    hit = {e["vector"] for e in M.events()}
    chk("清单与 B2 零事件集一致",
        {i["id"] for i in items} == zero, f"({len(items)} vs {len(zero)})")
    chk("清单里没有有事件的向量", not ({i["id"] for i in items} & hit))
    chk("score 与打分函数一致",
        all(i["score"] == score(i, True) for i in items))
    chk("priority 与 score 门槛一致",
        all(i["priority"] == priority(i["score"]) for i in items))
    p0 = [i for i in items if i["priority"] == "P0"]
    chk("P0 确为高危 + 零探针", all(i["risk"] == "high" and not i["covered"] for i in p0),
        f"({[i['id'] for i in p0]})")
    chk("每个未覆盖向量都有探针设计",
        all(i["design"] and i["design"] != "（未登记设计——需补）" for i in items),
        f"({[i['id'] for i in items if i['design'].startswith('（未登记')]})")
    chk("模式取值合法",
        all(i["mode"] in ("可自动化", "人机结合", "需人审") for i in items))
    chk("报告存在且含三档优先级", os.path.exists(OUT_MD)
        and all(k in open(OUT_MD, encoding="utf-8").read() for k in ("P0", "P1", "P2")))
    chk("B1 层数完整（参照）", len(T.LAYERS) == 8)
    print(f"B3 uncovered surfaces check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 B3 未覆盖攻击面（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写 data/uncovered_attack_surfaces.md")
    ap.add_argument("--json", action="store_true", help="打印清单 JSON")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.json:
        print(json.dumps(uncovered(), ensure_ascii=False, indent=2))
        return 0
    if args.report:
        print(f"written {write_report()}")
        return 0
    items = uncovered()
    print(f"uncovered={len(items)} " + " ".join(
        f"{p}={sum(1 for i in items if i['priority'] == p)}" for p in ("P0", "P1", "P2")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
