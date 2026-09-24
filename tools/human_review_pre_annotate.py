#!/usr/bin/env python3
"""人审预标注：读取 388 条候选边，按 MIS 组聚合，给出 approve/reject/modify 建议"""
import sys
import json
from collections import defaultdict
from pathlib import Path

REPO = Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible")
EDGES_FILE = REPO / "data" / "attack_edges_609.json"
OUTPUT_FILE = REPO / "data" / "human_review_pre_annotation_609.md"

def load_edges():
    edges = []
    with open(EDGES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                edges.append(json.loads(line))
    return edges

def classify_evidence(evidence: str) -> tuple:
    """根据 evidence 文本给出人审建议和理由"""
    if not evidence or len(evidence) < 20:
        return "reject", "证据过短或为空，无法判断攻击是否成立"
    
    # 有具体技术细节的信号
    strong_signals = [
        "实测", "GCC", "libstdc++", "libc++", "MSVC", "C++ 标准", "标准明文",
        "未定义行为", "UB", "编译期", "运行时", "漏报", "误报",
        "可移植性", "工具链", "版本", "差异", "不一致",
        "delete", "= delete", "deprecated", "移除", "弃用",
        "happens-before", "内存序", "原子操作", "数据竞争", "死锁",
        "所有权", "转移", "拷贝", "移动", "引用", "悬垂",
        "const", "constexpr", "noexcept", "override", "final",
        "模板", "泛型", "SFINAE", "Concepts", "Ranges",
        "RAII", "智能指针", "unique_ptr", "shared_ptr", "auto_ptr",
        "STL", "容器", "迭代器", "算法",
        "异常", "异常安全", "栈展开",
        "多态", "虚函数", "vtable", "RTTI",
        "内存", "泄漏", "分配", "释放", "对齐",
        "并发", "线程", "互斥", "条件变量", "future",
        "协程", "coroutine", "co_await", "co_yield",
        "模块", "module", "import", "export",
        "反射", "reflection", "元编程", "metaprogramming",
    ]
    
    # 弱证据信号（太笼统、可能是误解）
    weak_signals = [
        "一般来说", "通常", "大概", "可能", "也许", "似乎",
        "大家都知道", "众所周知", "显然", "当然",
        "不好", "不好用", "很差", "很烂", "垃圾",
        "不要用", "别用", "永远不要", "绝对不要",
        "过时", "老旧", "淘汰",
    ]
    
    strong_count = sum(1 for s in strong_signals if s in evidence)
    weak_count = sum(1 for s in weak_signals if s in evidence)
    
    # 有具体实测数据或标准引用
    has_measurement = any(x in evidence for x in ["实测", "测试", "验证", "复现", "对比"])
    has_standard = any(x in evidence for x in ["C++ 标准", "标准规定", "标准明文", "ISO", "标准说"])
    has_compiler = any(x in evidence for x in ["GCC", "Clang", "MSVC", "libstdc++", "libc++"])
    
    # 决策逻辑
    if strong_count >= 3 and weak_count == 0:
        suggestion = "approve"
        reason = f"证据充分（{strong_count}个强信号，含{'实测数据' if has_measurement else ''}{'标准引用' if has_standard else ''}{'编译器验证' if has_compiler else ''}），攻击成立可信度高"
    elif strong_count >= 2 and weak_count <= 1:
        suggestion = "approve"
        reason = f"证据较充分（{strong_count}个强信号），建议approve，可信度medium"
    elif strong_count >= 1 and weak_count == 0:
        suggestion = "modify"
        reason = f"证据有一定支撑（{strong_count}个强信号）但不够充分，建议modify为medium，需进一步验证"
    elif weak_count >= 2:
        suggestion = "reject"
        reason = f"证据薄弱（{weak_count}个弱信号），措辞笼统缺乏具体技术细节，建议reject"
    else:
        suggestion = "modify"
        reason = f"证据一般（{strong_count}个强信号/{weak_count}个弱信号），建议modify为low待进一步验证"
    
    return suggestion, reason.strip("，")

def main():
    edges = load_edges()
    print(f"加载 {len(edges)} 条边")
    
    # 只处理 mis_to_prop 的边（MIS 攻击命题，人审重点）
    mis_to_prop = [e for e in edges if e["direction"] == "mis_to_prop"]
    prop_to_mis = [e for e in edges if e["direction"] == "prop_to_mis"]
    print(f"mis_to_prop: {len(mis_to_prop)} 条（人审重点）")
    print(f"prop_to_mis: {len(prop_to_mis)} 条（对称边，W2自动击败，人审价值低）")
    
    # 按 MIS 组聚合
    by_mis = defaultdict(list)
    for e in mis_to_prop:
        mis_id = e["source"]
        by_mis[mis_id].append(e)
    
    print(f"唯一 MIS 组: {len(by_mis)} 个")
    
    # 生成预标注
    suggestions = {"approve": 0, "reject": 0, "modify": 0}
    pre_annotations = []
    
    for mis_id in sorted(by_mis.keys()):
        group_edges = by_mis[mis_id]
        for e in group_edges:
            suggestion, reason = classify_evidence(e["evidence"])
            suggestions[suggestion] += 1
            pre_annotations.append({
                "edge_id": e["id"],
                "mis_id": mis_id,
                "prop_id": e["target"],
                "evidence_preview": e["evidence"][:120] + ("..." if len(e["evidence"]) > 120 else ""),
                "suggestion": suggestion,
                "confidence": "high" if suggestion == "approve" else ("medium" if suggestion == "modify" else "low"),
                "reason": reason,
            })
    
    # 生成 Markdown 报告
    lines = []
    lines.append("# 人审预标注报告（609 批次辅助）")
    lines.append("")
    lines.append("> **声明**：本报告由 AI 预标注生成，仅作人审辅助参考，**不构成最终人审决策**。")
    lines.append("> 最终人审必须由人确认后通过 `human_review_cli.py` 执行，reviewer 必须为 `human`。")
    lines.append("> AI 预标注的建议基于 evidence 文本的信号强度分析，可能存在误判，请逐条核实。")
    lines.append("")
    lines.append("## 统计概览")
    lines.append("")
    lines.append(f"- 总候选边：{len(edges)} 条")
    lines.append(f"- mis_to_prop（人审重点）：{len(mis_to_prop)} 条")
    lines.append(f"- prop_to_mis（对称边，W2自动击败）：{len(prop_to_mis)} 条")
    lines.append(f"- 唯一 MIS 组：{len(by_mis)} 个")
    lines.append("")
    lines.append("### AI 预标注建议分布（仅 mis_to_prop 194 条）")
    lines.append("")
    lines.append("| 建议 | 数量 | 占比 | 说明 |")
    lines.append("|---|---:|---:|---|")
    total = len(mis_to_prop)
    lines.append(f"| approve | {suggestions['approve']} | {suggestions['approve']/total*100:.1f}% | 证据充分，建议确认攻击成立 |")
    lines.append(f"| modify | {suggestions['modify']} | {suggestions['modify']/total*100:.1f}% | 证据一般，建议调整权重待验证 |")
    lines.append(f"| reject | {suggestions['reject']} | {suggestions['reject']/total*100:.1f}% | 证据薄弱，建议拒绝攻击 |")
    lines.append("")
    lines.append("## 按 MIS 组逐条预标注")
    lines.append("")
    
    for mis_id in sorted(by_mis.keys()):
        group_edges = by_mis[mis_id]
        group_pre = [p for p in pre_annotations if p["mis_id"] == mis_id]
        approve_count = sum(1 for p in group_pre if p["suggestion"] == "approve")
        modify_count = sum(1 for p in group_pre if p["suggestion"] == "modify")
        reject_count = sum(1 for p in group_pre if p["suggestion"] == "reject")
        
        lines.append(f"### {mis_id}（{len(group_edges)} 条边）")
        lines.append("")
        lines.append(f"预标注分布：approve {approve_count} / modify {modify_count} / reject {reject_count}")
        lines.append("")
        lines.append("| edge_id | 目标命题 | 证据预览 | AI建议 | 理由 |")
        lines.append("|---|---|---|---|---|")
        for p in group_pre:
            evidence = p["evidence_preview"].replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {p['edge_id']} | {p['prop_id']} | {evidence} | **{p['suggestion']}** | {p['reason']} |")
        lines.append("")
    
    lines.append("## 一键执行脚本（人确认后使用）")
    lines.append("")
    lines.append("确认以上预标注后，可以用以下命令批量执行：")
    lines.append("")
    lines.append("```bash")
    lines.append("# 仅执行 approve 建议（需逐条确认后取消注释）")
    lines.append("# for edge in $(grep 'approve' data/human_review_pre_annotation_609.md | grep -o 'ae-[^|]*' | head -1); do")
    lines.append("#   .venv/Scripts/python.exe tools/human_review_cli.py approve \"$edge\" --reason \"AI预标注approve，人审确认\"")
    lines.append("# done")
    lines.append("```")
    lines.append("")
    lines.append("**注意**：不建议直接批量执行，应逐条核实后执行。AI 预标注的误判率未知，需人审把关。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*生成时间：2026-09-20 | 生成工具：AI 预标注脚本 | 数据来源：data/attack_edges_609.json（388条）*")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    
    print(f"\n预标注报告已生成：{OUTPUT_FILE}")
    print(f"approve: {suggestions['approve']}, modify: {suggestions['modify']}, reject: {suggestions['reject']}")

if "--check" in sys.argv:
    print("OK: human_review_pre_annotate --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)

if __name__ == "__main__":
    main()
