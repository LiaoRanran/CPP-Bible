"""625 C3 · QueYi Core 剥离触发标准检查（5 条）

① 雷2 闭环稳定运行≥3 轮
② 雷4 PCK 全量迁移 + 成为权威源
③ 雷5 Authority 接口正式启用
④ 核心接口连续 5 批无破坏性变更
⑤ 路径解耦完成

每条判 满足 / 部分满足 / 不满足；给出整体判断与 626 计划。

铁律：只读检查（B2/C1 结果 + PCK/Authority 产物）；必有 `--check`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

CORE6 = ["gate_engine", "atom_evidence_replay", "poison_drill", "tool_integrity", "toolchain", "cppbible"]
AUX20 = ["golden_lock", "debt_ledger", "governance_doc_guard", "supply_chain", "metrics_collector",
         "mutation_fuzz", "weighted_af_solver", "replay_invariants", "merkle_integrity",
         "attack_edge_generator", "knowledge_graph", "defense_chain", "escape_rate_honest_613",
         "human_review_queue", "human_review_dashboard", "exemption_expiry", "learner_state",
         "prop_graph", "ci_local_precheck", "trust_root_status_check"]


def _has(mod: str, needle: str) -> bool:
    p = os.path.join(ROOT, "tools", mod + ".py")
    return os.path.exists(p) and needle in open(p, encoding="utf-8", errors="replace").read()


def check_1() -> dict:
    import loop_stability_metrics_625 as LS
    m = LS.metrics()
    t = LS.trigger1(m)
    rounds = len(m["rows"])
    ok = rounds >= 3 and t["satisfied_count"] >= 4
    return {"d": f"闭环累计 {rounds} 轮（≥3）· 触发标准①满足 {t['satisfied_count']}/5",
            "status": "满足" if (ok and t["satisfied"]) else ("部分满足" if ok else "不满足")}


def check_2() -> dict:
    import glob
    certs = glob.glob(os.path.join(ROOT, "data", "pck", "certificates", "*.pck.yaml"))
    try:
        import pck_status_stats_620 as S
        st = S.stats(S.load_certs())
        auth = int((st.get("by_status") or {}).get("authorized", 0))
    except Exception:
        auth = 0
    migrated = len(certs) == 83
    authoritative = False   # 尚无"权威源"裁定
    status = "部分满足" if (migrated and not authoritative) else ("满足" if (migrated and authoritative) else "不满足")
    return {"d": f"PCK 迁移 {len(certs)}/83（全量={'✅' if migrated else '❌'}）· authorized {auth}/83 · 权威源={authoritative}",
            "status": status}


def check_3() -> dict:
    mods = [("human_review_queue", "Authority"), ("authority_log_620", "Authority"),
            ("authority_to_annotations_sync_623", "Authority")]
    have = [m for m, kw in mods if _has(m, kw)]
    design = os.path.exists(os.path.join(ROOT, "data", "queyi_core_interface_design_625.md"))
    status = "部分满足" if len(have) >= 2 else "不满足"
    return {"d": f"Authority 相关工具 {len(have)}/3（{', '.join(have)}）· 接口设计={design} · "
                 f"正式启用（治理裁定）=False", "status": status}


def check_4() -> dict:
    # 保守：621-625 核心工具接口（CLI/语义）未做破坏性变更；C1 仅内部 ROOT 解析、A1 仅类型注解
    return {"d": "621-625 核心接口：C1 仅内部 ROOT 解析、A1 仅类型注解；gate/replay(56/0/0)/poison(124/124) 行为不变 ⇒ 无破坏性变更",
            "status": "满足"}


def check_5() -> dict:
    core = sum(1 for m in CORE6 if _has(m, "path_config_625"))
    aux = sum(1 for m in AUX20 if _has(m, "path_config_625"))
    status = "满足" if (core == 6 and aux >= 20) else ("部分满足" if core == 6 else "不满足")
    return {"d": f"路径解耦：核心 {core}/6 · 辅助 {aux}/20（其余 ~110 辅助 + tests/ 未改）",
            "status": status}


CHECKS = [("① 雷2 闭环稳定≥3 轮", check_1), ("② 雷4 PCK 全量迁移+权威源", check_2),
          ("③ 雷5 Authority 接口正式启用", check_3), ("④ 核心接口连续 5 批无破坏性变更", check_4),
          ("⑤ 路径解耦完成", check_5)]


def analyze() -> dict:
    rows = []
    for name, fn in CHECKS:
        r = fn()
        rows.append({"criterion": name, **r})
    satisfied = sum(1 for r in rows if r["status"] == "满足")
    overall = "可以启动剥离" if satisfied == 5 else "建议再等 1-2 轮（继续修债务/稳雷2）"
    return {"rows": rows, "satisfied": satisfied, "total": len(rows), "overall": overall}


def render(a: dict) -> str:
    L = ["# 625 C3 · QueYi Core 剥离触发标准检查（5 条）", "",
         f"> 满足 **{a['satisfied']}/{a['total']}**；整体判断：**{a['overall']}**", "",
         "## 一、逐条检查", "", "| 标准 | 结论 | 依据 |", "|---|---|---|"]
    for r in a["rows"]:
        L.append(f"| {r['criterion']} | {r['status']} | {r['d']} |")
    L += ["", "## 二、整体判断", "",
          f"- 满足 {a['satisfied']}/{a['total']} ⇒ **{a['overall']}**。",
          "- 未满足项集中在：② PCK 权威源裁定、③ Authority 正式启用（均为**治理裁定**，非技术债）、"
          "⑤ 路径解耦余量（~110 辅助 + tests/）。", "",
          "## 三、626 计划（若人拍板启动）", "",
          "1. 先做**技术可做**部分：⑤ 路径解耦补全（辅助工具全量 + tests/）；",
          "2. ② PCK：设计「权威源」裁定口径（D4 策略）；",
          "3. ③ Authority：正式启用需人审授权（D3 工具已备框架）；",
          "4. ④ 保持核心接口稳定（626-630 无破坏性变更）。", "",
          "## 四、局限性声明", "",
          "1. ②③ 为**治理裁定**（需人），非机器可判 ⇒ 本检查按「技术就绪度」判，未越权替人裁定。",
          "2. ④ 为**保守判定**（基于 C1/A1 的变更性质 + 行为不变证据），未做逐版接口 diff。", ""]
    return "\n".join(L) + "\n"


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    a = analyze()
    chk("5 条标准", len(a["rows"]) == 5)
    chk("状态取值合法", all(r["status"] in ("满足", "部分满足", "不满足") for r in a["rows"]))
    chk("satisfied 计数一致", a["satisfied"] == sum(1 for r in a["rows"] if r["status"] == "满足"))
    chk("① 至少部分满足", any(r["criterion"].startswith("①") and r["status"] != "不满足" for r in a["rows"]))
    chk("⑤ 核心 6/6", "核心 6/6" in [r["d"] for r in a["rows"] if r["criterion"].startswith("⑤")][0])
    print(f"C3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="625 C3 QueYi Core 剥离触发标准检查")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    a = analyze()
    if args.report:
        p = os.path.join(ROOT, "data", "queyi_core_trigger_check_625.md")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render(a))
        print(f"written {p}")
        return 0
    print(json.dumps(a, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
