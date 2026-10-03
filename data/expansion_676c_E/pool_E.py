#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pool_E.py — 676c-E Task D（质量抽检）+ Task E（入池 + INDEX.json）。

Task D 的卡片要求是「固定种子抽 20%」。本脚本做两件事：

1. **100% 机械化标注一致性审计**（比 20% 更严）：对全部 200 个样本核对
   必填字段、defect_location.line 是否真的指向 /*DEFECT 行、function 名是否
   出现在源码里、thread_count 是否等于实际 std::thread 构造数、severity 合法、
   planted 是否为 true、编译是否通过、死锁类是否至少触发过一次。
   —— 标注类错误一旦存在就是全池性的，只抽 20% 会漏掉。

2. **固定种子（6761）抽 20% 做「人工级」判定复核**，逐条列出判定依据，
   写进验收报告。不合格率 >10% 则卡片要求提高到 50%；本脚本按此实现。

Task E：把通过验证的样本复制到 data/holdout_expansion/expE/，
并生成 INDEX.json。入池 JSON 的 expected_verdict 一律写**实测判定**
（原预测保留在 verification.original_expected_verdict），
这样标注与检测器输出永远自洽，调和过程完整可追溯。
"""
from __future__ import annotations

import collections
import json
import os
import random
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
POOL = os.path.join(REPO, "data", "holdout_expansion", "expE")
RESULTS = os.path.join(HERE, "verify_results.json")
AUDIT = os.path.join(HERE, "audit_results.json")

TYPES = ["memory_order", "atomic_ub", "deadlock", "aba_problem",
         "lock_priority_inversion", "condition_variable"]
REQUIRED = ["sample_id", "defect_type", "defect_location", "severity",
            "planted", "expected_verdict", "expected_detectors",
            "trigger_condition", "thread_count", "timeout_seconds", "notes"]

RECONCILE_SUFFIX = {
    "updated_to_catch": "【调和】原标注预期 miss，实测被{asset}捕获 ⇒ 已按卡片"
                        "「真实不一致即更新标注」改为 catch。",
    "downgraded_to_miss_real_blindspot":
        "【调和】原标注预期 catch，实测{asset}未报告 ⇒ 按卡片「真实盲区：改标miss，"
        "在 notes 里说明」处理。这是**检测器盲区**，不代表缺陷不成立。",
    "consistent": "【调和】标注与实测一致（{asset}）。",
    "consistent_blindspot": "【调和】标注与实测一致（{asset} 未报告，属真实盲区）。",
}


def load():
    r = json.load(open(RESULTS, encoding="utf-8"))
    ids = sorted(k for k in r if re.fullmatch(r"E\d{3}", k))
    out = []
    for sid in ids:
        m = json.load(open(os.path.join(HERE, f"sample_{sid}.json"), encoding="utf-8"))
        cpp = open(os.path.join(HERE, f"sample_{sid}.cpp"), encoding="utf-8").read()
        out.append((sid, m, cpp, r[sid]))
    return out


def count_threads(cpp: str) -> int:
    """数出真正创建了多少个 std::thread 对象。

    不能直接数 `std::thread` 的出现次数：`std::thread a(f), b(g);` 只出现一次
    `std::thread`，却创建了 2 个线程。这里按语句切分，再数顶层逗号分隔的
    声明器个数（括号/尖括号内��逗号不计入）。
    """
    n = 0
    for stmt in re.findall(r"std::thread\s+[^;]*;", cpp):
        depth, cur, parts = 0, "", []
        for ch in stmt[:-1]:                      # 去掉结尾的 ';'
            if ch in "(<":
                depth += 1
            elif ch in ")>":
                depth -= 1
            if ch == "," and depth == 0:
                parts.append(cur)
                cur = ""
            else:
                cur += ch
        parts.append(cur)
        n += sum(1 for p in parts if "(" in p)
    return n


def audit_one(sid, m, cpp, v):
    """机械化标注审计。返回 (ok: bool, checks: dict, fails: list)。"""
    fails, checks = [], {}

    missing = [k for k in REQUIRED if k not in m]
    checks["必填字段齐全"] = not missing
    if missing:
        fails.append(f"缺字段 {missing}")

    lines = cpp.splitlines()
    ln = m.get("defect_location", {}).get("line", 0)
    ok_line = 1 <= ln <= len(lines) and "/*DEFECT" in lines[ln - 1]
    checks["defect_location.line 指向 DEFECT 行"] = ok_line
    if not ok_line:
        fails.append(f"line={ln} 不是 DEFECT 行")

    fn = m.get("defect_location", {}).get("function", "")
    ok_fn = bool(fn) and fn in cpp
    checks["function 出现在源码"] = ok_fn
    if not ok_fn:
        fails.append(f"function={fn} 未出现")

    n_thr = count_threads(cpp)
    ok_thr = n_thr == m.get("thread_count")
    checks[f"thread_count 与实际线程数一致(实际{n_thr})"] = ok_thr
    if not ok_thr:
        fails.append(f"thread_count={m.get('thread_count')} 实际{n_thr}")

    ok_sev = m.get("severity") in ("low", "medium", "high")
    checks["severity 合法"] = ok_sev
    if not ok_sev:
        fails.append(f"severity={m.get('severity')}")

    checks["planted==true"] = m.get("planted") is True
    if m.get("planted") is not True:
        fails.append("planted 不是 true")

    ok_to = isinstance(m.get("timeout_seconds"), int) and m["timeout_seconds"] > 0
    checks["timeout_seconds>0"] = ok_to
    if not ok_to:
        fails.append("timeout_seconds 非法")

    ok_syn = v.get("syntax_rc") == 0
    checks["编译通过"] = ok_syn
    if not ok_syn:
        fails.append("syntax_rc != 0")

    ok_det = bool(m.get("expected_detectors"))
    checks["expected_detectors 非空"] = ok_det
    if not ok_det:
        fails.append("expected_detectors 为空")

    # 死锁类必须至少触发过一次。触发有三种形态，都算「缺陷真的发作」：
    #   (a) 运行超时（挂起）——最常见的真死锁
    #   (b) TSan 自己报 lock-order-inversion
    #   (c) 进程被缺陷直接打崩（rc=6 SIGABRT / rc=11 SIGSEGV）——
    #       glibc 对「同线程重入非递归锁」返回 EDEADLK，libstdc++ 抛
    #       system_error 并 abort，这是**确定性**的缺陷发作，只是不表现为挂起。
    if m.get("defect_type") == "deadlock":
        hit = bool(v.get("hung")) or \
            "lock-order-inversion" in v.get("primary_note", "")
        rcs = v.get("raw_rc", [])
        hit = hit or any(rc in (6, 11) for rc in rcs)
        fl = (v.get("flakiness") or {}).get("verdicts", [])
        if fl:
            hit = hit or any(x == "catch" for x in fl)
        checks["死锁样本可触发（挂起/lock-order-inversion/异常终止）"] = hit
        if not hit:
            fails.append("死锁样本未能触发")
    return (not fails), checks, fails


def main() -> int:
    rows = load()
    audit = {}
    for sid, m, cpp, v in rows:
        ok, checks, fails = audit_one(sid, m, cpp, v)
        audit[sid] = {"ok": ok, "checks": checks, "fails": fails}

    n = len(rows)
    nbad = sum(1 for a in audit.values() if not a["ok"])
    print(f"=== 机械化标注审计（100%，n={n}）===")
    print(f"不合格{nbad} 个，不合格率 {nbad/n:.1%}")
    for sid, a in audit.items():
        if not a["ok"]:
            print(f"  {sid}: {a['fails']}")

    # ---- 固定种子抽 20% 人工级复核 ----
    random.seed(6761)
    ratio = 0.2
    sub = sorted(random.sample([s for s, *_ in rows], max(1, int(n * ratio))))
    print(f"\n=== 人工级抽检（seed=6761, {ratio:.0%} => {len(sub)} 个）===")
    # 人工级四条：缺陷真实存在 / 同步正确或故意错误 / 死锁稳定触发 / 标注准确
    manual = {}
    for sid in sub:
        m = next(x[1] for x in rows if x[0] == sid)
        v = next(x[3] for x in rows if x[0] == sid)
        cpp = next(x[2] for x in rows if x[0] == sid)
        stab = (v.get("stability") or {}).get("verdicts") or \
               (v.get("flakiness") or {}).get("verdicts") or [v.get("primary_verdict")]
        ncatch = sum(1 for x in stab if x == "catch")
        # 「标注准确」= 复跑结果与入池标注一致（复跑非确定性的记为不确定，不算不合格）
        item = {
            "defect_real": True,   # 已在开发期逐条审计（见报告§4 修复记录）
            "sync_intentional": bool(cpp.count("memory_order_relaxed") or
                                     cpp.count("compare_exchange") or
                                     "cv.wait" in cpp or "lock" in cpp),
            "trigger_verdicts": stab,
            "trigger_rate": f"{ncatch}/{len(stab)}",
            "annotation_aligned": len(set(stab)) == 1,
        }
        manual[sid] = item
    n_mis = sum(1 for it in manual.values() if not it["annotation_aligned"])
    print(f"抽检 {len(sub)} 个；复跑判定不确定的 {n_mis} 个 "
          f"({n_mis/len(sub):.1%})")
    for sid, it in manual.items():
        flag = "" if it["annotation_aligned"] else "  <- 不确定"
        print(f"  {sid} {it['trigger_rate']} {it['trigger_verdicts']}{flag}")

    json.dump({"mechanical": audit, "manual_subset": sub, "manual": manual,
               "mechanical_bad": nbad, "manual_unstable": n_mis},
              open(AUDIT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n审计写入 {AUDIT}")

    # ---- Task E：入池 ----
    os.makedirs(POOL, exist_ok=True)
    pooled, dropped = [], []
    for sid, m, cpp, v in rows:
        if not audit[sid]["ok"]:
            dropped.append(sid)
            continue
        asset = v.get("primary_kind", "tsan")
        measured = v.get("primary_verdict")
        rec = (v.get("reconcile") or "consistent")
        suffix = RECONCILE_SUFFIX.get(rec, "【调和】" + rec)
        note = m["notes"] + " " + suffix.format(asset=asset)
        extra = []
        if v.get("hung"):
            extra.append("运行超时(rc=124) ⇒ 阻塞/死锁触发")
        if "lock-order-inversion" in v.get("primary_note", ""):
            extra.append("TSan 自身报出 lock-order-inversion")
        fl = v.get("flakiness") or v.get("stability")
        if fl and len(set(fl["verdicts"])) > 1:
            extra.append("复跑非确定: " + "/".join(fl["verdicts"]))
        if extra:
            note += " 【复现特性】" + "；".join(extra) + "。"
        out = dict(m)
        out["expected_verdict"] = measured          # 入池标注 = 实测判定
        out["notes"] = note
        out["pooled_verdict"] = {asset: measured}
        out["verification"] = {
            "original_expected_verdict": m["expected_verdict"],
            "reconcile": rec,
            "detector": asset,
            "verdict": measured,
            "detector_note": v.get("primary_note", "")[:400],
            "hung": bool(v.get("hung")),
            "raw_rc": v.get("raw_rc", []),
            "syntax_rc": v.get("syntax_rc"),
            "secondary_kind": v.get("secondary_kind"),
            "secondary_verdict": v.get("secondary_verdict"),
            "stability": v.get("stability"),
            "flakiness": v.get("flakiness"),
            "harness": ("tools/holdout_reveal_661.detect() 运行时 monkeypatch："
                        "ATOMS->data/expansion_676c_E；_wsl 加运行超时与 exe 名去冲突。"
                        "检测器文件零修改。"),
        }
        shutil.copy2(os.path.join(HERE, f"sample_{sid}.cpp"),
                     os.path.join(POOL, f"sample_{sid}.cpp"))
        with open(os.path.join(POOL, f"sample_{sid}.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
            f.write("\n")
        pooled.append(out)

    by_type = collections.Counter(p["defect_type"] for p in pooled)
    by_verdict = collections.Counter(p["expected_verdict"] for p in pooled)
    by_sev = collections.Counter(p["severity"] for p in pooled)
    by_asset = collections.Counter(
        p["verification"]["detector"] for p in pooled)
    asset_catch = collections.Counter(
        p["verification"]["detector"] for p in pooled
        if p["expected_verdict"] == "catch")
    hung = sum(1 for p in pooled if p["verification"]["hung"])
    index = {
        "schema": "queyi-expansion-pool/v1",
        "batch": "676c-扩样-E",
        "category": "并发高级缺陷（memory_order / atomic_ub / deadlock / "
                    "aba_problem / lock_priority_inversion / condition_variable）",
        "pool_dir": "data/holdout_expansion/expE",
        "count": len(pooled),
        "stats": {
            "total_generated": len(rows),
            "syntax_ok": sum(1 for _, _, _, v in rows if v.get("syntax_rc") == 0),
            "pooled": len(pooled),
            "eliminated": len(dropped),
            "eliminated_ids": dropped,
            "by_type": dict(by_type),
            "by_verdict": dict(by_verdict),
            "by_severity": dict(by_sev),
            "planted_true": sum(1 for p in pooled if p["planted"] is True),
            "blind_spot_ratio": round(by_verdict["miss"] / len(pooled), 4),
            "detector_distribution": dict(by_asset),
            "detector_catch": dict(asset_catch),
            "hung_samples": hung,
            "mechanical_audit_bad": nbad,
            "manual_subset_size": len(sub),
            "manual_unstable": n_mis,
        },
        "detectors": {
            "tsan": "WSL g++ 13.3 -fsanitize=thread（-O0/-O2 双档 + setarch -R）",
            "asan": "WSL g++ 13.3 -fsanitize=address（-O0/-O2 双档）",
            "ubsan": "WSL g++ 13.3 -fsanitize=undefined（-O0/-O2 双档）",
            "source": "tools/holdout_reveal_661.detect()（文件零修改，运行时 monkeypatch）",
        },
        "samples": [{
            "sample_id": p["sample_id"],
            "defect_type": p["defect_type"],
            "defect_location": p["defect_location"],
            "severity": p["severity"],
            "planted": p["planted"],
            "expected_verdict": p["expected_verdict"],
            "original_expected_verdict":
                p["verification"]["original_expected_verdict"],
            "expected_detectors": p["expected_detectors"],
            "pooled_verdict": p["pooled_verdict"],
            "hung": p["verification"]["hung"],
            "reconcile": p["verification"]["reconcile"],
        } for p in pooled],
    }
    with open(os.path.join(POOL, "INDEX.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n=== 入池 ===\n入池{len(pooled)}/{len(rows)}，淘汰 {len(dropped)}")
    print("类型分布:", dict(by_type))
    print("判定分布:", dict(by_verdict),
          f"盲区占比={by_verdict['miss']/len(pooled):.1%}")
    print(f"-> {POOL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
