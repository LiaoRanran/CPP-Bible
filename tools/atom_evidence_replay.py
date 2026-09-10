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
    4. sanitizer     —— ASan+UBSan 复编运行无新增报错；工具链不支持则 skip（不算 refute）

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


def _scalar(raw: str) -> Any:
    s = raw.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [x.strip() for x in inner.split(",")] if inner else []
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
    for part in inner.split(","):
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
            content = ln.strip()[2:]
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
            if resolved and Path(resolved).name.lower() != base:
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


def check_sanitizer(meta: dict[str, Any], workdir: Path, env: dict) -> tuple[str, str]:
    """返回 (状态, 说明)：ok / reported / skipped。"""
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
    r = subprocess.run([str(exe)], capture_output=True, text=True, errors="replace",
                       timeout=300, env=env)
    blob = (r.stderr or "") + (r.stdout or "")
    hit = [s for s in SANITIZER_SIGNS if s in blob]
    if hit:
        return "reported", f"命中 {hit[0]!r}"
    return "ok", "无 sanitizer 报错"


def replay_card(path: Path, *, do_sanitizer: bool = True, keep_tmp: bool = False) -> tuple[str, list[str]]:
    """执行四项校验。返回 (verdict, 日志行)。verdict ∈ confirm / refute:<reason>。"""
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
        if not art_path.exists():
            log.append(f"  ❌ artifact_sha  重生成后工件不存在：{art_rel}")
            return "refute:artifact_absent", log
        got_sha = _sha256(art_path)
        if got_sha != want_sha:
            log.append("  ❌ artifact_sha  工件与卡不同代（过期工件或卡写错）")
            log.append(f"      期望 {want_sha}")
            log.append(f"      实际 {got_sha}")
            return "refute:sha256_mismatch", log
        log.append(f"  ✅ artifact_sha  {got_sha[:16]}… == 卡值")

        # ⑤ sanitizer
        if do_sanitizer:
            st, why = check_sanitizer(meta, tmp, env)
            if st == "reported":
                log.append(f"  ❌ sanitizer    {why}")
                return "refute:sanitizer_reported", log
            log.append(f"  {'✅' if st == 'ok' else '⏭'} sanitizer    {why}")
        else:
            log.append("  ⏭ sanitizer    已按 --no-sanitizer 跳过")
        return "confirm", log
    finally:
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
    a = ap.parse_args(argv)

    cards = [Path(c) if Path(c).is_absolute() else ROOT / c for c in a.card] or find_cards()
    if not cards:
        print("[replay] 未找到证据卡（evidence/**/EV-*.md）")
        return 0

    n_ok = n_bad = 0
    for card in cards:
        verdict, log = replay_card(card, do_sanitizer=not a.no_sanitizer,
                                   keep_tmp=a.keep_tmp)
        ok = verdict == "confirm"
        n_ok += ok
        n_bad += not ok
        print("\n".join(log))
        print(f"  → {verdict}\n")
    print(f"[replay] confirm={n_ok} refute={n_bad} 共 {len(cards)} 张卡")
    return 1 if (a.check and n_bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
