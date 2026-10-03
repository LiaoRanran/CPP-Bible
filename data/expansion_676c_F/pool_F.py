"""pool_F.py — 任务 E 入池（676c-F）。

规格（data/prompts/676c_F_扩样嵌入式平台.md）入池目标（区间）：
  alignment 20-30 / endianness 25-30 / volatile_misuse 25-30 /
  bit_operation 25-30 / interrupt_safety 15-25 / register_ub 15-25，合计 125-170。

本批 200 个候选**全部**通过验证（Task B/C），故按类型目标做确定性裁剪：
  - 每类型先收全部 catch 样本（最大化检出样本代表性）；
  - 差额用 miss 样本在类型 ID 区间内**等距抽样**（保留变体多样性，端点必含）。

产物：data/holdout_expansion/expF/sample_FXXX.{cpp,json} + INDEX.json。
"""
import os, json, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = HERE
DST = os.path.join(REPO, "data", "holdout_expansion", "expF")

# 类型 → (ID 区间 [lo, hi], 入池目标数, 规格区间)
PLAN = {
    "alignment":        (1, 35, 25, (20, 30)),
    "endianness":       (36, 70, 28, (25, 30)),
    "volatile_misuse":  (71, 105, 28, (25, 30)),
    "bit_operation":    (106, 140, 28, (25, 30)),
    "interrupt_safety": (141, 170, 20, (15, 25)),
    "register_ub":      (171, 200, 20, (15, 25)),
}


def even_spaced(lo, hi, k):
    """[lo, hi] 内取 k 个等距整数（端点必含，升序去重）。"""
    if k <= 0:
        return []
    if k == 1:
        return [lo]
    if k >= hi - lo + 1:
        return list(range(lo, hi + 1))
    return sorted({round(lo + i * (hi - lo) / (k - 1)) for i in range(k)})


def main():
    results = json.load(open(os.path.join(SRC, "verify_results.json"), encoding="utf-8"))
    os.makedirs(DST, exist_ok=True)

    selected = []          # [(sid, meta, rec)]
    plan_report = {}
    for typ, (lo, hi, want, rng) in PLAN.items():
        ids = [f"F{i:03d}" for i in range(lo, hi + 1)]
        # 只收 pooled=True 的
        ok = [i for i in ids if results.get(i, {}).get("pooled")]
        catch = [i for i in ok
                 if json.load(open(os.path.join(SRC, f"sample_{i}.json"), encoding="utf-8"))["expected_verdict"] == "catch"]
        miss = [i for i in ok if i not in set(catch)]
        take_catch = catch
        need_miss = max(0, want - len(catch))
        # miss 等距抽样按其在 miss 列表中的位置映射回原 ID 区间
        take_miss = even_spaced(0, len(miss) - 1, need_miss) if need_miss else []
        take_miss = [miss[j] for j in take_miss]
        take = sorted(take_catch + take_miss)
        assert rng[0] <= len(take) <= rng[1], f"{typ} 入池数 {len(take)} 超出规格区间 {rng}"
        plan_report[typ] = {"target": want, "range": list(rng), "catch_avail": len(catch),
                            "miss_avail": len(miss), "pooled": len(take),
                            "pooled_catch": len(take_catch), "pooled_miss": len(take_miss)}
        for sid in take:
            meta = json.load(open(os.path.join(SRC, f"sample_{sid}.json"), encoding="utf-8"))
            selected.append((sid, meta, results[sid]))

    total = len(selected)
    assert 125 <= total <= 170, f"总入池数 {total} 超出 125-170"

    # 拷贝
    for sid, _meta, _rec in selected:
        for ext in (".cpp", ".json"):
            shutil.copy2(os.path.join(SRC, f"sample_{sid}{ext}"),
                         os.path.join(DST, f"sample_{sid}{ext}"))

    # 统计
    by_type, sev, det_mix, pd_cnt, catch_cnt = {}, {}, {}, 0, 0
    index = []
    for sid, meta, rec in selected:
        t = meta["defect_type"]
        by_type[t] = by_type.get(t, 0) + 1
        sev[meta["severity"]] = sev.get(meta["severity"], 0) + 1
        d = (meta.get("expected_detectors") or ["?"])[0]
        det_mix[d] = det_mix.get(d, 0) + 1
        if meta.get("platform_dependent"):
            pd_cnt += 1
        if meta["expected_verdict"] == "catch":
            catch_cnt += 1
        index.append({
            "id": sid, "defect_type": t, "severity": meta["severity"],
            "expected_verdict": meta["expected_verdict"], "detector": d,
            "defect_line": meta["defect_location"]["line"],
            "planted": meta["planted"],
            "platform_dependent": meta.get("platform_dependent", False),
        })

    index_doc = {
        "agent": "676c-expF",
        "category": "F",
        "theme": "嵌入式/平台特定缺陷（对齐/端序/volatile/位操作/中断安全/寄存器）",
        "generated": 200,
        "pooled": total,
        "not_pooled": 200 - total,
        "not_pooled_reason": ("全部 200 个候选均通过编译与检测器复现验证；按规格各类型入池目标区间"
                              "（20-30/25-30/25-30/25-30/15-25/15-25，合计 125-170）做确定性裁剪："
                              "每类型收全 catch 样本，差额在 miss 样本内等距抽样（端点必含，保留变体多样性）。"
                              "未入池候选保留于 data/expansion_676c_F/ 可追溯。"),
        "failed": 0,
        "failed_ids": [],
        "by_type": by_type,
        "by_type_plan": plan_report,
        "severity": sev,
        "detector_mix": det_mix,
        "blind_spot_ratio": round(1 - catch_cnt / total, 3),
        "platform_dependent_ratio": round(pd_cnt / total, 3),
        "platform_dependent_count": pd_cnt,
        "selection_rule": "catch 全收 + miss 等距抽样（deterministic，无随机种子依赖）",
        "index": index,
    }
    with open(os.path.join(DST, "INDEX.json"), "w", encoding="utf-8") as f:
        json.dump(index_doc, f, ensure_ascii=False, indent=2)

    print(f"入池 {total} 个 → {DST}")
    for t, r in plan_report.items():
        print(f"  {t:<18} pooled={r['pooled']:>2} (catch {r['pooled_catch']} + miss {r['pooled_miss']})  规格{tuple(r['range'])}")
    print(f"  blind_spot_ratio={index_doc['blind_spot_ratio']}  platform_dependent={pd_cnt}/{total}")
    print(f"  severity={sev}  detector_mix={det_mix}")


if __name__ == "__main__":
    main()
