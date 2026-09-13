"""470 P0-A 重编译不变量回归锁（452 E01 根因修复）。

正例=编译后覆写被 refute:artifact_tampered；反例=正常卡 confirm 不退化；
边界=构建脚本卡 fail-closed（infra_error:recompile_unavailable）。
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import atom_evidence_replay as replay  # noqa: E402
from toolchain import resolve_gpp  # noqa: E402


def _mk_sandbox(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    monkeypatch.setattr(replay, "ROOT", tmp_path)
    # Windows 相对路径可执行文件按**父进程 cwd** 解析（非 subprocess cwd 参数）；
    # replay 真实运行时 ROOT == 进程 cwd，沙箱必须同步 chdir 才能复现该语义。
    monkeypatch.chdir(tmp_path)
    (tmp_path / "fx.cpp").write_text(
        '#include <cstdio>\nint main(){ std::printf("result=A\\n"); }\n',
        encoding="utf-8")
    (tmp_path / "fx.out").write_text("result=A\n", encoding="utf-8")
    return Path(resolve_gpp()).as_posix()


def _run_line(gpp: str) -> str:
    # 必须走 build/ 子目录：纯 `./name.exe` 会被 argv 拆分剥成 `name.exe`，
    # Windows CreateProcess 不搜 cwd → 127（真实卡约定即产物写 build/）
    return f'"{gpp}" -std=c++17 fx.cpp -o build/fx.exe && ./build/fx.exe'


def _asm_line(gpp: str) -> str:
    return f'"{gpp}" -std=c++17 -S fx.cpp -o fx.asm'


def _card(tmp_path: Path, name: str, command: str, sha: str) -> Path:
    fields = {
        "id": "EV-T-RC", "serves": "[]", "hypothesis": "h", "kind": "asm",
        "command": command, "fixture": "fx.cpp", "artifact": "fx.asm",
        "artifact_sha256": sha, "verdict": "confirm", "falsification": "f",
        "expected": "result=A",
        "actual": "\n  run_match_file: fx.out\n  run_match_keys: [result]",
    }
    body = ""
    for k, v in fields.items():
        if k == "command":                      # 多行命令必须 block scalar（`|`）
            body += "command: |\n" + "".join("  " + ln + "\n" for ln in str(v).split("\n"))
        elif str(v).startswith("\n"):
            body += f"{k}:\n{v}\n"
        else:
            body += f"{k}: {v}\n"
    p = tmp_path / name
    p.write_text("---\n" + body + "---\n", encoding="utf-8")
    return p


def test_post_write_tamper_refuted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """E01 正例：编译后 helper 覆写 → got_sha==卡值 但独立重编译不一致 → refute。"""
    gpp = _mk_sandbox(tmp_path, monkeypatch)
    forged = b"\tret\n"
    (tmp_path / "_ow.py").write_text(
        "from pathlib import Path\n"
        f"Path(r'{(tmp_path / 'fx.asm').as_posix()}').write_bytes({forged!r})\n",
        encoding="utf-8")
    sha = hashlib.sha256(forged).hexdigest()
    card = _card(tmp_path, "tamper.md",
                 f"{_run_line(gpp)}\n{_asm_line(gpp)}\npython _ow.py", sha)
    verdict, log = replay.replay_card(card, do_sanitizer=False)
    assert verdict == "refute:artifact_tampered", \
        f"应 refute:artifact_tampered，实际 {verdict}\n" + "\n".join(log)


def test_normal_card_confirm(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """反例（阴性对照）：正常编译卡重编译 sha 一致 → confirm 不退化。"""
    gpp = _mk_sandbox(tmp_path, monkeypatch)
    subprocess.run(_asm_line(gpp), shell=True, cwd=str(tmp_path), check=True,
                   capture_output=True)
    sha = hashlib.sha256((tmp_path / "fx.asm").read_bytes()).hexdigest()
    card = _card(tmp_path, "clean.md", f"{_run_line(gpp)}\n{_asm_line(gpp)}", sha)
    verdict, log = replay.replay_card(card, do_sanitizer=False)
    assert verdict == "confirm", \
        f"正常卡不得退化，实际 {verdict}\n" + "\n".join(log)


def test_build_script_card_fail_closed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """边界：产出 artifact 的命令不是直接编译行（脚本）→ fail-closed 不静默放行。"""
    gpp = _mk_sandbox(tmp_path, monkeypatch)
    (tmp_path / "gen.py").write_text(
        "from pathlib import Path\n"
        f"Path(r'{(tmp_path / 'fx.asm').as_posix()}').write_bytes(b'\\tret\\n')\n",
        encoding="utf-8")
    sha = hashlib.sha256(b"\tret\n").hexdigest()
    # 命令文本含 fx.asm（过前置 missing_artifact_command 检查）但不是直接编译行
    card = _card(tmp_path, "script.md", f"{_run_line(gpp)}\npython gen.py fx.asm", sha)
    verdict, _log = replay.replay_card(card, do_sanitizer=False)
    assert verdict == "infra_error:recompile_unavailable", f"实际 {verdict}"


def test_compile_line_extraction_picks_artifact_producer():
    """提取必须选中产出 artifact 的行（不能取最后一条编译行；token 级编译器判定）。"""
    cmd = ("g++ -S -masm=intel a.cpp -o a.asm\n"
           "g++ a.cpp -o a.exe && ./a.exe\n"
           "g++ -S -O2 b.cpp -o b.asm")
    lines = replay._artifact_compile_lines(cmd, "a.asm")
    assert len(lines) == 1 and "-masm=intel" in lines[0]
    assert replay._artifact_compile_lines(cmd, "b.asm") == [cmd.split("\n")[2]]
    assert replay._artifact_compile_lines("python build.py -o x.asm", "x.asm") == []
    # 交叉编译器前缀也须识别（x86_64-w64-mingw32-g++）
    assert replay._artifact_compile_lines(
        "x86_64-w64-mingw32-g++ -S x.cpp -o x.asm", "x.asm") != []
