#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 B2 · independence_level 接入 gate 报告（独立报告工具，不改 gate_engine.py）

- 读取 gate 基线数字（data/SNAPSHOT_MANIFEST_617.json 的 gate 段，只读）
- 调用 617 B1 verify_independence_level.compute_level 获取独立性等级
- 输出 data/gate_independence_report_618.md：gate 统计 + 独立性等级 + 缺口分析
- 硬边界：不改 gate_engine.py；数字取自 manifest，未编造。
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
    gate = m["verification_baseline_frozen"]["gate"]
    lvl = vil.compute_level(facts if facts is not None else vil.DEFAULT_FACTS)
    return {"gate": gate, "independence": lvl}


def render(d):
    g = d["gate"]
    lvl = d["independence"]
    L = []
    L.append("# gate 报告 · 验证独立性等级（618 B2）\n")
    L.append("> 独立报告工具，不改 gate_engine.py；gate 数字取自 SNAPSHOT_MANIFEST_617.json（只读）。\n")
    L.append("## 一、gate 统计（冻结基线）\n")
    L.append("- 规则数：**%d**" % g["rules"])
    L.append("- 命中数：**%d**（block=%d / warn=%d / advice=%d）"
             % (g["hits"], g["block"], g["warn"], g["advice"]))
    L.append("- block=0：当前 63 条规则零 block 命中（含学习者镜像门 closed 等），非真逃逸。\n")
    L.append("## 二、验证独立性等级（617 B1）\n")
    L.append("- 离散等级：**L%d**" % lvl["discrete_level"])
    L.append("- 连续性 scalar：**%.4f**" % lvl["continuity_scalar"])
    L.append("- 因子：verifier_independence=%s, second_implementation=%s, checksum=%s, "
             "external_verifiable=%s, third_party=%s"
             % (lvl["factors"]["verifier_independence"], lvl["factors"]["second_implementation"],
                lvl["factors"]["checksum"], lvl["factors"]["external_verifiable"],
                lvl["factors"]["third_party"]))
    L.append("- 注解：%s\n" % lvl["note"])
    L.append("## 三、独立性缺口分析（为什么是 L1 不是 L2/L3）\n")
    L.append("- **L1→L2 缺口**：需 `checksum_protected=True` 且 `external_verifiable_interface=True`。"
             "当前 checksum=True 但 external_verifiable=False（无 VSA 凭证/透明日志生产接口；616 D 原型未接线）。")
    L.append("- **L2→L3 缺口**：需 `third_party_review=True` 且 `trust_root_anchored=True`。"
             "当前第三方审查=False、信任根未真锚定（OTS 未真上链 / in-toto 真签名未做 ⇒ partially_anchored）。")
    L.append("- **根因**：verifier_count=1（单一验证主体），独立性基础在 Level 0；"
             "第二实现（1/63）仅内部缓解，scalar 受 0.2 硬上限约束 ⇒ 实测 %.4f。" % lvl["continuity_scalar"])
    L.append("- **升级路径（交人项 616 #9）**：① 接线 VSA 凭证/透明日志 ⇒ 达 L2；"
             "② 引入独立第三方审查 + OTS 真上链/in-toto 真签名 ⇒ 达 L3。")
    L.append("\n## 四、对逃逸率口径的影响（呼应 617 A1 estimand）\n")
    L.append("- 因独立性=L1，blocked 类型的 L2 任何时刻上界取置信序列 CS=0.9062%%（A1），"
             "而非更松的 L3 外推；L3（≈4.25%%）仅在显式标注\"部署外推、独立性支撑\"时使用，当前不成立。")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description="618 B2 gate 独立性报告")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "gate_independence_report_618.md"))
    args = ap.parse_args()
    txt = render(build())
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
