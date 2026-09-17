"""tool_integrity 回归锁（498 任务 3）。

四态：全匹配 exit 0 / 被改 exit 1 / 缺基准 exit 2 / 工具缺失 exit 1。
全部走 tmp_path（不触碰真实 tools/ 与 .tool_checksums）。
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import tool_integrity as ti

NAMES = ("a_tool.py", "b_tool.py")
ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def _run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, *args], cwd=str(ROOT), capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def _mk(tmp: Path, *, content: dict[str, str] | None = None) -> Path:
    tools = tmp / "tools"
    tools.mkdir(exist_ok=True)
    for n in NAMES:
        (tools / n).write_text((content or {}).get(n, f"# {n}\n"), encoding="utf-8")
    return tools


def test_update_then_verify_ok(tmp_path: Path):
    tools = _mk(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=tools, names=NAMES)
    assert cs.is_file()
    changed, missing, code = ti.verify(path=cs, tools_dir=tools)
    assert (changed, missing, code) == ([], [], 0)


def test_tamper_detected(tmp_path: Path):
    tools = _mk(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=tools, names=NAMES)
    (tools / "a_tool.py").write_text("# 被篡改\n", encoding="utf-8")
    changed, missing, code = ti.verify(path=cs, tools_dir=tools)
    assert code == 1 and len(changed) == 1
    name, want, got = changed[0]
    assert name == "a_tool.py" and want != got


def test_missing_baseline_exit2(tmp_path: Path):
    tools = _mk(tmp_path)
    _, _, code = ti.verify(path=tmp_path / "nope.txt", tools_dir=tools)
    assert code == 2, "缺基准必须 exit 2（不得静默放行）"


def test_missing_tool_detected(tmp_path: Path):
    tools = _mk(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=tools, names=NAMES)
    (tools / "b_tool.py").unlink()
    changed, missing, code = ti.verify(path=cs, tools_dir=tools)
    assert code == 1 and missing == ["b_tool.py"]


# ── 567：完整性自检强制化（--check / 入口拦截 / fail-closed）────────────────────
# 病（564 PoC#1/#2 实锤）：以前只有 `--update`（钉完无法独立复核），且 gate_engine 源码里
# grep 不到任何 integrity 调用 ⇒ 改这五个核心文件的任何字节，门禁**仍全绿**。
# 本组用例锁三件事：① `--check` 能独立复核；② 三个判定入口在篡改态**拒绝运行**；
# ③ 校验自身异常/缺基准时 **fail-closed**（绝不把"没查成"伪装成"查过且通过"）。
# 纪律：篡改只发生在**临时副本 / 临时基准**上，正式 tools/ 全程只读（末尾有绿锁复核）。


def test_567_check_flag_on_real_repo():
    """显式 `--check` 入口存在，且真实仓库基线必绿（独立复核路径，不依赖 pytest monkeypatch）。"""
    r = _run([str(TOOLS / "tool_integrity.py"), "--check"])
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK" in r.stdout, r.stdout


def test_567_check_lists_tampered_file_with_prefixes(tmp_path: Path, monkeypatch, capsys):
    """篡改一个无关字节 ⇒ --check 必红（exit 1）并列出该文件；只打 12 位前缀（不刷全量哈希）。"""
    tools = _mk(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=tools, names=NAMES)
    monkeypatch.setattr(ti, "TOOLS", tools)
    monkeypatch.setattr(ti, "CHECKSUMS", cs)
    assert ti.main(["--check"]) == 0
    (tools / "a_tool.py").write_text("# 篡改：一个无关字节\n", encoding="utf-8")
    assert ti.main(["--check"]) == 1
    out = capsys.readouterr().out
    assert "a_tool.py" in out and "被改动" in out, out
    assert "…" in out, "按提示词只打前缀"
    assert not [w for w in out.split() if len(w) == 64], "不该刷全量哈希"


def test_567_entries_refuse_when_core_tampered(tmp_path: Path, monkeypatch, capsys):
    """入口拦截：核心被改动且未重钉 ⇒ gate/replay 的 `main()` **在任何参数解析之前** exit 1。

    用空 argv 调用：空 argv 下若没被拦，gate 会走自己的 usage 分支（也可能 exit 1）⇒
    故这里**必须**同时验拒绝文案与"期望/实际前缀"，否则测不出真拦截。
    """
    import atom_evidence_replay as replay
    import gate_engine as ge

    cs = tmp_path / ".tool_checksums"
    cs.write_text("0" * 64 + "  gate_engine.py\n", encoding="utf-8")
    monkeypatch.setattr(ti, "CHECKSUMS", cs)
    for mod, name in ((ge, "gate_engine.py"), (replay, "atom_evidence_replay.py")):
        with pytest.raises(SystemExit) as ei:
            mod.main([])
        assert ei.value.code == 1, (name, ei.value.code)
    err = capsys.readouterr().err
    assert "判定核心被改动且未重钉，拒绝运行" in err, err
    assert "gate_engine.py" in err and "000000000000" in err, err
    assert "tool_integrity.py --update" in err, "必须给出重钉修法"


def test_567_poison_entry_refuses_in_tampered_copy(tmp_path: Path):
    """poison 的入口在 `__main__` 块（无 `main()`）⇒ 用**整目录副本**验真入口拦截。

    副本里给 gate_engine.py 追加一个无关字节 ⇒ 三条 CLI 入口全部拒绝（同一道闸），
    且副本的 `--check` 同步红。**全程只动副本**，正式 tools/ 不受影响。
    """
    dst = tmp_path / "tools"
    shutil.copytree(TOOLS, dst)
    g = dst / "gate_engine.py"
    g.write_text(g.read_text(encoding="utf-8") + "\n# 567 篡改：一个无关字节\n", encoding="utf-8")
    r = _run([str(dst / "poison_drill.py"), "--json"])
    assert r.returncode == 1, (r.returncode, r.stdout[-400:], r.stderr[-400:])
    assert "拒绝运行" in r.stderr and "gate_engine.py" in r.stderr, r.stderr
    r2 = _run([str(dst / "gate_engine.py"), "--check"])
    assert r2.returncode == 1 and "拒绝运行" in r2.stderr, (r2.returncode, r2.stderr[-400:])
    r3 = _run([str(dst / "tool_integrity.py"), "--check"])
    assert r3.returncode == 1 and "gate_engine.py" in r3.stdout, (r3.returncode, r3.stdout)


def test_567_fail_closed_on_missing_baseline(tmp_path: Path, monkeypatch, capsys):
    """缺基准（exit 2）⇒ fail-closed 拒绝运行；绝不"没查成"就放行。"""
    monkeypatch.setattr(ti, "CHECKSUMS", tmp_path / "nope.txt")
    with pytest.raises(SystemExit) as ei:
        ti.enforce("dummy.py")
    assert ei.value.code == 1
    err = capsys.readouterr().err
    assert "缺基准" in err and "一律拒绝" in err, err


def test_567_enforce_is_silent_when_green(capsys):
    """通过时**静默**返回——免得污染各入口的 stdout 契约（`--json` 等）。"""
    for name in ti.CORE_TOOLS:
        ti.enforce(name)
    got = capsys.readouterr()
    assert got.out == "" and got.err == ""


def test_567_real_repo_left_clean():
    """"还原后全绿"：所有篡改都在临时副本/临时基准上 ⇒ 正式 tools/ 与基准仍一致。"""
    assert ti.verify() == ([], [], 0)


def test_baseline_format_and_self_exclusion(tmp_path: Path):
    """基准格式 `<sha256>  <name>`；且 .tool_checksums 自己不在清单里（递归无解）。"""
    tools = _mk(tmp_path)
    cs = tmp_path / ".tool_checksums"
    ti.write_baseline(path=cs, tools_dir=tools, names=NAMES)
    lines = cs.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == len(NAMES)
    for ln in lines:
        h, _, n = ln.partition("  ")
        assert len(h) == 64 and n in NAMES
        assert n != ".tool_checksums"
