# -*- coding: utf-8 -*-
"""676c-G Task E: 入池 → data/holdout_expansion/expG/ + INDEX.json"""
import json, os, shutil, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))   # 仓库根(HERE 上两级)
POOL = os.path.join(ROOT, "data", "holdout_expansion", "expG")
os.makedirs(POOL, exist_ok=True)

manifest = json.load(open(os.path.join(HERE, "_manifest.json"), encoding="utf-8"))
results = json.load(open(os.path.join(HERE, "verify_results.json"), encoding="utf-8"))
quality = json.load(open(os.path.join(HERE, "quality_check.json"), encoding="utf-8"))

samples_idx = []
by_type = collections.Counter()
sev = collections.Counter()
src_dist = collections.Counter()
verdict_dist = collections.Counter()
planted_false_ids = []

for sid in manifest["samples"]:
    meta = json.load(open(os.path.join(HERE, f"sample_{sid}.json"), encoding="utf-8"))
    v = results[sid]
    name = "sample_" + sid
    for ext in (".cpp", ".json"):
        shutil.copy2(os.path.join(HERE, name + ext), os.path.join(POOL, name + ext))
    pooled = {k: vd["verdict"] for k, vd in v["pooled_verdict"].items()}
    samples_idx.append({
        "sample_id": name,
        "defect_type": meta["defect_type"],
        "defect_location": {"line": meta["defect_location"]["line"], "function": meta["defect_location"]["function"]},
        "severity": meta["severity"],
        "planted": meta["planted"],
        "source": {"type": meta["source"]["type"], "id": meta["source"]["id"], "url": meta["source"]["url"],
                   "project": meta["source"]["project"]},
        "expected_verdict": meta["expected_verdict"],
        "expected_detectors": meta["expected_detectors"],
        "pooled_verdict": pooled,
        "notes": meta["notes"],
    })
    by_type[meta["defect_type"]] += 1
    sev[meta["severity"]] += 1
    src_dist[meta["source"]["type"]] += 1
    verdict_dist[meta["expected_verdict"]] += 1
    if meta["planted"] is False:
        planted_false_ids.append(name)

index = {
    "schema": "queyi-expansion-pool/v1",
    "batch": "676c-G(扩样真实世界缺陷)",
    "pool_dir": "data/holdout_expansion/expG",
    "count": len(samples_idx),
    "stats": {
        "total_generated": len(manifest["samples"]),
        "compiled": sum(1 for r in results.values() if r.get("syntax_mingw") == "PASS"),
        "pooled": len(samples_idx),
        "eliminated": 0,
        "by_type": dict(sorted(by_type.items())),
        "severity": dict(sorted(sev.items())),
        "planted_true": len(manifest["samples"]) - len(planted_false_ids),
        "planted_false": len(planted_false_ids),
        "source_distribution": dict(sorted(src_dist.items())),
        "verdict_distribution": dict(sorted(verdict_dist.items())),
    },
    "quality_check": {
        "seed": quality["seed"],
        "sampled": len(quality["sampled"]),
        "mech_fail": len(quality["mech_fail"]),
        "planted_false_source_checked": quality["planted_false_checked"],
        "source_problems": len(quality["source_problems"]),
    },
    "planted_false_samples": planted_false_ids,
    "samples": samples_idx,
}
with open(os.path.join(POOL, "INDEX.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(index, fh, ensure_ascii=False, indent=1)
print(f"pooled={len(samples_idx)} planted_false={len(planted_false_ids)}")
print("by_type:", dict(by_type))
print("source:", dict(src_dist), "| verdict:", dict(verdict_dist))
