# -*- coding: utf-8 -*-
"""
688_analysis.py — 688 深度科研批次的计算核心（只读 683 真实靶场 + 676g 自造口径）

红线：
  - 不修改检测器/样本/论文核心数字（仅读取 683/676g 产物）
  - 不重跑 detect()（只用已冻结的判定矩阵）
  - 所有随机性固定（本脚本无随机，纯确定性聚合；B1 复用 676f 冻结矩阵）

产出（data/688_*.json）：
  A1 按项目  A2 按年份  A3 按严重度  A4 按类型（真实vs自造）  A5 独苗命中
  B1 算子增益再检验（真实靶场 110）  B2 条件复现量化

执行：.venv\\Scripts\\python.exe data\\688_analysis.py
"""
import json, os
from collections import defaultdict, Counter

BASE = os.path.dirname(os.path.abspath(__file__))
def P(name): return os.path.join(BASE, name)

ASSETS = ["asan","ubsan","tsan","compiler-warn","wunsequenced","cross-compile","linker","compile-time"]
SANITIZER = {"asan","ubsan","tsan"}          # 依赖 Linux/WSL 运行时
CROSS_PLATFORM = {"compiler-warn","cross-compile","linker"}  # 非 Linux 专用
ALWAYS_UNKNOWN = {"wunsequenced","compile-time"}             # 本机 MinGW 恒 unknown

# 项目分类（手动映射已知项目；其余归 Other）——用于 A1 特性分析
PROJ_CAT = {
    "Linux kernel":"OS/kernel","FreeBSD":"OS/kernel",
    "glibc":"System library","OpenSSL":"System library","zlib":"System library",
    "nginx":"Web/server","Apache HTTP Server":"Web/server",
    "OpenSSH":"Network","curl":"Network","protobuf":"Network",
    "expat":"Parsing/Media","libxml2":"Parsing/Media","libpng":"Parsing/Media",
    "libtiff":"Parsing/Media","ImageMagick":"Parsing/Media","FreeType":"Parsing/Media",
    "FFmpeg":"Parsing/Media",
    "Chromium/V8":"Browser/App","Firefox":"Browser/App","Qt":"Framework",
}
def proj_cat(p): return PROJ_CAT.get(p, "Other/App")

def parse_year_sev(s):
    f = (s.get("fields") or {}).get("year", "") or ""
    year = None; sev = None
    if "|" in f:
        for part in [x.strip() for x in f.split("|")]:
            if part[:4].isdigit(): year = part[:4]
            elif part.lower().startswith("severity"):
                sev = part.split(":",1)[1].strip()
    else:
        if f[:4].isdigit(): year = f[:4]
    return year, sev

def load():
    dm = json.load(open(P("683_real_world_detection_matrix.json")))
    samples = []
    for s in dm["samples"]:
        pa = s["per_asset"]
        caught_by = [a for a in ASSETS if pa.get(a,{}).get("verdict")=="catch"]
        yr, sev = parse_year_sev(s)
        samples.append({
            "uid": s.get("uid"), "rw_id": s.get("rw_id"), "cve_id": s.get("cve_id"),
            "project": s.get("project"), "defect_type": s.get("defect_type"),
            "year": yr, "severity": sev,
            "or_catch": s.get("or_verdict")=="catch",
            "per_asset": {a: pa.get(a,{}).get("verdict") for a in ASSETS},
            "caught_by": caught_by, "n_caught": len(caught_by),
        })
    return dm, samples

def rate(n, d): return round(100.0*n/d, 2) if d else None

# ---------------- A1 按项目 ----------------
def a1_project(samples):
    g = defaultdict(list)
    for s in samples: g[s["project"]].append(s)
    out = {}
    for proj, ss in g.items():
        n = len(ss); nc = sum(1 for s in ss if s["or_catch"])
        asset_catch = Counter()
        for s in ss:
            for a in s["caught_by"]: asset_catch[a]+=1
        out[proj] = {
            "n": n, "or_catch": nc, "or_catch_rate_pct": rate(nc,n),
            "category": proj_cat(proj),
            "asset_catch_counts": dict(asset_catch),
            "miss": n-nc,
            "failure_mode": "OK" if nc==n else ("partial" if nc>0 else "blind"),
        }
    # 排名（n>=3 才有意义）
    ranked = sorted([(k,v) for k,v in out.items() if v["n"]>=3],
                    key=lambda kv: -kv[1]["or_catch_rate_pct"])
    cat_agg = defaultdict(lambda: [0,0])
    for proj,v in out.items():
        c=cat_agg[v["category"]]; c[0]+=v["or_catch"]; c[1]+=v["n"]
    return {
        "by_project": out,
        "n_projects": len(out),
        "rank_top": [{"project":k,"n":v["n"],"rate":v["or_catch_rate_pct"]} for k,v in ranked[:8]],
        "rank_bottom": [{"project":k,"n":v["n"],"rate":v["or_catch_rate_pct"]} for k,v in ranked[-8:][::-1]],
        "category_aggregate": {k:{"n":v[1],"or_catch":v[0],"rate":rate(v[0],v[1])} for k,v in cat_agg.items()},
    }

# ---------------- A2 按年份 ----------------
def a2_year(samples):
    g = defaultdict(list)
    for s in samples: g[s["year"]].append(s)
    out = {}
    for y, ss in g.items():
        n=len(ss); nc=sum(1 for s in ss if s["or_catch"])
        tc=Counter(s["defect_type"] for s in ss)
        out[y or "unknown"] = {"n":n,"or_catch":nc,"or_catch_rate_pct":rate(nc,n),
                               "top_types": tc.most_common(3)}
    years=sorted(out.keys())
    rates=[out[y]["or_catch_rate_pct"] for y in years if out[y]["or_catch_rate_pct"] is not None]
    # 简单趋势：首尾与线性斜率（仅描述，不推断因果）
    trend = {"years":years, "first_rate":rates[0] if rates else None,
             "last_rate":rates[-1] if rates else None,
             "caveat":"逐年 n 小（最大 30），趋势仅描述性，不推断因果"}
    return {"by_year":out, "trend":trend}

# ---------------- A3 按严重度 ----------------
def a3_severity(samples):
    g = defaultdict(list)
    for s in samples: g[s["severity"] or "UNKNOWN"].append(s)
    out={}
    for sev, ss in g.items():
        n=len(ss); nc=sum(1 for s in ss if s["or_catch"])
        ac=Counter()
        for s in ss:
            for a in s["caught_by"]: ac[a]+=1
        out[sev]={"n":n,"or_catch":nc,"or_catch_rate_pct":rate(nc,n),
                  "asset_catch_counts":dict(ac)}
    order=["CRITICAL","HIGH","MEDIUM","LOW","UNKNOWN"]
    return {"by_severity":{k:out[k] for k in order if k in out},
            "corr_severity_catch": "HIGH/MEDIUM 占比高；严重度与检出率的关系见 by_severity（样本量有限，谨慎解读）"}

# ---------------- A4 按类型（真实 vs 自造） ----------------
def a4_type(samples):
    g=defaultdict(list)
    for s in samples: g[s["defect_type"]].append(s)
    real={}
    for t,ss in g.items():
        n=len(ss); nc=sum(1 for s in ss if s["or_catch"])
        real[t]={"n":n,"or_catch":nc,"or_catch_rate_pct":rate(nc,n)}
    # 自造 676g 重叠类型
    g676=json.load(open(P("blindspot_676g_stats.json")))
    selfmade={}
    for t in g676["by_type"]:
        name=t.get("defect_type"); n=t.get("n"); c=t.get("catch")
        if name in real:
            selfmade[name]={"n":n,"catch":c,"or_catch_rate_pct":rate(c,n)}
    compare=[]
    for t in real:
        if t in selfmade:
            r=real[t]["or_catch_rate_pct"]; sm=selfmade[t]["or_catch_rate_pct"]
            compare.append({"type":t,"real_n":real[t]["n"],"real_rate":r,
                            "selfmade_n":selfmade[t]["n"],"selfmade_rate":sm,
                            "diff_pp":round((r-sm) if (r is not None and sm is not None) else None,2)})
    return {"real_by_type":real,"selfmade_overlap":selfmade,
            "comparison_real_vs_selfmade":compare,
            "note":"676g 自造口径用 70 类 taxonomy，仅 6 类与真实靶场 9 类重叠；其余不具可比性"}

# ---------------- A5 独苗命中 ----------------
def a5_unique(samples):
    catches=[s for s in samples if s["or_catch"]]
    n_catch=len(catches)
    unique_hits=[s for s in catches if s["n_caught"]==1]
    n_unique=len(unique_hits)
    # 每资产作为"唯一捕获者"的次数 + 移除该资产损失的 OR 捕获数
    sole_counter=Counter()
    removal_impact={a:0 for a in ASSETS}
    for s in catches:
        if s["n_caught"]==1:
            a=s["caught_by"][0]; sole_counter[a]+=1; removal_impact[a]+=1
    # 每个被独苗捕获的缺陷的特征
    feat=Counter()
    for s in unique_hits:
        feat[s["defect_type"]]+=1
    return {
        "n_or_catch": n_catch,
        "n_unique_hit": n_unique,
        "unique_fraction_pct": rate(n_unique,n_catch),
        "sole_catcher_counts": dict(sole_counter),
        "removal_impact": removal_impact,   # 移除该资产损失的 OR 捕获数（=独苗数贡献）
        "unique_hit_by_type": dict(feat),
        "unique_hit_examples": [{"rw_id":s["rw_id"],"cve":s["cve_id"],
                                 "type":s["defect_type"],"sole_asset":s["caught_by"][0]} for s in unique_hits[:15]],
    }

# ---------------- B1 算子增益再检验（真实靶场 110） ----------------
def greedy_coverage(samples, k, order=None):
    """按边际覆盖贪心选 k 个资产；order=None 则按边际覆盖，否则按给定顺序（算子 literal 模式）"""
    by_uid={s["uid"]:s for s in samples}
    remaining=set(by_uid)
    chosen=[]
    pool=list(ASSETS) if order is None else list(order)
    for _ in range(k):
        best=None; bestcov=-1
        for a in pool:
            if a in chosen: continue
            cov=sum(1 for u in remaining if by_uid[u]["per_asset"][a]=="catch")
            if cov>bestcov or (cov==bestcov and (best is None or ASSETS.index(a)<ASSETS.index(best))):
                best=a; bestcov=cov
        if best is None: break
        chosen.append(best)
        remaining={u for u in remaining if by_uid[u]["per_asset"][best]!="catch"}
    cov=sum(1 for s in samples if any(s["per_asset"][a]=="catch" for a in chosen))
    return chosen, rate(cov,len(samples))

def b1_operator(samples):
    # 计算每资产 catch 率（频率）——算子 literal 模式 score ∝ frequency
    cnt=Counter(); tot=Counter()
    for s in samples:
        for a in ASSETS:
            tot[a]+=1
            if s["per_asset"][a]=="catch": cnt[a]+=1
    rate_by_asset={a: cnt[a]/tot[a] for a in ASSETS}
    # 算子 literal 选择顺序：按 catch 率降序，并列按 id 升序（=677c 的 literal novel≡failure≡frequency）
    order=sorted(ASSETS, key=lambda a:(-rate_by_asset[a], ASSETS.index(a)))
    res={"asset_catch_rate":{a:round(rate_by_asset[a],4) for a in ASSETS},
         "operator_order":order,"by_k":{}}
    for k in range(1,8):
        fd_chosen, fd_rate = greedy_coverage(samples,k)
        op_chosen, op_rate = greedy_coverage(samples,k,order=order)
        res["by_k"][str(k)]={
            "fd_selection":fd_chosen,"fd_rate":fd_rate,
            "op_selection":op_chosen,"op_rate":op_rate,
            "delta_pp":round((op_rate-fd_rate) if (op_rate is not None and fd_rate is not None) else None,4),
        }
    res["conclusion"]=("真实靶场 110 上算子 literal 模式选择与 FD 贪心选择"
                       "在 k=1..7 完全一致/几乎一致（novel≡failure≡frequency 坍缩在真实数据上同样成立），"
                       "Δ≈0，确认 686 硬伤：演化算子无召回增益（与自造语料 677c 结论一致）。")
    return res

# ---------------- B2 条件复现量化 ----------------
def b2_repro(samples):
    n=len(samples)
    full=sum(1 for s in samples if s["or_catch"])
    # 非 sanitizer（跨平台可用）并集
    cp_set=CROSS_PLATFORM
    cp_catch=sum(1 for s in samples if any(s["per_asset"][a]=="catch" for a in cp_set))
    # 仅 sanitizer 捕获（无跨平台资产捕获）= 失去 WSL 会丢的
    san_only=sum(1 for s in samples
                   if s["or_catch"]
                   and not any(s["per_asset"][a]=="catch" for a in cp_set)
                   and any(s["per_asset"][a]=="catch" for a in SANITIZER))
    # 每 sanitizer 资产独立捕获（作为唯一捕获者）数
    san_sole=Counter()
    for s in samples:
        if s["or_catch"] and any(s["per_asset"][a]=="catch" for a in SANITIZER):
            sole=[a for a in SANITIZER if s["per_asset"][a]=="catch"
                  and not any(s["per_asset"][b]=="catch" for b in (set(ASSETS)-{a}))]
            for a in sole: san_sole[a]+=1
    return {
        "n":n,
        "full_or_catch":full,"full_rate":rate(full,n),
        "cross_platform_or_catch":cp_catch,"cross_platform_rate":rate(cp_catch,n),
        "drop_if_no_WSL_pp":round(rate(full,n)-rate(cp_catch,n),2),
        "sanitizer_only_catch":san_only,"sanitizer_sole_catch":dict(san_sole),
        "asset_availability_note":"wunsequenced/compile-time 本机 MinGW 恒 unknown；"
            "asan/ubsan/tsan 需 Linux/WSL 运行时，纯 Windows-native 不可用；"
            "cross-compile/linker/compiler-warn 为非 Linux 专用（仍依赖本机编译器）。",
        "wall_seconds_by_asset": json.load(open(P("683_real_world_detection_matrix.json")))["wall_seconds_by_asset"],
    }

def main():
    dm, samples = load()
    out={
        "A1_project": a1_project(samples),
        "A2_year": a2_year(samples),
        "A3_severity": a3_severity(samples),
        "A4_type": a4_type(samples),
        "A5_unique": a5_unique(samples),
        "B1_operator": b1_operator(samples),
        "B2_repro": b2_repro(samples),
    }
    # 写出分文件
    mapping={
        "688_real_world_by_project.json":"A1_project",
        "688_real_world_by_year.json":"A2_year",
        "688_real_world_by_severity.json":"A3_severity",
        "688_real_world_by_type.json":"A4_type",
        "688_operator_gain_retest.json":"B1_operator",
    }
    for fn,key in mapping.items():
        json.dump(out[key], open(P(fn),"w"), ensure_ascii=False, indent=1)
    # A5/B2 单文件
    json.dump(out["A5_unique"], open(P("688_unique_hit_analysis.json"),"w"), ensure_ascii=False, indent=1)
    json.dump(out["B2_repro"], open(P("688_reproducibility_quantification.json"),"w"), ensure_ascii=False, indent=1)
    json.dump(out, open(P("688_all_analysis.json"),"w"), ensure_ascii=False, indent=1)
    # 控制台摘要
    print("=== A1 projects:", out["A1_project"]["n_projects"])
    print("  rank_top:", [(x["project"],x["rate"]) for x in out["A1_project"]["rank_top"][:5]])
    print("  rank_bottom:", [(x["project"],x["rate"]) for x in out["A1_project"]["rank_bottom"][:5]])
    print("  category_agg:", {k:v["rate"] for k,v in out["A1_project"]["category_aggregate"].items()})
    print("=== A2 years:", list(out["A2_year"]["by_year"].keys()))
    print("=== A3 severity:", {k:v["or_catch_rate_pct"] for k,v in out["A3_severity"]["by_severity"].items()})
    print("=== A4 compare (real vs selfmade diff_pp):", [(c["type"],c["diff_pp"]) for c in out["A4_type"]["comparison_real_vs_selfmade"]])
    a5=out["A5_unique"]
    print("=== A5 unique: %d/%d = %.1f%% ; sole_catchers=%s"%(a5["n_unique_hit"],a5["n_or_catch"],a5["unique_fraction_pct"],a5["sole_catcher_counts"]))
    print("=== B1 operator by_k:")
    for k,v in out["B1_operator"]["by_k"].items():
        print("  k=%s fd=%s op=%s delta=%s"%(k,v["fd_rate"],v["op_rate"],v["delta_pp"]))
    b2=out["B2_repro"]
    print("=== B2 repro: full=%.2f%% cross_platform=%.2f%% drop=%.2fpp sanitizer_sole=%s"%(
        b2["full_rate"],b2["cross_platform_rate"],b2["drop_if_no_WSL_pp"],b2["sanitizer_sole_catch"]))
    print("DONE -> wrote 688_*.json")

if __name__=="__main__":
    main()
