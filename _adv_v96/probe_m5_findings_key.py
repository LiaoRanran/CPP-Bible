#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""575 验收探针：独立验证 mutation_fuzz._findings_key 三元组吞掉 M5 告警的 bug，
以及苦力声称的修法（文案并入键）能否翻盘。不改正式文件，全程 mf.sandbox 临时副本。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import gate_engine as ge  # noqa: E402
import mutation_fuzz as mf  # noqa: E402


def run(keyfn, label):
    mf._findings_key = keyfn  # _snapshot 内按模块全局名查找，patch 生效
    rows = []
    strict_rules = {}
    cards = sorted((ROOT / "atoms").rglob("ATOM-*.md"))  # 必须在进 sandbox 前用原始路径
    with mf.sandbox() as tmp:
        baseline = mf._snapshot()
        for card in cards:
            text = card.read_text(encoding="utf-8")
            sb = mf._rel_in_sandbox(card, tmp)
            try:
                variants = mf.mut_m5(text)
            except Exception as e:  # noqa: BLE001
                print("mut_m5 error", card.stem, e)
                continue
            if not variants:
                continue
            for point, vt in variants:
                if vt is None:
                    rows.append((card.stem, point, "n_a")); continue
                if vt == text:
                    rows.append((card.stem, point, "n_a")); continue
                sb.write_text(vt, encoding="utf-8")
                new = mf._snapshot() - baseline
                nb = sorted({f"{k[0]}@{k[2]}" for k in new if k[1] == "block"})
                nw = sorted({f"{k[0]}@{k[2]}" for k in new if k[1] == "warn"})
                if nb:
                    v = "strict"
                    for x in nb:
                        strict_rules[x.split("@")[0]] = strict_rules.get(x.split("@")[0], 0) + 1
                elif nw:
                    v = "warn_only"
                else:
                    v = "escaped"
                rows.append((card.stem, point, v))
            sb.write_text(text, encoding="utf-8")
    from collections import Counter
    c = Counter(r[2] for r in rows)
    judged = c["strict"] + c["warn_only"] + c["escaped"]
    print(f"\n===== {label} =====")
    print(f"M5 变体总数 {len(rows)}: strict={c['strict']} warn_only={c['warn_only']} "
          f"escaped={c['escaped']} n_a={c['n_a']} (可判 {judged})")
    print(f"strict 命中的 block 规则分布: {strict_rules}")
    esc = [f"{r[0]}[{r[1]}]" for r in rows if r[2] == "escaped"]
    print(f"escaped 明细(前10): {esc[:10]}")
    return c, strict_rules


print("修法验证前先确认现状基线 gate 命中：", len(mf._snapshot()), "条 finding")
c3, _ = run(lambda f: (f.rule_id, f.severity, f.target), "三元组(现状 _findings_key)")
c4, sr4 = run(lambda f: (f.rule_id, f.severity, f.target, f.message), "四元组(并入文案=苦力修法)")
print("\n===== 结论 =====")
print(f"escaped: 三元组 {c3['escaped']} -> 四元组 {c4['escaped']}")
print(f"strict 是否非 warn 冒充: {sr4}")
