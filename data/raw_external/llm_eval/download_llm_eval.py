#!/usr/bin/env python3
"""
699-B · LLM 评估数据集下载与统一格式脚本（可复现）

在**有网络出口**的 Linux/mac/Win 环境运行即可取全量（而非抽样）真实样本，
并写出 data/699_llm_eval_unified_format.json。

用法:
    pip install datasets   # 推荐（取全量）
    python download_llm_eval.py

或用 HuggingFace datasets-server REST（无需 datasets 库，仅标准库）:
    python download_llm_eval.py --rest
"""
import argparse
import json
import os
import sys
import time

try:
    import urllib.request
    _HAVE_URLLIB = True
except Exception:
    _HAVE_URLLIB = False

OUT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..",
    "data", "699_llm_eval_unified_format.json"))


def fetch_via_datasets(n_jb=2000, n_rb=20000):
    from datasets import load_dataset
    jb = load_dataset("ScalerLab/JudgeBench", split="claude")
    rb = load_dataset("allenai/reward-bench", split="filtered")
    unified = []
    for r in jb.select(range(min(n_jb, len(jb)))):
        unified.append({
            "id": "JB-" + str(r.get("pair_id", "")), "source_dataset": "JudgeBench",
            "prompt": r.get("question", ""), "response": None,
            "response_A": r.get("response_A", ""), "response_B": r.get("response_B", ""),
            "response_model": r.get("response_model", ""),
            "source_subset": r.get("source", ""),
            "human_ground_truth": r.get("label", ""), "judge_verdicts": {},
        })
    for r in rb.select(range(min(n_rb, len(rb)))):
        unified.append({
            "id": "RB-" + str(r.get("id", "")), "source_dataset": "RewardBench",
            "prompt": r.get("prompt", ""), "response": None,
            "response_A": r.get("chosen", ""), "response_B": r.get("rejected", ""),
            "response_model": "%s vs %s" % (r.get("chosen_model", ""), r.get("rejected_model", "")),
            "source_subset": r.get("subset", ""),
            "human_ground_truth": "A", "judge_verdicts": {},
        })
    return unified


def _rows(dataset, config, split, offset, length):
    u = ("https://datasets-server.huggingface.co/rows?dataset=%s&config=%s&split=%s"
         "&offset=%d&length=%d" % (dataset, config, split, offset, length))
    req = urllib.request.Request(u, headers={"User-Agent": "research"})
    return json.loads(urllib.request.urlopen(req, timeout=40).read())


def fetch_via_rest(n_each=200):
    unified = []
    for dataset, config, split, tag in [
        ("ScalerLab/JudgeBench", "default", "claude", "JB"),
        ("allenai/reward-bench", "default", "filtered", "RB"),
    ]:
        done = 0
        while done < n_each:
            n = min(100, n_each - done)
            d = _rows(dataset, config, split, done, n)
            for r in d.get("rows", []):
                row = r["row"]
                if tag == "JB":
                    unified.append({
                        "id": "JB-" + str(row.get("pair_id", done)), "source_dataset": "JudgeBench",
                        "prompt": row.get("question", ""), "response": None,
                        "response_A": row.get("response_A", ""), "response_B": row.get("response_B", ""),
                        "response_model": row.get("response_model", ""),
                        "source_subset": row.get("source", ""),
                        "human_ground_truth": row.get("label", ""), "judge_verdicts": {},
                    })
                else:
                    unified.append({
                        "id": "RB-" + str(row.get("id", done)), "source_dataset": "RewardBench",
                        "prompt": row.get("prompt", ""), "response": None,
                        "response_A": row.get("chosen", ""), "response_B": row.get("rejected", ""),
                        "response_model": "%s vs %s" % (row.get("chosen_model", ""), row.get("rejected_model", "")),
                        "source_subset": row.get("subset", ""),
                        "human_ground_truth": "A", "judge_verdicts": {},
                    })
            done += len(d.get("rows", []))
            if len(d.get("rows", [])) < n:
                break
            time.sleep(0.4)
    return unified


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rest", action="store_true", help="用 datasets-server REST 而非 datasets 库")
    ap.add_argument("--each", type=int, default=200, help="每数据集抽样条数 (REST 模式)")
    args = ap.parse_args()
    if args.rest:
        if not _HAVE_URLLIB:
            print("urllib 不可用"); sys.exit(1)
        unified = fetch_via_rest(args.each)
    else:
        unified = fetch_via_datasets()
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"meta": {"regenerated": True, "n_records": len(unified),
                            "sources": {"JudgeBench": sum(1 for x in unified if x["source_dataset"] == "JudgeBench"),
                                        "RewardBench": sum(1 for x in unified if x["source_dataset"] == "RewardBench")}},
                   "records": unified}, f, ensure_ascii=False, indent=1)
    print("wrote", len(unified), "records ->", OUT)


if __name__ == "__main__":
    main()
