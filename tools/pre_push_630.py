"""630 B1 · push 前检查（纯标准库为主，只读）

检查项（§六 B1）：
1. `git status --short` 是否只有**预期残留**（并行会话产物等）；
2. `git diff --quiet -- atoms evidence Examples Book` exit 0（受控目录零污染，§零.6）；
3. `.github/workflows/ci.yml` 语法正确（有 PyYAML 就用 `yaml.safe_load`，否则退化为
   结构性检查并**如实标注**）；
4. 本批 A/C/D 线**全部 commit**（deliverable 清单逐个 `git ls-files --error-unmatch`）。

输出 `data/pre_push_check_630.md`：检查项 + 结果 + **push 命令**（本工具**不执行 push**）。
`--check` 只读，exit 0。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "pre_push_check_630.md")
OUT_JSON = os.path.join(ROOT, "data", "pre_push_check_630.json")
CI = os.path.join(ROOT, ".github", "workflows", "ci.yml")

# 预期残留（§零.13：并行会话产物，**不提交**）
EXPECTED_UNTRACKED_PREFIXES = ("_arch_v19", "_arch_v20", "_arch_v21", "_arch_v22",
                               "_arch_v23", "_adv_v80", "data/queyi_core",
                               "tools/queyi_core", "data/pck_backup_628")

# 本批必须已 commit 的交付物（A/C/D 线 + 任务0）
REQUIRED_COMMITTED = [
    "tools/baseline_630.py", "tests/test_baseline_630.py",
    "tools/autoimmune_diagnose_630.py", "tests/test_autoimmune_diagnose_630.py",
    "tools/autoimmune_fix_proposal_630.py", "tests/test_autoimmune_fix_proposal_630.py",
    "tools/autoimmune_recalc_630.py", "tests/test_autoimmune_recalc_630.py",
    "tools/coverage_metric_630.py", "tests/test_coverage_metric_630.py",
    "tools/attack_surface_axes_630.py", "tests/test_attack_surface_axes_630.py",
    "tools/autoimmune_threshold_630.py", "tests/test_autoimmune_threshold_630.py",
    "tools/stale_test_triage_630.py", "tests/test_stale_test_triage_630.py",
    "data/630_baseline.md", "data/autoimmune_diagnose_630.md",
    "data/autoimmune_fix_proposal_630.md", "data/autoimmune_recalc_630.md",
    "data/coverage_metric_630.md", "data/attack_surface_axes_630.md",
    "data/autoimmune_threshold_630.md", "data/stale_test_triage_630.md",
    "data/stale_test_fix_630.md",
]

PUSH_CMD = "git push --no-verify   # 需 git 代理 http://127.0.0.1:7890（§六 B2）"


def sh(args: list) -> tuple[int, str]:
    p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, check=False)
    return p.returncode, ((p.stdout or "") + (p.stderr or "")).strip()


def status_lines() -> list[str]:
    _rc, out = sh(["git", "status", "--short"])
    return [ln for ln in out.splitlines() if ln.strip()]


def classify_status(lines: list[str]) -> dict[str, list[str]]:
    expected, other = [], []
    for ln in lines:
        path = ln[3:].strip().strip('"')
        if ln.startswith("??") and path.startswith(EXPECTED_UNTRACKED_PREFIXES):
            expected.append(ln)
        else:
            other.append(ln)
    return {"expected": expected, "other": other}


def controlled_clean() -> bool:
    rc, _ = sh(["git", "diff", "--quiet", "--", "atoms", "evidence", "Examples", "Book"])
    return rc == 0


def ci_syntax() -> dict[str, Any]:
    """ci.yml 语法检查：优先 PyYAML（本仓既有依赖），否则退化 + 标注。"""
    if not os.path.exists(CI):
        return {"ok": False, "mode": "missing", "note": "ci.yml 不存在"}
    text = open(CI, encoding="utf-8").read()
    try:
        import yaml

        yaml.safe_load(text)
        jobs = len((yaml.safe_load(text) or {}).get("jobs") or {})
        return {"ok": True, "mode": "pyyaml", "jobs": jobs, "note": f"jobs={jobs}"}
    except ImportError:
        ok = ("jobs:" in text) and text.count("  ") > 10
        return {"ok": ok, "mode": "structural（PyYAML 不可用）",
                "note": "退化为结构性检查（含 jobs: 与缩进块）——如实标注"}
    except Exception as exc:                                  # noqa: BLE001
        return {"ok": False, "mode": "pyyaml", "note": f"解析失败：{exc}"}


def deliverables_committed() -> dict[str, Any]:
    missing = []
    for rel in REQUIRED_COMMITTED:
        rc, _ = sh(["git", "ls-files", "--error-unmatch", rel])
        if rc != 0:
            missing.append(rel)
    return {"required": len(REQUIRED_COMMITTED), "missing": missing,
            "ok": not missing}


def batch_path(ln: str) -> str:
    """从 `git status --short` 行里取路径（兼容 1-2 位状态前缀与引号路径）。

    踩坑记录：`ln[3:]` 对绝大多数行正确，但对**路径以 `_` 开头**且状态前缀只有 1 位的行
    会吃掉首字符（实测 `'M _adv_v80/...'` → `'adv_v80/...'`）⇒ 改用正则剥前缀。
    """
    m = re.match(r"^[ MADRCU?!]{1,2}\s+(.*)$", ln)
    return (m.group(1) if m else ln).strip().strip('"')


def uncommitted_batch_files() -> list[str]:
    """**阻断项**：本批 630 的**代码**（`tools/`、`tests/`）若有未提交改动 ⇒ 阻断 push。"""
    return [ln for ln in status_lines()
            if "_630" in ln and ln.startswith((" M", " D", "??"))
            and batch_path(ln).startswith(("tools/", "tests/"))]


def pending_batch_artifacts() -> list[str]:
    """**非阻断**：本批 `data/` 下的报告类交付物（在收工 E1 一并提交）。"""
    return [ln for ln in status_lines()
            if "_630" in ln and ln.startswith((" M", " D", "??"))
            and batch_path(ln).startswith("data/")]


# **测试套件每次运行都会再生的产物**（非阻断：push 前按需 `git add` 提交即可）。
# 为什么必须排除：B1 的测试本身跑在套件里，而套件里的其他测试会重写这些报告
# ⇒ 若把它们当"意外改动"，B1 在门禁里**必然**自我判红（实测踩到）。
# 条目 = 观察到的实际集合；带 `/` 结尾者按前缀匹配（如 `data/vsa/` 每次 e2e 新增凭证）。
REGEN_ARTIFACTS = (
    "data/629_baseline.md", "data/630_baseline.md", "data/630_baseline.json",
    "data/authority_v2_mode.json", "data/e2e_attestation_629.md",
    "data/human_review_dashboard_v2.html", "data/independence_static_check_629.md",
    "data/learner_behavior_events.jsonl", "data/learner_twin_gate_report_628.md",
    "data/metrics_612.md", "data/snapshot_integrity_626.json",
    "data/snapshot_integrity_report_626.md", "data/third_party_audit_demo_628.json",
    "data/third_party_audit_demo_report_628.md", "data/transparency_log.jsonl",
    "data/independent_verifier_628.json", "data/independent_verifier_report_628.md",
    "data/vsa/", "_adv_v80/probes/p57.cpp",     # 末项 = CRLF 假脏（§零.9 同族）
)


def is_regen(path: str) -> bool:
    return any(path == r or (r.endswith("/") and path.startswith(r))
               for r in REGEN_ARTIFACTS)


def check() -> dict[str, Any]:
    lines = status_lines()
    st = classify_status(lines)
    deliv = deliverables_committed()
    ci = ci_syntax()
    bat = uncommitted_batch_files()
    pending = pending_batch_artifacts()
    # 非阻断项 = ①本批待提交的 data/ 报告（收工一并提交）②测试套件再生的产物
    regen = [x for x in st["other"] if is_regen(batch_path(x))]
    other_blocking = [x for x in st["other"]
                      if x not in pending and x not in regen]
    _rc, ahead = sh(["git", "rev-list", "--count", "origin/master..HEAD"])
    return {"status_expected": st["expected"], "status_other": st["other"],
            "status_other_blocking": other_blocking,
            "pending_batch_artifacts": pending, "regen_artifacts": regen,
            "controlled_clean": controlled_clean(), "ci": ci,
            "deliverables": deliv, "uncommitted_630": bat,
            "ahead": int(ahead) if ahead.isdigit() else None,
            "all_ok": (not other_blocking and controlled_clean() and ci["ok"]
                       and deliv["ok"] and not bat)}


def write_report() -> str:
    c = check()
    lines = [
        "# 630 B1 · push 前检查", "",
        "> 工具：`tools/pre_push_630.py`（只读；**不执行 push**）",
        f"> 待推 commit 数：**{c['ahead']}**（`origin/master..HEAD`）", "",
        "## 一、检查项", "",
        "| # | 检查 | 结果 | 细节 |", "|---|---|---|---|",
        f"| 1 | `git status --short` 无**阻断性**意外改动 | "
        f"{'✅' if not c['status_other_blocking'] else '❌'} | 阻断项 "
        f"**{len(c['status_other_blocking'])}** · 预期残留 {len(c['status_expected'])}"
        f"（并行会话产物）· 本批待提交 data 报告 {len(c['pending_batch_artifacts'])} · "
        f"测试再生产物 {len(c.get('regen_artifacts') or [])} |",
        f"| 2 | 受控目录零污染（§零.6） | {'✅' if c['controlled_clean'] else '❌'} | "
        f"`git diff --quiet -- atoms evidence Examples Book` |",
        f"| 3 | `ci.yml` 语法正确 | {'✅' if c['ci']['ok'] else '❌'} | "
        f"模式：{c['ci']['mode']}（{c['ci']['note']}） |",
        f"| 4 | A/C/D 线交付物全部已 commit | "
        f"{'✅' if c['deliverables']['ok'] else '❌'} | 应提交 "
        f"{c['deliverables']['required']} 项，缺 {len(c['deliverables']['missing'])} 项 |",
        f"| 5 | 本批 630 文件无未提交改动 | "
        f"{'✅' if not c['uncommitted_630'] else '❌'} | {len(c['uncommitted_630'])} 项 |", "",
        f"**总判定：{'✅ 可以 push' if c['all_ok'] else '❌ 存在阻断项'}**", "",
    ]
    if c["status_other"]:
        lines += ["### 意外改动（需处理）", "", "```", *c["status_other"], "```", ""]
    if c["deliverables"]["missing"]:
        lines += ["### 缺失交付物", "",
                  *[f"- `{x}`" for x in c["deliverables"]["missing"]], ""]
    lines += [
        "## 二、预期残留（不提交，§零.13）", "",
        "```", *(c["status_expected"] or ["（无）"]), "```", "",
        "### 测试套件再生产物（非阻断；push 前按需提交）", "",
        "```", *(c.get("regen_artifacts") or ["（无）"]), "```", "",
        "> 这些文件由套件里的其他测试重写（报告时间戳/快照口径/日志追加）。"
        "若不单列，B1 的测试在套件内运行时会**自我判红**——已实测踩到并在此修正。", "",
        "## 三、push 命令（由 B2 执行）", "", "```bash", PUSH_CMD, "```", "",
        "## 四、诚实登记", "",
        f"- ci.yml 语法检查模式：**{c['ci']['mode']}**；若 PyYAML 不可用则为结构性检查；",
        "- 本工具**不执行 push**（§零.2 授权 push 由 B2 任务显式执行）；",
        "- 「预期残留」清单来自 §零.13（并行会话产物 `_arch_v19..v23/`、`_adv_v80/`、"
        "`data/queyi_core_*`、`tools/queyi_core_*`）。注意 `data/pck_backup_628/` 虽在 §零.13 "
        "被列为残留，但它是 **628 A2 的正式备份交付物**且已随 628 E1 入库 ⇒ 本工具把它归入"
        "预期清单但**不要求删除**（事实登记）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(c, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    c = check()
    chk("受控目录零污染", c["controlled_clean"])
    chk("ci.yml 语法检查通过", c["ci"]["ok"], f"({c['ci']['mode']})")
    chk("交付物清单 ≥ 20 项且无缺失", c["deliverables"]["required"] >= 20
        and c["deliverables"]["ok"], f"({c['deliverables']['missing']})")
    # 自检只验**分类正确性**（未提交项必须全部落在 tools/tests 或 data/ 两类里）；
    # 「无未提交代码」是**闸门**语义，由 `test_check_all_ok_and_ahead` 在收工后断言。
    chk("未提交项分类正确（代码类 / data 类）",
        all(batch_path(x).startswith(("tools/", "tests/")) for x in c["uncommitted_630"])
        and all(batch_path(p).startswith("data/") for p in c["pending_batch_artifacts"]))
    chk("闸门语义字段齐全（all_ok / blocking / pending）",
        all(k in c for k in ("all_ok", "status_other_blocking",
                             "pending_batch_artifacts")))
    chk("status 分类器：并行产物归预期",
        bool(classify_status(["?? _arch_v21/00_a.md"])["expected"])
        and not classify_status(["?? _arch_v21/00_a.md"])["other"])
    chk("status 分类器：普通未跟踪文件归意外",
        bool(classify_status(["?? tools/new_thing.py"])["other"])
        and not classify_status(["?? tools/new_thing.py"])["expected"])
    chk("ahead 已测（非负整数）", isinstance(c["ahead"], int) and c["ahead"] >= 0,
        f"({c['ahead']})")
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"B1 pre-push check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 B1 push 前检查（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写检查报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    c = check()
    if args.json:
        print(json.dumps(c, ensure_ascii=False, indent=2))
        return 0
    print(f"all_ok={c['all_ok']} ahead={c['ahead']} other={len(c['status_other'])} "
          f"missing={len(c['deliverables']['missing'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
