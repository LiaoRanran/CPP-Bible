#!/usr/bin/env python3
"""676h · A5 全量结果从原始矩阵独立重算（不信任 results 文件里的率）。

输入（只读）：
  data/a5_676f_detection_matrix.json  1137 样本 × 8 资产的逐格真实 verdict
  data/a5_676f_results.json           676f 分析产物（被检验对象）

重算口径与 data/676f_analysis.py 一致：
  * catch：该资产在评估集上 verdict == "catch"；
  * 组合（OR）：指定的资产集合中任一 catch ⇒ catch；unknown 绝不当 miss；
  * 评估集：manifest 登记的 split == "evaluation"（n=566）；
  * 派生 fail_hits：派生集（split=="derivation"）上该资产的 catch 数——FD 排序只许用它。

检查项（任一失败即非零退出）：
  R1 FD/Random/Static/full_pool 四臂在 k=4 的 catch 数与率逐位可重算；
  R2 逐资产派生 fail_hits 与 results 登记一致；
  R3 FD 的资产集 == 派生 fail_hits 最高的 k 个可用资产；
  R4 并列分析（剔除退化资产）：FD-vs-Random Δ=0、FD-vs-Static Δ 可重算并与登记一致；
  R5 退化资产（全 unknown）判定可重算。
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIX = "data/a5_676f_detection_matrix.json"
RESULTS = "data/a5_676f_results.json"
OUT = "data/676h_a5_recompute.json"


def load(rel):
    with open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    mx = load(MATRIX)
    res = load(RESULTS)
    samples = mx["samples"]
    assets = list(mx["assets"])
    checks = []

    def check(cid, name, ok, detail):
        checks.append({"id": cid, "name": name, "ok": bool(ok), "detail": detail})

    split = {s["sample_id"]: s for s in samples}
    der = [s for s in samples if s.get("split") == "derivation"]
    ev = [s for s in samples if s.get("split") == "evaluation"]

    def catch_count(rows, asset_set):
        n = 0
        for r in rows:
            if any(r["per_asset"].get(a) == "catch" for a in asset_set):
                n += 1
        return n

    # 派生集 fail_hits（每资产）
    der_hits = {a: sum(1 for r in der if r["per_asset"].get(a) == "catch") for a in assets}
    b4 = None
    for b in res["primary_main_8candidates"]["by_k"]:
        if b["budget_k"] == 4:
            b4 = b
            break
    if b4 is None:
        check("R0", "results 含 k=4 主端点", False, "未找到 budget_k=4")
        verdict = "fail"
    else:
        reg_hits = b4["arms"]["fd"]["fail_hits_rank"]
        same = all(der_hits.get(a, 0) == reg_hits.get(a) for a in reg_hits)
        check("R2", "逐资产派生 fail_hits 与登记一致", same,
              "重算 " + json.dumps(der_hits, sort_keys=True)[:200])

        # R1：四臂重算
        recomputed = {}
        for arm in ("fd", "random", "static", "fd_full_pool"):
            a_rec = b4["arms"][arm]
            got = catch_count(ev, a_rec["assets"])
            recomputed[arm] = {"assets": a_rec["assets"], "recomputed_k": got,
                               "registered_k": a_rec["k"],
                               "recomputed_rate_pct": round(100.0 * got / len(ev), 4),
                               "registered_rate_pct": round(a_rec["rate_pct"], 4)}
        r1_ok = all(v["recomputed_k"] == v["registered_k"] for v in recomputed.values())
        check("R1", "k=4 四臂 catch 数可从原始矩阵重算", r1_ok,
              "; ".join(f"{k}: {v['recomputed_k']}/{len(ev)} vs 登记 {v['registered_k']}"
                        for k, v in recomputed.items()))

        # R3：FD 资产集 == 派生 fail_hits 最高的 k 个"可用"资产
        usable = [a for a in assets if der_hits[a] + sum(
            1 for r in der if r["per_asset"].get(a) == "unknown") < len(der)]
        ranked = sorted(usable, key=lambda a: (-der_hits[a], a))
        fd_set = set(b4["arms"]["fd"]["assets"])
        check("R3", "FD 资产集 == 派生 fail_hits 排序前 k 个可用资产",
              fd_set == set(ranked[:4]),
              f"FD={sorted(fd_set)}；排名前 4={ranked[:4]}")

        # R5：退化资产（全 unknown）
        degen = [a for a in assets if all(r["per_asset"].get(a) == "unknown" for r in samples)]
        check("R5", "退化资产（全样本 unknown）可重算", set(degen) == {"compile-time", "wunsequenced"},
              f"重算退化集 {degen}")

    # R4：并列分析
    co = None
    for b in res["co_primary_excl_degenerate"]["by_k"]:
        if b["budget_k"] == 4:
            co = b
            break
    if co:
        ev_pool = assets
        fd_k = catch_count(ev, co["arms"]["fd"]["assets"])
        rnd_k = catch_count(ev, co["arms"]["random"]["assets"])
        st_k = catch_count(ev, co["arms"]["static"]["assets"])
        delta_rnd = 100.0 * (fd_k - rnd_k) / len(ev)
        delta_st = 100.0 * (fd_k - st_k) / len(ev)
        ok = (abs(delta_rnd - co["paired_tests"]["fd_vs_random"]["delta_pp"]) < 0.05
              and abs(delta_st - co["paired_tests"]["fd_vs_static"]["delta_pp"]) < 0.05)
        check("R4", "并列分析 Δ 可从原始矩阵重算", ok,
              f"重算 Δ(FD−Rnd)={delta_rnd:+.2f}pp（登记 "
              f"{co['paired_tests']['fd_vs_random']['delta_pp']:+.2f}）、"
              f"Δ(FD−Static)={delta_st:+.2f}pp（登记 "
              f"{co['paired_tests']['fd_vs_static']['delta_pp']:+.2f}）")

    # ---------------- R6：676g 能力边界从矩阵重算 ----------------
    bmx_path = os.path.join(ROOT, "data", "blindspot_676g_detection_matrix.json")
    bstats_path = os.path.join(ROOT, "data", "blindspot_676g_stats.json")
    blindspot = None
    if os.path.exists(bmx_path) and os.path.exists(bstats_path):
        bmx = json.load(open(bmx_path, encoding="utf-8"))
        bst = json.load(open(bstats_path, encoding="utf-8"))
        bs = bmx["samples"]
        # 结构性恒 unknown 的资产不参与 catch 判定（OR 口径等价于 6 个可用资产）
        usable = [a for a in bmx["assets"]
                  if any(r["per_asset"].get(a, {}).get("verdict") == "catch" for r in bs)]
        n = len(bs)
        n_catch = sum(1 for r in bs
                      if any(r["per_asset"].get(a, {}).get("verdict") == "catch" for a in usable))
        n_unk = sum(1 for r in bs
                    if all(r["per_asset"].get(a, {}).get("verdict") == "unknown" for a in usable))
        n_miss = n - n_catch - n_unk
        ratio = (n_miss + n_unk) / n
        tot = bst.get("total", {})
        ok = (n == tot.get("n") and n_catch == tot.get("catch") and n_miss == tot.get("miss")
              and abs(ratio - tot.get("blindspot_ratio", 0)) < 5e-4)
        check("R6", "676g 盲区统计可从矩阵重算", ok,
              f"重算 n={n} catch={n_catch} miss={n_miss} unknown={n_unk} "
              f"盲区比={ratio:.4f}；登记 n={tot.get('n')} catch={tot.get('catch')} "
              f"miss={tot.get('miss')} 盲区比={tot.get('blindspot_ratio')}（可用资产 {usable}）")
        comp = bst.get("complementarity", {})
        union_catch = sum(1 for r in bs
                          if any(r["per_asset"].get(a, {}).get("verdict") == "catch" for a in usable))
        ok2 = abs(union_catch / n - comp.get("all6_union_rate", 0)) < 5e-4
        check("R7", "676g 并集覆盖率可从矩阵重算", ok2,
              f"重算并集 {union_catch}/{n} = {100.0*union_catch/n:.1f}%；登记 "
              f"{100.0*comp.get('all6_union_rate', 0):.1f}%")
        blindspot = {"n": n, "catch": n_catch, "miss": n_miss, "unknown": n_unk,
                     "blindspot_ratio": ratio, "usable_assets": usable}

    verdict = "pass" if all(c["ok"] for c in checks) else "fail"
    doc = {
        "schema": "queyi-a5-recompute/676h",
        "generated_by": "tools/recompute_a5_676f.py",
        "matrix": MATRIX,
        "n_samples": len(samples),
        "n_derivation": len(der),
        "n_evaluation": len(ev),
        "derivation_fail_hits": der_hits,
        "arms_k4": locals().get("recomputed"),
        "blindspot_676g": blindspot,
        "checks": checks,
        "verdict": verdict,
    }
    with open(os.path.join(ROOT, OUT.replace("/", os.sep)), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)

    for c in checks:
        print(f"[a5-recompute] {'OK  ' if c['ok'] else 'FAIL'} {c['id']} {c['name']} — {c['detail']}")
    print(f"[a5-recompute] 判定 {verdict}（输出 {OUT}）")
    return 0 if verdict == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
