#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""hash_datasets_670c.py — 670c B3：数据集完整性基线（复现 kit 的"秤"）。

为什么需要
==========
REPLICATION.md 声称"按这些命令能复算出这些数字"。但**数字对不上**至少有两种原因：

  ① 验证器/工具真的变了（代码问题）；
  ② 数据文件被人改过 / CRLF 转换 / 半截写入 / 根本没拿到（数据问题）。

两者混在一起就无法归因 —— 复现者看到的只是"87.5% 变成了 66.7%"。
本工具把**数据集文件本身**钉成 sha256 清单，先跑 `--check` 就能把"数据漂移"与
"结论漂移"分开。661 的 `data/dataset_hashes_661.json` 只覆盖 7 个文件、无分组、
无冻结语义；670c 这份扩到 holdout/corpus/defects/counterfactual/cards_index 五族，
并把"输入"与"产物"分开（见下）。

分组（group）与冻结语义（frozen）
================================
* `frozen=True` ：**输入**数据集（holdout / corpus / defect / counterfactual / cards_index）。
  它们变了 ⇒ 复算数字**必然**变 ⇒ `--check` 记 **ERROR**（退出码 1）。
* `frozen=False`：**产物**（reveal 报告 / 门禁状态 / 指标）。工具本来就会重写它们
  ⇒ 漂移记 **WARN**，不阻断（但一定打印，绝不静默）。

哈希的是**原始字节**（不做换行归一），因为 `.gitattributes` 的 CRLF 转换正是要抓的漂移形态。

用法与退出码
============
    python tools/hash_datasets_670c.py            # 现算并写 data/dataset_hashes_670c.json，exit 0
    python tools/hash_datasets_670c.py --check    # 与已落盘清单比对：0=一致 / 1=冻结文件漂移 / 2=清单缺失
    python tools/hash_datasets_670c.py --list     # 只列清单（不读盘、不写盘），exit 0
    python tools/hash_datasets_670c.py --json     # 机器可读（可与 --check 合用）

诚实边界
========
* `--check` 只能证明"文件与某次落盘的清单一致"，**不能**证明该清单本身可信 ——
  清单的可信度依赖 git 历史（谁改了它会留痕），与 `tools/.tool_checksums` 同一逻辑。
* 缺文件**不静默**：写清单时记 `missing=true` 并打印；`--check` 时冻结文件缺失记 ERROR。
* 本工具**只读**数据集，不修任何文件（缺失就是缺失，不代为生成）。
"""
from __future__ import annotations

import argparse
import glob as _glob
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

from utf8_console import ensure_utf8

TOOL_VERSION = "hash_datasets_670c/v1"
OUT_REL = "data/dataset_hashes_670c.json"

#: 数据集清单。`path` 可以是 glob（如 fixtures/*.cpp）；`frozen` 语义见模块 docstring。
#: 每条都写明**为什么它在射程内**，而不是"看见 json 就收"。
DATASETS: tuple[dict, ...] = (
    # ── holdout（真错/对照种子 + 665 新样本夹具）──────────────────────────────
    {"group": "holdout", "path": "data/holdout/holdout.json", "frozen": True,
     "note": "canonical 合并视图（旧 20 + 665 追加 10 = 30）；holdout_reveal_3_665 的输入"},
    {"group": "holdout", "path": "data/holdout/holdout_665.json", "frozen": True,
     "note": "665 C1 扩样文件（与 holdout.json 同为 canonical 视图，内容应一致）"},
    {"group": "holdout", "path": "data/holdout/holdout_extension_669d.json", "frozen": True,
     "note": "669d D1 补充 10 条（supplementary，未并入 holdout.json）"},
    {"group": "holdout", "path": "data/cards_665/fixtures/*.cpp", "frozen": True,
     "note": "h21–h30 与 ig-* 的真实夹具源码；holdout 新样本由它们编译而来"},
    # ── external corpus（D3 外部语料）────────────────────────────────────────
    {"group": "corpus", "path": "data/external_corpus/external_corpus_662.json", "frozen": True,
     "note": "canonical 合并视图（662 的 20 + 665 追加 20 = 40）"},
    {"group": "corpus", "path": "data/external_corpus/external_corpus_665.json", "frozen": True,
     "note": "665 D1 扩样视图（与 662 文件同为 canonical，内容应一致）"},
    {"group": "corpus", "path": "data/external_corpus/external_corpus_669d.json", "frozen": True,
     "note": "669d D3 补充 20 条（supplementary）"},
    # ── defects（从 git log 挖出的真实缺陷）──────────────────────────────────
    {"group": "defects", "path": "data/defect_fixtures/defects.json", "frozen": True,
     "note": "15 条真实修过的缺陷 + 各条 gate_caught 判定"},
    {"group": "defects", "path": "data/defect_injection_661.json", "frozen": True,
     "note": "661 重注入结果（门禁复抓率的事实源）"},
    # ── counterfactual（反事实引文算子案例）──────────────────────────────────
    {"group": "counterfactual", "path": "data/counterfactual_cases_660.json", "frozen": True,
     "note": "660 的 10 案例（**无真值标签** ⇒ 不进 P/R/F1 分母，见 665 的 denominator.unscored_sibling）"},
    {"group": "counterfactual", "path": "data/counterfactual_cases_665.json", "frozen": True,
     "note": "665 打分案例（10 条，带 external_anchor 真值标签）"},
    {"group": "counterfactual", "path": "data/counterfactual_cases_669d.json", "frozen": True,
     "note": "669d D2 补充 20 条（supplementary）"},
    # ── cards_index（卡台账 / 前端索引）─────────────────────────────────────
    {"group": "cards_index", "path": "web/data/cards_index.json", "frozen": True,
     "note": "tools/teach_card_656.py 产出的卡索引（count=47，含 10 草稿）"},
    {"group": "cards_index", "path": "web/data/cards.json", "frozen": True,
     "note": "卡的全文（前端渲染源）"},
    {"group": "cards_index", "path": "data/cards_665/index_665.json", "frozen": True,
     "note": "665 B1 机器卡 16 张（独立台账，不混入 cards.json）"},
    {"group": "cards_index", "path": "web/data/ig_cards_665.json", "frozen": True,
     "note": "665 机器卡的前端入口"},
    # ── 规则引擎（口径本身）──────────────────────────────────────────────────
    {"group": "rules", "path": "data/_gate_rules.json", "frozen": True,
     "note": "67 条规则清单（= 引擎唯一事实源；改它就等于改「什么算通过」）"},
    # ── 产物（可被工具重写 ⇒ frozen=False）──────────────────────────────────
    {"group": "holdout_reveal", "path": "data/holdout_reveal_3_665.json", "frozen": False,
     "note": "holdout reveal_3 报告（tools/holdout_reveal_3_665.py 的产物）"},
    {"group": "holdout_reveal", "path": "data/holdout/reveal_3_detail_668.json", "frozen": False,
     "note": "reveal_3 逐样本明细 + 环境（同一次运行写出）"},
    {"group": "holdout_reveal", "path": "data/holdout_reveal_1_661.json", "frozen": False,
     "note": "历史 reveal（不可回盲的历史留痕）"},
    {"group": "holdout_reveal", "path": "data/holdout_reveal_2_662.json", "frozen": False,
     "note": "历史 reveal_2（reveal_3 的对比基线）"},
    {"group": "corpus_reveal", "path": "data/external_corpus_reveal_662.json", "frozen": False,
     "note": "662 的 20 条留痕（不得覆写）"},
    {"group": "corpus_reveal", "path": "data/external_corpus_reveal_665.json", "frozen": False,
     "note": "665 的 40 条结果（论文 external 数字的事实源）"},
    {"group": "counterfactual_calibration", "path": "data/counterfactual_calibration_662.json",
     "frozen": False, "note": "662 阈值扫描（构造负例口径）"},
    {"group": "gate_status", "path": "data/658_gate_status.json", "frozen": False,
     "note": "658 门禁状态（run_658_gate.py 的产物；670c 红线：只读不重跑）"},
    {"group": "gate_status", "path": "data/669d_gate_status.json", "frozen": False,
     "note": "669d 门禁状态（669d 文件冻结：670c 只用 --no-write 复核）"},
    {"group": "gate_status", "path": "data/669d_known_gaps.json", "frozen": False,
     "note": "669d 已登记缺口台账（降级 WARN 的唯一依据）"},
    {"group": "experiments", "path": "data/experiments/669_experiments.json", "frozen": False,
     "note": "669 P3 基线表 + 口径消融（docs/669_实验结果.md 的事实源）"},
    {"group": "experiments", "path": "data/669_caliber_report.json", "frozen": False,
     "note": "669 口径表（率 ↔ 分母 ↔ CI）"},
    {"group": "mutation", "path": "data/656_mutation_report_core.json", "frozen": False,
     "note": "656 变异 core 作用域报告（97.3% = 110/147）"},
    {"group": "mutation", "path": "data/656_mutation_report_all.json", "frozen": False,
     "note": "656 变异 all 作用域报告（81.5% = 128/223）"},
    {"group": "web_metrics", "path": "web/data/metrics_666.json", "frozen": False,
     "note": "前端指标现算（666）"},
    {"group": "web_metrics", "path": "web/data/status.json", "frozen": False,
     "note": "前端状态块（含 ig_cards_665 段）"},
    {"group": "web_metrics", "path": "web/data/verdicts_667.json", "frozen": False,
     "note": "前端判决看板（cards_real=42 / holdout / external 现算值）"},
)


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    """分块算 sha256 —— 哈希的是**原始字节**，不做换行归一（CRLF 漂移必须显形）。"""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            b = fh.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def git_commit(root: Path) -> str:
    """取 HEAD sha。取不到就写 'unknown' —— 不编造，也不因此让清单不可用。"""
    try:
        r = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root),
                           capture_output=True, text=True, timeout=30)
        return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else "unknown"
    except Exception:  # noqa: BLE001  (git 不在 PATH / 非 git 副本都要能跑)
        return "unknown"


def expand(root: Path, entry: dict) -> list[dict]:
    """把一条清单项（可能是 glob）展开成逐文件记录。glob 无匹配 ⇒ 保留一条 missing 记录。"""
    pat = entry["path"]
    if "*" in pat or "?" in pat:
        hits = sorted(Path(p) for p in _glob.glob(str(root / pat)))
        if not hits:
            return [{**entry, "path": pat, "missing": True, "size": None, "sha256": None}]
        return [{**entry, "path": p.relative_to(root).as_posix(),
                 "missing": False, "size": p.stat().st_size,
                 "sha256": sha256_file(p)} for p in hits if p.is_file()]
    p = root / pat
    if not p.is_file():
        return [{**entry, "path": pat, "missing": True, "size": None, "sha256": None}]
    return [{**entry, "path": pat, "missing": False,
             "size": p.stat().st_size, "sha256": sha256_file(p)}]


def build_manifest(root: Path, entries: tuple[dict, ...] = DATASETS) -> dict:
    """现算清单（只读盘，不写盘）—— 测试可传小 entries 直接调用。"""
    files: list[dict] = []
    for e in entries:
        files.extend(expand(root, e))
    return {
        "schema": "queyi-dataset-hashes/v2",
        "batch": "670c",
        "generated_by": "tools/hash_datasets_670c.py",
        "tool_version": TOOL_VERSION,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "algorithm": "sha256",
        "hash_unit": "raw-bytes（不做换行归一；CRLF 转换会显形）",
        "python": sys.version.split()[0],
        "git_commit": git_commit(root),
        "count": len(files),
        "missing": sorted(f["path"] for f in files if f["missing"]),
        "total_bytes": sum(f["size"] or 0 for f in files),
        "groups": sorted({f["group"] for f in files}),
        "files": files,
        "honest_note": (
            "本清单只证明「文件与某次落盘一致」，不证明清单自身可信（依赖 git 历史留痕）。"
            "frozen=True 是**输入**数据集，漂移即 ERROR；frozen=False 是**产物**，漂移记 WARN。"),
    }


def compare(recorded: dict, current: dict) -> dict:
    """比对两份清单。返回 {frozen_drift, product_drift, added, removed, missing_frozen}。

    判定是**按 path** 的（不是按顺序）：清单可增删项，只要能对上号。
    """
    rec = {f["path"]: f for f in recorded.get("files", [])}
    cur = {f["path"]: f for f in current.get("files", [])}
    frozen_drift: list[dict] = []
    product_drift: list[dict] = []
    added: list[dict] = []
    removed: list[dict] = []
    missing_frozen: list[dict] = []
    for path, c in cur.items():
        r = rec.get(path)
        if r is None:
            added.append({"path": path, "frozen": c.get("frozen", False)})
            continue
        if c.get("missing"):
            row = {"path": path, "why": "文件缺失（清单里有、盘上没有）",
                   "frozen": bool(c.get("frozen"))}
            (missing_frozen if c.get("frozen") else product_drift).append(row)
            continue
        if r.get("sha256") != c.get("sha256") or r.get("size") != c.get("size"):
            row = {"path": path, "recorded": r.get("sha256"), "current": c.get("sha256"),
                   "recorded_size": r.get("size"), "current_size": c.get("size"),
                   "frozen": bool(c.get("frozen"))}
            (frozen_drift if c.get("frozen") else product_drift).append(row)
    for path, r in rec.items():
        if path not in cur:
            removed.append({"path": path, "frozen": bool(r.get("frozen"))})
    return {"frozen_drift": frozen_drift, "product_drift": product_drift,
            "added": added, "removed": removed, "missing_frozen": missing_frozen}


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(
        description="670c B3：数据集 sha256 完整性基线（默认现算并落盘清单）")
    ap.add_argument("--check", action="store_true",
                    help="与已落盘清单比对：0=一致 / 1=冻结文件漂移 / 2=清单缺失")
    ap.add_argument("--list", action="store_true", help="只列清单（不读盘、不写盘）")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--root", default=None, help="仓库根（默认取本文件上一级；测试可覆盖）")
    a = ap.parse_args(argv)

    root = Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
    out = root / OUT_REL

    if a.list:
        rows = [{"group": e["group"], "path": e["path"], "frozen": e["frozen"], "note": e["note"]}
                for e in DATASETS]
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
        else:
            print(f"{len(rows)} 条清单项（{sum(1 for r in rows if r['frozen'])} 冻结输入 / "
                  f"{sum(1 for r in rows if not r['frozen'])} 产物）")
            for r in rows:
                print(f"  [{'FROZEN' if r['frozen'] else 'prod  '}] {r['group']:<26} {r['path']}")
        return 0

    current = build_manifest(root)

    if a.check:
        if not out.is_file():
            print(f"[hash670c] 缺清单 {OUT_REL} —— 先跑 python tools/hash_datasets_670c.py 生成")
            return 2
        rec = json.loads(out.read_bytes().decode("utf-8"))
        d = compare(rec, current)
        err = len(d["frozen_drift"]) + len(d["missing_frozen"])
        warn = len(d["product_drift"]) + len(d["added"]) + len(d["removed"])
        if a.json:
            print(json.dumps({"overall": "PASS" if err == 0 else "FAIL",
                              "recorded_generated_at": rec.get("generated_at"),
                              "current_generated_at": current["generated_at"], **d},
                             ensure_ascii=False, indent=2))
        else:
            print(f"[hash670c] 比对 {OUT_REL}（落盘 {rec.get('generated_at')}）")
            print(f"  ERROR {err} 条（冻结输入漂移/缺失）   WARN {warn} 条（产物漂移/增删）")
            for row in d["frozen_drift"] + d["missing_frozen"]:
                print(f"  [ERROR] {row['path']}  {row.get('recorded')} -> {row.get('current')}")
            for row in d["product_drift"]:
                print(f"  [WARN ] {row['path']}  {row.get('recorded')} -> {row.get('current')}")
            for row in d["added"]:
                print(f"  [WARN ] 新增（清单外） {row['path']}")
            for row in d["removed"]:
                print(f"  [WARN ] 消失（盘上无） {row['path']}")
            print("  ⇒ " + ("PASS（冻结输入一致）" if err == 0 else "FAIL（冻结输入已漂移）"))
        return 0 if err == 0 else 1

    try:
        out.write_bytes(json.dumps(current, ensure_ascii=False, indent=2).encode("utf-8"))
    except OSError as e:
        print(f"[hash670c] 写 {OUT_REL} 失败：{e}")
        return 2
    if a.json:
        print(json.dumps(current, ensure_ascii=False, indent=2))
    else:
        print(f"[hash670c] {current['count']} 个文件 / {current['total_bytes']} 字节 ⇒ {OUT_REL}")
        print(f"  python={current['python']}  git={current['git_commit'][:12]}  "
              f"groups={','.join(current['groups'])}")
        if current["missing"]:
            print(f"  ⚠ 缺失 {len(current['missing'])} 项（已登记进 manifest.missing，不静默）：")
            for m in current["missing"]:
                print(f"    - {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
