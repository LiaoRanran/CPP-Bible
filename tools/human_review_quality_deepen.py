"""611 E2 · 人审质量报告深化（**只读** · 不裁决、不自动改判）。

在 609 A2 `human_review_quality` 的基础上**深化**质量信号（那些 A2 没覆盖、但 611 关心的维度）：
  * **单人评审风险**：全部 388 条是否来自同一 reviewer（无交叉校验 ⇒ 单点盲区）；
  * **逐 MIS 一致性**：一个 MIS 的多条边是否被给了**混合** verdict（approve 与 modify 并存
    ⇒ 该 MIS 的档位判断内部矛盾，须复核）；
  * **modify 集中区**：modify 比例 = 1.0 的 MIS（歧义集中，需第二轮人审沉淀判据）；
  * **主题覆盖**：各主题被评审的边数分布（失衡 ⇒ 结论外推风险）；
  * **理由健康度**：理由长度的最小/平均、过短理由数（A2 已用 20 字符阈值，这里给分布）。

⚠️ 只检测、只标记：**复核标记是人要处理的**，本工具绝不自动改判、绝不执行人审。

CLI：`--stats`（JSON）/ `--write`（写 `data/human_review_quality_deepen_611.md`）/ `--check`。
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "human_review_quality_deepen_611.md"
MIN_REASON = 20

# 611 E2 锁定已知事实（存量人审冻结前不变）
KNOWN = {"reviewers": 1, "modify_full_ratio_mis": 7}


def analyze(annotations_path=None) -> dict:
    import human_review_cli as hrc
    import human_review_report as hrr
    anns = (hrc.load_annotations(annotations_path) if annotations_path
            else hrc.load_annotations())
    if not anns:
        return {"insufficient_evidence": True, "records": 0}
    idx = hrr.edge_index()
    # 逐边：MIS、verdict、reviewer、reason_len
    mis_verdicts: dict[str, set[str]] = defaultdict(set)
    reviewers: set[str] = set()
    reason_lens: list[int] = []
    verdicts = Counter()
    topic_edge: dict[str, int] = defaultdict(int)
    for a in anns:
        e = idx.get(str(a.get("edge_id")))
        if e is None:
            continue
        kind = hrc.kind_of(a)
        verdicts[kind] += 1
        reviewers.add(str(a.get("reviewer", "")))
        rl = int(a.get("reason_len", len(str(a.get("reason", "") or ""))))
        reason_lens.append(rl)
        mid = hrr.mis_of(e)
        mis_verdicts[mid].add(kind)
        # 主题：从 MIS id 第二前缀
        t = mid.split("-")[1] if "-" in mid else "?"
        topic_edge[t] += 1
    # 逐 MIS 一致性
    inconsistent = sorted(m for m, vs in mis_verdicts.items()
                          if {"approve", "modify"} <= vs)
    modify_full = sorted(m for m, vs in mis_verdicts.items()
                         if vs == {"modify"})
    rl_n = len(reason_lens)
    short = sum(1 for x in reason_lens if x < MIN_REASON)
    return {
        "records": len(anns),
        "insufficient_evidence": False,
        "verdicts": dict(verdicts),
        "reviewer_diversity": {"distinct_reviewers": len(reviewers),
                               "reviewers": sorted(reviewers),
                               "single_reviewer_risk": len(reviewers) == 1},
        "mis_consistency": {"inconsistent_mis": inconsistent,
                            "inconsistent_count": len(inconsistent),
                            "modify_only_mis": modify_full,
                            "modify_only_count": len(modify_full),
                            "mis_groups": len(mis_verdicts)},
        "topic_coverage": {k: {"edges": v, "ratio": round(v / rl_n, 4)}
                           for k, v in sorted(topic_edge.items(), key=lambda kv: -kv[1])},
        "reason_health": {"min": min(reason_lens) if reason_lens else None,
                          "avg": round(sum(reason_lens) / rl_n, 2) if rl_n else None,
                          "max": max(reason_lens) if reason_lens else None,
                          "short_count": short,
                          "short_ratio": round(short / rl_n, 4) if rl_n else None},
        "note": "只读深化：单人评审风险 / 逐 MIS 一致性 / modify 集中区 / 主题覆盖 / 理由健康度",
    }


def render_report(a: dict) -> str:
    if a.get("insufficient_evidence"):
        return ("# 611 E2 · 人审质量报告深化\n\n"
                "> ⚠️ 零人审记录 ⇒ insufficient evidence：不填 0、不宣称质量良好。\n")
    rv = a["reviewer_diversity"]
    mc = a["mis_consistency"]
    rh = a["reason_health"]
    lines = [
        "# 611 E2 · 人审质量报告深化（只读）", "",
        "> 在 609 A2 基础上深化：单人评审风险 / 逐 MIS 一致性 / modify 集中区 / 主题覆盖 / 理由健康度。"
        "只检测、只标记，绝不自动改判或执行人审。", "",
        "## 一、总览", "",
        f"- 人审记录 **{a['records']}** 条 · verdict 分布 {a['verdicts']}",
        f"- **评审者**：{rv['distinct_reviewers']} 人（{', '.join(rv['reviewers']) or '—'}）"
        f" ⇒ {'⚠️ 单人评审风险（无交叉校验）' if rv['single_reviewer_risk'] else '多人交叉'}",
        f"- 理由健康度：最短 {rh['min']} / 平均 {rh['avg']} / 最长 {rh['max']} 字符；"
        f"过短（<{MIN_REASON}）{rh['short_count']} 条（占比 {rh['short_ratio']}）", "",
        "## 二、逐 MIS 一致性", "",
        f"- 内部**混合** verdict（approve 与 modify 并存）的 MIS：**{mc['inconsistent_count']}** 个"
        f"（{', '.join(mc['inconsistent_mis']) or '—'}）⇒ 该 MIS 档位判断自相矛盾，须复核；",
        f"- **仅 modify** 的 MIS：**{mc['modify_only_count']}** 个（modify 比例 = 1.0 的歧义集中区）；",
        f"- MIS 分组共 {mc['mis_groups']} 个。", "",
        "## 三、主题覆盖", "",
        "| 主题 | 评审边数 | 占比 |",
        "|---|---|---|",
    ]
    for t, v in a["topic_coverage"].items():
        lines.append(f"| {t} | {v['edges']} | {v['ratio']:.1%} |")
    lines += ["", "## 四、深化结论（NDW）", "",
              "- **Need**：单人评审风险 ⇒ 至少引入第二位评审交叉抽检，否则盲区无人兜底；",
              "- **Do**：混合 verdict 的 MIS + 仅 modify 的 MIS 进入第二轮人审，沉淀判据；",
              "- **Won't（本批不做）**：绝不自动改判、绝不重跑人审、不改 annotations（人审权在用户）。", ""]
    return "\n".join(lines)


def check(a: dict) -> list[str]:
    problems: list[str] = []
    if a.get("insufficient_evidence"):
        return problems
    rv = a["reviewer_diversity"]
    if rv["distinct_reviewers"] != KNOWN["reviewers"]:
        problems.append(f"评审者数应为 {KNOWN['reviewers']}（实测 {rv['distinct_reviewers']}）")
    if a["mis_consistency"]["modify_only_count"] != KNOWN["modify_full_ratio_mis"]:
        problems.append(f"仅 modify 的 MIS 应为 {KNOWN['modify_full_ratio_mis']}"
                        f"（实测 {a['mis_consistency']['modify_only_count']}）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="human_review_quality_deepen",
                                 description="611 E2 人审质量报告深化（只读）")
    ap.add_argument("--version", action="version", version=f"human_review_quality_deepen {VERSION}")
    ap.add_argument("--annotations", default=None)
    ap.add_argument("--stats", action="store_true", help="打印 JSON")
    ap.add_argument("--write", action="store_true", help=f"写 {REPORT_OUT.name}")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    res = analyze(a.annotations)
    if a.stats:
        print(json.dumps(res, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(res)
        if problems:
            for p in problems:
                print(f"[E2] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[E2] ✓ 人审质量深化锁定（评审者 {res['reviewer_diversity']['distinct_reviewers']} · "
              f"仅 modify MIS {res['mis_consistency']['modify_only_count']}）")
        return 0
    if a.write:
        REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
        REPORT_OUT.write_text(render_report(res), encoding="utf-8", newline="\n")
        print(f"[E2] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}"
              f"（记录 {res.get('records', 0)} 条）")
        return 0
    print(f"记录 {res.get('records', 0)} · 评审者 {res['reviewer_diversity']['distinct_reviewers']} · "
          f"混合 MIS {res['mis_consistency']['inconsistent_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
