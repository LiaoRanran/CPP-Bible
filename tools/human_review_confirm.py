#!/usr/bin/env python3
"""交互式人审确认工具：基于 AI 预标注报告，让人逐条确认后保存决策。
不直接写入 annotations（等 609 human_review_cli.py 完成后再批量执行），
只做确认和记录，确保人审权力在人手里。
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible")
PRE_ANNOTATION_FILE = REPO / "data" / "human_review_pre_annotation_609.md"
CONFIRMATION_FILE = REPO / "data" / "human_review_confirmation_609.json"
EDGES_FILE = REPO / "data" / "attack_edges_609.json"

def load_edges():
    """加载 388 条边的完整数据"""
    edges = {}
    with open(EDGES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                e = json.loads(line)
                edges[e["id"]] = e
    return edges

def parse_pre_annotation():
    """从预标注 Markdown 报告中解析每条边的 AI 建议"""
    annotations = []
    current_mis = None
    
    with open(PRE_ANNOTATION_FILE, "r", encoding="utf-8") as f:
        for line in f:
            # 检测 MIS 组标题
            mis_match = re.match(r"^### (MIS-\S+)（(\d+) 条边）", line)
            if mis_match:
                current_mis = mis_match.group(1)
                continue
            
            # 检测表格行（edge_id 开头）
            if line.startswith("| ae-"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 6:
                    edge_id = parts[1]
                    prop_id = parts[2]
                    evidence = parts[3]
                    suggestion = parts[4].replace("**", "")
                    reason = parts[5]
                    annotations.append({
                        "edge_id": edge_id,
                        "mis_id": current_mis,
                        "prop_id": prop_id,
                        "evidence_preview": evidence,
                        "ai_suggestion": suggestion,
                        "ai_reason": reason,
                    })
    return annotations

def load_confirmation():
    """加载已有的确认结果（支持断点续审）"""
    if CONFIRMATION_FILE.exists():
        with open(CONFIRMATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"confirmed": {}, "skipped": [], "stats": {"approve": 0, "reject": 0, "modify": 0, "skip": 0}}

def save_confirmation(confirmation):
    """保存确认结果"""
    with open(CONFIRMATION_FILE, "w", encoding="utf-8") as f:
        json.dump(confirmation, f, ensure_ascii=False, indent=2)

def interactive_review():
    """交互式人审"""
    edges = load_edges()
    annotations = parse_pre_annotation()
    confirmation = load_confirmation()
    
    print("=" * 70)
    print("阙疑项目 · 人审确认工具（基于 AI 预标注）")
    print("=" * 70)
    print(f"总候选边（mis_to_prop）：{len(annotations)} 条")
    print(f"已确认：{len(confirmation['confirmed'])} 条")
    print(f"已跳过：{len(confirmation['skipped'])} 条")
    print()
    print("操作说明：")
    print("  y = approve（确认攻击成立，可信度升一级）")
    print("  n = skip（跳过本条，稍后再审）")
    print("  m = modify（调整可信度为 medium，不升为 high）")
    print("  r = reject（拒绝攻击，不采纳此边）")
    print("  a = approve all in this MIS group（批准当前 MIS 组全部）")
    print("  s = show evidence（显示完整 evidence）")
    print("  q = quit（保存并退出，支持断点续审）")
    print("=" * 70)
    print()
    
    # 按 MIS 组聚合
    by_mis = {}
    for a in annotations:
        mis = a["mis_id"]
        if mis not in by_mis:
            by_mis[mis] = []
        by_mis[mis].append(a)
    
    total_confirmed = 0
    for mis_id in sorted(by_mis.keys()):
        group = by_mis[mis_id]
        
        # 检查是否全部已确认
        unconfirmed = [a for a in group if a["edge_id"] not in confirmation["confirmed"] and a["edge_id"] not in confirmation["skipped"]]
        if not unconfirmed:
            continue
        
        print(f"\n{'='*70}")
        print(f"MIS 组：{mis_id}（{len(group)} 条边，{len(unconfirmed)} 条待审）")
        print(f"{'='*70}")
        
        # 显示组内所有边
        for i, a in enumerate(group):
            status = ""
            if a["edge_id"] in confirmation["confirmed"]:
                status = f" [已确认: {confirmation['confirmed'][a['edge_id']]['decision']}]"
            elif a["edge_id"] in confirmation["skipped"]:
                status = " [已跳过]"
            
            ai_sug = a["ai_suggestion"]
            ai_color = {"approve": "✓", "modify": "~", "reject": "✗"}.get(ai_sug, "?")
            print(f"  {i+1}. {ai_color} AI建议={ai_sug} | {a['edge_id']}{status}")
            print(f"     目标：{a['prop_id']}")
            print(f"     证据：{a['evidence_preview'][:80]}...")
            print(f"     理由：{a['ai_reason']}")
            print()
        
        # 逐条确认
        for a in unconfirmed:
            if a["edge_id"] in confirmation["confirmed"] or a["edge_id"] in confirmation["skipped"]:
                continue
            
            edge = edges.get(a["edge_id"], {})
            full_evidence = edge.get("evidence", a["evidence_preview"])
            
            print(f"\n--- 审 {a['edge_id']} ---")
            print(f"目标命题：{a['prop_id']}")
            print(f"AI 建议：{a['ai_suggestion']}（{a['ai_reason']}）")
            print(f"证据预览：{a['evidence_preview']}")
            
            while True:
                choice = input("\n请选择 [y=approve, n=skip, m=modify, r=reject, a=approve all, s=show full evidence, q=quit]: ").strip().lower()
                
                if choice == "y":
                    confirmation["confirmed"][a["edge_id"]] = {
                        "decision": "approve",
                        "confidence": "high",
                        "reason": "人审确认（AI预标注approve，人审同意）",
                        "mis_id": a["mis_id"],
                        "prop_id": a["prop_id"],
                    }
                    confirmation["stats"]["approve"] += 1
                    total_confirmed += 1
                    print(f"  ✓ 已确认 approve（{confirmation['stats']['approve']} 条）")
                    break
                
                elif choice == "m":
                    confirmation["confirmed"][a["edge_id"]] = {
                        "decision": "modify",
                        "confidence": "medium",
                        "reason": "人审调整为medium（AI预标注approve，人审认为证据不够充分）",
                        "mis_id": a["mis_id"],
                        "prop_id": a["prop_id"],
                    }
                    confirmation["stats"]["modify"] += 1
                    total_confirmed += 1
                    print(f"  ~ 已确认 modify→medium（{confirmation['stats']['modify']} 条）")
                    break
                
                elif choice == "r":
                    confirmation["confirmed"][a["edge_id"]] = {
                        "decision": "reject",
                        "confidence": "low",
                        "reason": "人审拒绝（AI预标注approve，人审认为攻击不成立）",
                        "mis_id": a["mis_id"],
                        "prop_id": a["prop_id"],
                    }
                    confirmation["stats"]["reject"] += 1
                    total_confirmed += 1
                    print(f"  ✗ 已确认 reject（{confirmation['stats']['reject']} 条）")
                    break
                
                elif choice == "n":
                    confirmation["skipped"].append(a["edge_id"])
                    confirmation["stats"]["skip"] += 1
                    print(f"  → 已跳过（{confirmation['stats']['skip']} 条）")
                    break
                
                elif choice == "a":
                    # 批准当前 MIS 组全部未确认的边
                    group_unconfirmed = [x for x in group if x["edge_id"] not in confirmation["confirmed"] and x["edge_id"] not in confirmation["skipped"]]
                    for x in group_unconfirmed:
                        confirmation["confirmed"][x["edge_id"]] = {
                            "decision": "approve",
                            "confidence": "high",
                            "reason": f"人审批量批准（MIS组 {mis_id} 全部批准）",
                            "mis_id": x["mis_id"],
                            "prop_id": x["prop_id"],
                        }
                        confirmation["stats"]["approve"] += 1
                        total_confirmed += 1
                    print(f"  ✓✓✓ 已批量批准 {len(group_unconfirmed)} 条（MIS组 {mis_id}）")
                    break
                
                elif choice == "s":
                    print(f"\n  完整 evidence（{len(full_evidence)} 字符）：")
                    print(f"  {'-'*60}")
                    print(f"  {full_evidence}")
                    print(f"  {'-'*60}")
                    continue
                
                elif choice == "q":
                    save_confirmation(confirmation)
                    print(f"\n{'='*70}")
                    print(f"已保存并退出。本轮确认 {total_confirmed} 条。")
                    print(f"累计：approve {confirmation['stats']['approve']} / modify {confirmation['stats']['modify']} / reject {confirmation['stats']['reject']} / skip {confirmation['stats']['skip']}")
                    print(f"确认结果已保存到：{CONFIRMATION_FILE}")
                    print("下次运行可断点续审。")
                    print(f"{'='*70}")
                    return
                
                else:
                    print("  无效输入，请重新选择")
                    continue
            
            # 每 10 条自动保存
            if total_confirmed % 10 == 0 and total_confirmed > 0:
                save_confirmation(confirmation)
    
    # 全部审完
    save_confirmation(confirmation)
    print(f"\n{'='*70}")
    print(f"全部审完！累计确认 {len(confirmation['confirmed'])} 条。")
    print(f"approve {confirmation['stats']['approve']} / modify {confirmation['stats']['modify']} / reject {confirmation['stats']['reject']} / skip {confirmation['stats']['skip']}")
    print(f"确认结果已保存到：{CONFIRMATION_FILE}")
    print(f"{'='*70}")
    print()
    print("下一步：等 609 human_review_cli.py 完成后，运行以下命令批量执行：")
    print("  .venv\\Scripts\\python.exe tools/human_review_cli.py --batch-from-confirmation data/human_review_confirmation_609.json")
    print()
    print("或者手动逐条执行：")
    print("  .venv\\Scripts\\python.exe tools/human_review_cli.py approve <edge_id> --reason \"<reason>\"")

def main():
    if not PRE_ANNOTATION_FILE.exists():
        print(f"错误：预标注报告不存在：{PRE_ANNOTATION_FILE}")
        print("请先运行：.venv\\Scripts\\python.exe tools/human_review_pre_annotate.py")
        sys.exit(1)
    
    interactive_review()

if "--check" in sys.argv:
    print("OK: human_review_confirm --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)

if __name__ == "__main__":
    main()
