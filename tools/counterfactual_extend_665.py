#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""counterfactual_extend_665.py — 665 E2：反事实引文 10 → 20（**带真值标签**）。

662 B3 的结论是"反事实算子**校准不充分**：负例太易，所有 τ 下 P=R=F1=1.0"。
根因不在阈值 τ，而在**负例本身没有难度**：660 的 10 条全部是
"断言显式引用引文 id" ⇒ 算子闭着眼判 dependent 也能满分。

本批做两件不同的事
==================
1. **构造有真值标签的样本**：每条样本除了算子判定，还写 `ground_truth`
   （断言到底依不依赖这条引文），判据是**外部锚**：
     dependent   = 该断言的支撑**只有**这条实测引文（例如平台相关的测量值）
     independent = 断言本身另有**标准/语言规则**作依据（实测引文只是佐证）
2. **让算子被打分**：用 `tools/counterfactual_citation_658.py::counterfactual()`
   （唯一算子版本）跑一遍，和 ground_truth 比出 P/R/F1 —— 662 说"校准不充分"，
   本批把它变成**一个可以读出来的数**。

断言与引文都不是手写故事：从 `data/cards_665/index_665.json` 里取**本次真机实测**的
内容（哪张卡、什么命令行、读到什么输出）。

输出：data/counterfactual_cases_665.json
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
INDEX = os.path.join(ROOT, "data", "cards_665", "index_665.json")
OUT = os.path.join(ROOT, "data", "counterfactual_cases_665.json")


def _load_op658():
    spec = importlib.util.spec_from_file_location("cf658", os.path.join(HERE, "counterfactual_citation_658.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


#: 10 条新案例的设计表：`card` → (断言模板, 假引文文本, 外部锚类型)
#: external_anchor 取值：
#:   "standard"     ⇒ 断言另有标准依据 ⇒ 引文为假也成立（ground_truth=independent）
#:   "measurement"  ⇒ 断言只靠这次实测 ⇒ 引文为假则不成立（ground_truth=dependent）
CASES: list[dict] = [
    {"cid": "ig-01", "external_anchor": "standard",
     "assertion": "有符号整数溢出是 UB（不是回绕）：标准规定结果超出类型可表示范围时行为未定义",
     "fake": "UBSan 在本机从未对 INT_MAX+1 报 runtime error（假）"},
    {"cid": "ig-02", "external_anchor": "standard",
     "assertion": "数组越界访问是 UB：即使没崩，语义也已不被保证",
     "fake": "ASan 在本机从未报过越界（假）"},
    {"cid": "ig-03", "external_anchor": "standard",
     "assertion": "delete 空指针是标准保证的 no-op，不是不安全操作",
     "fake": "ASan 对 delete nullptr 报了错（假）"},
    {"cid": "ig-05", "external_anchor": "measurement",
     "assertion": "在本机 x86-64 MinGW-w64 上 sizeof(unique_ptr<int>) 等于 sizeof(void*)",
     "fake": "本机实测 sizeof(unique_ptr<int>)=16 而 sizeof(void*)=8（假）"},
    {"cid": "ig-06", "external_anchor": "standard",
     "assertion": "用 weak_ptr 断开环后两个对象都能析构（weak_ptr 不增加引用计数）",
     "fake": "weak_ptr 也会增加引用计数（假）"},
    {"cid": "ig-07", "external_anchor": "standard",
     "assertion": "解引用空指针是 UB（不保证一定段错误）",
     "fake": "ASan 在本机从未对空指针解引用报 DEADLYSIGNAL（假）"},
    {"cid": "ig-08", "external_anchor": "standard",
     "assertion": "整数除零是 UB/信号，不是 C++ 异常（catch(...) 抓不到）",
     "fake": "UBSan 对除零从未报 runtime error（假）"},
    {"cid": "ig-11", "external_anchor": "measurement",
     "assertion": "在本机 MinGW-w64 上 sizeof(int) 等于 4",
     "fake": "本机实测 sizeof(int)=8（假）"},
    {"cid": "ig-12", "external_anchor": "standard",
     "assertion": "vector<bool> 是位压缩特化，取 &v[0] 得不到 bool*",
     "fake": "g++ 接受 &v[0] 且类型就是 bool*（假）"},
    {"cid": "ig-15", "external_anchor": "standard",
     "assertion": "具名右值引用形参是左值，直接传递会走拷贝（需显式 std::move）",
     "fake": "实测 h(T&&) 内部调用 g(x) 打印的是 move（假）"},
]


def mechanism_class(mech: str) -> str:
    """把算子给出的 `mechanism` 文案归类到**是哪条判据命中的**（668：给第三判据一个可数的口径）。

    算子返回的是自然语言（"断言显式引用引文 id" / "共用 N 个 token" / "自报机器…"），
    归类靠关键词。分类口径**写在这里**，不散落在报告里 —— 否则下一个人又要靠猜。
    """
    if "显式引用" in mech:
        return "cited_id"          # 判据 1
    if "共享" in mech:
        return "token_overlap"     # 判据 2
    if "自报机器" in mech:
        return "machine_marker"    # 判据 3（666 A4）
    return "none"


def main() -> int:
    cf = _load_op658()
    idx = json.load(open(INDEX, encoding="utf-8"))
    rows = {r["source_id"]: r for r in idx["cards"]}

    cases, n_tp = [], {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    for i, c in enumerate(CASES, start=11):
        row = rows.get(c["cid"])
        if row is None:
            print(f"[skip] {c['cid']} 不在 index_665（先 --build）")
            continue
        citation_id = f"EV-{row['id']}"
        citation_text = f"{row['detector']} 实测：{row['note']}（签名 {row['signature']}）"
        res = cf.counterfactual(c["assertion"], citation_id, citation_text)
        truth = "dependent" if c["external_anchor"] == "measurement" else "independent"
        pred = "dependent" if res["dependent"] else "independent"
        if truth == "dependent" and pred == "dependent":
            n_tp["tp"] += 1
        elif truth == "independent" and pred == "dependent":
            n_tp["fp"] += 1
        elif truth == "independent" and pred == "independent":
            n_tp["tn"] += 1
        else:
            n_tp["fn"] += 1
        cases.append({"id": f"cf{i}", "card": row["id"], "source_id": c["cid"],
                      "mechanism_class": mechanism_class(res.get("mechanism", "")),
                      "atom_ref": row["fixture_rel"],
                      "original_assertion": c["assertion"],
                      "original_citation": {"id": citation_id, "text": citation_text,
                                            "measured_out": row.get("measured_out", ""),
                                            "reproduce": row["fixture_rel"]},
                      "fake_citation": {"id": citation_id, "text": c["fake"]},
                      "question": f"若 {citation_id} 为假，原断言还成立吗？",
                      "external_anchor": c["external_anchor"],
                      "ground_truth": truth,
                      "operator": res,
                      "operator_prediction": pred,
                      "agree": truth == pred})
        print(f"  cf{i}  truth={truth:<11} pred={pred:<11} agree={truth == pred}")

    tp, fp, _tn, fn = n_tp["tp"], n_tp["fp"], n_tp["tn"], n_tp["fn"]  # tn 供报告用（见下）
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    mech_counts: dict[str, int] = {}
    for c in cases:
        mech_counts[c["mechanism_class"]] = mech_counts.get(c["mechanism_class"], 0) + 1
    third_hits = [c["id"] for c in cases if c["mechanism_class"] == "machine_marker"]

    rep = {
        "schema": "queyi-counterfactual/v2",
        "generated_at": time.strftime("%Y-%m-%d"),
        "generated_by": "tools/counterfactual_extend_665.py",
        "operator_reuse": "tools/counterfactual_citation_658.py::counterfactual（唯一算子版本）",
        "cases_total": len(cases),
        # 668：**分母必须自己说清**。666 的"20 条"是把本文件的 10 条与 660 的 10 条
        # 混着说了 —— 而 660 那 10 条**没有 ground_truth 标签**，根本进不了 P/R/F1。
        "denominator": {
            "value": len(cases),
            "meaning": "本文件里**带 ground_truth 标签**的案例数（P/R/F1 的分母）",
            "scored": len(cases),
            "unscored_sibling": {
                "file": "data/counterfactual_cases_660.json",
                "cases": 10,
                "why": "660 只记录算子输出，**没有真值标签** ⇒ 不能进 P/R/F1（登记，不计入）",
            },
            "why_it_matters": "对外说'20 条'而实际打分 10 条 = 分母未声明（667 已记过一次同类问题）",
        },
        "truth_labels": {"dependent": sum(1 for c in cases if c["ground_truth"] == "dependent"),
                         "independent": sum(1 for c in cases if c["ground_truth"] == "independent")},
        "confusion": n_tp,
        "scores": {"precision": round(prec, 3), "recall": round(rec, 3), "f1": round(f1, 3)},
        "mechanism_counts": mech_counts,
        "third_criterion": {
            "name": "machine_marker（666 A4 新增的第 3 条判据）",
            "hits": third_hits,
            "hit_count": len(third_hits),
            "note": ("这两条真·dependent 断言（平台测量类）正是判据 1/2 抓不到的；"
                     "判据 3 把它们抓住了。**但真值标签与判据 3 同源** ⇒ F1 是上界。"),
        },
        "honest_note": ("真值标签的判据是**外部锚**（standard ⇒ 引文为假断言仍成立；"
                        "measurement ⇒ 断言只靠这次实测），不是靠感觉。"
                        "662 说'校准不充分'，本批把它换成可复算的 P/R/F1；"
                        f"分母只有 {len(cases)} 条，**任何百分比都是点估计**（n={len(cases)} 时 "
                        "95% CI 宽度约 ±30pp，Clopper–Pearson）。"
                        "⚠ 判据 3 与真值标签**同源**（都按'是否平台测量'判）⇒ "
                        "本 F1 是**上界**，不代表泛化能力；要真校准需引文级标注的外部语料（未做）。"),
        "cases": cases,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nconfusion={n_tp}  P={prec:.3f} R={rec:.3f} F1={f1:.3f}")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
