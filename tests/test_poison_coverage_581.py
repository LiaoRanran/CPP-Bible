"""581 hole A 回归锁：覆盖率不可伪造（行为级 covered，非源码文本 grep）。

背景（见 _worklog_581.md）：旧 rule_coverage 从源码文本 grep `"X" in who` 计数，
会被注释/字符串污染（已出现 RULE-ID 幽灵，covered 虚高）。581 改为 drill() 运行时
收集每个**通过**载荷的 who（真实 gate 命中规则 ID），只收运行时实含且 payload 通过的规则。
本文件锁三件事：
  (a) 行为级 covered 严格 ⊆ 注册规则（无任何幽灵进分子）；
  (b) 源码里 `"X" in who` 的死文本（非注册规则）必须为 0（hole A 自检红）；
  (c) 向源码注入一行 `# ok = "FAKE-GHOST-581" in who` 死文本，行为级 covered 不得涨
      （防回归 hole A：覆盖以运行时 who 为准，文本注入无法伪造）。
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import gate_engine as ge
import poison_drill as pd
import pytest


def _rule_ids() -> set[str]:
    return {r.id for r in ge.RULES}


def test_behavioral_covered_has_no_ghost_in_numerator():
    """(a) 行为级覆盖里的每个 ID 都必须是注册规则——幽灵不得进分子。"""
    cov = pd.behavioral_covered()
    rules = _rule_ids()
    ghosts = cov - rules
    assert not ghosts, f"行为级覆盖含非规则 ID（幽灵进分子）：{sorted(ghosts)}"
    assert len(cov) == len(cov & rules)


def test_no_dead_who_text_for_non_rules():
    """(b) 源码 `"X" in who` 文本若引用非注册规则 ID，即幽灵死文本——必须为零。"""
    src = Path(pd.__file__).read_text(encoding="utf-8")
    text_claimed = set(re.findall(r'"([A-Z][A-Z0-9-]+)" in who', src))
    ghosts = text_claimed - _rule_ids()
    assert ghosts == set(), (
        f"源码存在死文本声明(非规则ID) {sorted(ghosts)} ——"
        "须删除这些注释/字符串，避免误导覆盖率口径")


def test_injected_ghost_comment_does_not_inflate_coverage(tmp_path: Path):
    """(c) 注入一行死文本 `# ok = "FAKE-GHOST-581" in who`，行为级 covered 不得涨。

    直接证明 hole A：覆盖来自运行时 who，而非源码文本——文本注入无法伪造覆盖率。
    """
    repo_root = Path(pd.__file__).resolve().parent.parent
    src = Path(pd.__file__).read_text(encoding="utf-8")
    injected = (
        src
        + '\n# 581 回归探针：ok = "FAKE-GHOST-581" in who  '
          "# 死文本，行为级覆盖必须忽略\n"
    )
    mod_file = tmp_path / "poison_drill_ghost.py"
    mod_file.write_text(injected, encoding="utf-8")

    sys.path.insert(0, str(repo_root))  # 让临时模块能 import gate_engine/toolchain
    spec = importlib.util.spec_from_file_location("poison_drill_ghost_581", mod_file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # 临时模块的文件名在仓库外，其模块级 ROOT 会解析到错误目录，导致 drill 把
    # `build/_poison_out_*.out` 写到错处、而 ge.ROOT（共享单例）仍指向仓库 ⇒ 校验读空。
    # 这里把 ROOT 钉回真实仓库根，隔离"路径错位"干扰，只验证"注入死文本不涨覆盖"。
    mod.ROOT = pd.ROOT

    real_cov = pd.behavioral_covered()
    ghost_cov = mod.behavioral_covered()
    assert "FAKE-GHOST-581" not in ghost_cov, (
        "注入死文本不应使幽灵规则进入覆盖分子（hole A 防回归失败）")
    assert ghost_cov == real_cov, "注入无害注释后行为级覆盖集合不应改变"
