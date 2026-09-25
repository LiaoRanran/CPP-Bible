"""635 V26-5 · 验证器准入表（Daubert 五问，只加数据，不改判决）

对 **67 条规则 + mutation 生成器**逐条填 Daubert 五问：
可检验性 / 同行评审 / 已知错误率 / 操作标准 / 社区接受度。

**缺失 `known_error_rate` 的验证器进入「观察态」**：**可以报信号，但不能单独判 block**
（本批**只标记，不改任何判决逻辑**，§零.1）。

关键实测：**67 条规则均无逐规则错误率**（VFDR 只记覆盖率，非错误率）⇒ 67 条全部观察态；
其下游 `mutation_generator` 有逃逸率（1/1406）⇒ **非**观察态。

**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/635_verifier_admissibility.md`。
纯标准库；≥5 例单测（tests/test_verifier_admissibility_635.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "635_verifier_admissibility.md")


def get_rules() -> list[dict[str, str]]:
    try:
        import gate_engine as ge
        return [{"id": r.id, "title": getattr(r, "title", ""), "scope": getattr(r, "scope", ""),
                 "kind": getattr(r, "kind", "")} for r in ge.RULES]
    except Exception:  # noqa: BLE001
        return []


def daubert(rule: dict[str, str]) -> dict[str, Any]:
    """五问（启发式；known_error_rate 实测全缺 ⇒ 观察态）。"""
    return {
        "id": rule["id"],
        "testable": True,                              # 每条规则都有可执行的 check 函数
        "peer_reviewed": False,                        # 无独立第三方评审记录
        "known_error_rate": False,                     # 实测：无逐规则错误率
        "operational_standard": True,                  # 有明确 scope/severity 执行口径
        "community_acceptance": rule.get("scope") in ("atom", "evidence"),
        "observation_state": True,                     # 缺 known_error_rate
    }


def mutation_generator() -> dict[str, Any]:
    return {
        "id": "mutation_generator",
        "testable": True,
        "peer_reviewed": False,
        "known_error_rate": True,                      # 逃逸率 1/1406
        "operational_standard": True,
        "community_acceptance": True,
        "observation_state": False,
    }


def rows() -> list[dict[str, Any]]:
    return [daubert(r) for r in get_rules()] + [mutation_generator()]


def stats() -> dict[str, Any]:
    rs = rows()
    obs = [r["id"] for r in rs if r["observation_state"]]
    no_err = [r["id"] for r in rs if not r["known_error_rate"]]
    return {"total": len(rs), "observation_state": obs, "n_observation": len(obs),
            "missing_known_error_rate": no_err}


def write_report() -> str:
    rs = rows()
    s = stats()
    lines = [
        "# 635 V26-5 · 验证器准入表（Daubert 五问）", "",
        f"- 验证器：**{s['total']}**（67 规则 + 1 mutation 生成器）",
        f"- **观察态**（缺 known_error_rate）：**{s['n_observation']}**", "",
        "## 一、五问填表", "",
        "| 验证器 | 可检验性 | 同行评审 | 已知错误率 | 操作标准 | 社区接受 | 观察态 |",
        "|---|---|---|---|---|---|---|"]
    for r in rs:
        lines.append(f"| `{r['id']}` | {'✅' if r['testable'] else '❌'} | "
                     f"{'✅' if r['peer_reviewed'] else '❌'} | "
                     f"{'✅' if r['known_error_rate'] else '❌'} | "
                     f"{'✅' if r['operational_standard'] else '❌'} | "
                     f"{'✅' if r['community_acceptance'] else '❌'} | "
                     f"{'⚠️ 是' if r['observation_state'] else '否'} |")
    lines += ["", "## 二、观察态验证器（可报信号，不能单独判 block）", ""]
    lines += [f"- `{x}`" for x in s["observation_state"]]
    lines += ["", "## 三、缺失 known_error_rate 的验证器", "",
              f"- **{len(s['missing_known_error_rate'])}** 个（= 全部 67 规则）", "",
              "## 诚实登记", "",
              "1. **67 规则全缺逐规则错误率**（VFDR 只记**覆盖率**，非错误率）⇒ 全部观察态；",
              "2. 五问中 `peer_reviewed` 全为 False（**无独立第三方评审记录**），"
              "`testable/operational_standard` 为 True（有 check 函数与 scope/severity 口径）；",
              "3. **「观察态」仅标记，不改任何判决逻辑**（§零.1：只加数据）——"
              "实际「不能单独判 block」的落地需人审决定（交人项）；",
              "4. 唯一 `known_error_rate=True` 的是 mutation 生成器（逃逸率 1/1406）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    rs = rows()
    chk("验证器 = 68", len(rs) == 68)
    chk("五问字段齐", set(rs[0]) >= {"testable", "peer_reviewed", "known_error_rate",
                                     "operational_standard", "community_acceptance"})
    s = stats()
    chk("观察态 = 67", s["n_observation"] == 67)
    chk("生成器非观察态", not any(r["id"] == "mutation_generator" and r["observation_state"]
                                  for r in rs))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 V26-5 验证器准入表")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    if args.json:
        print(json.dumps(stats(), ensure_ascii=False, indent=2))
        return 0
    print(stats())
    return 0


if __name__ == "__main__":
    sys.exit(main())
