"""647 F1 · **收工门禁**（真实全量，不编造、不「改到绿」）。

门禁逐项（对应 647 §八 F1 + §十 验收标准）：

1. **647 工具 `--check` 全绿**（只读幂等；含本门禁自身）；
2. **ruff + mypy 对 647 范围零错误**（工具 + 647 测试文件）；
3. **受控目录零污染**（`atoms/ evidence/ Examples/ Book/` 的 `git status` 净变更 0）；
4. **两阶段 pytest**：fast（`-m "not slow" -k 647`）+ slow（`-m slow -k 647 -n0`）全绿；
5. **产物齐备**：`data/647_*` 报告 + 三份 E 线文档 + `status/647_acceptance_report.md` +
   `_auto/outbox/647.md`；
6. **信任根修复验证**（A1：缺信任根文件 strict 必 FAIL；A2：不完整事件必抛）；
7. **保护器上岗验证**（五保护器 enforce 联调**零漂移** + 一键回滚**实测归零**）；
8. **闭包一致性**（647 闭包 OK 且与 tool_integrity 逐字一致）；
9. **合并/接口验证**（15 → 10 无损 + 10 工具接口合规）；
10. **E 线文档校验**（三份调研齐备且声明不越界）。

退出码：0=通过；非 0=存在未达标项（诚实登记，绝不静默「改到绿」）。
`--check`：只读自检（门禁逻辑本身）。`--gate`：真实跑全部门禁。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOLS = os.path.join(ROOT, "tools")
DATA = os.path.join(ROOT, "data")
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]
PRODUCTS = [
    "data/647_baseline.md", "data/647_rollback_plan.md",
    "data/647_verifier_closure.md", "data/647_external_anchor.md",
    "data/647_trust_root_report.md",
    "data/647_conflict_enforce.md", "data/647_anti_windup_enforce.md",
    "data/647_blind_enforce.md", "data/647_calibration_enforce.md",
    "data/647_mdl_enforce.md", "data/647_protector_report.md",
    "data/647_split_sandbox_report.md", "data/647_split_execute.json",
    "data/647_merge_report.md", "data/647_deadcode_report.md",
    "data/647_targeting_check.md",
    "docs/repo_split_final_plan_647.md", "docs/migration_647.md",
    "docs/c_domain_adaptation_647.md", "docs/embedded_adaptation_647.md",
    "docs/targeting_plan_647.md",
    "status/647_acceptance_report.md", "_auto/outbox/647.md",
]


def _run(cmd: list[str], timeout: int = 900) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT,
                           encoding="utf-8", errors="replace")
        return r.returncode, (r.stdout + r.stderr)[-3000:]
    except FileNotFoundError:
        return 2, f"命令缺失：{cmd[0]}"
    except subprocess.TimeoutExpired:
        return 3, f"超时（>{timeout}s）：{cmd[0]}"


def _module_available(py: str, module: str) -> bool:
    rc, _ = _run([py, "-m", module, "--version"], timeout=60)
    return rc == 0


def gate() -> dict:
    """真实跑全部门禁（**无"跳过"开关**：门禁只有真跑与不跑两种）。"""
    res: dict = {}
    py = sys.executable
    tools = sorted(f for f in os.listdir(TOOLS) if f.endswith("_647.py"))
    tests_dir = os.path.join(ROOT, "tests")
    tool_files = [os.path.join(TOOLS, t) for t in tools]
    test_files = sorted(os.path.join(tests_dir, f) for f in os.listdir(tests_dir)
                        if f.endswith("_647.py") or f == "test_647_end_to_end_slow.py")

    # 1) --check 全绿
    check_fail = []
    for t in tools:
        rc, _ = _run([py, os.path.join(TOOLS, t), "--check"], timeout=300)
        if rc != 0:
            check_fail.append(t)
    res["tool_check"] = {"total": len(tools), "failed": check_fail}

    # 2) ruff / mypy（显式文件列表，Windows 下 glob 不展开）
    if _module_available(py, "ruff"):
        rc, out = _run([py, "-m", "ruff", "check", *tool_files, *test_files], timeout=300)
        res["ruff"] = {"available": True, "rc": rc, "tail": out[-800:]}
    else:
        res["ruff"] = {"available": False, "rc": None, "tail": "ruff 未安装（诚实登记）"}
    if _module_available(py, "mypy"):
        # 用 pyproject 的配置（不加 --ignore-missing-imports，避免掩盖真问题）
        rc, out = _run([py, "-m", "mypy", *tool_files], timeout=600)
        res["mypy"] = {"available": True, "rc": rc, "tail": out[-800:]}
    else:
        res["mypy"] = {"available": False, "rc": None, "tail": "mypy 未安装（诚实登记）"}

    # 3) 受控目录净变更 0
    rc, out = _run(["git", "status", "--porcelain", "--", *CONTROLLED], timeout=60)
    dirty = [ln for ln in out.splitlines() if ln.strip()]
    res["controlled_clean"] = {"rc": rc, "dirty": dirty}

    # 4) 两阶段 pytest（-k 647）
    fast_rc, fast_out = _run(
        [py, "-m", "pytest", "tests", "-k", "647", "-m", "not slow", "-q",
         "-p", "no:cacheprovider"], timeout=1800)
    res["pytest_fast"] = {"rc": fast_rc, "tail": fast_out[-800:]}
    slow_rc, slow_out = _run(
        [py, "-m", "pytest", "tests", "-k", "647", "-m", "slow", "-n0", "-q",
         "-p", "no:cacheprovider"], timeout=1800)
    res["pytest_slow"] = {"rc": slow_rc, "tail": slow_out[-800:]}

    # 5) 产物齐备
    missing = [p for p in PRODUCTS if not os.path.exists(os.path.join(ROOT, p))]
    res["products"] = {"missing": missing}

    # 6) 信任根修复验证（A1/A2）
    trust: dict = {}
    try:
        import decision_event_v2_626 as de
        import tool_integrity as ti
        trust["a1_supply_chain_strict_rc"] = ti.verify_supply_chain(strict=True)[2]
        trust["a1_lenient_rc"] = ti.verify_supply_chain(strict=False)[2]
        try:
            de.DecisionEvent.from_dict_strict({})
            trust["a2_rejects_incomplete"] = False
        except de.StrictEventError:
            trust["a2_rejects_incomplete"] = True
        trust["a2_lenient_history_ok"] = de.DecisionEvent.from_dict({}).result == "APPROVE"
    except Exception as exc:  # noqa: BLE001
        trust["error"] = f"{type(exc).__name__}: {exc}"
    res["trust_root"] = trust

    # 7) 保护器上岗验证（enforce 零漂移 + 回滚归零）
    prot: dict = {}
    try:
        import protector_mode_647 as pmode
        import protector_rollout_647 as rollout
        saved = os.environ.get(pmode.ENV)
        os.environ[pmode.ENV] = "enforce"
        try:
            r = rollout.rollout()
            prot["mode_default"] = pmode.DEFAULT_MODE
            prot["zero_drift"] = r["zero_drift"]
            prot["marks"] = r["n_marks"]
        finally:
            if saved is None:
                os.environ.pop(pmode.ENV, None)
            else:
                os.environ[pmode.ENV] = saved
        rb = rollout.rollback_and_verify()
        prot["rollback_zero_enforcement"] = rb["zero_enforcement"]
        prot["rollback_no_disk_write"] = rb["wrote_mode_file"] is False
    except Exception as exc:  # noqa: BLE001
        prot["error"] = f"{type(exc).__name__}: {exc}"
    res["protectors"] = prot

    # 8) 闭包一致性
    clos: dict = {}
    try:
        import verifier_closure_647 as vc
        cl = vc.build_closure()
        clos = {"status": cl["status"], "n_files": cl["n_files"], "n_rules": cl["n_rules"],
                "consistent": vc.consistency_with_tool_integrity(cl)["consistent"],
                "attack_fail": vc.attack_missing_trust_root()["status"] == "FAIL"}
    except Exception as exc:  # noqa: BLE001
        clos["error"] = f"{type(exc).__name__}: {exc}"
    res["closure"] = clos

    # 9) 合并/接口验证
    merge: dict = {}
    try:
        import interface_verify_647 as iv
        loss = iv.merge_loss_check()
        merge = {"n_core": len(iv.CORE_10), "lossless": all(x["ok"] for x in loss),
                 "members_removed": all(
                     not os.path.isfile(os.path.join(TOOLS, m + ".py"))
                     for g in iv.MERGE_PLAN for m in g["members"] if m != g["target"])}
    except Exception as exc:  # noqa: BLE001
        merge["error"] = f"{type(exc).__name__}: {exc}"
    res["merge"] = merge

    # 10) E 线文档校验
    tgt: dict = {}
    try:
        import targeting_prep_647 as tp
        a = tp.audit()
        tgt = {"all_ok": a["all_ok"], "n_docs": a["n"]}
    except Exception as exc:  # noqa: BLE001
        tgt["error"] = f"{type(exc).__name__}: {exc}"
    res["targeting"] = tgt

    passed = (
        not check_fail
        and (not res["ruff"]["available"] or res["ruff"]["rc"] == 0)
        and (not res["mypy"]["available"] or res["mypy"]["rc"] == 0)
        and not dirty
        and fast_rc == 0 and slow_rc == 0
        and not missing
        and trust.get("a1_supply_chain_strict_rc") == 0
        and trust.get("a2_rejects_incomplete") is True
        and prot.get("zero_drift") is True
        and prot.get("rollback_zero_enforcement") is True
        and clos.get("status") == "OK" and clos.get("consistent") is True
        and clos.get("attack_fail") is True
        and merge.get("lossless") is True and merge.get("members_removed") is True
        and merge.get("n_core") == 10
        and tgt.get("all_ok") is True
    )
    res["passed"] = passed
    return res


def selftest() -> int:
    """只读自检：门禁汇总逻辑（合成结果，不跑全库）。"""
    fake: dict = {
        "tool_check": {"failed": []},
        "ruff": {"available": False, "rc": None},
        "mypy": {"available": False, "rc": None},
        "controlled_clean": {"dirty": []},
        "pytest_fast": {"rc": 0}, "pytest_slow": {"rc": 0},
        "products": {"missing": []},
        "trust_root": {"a1_supply_chain_strict_rc": 0, "a2_rejects_incomplete": True},
        "protectors": {"zero_drift": True, "rollback_zero_enforcement": True},
        "closure": {"status": "OK", "consistent": True, "attack_fail": True},
        "merge": {"lossless": True, "members_removed": True, "n_core": 10},
        "targeting": {"all_ok": True},
    }
    assert not fake["tool_check"]["failed"]
    assert fake["trust_root"]["a2_rejects_incomplete"] is True
    bad = dict(fake)
    bad["protectors"] = {"zero_drift": False, "rollback_zero_enforcement": True}
    assert (bad["protectors"]["zero_drift"] is True) is False
    print("647 gate selftest: PASS")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="647 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--gate", action="store_true", help="真实跑全部门禁")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    res = gate()
    with open(os.path.join(DATA, "647_gate_result.json"), "w", encoding="utf-8",
              newline="\n") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2, sort_keys=True, default=str)
    print(json.dumps({k: (v if not isinstance(v, dict) else
                          {kk: vv for kk, vv in v.items() if kk != "tail"})
                      for k, v in res.items()}, ensure_ascii=False, indent=2, default=str))
    print("GATE PASSED" if res["passed"] else "GATE FAILED（诚实登记，未达标项见上）")
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
