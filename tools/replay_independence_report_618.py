#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 B4 · independence_level 接入 replay 报告（独立报告工具，不改 atom_evidence_replay.py）

- 读取 replay 基线数字（data/SNAPSHOT_MANIFEST_617.json 的 replay 段，只读）
- 调用 617 B1 verify_independence_level.compute_level 获取独立性等级
- 输出 data/replay_independence_report_618.md：replay 统计 + 独立性等级 + 缺口分析
- 硬边界：不改 atom_evidence_replay.py；数字取自 manifest，未编造。
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "data", "SNAPSHOT_MANIFEST_617.json")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import verify_independence_level as vil  # noqa: E402


def build(facts=None):
    with open(MANIFEST, encoding="utf-8") as f:
        m = json.load(f)
    rp = m["verification_baseline_frozen"]["replay"]
    lvl = vil.compute_level(facts if facts is not None else vil.DEFAULT_FACTS)
    return {"replay": rp, "independence": lvl}


def render(d):
    rp = d["replay"]
    lvl = d["independence"]
    L = []
    L.append("# replay 报告 · 验证独立性等级（618 B4）\n")
    L.append("> 独立报告工具，不改 atom_evidence_replay.py；replay 数字取自 SNAPSHOT_MANIFEST_617.json（只读）。\n")
    L.append("## 一、replay 统计（冻结基线）\n")
    L.append("- confirm（一致）：**%d**" % rp["confirm"])
    L.append("- refute（反驳）：**%d**" % rp["refute"])
    L.append("- infra_error（基础设施错误）：**%d**" % rp["infra_error"])
    L.append("- refute=0：atom↔evidence 重放零反驳，未观测逃逸（声称零逃逸 regime，见 617 A1 escaped 类型）。\n")
    L.append("## 二、验证独立性等级（617 B1）\n")
    L.append("- 离散等级：**L%d**" % lvl["discrete_level"])
    L.append("- 连续性 scalar：**%.4f**" % lvl["continuity_scalar"])
    L.append("- 注解：%s\n" % lvl["note"])
    L.append("## 三、独立性缺口分析（为什么是 L1 不是 L2/L3）\n")
    L.append("- **L1→L2 缺口**：需 `checksum_protected=True` 且 `external_verifiable_interface=True`。"
             "replay 工件受 checksum 保护，但 external_verifiable=False（重放凭证未作为可第三方验证接口暴露）。")
    L.append("- **L2→L3 缺口**：需第三方审查 + 信任根真锚定；当前均为 False（partially_anchored）。")
    L.append("- **根因**：单一验证主体（verifier=1），scalar 受 0.2 硬上限 ⇒ 实测 %.4f。" % lvl["continuity_scalar"])
    L.append("- **升级路径（交人项 616 #9）**：重放凭证经 VSA/透明日志暴露给独立第三方重放 ⇒ 达 L2/L3。")
    L.append("\n## 四、对逃逸率口径的影响（呼应 617 A1 estimand）\n")
    L.append("- replay refute=0 即“声称零逃逸”，其 L2b 由 618 A3 的 e-process mixture 给出（≈0.6488%% 任何时刻上界），"
             "而非简单宣布 0；L3 外推（≈4.235%%）当前不成立（独立性 L1）。")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="618 B4 replay 独立性报告")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "replay_independence_report_618.md"))
    args = ap.parse_args()
    txt = render(build())
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
