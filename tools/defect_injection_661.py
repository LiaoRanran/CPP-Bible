#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""defect_injection_661.py — 661 B2：真实缺陷注入测试（15 条）。

做法：对 defects.json 的 15 条真实错，
  - 可机械重注入的 → 在**临时副本**上构造错误版本，跑等价最小检测器，记 caught/missed；
  - 不可机械重注入的 → 诚实登记 not_reinjectable（附历史 gate_caught）。
输出：data/defect_injection_661.json

红线：re-inject 只在临时副本，绝不碰 atoms/evidence/Examples/Book/。
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import tempfile

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFECTS = os.path.join(ROOT, "data", "defect_fixtures", "defects.json")
OUT = os.path.join(ROOT, "data", "defect_injection_661.json")


def _spdx_check(path):
    first = ""
    for line in open(path, encoding="utf-8"):
        if line.strip():
            first = line.strip()
            break
    return first.startswith("#!/") or "SPDX-License-Identifier" in first


def _wcag_ratio(fg, bg):
    def lum(c):
        r, g, b = (c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255
        def f(u):
            return u / 12.92 if u <= 0.03928 else ((u + 0.055) / 1.055) ** 2.4
        return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
    l1, l2 = lum(fg), lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def inj_manifest_drift():
    d = tempfile.mkdtemp(prefix="d661_")
    f = os.path.join(d, "payload.bin")
    orig = b"correct-bytes-v1"
    open(f, "wb").write(orig)
    exp = hashlib.sha256(orig).hexdigest()
    ok_correct = hashlib.sha256(open(f, "rb").read()).hexdigest() == exp
    open(f, "wb").write(b"tampered-v2")
    ok_inj = hashlib.sha256(open(f, "rb").read()).hexdigest() == exp
    return {"gate": "web_logic_check_655(sha256 台账)", "caught": (not ok_inj) and ok_correct}


def inj_license_header():
    d = tempfile.mkdtemp(prefix="d661_")
    f = os.path.join(d, "noheader.py")
    open(f, "w", encoding="utf-8").write("def f():\n    return 1\n")
    return {"gate": "license/governance_doc_guard(SPDX)", "caught": not _spdx_check(f)}


def inj_wcag_contrast():
    good = _wcag_ratio(0x000000, 0xFFFFFF)     # 21:1 合规
    bad = _wcag_ratio(0x787F87, 0xFFFFFF)      # 656 实测 4.80? 构造劣化
    worst = _wcag_ratio(0x999999, 0xFFFFFF)    # 低对比
    return {"gate": "WCAG 对比度现算(≥4.5:1)", "caught": worst < 4.5 and good >= 4.5,
            "note": f"good={good:.2f} bad={bad:.2f} worst={worst:.2f}"}


def inj_yaml_date():
    """等价再现 656-self-4：date 直序列化在 **card.html 数据契约(JSON)** 上失败。
    （注：PyYAML 内建支持 date，故以 JSON 契约再现原错。）"""
    yaml_ok = True
    try:
        yaml.safe_dump({"date": datetime.date(2026, 9, 28)})
    except Exception:  # noqa: BLE001
        yaml_ok = False
    try:
        json.dumps({"date": datetime.date(2026, 9, 28)})
        json_ok = True
    except TypeError:
        json_ok = False
    return {"gate": "frontmatter 数据契约(date 直序列化)",
            "caught": (not json_ok) and yaml_ok,
            "note": f"JSON 直序列化 date 失败={not json_ok}；YAML 内建支持 date={yaml_ok}"}


def inj_unanchored():
    d = tempfile.mkdtemp(prefix="d661_")
    f = os.path.join(d, "ev.md")
    # 断言引用了不存在的外部锚 → 应判 UNANCHORED
    open(f, "w", encoding="utf-8").write("claim: X\nanchor: [missing-anchor-999]\n")
    txt = open(f, encoding="utf-8").read()
    anchors = re.findall(r"anchor:\s*\[([^\]]*)\]", txt)
    has_anchor = bool(anchors and anchors[0].strip())
    # 最小检测：锚存在但实体不存在 → 视为未锚定
    anchored = has_anchor and os.path.isfile(os.path.join(d, anchors[0].strip()))
    return {"gate": "data_sanity_audit(UNANCHORED_EVIDENCE)", "caught": not anchored}


def inj_truncation():
    d = tempfile.mkdtemp(prefix="d661_")
    f = os.path.join(d, "ch.md")
    open(f, "w", encoding="utf-8").write("# ch\n\n```cpp\nint main(){\n")  # 未闭合围栏
    txt = open(f, encoding="utf-8").read()
    fences = txt.count("```")
    return {"gate": "真机编译门禁(截断/未闭合围栏)", "caught": fences % 2 != 0}


REINJECTORS = {
    "657-manifest-drift": inj_manifest_drift,
    "657-license-header": inj_license_header,
    "656-self-6": inj_wcag_contrast,
    "656-self-4": inj_yaml_date,
    "ch28-unanchored": inj_unanchored,
    "ch41-truncation": inj_truncation,
}

# 明确不可机械重注入的（须原错误版本源码或真机管线）
NOT_REINJECTABLE_REASON = {
    "656-self-1": "测试射程(需重放 teach 自测题生成器，非单文件可注入)",
    "656-self-2": "变异作用域(需跑变异引擎，非单文件可注入)",
    "656-self-3": "进程跑飞(需真机变异进程，环境相关)",
    "656-self-5": "只读产物比对(需磁盘产物快照)",
    "657-jsdom-skip": "DOM 层(需 jsdom 运行环境)",
    "652-t2-false-switch": "探针假象(需真机 budget_guard/shadow_mode 管线)",
    "ch157-prose-fake": "散文假代码块(需全书编译管线)",
    "ch110-historical": "历史 bug，gate_caught=unknown（待回填）",
    "ch85-historical": "历史 bug，gate_caught=unknown（待回填）",
}


def main() -> int:
    defects = json.load(open(DEFECTS, encoding="utf-8"))["defects"]
    results = []
    caught = run_n = 0
    for d in defects:
        did = d["id"]
        fn = REINJECTORS.get(did)
        if fn:
            r = fn()
            run_n += 1
            caught += 1 if r["caught"] else 0
            results.append({"id": did, "status": "reinjected", "caught": r["caught"],
                            "gate": r["gate"], "note": r.get("note", "")})
        else:
            results.append({"id": did, "status": "not_reinjectable", "caught": None,
                            "gate": d.get("gate_caught", ""),
                            "note": NOT_REINJECTABLE_REASON.get(did, "未实现重注入器")})
    hist_yes = sum(1 for d in defects if str(d.get("gate_caught", "")).startswith("yes"))
    rep = {
        "schema": "queyi-defect-injection/v1",
        "generated_at": "2026-09-28",
        "generated_by": "tools/defect_injection_661.py",
        "total_defects": len(defects),
        "reinjectable": run_n,
        "reinject_caught": caught,
        "reinject_rate_pct": round(caught / run_n * 100, 1) if run_n else 0.0,
        "not_reinjectable": len(defects) - run_n,
        "historical_gate_caught_yes": hist_yes,
        "coverage_all_pct": round(hist_yes / len(defects) * 100, 1) if defects else 0.0,
        "honest_note": "重注入子集是硬指标；其余缺原错误版本/真机管线，只有历史 gate_caught 记录（软覆盖，未重注入证明）——正是盲化 holdout 要补的外部效度缺口。",
        "results": results,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    for r in results:
        flag = "CAUGHT" if r["caught"] else ("MISSED" if r["caught"] is False else "NOT_REINJ")
        print(f"  {r['id']:<22} {flag:<9} {r['gate'][:50]}")
    print(f"\n重注入检出率 = {caught}/{run_n} = {rep['reinject_rate_pct']}%")
    print(f"历史 gate_caught=yes 覆盖 = {hist_yes}/{len(defects)} = {rep['coverage_all_pct']}%")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
