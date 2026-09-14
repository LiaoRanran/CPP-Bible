"""S1-GIT-AUTHOR-BINDING 回归锁（479 任务 4 / v5-E12 观察期）。

背景：v5 报告 E12 —— `human:liaoranran` 自签在修复前**零 block 零 warn**：签收机制只验
「名字在册」，不验「签字者与产出者同一人」。

本规则是**可机器核实的下限**（人级签收 vs 该文件 git 最后作者），且明确只到 warn：
协作代签与历史迁移都可能造成"作者≠签收人"，block 会砸非本代罪。下列测试锁定该语义边界。
"""
from __future__ import annotations

from pathlib import Path

import pytest

import gate_engine as ge

HIST = ("\n  - {level: draft, at: legacy, by: writer:agent}"
        "\n  - {level: machine-verified, at: 2026-09-12, by: machine:gate}"
        "\n  - {level: human-verified, at: 2026-09-13, by: human:liaoranran}")


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    (tmp_path / "atoms").mkdir()
    monkeypatch.setattr(ge, "_GIT_AUTHOR_CACHE", {})
    return tmp_path


def _atom(sb: Path, cid: str, hist: str = HIST,
          verified_by: str = "human:liaoranran") -> Path:
    p = sb / "atoms" / f"{cid}.md"
    p.write_text("---\nid: " + cid + "\ntitle: t\ndomain: MEM\ntype: mechanism\n"
                 "status: human-verified\nclaim: c\nclaim_boundary: b\nrelations: []\n"
                 "evidence: [EV-MEM-X]\nsources: [{kind: iso, ref: X, independent: true}]\n"
                 "first_hand: true\nsuperiority: 真实增量\ndepth: asm\npedagogy: p\n"
                 "dal: B\nhuman_review: required\n"
                 f"status_history:{hist}\nverified_by: {verified_by}\n---\n",
                 encoding="utf-8")
    return p


def _author(monkeypatch: pytest.MonkeyPatch, value: tuple[str, str] | None) -> None:
    monkeypatch.setattr(ge, "_git_author_for", lambda _p: value)


# ── 正例 ──────────────────────────────────────────────────────────────────
def test_mismatch_warns(sb: Path, monkeypatch: pytest.MonkeyPatch):
    """签收名 ≠ 该文件 git 作者 → 命中，且**级别必须是 warn**（观察期不阻断）。"""
    _atom(sb, "ATOM-MEM-GA1")
    _author(monkeypatch, ("someone-else", "other@example.com"))
    hits = ge.check_git_author_binding()
    assert len(hits) == 1, hits
    assert hits[0].rule_id == "S1-GIT-AUTHOR-BINDING"
    assert hits[0].severity == "warn", "观察期不得升 block（协作代签/历史迁移会误伤）"


def test_rule_registered_as_warn():
    r = next((x for x in ge.RULES if x.id == "S1-GIT-AUTHOR-BINDING"), None)
    assert r is not None and r.severity == "warn", r


# ── 反例：宽松匹配必须放行 ─────────────────────────────────────────────────
@pytest.mark.parametrize("author", [
    ("liaoranran", "x@y.z"),                     # 同名
    ("LiaoRanran", "x@y.z"),                     # 大小写差异
    ("某人", "liaoranran@example.com"),          # 邮箱前缀匹配
    ("Liao Ranran", "x@y.z"),                    # 空格/分隔符差异（归一后包含）
])
def test_loose_match_passes(sb: Path, monkeypatch: pytest.MonkeyPatch,
                            author: tuple[str, str]):
    _atom(sb, "ATOM-MEM-GA2")
    _author(monkeypatch, author)
    assert ge.check_git_author_binding() == [], f"宽松匹配失败：{author}"


# ── 边界 ─────────────────────────────────────────────────────────────────
def test_git_unavailable_skips(sb: Path, monkeypatch: pytest.MonkeyPatch):
    """git 不可用（CI 浅克隆/无仓库）⇒ 跳过不报警（门禁不因环境差异改变结论）。"""
    _atom(sb, "ATOM-MEM-GA3")
    _author(monkeypatch, None)
    assert ge.check_git_author_binding() == []


def test_no_human_signoff_not_checked(sb: Path, monkeypatch: pytest.MonkeyPatch):
    """纯机器/红队签收的原子不适用本规则（不产生噪音）。"""
    _atom(sb, "ATOM-MEM-GA4",
          hist="\n  - {level: draft, at: legacy, by: writer:agent}"
               "\n  - {level: machine-verified, at: 2026-09-12, by: machine:gate}",
          verified_by="machine:gate")
    _author(monkeypatch, ("someone-else", "other@example.com"))
    assert ge.check_git_author_binding() == []


def test_multiple_signoffs_reported_once(sb: Path, monkeypatch: pytest.MonkeyPatch):
    """同一原子多处 human 签收只报一条（聚合，避免刷屏）。"""
    _atom(sb, "ATOM-MEM-GA5")
    _author(monkeypatch, ("nobody", "nobody@example.com"))
    hits = ge.check_git_author_binding()
    assert len(hits) == 1, f"应聚合为一条：{hits}"


def test_git_author_lookup_cached(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """`_git_author_for` 结果缓存：同一路径不重复调用 git（27 原子 ≈1.5s 的关键）。"""
    calls: list[int] = []
    real_run = ge.subprocess.run

    def fake_run(argv, **kw):                       # noqa: ANN001
        calls.append(1)

        class R:
            returncode = 0
            stdout = "LiaoRanran\x1f1026708211@qq.com\n"
        return R()

    monkeypatch.setattr(ge.subprocess, "run", fake_run)
    monkeypatch.setattr(ge, "_GIT_AUTHOR_CACHE", {})
    p = tmp_path / "x.md"
    assert ge._git_author_for(p) == ("LiaoRanran", "1026708211@qq.com")
    assert ge._git_author_for(p) == ("LiaoRanran", "1026708211@qq.com")
    assert len(calls) == 1, "第二次应命中缓存"
    monkeypatch.setattr(ge.subprocess, "run", real_run)
