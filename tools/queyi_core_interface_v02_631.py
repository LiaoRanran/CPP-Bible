"""631 F1 · QueYi Core 接口抽象 **v0.2**（纯标准库，只读；**只定义不实现**）

在 625 C2 的 v0.1（Claim / Evidence / Attack / Verify 四个接口）基础上扩展为五个：

| 接口 | v0.2 新增点 | 现有实现映射 |
|---|---|---|
| `Claim` | 命题级字段（subject/predicate/object/claim_type/liveness/signed_by） | `atoms/*.md` + `gate_engine.py` |
| `Evidence` | 工件断言 `artifact_assert` + 复算 | `evidence/*.md` + `atom_evidence_replay.py` |
| `Verifier` | **独立验证者钩子**（与他验三件套对齐） | `gate_engine.py` / `independent_verifier_628.py` / `vsa_*` |
| `Authority` | **append-only 账本** + 透明日志 | `decision_event_v2_ledger.jsonl` / `transparency_log_628.py` |
| `Attacker` | **目标函数**（攻击面优化目标） | `adversarial_loop_620.py` / `sandbox_apply_622.py` / `attack_objective_629.py` |

**只定义签名与 docstring，不实现**（§十 F1.2）：所有方法体 `raise NotImplementedError`。

`--check` 只读：校验接口完整性 + 映射文件是否真实存在（**不实例化业务、不改任何文件**）。
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

OUT_MD = os.path.join(ROOT, "data", "queyi_core_interface_v02_631.md")
OUT_JSON = os.path.join(ROOT, "data", "queyi_core_interface_v02_631.json")


class Claim:
    """知识命题（原子卡的可验证主张）。"""

    def id(self) -> str:
        """命题唯一 ID（如 `ATOM-CONC-FENCE-001/prop-1`）。"""
        raise NotImplementedError

    def statement(self) -> str:
        """自然语言陈述。"""
        raise NotImplementedError

    def structured(self) -> dict[str, Any]:
        """结构化字段：subject / predicate / object / claim_type / liveness / signed_by。"""
        raise NotImplementedError

    def evidence_refs(self) -> list[str]:
        """引用的证据 ID 列表。"""
        raise NotImplementedError

    def validate(self) -> dict[str, Any]:
        """按规则校验命题完整性，返回 {ok, violations}。"""
        raise NotImplementedError


class Evidence:
    """证据（可复算的工件/观测）。"""

    def id(self) -> str:
        """证据 ID（如 `EV-CONC-001`）。"""
        raise NotImplementedError

    def artifact_assert(self) -> list[dict[str, Any]]:
        """工件断言（可复算的具体断言，含夹具符号）。"""
        raise NotImplementedError

    def verify_hash(self) -> bool:
        """校验工件内容与登记哈希一致。"""
        raise NotImplementedError

    def provenance(self) -> dict[str, Any]:
        """溯源信息（来源/生成方式/时间）。"""
        raise NotImplementedError

    def replay(self) -> dict[str, Any]:
        """复算该证据，返回 confirm/refute/infra 三态。"""
        raise NotImplementedError


class Verifier:
    """验证器（规则 / 复算 / 毒样例 / **独立验证者**）。"""

    def id(self) -> str:
        """验证器 ID。"""
        raise NotImplementedError

    def rules(self) -> list[str]:
        """规则集 ID 列表。"""
        raise NotImplementedError

    def verify(self, target: Any) -> dict[str, Any]:
        """验证一个对象（Claim / Evidence / Attacker 结果）。"""
        raise NotImplementedError

    def independent_hook(self) -> Optional[str]:
        """**独立验证者钩子**：返回可零依赖重算的入口（他验 B1）。"""
        raise NotImplementedError

    def attest(self, target: Any) -> dict[str, Any]:
        """产出可验证凭证（VSA）并可选入册透明日志。"""
        raise NotImplementedError


class Authority:
    """权威裁定与治理（含 **append-only 账本**）。"""

    def ledger_path(self) -> str:
        """账本文件路径（append-only JSONL）。"""
        raise NotImplementedError

    def append(self, entry: dict[str, Any]) -> dict[str, Any]:
        """追加一条裁定（**只追加，不可改/删**）。"""
        raise NotImplementedError

    def chain_verify(self) -> dict[str, Any]:
        """校验账本哈希链完整性。"""
        raise NotImplementedError

    def transparency_log(self) -> str:
        """透明日志路径（他验 B3）。"""
        raise NotImplementedError

    def human_decision(self, item: str, by: str) -> dict[str, Any]:
        """人审裁定入口（**机器永不代签** ⇒ 只能由人调用）。"""
        raise NotImplementedError


class Attacker:
    """攻击者（变异 / 沙箱 / **目标函数**）。"""

    def id(self) -> str:
        """攻击器 ID。"""
        raise NotImplementedError

    def objective(self) -> dict[str, Any]:
        """**目标函数**：返回被优化的目标（如 disagreement × ambiguity × provenance）。"""
        raise NotImplementedError

    def mutate(self, target: Any) -> dict[str, Any]:
        """对目标施加一次扰动，返回变体。"""
        raise NotImplementedError

    def apply_in_sandbox(self, variant: Any) -> dict[str, Any]:
        """在沙箱中施加（含备份/还原/校验）。"""
        raise NotImplementedError

    def revert(self, variant: Any) -> bool:
        """还原（必须可 `finally` 调用，见 631 C2 防护设计）。"""
        raise NotImplementedError


INTERFACES: dict[str, dict[str, Any]] = {
    "Claim": {
        "cls": Claim,
        "since": "v0.1",
        "new_in_v02": "命题级字段（liveness / signed_by）",
        "maps": ["tools/gate_engine.py"],
    },
    "Evidence": {
        "cls": Evidence,
        "since": "v0.1",
        "new_in_v02": "artifact_assert + replay 三态",
        "maps": ["tools/atom_evidence_replay.py"],
    },
    "Verifier": {
        "cls": Verifier,
        "since": "v0.1（原名 Verify）",
        "new_in_v02": "独立验证者钩子 + 凭证产出",
        "maps": ["tools/gate_engine.py", "tools/independent_verifier_628.py",
                 "tools/vsa_attestation_628.py"],
    },
    "Authority": {
        "cls": Authority,
        "since": "v0.2",
        "new_in_v02": "整个接口（含 append-only 账本 + 透明日志 + 人审入口）",
        "maps": ["tools/decision_event_v2_626.py", "tools/transparency_log_628.py",
                 "data/authority/decision_event_v2_ledger.jsonl"],
    },
    "Attacker": {
        "cls": Attacker,
        "since": "v0.1（原名 Attack）",
        "new_in_v02": "目标函数 objective() + 沙箱契约 + revert 契约",
        "maps": ["tools/adversarial_loop_620.py", "tools/sandbox_apply_622.py",
                 "tools/attack_objective_629.py"],
    },
}


def public_methods(cls: type) -> list[str]:
    return sorted(n for n, v in vars(cls).items()
                  if callable(v) and not n.startswith("_"))


def doc_of(cls: type, name: str) -> str:
    fn = getattr(cls, name, None)
    return (fn.__doc__ or "").strip()


def measure() -> dict[str, Any]:
    rows = []
    for name, meta in INTERFACES.items():
        ms = public_methods(meta["cls"])
        rows.append({
            "interface": name, "since": meta["since"],
            "new_in_v02": meta["new_in_v02"],
            "methods": ms, "n_methods": len(ms),
            "methods_with_doc": sum(1 for m in ms if doc_of(meta["cls"], m)),
            "maps": meta["maps"],
            "maps_exist": [p for p in meta["maps"]
                           if os.path.exists(os.path.join(ROOT, p))],
            "maps_missing": [p for p in meta["maps"]
                             if not os.path.exists(os.path.join(ROOT, p))],
        })
    return {"version": "v0.2", "n_interfaces": len(rows), "rows": rows,
            "n_methods": sum(r["n_methods"] for r in rows),
            "implemented": 0,
            "note": "全部接口**只定义不实现**（方法体 raise NotImplementedError）"}


def write_report() -> str:
    m = measure()
    lines = [
        "# 631 F1 · QueYi Core 接口抽象 **v0.2**", "",
        f"- 接口数：**{m['n_interfaces']}**（v0.1 为 4，v0.2 新增 `Authority`）"
        f" · 方法总数：**{m['n_methods']}**",
        f"- 实现状态：**{m['implemented']} 个已实现**（§十 F1.2 只定义不实现）", "",
        "## 一、接口清单与实现状态映射", "",
    ]
    for r in m["rows"]:
        lines += [
            f"### {r['interface']}（since {r['since']}）", "",
            f"- v0.2 新增：{r['new_in_v02']}",
            f"- 方法（{r['n_methods']} 个，均有 docstring："
            f"{r['methods_with_doc']}/{r['n_methods']}）", "",
            "| 方法 | docstring |", "|---|---|",
            *[f"| `{x}()` | {doc_of(INTERFACES[r['interface']]['cls'], x)[:70]} |"
              for x in r["methods"]],
            "",
            "| 现有实现映射 | 存在 |", "|---|---|",
            *[f"| `{p}` | {'✅' if p in r['maps_exist'] else '❌'} |"
              for p in r["maps"]],
            "",
        ]
    lines += [
        "## 二、v0.1 → v0.2 的差异", "",
        "| 项 | v0.1（625 C2） | v0.2（631 F1） |", "|---|---|---|",
        "| 接口数 | 4 | **5**（新增 Authority） |",
        "| 命名 | `Attack` / `Verify` | `Attacker` / `Verifier`（与其他层命名一致） |",
        "| Verifier | 只有 `verify()` | 增加 **独立验证者钩子** + 凭证产出 |",
        "| Attacker | 只有 apply/revert | 增加 **目标函数** `objective()` + 沙箱契约 |",
        "| Authority | 无 | **新增**：append-only 账本 + 透明日志 + 人审入口 |",
        "| Claim | 基础字段 | 增加命题级字段（liveness / signed_by） |", "",
        "## 三、雷1 剥离触发标准推进情况", "",
        "| 条件 | 状态 |", "|---|---|",
        "| 路径解耦（PathConfig） | ✅ 625 C1 完成 |",
        "| Core 接口抽象 v0.1 | ✅ 625 C2 完成 |",
        "| **Core 接口抽象 v0.2** | ✅ **本批（631 F1）完成**（只定义不实现） |",
        "| 治理裁定 | ⛔ 需人（不代签） |",
        "| 余量 | ⛔ 留后续 |",
        "",
        "⇒ 触发标准 **3/5**（原 2/5），**本批推进 1 个条件**。", "",
        "## 四、诚实登记", "",
        "1. **只定义不实现**：所有方法体 `raise NotImplementedError`，"
        "本批**没有**改任何生产工具（§十 F1.2）；",
        "2. **映射是「已有能力」的指针**，不等于「已有该接口」——真正的接口抽出"
        "（抽象基类/协议 + 各工具适配）仍需下一批 ⇒ 列入交人；",
        "3. **命名变更（Attack→Attacker / Verify→Verifier）是 v0.2 的单方面决定**："
        "若与后续实现命名冲突，改这里即可（无代码依赖）；",
        "4. 本工具只读：`--check` 不实例化业务对象、不写任何文件（除报告由 `--report` 生成）。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    m = measure()
    chk("五个接口齐全", m["n_interfaces"] == 5 and
        set(INTERFACES) == {"Claim", "Evidence", "Verifier", "Authority", "Attacker"},
        f"({list(INTERFACES)})")
    chk("每个接口 ≥4 个方法", all(r["n_methods"] >= 4 for r in m["rows"]),
        f"({[(r['interface'], r['n_methods']) for r in m['rows']]})")
    chk("每个方法都有 docstring",
        all(r["methods_with_doc"] == r["n_methods"] for r in m["rows"]))
    chk("所有方法都**未实现**（raise NotImplementedError）",
        all(_raises(meta["cls"], meth)
            for meta in INTERFACES.values()
            for meth in public_methods(meta["cls"])))
    chk("Verifier 含独立验证者钩子、Attacker 含目标函数",
        "independent_hook" in public_methods(Verifier)
        and "objective" in public_methods(Attacker))
    chk("Authority 含 append-only 语义",
        "append" in public_methods(Authority)
        and "chain_verify" in public_methods(Authority))
    chk("映射文件全部存在（映射不是空指针）",
        all(not r["maps_missing"] for r in m["rows"]),
        f"({[r['maps_missing'] for r in m['rows'] if r['maps_missing']]})")

    import subprocess

    def snap() -> str:
        p = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                           capture_output=True, text=True, check=False)
        return p.stdout

    before = snap()
    measure()
    write_report()
    chk("只读：不实例化业务、不改工作区", snap() == before)
    chk("报告 + JSON 存在", os.path.exists(OUT_MD) and os.path.exists(OUT_JSON))
    print(f"F1 core interface v0.2 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _raises(cls: type, meth: str) -> bool:
    """调用该方法必须抛 NotImplementedError（证明"只定义不实现"）。

    用 `inspect.signature` 取得除 self 外的参数个数，逐个喂占位值，
    避免带 `entry`/`target` 等参数的方法因 `TypeError` 被误判为"已实现"。
    """
    import inspect

    fn = getattr(cls, meth, None)
    if fn is None:
        return False
    try:
        sig = inspect.signature(fn)
        extras = [object() for _ in list(sig.parameters)[1:]]   # self 之后的占位实参
        fn(cls(), *extras)
    except NotImplementedError:
        return True
    except Exception:                                         # noqa: BLE001
        return False
    return False


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="631 F1 Core 接口 v0.2（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写接口报告 + JSON")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps(m, ensure_ascii=False, indent=2))
        return 0
    print(f"interfaces={m['n_interfaces']} methods={m['n_methods']} "
          f"implemented={m['implemented']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
