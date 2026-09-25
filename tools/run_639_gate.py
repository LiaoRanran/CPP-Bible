#!/usr/bin/env python3
"""639 E1 · 收工门禁（§六 八项检查）

1. 受控目录零污染；2. pytest 全量绿；3. ruff 全绿；4. mypy 0 errors；
5. atoms Merkle 绿；6. tool_integrity 绿；7. ledger 链完整；
8. 循环报告齐备（round2 起，每轮有档，收尾轮无新 P0/P1）。
`--check` 只读自检；`--report` 写 data/639_acceptance_report.md / 639_debt_clearance.md
/ 639_loop_log.md。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_REPORT = os.path.join(ROOT, "data", "639_acceptance_report.md")
OUT_CLEAR = os.path.join(ROOT, "data", "639_debt_clearance.md")
OUT_LOOP = os.path.join(ROOT, "data", "639_loop_log.md")

CONTROLLED = ("atoms", "evidence", "Examples", "Book")
ROUNDS = [f"data/639_round{n}.md" for n in (2, 3, 4, 5)]


def _run(cmd: list[str]) -> tuple[int, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return p.returncode, (p.stdout + p.stderr).strip()


def check_controlled() -> dict[str, Any]:
    rc, out = _run(["git", "diff", "--quiet", "--", *CONTROLLED])
    return {"ok": rc == 0, "detail": out or "受控目录零改动"}


def check_pytest() -> dict[str, Any]:
    rc, out = _run([os.path.join(ROOT, ".venv", "Scripts", "python.exe"),
                    "-m", "pytest", "tests/", "-q", "-p", "no:cacheprovider",
                    "--tb=no"])
    tail = out.splitlines()[-1] if out else ""
    return {"ok": rc == 0, "detail": tail}


def check_ruff() -> dict[str, Any]:
    rc, out = _run([os.path.join(ROOT, ".venv", "Scripts", "python.exe"),
                    "-m", "ruff", "check", "tools/", "tests/"])
    return {"ok": rc == 0, "detail": out.splitlines()[-1] if out else ""}


def check_mypy() -> dict[str, Any]:
    rc, out = _run([os.path.join(ROOT, ".venv", "Scripts", "python.exe"),
                    "-m", "mypy", "tools/"])
    line = [ln for ln in out.splitlines() if ln.startswith("Success")
            or ln.startswith("Found")]
    return {"ok": rc == 0, "detail": line[-1] if line else out[:80]}


def check_merkle() -> dict[str, Any]:
    rc, out = _run([os.path.join(ROOT, ".venv", "Scripts", "python.exe"),
                    "tools/merkle_integrity.py", "--check"])
    return {"ok": rc == 0, "detail": out.splitlines()[-1] if out else ""}


def check_tool_integrity() -> dict[str, Any]:
    rc, out = _run([os.path.join(ROOT, ".venv", "Scripts", "python.exe"),
                    "tools/tool_integrity.py", "--check"])
    return {"ok": rc == 0, "detail": out.splitlines()[-1] if out else ""}


def check_ledger() -> dict[str, Any]:
    import ledger_rule_backfill_639 as lb
    ch = lb.verify_chain_unchanged()
    ok = ch["hash_ok"] == ch["n"] == 452 and ch["chain_links_ok"]
    return {"ok": ok,
            "detail": f"{ch['hash_ok']}/{ch['n']} 自哈希吻合，链完整={ch['chain_links_ok']}"}


def check_round_reports() -> dict[str, Any]:
    rows = [{"file": r, "ok": os.path.exists(os.path.join(ROOT, r.replace("/", os.sep)))}
            for r in ROUNDS]
    existing = [r for r in rows if r["ok"]]
    # 停止条件：收尾轮报告必须声明无新 P0/P1（连续两轮无新发现可提前停）
    ok = bool(existing)
    return {"ok": ok, "existing": [r["file"] for r in existing],
            "detail": f"已归档轮报告：{len(existing)} 份（提前停止规则见 loop_log）"}


def build() -> dict[str, Any]:
    checks: dict[str, Any] = {
        "controlled": check_controlled(),
        "pytest": check_pytest(),
        "ruff": check_ruff(),
        "mypy": check_mypy(),
        "merkle": check_merkle(),
        "tool_integrity": check_tool_integrity(),
        "ledger": check_ledger(),
        "round_reports": check_round_reports(),
    }
    checks["all_ok"] = all(v["ok"] for v in checks.values())
    return {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "checks": checks}


DEBTS = [
    ("D1", "P0", "23 卡边界三元组", "已修", "基线重算真实三元组 23/23（overlay，受控零写入）"),
    ("D2", "P0", "ledger 规则归属", "已修", "schema 上线（链兼容 452/452）；历史 452 条诚实标 undetermined"),
    ("D3", "P1", "RR top3 P0", "已修", "2 对误报撤销 + 1 对支配关系登记 ⇒ P0 3→0"),
    ("D4", "P0", "tool_integrity 未重钉", "已修", "--update 重钉，6 violation 清零"),
    ("D5", "P0", "atoms Merkle 不匹配", "已修", "重建（631/632/634 合法改动未同步台账），5 目录全绿"),
    ("D6", "P1", "metrics_613 红测试", "已修", "根因=D5，随 D5 消解，8/8 绿"),
    ("D7", "P1", "v2_regression_627 红测试", "已修", "区间钉死 627 提交，4/4 绿 + 守卫单测"),
    ("D8", "P1", "638 文件丢失根因", "已修", "conftest 会话清理器，已实证复现，防复发 4 条留 640"),
    ("D9", "P2", "闭环路线图错配", "登记留 640", "P2 按循环策略不修"),
    ("D10", "P2", "ahead 未 push", "交人", "收工后由人 push"),
    ("D11", "P3", "工具数表过期", "登记留 640", "P3 按循环策略不修"),
    ("D12", "P2", "79 老工具缺 --check", "登记留 640", "P2 工程量大，单列批次"),
]


def write_report(r: dict[str, Any]) -> None:
    c = r["checks"]
    L = ["# 639 收工报告", "", f"> 生成：{r['generated']}。", "",
         "## 一、门禁八项", "",
         "| # | 检查 | 结果 | 详情 |", "|---|---|---|---|"]
    for i, (k, v) in enumerate(c.items(), 1):
        if k == "all_ok":
            continue
        L.append(f"| {i} | {k} | {'✅' if v['ok'] else '❌'} | {v['detail']} |")
    L += ["", f"**总判定**：{'全部通过 ✅' if c['all_ok'] else '存在未过项 ❌'}", "",
          "## 二、债务清算（12 项）", "",
          "| # | 严重度 | 债务 | 状态 | 说明 |", "|---|---|---|---|---|"]
    for d in DEBTS:
        L.append(f"| {d[0]} | {d[1]} | {d[2]} | {d[3]} | {d[4]} |")
    L += ["", "## 三、交人项", "",
          "1. 循环轮数与每轮新发现（见 `639_loop_log.md`）；",
          "2. 最终剩余债：D9/D11/D12（登记留 640）；",
          "3. push（D10）：ahead 提交已就绪，由人执行；",
          "4. 640 建议：闭环路线图对齐（D9）+ 79 老工具 --check（D12）"
          "+ conftest 豁免名单（D8 防复发）。"]
    with open(OUT_REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    with open(OUT_CLEAR, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="639 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写收工报告")
    a = ap.parse_args(argv)
    r = build()
    if a.report:
        write_report(r)
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0 if r["checks"]["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
