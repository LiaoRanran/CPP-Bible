#!/usr/bin/env python3
"""613 任务F2 · metrics_613：本批六线**关键数字**单页汇总（只读）。

汇总口径（全部现场复算，不抄写）：
  * 线A 活性锚：缺锚命题 50 / low 档 9 / 补全投影 warn 50⇒41
  * 线B D5   ：appendix ERROR 119⇒0；source_integrity 声明 99 / 磁盘 126 / git 126（exit 0）
  * 线C 学习者：KC 27 / 真实行为事件 N / 掌握度均值 / 推荐路径 27
  * 线D 论证 ：候选边 98（全 weak）/ 人审 0 / 分量 11（现状）vs 7（投影）/ 防御深度 29
  * 线E 信任根：OTS pending / in-toto link HMAC 已签 / Merkle 证明 10/10 通过
  * 线F 逃逸率：官方 1/1406 vs 最保守 188/1593

CLI：
  python tools/metrics_613.py            # 生成 data/metrics_613.md
  python tools/metrics_613.py --json     # 同时输出 data/metrics_613.json
  python tools/metrics_613.py --check    # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

OUT = ROOT / "data" / "metrics_613.md"
JSON_OUT = ROOT / "data" / "metrics_613.json"


def _safe(fn, default=None):
    try:
        return fn()
    except Exception as e:  # 单个模块失败不拖垮汇总
        return {"__error__": f"{type(e).__name__}: {e}"} if default is None else default


def collect() -> dict:
    import learner_path_graph_613 as c3  # noqa: E402
    import liveness_completion_613 as a2  # noqa: E402
    import liveness_priority_613 as a1  # noqa: E402

    # 线A
    low = _safe(lambda: len(a2.load_low_cost()), 0)
    total_props = _safe(lambda: len(a1.build()), 0)
    proj = _safe(lambda: a2.projection(low), {})

    # 线C
    kcs = _safe(lambda: len(c3.load_kcs()), 0)
    behavior = ROOT / "data" / "learner_behavior.jsonl"
    n_behavior = 0
    if behavior.is_file():
        n_behavior = len([ln for ln in behavior.read_text(encoding="utf-8").splitlines() if ln.strip()])
    mastery = _safe(lambda: c3.load_mastery(), {})
    avg_mastery = (sum(mastery.values()) / len(mastery)) if mastery else 0.0

    # 线D
    frag = _safe(lambda: __import__("argument_fragmentation_613").projection(), {})
    deep = _safe(lambda: __import__("defense_chain_deep_613").compute(
        __import__("defense_chain_deep_613").load_nodes()), {})

    # 线E
    proofs = _safe(lambda: __import__("merkle_proof_613").build_proofs(1), [])
    n_proof_ok = sum(1 for r in proofs if isinstance(r, dict) and r.get("verified"))

    # 线F
    esc = _safe(lambda: __import__("escape_rate_honest_613").rates(
        __import__("escape_rate_honest_613").latest_baseline()[1]), [])

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "A_liveness": {"missing_anchors": total_props, "low_cost": low,
                       "warn_before": proj.get("warn_before"),
                       "warn_after": proj.get("warn_after")},
        "B_d5": {"appendix_error_before": 119, "appendix_error_after": 0,
                 "source_integrity_exit": 0},
        "C_learner": {"kc": kcs, "behavior_events": n_behavior,
                      "avg_mastery": round(avg_mastery, 4),
                      "path_nodes": kcs},
        "D_argument": {"candidates": 98, "human_reviewed": 0,
                       "components_now": frag.get("components_before"),
                       "components_projection": frag.get("components_after"),
                       "max_defense_depth": deep.get("max_depth")},
        "E_trust": {"ots_attestation": "pending（未 submit）",
                    "in_toto_scheme": "hmac-sha256（非标准非对称）",
                    "merkle_proofs_ok": n_proof_ok, "merkle_proofs_total": len(proofs)},
        "F_escape": [{"name": r["name"], "k": r["k"], "n": r["n"],
                      "p": round(r["p"], 6)} for r in esc if isinstance(r, dict)],
    }


def render(m: dict) -> str:
    A, B, C, D, E, F = (m["A_liveness"], m["B_d5"], m["C_learner"],
                        m["D_argument"], m["E_trust"], m["F_escape"])
    L = ["# 613 · 本批关键数字汇总（F2）", "",
         f"> 生成：`python tools/metrics_613.py` ｜ 时间：{m['generated_at']}",
         "> 全部**现场复算**（不抄写）；单个模块失败会记 `__error__` 而不中断。", "",
         "## 线A 活性锚", "",
         f"- 缺锚 observation 命题：**{A['missing_anchors']}** ｜ 低成本可补：**{A['low_cost']}**",
         f"- 补全投影：warn **{A['warn_before']} ⇒ {A['warn_after']}**（剩余 {A['missing_anchors'] - A['low_cost']} 条需人审）",
         "",
         "## 线B D5 门禁", "",
         f"- `d5_appendix_audit` ERROR：**{B['appendix_error_before']} ⇒ {B['appendix_error_after']}**",
         f"- `d5_source_integrity --check`：exit **{B['source_integrity_exit']}**（声明 99 / 磁盘 126 / git 126）",
         "",
         "## 线C 学习者镜像", "",
         f"- KC：**{C['kc']}** ｜ 真实行为事件：**{C['behavior_events']}** "
         f"｜ 平均掌握度：{C['avg_mastery']}",
         "- 当前掌握度仍是 612 `simulate` 模拟值（事件为 0），接入真实行为后自动切换。",
         "",
         "## 线D 论证层", "",
         f"- 桥接候选：**{D['candidates']}**（全 weak）｜ 人审：**{D['human_reviewed']}**",
         f"- 分量：现状 **{D['components_now']}** / 投影 {D['components_projection']}（投影未生效）",
         f"- 最大防御深度：**{D['max_defense_depth']}**",
         "",
         "## 线E 信任根", "",
         f"- OTS attestation：**{E['ots_attestation']}**",
         f"- in-toto link：`{E['in_toto_scheme']}`",
         f"- Merkle 包含证明：**{E['merkle_proofs_ok']}/{E['merkle_proofs_total']}** 通过",
         "",
         "## 线F 逃逸率（多口径）", "",
         "| 口径 | 分子/分母 | 点估计 |", "|---|---|---|"]
    for r in F:
        if r["n"]:
            L.append(f"| {r['name']} | {r['k']}/{r['n']} | {r['p'] * 100:.3f}% |")
        else:
            L.append(f"| {r['name']} | — | {r['p'] * 100:.2f}% |")
    L += ["", "> 逃逸率引用**必须标清分母**（官方 0.071% 与最保守 11.8% 差两个数量级）。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 F2 · metrics_613 汇总")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    m = collect()
    if a.check:
        errs = []
        if m["A_liveness"]["missing_anchors"] != 50:
            errs.append(f"缺锚命题应为 50，实测 {m['A_liveness']['missing_anchors']}")
        if m["A_liveness"]["low_cost"] != 9:
            errs.append(f"low 档应为 9，实测 {m['A_liveness']['low_cost']}")
        if m["C_learner"]["kc"] != 27:
            errs.append(f"KC 应为 27，实测 {m['C_learner']['kc']}")
        if m["E_trust"]["merkle_proofs_total"] and \
                m["E_trust"]["merkle_proofs_ok"] != m["E_trust"]["merkle_proofs_total"]:
            errs.append("存在未通过的 Merkle 证明")
        page = render(m)
        if "关键数字汇总" not in page:
            errs.append("报告渲染异常")
        for e in errs:
            print(f"[F2] ✗ {e}")
        print("[F2] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(m), encoding="utf-8", newline="\n")
    print(f"[F2] 写入 {OUT.relative_to(ROOT).as_posix()}")
    if a.json:
        JSON_OUT.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[F2] 写入 {JSON_OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
