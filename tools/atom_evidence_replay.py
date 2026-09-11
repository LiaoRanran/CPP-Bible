#!/usr/bin/env python3
"""证据卡机器复算（G3 首项）：把「工件过期 / 卡写错 / 命令跑不通」从人工发现变成机器 refute。

契约（与 `docs/kernel/M2_empirical.md` §1 对齐）：
    输入 = `evidence/**/EV-*.md` 的 YAML frontmatter；机器执行的唯一入口是卡的 `command`
    （多行 shell，逐行执行）——命令不硬编码在工具里。
    必填：`command` / `artifact` / `artifact_sha256` / `actual.run_*`；缺任一 → `refute:missing_field`。

四项校验（任一不过即 refute，退出码 1）：
    1. compile_rc    —— 每条命令退出码 0
    2. run_match     —— 运行输出与卡的 `run_*` 逐字匹配（**精确**，允许行序归一化；
                        多组 `run_*` 值不一致时须用 `expected_key` 指明，否则判 ambiguous）
    3. artifact_sha  —— **删旧工件 → 重跑生成命令 → sha256 必须等于卡的 `artifact_sha256`**
                        （"工件必须与断言同代"的机器化核心：重生成不一致 = 工件过期或卡写错）
    4. sanitizer     —— ASan+UBSan 复编运行无新增报错；工具链不支持则 skip（不算 refute）。
                        卡可声明 `expected_sanitizer`（如 `[leak]`）：命中的报错类型**全部**在
                        声明内时计入 confirm（演示卡的反向证据），声明外类型仍 refute。

用法：
    python tools/atom_evidence_replay.py                 # 扫描 evidence/**/EV-*.md
    python tools/atom_evidence_replay.py --card <path>   # 单卡
    python tools/atom_evidence_replay.py --check         # 任一 refute 即 exit 1（门禁用）
    python tools/atom_evidence_replay.py --no-sanitizer  # 跳过 sanitizer 校验
    python tools/atom_evidence_replay.py --keep-tmp      # 保留临时目录（排查用）
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / "evidence"
SANITIZER_SIGNS = ("ERROR: AddressSanitizer", "runtime error:", "LeakSanitizer",
                   "ERROR: ThreadSanitizer", "SUMMARY: AddressSanitizer")

# sanitizer 报错**类型**判定（2026-09-11 CI gcc-14 红修复）。
# 为何不能按"命中了 SANITIZER_SIGNS 里哪几条"直接豁免：LeakSanitizer 的总结行会同时含
# `SUMMARY: AddressSanitizer`（LSan 复用 ASan 的总结格式，实测 WSL g++-14 输出），
# 于是 `[leak]` 声明会被 "SUMMARY: AddressSanitizer" 这条附属信号带偏、判成未声明类型。
# 故按**类型**归并：address 只认 `ERROR: AddressSanitizer`（ASan 真报错），
# leak 只认 `LeakSanitizer`——两者互不串味。
SANITIZER_KIND_SIGNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("leak", ("LeakSanitizer",)),
    ("thread", ("ERROR: ThreadSanitizer",)),
    ("ub", ("runtime error:",)),
    ("address", ("ERROR: AddressSanitizer",)),
)
SANITIZER_KIND_ALIASES: dict[str, str] = {
    "leak": "leak", "lsan": "leak", "leaksanitizer": "leak",
    "address": "address", "asan": "address", "addresssanitizer": "address",
    "thread": "thread", "tsan": "thread", "threadsanitizer": "thread",
    "ub": "ub", "ubsan": "ub", "undefined": "ub",
}


# ── 最小 YAML frontmatter 解析（零第三方依赖：只覆盖证据卡用到的形态）──────────
def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _strip_comment(s: str) -> str:
    """剥离行尾注释（引号内的 # 不算）。"""
    out: list[str] = []
    quote = ""
    for ch in s:
        if quote:
            out.append(ch)
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif ch == "#":
            break
        else:
            out.append(ch)
    return "".join(out).rstrip()


def _split_flow(inner: str) -> list[str]:
    """按顶层逗号切分 flow 内容（不切 `{}`/`[]` 内部）。"""
    out: list[str] = []
    depth = 0
    cur: list[str] = []
    for ch in inner:
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    if cur:
        out.append("".join(cur))
    return out


def _scalar(raw: str) -> Any:
    s = raw.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    low = s.lower()
    if low in ("true", "yes"):               # YAML 布尔（否则 first_hand 会变成字符串）
        return True
    if low in ("false", "no"):
        return False
    if s.startswith("{") and s.endswith("}"):     # 内联 flow map 作为值（actual/matrix）
        return _parse_flow_map(s)
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        items: list[Any] = []
        for x in _split_flow(inner):
            x = x.strip()
            # `relations: [{type: prerequisite, target: X}]` 是 G1_layout 模板的标准写法，
            # 内联 flow map 必须解析成 dict，否则关系规则全部读不到边。
            items.append(_parse_flow_map(x) if x.startswith("{") and x.endswith("}")
                         else _scalar(x))
        return items
    return s


def _read_block_scalar(lines: Sequence[str], i: int, indent: int, fold: bool) -> tuple[str, int]:
    buf: list[str] = []
    j = i
    while j < len(lines):
        ln = lines[j]
        if ln.strip() and _indent(ln) <= indent:
            break
        buf.append(ln)
        j += 1
    body = [ln for ln in buf]
    while body and not body[-1].strip():
        body.pop()
    pads = [_indent(ln) for ln in body if ln.strip()]
    cut = min(pads) if pads else 0
    pieces = [ln[cut:].rstrip() for ln in body]
    text = " ".join(p.strip() for p in pieces if p.strip()) if fold \
        else "\n".join(pieces)
    return text, j


def _parse_flow_map(raw: str) -> dict[str, Any]:
    inner = raw.strip()[1:-1]
    out: dict[str, Any] = {}
    # 必须用 _split_flow（顶层逗号）而非裸 split(",")：否则 `{refutations: [EV-1, EV-2]}`
    # 会被内层逗号切断，只读到 1 个元素（2026-09-10 由误解分层测试暴露）。
    for part in _split_flow(inner):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip()] = _scalar(v)
    return out


def _parse_block(lines: Sequence[str], i: int, indent: int) -> tuple[Any, int]:
    n = len(lines)
    while i < n and (not lines[i].strip() or lines[i].strip().startswith("#")):
        i += 1
    if i >= n or _indent(lines[i]) < indent:
        return None, i

    if lines[i].strip().startswith("- "):
        items: list[Any] = []
        while i < n:
            ln = lines[i]
            if not ln.strip():
                i += 1
                continue
            if _indent(ln) < indent or not ln.strip().startswith("- "):
                break
            # 列表项也要剥行尾注释（2026-09-10 暴露：`- {kind: call_count, ...}  # 说明`
            # 因尾部注释而不以 `}` 结尾 → 退化成字符串，flow map 内容全丢）。引号内的 # 受保护。
            content = _strip_comment(ln.strip()[2:]).strip()
            if content.startswith("{") and content.endswith("}"):
                items.append(_parse_flow_map(content))
                i += 1
                continue
            if re.match(r"^[A-Za-z_][\w.\-]*:", content):
                sub = [" " * (indent + 2) + content]
                i += 1
                while i < n and _indent(lines[i]) > indent and not lines[i].strip().startswith("- "):
                    sub.append(lines[i])
                    i += 1
                val, _ = _parse_block(sub, 0, indent + 2)
                items.append(val)
                continue
            items.append(_scalar(content))
            i += 1
        return items, i

    out: dict[str, Any] = {}
    while i < n:
        ln = lines[i]
        if not ln.strip() or ln.strip().startswith("#"):
            i += 1
            continue
        if _indent(ln) < indent:
            break
        m = re.match(r"^([A-Za-z_][\w.\-]*):\s*(.*)$", ln.strip())
        if not m:
            i += 1
            continue
        key, rest = m.group(1), _strip_comment(m.group(2)).strip()
        i += 1
        if rest in ("|", "|-", "|+", ">", ">-", ">+"):
            val, i = _read_block_scalar(lines, i, indent, fold=rest.startswith(">"))
            out[key] = val
        elif rest == "":
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j < n and _indent(lines[j]) > indent:
                out[key], i = _parse_block(lines, i, _indent(lines[j]))
            else:
                out[key] = None
        else:
            # 支持 plain scalar 的折叠续行（如 `asm:` 的第二行解释）
            parts = [rest]
            while i < n and lines[i].strip() and _indent(lines[i]) > indent \
                    and not re.match(r"^[A-Za-z_][\w.\-]*:", lines[i].strip()):
                parts.append(_strip_comment(lines[i].strip()))
                i += 1
            out[key] = _scalar(" ".join(parts))
    return out, i


def parse_frontmatter(text: str) -> dict[str, Any]:
    """解析 `---` 包裹的 YAML 子集；不足子集形态抛 ValueError。"""
    if not text.startswith("---"):
        raise ValueError("卡缺少 frontmatter")
    end = text.find("\n---", 3)
    if end < 0:
        raise ValueError("frontmatter 未闭合")
    lines = text[3:end].strip("\n").split("\n")
    meta, _ = _parse_block(lines, 0, 0)
    if not isinstance(meta, dict):
        raise ValueError("frontmatter 顶层不是映射")
    return meta


# ── 卡校验 ────────────────────────────────────────────────────────────────
SHELL_META = ("|", ">", "<", "*", "$", "`", ";")


def _split_argv(cmd: str) -> list[list[str]] | None:
    """把一条命令按 `&&` 拆为多段 argv；含不支持的 shell 特性时返回 None。

    设计（为何不用 shell=True）：卡的 `command` 按 POSIX 语义书写，但 Windows cmd 不认
    `./x`（实测带 `./` 前缀的 exe 在 cmd 下均不可执行）。改为**不经 shell**：`&&` 拆段 +
    `shlex` 解析 + 去掉 `./` 前缀（两平台相对路径都可直接 exec），既跨平台可靠又无注入风险。
    不支持的：管道/重定向/通配/变量展开——遇到就报 unsupported（诚实，不猜）。
    """
    if any(m in cmd for m in SHELL_META):
        return None
    out: list[list[str]] = []
    for seg in (s.strip() for s in cmd.split("&&")):
        if not seg:
            continue
        try:
            args = shlex.split(seg, posix=True)
        except ValueError:
            return None
        if not args:
            continue
        out.append([a[2:] if a.startswith("./") else a for a in args])
    return out or None


def _pin_compiler(argv: list[str]) -> list[str]:
    """把 argv[0] 的**裸编译器名**钉到 `toolchain` 解析出的完整路径。

    为何必须（2026-09-10 监工复现的假阳性）：Windows 多 MinGW 环境下 CreateProcess 按 PATH
    解析裸 `g++` —— 本机 PATH 里是 mingw**1310**（13.1.0），它在 subprocess 环境里找不到
    cc1plus，报 `fatal error: cannot execute 'cc1plus'`。此前工具只因调用者 PATH 恰好前置了
    1530 才"通过"，一旦换环境即 `refute:compile_failed`。钉死后结果与调用者 PATH 无关。
    """
    if not argv:
        return argv
    base = Path(argv[0]).name.lower()
    if base in ("g++", "gcc", "c++", "cc", "g++.exe", "gcc.exe"):
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from toolchain import resolve_gpp
            resolved = resolve_gpp()
            # 判据是"解析结果与命令行**字面量**不同"，不是"basename 不同"（2026-09-10 CI 修）：
            # Linux 上 resolve_gpp() 回退 PATH 得 `/usr/bin/g++`，其 basename 恰为 `g++`，
            # 旧判据据此认为"无需替换"而保留裸名——该环境恰好可用，但**行为随平台漂移**
            # （Windows 换 basename 则替换）。统一为：解析到任何与字面量不同的路径就替换，
            # 使最终执行与调用者 PATH 无关，语义也不依赖平台。
            if resolved and resolved != argv[0]:
                return [resolved, *argv[1:]]
        except Exception:                                   # pragma: no cover
            pass
    elif base in ("clang++", "clang", "clang++.exe", "clang.exe"):
        found = shutil.which(base) or shutil.which(base.replace(".exe", ""))
        if found:
            return [found, *argv[1:]]
    return argv


def run_commands(lines: Sequence[str], cwd: Path, env: dict) -> tuple[list[tuple[str, int, str]], str]:
    """逐行执行命令（`&&` 拆段、不经 shell、裸编译器名钉完整路径）。

    返回 ([(cmd, rc, stderr)], 合并 stdout)。`&&` 语义保留：同段内前一条失败即短路。
    """
    results: list[tuple[str, int, str]] = []
    stdout_parts: list[str] = []
    for raw in lines:
        cmd = raw.strip()
        if not cmd or cmd.startswith("#"):
            continue
        argv_list = _split_argv(cmd)
        if argv_list is None:
            results.append((cmd, 127, "含不支持的 shell 特性（管道/重定向/通配/变量）"))
            continue
        failed = False
        for argv in argv_list:
            if failed:                                      # `&&` 短路
                break
            argv = _pin_compiler(argv)
            try:
                r = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True,
                                   errors="replace", timeout=600, env=env)
                rc, err, out = r.returncode, (r.stderr or "").strip()[:400], r.stdout or ""
            except FileNotFoundError:                       # 编译失败后 exe 不存在 → 不崩溃
                rc, err, out = 127, f"可执行文件不存在或不可执行：{argv[0]}", ""
            except subprocess.TimeoutExpired:
                rc, err, out = 124, f"命令超时（600s）：{argv[0]}", ""
            results.append((cmd, rc, err))
            if out:
                stdout_parts.append(out)
            failed = rc != 0
    return results, "\n".join(stdout_parts)


def _sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _platform_tag() -> str:
    """平台标签：工件字节与平台强相关（同为 GCC 15，MinGW 与 Linux 的 .asm 也不同）。"""
    if sys.platform == "win32":
        return "MinGW-w64"
    if sys.platform.startswith("linux"):
        return "Linux"
    if sys.platform == "darwin":
        return "macOS"
    return sys.platform


def _compiler_id(gpp: str) -> str:
    """返回 `GCC 15.3.0 (MinGW-w64)` 形式的编译器身份；解析失败返回 ""。

    `-dumpfullversion` 优先（GCC 7+ 的 `-dumpversion` 只给 major），失败再退回。
    """
    if not gpp:
        return ""
    ver = ""
    for flag in ("-dumpfullversion", "-dumpversion"):
        try:
            r = subprocess.run([gpp, flag], capture_output=True, text=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            return ""
        ver = (r.stdout or "").strip().splitlines()[0] if r.stdout.strip() else ""
        if ver:
            break
    if not ver:
        return ""
    name = "Clang" if "clang" in Path(gpp).name.lower() else "GCC"
    return f"{name} {ver} ({_platform_tag()})"


def _current_toolchain_id() -> str:
    """当前环境实际生成工件所用的编译器身份（与卡 `artifact_compiler` 比对）。"""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from toolchain import resolve_gpp
        return _compiler_id(resolve_gpp())
    except Exception:                                     # pragma: no cover
        return ""


def check_artifact_assert(meta: dict[str, Any], art_path: Path) -> tuple[bool, list[str]]:
    """跨编译器可移植的**结构断言**（编译产物内容级，不依赖字节哈希）。

    为何需要：`artifact_sha256` 只能在同一编译器（含平台）下复算——实测同一夹具
    MinGW GCC 15.3 与 GCC 13.1 产出的 .asm 字节完全不同（2026-09-10 CI 红因）。
    故工件归属编译器与当前环境不符时，改判本函数；**断言缺失或不满足仍判 refute**
    （"降级"是换成另一种真实校验，不是逃生舱）。

    支持 kind：
      - `contains`      `{kind: contains, text: "_Znwy"}`              必须出现
      - `contains_any`  `{kind: contains_any, texts: ["call\tmalloc", "call\t_Znwm"]}`
                       任候出现即可——**跨平台/跨版本首选形态**（符号名与拼写差异都吸收掉）
      - `absent`        `{kind: absent, text: "call _Znwm"}`            必须不出现（反例路径）
      - `call_count`    `{kind: call_count, symbols: ["malloc"], count: 3}`  调用计数
                        ⚠️ 调用点数量随编译器的内联决策变化（实测同一夹具 GCC 15.3 = 3 次、
                        GCC 13.1 = 4 次），**只在单一编译器平台的卡上使用**；跨编译器卡请改用
                        符号存在性断言，把"次数"语义交给运行层 run_match（跨平台稳定）。

    文本比较前做**空白归一**（`\t` → 空格，含卡里字面写的 `\t`）：不同平台/编译器的汇编用
    不同空白分隔（`call\tmalloc` vs `call malloc`），归一后断言才可比。
    """
    rules = meta.get("artifact_assert")
    rules = [r for r in rules if isinstance(r, dict)] if isinstance(rules, list) else []
    if not rules:
        return False, ["卡缺 artifact_assert[]：编译器不匹配时无可用校验"]
    text = art_path.read_text(encoding="utf-8", errors="replace").replace("\t", " ")

    def _norm(s: str) -> str:
        """卡里的断言按可读写法书写（`\\t` 是两个字面字符），归一成单空格。"""
        return s.replace("\\t", " ").replace("\t", " ")
    lines: list[str] = []
    ok = True
    for r in rules:
        kind = str(r.get("kind") or "")
        if kind == "call_count":
            syms = [str(s) for s in (r.get("symbols") or [])] or \
                   ([str(r["symbol"])] if r.get("symbol") else [])
            want = int(r.get("count") or 0)
            # 多符号**求和**：同一逻辑在不同平台走不同入口（MinGW 的 operator new 是
            # `jmp malloc` 跳板 → `call malloc`；Linux 是弱符号 → `call _Znwm@PLT`），
            # 而"分配入口被调用几次"这一语义跨平台一致。
            got = sum(1 for ln in text.split("\n")
                      if any(re.search(rf"\bcall\s+{re.escape(s)}\b", ln) for s in syms))
            hit = got == want
            lines.append(f"    {'✅' if hit else '❌'} call_count {'/'.join(syms)}"
                         f" 期望 {want} 实得 {got}")
        elif kind == "contains_any":
            texts = [str(t) for t in (r.get("texts") or [])]
            seen = {t: text.count(_norm(t)) for t in texts}
            hit = any(n > 0 for n in seen.values())
            detail = ", ".join(f"{t!r}:{n}" for t, n in seen.items())
            lines.append(f"    {'✅' if hit else '❌'} contains_any 任一出现（{detail}）")
        elif kind in ("contains", "absent"):
            lit = str(r.get("text") or "")
            got = text.count(_norm(lit))
            hit = (got > 0) if kind == "contains" else (got == 0)
            verb = "出现" if kind == "contains" else "不得出现"
            lines.append(f"    {'✅' if hit else '❌'} {kind} {lit!r} {verb}（实得 {got} 次）")
        else:
            hit = False
            lines.append(f"    ❌ 未知断言 kind：{kind!r}（不猜，判失败）")
        ok = ok and hit
    return ok, lines


def _compiler_env() -> dict:
    """把编译器目录注入 PATH（MinGW 的 exe/sanitizer 运行期依赖同目录 DLL）。"""
    env = dict(os.environ)
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from toolchain import resolve_gpp  # 复用既有解析（prefer→PATH→兜底）
        bindir = str(Path(resolve_gpp()).resolve().parent)
        if bindir not in env.get("PATH", ""):
            env["PATH"] = bindir + os.pathsep + env.get("PATH", "")
    except Exception:                                   # pragma: no cover
        pass
    return env


def sanitizer_kinds(blob: str) -> list[str]:
    """从 sanitizer 输出里判定报错**类型**（leak/thread/ub/address，按固定顺序）。

    纯函数（不跑编译器），使豁免判定可被单元测试直接锁定——本机 MinGW 无 sanitizer 运行时，
    若把判定逻辑埋在 subprocess 之后，这条契约就只能在 Linux 上被测试覆盖（覆盖不对称）。
    """
    return [k for k, signs in SANITIZER_KIND_SIGNS if any(s in blob for s in signs)]


def expected_sanitizer_kinds(exp: Any) -> set[str]:
    """把卡的 `expected_sanitizer` 声明规范化为类型集合（`true` = 全部类型）。

    接受列表（`[leak]` / `[address, ub]`）或单个字符串；别名（`lsan`/`asan`/`ubsan`…）归一到
    类型名。未识别的词原样保留——它不会匹配任何实测类型，于是该卡仍判 refute（不静默放行）。
    """
    if exp is True:
        return {k for k, _ in SANITIZER_KIND_SIGNS}
    if isinstance(exp, str):
        exp = [exp]
    if not isinstance(exp, (list, tuple)):
        return set()
    out: set[str] = set()
    for raw in exp:
        w = str(raw).strip().lower()
        if w:
            out.add(SANITIZER_KIND_ALIASES.get(w, w))
    return out


def classify_sanitizer(blob: str, expected: Any = None) -> tuple[str, str]:
    """纯函数：把 sanitizer 输出判成 ok / expected / reported（+ 说明）。

    check_sanitizer 只负责"跑出 blob"，判定收敛在此处——本机 MinGW 无 sanitizer 运行时，
    若判定埋在 subprocess 之后，这条豁免契约就只能在 Linux 上被测到（覆盖不对称）。
    """
    if not any(s in blob for s in SANITIZER_SIGNS):
        return "ok", "无 sanitizer 报错"
    kinds = sanitizer_kinds(blob) or ["unknown"]
    allow = expected_sanitizer_kinds(expected)
    unexpected = [k for k in kinds if k not in allow]
    if allow and not unexpected:
        return "expected", f"命中 {', '.join(kinds)}（卡预期内演示性报错，反向证 claim）"
    why = f"命中 {', '.join(kinds)}"
    if allow and unexpected:
        why += f"（未在 expected_sanitizer 声明：{', '.join(unexpected)}）"
    return "reported", why


def check_sanitizer(meta: dict[str, Any], workdir: Path, env: dict) -> tuple[str, str]:
    """返回 (状态, 说明)：ok / expected / reported / skipped。

    `expected_sanitizer`（卡可选字段）声明"本卡演示的就是这类报错"：命中类型**全部**落在声明内
    时返回 `expected`（计入 confirm——它反向证成了 claim，如循环引用泄漏演示卡）；未声明、或
    命中了声明外的类型，一律 `reported` → refute（豁免不是逃生舱）。
    """
    fixture = meta.get("fixture")
    if not fixture or not (ROOT / str(fixture)).is_file():
        return "skipped", f"fixture 不存在：{fixture}"
    matrix = meta.get("matrix") or {}
    stds = matrix.get("std") if isinstance(matrix, dict) else None
    std = (stds[0] if isinstance(stds, list) and stds else "c++17")
    try:
        from toolchain import resolve_gpp
        gpp = resolve_gpp()
    except Exception:                                   # pragma: no cover
        return "skipped", "无法解析 g++"
    exe = workdir / "san.exe"
    c = subprocess.run([gpp, f"-std={std}", "-O1", "-g",
                        "-fsanitize=address,undefined", str(ROOT / str(fixture)), "-o", str(exe)],
                       capture_output=True, text=True, errors="replace", timeout=300, env=env)
    if c.returncode != 0:
        return "skipped", f"工具链不支持 ASan/UBSan：{(c.stderr or '').strip()[:120]}"
    # ASan 的分配器对"超过上限的分配请求"默认**abort 报 OOM**（`allocator_may_return_null=0`），
    # 而真实运行时同一请求只是**分配失败**——对 `new (std::nothrow) T[huge]` 这类"故意让分配失败"
    # 的演示卡（EV-MEM-018：约 400GB 请求 ⇒ 期望返回 nullptr），默认行为把"预期返回 null"误判成
    # refute:sanitizer(address)。注入标准选项 `allocator_may_return_null=1` 让 ASan 回归真实语义
    # （分配失败返回 null），而**越界/泄漏/UB 的检测能力一条不减**——这是"换一种真校验"，不是豁免通道
    # （2026-09-11 gcc-14 CI 红修复，实测注入后 EV-MEM-018 输出与卡 run_* 逐字一致）。
    san_env = dict(env)
    san_env["ASAN_OPTIONS"] = (san_env.get("ASAN_OPTIONS", "") +
                               ":allocator_may_return_null=1").lstrip(":")
    r = subprocess.run([str(exe)], capture_output=True, text=True, errors="replace",
                       timeout=300, env=san_env)
    blob = (r.stderr or "") + (r.stdout or "")
    return classify_sanitizer(blob, meta.get("expected_sanitizer"))


def replay_card(path: Path, *, do_sanitizer: bool = True, keep_tmp: bool = False,
                restore_artifact: bool = True) -> tuple[str, list[str]]:
    """执行四项校验。返回 (verdict, 日志行)。verdict ∈ confirm / refute:<reason>。

    `restore_artifact`（默认 True）：校验结束后把仓库里的 `artifact` 还原成本次运行前的字节。
    为什么需要（2026-09-10 踩坑）：校验流程是「删旧工件 → 重生成 → 比 sha256」，这在**同一编译器
    环境**下无害；但在**异构环境**（如 WSL/Linux 上跑，而卡声明 MinGW 归属）会把仓库工件**静默
    改写成异平台产物**——实测一次 WSL 复算就把 4 份 `.asm` 全换成 ELF/Linux 版（汇编里出现
    `endbr64` / `__printf_chk@PLT`），而卡里的 sha256 仍是 MinGW 的 → 仓库工件与卡**不同代**。
    校验工具是只读角色，不该改写被校验对象；要留调试痕迹时用 `--no-restore`。
    """
    try:                                   # 卡可能不在仓库内（--card 指向临时路径）
        shown = path.relative_to(ROOT).as_posix()
    except ValueError:
        shown = str(path)
    log: list[str] = [f"[replay] {shown}"]
    try:
        meta = parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
    except ValueError as exc:
        return "refute:bad_frontmatter", log + [f"  ❌ {exc}"]

    # ① 必填字段
    missing: list[str] = []
    for k in ("command", "artifact", "artifact_sha256"):
        if not meta.get(k):
            missing.append(k)
    actual = meta.get("actual") or {}
    run_keys = [k for k in (actual if isinstance(actual, dict) else {}) if k.startswith("run")]
    if not run_keys:
        missing.append("actual.run_*")
    if missing:
        return "refute:missing_field", log + [f"  ❌ 缺字段：{', '.join(missing)}"]

    art_rel = str(meta["artifact"])
    art_path = ROOT / art_rel
    want_sha = str(meta["artifact_sha256"]).strip().lower()
    cmd_lines = str(meta["command"]).split("\n")

    env = _compiler_env()
    (ROOT / "build").mkdir(exist_ok=True)      # 卡命令产物约定写 build/（仓库源只读）
    tmp = Path(tempfile.mkdtemp(prefix="replay_"))
    original = art_path.read_bytes() if art_path.exists() else None   # 校验前快照（见 docstring）
    try:
        # 工件生成命令 = 命令行里出现 artifact 路径的那条（从卡推导，不硬编码）
        gen = [ln for ln in cmd_lines if ln.strip() and art_rel in ln]
        if not gen:
            return "refute:missing_artifact_command", log + [
                f"  ❌ command 中没有生成 {art_rel} 的命令"]

        # ② 先删旧工件（存在才删），确保"重生成"而非复用旧产物
        # 注意：工件**不存在**是合法场景（新卡首次复算）——由下面的命令生成，
        # 生成后仍缺失才判 artifact_absent（曾误判，2026-09-10 由测试暴露）。
        art_path.unlink(missing_ok=True)

        results, stdout_all = run_commands(cmd_lines, ROOT, env)
        bad = [(c, rc, err) for c, rc, err in results if rc != 0]
        if bad:
            log.append(f"  ❌ compile_rc：{len(bad)}/{len(results)} 条命令失败")
            for c, rc, err in bad[:3]:
                log.append(f"      rc={rc} {c[:80]} :: {err[:160]}")
            return "refute:compile_failed", log
        log.append(f"  ✅ compile_rc    {len(results)} 条命令全部退出码 0")

        # ③ run_match：输出行集合 vs 卡里 run_* 片段集合（行序归一化）
        got = [ln.strip() for ln in stdout_all.split("\n") if ln.strip()]
        variants = {tuple(sorted(p.strip() for p in str(v).split("|") if p.strip()))
                    for v in (actual[k] for k in run_keys)}
        if len(variants) > 1:
            key = meta.get("expected_key")
            if not key or key not in actual:
                log.append(f"  ❌ run_match    多组 run_* 值不一致（{len(variants)} 种），"
                           f"卡须用 expected_key 指明 command 对应哪组")
                return "refute:ambiguous_expected", log
            variants = {tuple(sorted(p.strip() for p in str(actual[key]).split("|") if p.strip()))}
        want = next(iter(variants))
        if tuple(sorted(got)) != want:
            log.append("  ❌ run_match    输出与卡不符（精确比对，行序已归一化）")
            log.append(f"      期望 {len(want)} 行：{list(want)}")
            log.append(f"      实际 {len(got)} 行：{got}")
            return "refute:run_mismatch", log
        log.append(f"  ✅ run_match    输出 {len(got)} 行与 run_* 逐字一致（行序归一化）")

        # ④ artifact_sha：重生成后的工件必须与卡同代
        # 分流（2026-09-10 CI 红因修复）：sha 只在**同一编译器（含平台）**下可复算——
        # 实测同一夹具 MinGW GCC 15.3 与 GCC 13.1 产出的 .asm 字节完全不同，CI 跑在
        # Ubuntu（系统 g++ ≠ 卡归属的 MinGW 15.3）时必然 mismatch。故：
        #   编译器身份**匹配**   → 强制 sha256（"工件同代"原承诺不变）
        #   编译器身份**不匹配** → 改判 artifact_assert[] 结构断言（真实内容校验）；
        #                          断言缺失或不满足仍 refute——"降级"是换一种真校验，
        #                          不是逃生舱。
        if not art_path.exists():
            log.append(f"  ❌ artifact_sha  重生成后工件不存在：{art_rel}")
            return "refute:artifact_absent", log
        got_sha = _sha256(art_path)
        owner = str(meta.get("artifact_compiler") or "").strip()
        cur_id = _current_toolchain_id()
        if got_sha == want_sha:
            log.append(f"  ✅ artifact_sha  {got_sha[:16]}… == 卡值（归属 {owner or '未声明'}）")
        elif owner and cur_id and owner != cur_id:
            log.append(f"  ⏭ artifact_sha  编译器不匹配，改判结构断言"
                       f"（本地 {cur_id} vs 卡归属 {owner}）")
            a_ok, a_lines = check_artifact_assert(meta, art_path)
            log.extend(a_lines)
            if not a_ok:
                log.append("  ❌ artifact_assert  跨编译器替代校验未通过")
                return "refute:artifact_assert_failed", log
            log.append(f"  ✅ artifact_assert  {len(a_lines)} 条结构断言全部满足"
                       f"（字节差异属跨编译器正常）")
        else:
            log.append("  ❌ artifact_sha  工件与卡不同代（过期工件或卡写错）")
            log.append(f"      期望 {want_sha}")
            log.append(f"      实际 {got_sha}")
            log.append(f"      归属 {owner or '未声明'} · 本地 {cur_id or '未知'}")
            return "refute:sha256_mismatch", log

        # ⑤ sanitizer
        if do_sanitizer:
            st, why = check_sanitizer(meta, tmp, env)
            if st == "reported":
                log.append(f"  ❌ sanitizer    {why}")
                return "refute:sanitizer_reported", log
            log.append(f"  {'✅' if st in ('ok', 'expected') else '⏭'} sanitizer    {why}")
        else:
            log.append("  ⏭ sanitizer    已按 --no-sanitizer 跳过")
        return "confirm", log
    finally:
        if restore_artifact and original is not None:
            art_path.write_bytes(original)     # 还原：校验工具不改写被校验对象（见 docstring）
        if not keep_tmp:
            shutil.rmtree(tmp, ignore_errors=True)


def find_cards() -> list[Path]:
    return sorted(p for p in EVIDENCE.rglob("EV-*.md"))


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="证据卡机器复算（confirm / refute）")
    ap.add_argument("--card", action="append", default=[], help="指定证据卡（可多次）")
    ap.add_argument("--check", action="store_true", help="任一 refute 即 exit 1")
    ap.add_argument("--no-sanitizer", action="store_true", help="跳过 sanitizer 校验")
    ap.add_argument("--keep-tmp", action="store_true", help="保留临时目录")
    ap.add_argument("--no-restore", action="store_true",
                    help="校验后不还原仓库工件（默认还原：校验不应改写被校验对象）")
    a = ap.parse_args(argv)

    cards = [Path(c) if Path(c).is_absolute() else ROOT / c for c in a.card] or find_cards()
    if not cards:
        print("[replay] 未找到证据卡（evidence/**/EV-*.md）")
        return 0

    n_ok = n_bad = 0
    for card in cards:
        verdict, log = replay_card(card, do_sanitizer=not a.no_sanitizer,
                                   keep_tmp=a.keep_tmp,
                                   restore_artifact=not a.no_restore)
        ok = verdict == "confirm"
        n_ok += ok
        n_bad += not ok
        print("\n".join(log))
        print(f"  → {verdict}\n")
    print(f"[replay] confirm={n_ok} refute={n_bad} 共 {len(cards)} 张卡")
    return 1 if (a.check and n_bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
