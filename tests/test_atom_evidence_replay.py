"""锁定证据卡复算契约（G3 首项）与三类 refute —— 把"毒样例"固化为回归。

覆盖：
  1. 解析器能读真实卡的全部形态（block scalar / 嵌套映射 / flow 序列 / 尾注释 / 折叠续行）
  2. `refute:missing_field`（缺 artifact / artifact_sha256 / actual.run_*）
  3. `refute:sha256_mismatch` —— 首版验收标准：旧工件 hash 喂进去必须被拦
  4. `refute:run_mismatch` —— 输出与 `run_*` 不逐字一致
  5. `confirm` —— 一致时放行（阴性对照：门禁不能恒红）
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

import pytest

import atom_evidence_replay as rp

REAL_CARD = rp.ROOT / "evidence/mem/EV-MEM-001.md"


def _compiler() -> str:
    """解析本机 g++（与工具同源：prefer 列表 → PATH → 兜底）。"""
    from toolchain import resolve_gpp
    return resolve_gpp()


def _has_compiler() -> bool:
    gpp = _compiler()
    return bool(shutil.which(gpp) or Path(gpp).exists())


needs_gpp = pytest.mark.skipif(not _has_compiler(), reason="本机无 g++")


# ── 1. 解析器契约 ──────────────────────────────────────────────────────────
def test_parse_frontmatter_real_card_shapes():
    """真实卡（EV-MEM-001）的字段全部可解析，形态覆盖卡模板的所有用法。"""
    meta = rp.parse_frontmatter(REAL_CARD.read_text(encoding="utf-8"))
    assert meta["id"] == "EV-MEM-001"
    assert meta["matrix"]["std"] == ["c++23", "c++17"]          # flow 序列 + 尾注释剥离
    assert str(meta["command"]).startswith("g++ -std=c++23")     # block scalar（|）保换行
    assert str(meta["artifact_sha256"]).startswith("d8b6b18d")
    assert str(meta["artifact_compiler"]) == "GCC 15.3.0 (MinGW-w64)"   # 哈希归属声明
    assert meta["artifact_assert"][0]["text"] == "_ZL8g_allocs"        # 源码结构决定，跨编译器稳定
    assert meta["artifact_assert"][1]["texts"][0] == "_Znay"           # 平台差异用 contains_any 吸收
    run_keys = [k for k in meta["actual"] if k.startswith("run")]
    assert len(run_keys) == 6, "6 组矩阵实测"
    assert str(meta["hypothesis"]).startswith("对含堆缓冲的类型")  # 折叠 scalar（>-）


def test_parse_frontmatter_rejects_non_card():
    with pytest.raises(ValueError):
        rp.parse_frontmatter("no frontmatter here\n")


# ── 2. 缺字段 ─────────────────────────────────────────────────────────────
def test_missing_field_refutes(tmp_path: Path):
    card = tmp_path / "EV-T-001.md"
    card.write_text("---\nid: EV-T-001\ncommand: echo hi\n---\n", encoding="utf-8")
    verdict, log = rp.replay_card(card)
    assert verdict == "refute:missing_field"
    assert any("artifact" in ln and "artifact_sha256" in ln for ln in log)


# ── 3~5. 真编译三类结局 ────────────────────────────────────────────────────
def _make_card(tmp_path: Path, *, expect: str, sha: str, extra: str = "") -> Path:
    """造一张自包含卡：fixture 打印 A/B 两行，artifact 为 -S 产物。

    `command` 用**裸 `g++`**——与真实卡（EV-MEM-001）格式一致。2026-09-10 监工抓到的
    "毒样例 3/3 是假阳性"正是因为旧版测试卡写了完整路径 g++，绕过了裸名校验路径。
    `extra` 追加额外 frontmatter 行（用于编译器身份/结构断言的场景）。
    """
    fx = tmp_path / "fx.cpp"
    fx.write_text('#include <cstdio>\nint main(){ std::printf("A\\nB\\n"); }\n',
                  encoding="utf-8")
    exe = tmp_path / "fx.exe"
    asm = tmp_path / "fx.asm"

    def q(p: object) -> str:
        """卡内路径一律正斜杠（M2 command 契约）。"""
        return '"' + str(p).replace("\\", "/") + '"'
    command = (f'g++ -std=c++17 -O2 {q(fx)} -o {q(exe)} && {q(exe)}\n'
               f'g++ -std=c++17 -O2 -S {q(fx)} -o {q(asm)}')
    card = tmp_path / "EV-T-002.md"
    card.write_text(
        "---\n"
        "id: EV-T-002\n"
        "command: |\n"
        + "".join(f"  {ln}\n" for ln in command.split("\n")) +
        f"artifact: {asm.as_posix()}\n"
        f"artifact_sha256: {sha}\n"
        + extra
        + "fixture: " + fx.as_posix() + "\n"
        "actual:\n"
        f'  run_case: "{expect.replace(chr(10), " | ")}"\n'
        "---\n",
        encoding="utf-8")
    return card


@needs_gpp
def test_sha256_mismatch_refutes(tmp_path: Path):
    """毒样例：工件 hash 与卡不符（本次 G2 缺陷的机器化回归）。"""
    card = _make_card(tmp_path, expect="A\nB", sha="0" * 64)
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "refute:sha256_mismatch", log
    assert any("工件与卡不同代" in ln for ln in log)


@needs_gpp
def test_run_mismatch_refutes(tmp_path: Path):
    """毒样例：运行输出与 run_* 不逐字一致（精确比对，非包含）。"""
    card = _make_card(tmp_path, expect="A\nWRONG", sha="0" * 64)
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "refute:run_mismatch", log
    assert any("实际 2 行" in ln for ln in log)


@needs_gpp
def test_confirm_when_artifact_and_output_match(tmp_path: Path):
    """阴性对照：一致的卡必须放行（门禁不得恒红）。"""
    gpp = _compiler()
    fx = tmp_path / "fx.cpp"
    fx.write_text('#include <cstdio>\nint main(){ std::printf("A\\nB\\n"); }\n',
                  encoding="utf-8")
    asm = tmp_path / "fx.asm"
    subprocess.run([gpp, "-std=c++17", "-O2", "-S", fx.as_posix(), "-o", asm.as_posix()],
                   check=True, capture_output=True)
    real = hashlib.sha256(asm.read_bytes()).hexdigest()
    card = _make_card(tmp_path, expect="A\nB", sha=real)
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "confirm", log


# ── 5.5 跨编译器分流（2026-09-10 修 CI 红因的回归锁）────────────────────────
# 背景：sha256 只在同一编译器（含平台）下可复算；实测同一夹具 MinGW GCC 15.3 与 13.1 的
# .asm 字节完全不同，CI（Ubuntu 系统 g++）重生成必然 mismatch。分流后：身份不匹配 →
# 改判 artifact_assert[] 结构断言；**断言缺失或不满足仍 refute**（不是逃生舱）。
def test_check_artifact_assert_kinds(tmp_path: Path):
    """纯函数：三种 kind 的判定，以及未知 kind / 空断言的失败处置。"""
    art = tmp_path / "a.asm"
    art.write_text("main:\n\tcall\tmalloc\n\tcall\tmalloc\n\tcall\tfree\n", encoding="utf-8")
    ok, lines = rp.check_artifact_assert({"artifact_assert": [
        {"kind": "call_count", "symbol": "malloc", "count": 2},
        {"kind": "contains", "text": "call\tfree"},
        {"kind": "absent", "text": "call\tnew"},
    ]}, art)
    assert ok and len(lines) == 3, lines
    # 多符号**求和**（跨平台同一语义）+ contains_any（任一候选）
    ok2, l2 = rp.check_artifact_assert({"artifact_assert": [
        {"kind": "call_count", "symbols": ["malloc", "free"], "count": 3},
        {"kind": "contains_any", "texts": ["nope", "call\tfree"]},
    ]}, art)
    assert ok2 and len(l2) == 2, l2
    assert not rp.check_artifact_assert(
        {"artifact_assert": [{"kind": "contains_any", "texts": ["nope"]}]}, art)[0]
    assert not rp.check_artifact_assert({"artifact_assert": [{"kind": "wat"}]}, art)[0]
    assert not rp.check_artifact_assert({}, art)[0], "缺断言必须判失败"


@needs_gpp
def test_cross_compiler_falls_back_to_artifact_assert(tmp_path: Path):
    """身份不匹配时 sha 不比字节，改判结构断言并通过（CI 实际走的就是这条路）。"""
    card = _make_card(tmp_path, expect="A\nB", sha="0" * 64,
                      extra='artifact_compiler: "GCC 0.0.0 (Mars)"\n'
                            "artifact_assert:\n"
                            '  - {kind: contains, text: "main"}\n')
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "confirm", log
    assert any("改判结构断言" in ln for ln in log)


@needs_gpp
def test_cross_compiler_assert_failure_refutes(tmp_path: Path):
    """断言不满足 → refute：降级是"换一种真校验"，不是放行。"""
    card = _make_card(tmp_path, expect="A\nB", sha="0" * 64,
                      extra='artifact_compiler: "GCC 0.0.0 (Mars)"\n'
                            "artifact_assert:\n"
                            "  - {kind: call_count, symbol: no_such_symbol, count: 1}\n")
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "refute:artifact_assert_failed", log


@needs_gpp
def test_cross_compiler_missing_assert_refutes(tmp_path: Path):
    """身份不匹配但卡没写 artifact_assert → 仍 refute（防"降级"被当逃生舱）。"""
    card = _make_card(tmp_path, expect="A\nB", sha="0" * 64,
                      extra='artifact_compiler: "GCC 0.0.0 (Mars)"\n')
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "refute:artifact_assert_failed", log
    assert any("无可用校验" in ln for ln in log)


@needs_gpp
def test_toolchain_id_shape():
    """编译器身份形如 `GCC 15.3.0 (MinGW-w64)`：比 sha 前必须先能说清"是谁生成的"。"""
    cid = rp._current_toolchain_id()
    assert cid.startswith(("GCC ", "Clang ")), cid
    assert cid.endswith(")"), cid


# ── 6. 不支持的 shell 特性必须诚实报错（不猜） ─────────────────────────────
def test_unsupported_shell_feature_is_reported():
    assert rp._split_argv("g++ a.cpp | tee log") is None
    assert rp._split_argv("g++ a.cpp > out.txt") is None
    assert rp._split_argv('g++ a.cpp -o b.exe && b.exe') is not None


# ── 7. 裸编译器名必须被钉到完整路径（监工缺陷 1 的回归锁） ──────────────────
def test_bare_compiler_name_is_pinned_to_resolved_path():
    """本机 PATH 里的 g++ 是 mingw1310（13.1.0，缺 cc1plus）；裸名必须被替换成
    `resolve_gpp()` 的完整路径，否则编译失败——工具不得依赖调用者 PATH。"""
    from toolchain import resolve_gpp
    argv = rp._pin_compiler(["g++", "-std=c++17", "x.cpp"])
    assert argv[0] != "g++", "裸名必须替换为完整路径"
    assert Path(argv[0]).name.lower() == Path(resolve_gpp()).name.lower()
    assert argv[1:] == ["-std=c++17", "x.cpp"], "其余参数原样保留"
    # 已是完整路径时不重复改写
    pinned = rp._pin_compiler([resolve_gpp(), "x.cpp"])
    assert pinned[0] == resolve_gpp()


def test_missing_executable_does_not_crash(tmp_path: Path):
    """缺陷 2 的回归锁：编译失败后执行不存在的 exe → rc=127 且不抛异常。"""
    fx = tmp_path / "broken.cpp"
    fx.write_text("int main(){ this is not c++ }\n", encoding="utf-8")
    exe = (tmp_path / "nope.exe").as_posix()
    card = tmp_path / "EV-T-003.md"
    card.write_text(
        "---\n"
        "id: EV-T-003\n"
        "command: |\n"
        f'  g++ -std=c++17 {fx.as_posix()} -o "{exe}"\n'
        f'  "{exe}"\n'
        f"artifact: {fx.as_posix()}\n"
        f"artifact_sha256: {'0' * 64}\n"
        "actual:\n"
        '  run_case: "A"\n'
        "---\n", encoding="utf-8")
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "refute:compile_failed", log
    assert any("可执行文件不存在" in ln or "rc=127" in ln for ln in log), log


# ── 8. `&&` 语义：同段前一条失败则短路，不误跑后续 ───────────────────────────
@needs_gpp
def test_and_and_short_circuits_after_failure(tmp_path: Path):
    card = tmp_path / "EV-T-004.md"
    card.write_text(
        "---\n"
        "id: EV-T-004\n"
        "command: |\n"
        f'  g++ -std=c++17 {tmp_path.as_posix()}/nope.cpp -o "{tmp_path.as_posix()}/x.exe" '
        f'&& "{tmp_path.as_posix()}/x.exe"\n'
        f"artifact: {tmp_path.as_posix()}/x.exe\n"
        f"artifact_sha256: {'0' * 64}\n"
        "actual:\n"
        '  run_case: "A"\n'
        "---\n", encoding="utf-8")
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "refute:compile_failed", log
    assert len([ln for ln in log if "rc=" in ln]) == 1, "&& 短路后不应再执行第二段"
