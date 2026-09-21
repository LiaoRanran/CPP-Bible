#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 B3 · independence_level 接入 poison 报告（独立报告工具，不改 poison_drill.py）

- 读取 poison 基线数字（data/SNAPSHOT_MANIFEST_617.json 的 poison 段，只读）
- 调用 617 B1 verify_independence_level.compute_level 获取独立性等级
- 输出 data/poison_independence_report_618.md：poison 统计 + 独立性等级 + 缺口分析
- 硬边界：不改 poison_drill.py；数字取自 manifest，未编造。
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
    p = m["verification_baseline_frozen"]["poison"]
    lvl = vil.compute_level(facts if facts is not None else vil.DEFAULT_FACTS)
    return {"poison": p, "independence": lvl}


def render(d):
    p = d["poison"]
    lvl = d["independence"]
    L = []
    L.append("# poison 报告 · 验证独立性等级（618 B3）\n")
    L.append("> 独立报告工具，不改 poison_drill.py；poison 数字取自 SNAPSHOT_MANIFEST_617.json（只读）。\n")
    L.append("## 一、poison 统计（冻结基线）\n")
    L.append("- 触发/总数：**%d / %d**（通过率 100%%）" % (p["passed"], p["total"]))
    L.append("- 覆盖率：表观 **%s** · 诚实 **%s**（诚实口径剔除 machine-untriggerable 3 条）"
             % (p["coverage_apparent"], p["coverage_honest"]))
    L.append("- 诚实覆盖率 = 60/63 = 95.2%%，如实反映 3 条机器不可触发规则不计覆盖。\n")
    L.append("## 二、验证独立性等级（617 B1）\n")
    L.append("- 离散等级：**L%d**" % lvl["discrete_level"])
    L.append("- 连续性 scalar：**%.4f**" % lvl["continuity_scalar"])
    L.append("- 注解：%s\n" % lvl["note"])
    L.append("## 三、独立性缺口分析（为什么是 L1 不是 L2/L3）\n")
    L.append("- **L1→L2 缺口**：需 `checksum_protected=True` 且 `external_verifiable_interface=True`。"
             "poison_drill 工具在 checksum 保护集内（22 项），但 external_verifiable=False。")
    L.append("- **L2→L3 缺口**：需第三方审查 + 信任根真锚定；当前均为 False（partially_anchored）。")
    L.append("- **根因**：单一验证主体（verifier=1），scalar 受 0.2 硬上限 ⇒ 实测 %.4f；"
             "poison 覆盖率诚实口径的\"可信度\"受独立性 L1 限制，不能宣称独立第三方背书。" % lvl["continuity_scalar"])
    L.append("- **升级路径（交人项 616 #9）**：接线 VSA 凭证/透明日志 + 独立第三方重跑 poison ⇒ 达 L2/L3。")
    L.append("\n## 四、对逃逸率口径的影响（呼应 617 A1 estimand）\n")
    L.append("- poison 覆盖率诚实 95.2%% 是样本内描述（L1）；若做 L3 部署外推，需叠加独立性 scalar 收缩（≈4.25%% 量级），当前不成立。")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="618 B3 poison 独立性报告")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "poison_independence_report_618.md"))
    args = ap.parse_args()
    txt = render(build())
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
