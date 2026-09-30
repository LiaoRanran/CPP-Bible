# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""668 · 「改了验证代码必须重跑落盘」的回归锁（R4/R6）。

667 抓到两次同类翻车（声称 81.2% / F1=1.0，产物里却是 66.7% / 0.0，因为改了判定代码没重跑）。
本文件把"不许再犯"变成**可执行的断言**：

  ① `web_metrics_666 --check` 必须覆盖三个率 —— **改一个数必须变红**（射程自检，R4）；
  ② 产物必须自带 `caliber` / `denominator`，且**能按分母重算出来**（R1）；
  ③ 逐样本明细与汇总值必须**互相一致**（同一生成器同一次运行）；
  ④ 新卡不许**人签**（`machine-verified` + `verified_by` 只能是 `machine:*`/`redteam:*`），
     且**不许预写边界三元组**（669 修订：原断言误把"机器 principal 留名"也当成了代签）。
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import counts_659 as counts  # noqa: E402
import web_metrics_666 as W  # noqa: E402


def _j(rel: str) -> dict:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


# ── ① 射程自检：改了数就必须红 ────────────────────────────────────────────
def _tamper(monkeypatch, tmp_path, key_path: list[str], value) -> int:
    out = tmp_path / "metrics_666.json"
    monkeypatch.setattr(W, "OUT", str(out))
    assert W.main(["--write"]) == 0
    d = json.loads(out.read_text(encoding="utf-8"))
    node = d["metrics"]
    for k in key_path[:-1]:
        node = node[k]
    node[key_path[-1]] = value
    out.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return W.main(["--check"])


def test_check_detects_holdout_tampering(monkeypatch, tmp_path):
    assert _tamper(monkeypatch, tmp_path, ["holdout", "rate_pct"], 99.9) == 1, \
        "改了 holdout 检出率仍报绿 ⇒ --check 没进射程（666 的假绿就是这个形态）"


def test_check_detects_external_tampering(monkeypatch, tmp_path):
    assert _tamper(monkeypatch, tmp_path, ["external", "catch"], 999) == 1


def test_check_detects_counterfactual_tampering(monkeypatch, tmp_path):
    assert _tamper(monkeypatch, tmp_path, ["counterfactual", "f1"], 0.123) == 1


def test_check_green_on_untampered(monkeypatch, tmp_path):
    out = tmp_path / "metrics_666.json"
    monkeypatch.setattr(W, "OUT", str(out))
    assert W.main(["--write"]) == 0
    assert W.main(["--check"]) == 0


# ── ② 口径 / 分母必须来自产物，且算术自洽 ────────────────────────────────
def test_caliber_and_denominator_come_from_artifact():
    m = W.collect()["metrics"]
    h = m["holdout"]
    assert h["caliber"] and "未声明" not in h["caliber"]
    assert h["den"] == h["catch"] + h["miss"]
    assert h["opt_levels"] == ["-O0", "-O2"], "档位必须与生成器一致（不许在工具里另写一份）"
    e = m["external"]
    assert e["den"] == e["catch"] + e["miss"]
    assert e["rate_pct_all"] == round(e["catch"] / e["total"] * 100, 1)
    c = m["counterfactual"]
    assert c["cases"] and c["denominator"] and "未声明" not in c["denominator"]


def test_holdout_detail_matches_summary():
    """逐样本明细与汇总必须一致（同一次运行的两个落盘）。"""
    rep = _j("data/holdout_reveal_3_665.json")
    det = _j("data/holdout/reveal_3_detail_668.json")
    assert det["summary_for"] == "data/holdout_reveal_3_665.json"
    assert len(det["per_sample"]) == len(rep["results"])
    for a, b in zip(det["per_sample"], rep["results"]):
        assert a["id"] == b["id"] and a["verdict"] == b["verdict"], f"{a['id']} 明细与汇总不一致"
    for st in ("catch", "miss", "unknown"):
        got = sum(1 for r in det["per_sample"]
                  if r["planted"] is True and r["verdict"] == st)
        assert got == rep["error_subset"][st], f"{st} 计数不一致"
    assert det["opt_levels"] == rep["opt_levels"]
    assert det["env"].get("wsl_gpp")


def test_counterfactual_denominator_and_third_criterion():
    d = _j("data/counterfactual_cases_665.json")
    assert d["denominator"]["value"] == d["cases_total"] == len(d["cases"])
    hits = [c["id"] for c in d["cases"] if c["mechanism_class"] == "machine_marker"]
    assert hits == d["third_criterion"]["hits"]
    assert d["third_criterion"]["hit_count"] == len(hits)
    # 上界声明必须在产物里（否则会被当泛化能力读）
    assert "上界" in d["honest_note"]


def test_external_denominator_declared():
    d = _j("data/external_corpus_reveal_665.json")
    assert d["denominator"]["value"] == d["catch"] + d["miss"]
    assert d["rate_pct_all_samples"] == round(d["catch"] / d["total"] * 100, 1)
    assert d["denominator"]["all_samples"] == d["total"]


# ── ③ 补卡：不代签 + 不预写边界 ──────────────────────────────────────────
NEW_CARDS = ["atoms/ub/ATOM-UB-WRAP-001.md", "atoms/ub/ATOM-UB-OOB-001.md",
             "atoms/ub/ATOM-UB-NULLDEREF-001.md", "atoms/ub/ATOM-UB-DIVZERO-001.md",
             "atoms/mem/ATOM-MEM-NEWARR-001.md"]


def test_new_cards_are_unsigned_and_keep_correct_status():
    """669 修订：**不代签**的不变量是"没有人签"，不是"连机器 principal 都不许留名"。

    668 原文写 `assert not re.search(r"^verified_by:")` —— 把两件事混为一谈：
      · 人签（`verified_by: human:*`）= 放权体系里**唯人可置**的授权（绝不许代签，本批锁死）；
      · **机器 principal 留名**（`verified_by: machine:*`）= 声明"是哪个机器判的"，
        `gate_engine` 的 `S1-AUTHOR-SELF-VERIFY` 对 `status=machine-verified` **要求**该字段
        （`LEVEL_PRINCIPALS["machine-verified"] == ("machine:",)`）。
    668 的写法让 5 张卡在 gate 里各挂 1 条 block（实测：`S1-AUTHOR-SELF-VERIFY` ×5），
    而按"不许留名"改是**反向**的（把可审计的判定主体抹掉）。669 按事实源（gate 规则）修正断言：
    人签仍然**零容忍**，机器 principal 必须**前缀合法**（machine:/redteam:）。
    """
    for rel in NEW_CARDS:
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        assert "status: machine-verified" in text, f"{rel} 状态必须是 machine-verified"
        assert "human_review: required" in text, f"{rel} 必须标 human_review required"
        assert not re.search(r"^verified_by:\s*human:", text, re.MULTILINE), \
            f"{rel} 不得代签（human:* 署名必须由人复核后写入）"
        m = re.search(r"^verified_by:\s*(\S+)", text, re.MULTILINE)
        assert m is None or m.group(1).startswith(("machine:", "redteam:")), \
            f"{rel} verified_by 只能是 machine:/redteam: 前缀（当前：{m.group(1) if m else ''}）"
        # 未跑变异 ⇒ 不得预写三元组（判决未定不预写边界）
        assert not re.search(r"^mutation_set_hash:", text, re.MULTILINE), \
            f"{rel} 不许预写边界三元组"


def test_new_cards_carry_real_machine_evidence():
    idx = {c["source_id"]: c for c in _j("data/cards_665/index_665.json")["cards"]}
    for rel in NEW_CARDS:
        text = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        hit = [c for c in idx.values() if c["fixture_rel"] in text]
        assert hit, f"{rel} 未引用任何真实夹具"
        c = hit[0]
        assert c["fixture_sha256"][:16] in text, f"{rel} 未记录夹具 sha256"
        assert c["detector"] in text and str(c["verdict"]) in text


def test_ledger_and_controlled_dirs_untouched_by_this_batch():
    """本批只允许 **新增** 卡文件；受控目录不得出现删除/改名。"""
    assert counts.ATOMS_REAL >= 42
    assert counts.ATOMS_DRAFT == 10
    for rel in NEW_CARDS:
        assert os.path.isfile(os.path.join(ROOT, rel))
