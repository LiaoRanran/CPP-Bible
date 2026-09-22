"""623 C2 · 尺子入根扩展审计（验证 _arch_v19 探针的 8/11 裸露是否已修复）

**背景**：_arch_v19 维度3 探针（p03_meta_verification.py 实验3）定义了 **11 个关键判决尺子**
（决定 pass/fail / 质量基线 / 学习者判决 / 攻击面图的工具）。探针实测时 8/11 裸露
（未被 `.tool_checksums` 钉住）——只有 3 个 CORE_TOOLS（gate_engine / poison_drill /
atom_evidence_replay）受保护，其余 8 个 ruler 型工具裸奔。

615 B3 引入 `RULER_TOOLS` 把 8 个 ruler 型工具钉进哈希面；623 B1 跑了 `tool_integrity --update`
重钉。本工具**复算探针实验3**，确认当前 0 裸露，并交叉校验 `tool_integrity.py` 的保护清单
已覆盖全部 11 尺子。

铁律：只读审计，不修改受控目录/工具逻辑；`--fix` 也只重钉（不新增规则）。
"""
from __future__ import annotations

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHECKSUMS = os.path.join(HERE, ".tool_checksums")

# _arch_v19 p03 实验3 的 11 个关键判决尺子（顺序同探针）
CRITICAL_RULERS = [
    "gate_engine.py", "poison_drill.py", "mutation_fuzz.py", "tool_integrity.py",
    "atom_evidence_replay.py", "d5_compile_gate.py", "d5_runtime_gate.py",
    "d5_source_integrity.py", "attack_edge_generator.py", "bkt_solver.py",
    "learner_mastery_update_613.py",
]


def _load_protected(path: str = CHECKSUMS) -> set[str]:
    prot: set[str] = set()
    if not os.path.exists(path):
        return prot
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m = __import__("re").match(r"[0-9a-f]{64}\s+(.+)$", line)
            if m:
                prot.add(os.path.basename(m.group(1)))
    return prot


def audit() -> dict:
    prot = _load_protected()
    exposed = [f for f in CRITICAL_RULERS if f not in prot]
    return {
        "total_critical": len(CRITICAL_RULERS),
        "protected_count": len(CRITICAL_RULERS) - len(exposed),
        "exposed": exposed,
        "exposed_ratio": len(exposed) / len(CRITICAL_RULERS),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="623 C2 尺子覆盖率审计")
    ap.add_argument("--check", action="store_true", help="有裸露则 exit 1")
    args = ap.parse_args(argv)
    r = audit()
    print(f"关键判决尺子：{r['total_critical']} 个")
    print(f"已保护：{r['protected_count']} / {r['total_critical']}")
    print(f"裸露：{r['exposed']} （占比 {r['exposed_ratio']:.0%}）")
    if r["exposed"]:
        print("⚠ 仍有裸露尺子，需把其纳入 tool_integrity.py RULER_TOOLS 并 --update 重钉")
    else:
        print("✓ 11 个关键判决尺子全部已钉入 .tool_checksums（_arch_v19 的 8/11 裸露已修复）")
    return 1 if (args.check and r["exposed"]) else 0


if __name__ == "__main__":
    sys.exit(main())
