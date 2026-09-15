"""530 任务5：golden_lock 的 warn 会计制度（强制 `--classify` + 四桶复算）。

为什么值得单独一个模块：本任务的两条硬约束都是**"人能核对的账"**，而不是顺手加的开关——
① 无分类**不得** accept（否则只是换个姿势整体接受债务，"逐条可解释"退化成一句理由）；
② 四桶必须能从「快照里的分类表 + 当期命中」**复算**出来（否则分类是文档、不是制度）。
两件事都不碰编译器，故归 fast 组。

**隔离纪律**：`--accept` 会改写 `tools/golden_state.json`（真实黄金基线），本模块一律把
`golden_lock.STATE` 指到 tmp，且断言"被拒绝时快照分毫未动"。
`measure()` 内含 replay（slow），本模块只验分类记账，故以受控假指标替换。
"""
import json
from pathlib import Path

import pytest

import gate_engine as ge
import golden_lock as gl


@pytest.fixture()
def sandbox(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """空内容 + 独立快照：门禁扫不到东西，accept 也写不到真实基线。"""
    monkeypatch.setattr(ge, "ATOMS", tmp_path / "atoms")
    monkeypatch.setattr(ge, "EVIDENCE", tmp_path / "evidence")
    monkeypatch.setattr(ge, "MISCONCEPTIONS", tmp_path / "misconceptions")
    for d in ("atoms", "evidence", "misconceptions"):
        (tmp_path / d).mkdir()
    state = tmp_path / "golden_state.json"
    state.write_text(json.dumps({"metrics": {"warn_findings": 0}, "accepted": []}),
                     encoding="utf-8")
    monkeypatch.setattr(gl, "STATE", state)
    # 真 measure() 要跑 replay；本模块验的是分类记账这一层，指标给受控假值
    monkeypatch.setattr(gl, "measure", lambda findings=None: {"warn_findings": 1})
    return state


def _load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def test_accept_without_classify_is_refused(sandbox: Path):
    """无 `--classify` 的 accept 必须 exit 非 0，且**不得**写快照。

    这是"停止整体 accept"的唯一硬点：拒绝发生在测量之前，基线必须分毫未动。
    """
    before = _load(sandbox)
    assert gl.cmd_check("想直接接受", None) != 0
    assert _load(sandbox) == before


@pytest.mark.parametrize("bad", ["RULE-A=maybe", "RULE-A", "=real", "", "RULE-A=real,ok"])
def test_accept_with_invalid_classify_is_refused(sandbox: Path, bad: str):
    """分类非法（值不在四桶内 / 缺 `=` / 缺规则 ID / 空串）同样拒绝，且不留痕。"""
    assert gl.cmd_check("理由", bad) != 0
    assert _load(sandbox)["accepted"] == []


def test_accept_records_classification(sandbox: Path):
    """合法分类 → accept 成功；审计记录**逐条**带分类，快照记住分类表供下轮复算。"""
    assert gl.cmd_check("530 演练", "RULE-A=real,RULE-B=legacy") == 0
    st = _load(sandbox)
    rec = st["accepted"][-1]
    assert rec["reason"] == "530 演练"
    assert rec["classify"] == {"RULE-A": "real", "RULE-B": "legacy"}
    assert st["warn_classify"] == {"RULE-A": "real", "RULE-B": "legacy"}


def test_buckets_group_warns_by_classification(sandbox: Path):
    """四桶从「快照分类表 + 当期命中」复算；未分类单独可见、不得被并进任何一桶。"""
    st = _load(sandbox)
    st["warn_classify"] = {"R1": "real", "R2": "false_positive"}
    sandbox.write_text(json.dumps(st), encoding="utf-8")

    class _F:
        def __init__(self, rid: str) -> None:
            self.rule_id, self.severity = rid, "warn"

    b = gl.warn_buckets([_F("R1"), _F("R1"), _F("R2"), _F("R3")])
    assert gl._bucket_n(b, "real") == 2
    assert gl._bucket_n(b, "false_positive") == 1
    assert gl._bucket_n(b, "legacy") == 0
    assert gl._bucket_n(b, "accepted") == 0
    assert b[gl.UNCLASSIFIED] == {"R3": 1}


def test_old_snapshot_without_classify_key_does_not_crash(sandbox: Path):
    """向后兼容：老快照无 `warn_classify` 键 → 全落"未分类"，不得抛异常。"""
    assert "warn_classify" not in _load(sandbox)
    assert gl._bucket_n(gl.warn_buckets([]), gl.UNCLASSIFIED) == 0
