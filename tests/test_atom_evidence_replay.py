"""锁定证据卡复算契约（G3 首项）与各类 refute / infra_error —— 把"毒样例"固化为回归。

覆盖：
 1. 解析器能读真实卡的全部形态（block scalar / 嵌套映射 / flow 序列 / 尾注释 / 折叠续行）
 2. `refute:missing_field`（缺 artifact / artifact_sha256 / actual.run_*）
 3. `refute:sha256_mismatch` —— 首版验收标准：旧工件 hash 喂进去必须被拦
 4. `refute:run_mismatch` —— 输出与 `run_*` 不逐字一致
 5. `confirm` —— 一致时放行（阴性对照：门禁不能恒红）
 6. `infra_error:compiler_missing` —— 环境故障与内容证伪分流（G6 §4.1 放权前必修）
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


def test_check_artifact_assert_symbol_scope(tmp_path: Path):
    """区间断言：`contains_in`/`absent_in` 只看 `symbol` 的函数体（ATOM-CONC-001 需求）。

    动机：全局 `absent` 无法表达"**某个函数体内**没有 X"——同一 TU 里其它函数（置位用的
    setter、同组对照函数）会提到同一个符号，全局计数必然被污染；用"枚举寄存器拼写"顶替
    会引入**静默漏判**（编译器换了寄存器拼写即自动通过）。故按函数区间判定，符号缺失
    一律判失败（不静默通过）。
    """
    art = tmp_path / "b.asm"
    art.write_text(
        ".globl\t_Z3foov\n"
        "_Z3foov:\n"
        ".LFB0:\n"
        "\tmov\teax, DWORD PTR g_x[rip]\n"
        "\tret\n"
        "\t.seh_endproc\n"
        "\t.p2align 4\n"
        ".globl\t_Z3barv\n"
        "_Z3barv:\n"
        ".LFB1:\n"
        "\tmov\teax, DWORD PTR g_y[rip]\n"
        "\tret\n"
        "\t.seh_endproc\n",
        encoding="utf-8")
    ok, lines = rp.check_artifact_assert({"artifact_assert": [
        {"kind": "contains_in", "symbol": "_Z3foov", "text": "g_x[rip]"},
        {"kind": "absent_in", "symbol": "_Z3barv", "text": "g_x"},
        {"kind": "absent_in", "symbol": "_Z3foov", "text": "g_y"},
    ]}, art)
    assert ok and len(lines) == 3, lines
    # 区间不能退化成全局：本函数内出现的符号，absent_in 必须失败
    assert not rp.check_artifact_assert(
        {"artifact_assert": [{"kind": "absent_in", "symbol": "_Z3foov", "text": "g_x"}]}, art)[0]
    # 区间不能越界到下一个函数：g_y 属于 bar，在 foo 区间内必须判 absent
    assert not rp.check_artifact_assert(
        {"artifact_assert": [{"kind": "contains_in", "symbol": "_Z3foov", "text": "g_y"}]}, art)[0]
    # 符号不存在 → 判失败（不静默通过）
    ok3, l3 = rp.check_artifact_assert(
        {"artifact_assert": [{"kind": "absent_in", "symbol": "_Z9missingv", "text": "g_x"}]}, art)
    assert not ok3 and "找不到符号区间" in l3[0], l3


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
def test_artifact_restored_after_replay():
    """校验不应改写被校验对象：跑完 replay 后仓库工件字节必须与跑前一致。

    背景（2026-09-10 实测踩坑）：复算流程是「删旧工件 → 重生成 → 比 sha256」，在**异构环境**
    下（在 WSL/Linux 跑、而卡归属 MinGW）会把仓库工件静默改写成 Linux 产物（汇编里出现
    `endbr64` / `__printf_chk@PLT`），而卡里的 sha256 仍是 MinGW 的 → 仓库工件与卡不同代。
    校验工具是只读角色，跑完必须还原。这个测试就是那次事故的回归锁。
    """
    art = rp.ROOT / "Examples/atoms/_atom_move_alloc.asm"
    before = art.read_bytes()
    rp.replay_card(REAL_CARD, do_sanitizer=False)
    assert art.read_bytes() == before, "复算改写了仓库工件（异构环境会静默污染）"


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
    """缺陷 2 的回归锁：编译失败后执行不存在的 exe → rc=127 且不抛异常。

    分流口径（G6 §4.1）：g++ **跑起来了**才拒绝源码 ⇒ 内容层 `refute:compile_error`；
    紧随其后的 rc=127（exe 不存在）是它的级联，不得把整卡改判成环境故障。
    """
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
    assert verdict == "refute:compile_error", log
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
    assert verdict == "refute:compile_error", log
    assert len([ln for ln in log if "rc=" in ln]) == 1, "&& 短路后不应再执行第二段"


# ── 8b. 三分类分流（G6 §4.1 放权前必修）：环境故障 ≠ 内容证伪 ────────────────
def test_command_failure_classification_is_pure():
    """分流是纯函数：只吃"哪个程序 / 退出码"，不解析编译器 stderr（文本随版本漂移）。"""
    # 编译器**没启动起来**（rc=127 + 编译器名）⇒ 环境层，须 fail-closed 但仍分列计数
    assert rp.classify_command_failure(
        [("g++ x.cpp", 127, "可执行文件不存在或不可执行：C:/x/g++.exe", "C:/x/g++.exe")]
    ) == "infra_error:compiler_missing"
    # 编译器跑起来了但拒绝源码（rc=1）⇒ 内容层
    assert rp.classify_command_failure(
        [("g++ x.cpp", 1, "error: expected ';'", "C:/x/g++.exe")]
    ) == "refute:compile_error"
    # 卡的命令写法不支持（管道等，工具不猜）⇒ 内容层
    assert rp.classify_command_failure(
        [("g++ x.cpp | tee l", 127, "含不支持的 shell 特性", "")]
    ) == "refute:unsupported_shell"
    # 超时被杀 ⇒ 环境层（无法区分"环境慢"与"代码死循环"，取环境侧，仍 exit 1）
    assert rp.classify_command_failure(
        [("g++ x.cpp", 124, "命令超时（600s）：g++", "g++")]
    ) == "infra_error:compile_timeout"
    # 全部成功 ⇒ confirm；只有**首个**失败参与判定（后续是级联）
    assert rp.classify_command_failure([("g++ x.cpp", 0, "", "g++")]) == "confirm"
    assert rp.classify_command_failure(
        [("g++ x.cpp", 1, "error", "g++"), ('"x.exe"', 127, "不存在", "x.exe")]
    ) == "refute:compile_error"


@needs_gpp
def test_compiler_missing_is_infra_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """工具链找不到 ⇒ `infra_error:compiler_missing`（不是 refute，也不是静默放行）。

    回归锁的意义：夹具/工具链缺失曾一次性把 48 张卡判成"内容被证伪"（G6 §4.1 实例）。
    同时锁住**不得恒红**：同一张卡在编译器可用时必须是别的判决（见上面的 refute/confirm 用例）。
    """
    import toolchain

    monkeypatch.setattr(toolchain, "resolve_gpp", lambda *a, **k: str(tmp_path / "no_such_g++.exe"))
    fx = tmp_path / "ok.cpp"
    fx.write_text("int main(){return 0;}\n", encoding="utf-8")
    card = tmp_path / "EV-T-005.md"
    card.write_text(
        "---\n"
        "id: EV-T-005\n"
        "command: |\n"
        f"  g++ -std=c++17 -S {fx.as_posix()} -o {fx.as_posix()}.s\n"
        f"artifact: {fx.as_posix()}.s\n"
        f"artifact_sha256: {'0' * 64}\n"
        "actual:\n"
        '  run_case: "A"\n'
        "---\n", encoding="utf-8")
    verdict, log = rp.replay_card(card, do_sanitizer=False)
    assert verdict == "infra_error:compiler_missing", log
    assert any("编译器不可用" in ln for ln in log), log


# ── 9. sanitizer 预期内豁免（2026-09-11 gcc-14 CI 红修复的回归锁）───────────────
# 背景：EV-MEM-014 是"循环引用泄漏"演示卡——ASan 跑出的 LeakSanitizer 报错**正是它的 claim**
# （泄漏可观测），旧工具一律判 refute:sanitizer_reported，使该卡在 CI 永远红。新增
# `expected_sanitizer` 声明后：命中类型全部落在声明内 → 折算 expected（计入 confirm）；
# 声明外类型仍 refute——豁免不是逃生舱。
LEAK_BLOB = """=================================================================
==12345==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 96 byte(s) in 2 object(s) allocated from:
    #0 0x7f in operator new(unsigned long) (/lib/libasan.so+0x1)
    #1 0x55 in main (/tmp/a.out+0x1)

SUMMARY: AddressSanitizer: 96 byte(s) leaked in 2 allocation(s).
"""
OVERFLOW_BLOB = """=================================================================
==12345==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x603000000010
WRITE of size 4 at 0x603000000010 thread T0
    #0 0x55 in main (/tmp/a.out+0x1)

SUMMARY: AddressSanitizer: heap-buffer-overflow /tmp/fx.cpp:5
"""


def test_expected_sanitizer_passes():
    """声明 [leak] 且实测就是 leak ⇒ 折算 expected（计入 confirm），不再 refute。

    注意 LSan 的总结行写作 `SUMMARY: AddressSanitizer: ... leaked`（复用 ASan 的总结格式）——
    若按"命中了哪条子串"判定，这条附属信号会把 leak 误判成未声明的 address 类型而继续 refute；
    故判定按**类型**归并（leak 只认 LeakSanitizer，address 只认 ERROR: AddressSanitizer）。
    """
    assert rp.sanitizer_kinds(LEAK_BLOB) == ["leak"], rp.sanitizer_kinds(LEAK_BLOB)
    st, why = rp.classify_sanitizer(LEAK_BLOB, ["leak"])
    assert st == "expected", why
    # 声明字段的形态兼容：全名 / 短别名 / 单串 / true（全部类型）
    assert rp.expected_sanitizer_kinds("LeakSanitizer") == {"leak"}
    assert rp.expected_sanitizer_kinds(["lsan"]) == {"leak"}
    assert rp.expected_sanitizer_kinds(True) == {"leak", "thread", "ub", "address"}


def test_unexpected_sanitizer_still_refutes():
    """声明 [leak] 但实测是 ASan 堆溢出 ⇒ 仍判 refute（豁免只覆盖声明的那一类）。"""
    assert rp.sanitizer_kinds(OVERFLOW_BLOB) == ["address"]
    st, why = rp.classify_sanitizer(OVERFLOW_BLOB, ["leak"])
    assert st == "reported", why
    assert "address" in why
    # 未声明（None）→ 任何命中都算未预期；干净输出 → ok（门禁不得恒红）
    assert rp.classify_sanitizer(LEAK_BLOB)[0] == "reported"
    assert rp.classify_sanitizer("clean run\n")[0] == "ok"
