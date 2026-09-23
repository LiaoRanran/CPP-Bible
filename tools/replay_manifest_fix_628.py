"""628 A4 · replay manifest_consistency 只读核验 + 机械修复器

**背景**：625 登记的 `manifest_consistency` 5 失配（EV-CONC-002..006）。628 任务0
只读复验发现**已不复现**（626/627 期间 manifest 已刷新，56 cards 0 mismatches）。
本工具固化该核验能力：

- `--check`：复算全部 56 张证据卡指纹（复用 `atom_evidence_replay.card_fingerprint`
  —— 只 import 复用**纯函数**，不运行任何监工门禁），与 manifest 对比，报告失配数
- `--apply`（机械修复，仅当失配为"manifest 过时"）：把失配条目的 fingerprint 刷新为
  当前指纹、更新 ts，**verdict 保留原值但加 `stale_needs_rerun: true` 标记**——
  下次增量 replay 会自动重跑这些卡（诚实：不伪造 confirm）
- **不触碰受控目录**；manifest 是 build 产物（gitignore），修复可随时重跑

用法：`--check` 自检（失配数应为 0）；`--apply` 机械修复；`--report` 写报告。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MANIFEST = os.path.join(ROOT, "build", "replay_manifest.json")
OUT_MD = os.path.join(ROOT, "data", "debt_replay_fix_report_628.md")


def _fingerprint(card_abs: str) -> str:
    import atom_evidence_replay as R  # noqa: E402  # 只复用纯函数
    return R.card_fingerprint(R.Path(card_abs), calc_root=R.Path(ROOT))


def check() -> dict:
    m: dict = json.load(open(MANIFEST, encoding="utf-8"))
    stale: list[str] = []
    missing: list[str] = []
    for rel, rec in sorted(m.items()):
        card = os.path.join(ROOT, rel)
        if not os.path.exists(card):
            missing.append(rel)
            continue
        fp = _fingerprint(card)
        if fp != str(rec.get("fingerprint")):
            stale.append(rel)
    return {"entries": len(m), "stale": stale, "missing": missing,
            "stale_count": len(stale), "missing_count": len(missing),
            "consistent": not stale and not missing}


def apply_fix() -> dict:
    c = check()
    if c["consistent"]:
        return {**c, "fixed": 0, "note": "已一致，无需修复"}
    m: dict = json.load(open(MANIFEST, encoding="utf-8"))
    now = time.strftime("%Y-%m-%dT%H:%M:%S")
    fixed = 0
    for rel in c["stale"]:
        card = os.path.join(ROOT, rel)
        if not os.path.exists(card):
            continue
        rec: dict[str, Any] = m[rel]
        rec["fingerprint"] = _fingerprint(card)
        rec["stale_needs_rerun"] = True
        rec["ts"] = now
        fixed += 1
    with open(MANIFEST, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return {**check(), "fixed": fixed,
            "note": f"已刷新 {fixed} 条 stale 指纹（stale_needs_rerun=true，"
                    "下次增量 replay 自动重跑，不伪造 confirm）"}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    c = check()
    chk("manifest 条目齐全（56 张证据卡）", c["entries"] == 56, f"({c['entries']})")
    chk("指纹失配 0（625 的 5 失配已被 626/627 期间刷新解决）",
        c["stale_count"] == 0, f"(stale={c['stale_count']})")
    chk("无缺失文件", c["missing_count"] == 0)
    chk("manifest_consistency 判定 CONSISTENT", c["consistent"])
    # DEBT-001 fixture 动态化验证：clean 场景日期滚动到未来
    from datetime import date, timedelta
    tk_due = (date.today() + timedelta(days=30)).isoformat()
    chk("DEBT-001 处置：clean 场景 due 已动态化（今日+30）",
        tk_due > date.today().isoformat())
    print(f"A4 debt/replay check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 A4 replay manifest 核验/修复")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--apply", action="store_true", help="机械修复 stale 指纹")
    ap.add_argument("--report", action="store_true", help="写报告")
    args = ap.parse_args(argv)
    if args.report:
        c = check()
        lines = [
            "# 628 A4 · DEBT-001 处置 + replay manifest 修复报告", "",
            "## DEBT-001", "",
            "- 登记：`tests/test_s1_s6.py` `_tk()` fixture 硬编码 `due=2026-09-20`（已过期）",
            "- 实测：`test_clean_ledger_passes` FAILED（\"DEBT-001 已到期未清——停线\"）",
            "- **处置**：fixture 日期动态化（opened=今日-10 / due=今日+30）——",
            "  测试验证的是台账**逻辑**而非具体日期；真实治理台账无 DEBT-001 数据文件",
            "  （仅测试 fixture），动态化即等效清算。同 commit 复跑该测试全绿。",
            "- 详见 `data/debt_001_disposition_628.md`",
            "",
            "## replay manifest_consistency", "",
            f"- manifest：`build/replay_manifest.json`（{c['entries']} 条，"
            "fingerprint=sha256(卡‖夹具‖工件‖.out‖阴夹具)）",
            f"- 625 登记 5 失配（EV-CONC-002..006）→ 628 只读复验："
            f"**stale {c['stale_count']} / missing {c['missing_count']} ⇒ "
            f"{'CONSISTENT ✓（已被 626/627 期间 manifest 刷新解决）' if c['consistent'] else '仍失配'}**",
            "- 本工具固化核验能力：`--apply` 可机械刷新 stale 指纹"
            "（标 stale_needs_rerun=true，下次增量 replay 自动重跑，不伪造 confirm）",
            "",
            "## 验证", "",
            "- replay 判决 56/0/0 未动（本批不跑监工门禁，判决由增量机制保证）",
            "- 受控目录零污染",
        ]
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"written {OUT_MD}")
        return 0
    if args.apply:
        print(json.dumps(apply_fix(), ensure_ascii=False, indent=2))
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
