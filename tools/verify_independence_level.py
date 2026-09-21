#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""617 B1 · 验证独立性 4 级判定（纯标准库，只读事实）

按事实（默认取自 616 D 他验基线，可 --facts 覆盖）计算：
  - discrete_level: 0/1/2/3（自证 / 内部第二实现 / 外部可验证 / 独立第三方）
  - continuity_scalar: 0..1（A1 L3 shrinkage 的 independence_level；verifier=1 时封顶 0.2）

铁律：只读事实判定，不代签任何裁决；是否投入 Level 2/3 见交人项（616 #9）。
"""
import argparse
import json
import sys

# 当前事实（616 D 他验基线）
DEFAULT_FACTS = {
    "verifier_count": 1,
    "second_implementation_rules": 1,
    "second_implementation_total": 63,
    "checksum_protected": True,
    "external_verifiable_interface": False,  # VSA 凭证 / 透明日志
    "third_party_review": False,
    "trust_root_anchored": False,            # OTS 真上链 / in-toto 真签名
}

WEIGHTS = {
    "verifier_independence": 0.5,
    "second_implementation": 0.2,
    "checksum": 0.15,
    "external_verifiable": 0.1,
    "third_party": 0.05,
}


def compute_level(facts):
    vi = 1.0 if facts["verifier_count"] > 1 else 0.0
    si = facts["second_implementation_rules"] / max(1, facts["second_implementation_total"])
    cs = 1.0 if facts["checksum_protected"] else 0.0
    ev = 1.0 if facts["external_verifiable_interface"] else 0.0
    tp = 1.0 if (facts["third_party_review"] and facts["trust_root_anchored"]) else 0.0

    # 离散等级
    level = 0
    if facts["second_implementation_rules"] > 0:
        level = 1
    if facts["checksum_protected"] and facts["external_verifiable_interface"]:
        level = 2
    if level >= 2 and facts["third_party_review"] and facts["trust_root_anchored"]:
        level = 3

    # 连续 scalar：verifier 独立性 = 0 时封顶 0.2（仅内部缓解）
    raw = (WEIGHTS["verifier_independence"] * vi
           + WEIGHTS["second_implementation"] * si
           + WEIGHTS["checksum"] * cs
           + WEIGHTS["external_verifiable"] * ev
           + WEIGHTS["third_party"] * tp)
    scalar = raw if vi > 0 else min(raw, 0.2)

    return {
        "discrete_level": level,
        "continuity_scalar": round(scalar, 4),
        "factors": {
            "verifier_independence": vi,
            "second_implementation": round(si, 4),
            "checksum": cs,
            "external_verifiable": ev,
            "third_party": tp,
        },
        "note": (
            "verifier=1 ⇒ 基础在 Level 0；当前离散=1（第二实现存在，缺外部接口/第三方）；"
            "scalar 受 verifier 独立性=0 硬上限约束。"
        ),
    }


def selftest():
    """只读自验证（不写任何文件）。返回失败项列表，空列表 = 通过。"""
    fails = []
    d = compute_level(dict(DEFAULT_FACTS))
    if d["discrete_level"] not in (0, 1, 2, 3):
        fails.append("discrete_level 越界：%s" % d["discrete_level"])
    if not (0.0 <= d["continuity_scalar"] <= 1.0):
        fails.append("continuity_scalar 越界：%s" % d["continuity_scalar"])
    if DEFAULT_FACTS["verifier_count"] == 1 and d["continuity_scalar"] > 0.2:
        fails.append("verifier=1 时 scalar 超过 0.2 硬上限：%s" % d["continuity_scalar"])
    strong = dict(DEFAULT_FACTS, verifier_count=2, external_verifiable_interface=True,
                  third_party_review=True, trust_root_anchored=True)
    ds = compute_level(strong)
    if ds["discrete_level"] != 3:
        fails.append("全满足事实应判 L3，实得 L%d" % ds["discrete_level"])
    if ds["continuity_scalar"] < d["continuity_scalar"]:
        fails.append("独立性增强后 scalar 反而下降")
    zero = dict(DEFAULT_FACTS, second_implementation_rules=0)
    if compute_level(zero)["discrete_level"] != 0:
        fails.append("无第二实现应判 L0")
    return fails


def main():
    ap = argparse.ArgumentParser(description="617 B1 验证独立性 4 级判定")
    ap.add_argument("--facts", help="JSON 覆盖事实（如 '{\"verifier_count\":2}'）")
    ap.add_argument("--check", action="store_true", help="只读自验证（不写文件），exit 0=通过")
    args = ap.parse_args()
    if args.check:
        fails = selftest()
        for f in fails:
            print("FAIL: %s" % f)
        print("617 B1 --check: %s" % ("PASS" if not fails else "FAIL"))
        sys.exit(0 if not fails else 1)
    facts = dict(DEFAULT_FACTS)
    if args.facts:
        facts.update(json.loads(args.facts))
    print(json.dumps(compute_level(facts), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
