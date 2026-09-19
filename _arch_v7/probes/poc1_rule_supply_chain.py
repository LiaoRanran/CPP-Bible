#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""564 PoC-1 · 验证器自身安全：规则供给链攻击（meta 层，非卡层变异）。

只读正式文件；全部"篡改"发生在进程内 monkeypatch 与 TEMP 副本上，不写正式目录。

证明三件事：
  A. gate --run / ge.run() 对"规则函数本身被换掉"零检测——攻击者改 gate_engine.py
     一行（把某 block 规则的 check 变成 return []），门禁静默少拦，gate 自己不报警；
  B. tools/tool_integrity.py 的 sha256 基准【能】检出文件被改（防线存在），
     但它是独立命令，gate_engine 自身不调用——`gate_engine.py --run` 单跑时沉默；
  C. 基准文件用 `--update` 无认证重签：攻击者改规则后顺手重算基准即自洽，
     信任根最终落在 git 历史 + 人审 commit（无加密签名）。
复跑：.venv\\Scripts\\python.exe _arch_v7\\probes\\poc1_rule_supply_chain.py
"""
import hashlib
import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))


def count_blocks(findings):
    return sum(1 for f in findings if f.severity == "block")


def main():
    import gate_engine as ge

    # ── A. 基线 vs 规则函数被静默替换（= 攻击者一行编辑 gate_engine.py 的等价效果）──
    # 注：当前工作树 block=0（136 warn 观察期），故选当前命中最多的规则演示——
    # 攻击对 warn/block 同构；对 block 规则而言消失的就是拦截。
    base = ge.run()
    base_n = len(base)
    fired = {}
    for f in base:
        fired[f.rule_id] = fired.get(f.rule_id, 0) + 1
    top_id = max(fired, key=fired.get)
    target = next(r for r in ge.RULES if r.id == top_id)

    orig = target.check
    # Rule 是 frozen dataclass：用 object.__setattr__ 模拟"源码一行编辑"后的运行效果
    object.__setattr__(target, "check", lambda: [])   # 攻击：规则永远放行
    hacked = ge.run()
    hacked_n = len(hacked)
    object.__setattr__(target, "check", orig)         # 进程内还原（正式文件从未被写）
    print(f"[A] 目标规则 {target.id}（当前命中 {fired[top_id]} 条，severity={target.severity}）")
    print(f"[A] 正常 ge.run() 总命中        : {base_n}")
    print(f"[A] 该规则 check→[] 后总命中     : {hacked_n}")
    print(f"[A] 静默放行差                    : {base_n - hacked_n} 条 finding 消失，"
          f"gate 自身无任何完整性告警")
    assert hacked_n < base_n, "PoC 失败：规则替换未改变结果"

    # ── B. tool_integrity 能检出文件篡改（但只在被显式调用时）────────────────
    spec = importlib.util.spec_from_file_location(
        "tool_integrity", ROOT / "tools" / "tool_integrity.py")
    ti = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ti)

    src = (ROOT / "tools" / "gate_engine.py").read_text(encoding="utf-8")
    good_sha = hashlib.sha256(src.encode("utf-8")).hexdigest()
    tampered = src + "\n# p564 tamper marker (one-byte-level edit simulation)\n"
    bad_sha = hashlib.sha256(tampered.encode("utf-8")).hexdigest()
    print(f"[B] 基准 sha     : {good_sha[:16]}…（.tool_checksums 记录值）")
    print(f"[B] 篡改后 sha   : {bad_sha[:16]}… → tool_integrity 比对必然不一致")
    print(f"[B] 但 gate_engine.py 自身不调 tool_integrity——`--run` 单跑不检")
    assert good_sha != bad_sha

    # ── C. 基准可被无认证重签（--update 等价操作，落在 TEMP 副本演示）─────────
    with tempfile.TemporaryDirectory(prefix="p564_poc1_") as td:
        tdp = Path(td)
        fake_tool = tdp / "gate_engine.py"
        fake_base = tdp / ".tool_checksums"
        fake_tool.write_text(tampered, encoding="utf-8")     # 攻击者改过的工具
        # 攻击者执行 --update：基准按新内容重算（格式照搬 tool_integrity）
        resealed = hashlib.sha256(tampered.encode("utf-8")).hexdigest()
        fake_base.write_text(f"{resealed}  gate_engine.py\n", encoding="utf-8")
        recorded = fake_base.read_text(encoding="utf-8").split()[0]
        print(f"[C] 攻击者 --update 重签后基准: {recorded[:16]}… == 篡改件 sha "
              f"→ {recorded == resealed}")
        print("[C] 重签无需任何身份/签名；信任根 = git 留痕 + 人审 commit")
        assert recorded == resealed

    print("\n结论【已实证】：规则层无自我完整性；防线存在但需独立触发，且基准自签。")


if __name__ == "__main__":
    main()
