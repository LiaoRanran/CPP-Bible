#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""564 PoC-2 · 毒样例供给链：覆盖率"自证"与豁免台账"自批"（meta 层）。

只读正式文件；演示全部针对进程内 monkeypatch / TEMP 文本副本，不写正式目录。

证明两件事：
  A. RULE-COVERAGE 的 covered 集合是用正则在 poison_drill【自己的源码】里
     grep `"RULE-ID" in who` 文本得到的（poison_drill.rule_coverage 实现）——
     攻击者只要往源码加一行这种字符串（不需要任何真载荷触发），覆盖率即+1；
  B. poison_exemptions.yaml 的豁免由工具自行解析、无签名：自写一条
     id/reason/date 即可把任意未覆盖规则永久移出分母（load_exemptions 原样接受）。
复跑：.venv\\Scripts\\python.exe _arch_v7\\probes\\poc2_poison_self_attest.py
"""
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))


def main():
    import poison_drill as pd

    # ── 基线：当前真实覆盖率与未覆盖清单 ────────────────────────────────────
    covered_n, total_n, uncovered = pd.rule_coverage()
    print(f"[基线] 已覆盖 {covered_n}/{total_n}；未覆盖 {len(uncovered)}：{uncovered[:5]}")

    # ── A. covered 是源码文本自证：往 TEMP 副本注入一行无载荷字符串即+1 ────
    src = Path(pd.__file__).read_text(encoding="utf-8")
    fake_id = "FAKE-COVERAGE-NO-PAYLOAD"
    injected = src + f'\n# "{fake_id}" in who   # 攻击者注释行：没有任何对应毒载荷\n'
    # 复刻 rule_coverage 里的同一正则（poison_drill.py:1955 附近）
    covered_real = set(re.findall(r'"([A-Z][A-Z0-9-]+)" in who', src))
    covered_fake = set(re.findall(r'"([A-Z][A-Z0-9-]+)" in who', injected))
    gained = covered_fake - covered_real
    print(f"[A] 注入 0 个真载荷、仅 1 行文本后，covered 新增: {sorted(gained)}")
    print(f"[A] 该 ID 在 RULES 注册表里吗: {fake_id in {r.id for r in __import__('gate_engine').RULES}}")
    print("[A] → 对已注册未覆盖规则，同样手法可在不构造任何攻击的情况下谎报覆盖")
    assert fake_id in gained

    # ── B. 豁免台账自批：TEMP 里写一条豁免，load_exemptions 原样接受 ────────
    with tempfile.TemporaryDirectory(prefix="p564_poc2_") as td:
        fake_exempt = Path(td) / "poison_exemptions.yaml"
        target = uncovered[0] if uncovered else "EV-FM-DUP-KEY"
        fake_exempt.write_text(
            f'- {{id: {target}, reason: "攻击者自写理由，无签名无复核", date: 2026-09-17}}\n',
            encoding="utf-8")
        # 用工具自己的解析器逻辑（临时把它的 EXEMPTIONS 路径指过去）
        orig_path = pd.EXEMPTIONS
        pd.EXEMPTIONS = fake_exempt
        try:
            accepted = pd.load_exemptions()
        finally:
            pd.EXEMPTIONS = orig_path
        print(f"[B] 自写豁免条目被 load_exemptions 接受: {target} → {accepted.get(target)!r}")
        assert target in accepted

        # 覆盖率判定因此把该规则移出 uncovered（复刻 rule_coverage 集合运算）
        exempt = set(accepted)
        still = sorted(({r.id for r in __import__("gate_engine").RULES}
                        - covered_real - exempt))
        moved = target not in still
        print(f"[B] 该规则在 uncovered 中被移除: {moved}（分母自缩，CI 转绿）")
        assert moved or target not in uncovered

    print("\n结论【已实证】：覆盖率=源码文本自证（无载荷也可+1）；")
    print("豁免台账=无签名自批（任意 id 可永久移出分母）。两者均无外部 Oracle。")


if __name__ == "__main__":
    main()
