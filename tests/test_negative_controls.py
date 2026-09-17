"""535 批次2 · V3 回归锁：replay 侧阴面判决（`check_negative_controls`）。

为什么单独锁：V-iso 的判决语义是**"阴面上断言依然成立 ⇒ 该卡无判别力"**（refute），而不是
"没跑成/环境不对"（infra）。这两条一旦混淆，坏阴面就会被当成环境问题**静默放行**——本文件
把每个 verdict 分支各钉一条反例/正例，且**不调真编译器**（`run_commands` 用替身），
跑得快、不进 slow 组；真编译链路另由 `tests/test_atom_evidence_replay.py` 与 56 卡全量覆盖。
"""
from __future__ import annotations

import re
from pathlib import Path

import atom_evidence_replay as rp
import pytest

YANG = """static int s_sf_a = 0;
static int s_sf_b = 0;
static int s_p_a = 0;
static int s_p_b = 0;
static long s_acc = 1;

int spin_signal_fence() {
    while (!s_sf_b) {
        __atomic_signal_fence(__ATOMIC_SEQ_CST);
    }
    return s_sf_a;
}

int spin_plain() {
    int acc = 0;
    while (!s_p_b) {
        acc += s_p_a;
    }
    return acc + s_p_a;
}

long accumulate_loop(int n) {
    long total = 0;
    for (int i = 0; i < n; ++i) {
        total += static_cast<long>(i) * 3 + s_p_a;
    }
    return total + s_acc;
}

int nested_branch(int n) {
    int r = 0;
    for (int i = 0; i < n; ++i) {
        if (i % 3 == 0) {
            r += i;
        } else if (i % 5 == 0) {
            r -= i;
        } else {
            r += 2 * i;
        }
    }
    return r;
}

int table_sum() {
    int r = 0;
    for (int i = 0; i < 8; ++i) {
        r += i * i + 1;
    }
    for (int j = 0; j < 4; ++j) {
        r -= j * 3;
    }
    return r;
}

int mix_all(int n) {
    int r = nested_branch(n) + table_sum() + spin_plain();
    r += accumulate_loop(n) > 0 ? 1 : 0;
    return r + s_p_b;
}
"""
YIN = YANG.replace("        __atomic_signal_fence(__ATOMIC_SEQ_CST);\n", "", 1)
_HEAD = "\t.globl\t_Z17spin_signal_fencev\n_Z17spin_signal_fencev:\n"
_YANG_BODY = "\tmov\teax, s_sf_b\n\tje\t.L2\n\tmov\teax, s_sf_b\n.L2:\n\tret\n"


def _asm(body: str) -> str:
    return _HEAD + body


def _nc(**over) -> dict:
    nc = {
        "id": "nc1",
        "variant": "v1",
        "mutation": "delete_mechanism",
        "fixture": "y.nc1.cpp",
        "anchor": "spin_signal_fence",
        "remove": "__atomic_signal_fence(__ATOMIC_SEQ_CST);",
        "retain": ["while (!s_sf_b)", "return s_sf_a;"],
        "probe": {"channel": "artifact", "symbol": "_Z17spin_signal_fencev",
                  "text": "s_sf_b", "op": "becomes_absent"},
        "note": "删体内零指令屏障",
    }
    nc.update(over)
    return nc


def _meta(ncs, **over) -> dict:
    m = {
        "fixture": "y.cpp",
        "artifact": "y.asm",
        "command": "g++ -std=c++23 -O2 -S y.cpp -o y.asm",
        "actual": {"run_match_keys": ["spin_signal_fence_ret"]},
    }
    if ncs is not None:
        m["negative_controls"] = ncs
    m.update(over)
    return m


@pytest.fixture()
def ncroot(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    """临时锚根 + 阳夹具/阴夹具/阳面 .asm（不碰真实仓库）。"""
    (tmp_path / "y.cpp").write_text(YANG, encoding="utf-8")
    (tmp_path / "y.nc1.cpp").write_text(YIN, encoding="utf-8")
    art = tmp_path / "y.asm"
    art.write_text(_asm(_YANG_BODY), encoding="utf-8")
    monkeypatch.setattr(rp, "ROOT", tmp_path)
    return tmp_path, art


def _stub(monkeypatch: pytest.MonkeyPatch, *, rc: int, body: str | None) -> None:
    """替身编译：把"阴面产物"写到命令行 `-o` 目标；rc/内容由用例决定。"""
    def fake(lines, cwd, env):
        out = re.search(r"-o\s+(\S+)", lines[-1]).group(1)
        if rc == 0 and body is not None:
            Path(out).write_text(_asm(body), encoding="utf-8")
        return [(lines[-1], rc, "boom" if rc else "", "g++")], ""

    monkeypatch.setattr(rp, "run_commands", fake)


def _call(meta: dict, art: Path, tmp_path: Path):
    return rp.check_negative_controls(meta, workdir=tmp_path, env={}, art_path=art)


def test_missing_field_is_noop(ncroot, tmp_path):
    """**字段缺失 = 整段跳过**：verdict 空、日志空（存量 56 卡行为逐字不变）。"""
    _, art = ncroot
    v, log = _call(_meta(None), art, tmp_path)
    assert v == "" and log == []


def test_bad_schema_rejected(ncroot, tmp_path):
    _, art = ncroot
    v, log = _call(_meta([_nc(variant="v2")]), art, tmp_path)
    assert v == "refute:negative_control_bad_schema"
    assert any("variant" in ln for ln in log), log


def test_missing_fixture_rejected(ncroot, tmp_path):
    root, art = ncroot
    (root / "y.nc1.cpp").unlink()
    v, log = _call(_meta([_nc()]), art, tmp_path)
    assert v == "refute:negative_control_missing"
    assert any("阴夹具不存在" in ln for ln in log), log


def test_diff_violation_rejected(ncroot, tmp_path):
    """阴面与阳面零语义差异（只加注释行）⇒ 形态判据拒（不是"翻转"问题）。"""
    root, art = ncroot
    (root / "y.nc1.cpp").write_text(YANG + "// 看起来改了，其实没改\n", encoding="utf-8")
    v, log = _call(_meta([_nc()]), art, tmp_path)
    assert v == "refute:negative_control_diff"
    assert any("零语义" in ln for ln in log), log


def test_command_missing_rejected(ncroot, tmp_path):
    """卡命令里没有产出该工件的编译行（或该行不含阳夹具路径）⇒ 明确拒绝。"""
    _, art = ncroot
    v, log = _call(_meta([_nc()], command="g++ -std=c++23 -O2 -S other.cpp -o y.asm"),
                   art, tmp_path)
    assert v == "refute:negative_control_command_missing"
    assert any("提取不到" in ln for ln in log), log


def test_broken_fixture_is_refute_not_infra(ncroot, tmp_path, monkeypatch):
    """阴面编译 rc≠0（阳面同次 rc=0）⇒ **refute**，绝不能落 infra 当逃生舱。"""
    _, art = ncroot
    _stub(monkeypatch, rc=1, body=None)
    v, log = _call(_meta([_nc()]), art, tmp_path)
    assert v == "refute:negative_control_broken" and not v.startswith("infra")
    assert any("夹具写坏" in ln for ln in log), log


def test_not_flipping_is_refute_passed(ncroot, tmp_path, monkeypatch):
    """阴面能编译能跑、但探针读数与阳面相同 ⇒ `negative_control_passed`（零判别力，核心判决）。"""
    _, art = ncroot
    _stub(monkeypatch, rc=0, body=_YANG_BODY)
    v, log = _call(_meta([_nc()]), art, tmp_path)
    assert v == "refute:negative_control_passed"
    assert any("无判别力" in ln for ln in log), log


def test_flip_verified_logs_reading(ncroot, tmp_path, monkeypatch):
    """真阴面：阳=2 阴=0 ⇒ 通过（verdict 空）且日志给出阳→阴读数（人可核）。"""
    _, art = ncroot
    _stub(monkeypatch, rc=0, body="\tje\t.L2\n.L2:\n\tret\n")
    v, log = _call(_meta([_nc()]), art, tmp_path)
    assert v == "", log
    assert any("flip verified" in ln and "阳=2 阴=0" in ln for ln in log), log


def test_wrong_direction_is_refute(ncroot, tmp_path, monkeypatch):
    """方向与 op 不符（要求 becomes_absent 却变成更多）⇒ 单独归类，便于排障。"""
    _, art = ncroot
    _stub(monkeypatch, rc=0, body=_YANG_BODY + "\tmov\teax, s_sf_b\n")
    v, log = _call(_meta([_nc()]), art, tmp_path)
    assert v == "refute:negative_control_wrong_direction"
    assert any("方向" in ln for ln in log), log


def test_fingerprint_covers_nc_fixture(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """阴夹具字节必须进增量指纹：改了阴面 ⇒ 指纹必须变（否则沿用旧 confirm）；
    阴夹具缺失 ⇒ `MISSING`（强制重跑）。"""
    (tmp_path / "y.cpp").write_text(YANG, encoding="utf-8")
    (tmp_path / "y.nc1.cpp").write_text(YIN, encoding="utf-8")
    card = tmp_path / "EV-X.md"
    meta_lines = [
        "id: EV-X", "fixture: y.cpp", "artifact: y.asm", "artifact_sha256: " + "0" * 64,
        "command: |", "  g++ -O2 -S y.cpp -o y.asm",
        "actual:", "  run_match_keys: [k]",
        "negative_controls:",
        "  - id: nc1",
        "    variant: v1",
        "    mutation: delete_mechanism",
        "    fixture: y.nc1.cpp",
        "    anchor: spin_signal_fence",
        '    remove: "__atomic_signal_fence(__ATOMIC_SEQ_CST);"',
        '    retain: ["while (!s_sf_b)"]',
        "    probe: {channel: artifact, symbol: _Z17spin_signal_fencev, text: s_sf_b, op: becomes_absent}",
    ]
    card.write_text("---\n" + "\n".join(meta_lines) + "\n---\n正文\n", encoding="utf-8")
    (tmp_path / "y.asm").write_text("x\n", encoding="utf-8")
    monkeypatch.setattr(rp, "ROOT", tmp_path)
    fp1 = rp.card_fingerprint(card)
    assert fp1 != "MISSING"
    (tmp_path / "y.nc1.cpp").write_text(YIN + "// 改\n", encoding="utf-8")
    assert rp.card_fingerprint(card) != fp1, "阴夹具被改 ⇒ 指纹必须变"
    (tmp_path / "y.nc1.cpp").unlink()
    assert rp.card_fingerprint(card) == "MISSING", "阴夹具缺失 ⇒ 强制重跑"
