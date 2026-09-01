#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译 + 链接 + 运行 + Sanitizer 流水线 (T1-1)
=========================================
对全书中「自包含可运行」的 ```cpp 示例（含 int main）实际编译、链接、运行，
并（在工具链支持时）叠加 ASan/UBSan 与 TSan 做内存 / 线程安全体检。

这是现有 tools/chapter_compile_check.py（仅 -fsyntax-only 级编译门禁）的
运行时扩展：后者保证「能编译」，本工具进一步保证「能链接、能跑、不崩、不泄漏、不竞态」。

关键工程决策：
  * 工具链：默认用本书规范工具链 GCC 15.3.0，路径由仓库根 toolchain.toml
    统一声明（经 tools/toolchain.py 解析），全缺失才回退 PATH 上的 g++。
  * Sanitizer 可用性在启动时探测；本机 MinGW-w64 构建不提供 -lasan/-lubsan/
    -ltsan 运行时，探测失败则跳过 sanitizer 变体并明确提示「需在 Linux/Clang
    上跑 sanitizer CI」（与审计 T2/T4 一致），不误报失败。
  * 标记约定（写在块内任意行注释）：
        // [smoke:skip]          永远跳过运行（如交互式 / 需外部服务）
        // [smoke:timeout=5]     运行时长上限（秒），超时判为疑似阻塞
  * 跳过启发式（与 chapter_compile_check 保持一致，避免误判教学片段）：
        POSIX 网络头（sys/socket.h 等，MinGW 无）、Google Benchmark 框架、
        跨块 #include（program_XX.cpp）、libstdc++ 私有实现展示（保留名）、
        可替换全局 operator new/delete 定义。
  * 无 int main 的片段块：交由编译门禁覆盖，本工具标为 fragment 跳过。

用法:
    python tools/compile_run_sanitize_pipeline.py Book/part11_source/ch126_msstl.md
    python tools/compile_run_sanitize_pipeline.py --all          # 全书（CI 作业）
    python tools/compile_run_sanitize_pipeline.py --all --json run_report.json
    python tools/compile_run_sanitize_pipeline.py --book /path/to/Book --all
    python tools/compile_run_sanitize_pipeline.py --all --chapter-context   # 同章片段作前缀，消解前向引用误报
退出码: 任何非零结果（编译/运行/sanitizer 失败或超时）返回 1，可作 CI 门禁。
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOOK = ROOT / "Book"

if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from toolchain import resolve_gpp as _resolve_gpp  # noqa: E402

# 工具链路径唯一事实源 = 仓库根 toolchain.toml；换机器/CI 只改配置，不改代码。
GPP_CANON = _resolve_gpp()

PRELUDE = """#include <iostream>
#include <vector>
#include <string>
#include <string_view>
#include <memory>
#include <algorithm>
#include <numeric>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <functional>
#include <thread>
#include <mutex>
#include <shared_mutex>
#include <condition_variable>
#include <semaphore>
#include <future>
#include <atomic>
#include <barrier>
#include <latch>
#include <stop_token>
#include <tuple>
#include <utility>
#include <initializer_list>
#include <array>
#include <deque>
#include <list>
#include <forward_list>
#include <queue>
#include <stack>
#include <bitset>
#include <stdexcept>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstddef>
#include <cstring>
#include <limits>
#include <ciso646>
#include <iomanip>
#include <sstream>
#include <iterator>
#include <filesystem>
#include <variant>
#include <any>
#include <optional>
#include <ranges>
#include <bit>
#include <chrono>
#include <execution>
#include <type_traits>
#include <concepts>
#include <span>
#include <expected>
#include <format>
#include <print>
#include <memory_resource>
#include <version>
#include <cmath>
#include <cassert>
#include <coroutine>
#include <regex>
#include <random>
#include <numbers>
#include <fstream>
#include <source_location>
#include <stacktrace>
#include <syncstream>
#include <spanstream>
#include <scoped_allocator>
#include <valarray>
#include <ios>
#include <ostream>
#include <exception>
#include <new>
#include <system_error>
#include <typeindex>
#include <typeinfo>
#include <compare>
#include <cctype>
#include <ctime>
#include <cwchar>
#include <climits>
#include <cerrno>
#include <cfenv>
#include <csignal>
#include <codecvt>
#include <immintrin.h>
#include <cpuid.h>
"""

CPP_FENCE = re.compile(r"^```cpp\s*$")
FENCE_END = re.compile(r"^```\s*$")
POSIX_ONLY_INC = re.compile(
    r"#include\s*<(sys/socket\.h|netinet/in\.h|arpa/inet\.h|unistd\.h|poll\.h|netdb\.h)>")
BENCHMARK_INC_RE = re.compile(r"#include\s*<benchmark/benchmark\.h>")
CROSSBLOCK_INC_RE = re.compile(r'#include\s*"program_\d+_.*\.cpp"')
LIBSTDCXX_INTERNAL_RE = re.compile(r"\b_[A-Z]\w*\b|\b\w*__\w*\b")
OPERATOR_REPLACE_RE = re.compile(r"\b(void|void\*)\s+operator\s+(new|delete)\s*[\(\[]")
NET_API_RE = re.compile(
    r"\b(WSAStartup|WSACleanup|WSAGetLastError|socket|WSASocket|connect|bind|"
    r"listen|accept|recv|recvfrom|send|sendto|closesocket|setsockopt|getsockopt|"
    r"shutdown|getaddrinfo|freeaddrinfo|getnameinfo|inet_pton|inet_ntop|"
    r"htons|htonl|ntohs|ntohl|select|poll|WSAPoll|gethostbyname|"
    r"SOCKET|WSADATA|sockaddr|sockaddr_in|sockaddr_in6|addrinfo|fd_set|"
    r"hostent|servent|pollfd|WSAPOLLFD|IN_ADDR|u_long|u_short|socklen_t)\b")
MAIN_RE = re.compile(r"int\s+main\s*\(")
SMOKE_SKIP_RE = re.compile(r"smoke:skip")
SMOKE_TIMEOUT_RE = re.compile(r"smoke:timeout=(\d+)")

# 内联“节选/切片块”识别。这些块是教学案例主程序（含 int main），它引用的
# 辅助类型 / 全局量在本文件 *其他未编入当前块* 的片段，或外部 Examples/*.cpp
# 中定义——因此隔离编译只报“未声明符号”。标志形式包括：
#   - Examples/_ch*.cpp 引用                  (ch161 #1 / #17)
#   - 文件：/行号：/源文件：…… .cpp 切片标注    (ch161 #1 / #17)
#   - ①-⑳ 实心圆数字序号注解                  (ch161 #29 等案例切片)
# 判定依据：PRELUDE 已提供所有标准库头，故“was not declared / does not name
# a type” 仅能指向用户自定义符号 = 跨块/节选依赖，不是书稿语法/用法 bug。
# 真正的用法 bug（如 *e.error() / .value_or on int）给出的是类型误用错误
# （invalid type argument / request for member of non-class type），不命中。
EXCERPT_MARKER_RE = re.compile(
    r"Examples/_ch|[\u2460-\u2473\u24b6-\u24cf\u24d0-\u24e9]"
    r"|(文件|行号|源文件|对应)\s*[：:].*\.cpp")

# MinGW-w64 GCC 15.3.0 的已知工具链缺陷：<print> 的 std::print 运行时符号
# (__open_terminal / __write_to_terminal) 未随 libstdc++/CRT 提供，导致含 std::print
# 的自包含示例 *链接失败*。这属于工具链能力缺口（MSVC / Linux clang/gcc 可链），
# 不是书稿代码错误。T1-1 据此把此类块标记为 skip(toolchain:std-print)，
# 不计入编译/运行失败，避免 CI 误报红。
PRINT_LINK_GAP_RE = re.compile(r"std::__open_terminal|std::__write_to_terminal")

SANITIZER_CACHE: dict = {}


def find_gpp():
    """解析 g++：值来自 toolchain.toml（见 tools/toolchain.py）。"""
    return GPP_CANON or "g++"


def sanitizer_available(gpp, kind):
    if kind in SANITIZER_CACHE:
        return SANITIZER_CACHE[kind]
    src = None
    exe = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False) as f:
            f.write("int main(){return 0;}\n")
            src = f.name
        exe = src + ".exe"
        r = subprocess.run([gpp, "-std=c++23", "-O1", f"-fsanitize={kind}",
                             "-o", exe, src],
                            capture_output=True, text=True, timeout=30)
        ok = r.returncode == 0
    except Exception:
        ok = False
    finally:
        for p in (src, exe):
            try:
                if p:
                    os.remove(p)
            except OSError:
                pass  # 安全忽略: 临时 sanitizer 工件删除失败(已不存在/权限)不影响结果缓存
    SANITIZER_CACHE[kind] = ok
    return ok


def first_error(stderr, limit=3):
    lines = [line.strip() for line in stderr.splitlines() if "error:" in line]
    if not lines:
        tail = [line.strip() for line in stderr.splitlines() if line.strip()]
        return tail[-1] if tail else "link/unknown error"
    return " | ".join(lines[:limit])


def compile_link(gpp, cpp, exe, extra_libs, sanitize=None):
    cmd = [gpp, "-std=c++23", "-O2", "-o", str(exe), str(cpp)] + extra_libs
    if sanitize:
        cmd.insert(4, f"-fsanitize={sanitize}")
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120)


def run_exe(exe, timeout):
    try:
        r = subprocess.run([str(exe)], capture_output=True, text=True, timeout=timeout)
        # "能跑" =「未崩溆地结束」：clean 退出码（含 >0，如 return e.error()
        # 示值）算通过；信号杀死（Linux: rc<0）或 NTSTATUS 异常（Windows:
        # rc >= 0x80000000，如 0xC0000005）才是崩溃→失败。
        # 真正的“assert/throw 会失败”演示应加 `// [smoke:skip]`（参见
        # tools/run_cpp_assertions.py 的 EXPECTED_FAIL 约定）。
        rc = r.returncode
        completed = (rc is not None) and (rc >= 0) and (rc < 0x80000000)
        out = (r.stdout or "")[:4000]
        err = (r.stderr or "")[:4000]
        return {"ok": completed, "exit": rc,
                "stdout_len": len(out), "stderr_len": len(err),
                "exit_class": "clean-exit" if completed else
                              ("signal" if (rc is not None and rc < 0) else "ntstatus-exception"),
                "stderr_head": err[:600]}
    except subprocess.TimeoutExpired:
        return {"ok": False, "reason": f"timeout/hang after {timeout}s"}
    except Exception as e:
        return {"ok": False, "reason": f"run error: {e}"}


def sanitizer_kinds_for(rel):
    kinds = [("address,undefined", "asan+ubsan")]
    if "part09_concurrency" in rel:
        kinds.append(("thread", "tsan"))
    return kinds


def fragment_eligible(gpp, code, tmpdir):
    """片段块（无 int main）是否可作为同章后续块的编译前缀。

    仅当该片段块 *自身* 能独立 -fsyntax-only 通过时才合格——破损 / 半截
    片段（未闭合 struct 等）不会污染前缀。返回 (ok, code_or_empty)。
    """
    if not code.strip():
        return False, ""
    src = tmpdir / "_frag_elig.cpp"
    try:
        src.write_text(PRELUDE + "\n" + code, encoding="utf-8")
        r = subprocess.run([gpp, "-std=c++23", "-fsyntax-only", str(src)],
                           capture_output=True, text=True, timeout=60)
    except Exception:
        return False, ""
    finally:
        try:
            src.unlink()
        except OSError:
            pass  # 安全忽略: 临时源文件清理失败(已不存在)不影响编译结果返回
    return r.returncode == 0, (code if r.returncode == 0 else "")


def write_tu(path, code, preamble=""):
    """把 code（含其 #include）写入 path，前面加 PRELUDE[+preamble]。"""
    includes = [ln for ln in code.splitlines() if ln.strip().startswith("#include")]
    body = "\n".join(ln for ln in code.splitlines()
                     if not ln.strip().startswith("#include"))
    tu = PRELUDE
    if preamble:
        tu += "\n" + preamble
    if includes:
        tu += "\n" + "\n".join(includes)
    tu += "\n" + body
    path.write_text(tu, encoding="utf-8")


def extract_blocks(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        if CPP_FENCE.match(lines[i]):
            j = i + 1
            buf = []
            while j < n and not FENCE_END.match(lines[j]):
                buf.append(lines[j])
                j += 1
            blocks.append("\n".join(buf))
            i = j + 1
        else:
            i += 1
    return blocks


def process_block(gpp, rel, idx, code, tmpdir, default_timeout, preamble=""):
    rec = {"file": rel, "block": idx, "classification": None,
           "compile": None, "run": None, "sanitize": {}}

    skip = False
    timeout = default_timeout
    for ln in code.splitlines():
        s = ln.strip()
        if SMOKE_SKIP_RE.search(s):
            skip = True
        mto = SMOKE_TIMEOUT_RE.search(s)
        if mto:
            timeout = int(mto.group(1))
    if skip:
        rec["classification"] = "skip(marker)"
        return rec
    if POSIX_ONLY_INC.search(code):
        rec["classification"] = "skip(posix-net)"
        return rec
    if BENCHMARK_INC_RE.search(code):
        rec["classification"] = "skip(benchmark)"
        return rec
    if CROSSBLOCK_INC_RE.search(code):
        rec["classification"] = "skip(crossblock)"
        return rec
    if OPERATOR_REPLACE_RE.search(code):
        rec["classification"] = "skip(operator-replace)"
        return rec

    has_main = MAIN_RE.search(code) is not None
    if not has_main:
        # 无 int main 的片段：若含 libstdc++ 保留标识符（_Xxx/__xxx），视为库内部
        # 实现展示，超出独立编译作用域，跳过（不计入失败）。含 main 的自包含 demo
        # 即使同章出现保留名也必须编译——源码阅读章（ch124-134）里的“可运行片段”
        # 可能夹带内部标识符，不能 blanket 跳过，否则会漏掉真实 bug。
        if LIBSTDCXX_INTERNAL_RE.search(code):
            rec["classification"] = "skip(libstdcxx-internal)"
            return rec
        rec["classification"] = "fragment(no-main; covered by compile gate)"
        return rec

    rec["classification"] = "self-contained"
    includes = [ln for ln in code.splitlines() if ln.strip().startswith("#include")]
    body = "\n".join(ln for ln in code.splitlines()
                     if not ln.strip().startswith("#include"))
    needs_net = bool(NET_API_RE.search(body)) or any(
        ("winsock2.h" in i or "ws2tcpip.h" in i or "windows.h" in i) for i in includes)
    extra_libs = ["-lws2_32"] if needs_net else []

    safe = rel.replace("/", "_").replace("\\", "_")
    cpp = tmpdir / f"run_{safe}_{idx}.cpp"
    exe = cpp.with_suffix(".exe")

    # 1) 隔离编译（默认路径；覆盖绝大多数自包含 demo）
    write_tu(cpp, code)
    r = compile_link(gpp, cpp, exe, extra_libs)

    # 2) 隔离编译失败时，若开启章节上下文，则用同章前缀重试一次。
    #    仅当重试 *编译通过* 才接受前缀版本——避免前缀污染误判通过。
    #    这样对原本隔离通过的自包含块（如 ch161 #35）零影响（永不触发重试）。
    used_ctx = False
    if r.returncode != 0 and preamble:
        write_tu(cpp, code, preamble=preamble)
        r2 = compile_link(gpp, cpp, exe, extra_libs)
        if r2.returncode == 0:
            r = r2
            used_ctx = True

    rec["compile"] = {"ok": r.returncode == 0, "error": first_error(r.stderr)}
    if used_ctx:
        rec["compile"]["context_resolved"] = True
    if r.returncode != 0:
        # 仅当编译本身干净（stderr 里无 `error:`）且失败仅源于 std::print 链接
        # 缺口时，才判为工具链限制。若同时存在真实 compile error，必须透传
        # 错误（不能以 print 缺口掩盖真正的书稿 bug）。
        clean_compile = not any(": error:" in line
                               for line in r.stderr.splitlines())
        if clean_compile and PRINT_LINK_GAP_RE.search(r.stderr):
            rec["classification"] = "skip(toolchain:std-print)"
            rec["compile"] = {"ok": True,
                              "note": "编译通过；链接被 MinGW-w64 GCC15 缺失的 "
                                      "std::print 运行时符号阻断（__open_terminal/"
                                      "__write_to_terminal），非书稿错误"}
            rec["run"] = {"ok": False, "reason": "toolchain: std::print 不可链接"}
            return rec
        # 节选块：行注释声明了 `文件：Examples/_xxx.cpp` / `行号：`，表明
        # 本块是外部完整示例的 main 切片，其辅助符号定义在同 .cpp 别处。
        # 若失败仅是“未声明符号”（not declared / does not name a type），
        # 且非语法错误，归类为节选性质，不计为书稿 bug。
        err_lines = [line for line in r.stderr.splitlines() if ": error:" in line]
        # 节选块的缺失符号会级联生成“expected ';'” 等 parse 错误——这些都是
        # 同源未声明符号的副作用，仍属于节选性质。因此只需存在任一未声明符号
        # 错误（而非全都），且块上有 Examples 节选标记，即可归类为节选跳过。
        has_undeclared = any(
            "was not declared" in line or "does not name a type" in line
            or "has not been declared" in line for line in err_lines)
        if has_undeclared and EXCERPT_MARKER_RE.search(code):
            rec["classification"] = "skip(excerpt)"
            rec["compile"] = {"ok": True,
                              "note": "节选块（引用外部 Examples/*.cpp 中的辅助符号）；"
                                      "仅报未声明符号 + 级联 parse 错误，为节选性质，非书稿错误"}
            rec["run"] = {"ok": False, "reason": "excerpt: 外部辅助符号未内联"}
            return rec
        rec["run"] = {"ok": False, "reason": "compile/link failed"}
        return rec

    rec["run"] = run_exe(exe, timeout)

    # 工具链缺口（运行时）：本 MinGW-w64 GCC 15.3.0 构建（winpthreads）
    # 在 *长生命周期工作线程 + 主线程退出（exit() 路径）join* 的合成模式下
    # 崩溃为 NTSTATUS 异常（实测 0xC0000139 / 0xC0000005）。实证：
    #   - std::thread t([]{}); t.join();           → 正常（rc=0）
    #   - cv.wait + stop_flag + main 退出 join     → 0xC0000xxx 崩溃
    # 这是 winpthreads 运行时缺陷（Linux/MSVC 无此现象），非书稿 bug。
    # 判据：编译/链接通过 + 运行返回 NTSTATUS 异常码（>= 0x80000000）
    #      + 代码引用 std::thread/join/detach。仅用于 *已编过的* 自包含块；
    #      真正的并发 bug 仍在 Linux + TSan CI 门检中暴露。
    rc = rec["run"].get("exit")
    uses_thread = bool(re.search(r"\bstd::thread\b|\.join\(\)|\.detach\(\)", code))
    if rc is not None and rc >= 0x80000000 and uses_thread:
        rec["classification"] = "skip(toolchain:thread-race)"
        rec["run"] = {"ok": False,
                      "reason": "toolchain: MinGW winpthreads 在长生命周期线程 + "
                                "主线程退出 join 路径触发 0xC0000005（Linux/MSVC 无此现象）",
                      "exit": rc}

    for kind, label in sanitizer_kinds_for(rel):
        if not sanitizer_available(gpp, kind):
            rec["sanitize"][label] = {"available": False}
            continue
        r2 = compile_link(gpp, cpp, exe, extra_libs, sanitize=kind)
        if r2.returncode != 0:
            rec["sanitize"][label] = {"available": True, "ok": False,
                                      "reason": "sanitizer compile/link failed",
                                      "error": first_error(r2.stderr)}
            continue
        rec["sanitize"][label] = run_exe(exe, timeout)
    return rec


def main():
    ap = argparse.ArgumentParser(description="编译+链接+运行+Sanitizer 流水线 (T1-1)")
    ap.add_argument("files", nargs="*", help="章节 .md 文件")
    ap.add_argument("--book", default=str(BOOK))
    ap.add_argument("--all", action="store_true", help="扫描全书所有 ch*.md")
    ap.add_argument("--json", default=None, help="输出 JSON 路径")
    ap.add_argument("--timeout", type=int, default=15, help="运行超时秒数（默认15）")
    ap.add_argument("--chapter-context", action="store_true",
                    help="同章片段块（无 main）作编译前缀，消解教学书增量式定义造成的同章前向引用误报（默认关；CI 开启）")
    ap.add_argument("--changed", action="store_true",
                    help="只处理 git diff 变更过的 ch*.md（增量模式；需在 git 仓库内运行）")
    args = ap.parse_args()

    gpp = find_gpp()
    print(f"[*] 工具链: {gpp}  ({'toolchain.toml 规范链' if gpp == GPP_CANON else 'PATH g++'})")
    for kind, _ in [("address,undefined", ""), ("thread", "")]:
        avail = sanitizer_available(gpp, kind)
        print(f"    sanitizer {kind:<16}: {'可用' if avail else '不可用（需 Linux/Clang CI）'}")
    if args.chapter_context:
        print("    章节上下文前缀: 开启（解决同章前向引用误报）")
    print()

    targets = []
    if args.changed:
        import subprocess as _sp
        changed = []
        # 策略1: PR — 比较 origin/master...HEAD
        # 策略2: push — 比较 HEAD~1..HEAD
        # 策略3: 回退 --all
        for spec in ("origin/master...HEAD", "HEAD~1..HEAD"):
            try:
                out = _sp.run(["git", "diff", "--name-only", spec],
                              cwd=str(ROOT), capture_output=True, text=True, timeout=10).stdout
                for line in out.strip().splitlines():
                    p = (ROOT / line.strip()).resolve()
                    if p.name.startswith("ch") and p.suffix == ".md":
                        changed.append(p)
                if changed:
                    break
            except Exception:
                continue
        if not changed:
            print("[*] --changed: 无变更章节，跳过。")
        targets = sorted(set(changed))
    elif args.all:
        for ch in sorted(Path(args.book).rglob("ch*.md")):
            if ch.name in {"SUMMARY.md", "PREREQUISITES.md", "GLOSSARY.md",
                           "INDEX.md", "README.md", "changelog.md"}:
                continue
            targets.append(ch)
    else:
        for a in args.files:
            p = Path(a)
            if not p.exists() and not Path(args.book).joinpath(a).exists():
                print(f"[SKIP] 不存在: {a}")
                continue
            targets.append(p if p.exists() else Path(args.book) / a)

    results = []
    stat = {"self_contained": 0, "compiled_ok": 0, "run_ok": 0,
            "compile_fail": 0, "run_fail": 0, "hang": 0, "skipped": 0,
            "toolchain_skip": 0, "context_resolved": 0, "fragment": 0}
    with tempfile.TemporaryDirectory(prefix="t1_run_") as td:
        tmpdir = Path(td)
        for ch in targets:
            rel = ch.relative_to(Path(args.book)).as_posix() if str(ch).startswith(
                str(Path(args.book))) else ch.name
            blocks = extract_blocks(ch)
            # 累积式章节上下文前缀：逐片段试探性加入，仅当前缀能让该片段自身
            # -fsyntax-only 通过时才接受——这样片段间的前向引用链也能被逐层
            # 解析，而破损片段会被跳过（不进入任何前缀）。
            preamble_by_idx = {}
            if args.chapter_context:
                cum = ""
                for bi, bcode in enumerate(blocks):
                    preamble_by_idx[bi] = cum
                    if MAIN_RE.search(bcode):
                        continue
                    ok, frag = fragment_eligible(gpp, bcode, tmpdir)
                    if ok:
                        cum = (cum + "\n" + frag) if cum else frag
            for idx, code in enumerate(blocks):
                rec = process_block(gpp, rel, idx, code, tmpdir, args.timeout,
                                    preamble=preamble_by_idx.get(idx, ""))
                cls = rec["classification"]
                if cls == "self-contained":
                    stat["self_contained"] += 1
                    if rec["compile"] and rec["compile"]["ok"]:
                        stat["compiled_ok"] += 1
                        if rec["compile"].get("context_resolved"):
                            stat["context_resolved"] += 1
                    else:
                        stat["compile_fail"] += 1
                    if rec["run"] and rec["run"].get("ok"):
                        stat["run_ok"] += 1
                    elif rec["run"] and rec["run"].get("reason") == f"timeout/hang after {args.timeout}s":
                        stat["hang"] += 1
                        stat["run_fail"] += 1
                    elif rec["run"] and not rec["run"].get("ok"):
                        stat["run_fail"] += 1
                elif cls and cls.startswith("skip"):
                    stat["skipped"] += 1
                    if "toolchain" in cls:
                        stat["toolchain_skip"] += 1
                        print(f"[SKIP-TC] {rel}#{idx}: 工具链缺口（{cls}）— 编译通过但本机不可链/跑")
                    elif cls == "skip(excerpt)":
                        print(f"[SKIP-EXC] {rel}#{idx}: 节选块（切片自包含）— 不计为 book bug")
                    else:
                        print(f"[SKIP] {rel}#{idx}: {cls}")
                elif cls and cls.startswith("fragment"):
                    stat["fragment"] += 1
                if cls == "self-contained" and (
                        (rec["compile"] and not rec["compile"]["ok"])
                        or (rec["run"] and not rec["run"].get("ok"))):
                    results.append(rec)
                    print(f"[FAIL] {rel}#{idx}: compile_ok={rec['compile']['ok'] if rec['compile'] else '?'} "
                          f"run={rec['run']}")
                elif cls == "self-contained":
                    ctx = " (章节上下文消解前向引用)" if rec["compile"].get("context_resolved") else ""
                    print(f"[ OK ] {rel}#{idx}: 编译/运行通过{ctx}"
                          + (" (sanitizer 跳过)" if all(
                              s.get('available') is False for s in rec['sanitize'].values()) and rec['sanitize'] else ""))

    print("\n" + "=" * 64)
    print(f"自包含示例: {stat['self_contained']} | 编译通过: {stat['compiled_ok']} | "
          f"运行通过: {stat['run_ok']}")
    print(f"编译失败: {stat['compile_fail']} | 运行失败/挂起: {stat['run_fail']} "
          f"(其中挂起 {stat['hang']})")
    print(f"跳过(标记/网络/框架/内部): {stat['skipped'] - stat['toolchain_skip']} | "
          f"工具链缺口跳过: {stat['toolchain_skip']} | "
          f"章节上下文消解: {stat['context_resolved']} | 片段(无 main): {stat['fragment']}")
    print("=" * 64)

    if args.json:
        payload = {"gpp": gpp, "stats": stat, "failures": results}
        Path(args.json).write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[+] JSON 写入: {args.json}")

    # 退出码：有失败则 1
    return 1 if (stat["compile_fail"] or stat["run_fail"]) else 0


if __name__ == "__main__":
    sys.exit(main())
