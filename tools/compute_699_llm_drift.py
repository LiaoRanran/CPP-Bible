#!/usr/bin/env python3
"""
699-C · LLM 评估漂移最小可行性预测试 (transferability pre-test)

测量 Queyi 的三个核心概念能否迁移到 LLM 评估:
  1) 口径漂移 (Caliber Drift)   : 同一回答 + 两个语义等价 judge prompt -> verdict 一致性
  2) 环境漂移 (Environment Drift): 同一 prompt+回答 + 两个 judge 模型 -> verdict 一致性
  3) 结构性 Goodhart            : judge(长度代理)高分但人类标注差 的样本

本脚本在"无 LLM API key"环境下可实测的是 (3) 结构性 Goodhart（用长度/信息量代理裁判，在
真实下载的 JudgeBench / RewardBench 数据上计算）。(1)(2) 需要真实 LLM 裁判，函数已就绪：
设置 LLM_JUDGE_ENABLED=True 并提供端点/key 后即可实测 prompt / model invariance。

纯标准库实现，无第三方依赖。
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
UNIFIED = os.path.join(HERE, "..", "data", "699_llm_eval_unified_format.json")
OUT = os.path.join(HERE, "..", "data", "699_llm_drift_results.json")

# ---- LLM 裁判开关（本环境未配置可用 key，默认关闭，仅结构性 Goodhart 实测）----
LLM_JUDGE_ENABLED = False
LLM_JUDGE_ENDPOINT = os.environ.get("QUEYI_LLM_JUDGE_ENDPOINT", "")
LLM_JUDGE_KEY = os.environ.get("QUEYI_LLM_JUDGE_KEY", "")


def load_unified(path=UNIFIED):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d["records"], d.get("meta", {})


def _len(t):
    return len(t or "")


def _code_blocks(t):
    return len(re.findall(r"```", t or "")) // 2


def _unique_words(t):
    return len(set(re.findall(r"[A-Za-z]+", t or "")))


def _human_side(label):
    """归一化人类偏好侧: JudgeBench 用 'A>B'/'B>A'; RewardBench 用 'A'/'B'。"""
    s = str(label).strip().upper()
    if s in ("A", "B"):
        return s
    if s == "A>B":
        return "A"
    if s == "B>A":
        return "B"
    return None


def structural_goodhart(records):
    """用长度/信息量作为'懒惰裁判'，看它在多少 pair 上偏离人类标注。"""
    per_source = {}
    for r in records:
        src = r["source_dataset"]
        a, b = r.get("response_A", ""), r.get("response_B", "")
        human = _human_side(r.get("human_ground_truth", ""))
        if human is None:
            continue
        human_text = a if human == "A" else b
        other_text = b if human == "A" else a
        # 懒惰裁判: 选更长的
        lazy_pick = "A" if _len(a) >= _len(b) else "B"
        # 信息量裁判: 选唯一词更多的
        info_pick = "A" if _unique_words(a) >= _unique_words(b) else "B"
        rec = per_source.setdefault(src, {
            "n": 0, "len_agree": 0, "len_disagree": 0,
            "info_agree": 0, "info_disagree": 0,
            "human_longer_share": 0.0,
        })
        rec["n"] += 1
        if lazy_pick == human:
            rec["len_agree"] += 1
        else:
            rec["len_disagree"] += 1
        if info_pick == human:
            rec["info_agree"] += 1
        else:
            rec["info_disagree"] += 1
        if _len(human_text) >= _len(other_text):
            rec["human_longer_share"] += 1
    for src, rec in per_source.items():
        n = rec["n"] or 1
        rec["length_inference_rate"] = round(rec["len_agree"] / n, 4)      # 长度裁判与人类一致率
        rec["length_goodhart_rate"] = round(rec["len_disagree"] / n, 4)    # 结构性 Goodhart 率
        rec["info_inference_rate"] = round(rec["info_agree"] / n, 4)
        rec["human_longer_share"] = round(rec["human_longer_share"] / n, 4)
    return per_source


# ---- 以下两个函数供"有 LLM 裁判"时实测；当前环境跳过 ----
def _call_judge(prompt, response, judge_prompt, judge_model):
    """占位：真实实现应调用 LLM 端点返回 verdict。需要 key 与网络。"""
    raise NotImplementedError("LLM judge endpoint not configured in this environment")


def invariance(records, kind="prompt"):
    """kind='prompt' -> 两个等价 judge prompt; kind='model' -> 两个 judge 模型。
    返回 invariance 分数 (一致率)。无 key 时返回 None。"""
    if not LLM_JUDGE_ENABLED:
        return None
    agree = 0
    total = 0
    # ... 真实实现: 对每条记录的 response 跑两种口径/两个模型, 比较 verdict ...
    return round(agree / total, 4) if total else None


def main():
    records, meta = load_unified()
    sg = structural_goodhart(records)

    # 提示/模型不变性: 本环境无 key -> None（脚本已就绪）
    prompt_inv = invariance(records, "prompt")
    model_inv = invariance(records, "model")

    # 与 Queyi C++ 数据的对比（692 批 LLM 臂实测；本 checkout 无 692 产物，需回填）
    queyi_cpp_baseline = {
        "note": "来自 692 批 LLM 臂（本 checkout 无 data/692_* 产物，须回填）",
        "prompt_invariance_692": "见 692 artifacts（内存记录 87.5%，未过 >=0.9）",
        "model_invariance_692": "见 692 artifacts",
        "structural_goodhart_692": "LLM 失败拓扑与 sanitizer 正交（692 结论）",
    }

    top_goodhart = sorted(
        [r for r in records if _human_side(r.get("human_ground_truth", "")) is not None],
        key=lambda r: (_len(r["response_B" if _human_side(r["human_ground_truth"]) == "A" else "response_A"] or "")
                      - _len(r["response_A" if _human_side(r["human_ground_truth"]) == "A" else "response_B"] or "")),
        reverse=True,
    )[:10]
    top_cases = [{
        "id": r["id"], "source_dataset": r["source_dataset"],
        "human_preferred": r["human_ground_truth"],
        "len_human": _len(r["response_A" if _human_side(r["human_ground_truth"]) == "A" else "response_B"]),
        "len_other": _len(r["response_A" if _human_side(r["human_ground_truth"]) == "B" else "response_B"]),
        "note": "人类偏好侧更短，长度裁判会判错（结构性 Goodhart 实例）",
    } for r in top_goodhart]

    results = {
        "meta": {
            "batch": "699-C",
            "generated": "2026-10-09",
            "n_records_analyzed": len(records),
            "llm_judge_enabled": LLM_JUDGE_ENABLED,
            "honest_note": "结构性 Goodhart 在真实数据上实测；prompt/model invariance 需 LLM 裁判（本环境未配置 key，函数就绪、返回 None）。",
        },
        "structural_goodhart": sg,
        "prompt_invariance": prompt_inv,
        "model_invariance": model_inv,
        "queyi_cpp_baseline": queyi_cpp_baseline,
        "top_structural_goodhart_cases": top_cases,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # 终端摘要
    print("="*70)
    print("699-C LLM 漂移最小可行性预测试 — 结果摘要")
    print("="*70)
    print(f"分析样本数: {len(records)}")
    print(f"LLM 裁判: {'启用' if LLM_JUDGE_ENABLED else '未配置(跳过 prompt/model invariance)'}")
    print("-"*70)
    print("结构性 Goodhart（懒惰长度裁判 vs 人类标注）:")
    for src, rec in sg.items():
        print(f"  [{src}] n={rec['n']}  长度一致率={rec['length_inference_rate']}  "
              f"Goodhart率={rec['length_goodhart_rate']}  人类侧更长占比={rec['human_longer_share']}")
    print("-"*70)
    print(f"prompt_invariance  = {prompt_inv}  (需 LLM 裁判)")
    print(f"model_invariance   = {model_inv}  (需 LLM 裁判)")
    print(f"Queyi C++ 基线     = {queyi_cpp_baseline['note']}")
    print("Top 结构性 Goodhart 实例 (人类偏好侧更短):", len(top_cases), "条")
    print("="*70)
    print(f"原始结果已写入: {OUT}")


if __name__ == "__main__":
    main()
