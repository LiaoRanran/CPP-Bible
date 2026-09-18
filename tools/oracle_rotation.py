#!/usr/bin/env python3
"""oracle_rotation.py — 验证者换代**影响面**只读报告（583 任务 3 / 调研包 `_arch_v9/03` 的 N3）。

回答的问题：**"g++ 升到 16 / 规则引擎重写之后，哪些结论必须重验？"**

今天（2026-09-18）的诚实答案是：**全体**——因为卡面的 `verified_by_oracle` **83 张卡 0 张填**
（`_arch_v9/01` 实测），机器无从细分归属 ⇒ 保守按"全部强制重验"。报告必须把这句话说成人话，
**不许**让读者以为"stale 0 条 = 版本齐备"。

硬纪律（583 §任务 3）：
  * **只读**：不写 registry、不写任何文件、**不跑** gate/replay/poison/mutation（只列"需重跑清单"）；
    源码不含判决入口（`gate_engine.run` / `replay.replay_card`）调用；
  * 与 `metrics_collector.oracle_report()` 的 stale 判定**双实现对账**（不一致 ⇒ 以参考实现为准并报错）；
  * **继承必须 fail-closed 的立场只写进报告文案**：本批**不实现**继承逻辑、不实现签名（冻结项）。

用法::

    python tools/oracle_rotation.py --check-registry      # 只对账"卡面 vs registry"
    python tools/oracle_rotation.py --to gcc=16.0.0       # 假设换代后的影响面
    python tools/oracle_rotation.py --json                # 机器读（确定性）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "data" / "oracle_registry.json"
VERSION = "v1.0"

# 换代后必须重跑的"验证者指纹"（本工具**不跑**它们，只列清单——跑它们会改基线，属另一批）
CHECKLIST = (
    ("gate 规则/命中", "python tools/gate_engine.py --check", "规则数 + 命中数（block/warn/advice）"),
    ("replay 复算", "python tools/atom_evidence_replay.py --check", "confirm / refute / infra_error"),
    ("poison 制衡层", "python tools/poison_drill.py", "通过数 + RULE-COVERAGE + legacy 豁免"),
    ("mutation 权威值", "python tools/mutation_fuzz.py --cards all --limit 999 "
                        "--report <tmp>", "blocked/escaped/n_a 逐算子"),
)

FAIL_CLOSED_NOTE = (
    "**继承默认 fail-closed**：任何「版本号向前兼容 ⇒ 结论自动继承」的做法都视为**危险**——"
    "攻击者只要把 registry 里的版本号改成兼容形态，就能让结论免于重验。"
    "兼容性声明必须绑定**人签**（本仓已有先例：`log_overturned()` 要求 human 名与该卡最后一次 "
    "git 提交作者一致）。本批**不实现**继承逻辑、**不实现**签名（冻结项）——只把清单与立场写给监工。"
)


def _load_registry() -> dict:
    if not REGISTRY.is_file():
        print(f"[oracle_rotation] ❌ registry 不存在：{REGISTRY}", file=sys.stderr)
        raise SystemExit(2)
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8")) or {}
    except ValueError as exc:
        print(f"[oracle_rotation] ❌ registry 解析失败：{exc}", file=sys.stderr)
        raise SystemExit(2)


def _load_cards() -> list[dict]:
    """只读加载全库卡面的 `verified_by_oracle`（与 `metrics_collector.oracle_report()` 同源的输入）。"""
    sys.path.insert(0, str(ROOT / "tools"))
    import atom_evidence_replay as replay
    out: list[dict] = []
    for base, pat in ((ROOT / "atoms", "ATOM-*.md"), (ROOT / "evidence", "EV-*.md")):
        for p in sorted(base.rglob(pat)):
            if not p.is_file():
                continue
            try:
                meta = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
            except ValueError:
                meta = {}
            out.append({"id": meta.get("id") or p.stem,
                        "path": p.relative_to(ROOT).as_posix(),
                        "verified_by_oracle": meta.get("verified_by_oracle")})
    return out


def _parse_to(spec: str | None) -> dict[str, str]:
    """`--to gcc=16.0.0,gate_engine=M5-x` ⇒ {"gcc": "16.0.0", ...}。"""
    want: dict[str, str] = {}
    for item in (spec or "").split(","):
        item = item.strip()
        if not item:
            continue
        if "=" not in item:
            print(f"[oracle_rotation] ❌ --to 需要 `名字=版本` 形式：{item!r}", file=sys.stderr)
            raise SystemExit(2)
        name, ver = item.split("=", 1)
        want[name.strip()] = ver.strip()
    return want


def build_report(to: str | None = None) -> dict:
    reg = _load_registry()
    oracles = (reg.get("oracles") or {}) if isinstance(reg, dict) else {}
    deleg = (reg.get("delegation") or {}) if isinstance(reg, dict) else {}
    cards = _load_cards()
    want = _parse_to(to) or {n: str((v or {}).get("version") or "") for n, v in oracles.items()}

    missing = [c for c in cards if not c.get("verified_by_oracle")]
    mismatch: list[dict] = []
    for c in cards:
        vo = c.get("verified_by_oracle")
        if not vo:
            continue
        name = str(vo.get("oracle") if isinstance(vo, dict) else vo)
        ver = str(vo.get("version") or "") if isinstance(vo, dict) else ""
        want_ver = want.get(name) or str((oracles.get(name) or {}).get("version") or "")
        if name not in oracles or (want_ver and ver and ver != want_ver):
            mismatch.append({"card": c["id"], "path": c["path"], "have": {"oracle": name, "version": ver},
                             "want": want_ver or "<未登记>"})

    # 判据细分：registry 里**没有** `judges`/`invalidates_on_change` 时 ⇒ 无法细分 ⇒ 全体强制重验
    can_split = any(isinstance(v, dict) and ("judges" in v or "invalidates_on_change" in v)
                    for v in oracles.values())
    # 保守集合：无归属 + 不匹配，都进强制重验；无法细分时**全部卡**进（今天就是这一档）
    force_cards = sorted({c["id"] for c in cards}) if not can_split else \
        sorted({c["id"] for c in cards if not c.get("verified_by_oracle")} |
               {m["card"] for m in mismatch})
    return {
        "version": VERSION,
        "asked_to": want,
        "registry_current": {n: str((v or {}).get("version") or "") for n, v in oracles.items()},
        "registry_has_split_fields": can_split,
        "delegation_switches": deleg.get("switches") or {},
        "counts": {"cards_total": len(cards),
                   "cards_missing_oracle": len(missing),
                   "cards_mismatch": len(mismatch),
                   "cards_force_revalidate": len(force_cards)},
        "force_revalidate_cards": force_cards,
        "missing_oracle_cards": [c["path"] for c in missing],
        "mismatch": sorted(mismatch, key=lambda d: d["card"]),
        "recheck_checklist": [{"what": w, "command": cmd, "records": rec}
                              for w, cmd, rec in CHECKLIST],
        "stance": FAIL_CLOSED_NOTE,
        "honest_note": ("无归属 ⇒ 保守全量重验：这是**缺口未补的代价**（83 张卡 0 张填 "
                        "`verified_by_oracle`），不是「版本齐备」。补字段是人/强模型的活，机器只列缺。"),
    }


def _print_human(rep: dict) -> None:
    c = rep["counts"]
    print(f"[oracle_rotation] {rep['version']} · 目标版本 {rep['asked_to']}")
    print(f"[oracle_rotation] registry 现有 oracle：{rep['registry_current']} · "
          f"放权开关 {rep['delegation_switches']}")
    print(f"[oracle_rotation] 卡 {c['cards_total']} 张：缺 oracle 字段 {c['cards_missing_oracle']} · "
          f"版本不匹配 {c['cards_mismatch']} ⇒ **强制重验 {c['cards_force_revalidate']} 张**")
    print(f"[oracle_rotation] ⚠ {rep['honest_note']}")
    if not rep["registry_has_split_fields"]:
        print("[oracle_rotation] ⚠ registry 无 `judges`/`invalidates_on_change` ⇒ **无法细分** ⇒ "
              "一律按全体强制重验（建议字段已在报告中给出，**本工具不落盘**）")
    print("[oracle_rotation] 换代后必须重跑（本工具**不跑**它们，只列清单）：")
    for it in rep["recheck_checklist"]:
        print(f"   - {it['what']:14s} `{it['command']}`  → 记录 {it['records']}")
    print(f"[oracle_rotation] {rep['stance']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="583 N3：验证者换代影响面（只读；不跑任何 --check）")
    ap.add_argument("--to", default=None,
                    help="假设换代目标，形如 `gcc=16.0.0`（可逗号分隔多个）；缺省=按 registry 现值对账")
    ap.add_argument("--check-registry", action="store_true",
                    help="只做「卡面 vs registry」对账（等价于不给 --to）")
    ap.add_argument("--json", action="store_true", help="输出 JSON（确定性）")
    a = ap.parse_args(argv)
    rep = build_report(None if a.check_registry else a.to)
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1, sort_keys=True))
    else:
        _print_human(rep)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
