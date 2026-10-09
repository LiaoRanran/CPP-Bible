#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
705-C · 可视化素材生成（只读，不渲染图片，不调用 detect()）。

输入（冻结，只读）：
  - data/683_real_world_detection_matrix.json    （110 真实缺陷 8 资产判定）
  - data/blindspot_676g_stats.json               （1147 合成语料 34 类型 × 8 资产）
  - data/688_unique_hit_analysis.json            （独苗命中分布）
  - data/692_environment_report.md               （环境感知数字）

输出（本批产物）：
  - figures/data/*.json      （6-8 个数据文件）
  - figures/echarts/*.json   （对应 ECharts option，学术配色）
  - figures/README.md
  - figures/keynumbers.md
"""
import json
import os
import random

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")
FIG = os.path.join(REPO, "figures")
FIGD = os.path.join(FIG, "data")
FIGE = os.path.join(FIG, "echarts")
os.makedirs(FIGD, exist_ok=True)
os.makedirs(FIGE, exist_ok=True)

MATRIX = os.path.join(DATA, "683_real_world_detection_matrix.json")
BLIND = os.path.join(DATA, "blindspot_676g_stats.json")
UNIQUE = os.path.join(DATA, "688_unique_hit_analysis.json")
ASSETS = ["asan", "ubsan", "tsan", "compiler-warn", "wunsequenced",
          "cross-compile", "linker", "compile-time"]
# 有效资产（非恒 unknown）
EFF = ["asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"]


def load_matrix():
    with open(MATRIX, encoding="utf-8") as f:
        m = json.load(f)
    samples = []
    for s in m["samples"]:
        pa = s.get("per_asset", {})
        caught_by = set(a for a in ASSETS if pa.get(a, {}).get("verdict") == "catch")
        samples.append(caught_by)
    return m, samples


def greedy_order(samples):
    """贪心选择资产顺序（按边际 OR 覆盖增益）。"""
    remaining = list(ASSETS)
    chosen = []
    covered = set()
    while remaining:
        best, best_gain = None, -1
        for a in remaining:
            gain = sum(1 for i, sb in enumerate(samples)
                       if a in sb and i not in covered)
            if gain > best_gain:
                best, best_gain = a, gain
        chosen.append(best)
        remaining.remove(best)
        covered = set(i for i, sb in enumerate(samples) if sb & set(chosen))
    return chosen


def random_mean_cov(samples, k, n_iter=2000, seed=20261009):
    rnd = random.Random(seed)
    n = len(samples)
    tot = 0
    for _ in range(n_iter):
        sel = rnd.sample(ASSETS, k)
        cov = sum(1 for sb in samples if sb & set(sel))
        tot += cov
    return tot / (n_iter * n) * 100.0


def fd_vs_random_chart(samples):
    order = greedy_order(samples)
    fd = []
    rnd = []
    covered = set()
    for k in range(1, len(ASSETS) + 1):
        chosen = order[:k]
        covered = set(i for i, sb in enumerate(samples) if sb & set(chosen))
        fd.append(round(len(covered) / len(samples) * 100.0, 2))
        rnd.append(round(random_mean_cov(samples, k), 2))
    return {
        "title": "FD（贪心组合）vs Random 基线 · 真实靶场 110 条（k=1..8 资产数）",
        "caliber": "real-world 110 (683 frozen matrix)；资产顺序=贪心边际增益；"
                   "random=2000 次均匀随机 k-子集 OR 覆盖均值。论文合成帧等效锚点："
                   "684 greedy 4 资产=58.49% vs random_mean(full8)=42.52%（+15.97pp）。",
        "k": list(range(1, len(ASSETS) + 1)),
        "fd_greedy_pct": fd,
        "random_mean_pct": rnd,
        "greedy_asset_order": order,
    }


def heatmap_34x8():
    with open(BLIND, encoding="utf-8") as f:
        st = json.load(f)
    rows = st["by_type"]
    # 去重到唯一 defect_type（跨批次合并：catch/n 聚合），还原 34 类词表
    agg = {}
    for r in rows:
        dt = r["defect_type"]
        if dt not in agg:
            agg[dt] = {"catch": 0, "n": 0, "acr": {a: [0, 0] for a in ASSETS}}
        agg[dt]["catch"] += r.get("catch", 0)
        agg[dt]["n"] += r.get("n", 0)
        acr = r.get("asset_catch_rate", {})
        for a in ASSETS:
            v = acr.get(a, 0.0)
            # asset_catch_rate 是比例；转为 catch 计数需乘 n（近似）
            agg[dt]["acr"][a][0] += round(v * r.get("n", 0))
            agg[dt]["acr"][a][1] += r.get("n", 0)
    types = sorted(agg.keys())
    data = []
    for ti, dt in enumerate(types):
        for ai, a in enumerate(ASSETS):
            c, n = agg[dt]["acr"][a]
            v = round(c / n * 100.0, 2) if n else 0.0
            data.append([ai, ti, v])
    return {
        "title": f"能力边界热力图 · {len(types)} 缺陷类型 × 8 资产（合成语料 1147，catch%）",
        "caliber": "blindspot_676g_stats.json by_type（跨批次去重到唯一 defect_type 聚合）；"
                   "wunsequenced/compile-time 恒 0。",
        "assets": ASSETS,
        "types": types,
        "data": data,
    }


def environment_chart():
    return {
        "title": "环境感知对比 · WSL(g++) vs native(MinGW)（692 配对实验）",
        "caliber": "692_environment_report.md；E1=wsl-gcc-13.3(6 可捕获资产), "
                   "E2=windows-native-mingw(3 资产)。unaware 记账。",
        "frames": [
            {"frame": "A5 evaluation 566", "E1_catch_pct": 60.07, "E2_catch_pct": 24.74,
             "delta_pp": -35.34},
            {"frame": "真实靶场 110", "E1_catch_pct": 59.09, "E2_catch_pct": 23.64,
             "delta_pp": -35.45},
        ],
        "lost_by_asset_A5": {"asan": 60, "ubsan": 44, "tsan": 29, ">=2_assets": 67,
                              "total_lost": 200, "total_E1_catch": 340},
        "silent_fingerprint_delta_unknown_pp": 0.00,
        "conditional_recall_E2": "不可计算（分母为 0，aware 口径）",
    }


def realworld_vs_synthetic():
    # 683 §1.1
    return {
        "title": "真实 CVE vs 自造语料 · 逐资产 catch%（683 §1.1）",
        "caliber": "683_real_world_analysis.md §1.1；真实=110 真实缺陷，自造=1147 合成语料（同 8 资产）。",
        "assets": ASSETS,
        "real_pct": [49.09, 18.18, 22.73, 4.55, 0.0, 20.0, 0.0, 0.0],
        "synthetic_pct": [35.57, 23.54, 22.93, 12.47, 0.0, 10.64, 0.87, 0.0],
        "delta_pp": [13.52, -5.36, -0.2, -7.92, 0.0, 9.36, -0.87, 0.0],
        "note": "z 检验：asan p=0.005 / cross-compile p=0.003（真实更强）；"
                "compiler-warn p=0.014（真实更弱）；总体 OR 真实 59.09% vs 自造 61.64% "
                "无显著差异（z=-0.52, p=0.60）。",
    }


def unique_hit_chart():
    with open(UNIQUE, encoding="utf-8") as f:
        u = json.load(f)
    return {
        "title": "检测器独苗命中分布（真实靶场 110，688）",
        "caliber": "688_unique_hit_analysis.json；n_unique_hit=27（占 catch 41.5%）。",
        "sole_catcher_counts": u["sole_catcher_counts"],
        "unique_hit_by_type": u["unique_hit_by_type"],
        "n_or_catch": u["n_or_catch"],
        "n_unique_hit": u["n_unique_hit"],
        "unique_fraction_pct": u["unique_fraction_pct"],
    }


def per_asset_110():
    with open(MATRIX, encoding="utf-8") as f:
        m = json.load(f)
    pas = m["per_asset_summary"]
    return {
        "title": "逐资产 catch 表现 · 真实靶场 110（683 矩阵）",
        "caliber": "683_real_world_detection_matrix.json per_asset_summary。",
        "assets": ASSETS,
        "catch": [pas[a]["catch"] for a in ASSETS],
        "miss": [pas[a]["miss"] for a in ASSETS],
        "unknown": [pas[a]["unknown"] for a in ASSETS],
        "catch_pct": [round(pas[a]["catch_rate_pct"], 2) for a in ASSETS],
    }


def realworld_by_type():
    # 683 §1.2
    rows = [
        ("out_of_bounds", 38, 84.21), ("logic_error", 31, 3.23),
        ("integer_overflow", 14, 71.43), ("use_after_free", 10, 100.0),
        ("null_pointer_deref", 6, 100.0), ("data_race", 4, 75.0),
        ("type_punning", 4, 0.0), ("double_free", 2, 100.0),
        ("memory_leak", 1, 100.0),
    ]
    return {
        "title": "真实靶场按缺陷类型 OR 检出率（683 §1.2）",
        "caliber": "683_real_world_analysis.md §1.2。",
        "types": [r[0] for r in rows],
        "n": [r[1] for r in rows],
        "or_catch_pct": [r[2] for r in rows],
    }


def four_type_family_drift():
    """四型（家族）真实 vs 合成 catch% 漂移（real-world 110 by_type 分组 + 合成 1147 by family）。"""
    with open(MATRIX, encoding="utf-8") as f:
        m = json.load(f)
    fam_real = {"memory_safety": set(), "undefined_behavior": set(),
                "concurrency": set(), "logic_error": set()}
    for s in m["samples"]:
        dt = s["defect_type"]
        pa = s.get("per_asset", {})
        catch = any(pa.get(a, {}).get("verdict") == "catch" for a in ASSETS)
        if dt in ("out_of_bounds", "use_after_free", "null_pointer_deref",
                  "double_free", "memory_leak"):
            fam_real["memory_safety"].add((s["rw_id"], catch))
        elif dt in ("integer_overflow", "type_punning"):
            fam_real["undefined_behavior"].add((s["rw_id"], catch))
        elif dt == "data_race":
            fam_real["concurrency"].add((s["rw_id"], catch))
        elif dt == "logic_error":
            fam_real["logic_error"].add((s["rw_id"], catch))
    real_or = {}
    for fam, items in fam_real.items():
        n = len(items)
        c = sum(1 for _, ok in items if ok)
        real_or[fam] = round(c / n * 100.0, 2) if n else None
    # 合成 1147 家族 OR%（来自 683 §3 记忆：剔除 logic/挂起后内存安全族 79 条 OR=81.01%；
    # 但按家族精确值需 blindspot；此处用 683 报告口径近似值，标注来源）
    # 用 blindspot by_type family 聚合
    with open(BLIND, encoding="utf-8") as f:
        st = json.load(f)
    fam_syn = {"memory_safety": [0, 0], "undefined_behavior": [0, 0],
               "concurrency": [0, 0], "logic_error": [0, 0]}
    # blindspot by_type 无 logic 家族（合成语料逻辑类极少）；用其 family 字段聚合
    for r in st["by_type"]:
        fam = r.get("family")
        if fam in fam_syn:
            fam_syn[fam][0] += r["catch"]
            fam_syn[fam][1] += r["n"]
    syn_or = {fam: round(v[0] / v[1] * 100.0, 2) if v[1] else None
              for fam, v in fam_syn.items()}
    return {
        "title": "四型（缺陷家族）真实 vs 合成 catch% 结构性漂移（705-C 代理指标）",
        "caliber": "真实=683 110 by_type 分组聚合；合成=blindspot_676g_stats by family 聚合。"
                   "注：精确「Goodhart 漂移量」未在本批冻结数据中独立核算 → 本图以四家族真实/合成 OR% 差"
                   "作为结构性漂移的代理指标，最终采用权在作者。",
        "families": list(real_or.keys()),
        "real_or_pct": [real_or[f] for f in real_or],
        "synthetic_or_pct": [syn_or.get(f) for f in real_or],
        "status": "代理指标（精确 Goodhart 漂移量待补）",
    }


# ---------------- ECharts option 生成（学术配色）----------------
PALETTE = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
           "#EDC948", "#B07AA1", "#9C755F"]
GRID = {"left": 60, "right": 30, "top": 60, "bottom": 60}


def line_option(title, xname, yname, series):
    return {
        "title": {"text": title, "left": "center",
                  "textStyle": {"fontSize": 14, "color": "#333"}},
        "tooltip": {"trigger": "axis"},
        "legend": {"top": 30, "textStyle": {"fontSize": 11}},
        "grid": GRID,
        "xAxis": {"type": "category", "name": xname, "nameLocation": "middle",
                  "nameGap": 30, "data": series["x"]},
        "yAxis": {"type": "value", "name": yname, "min": 0, "max": 100},
        "series": series["s"],
        "color": PALETTE,
    }


def bar_option(title, cats, series, yname="%"):
    return {
        "title": {"text": title, "left": "center",
                  "textStyle": {"fontSize": 14, "color": "#333"}},
        "tooltip": {"trigger": "axis"},
        "legend": {"top": 30, "textStyle": {"fontSize": 11}},
        "grid": GRID,
        "xAxis": {"type": "category", "data": cats, "axisLabel": {"fontSize": 10}},
        "yAxis": {"type": "value", "name": yname},
        "series": series,
        "color": PALETTE,
    }


def heat_option(title, types, assets, data):
    return {
        "title": {"text": title, "left": "center",
                  "textStyle": {"fontSize": 13, "color": "#333"}},
        "tooltip": {"position": "top"},
        "grid": {"left": 160, "right": 30, "top": 50, "bottom": 60},
        "xAxis": {"type": "category", "data": assets, "splitArea": {"show": True}},
        "yAxis": {"type": "category", "data": types, "splitArea": {"show": True}},
        "visualMap": {"min": 0, "max": 100, "calculable": True, "orient": "horizontal",
                      "left": "center", "bottom": 10, "inRange": {"color":
                      ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"]}},
        "series": [{"name": "catch%", "type": "heatmap", "data": data,
                    "label": {"show": True, "fontSize": 8}}],
    }


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def main():
    m, samples = load_matrix()
    # 1. FD vs Random
    fd = fd_vs_random_chart(samples)
    write_json(os.path.join(FIGD, "fd_vs_random.json"), fd)
    write_json(os.path.join(FIGE, "fd_vs_random.json"), line_option(
        fd["title"], "k (资产数)", "OR catch%",
        {"x": fd["k"],
         "s": [{"name": "FD (greedy)", "type": "line", "data": fd["fd_greedy_pct"],
                "smooth": True, "symbolSize": 7},
               {"name": "Random mean", "type": "line", "data": fd["random_mean_pct"],
                "smooth": True, "symbolSize": 7, "lineStyle": {"type": "dashed"}}]}))

    # 2. heatmap 34x8
    hm = heatmap_34x8()
    write_json(os.path.join(FIGD, "capability_heatmap_34x8.json"), hm)
    write_json(os.path.join(FIGE, "capability_heatmap_34x8.json"),
               heat_option(hm["title"], hm["types"], hm["assets"], hm["data"]))

    # 3. environment
    env = environment_chart()
    write_json(os.path.join(FIGD, "environment_wsl_vs_native.json"), env)
    cats = [f["frame"] for f in env["frames"]]
    write_json(os.path.join(FIGE, "environment_wsl_vs_native.json"), bar_option(
        env["title"], cats,
        [{"name": "E1 WSL", "type": "bar", "data": [f["E1_catch_pct"] for f in env["frames"]]},
         {"name": "E2 native", "type": "bar", "data": [f["E2_catch_pct"] for f in env["frames"]]}]))

    # 4. realworld vs synthetic
    rv = realworld_vs_synthetic()
    write_json(os.path.join(FIGD, "realworld_vs_synthetic.json"), rv)
    write_json(os.path.join(FIGE, "realworld_vs_synthetic.json"), bar_option(
        rv["title"], rv["assets"],
        [{"name": "真实 CVE", "type": "bar", "data": rv["real_pct"]},
         {"name": "自造语料", "type": "bar", "data": rv["synthetic_pct"]}]))

    # 5. unique hit
    uh = unique_hit_chart()
    write_json(os.path.join(FIGD, "unique_hit_distribution.json"), uh)
    write_json(os.path.join(FIGE, "unique_hit_distribution.json"), bar_option(
        "独苗命中资产分布（27 条）", list(uh["sole_catcher_counts"].keys()),
        [{"name": "sole-catcher count", "type": "bar",
          "data": list(uh["sole_catcher_counts"].values())}], yname="条数"))

    # 6. per-asset 110
    pa = per_asset_110()
    write_json(os.path.join(FIGD, "per_asset_catch_110.json"), pa)
    write_json(os.path.join(FIGE, "per_asset_catch_110.json"), bar_option(
        pa["title"], pa["assets"],
        [{"name": "catch", "type": "bar", "data": pa["catch"]},
         {"name": "miss", "type": "bar", "data": pa["miss"]},
         {"name": "unknown", "type": "bar", "data": pa["unknown"]}], yname="条数"))

    # 7. realworld by type
    rt = realworld_by_type()
    write_json(os.path.join(FIGD, "realworld_by_type.json"), rt)
    write_json(os.path.join(FIGE, "realworld_by_type.json"), bar_option(
        rt["title"], rt["types"],
        [{"name": "OR catch%", "type": "bar", "data": rt["or_catch_pct"]}]))

    # 8. four-type drift
    ft = four_type_family_drift()
    write_json(os.path.join(FIGD, "four_type_family_drift.json"), ft)
    write_json(os.path.join(FIGE, "four_type_family_drift.json"), bar_option(
        ft["title"], ft["families"],
        [{"name": "真实 OR%", "type": "bar", "data": ft["real_or_pct"]},
         {"name": "合成 OR%", "type": "bar", "data": ft["synthetic_or_pct"]}]))

    # README
    readme = ["# 705-C · 可视化素材说明", "",
              "所有图表为**数据文件 + ECharts 配置**，未渲染图片。配色学术风格（蓝/橙/红/青）。",
              "数字均来自冻结批次（683/684/688/692/blindspot_676g），与论文一致；缺失项标「待补」。",
              "",
              "## 图表清单", ""]
    charts = [
        ("fd_vs_random", "FD（贪心组合）vs Random 基线，k=1..8（真实靶场 110 复算；论文合成帧锚点 684 greedy 58.49% vs random 42.52%）", "论文 Figure：组合增益 / 子模"),
        ("capability_heatmap_34x8", "70 细粒度缺陷类型（34 类词表的细粒度展开）× 8 资产 catch% 热力图（合成 1147）", "论文 Figure：能力边界地图"),
        ("environment_wsl_vs_native", "WSL vs native 环境感知对比（692，−35pp）", "论文 Appendix：环境感知"),
        ("realworld_vs_synthetic", "真实 CVE vs 自造语料逐资产 catch%（683 §1.1）", "论文 Real-World Validation"),
        ("unique_hit_distribution", "独苗命中资产分布（27 条，占比 41.5%）", "论文：资产互补性"),
        ("per_asset_catch_110", "逐资产 catch/miss/unknown（真实靶场 110）", "论文：逐资产基线"),
        ("realworld_by_type", "真实靶场按缺陷类型 OR 检出率", "论文：类型级分析"),
        ("four_type_family_drift", "四家族真实 vs 合成 OR% 漂移（代理指标，精确 Goodhart 漂移量待补）", "论文：结构性漂移"),
    ]
    for cid, desc, where in charts:
        readme.append(f"- **{cid}**：{desc}  → 放 `{where}`")
        readme.append(f"  - 数据：`figures/data/{cid}.json` ｜ ECharts：`figures/echarts/{cid}.json`")
    readme.extend(["", "## 怎么用",
                   "- 把 `figures/echarts/<id>.json` 内容贴入 ECharts 官网 `setOption()` 即可预览。",
                   "- 数据文件为纯 JSON，可喂任意绘图库（matplotlib/vega/plotly）。", "",
                   "## 诚实边界",
                   "- `four_type_family_drift` 的精确 Goodhart 漂移量在本批冻结数据中未独立核算，图以四家族真实/合成 OR% 差作代理。",
                   "- 所有数字绑定「本 8 资产 + 本工具链」口径；环境类数字来自 692 配对实验（只读冻结矩阵）。"])
    with open(os.path.join(FIG, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(readme))

    # keynumbers
    keynums = ["# 705-C · 演讲用关键数字卡片", "",
               "> 10 个最有冲击力的数字，每个配一句话，可直接进 slides。", ""]
    kn = [
        ("59.09%", "真实靶场 110 条缺陷的 8 资产 OR 检出率——与自造语料 61.64% 无显著差异（p=0.60），'真实一定更难'被证伪。"),
        ("41.5%", "110 条 catch 中 27 条为独苗命中：没有单一资产足够，OR 组合的价值由这些样本直接支撑。"),
        ("+15.97pp", "FD 贪心组合（58.49%）相对 Random 均值（42.52%）的增益（684，1137 样本），且贪心=最优 ratio 1.0。"),
        ("−35.34pp", "换 deployment profile（WSL→native）使 catch 从 60.07% 暴跌到 24.74%（692）——环境是测量的一部分，不是复现细节。"),
        ("0.00pp", "692 静默退化的可检验指纹：Δunknown=0，'没测'被写成'测了没中'，200/340 丢失捕获其实是真阳性。"),
        ("3.23%", "logic_error 族 OR 检出率——逻辑/协议缺陷在内存/UB 检测器下几乎不可观测，点出能力边界。"),
        ("100.0%", "use_after_free / null_pointer_deref / double_free / memory_leak 族在真实靶场的 OR 检出率——asan 主力覆盖。"),
        ("18 / 3 / 3 / 3", "独苗命中资产分布：asan 18、cross-compile 3、tsan 3、ubsan 3——asan 贡献最大（与 682 Shapley +19.53pp 一致）。"),
        ("93.5%", "clang 18 vs g++ 13.3 跨工具链一致率（689），且 Δcatch≤2pp——同 OS 换编译器几乎无感（与换 profile 的 −35pp 对比强烈）。"),
        ("110 / 1137", "真实缺陷 110 条 + 合成语料 1137 条双基准；真实靶场把证据从'自造样本'推进到'真实缺陷类别重构'，提升生态效度。"),
    ]
    for v, desc in kn:
        keynums.append(f"- **{v}** — {desc}")
    with open(os.path.join(FIG, "keynumbers.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(keynums))

    print("[done] 8 数据文件 + 8 ECharts + README + keynumbers")


if __name__ == "__main__":
    main()
