"""413 Writer 自检层回归锁：7 项检查 + 存量 0 fail 基线 + 第五批 E1/E2 回放拦截。"""
from __future__ import annotations

import hashlib
import os
import time
from pathlib import Path

import pytest

import gate_engine as ge
import writer_selfcheck as ws


def _card(tmp: Path, name: str, **over: str) -> Path:
    fields = {
        "id": "EV-MEM-TEST", "serves": "[]", "hypothesis": "h", "kind": "run",
        "command": "g++ -S fx.cpp -o fx.asm", "fixture": "fx.cpp",
        "artifact": "fx.asm", "verdict": "confirm", "falsification": "f",
    }
    fields.update(over)
    body = "".join(
        (f"{k}:\n{v}\n" if str(v).startswith("\n") else f"{k}: {v}\n")
        for k, v in fields.items())
    p = tmp / name
    p.write_text("---\n" + body + "---\n", encoding="utf-8")
    return p


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(ge, "ROOT", tmp_path)
    (tmp_path / "fx.cpp").write_text("int main(){return 0;}\n", encoding="utf-8")
    (tmp_path / "fx.asm").write_text("\tmovl $1, %eax\n\tret\n", encoding="utf-8")
    return tmp_path


def _by_id(checks: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {c["id"]: c for c in checks}


def test_wc01_pass_and_fail(sb: Path):
    sha = hashlib.sha256((sb / "fx.asm").read_bytes()).hexdigest()
    ok = _by_id(ws.check_card(_card(sb, "a.md", artifact_sha256=sha)))
    assert ok["WC-01"]["status"] == "pass"
    bad = _by_id(ws.check_card(_card(sb, "b.md", artifact_sha256="0" * 64)))
    assert bad["WC-01"]["status"] == "fail", "卡面 sha 与磁盘工件不一致必须 fail"


def test_wc01_cross_compiler_skip(sb: Path):
    """跨编译器工件（matrix 多编译器）字节必然不同——与 replay 同口径跳过。"""
    c = _by_id(ws.check_card(_card(sb, "c.md", artifact_sha256="0" * 64,
                                   artifact_compiler="GCC 13.3.0 (WSL)")))
    assert c["WC-01"]["status"] == "skip"


def test_wc02_missing_label_warn(sb: Path):
    """contains 标签不在工件中 → 检出（warn：拼写差异与伪造结构不可区分）。"""
    c = _by_id(ws.check_card(
        _card(sb, "d.md", kind="asm",
              artifact_assert="\n  - {kind: contains, text: _Znever_exists_xyz}")))
    assert c["WC-02"]["status"] == "warn" and "_Znever_exists_xyz" in c["WC-02"]["message"]


def test_wc02_absent_claim_not_checked(sb: Path):
    """absent 的主张就是「不存在」——文本缺席不得算检出。"""
    c = _by_id(ws.check_card(
        _card(sb, "e.md", kind="asm",
              artifact_assert="\n  - {kind: absent, text: _Znever_exists_xyz}")))
    assert c["WC-02"]["status"] == "pass"


def test_wc03_msvc_skip_and_missing_fixture(sb: Path):
    c = _by_id(ws.check_card(_card(sb, "f.md", command="cl /c fx.cpp")))
    assert c["WC-03"]["status"] == "skip", "MSVC 永久边界 → skip"
    c = _by_id(ws.check_card(_card(sb, "g.md", fixture="nope.cpp")))
    assert c["WC-03"]["status"] == "fail", "fixture 路径不存在必须 fail"


def test_wc04_out_same_generation(sb: Path):
    (sb / "fx.out").write_text("x=1\n", encoding="utf-8")
    c = _by_id(ws.check_card(
        _card(sb, "h.md", actual="\n  run_match_file: fx.out\n  run_match_keys: []")))
    assert c["WC-04"]["status"] == "pass"
    past = time.time() - 600
    os.utime(sb / "fx.out", (past, past))
    c = _by_id(ws.check_card(
        _card(sb, "i.md", actual="\n  run_match_file: fx.out\n  run_match_keys: []")))
    assert c["WC-04"]["status"] == "warn", ".out 早于夹具须检出"
    c = _by_id(ws.check_card(
        _card(sb, "j.md", actual="\n  run_match_file: gone.out\n  run_match_keys: []")))
    assert c["WC-04"]["status"] == "fail", "声明的 .out 不存在必须 fail"


def test_wc05_live_control(sb: Path):
    c = _by_id(ws.check_card(
        _card(sb, "k.md", kind="asm", actual="\n  note: 仅工件文本无运行读数")))
    assert c["WC-05"]["status"] == "warn", "asm 卡无运行时读数须 warn"
    c = _by_id(ws.check_card(
        _card(sb, "k2.md", kind="asm", actual="\n  run_case: none")))
    assert c["WC-05"]["status"] == "pass", "run_case 是运行时读数"
    c = _by_id(ws.check_card(
        _card(sb, "l.md", actual="\n  run_match_file: fx.out\n  run_match_keys: []")))
    assert c["WC-05"]["status"] == "pass"


def test_wc07_unbounded_loop(sb: Path):
    (sb / "spin_bad.cpp").write_text(
        "int main(){ while(1){ int x = 1; } }\n", encoding="utf-8")
    (sb / "spin_ok.cpp").write_text(
        "int main(){ while(1){ if (x > 1000) break; } }\n", encoding="utf-8")
    c = _by_id(ws.check_card(_card(sb, "m.md", fixture="spin_bad.cpp")))
    assert c["WC-07"]["status"] == "fail", "无界循环无退出必须 fail"
    c = _by_id(ws.check_card(_card(sb, "n.md", fixture="spin_ok.cpp")))
    assert c["WC-07"]["status"] == "pass", "有 break 的循环放行"


def test_stock_zero_false_positive(replay_serial):
    """存量 56 卡 0 fail（warn/skip 允许）——420 铁律。

    559 B：本用例是**唯一**直接读真实仓库工件的 WC 用例（其余走 `sb` 沙箱），
    故与 replay 同锁串行——否则并发 replay 的"删→重生成→还原"窗口里，
    WC-01「磁盘 sha == 卡值」会假红（558 `-n auto` 误跑法实测）。
    """
    n_fail = 0
    for p in ge._cards(ge.EVIDENCE, "EV-*.md"):
        n_fail += sum(1 for c in ws.check_card(p) if c["status"] == "fail")
    assert n_fail == 0, f"存量卡出现 {n_fail} 个 fail（误伤或真债，需逐条裁决）"


def test_fifth_batch_e1_e2_caught(sb: Path):
    """第五批 E1/E2 回放：E1 工件不同代 / E2 断言未实测 / E1 .out 陈旧——拦截率 ≥80%。

    拦住 = 该项检查 status != pass（机械错误被自检层看见）。
    """
    cases: list[tuple[str, dict[str, str]]] = [
        ("E1 工件不同代（sha 旧）", dict(artifact_sha256="0" * 64)),
        ("E2 断言标签未实测", dict(kind="asm",
                               artifact_assert="\n  - {kind: contains, text: _Zunmeasured_sym}")),
        ("E1 .out 陈旧", dict(actual="\n  run_match_file: stale.out\n  run_match_keys: []")),
    ]
    (sb / "stale.out").write_text("x=1\n", encoding="utf-8")
    past = time.time() - 600
    os.utime(sb / "stale.out", (past, past))
    caught = 0
    for i, (name, over) in enumerate(cases):
        checks = _by_id(ws.check_card(_card(sb, f"e{i}.md", **over)))
        hit = any(c["status"] != "pass" for c in checks.values())
        caught += hit
        assert hit, f"{name} 未被任何检查拦住"
    assert caught / len(cases) >= 0.8, "E1/E2 拦截率不足 80%"
