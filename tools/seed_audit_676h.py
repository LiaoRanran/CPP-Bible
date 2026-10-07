# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""676h 任务 B2 · 随机种子审计（全仓口径，比 671i 的种子门禁更宽）。

与 tools/seed_check_671i.py 的区别
----------------------------------
671i 是**门禁**（只扫 tools/，只看有没有写 seed，ERROR/WARN 二分）；
本工具是**审计证据**：
  1. 扫描范围扩到 tools/ + data/（实验脚本两个位置都放）；
  2. 不只判断"有没有 seed"，还把**种子常量的字面值**抄出来登记；
  3. 区分"实验用随机"（参与结论 ⇒ 必须有固定种子）与
     "非实验用随机"（演示/日志抖动 ⇒ 只需登记）；
  4. 产出带时间戳的 json/md，供论文附录 Reproducibility 引用。

用法
----
    python tools/seed_audit_676h.py [--out-json data/676h_seed_audit.json] [--out-md data/676h_seed_audit.md]

退出码：0 = 无 ERROR；1 = 存在实验类脚本未固定种子。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCAN_DIRS = ("tools", "data")

# 实验类：随机性参与**结论**（抽样 / 对照 / 切分 / 扰动 / 重 inject）
EXPERIMENT_HINTS = (
    "experiment", "baseline", "attack", "mutation", "blind", "select_assets",
    "targeted", "fuzz", "mutator", "ablation", "replay", "reveal", "verifier_pool",
    "selection_strategies", "holdout", "external_corpus", "run_a5", "detect_for_assets",
    "external_anchor", "llm_arm", "stats_", "confidence_sequence", "eprocess",
    "676f", "676g",
)
# 非实验：随机性只用于演示 / 命名 / 日志
NONEXPERIMENT_HINTS = (
    "dashboard", "logger", "metrics_collector", "learner_", "a11y", "mermaid",
)

USE_RE = re.compile(
    r"(?:^|\W)(?:import\s+random|from\s+random|np\.random|numpy\.random|random\.)",
    re.MULTILINE,
)
SEED_CALL_RE = re.compile(
    r"(?:random|np\.random|numpy\.random)\.seed\(|np\.random\.default_rng|RandomState\(|random\.Random\(")
SEED_CONST_RE = re.compile(r"(?<![A-Za-z0-9_.])(?:SEED|SEED_[A-Z_]+|DEFAULT_SEED|_SEED)\s*[:=]\s*(\d+)")
ANY_SEED_LITERAL_RE = re.compile(r"\bseed\s*[:=]\s*(\d{4,})", re.IGNORECASE)
# CLI 默认值 / random.Random(...) / .seed(...) 里写死的种子也算登记
SEED_LITERAL_EXTRA_RES = [
    re.compile(r"\bdefault\s*=\s*(\d{4,})"),
    re.compile(r"\.seed\(\s*(\d{4,})\s*\)"),
    re.compile(r"Random\(\s*(\d{4,})\s*\)"),
]
DOWNSTREAM_RE = re.compile(r"(?:^|\W)([A-Za-z_]*[Ss][Ee][Ee][Dd][A-Za-z_]*)\b", re.MULTILINE)


def classify_file(rel_path: str) -> str:
    base = os.path.basename(rel_path).lower()
    if any(h in base for h in EXPERIMENT_HINTS):
        return "experiment"
    if any(h in base for h in NONEXPERIMENT_HINTS):
        return "non-experiment"
    return "unknown"


def scan_file(path: str, rel: str):
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return None
    seed_set = set(SEED_CONST_RE.findall(text)) | set(ANY_SEED_LITERAL_RE.findall(text))
    for rx in SEED_LITERAL_EXTRA_RES:
        seed_set |= set(rx.findall(text))
    seeds = sorted(seed_set)
    if not USE_RE.search(text) and not seeds:
        return None
    symbols = sorted({m.group(1) for m in DOWNSTREAM_RE.finditer(text)})
    return {
        "file": rel,
        "kind": classify_file(rel),
        "uses_random": bool(USE_RE.search(text)),
        "seed_call": bool(SEED_CALL_RE.search(text)),
        "seed_constants": seeds,
        "seed_symbols": symbols[:12],
        "lines": len(text.splitlines()),
    }


def run_scan():
    rows = []
    for d in SCAN_DIRS:
        root = os.path.join(ROOT, d)
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            if any(p in dirpath for p in (".git", "__pycache__", "node_modules")):
                dirnames[:] = []
                continue
            for fn in filenames:
                if not fn.endswith(".py"):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
                r = scan_file(full, rel)
                if r:
                    rows.append(r)
    rows.sort(key=lambda r: r["file"])
    return rows


# 产物里登记的种子 vs 代码里的种子常量：漂移必须在论文层面诚实登记
ARTIFACT_SEED_SOURCES = [
    ("data/656_mutation_report.json", "seed", "变异（core）"),
    ("data/656_mutation_report_all.json", "seed", "变异（all）"),
    ("data/current_numbers.json", "seed", "672h 扩样"),
    ("data/experiments/a5_673p.json", "seed", "A5 实验"),
    ("data/experiments/a5_673p.json", "real_attribution.seed", "A5 Real Attribution"),
    ("data/external_anchor_reveal_672j.json", "runs", "外部锚点（重复次数，非种子）"),
]


def collect_artifact_seeds():
    out = []
    for rel, dotted, label in ARTIFACT_SEED_SOURCES:
        try:
            obj = json.load(open(os.path.join(ROOT, rel.replace("/", os.sep)), encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        cur = obj
        ok = True
        for part in dotted.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok:
            out.append({"artifact": rel, "field": dotted, "value": str(cur), "label": label})
    return out


def build_report(rows):
    def seeded(r):
        return bool(r["seed_call"] or r["seed_constants"])

    exp = [r for r in rows if r["kind"] == "experiment"]
    exp_unseeded = [r for r in exp if not seeded(r)]
    exp_seeded = [r for r in exp if seeded(r)]
    other = [r for r in rows if r["kind"] != "experiment"]
    seed_values = {}
    for r in rows:
        for s in r["seed_constants"]:
            seed_values.setdefault(s, []).append(r["file"])

    # 漂移检测：产物登记的种子必须能在某个脚本的种子常量里找到；找不到就如实登记
    code_seeds = set(seed_values)
    artifacts = collect_artifact_seeds()
    drift = []
    for a in artifacts:
        if not re.fullmatch(r"\d{6,}", str(a["value"])):
            continue  # 像 runs=3 这种不是种子
        if a["value"] not in code_seeds:
            drift.append(a)
    return {
        "schema": "queyi-676h/seed-audit",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "scope": list(SCAN_DIRS),
        "summary": {
            "files_using_random": len(rows),
            "experiment_seeded": len(exp_seeded),
            "experiment_unseeded": len(exp_unseeded),
            "non_experiment_or_unknown": len(other),
        },
        "seed_registry": {k: sorted(set(v)) for k, v in sorted(seed_values.items())},
        "artifact_seeds": artifacts,
        "seed_drift": drift,
        "experiment_unseeded": [r["file"] for r in exp_unseeded],
        "files": rows,
    }


def write_md(path, rep):
    L = ["# 676h · 随机种子审计（tools/ + data/）", ""]
    L.append(f"- 生成时间：{rep['generated_at']}")
    L.append(f"- 扫描范围：{', '.join(rep['scope'])}")
    s = rep["summary"]
    L.append(f"- 使用随机性的脚本：**{s['files_using_random']}**；"
             f"实验类已固定种子 {s['experiment_seeded']}；"
             f"**实验类未固定种子 {s['experiment_unseeded']}**；"
             f"非实验/未知 {s['non_experiment_or_unknown']}")
    L.append("")
    L.append("## 1. 种子注册表（各脚本实际引用的种子常量）")
    L.append("")
    L.append("| 种子 | 用到它的脚本 |")
    L.append("|---|---|")
    for seed, files in rep["seed_registry"].items():
        shown = ", ".join(f"`{f}`" for f in files[:8])
        more = "" if len(files) <= 8 else f" …(+{len(files)-8})"
        L.append(f"| `{seed}` | {shown}{more} |")
    L.append("")
    L.append("### 1b. 漂移检测：产物登记的种子 vs 代码里的种子常量")
    L.append("")
    L.append("| 产物 | 字段 | 登记值 | 说明 |")
    L.append("|---|---|---|---|")
    for a in rep["artifact_seeds"]:
        flag = "**漂移**：代码里已找不到该种子常量" if a in rep["seed_drift"] else "一致"
        L.append(f"| `{a['artifact']}` | `{a['field']}` | `{a['value']}` | {a['label']} → {flag} |")
    L.append("")
    L.append("## 2. 实验类脚本中未固定种子的")
    L.append("")
    if rep["experiment_unseeded"]:
        for f in rep["experiment_unseeded"]:
            L.append(f"- `{f}`")
    else:
        L.append("（空）—— 所有被判为实验类的脚本都固定了种子或引用了固定种子常量。")
    L.append("")
    L.append("## 3. 逐文件明细")
    L.append("")
    L.append("| 文件 | 类别 | seed 调用 | 种子常量 |")
    L.append("|---|---|---|---|")
    for r in rep["files"]:
        seeds = ", ".join(f"`{x}`" for x in r["seed_constants"]) or "—"
        call = "yes" if r["seed_call"] else "no"
        L.append(f"| `{r['file']}` | {r['kind']} | {call} | {seeds} |")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="676h 随机种子审计")
    ap.add_argument("--out-json", default="data/676h_seed_audit.json")
    ap.add_argument("--out-md", default="data/676h_seed_audit.md")
    args = ap.parse_args(argv)

    rows = run_scan()
    rep = build_report(rows)
    with open(os.path.join(ROOT, args.out_json.replace("/", os.sep)), "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    write_md(os.path.join(ROOT, args.out_md.replace("/", os.sep)), rep)

    s = rep["summary"]
    print(f"使用随机性的脚本 {s['files_using_random']}；"
          f"实验类未固定种子 {s['experiment_unseeded']}")
    return 1 if rep["experiment_unseeded"] else 0


if __name__ == "__main__":
    sys.exit(main())
