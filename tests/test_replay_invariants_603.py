"""603 任务3.1：replay 不变量回归锁（把 replay 的**隐含契约**显性化为可证属性）。

不变量清单（引自 603 任务书 §任务3）与本文件的对应：
  I1 仓库一致性 : `replay_card` 结束后 artifact 字节 == 运行前字节（校验工具不改写被校验对象）。
  I2 判定一致性 : replay 判决族与卡的声明一致（confirm 卡→`confirm`；错 sha 卡→`refute:*`）。
  I3 还原幂等   : `_restore_artifact` 幂等（工件有效时不动；缺失/空才重建；重复调用无漂移）。
  I4 错误处理   : 环境故障走 `infra_error`（compiler_missing / msvc_unavailable），**绝不退化成 refute**；
                  内容缺失仍走 `refute`（判别力保留，环境故障不成为"删卡即放行"的逃生舱）。
  I5 并发隔离   : 由 `tests/test_replay_lock_serial.py` 覆盖（锁语义/串行契约）；本批不复测，避免重复。

纪律：全部在沙箱内运行——`monkeypatch replay.ROOT = tmp_path` + `chdir`（复现"ROOT==进程 cwd"语义），
      不触碰真实仓库；合成卡范式的构造与 `tests/test_recompile_invariant.py` 对齐。
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import atom_evidence_replay as replay  # noqa: E402
import toolchain  # noqa: E402
from toolchain import resolve_gpp  # noqa: E402

# 运行前的"哨兵"字节：与命令重生成的工件**逐字节不同**，
# 用于区分"真·还原成运行前字节"与"恰好重生成出同样字节"。
_SENTINEL = b"SENTINEL-PRE-RUN-BYTES-603\n"


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
    # 产物写 build/（Windows CreateProcess 不搜 cwd；真实卡约定即产物写 build/）
    return f'"{gpp}" -std=c++17 fx.cpp -o build/fx.exe && ./build/fx.exe'


def _asm_line(gpp: str) -> str:
    return f'"{gpp}" -std=c++17 -S fx.cpp -o fx.asm'


def _card(tmp_path: Path, name: str, command: str, sha: str, *,
          artifact: str = "fx.asm", verdict: str = "confirm",
          with_sha_field: bool = True) -> Path:
    fields: dict[str, str] = {
        "id": "EV-T-INV", "serves": "[]", "hypothesis": "h", "kind": "asm",
        "command": command, "fixture": "fx.cpp", "artifact": artifact,
        "verdict": verdict, "falsification": "f", "expected": "result=A",
        "actual": "\n  run_match_file: fx.out\n  run_match_keys: [result]",
    }
    if with_sha_field:
        fields["artifact_sha256"] = sha
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


def _compile_asm(gpp: str, tmp_path: Path) -> str:
    subprocess.run(_asm_line(gpp), shell=True, cwd=str(tmp_path), check=True,
                   capture_output=True)
    return hashlib.sha256((tmp_path / "fx.asm").read_bytes()).hexdigest()


# ── I1 + I2（confirm 侧）：判决=confirm，且运行后仓库工件回到运行前字节 ──────────────
def test_repo_consistency_and_verdict_confirm(tmp_path: Path,
                                              monkeypatch: pytest.MonkeyPatch):
    gpp = _mk_sandbox(tmp_path, monkeypatch)
    real_sha = _compile_asm(gpp, tmp_path)
    # 用哨兵覆盖工件：命令重生成的是"真实 asm"（sha==real_sha），与哨兵必然不同。
    (tmp_path / "fx.asm").write_bytes(_SENTINEL)
    card = _card(tmp_path, "clean.md", f"{_run_line(gpp)}\n{_asm_line(gpp)}", real_sha)

    verdict, log = replay.replay_card(card, do_sanitizer=False)

    assert verdict == "confirm", f"应 confirm，实际 {verdict}\n" + "\n".join(log)
    # I1：即便校验中途删旧/重生成，工具最终必须把工件**逐字节**还原成运行前（哨兵）。
    assert (tmp_path / "fx.asm").read_bytes() == _SENTINEL, "校验工具改写了被校验对象"


# ── I1（refute 侧）+ I2（refute 侧）：错 sha 卡判决=refute，且工件仍被还原 ────────────
def test_repo_consistency_and_verdict_refute(tmp_path: Path,
                                             monkeypatch: pytest.MonkeyPatch):
    gpp = _mk_sandbox(tmp_path, monkeypatch)
    _compile_asm(gpp, tmp_path)
    (tmp_path / "fx.asm").write_bytes(_SENTINEL)
    wrong = "0" * 64
    card = _card(tmp_path, "wrong.md", f"{_run_line(gpp)}\n{_asm_line(gpp)}", wrong,
                 verdict="refute")

    verdict, log = replay.replay_card(card, do_sanitizer=False)

    assert verdict.startswith("refute"), f"应 refute:*，实际 {verdict}\n" + "\n".join(log)
    assert verdict == "refute:sha256_mismatch", f"应为 sha 失配，实际 {verdict}"
    assert (tmp_path / "fx.asm").read_bytes() == _SENTINEL, "refute 路径也必须还原工件"


# ── I3：`_restore_artifact` 幂等（工件有效→不动；缺失/空→重建；重复调用无漂移）────────
def test_restore_artifact_idempotent(tmp_path: Path):
    art = tmp_path / "a.bin"
    bak = tmp_path / "a.bin.bak"
    art.write_bytes(b"GOOD-CURRENT")
    bak.write_bytes(b"BACKUP-OLD")

    # ① 工件有效（非空）→ 不动：返回 False，内容保持
    assert replay._restore_artifact(art, bak) is False
    assert art.read_bytes() == b"GOOD-CURRENT"

    # ② 工件为空（模拟重生成被中断/清空）→ 从备份重建
    art.write_bytes(b"")
    assert replay._restore_artifact(art, bak) is True
    assert art.read_bytes() == b"BACKUP-OLD"

    # ③ 再次调用 → 已是有效工件，再不动（幂等，无漂移）
    assert replay._restore_artifact(art, bak) is False
    assert art.read_bytes() == b"BACKUP-OLD"


# ── I4a：编译器缺失 → infra_error:compiler_missing，不是 refute，也不碰工件 ──────────
def test_infra_error_compiler_missing_not_refute(tmp_path: Path,
                                                 monkeypatch: pytest.MonkeyPatch):
    gpp = _mk_sandbox(tmp_path, monkeypatch)
    real_sha = _compile_asm(gpp, tmp_path)
    before = (tmp_path / "fx.asm").read_bytes()
    card = _card(tmp_path, "nocc.md", f"{_run_line(gpp)}\n{_asm_line(gpp)}", real_sha)

    monkeypatch.setattr(toolchain, "resolve_gpp",
                        lambda: str(tmp_path / "no_such_gpp.exe"))
    verdict, log = replay.replay_card(card, do_sanitizer=False)

    assert verdict == "infra_error:compiler_missing", \
        f"环境故障须 infra_error，实际 {verdict}\n" + "\n".join(log)
    assert not verdict.startswith("refute"), "环境故障被误判成内容证伪"
    assert (tmp_path / "fx.asm").read_bytes() == before, "未进入校验流程，不应改动工件"


# ── I4b：MSVC(cl) 卡是永久边界 → infra_error:msvc_unavailable，不尝试编译、不误判 ──────
def test_infra_error_msvc_not_refute(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _mk_sandbox(tmp_path, monkeypatch)
    card = _card(tmp_path, "msvc.md", "cl /c fx.cpp /Fo build/fx.obj", "0" * 64,
                 artifact="fx.obj")

    verdict, log = replay.replay_card(card, do_sanitizer=False)

    assert verdict == "infra_error:msvc_unavailable", \
        f"MSVC 边界须 infra_error，实际 {verdict}\n" + "\n".join(log)


# ── I4c：内容缺失仍是 refute（判别力保留：环境故障 ≠ 内容证伪）────────────────────
def test_missing_field_still_refute(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    _mk_sandbox(tmp_path, monkeypatch)
    card = _card(tmp_path, "nofield.md", "g++ -S fx.cpp -o fx.asm", "",
                 with_sha_field=False)          # 缺 artifact_sha256

    verdict, log = replay.replay_card(card, do_sanitizer=False)

    assert verdict == "refute:missing_field", \
        f"内容缺失须 refute，实际 {verdict}\n" + "\n".join(log)
