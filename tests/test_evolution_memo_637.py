"""637 E · evolution_memo_637 单测（纯标准库，≥5 例）。编号 TE-1..TE-6。"""
from __future__ import annotations

import evolution_memo_637 as M


def _memo():
    return M.build_memo(*M._demo())


# TE-1：固定格式五段齐全
def test_sections():
    memo = _memo()
    for sec in ["# 阙疑进化建议书 · 自动生成", "系统体检（10 项指标）",
                "我发现的 top 5 问题", "我建议下一步做什么", "我觉得不靠谱的地方"]:
        assert sec in memo


# TE-2：10 项体检表
def test_body_ten():
    assert len(M.BODY) == 10


# TE-3：奖牌与审批声明
def test_medal_and_approval():
    memo = _memo()
    assert "🥇" in memo and "人审批后才执行" in memo


# TE-4：无候选时不崩
def test_empty_top():
    obs, errs, _ = M._demo()
    assert "无候选方案" in M.build_memo(obs, errs, {"top3": []})


# TE-5：诚实章为真（未采集重指标要自曝）
def test_unsure_light():
    obs, errs, scored = M._demo()
    obs["heavy"] = False
    memo = M.build_memo(obs, errs, scored)
    assert "未采集" in memo


# TE-6：--check 自检通过
def test_selftest():
    assert M.selftest() == 0
