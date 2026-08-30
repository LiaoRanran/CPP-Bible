#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""wave_intake_check.py — Wave 收口复验（报告型，不入 CI 门禁）

为什么需要这个轮子
==================
Wave 5/6 派发子 agent 写 D5 附录 + 基准源文件时，反复出现"子 agent 自称编译通过，
实则本机复验失败"的事故（ch72 `Vec et(4)` 无匹配构造、ch86 漏 `#include <stack>`、
ch42 unused param 警告、GCC 版本不一致等）。教训写进 MEMORY.md：
  **"子 agent 自称编译通过不可信，必须本机复验。"**

本工具是 Wave 收口的**验收闸门**：给定一批章 md + 基准 cpp（或 --auto 从 git status
自动取 Wave 工作树改动），做三件事：
  1. 围栏偶数校验：md 内 ``` 围栏必须成对（正则 `^\s*``` `，允许缩进围栏，避开 ch87 式
     ODD_FENCE 误报）。孤儿围栏会让 consistency / 渲染崩。
  2. LF / BOM 检查：源码必须 LF 行尾、无 BOM（Windows 编辑器常见污染）。
  3. 本机 g++ 真编译：对 md 内"含 int main 的 cpp demo"与基准 cpp 文件，用本机
     `g++ -O2 -std=c++23`（涉线程自动加 -pthread）真实编译，复验"编译通过"声称。

  豁免意识（避免假阳性）
  ======================
  本闸门会对照 tools/compile_exempt.json：命中（章文件名, 1-based 块序）的 demo 只报
  [WAIVED] 而不计入 fails。原因：CI 的 compile_gate 本就对 CROSS_BLOCK（符号在前序块
  定义，顺读可编）等块放行；若本闸门把它们当 FAIL，会制造假阳性、阻碍合法提交。未命中
  豁免却又编译失败的 demo 才是真正须修的新缺陷。

设计约束（对齐 AGENT.md 红线）
==============================
- 只读 + 临时编译（写到 build/_wave_intake/，结束清理），不污染源码树。
- 绝不修改源文件；只报问题。
- g++ 路径优先本机 MinGW GCC 15.3.0，回退 PATH 的 g++。

用法
====
  python3 tools/wave_intake_check.py --auto
      # 自动取 git status 中 Wave 工作树改动（M 的 ch*.md + ?? 的 _bench_d5_*.cpp）
  python3 tools/wave_intake_check.py Book/partXX/chNN.md _bench_d5_nn.cpp
  python3 tools/wave_intake_check.py --auto --no-compile   # 只做围栏/LF/BOM
"""
import re
import sys
import shutil
import subprocess
import argparse
import tempfile
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / 'Book'

# 围栏：允许前导空格 + 可选语言标识；开/闭都匹配；必须偶数
FENCE_RE = re.compile(r'^\s*```(?:[a-zA-Z][\w-]*)?$')
BOM = b'\xef\xbb\xbf'


def find_gpp():
    cand = r'C:/Qt/Tools/mingw1530_64/bin/g++.EXE'
    if Path(cand).exists():
        return cand
    # 回退 PATH
    for name in ('g++.exe', 'g++'):
        loc = shutil.which(name)
        if loc:
            return loc
    return None


GPP = find_gpp()


def load_exempt():
    """读取 tools/compile_exempt.json，返回 set[(章文件名, 1-based 块序)]。

    CI 的 compile_gate 已对 CROSS_BLOCK / MULTI_FILE 等"隔离审计看不到、但顺读可编"
    的块放行。本闸门若也把它们报成 FAIL，会制造假阳性、阻碍合法提交。因此命中豁免
    列表的块只报 [WAIVED]，不计入 fails。
    """
    p = ROOT / 'tools' / 'compile_exempt.json'
    s = set()
    if not p.exists():
        return s
    try:
        d = json.load(open(p, encoding='utf-8'))
    except Exception:
        return s
    for e in d.get('exempt', []):
        f = e.get('file')
        b = e.get('block')
        if f and isinstance(b, int):
            s.add((f, b))
    return s


def cpp_block_index(text, fence_line_1based):
    """给定 ```cpp 围栏的 1-based 行号，返回它在文件中按出现顺序的 1-based 序号。

    与 compile_exempt.json 的 block 字段对齐（1-based）。
    """
    cnt = 0
    for idx, l in enumerate(text.split('\n'), 1):
        if idx > fence_line_1based:
            break
        if FENCE_RE.match(l) and l.strip().lstrip('`').strip().startswith('cpp'):
            cnt += 1
    return cnt


EXEMPT = load_exempt()


def fence_even_ok(text):
    cnt = sum(1 for l in text.split('\n') if FENCE_RE.match(l))
    return cnt % 2 == 0, cnt


def text_health(path: Path):
    """返回 (bom, crlf, fence_even, fence_count, err)。"""
    raw = path.read_bytes()
    bom = raw.startswith(BOM)
    text = raw.decode('utf-8', errors='replace')
    crlf = '\r\n' in text
    even, fc = fence_even_ok(text)
    return bom, crlf, even, fc, None


def extract_cpp_demos(text):
    """提取 md 内所有 ```cpp 块内容；返回 list[(fence_line_1based, code)]。

    fence_line_1based 是开围栏 ```cpp 的 1-based 行号，用于对齐 compile_exempt.json
    的 1-based 块序。
    """
    lines = text.split('\n')
    demos = []
    i = 0
    n = len(lines)
    while i < n:
        m = FENCE_RE.match(lines[i])
        if m and lines[i].strip().lstrip('`').strip().startswith('cpp'):
            fence_line = i + 1
            buf = []
            j = i + 1
            while j < n and not FENCE_RE.match(lines[j]):
                buf.append(lines[j])
                j += 1
            demos.append((fence_line, '\n'.join(buf)))
            i = j + 1
        else:
            i += 1
    return demos


def compile_cpp(code: str, with_pthread: bool, tmpdir: Path):
    """编译一段 cpp 源码；返回 (ok, stderr_short)。"""
    if GPP is None:
        return False, 'NO_GPP: 本机未找到 g++'
    src = tmpdir / 'demo.cpp'
    src.write_text(code, encoding='utf-8')
    cmd = [GPP, '-O2', '-std=c++23', '-c', str(src), '-o', str(tmpdir / 'demo.o')]
    if with_pthread:
        cmd.insert(-2, '-pthread')
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode == 0:
        return True, ''
    return False, (r.stderr or r.stdout).strip().splitlines()[-3:]


def auto_discover():
    """从 git status --porcelain 取 Wave 工作树改动。"""
    out = subprocess.run(
        ['git', '-C', str(ROOT), 'status', '--porcelain'],
        capture_output=True, text=True, timeout=30).stdout
    mds, cpps = [], []
    for line in out.splitlines():
        if len(line) < 4:
            continue
        st, path = line[:2], line[3:].strip()
        if path.startswith('Book/') and 'ch' in path and path.endswith('.md') and st != '??':
            mds.append(path)
        if '_bench_d5_' in path and path.endswith('.cpp') and st == '??':
            cpps.append(path)
    return mds, cpps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*', help='显式指定 md / cpp 文件')
    ap.add_argument('--auto', action='store_true', help='从 git status 自动取 Wave 改动')
    ap.add_argument('--no-compile', action='store_true', help='跳过 g++ 编译复验')
    args = ap.parse_args()

    mds, cpps = [], []
    for f in args.files:
        p = Path(f)
        if p.suffix == '.md':
            mds.append(f)
        elif p.suffix == '.cpp':
            cpps.append(f)
    if args.auto:
        a_mds, a_cpps = auto_discover()
        mds += a_mds
        cpps += a_cpps
    mds = sorted(set(mds))
    cpps = sorted(set(cpps))

    if not mds and not cpps:
        print('无输入文件。用 --auto 或显式指定 md/cpp。')
        return

    print("=" * 72)
    print(f"Wave 收口复验  —  md {len(mds)} 个, cpp {len(cpps)} 个"
          f"  g++={'YES' if GPP else 'NO'}")
    print("=" * 72)

    fails = 0
    waived_total = 0
    tmp_root = ROOT / 'build' / '_wave_intake'
    tmp_root.mkdir(parents=True, exist_ok=True)

    # ---- md 检查 ----
    for rel in mds:
        p = ROOT / rel if not Path(rel).is_absolute() else Path(rel)
        if not p.exists():
            print(f"  [SKIP] {rel} 不存在")
            continue
        print(f"\n### md: {rel}")
        bom, crlf, even, fc, _ = text_health(p)
        if not even:
            print(f"  [FAIL] 围栏奇数 ({fc} 个 ```，须成对) — ODD_FENCE 风险")
            fails += 1
        else:
            print(f"  [OK]   围栏偶数 ({fc})")
        if bom:
            print("  [FAIL] BOM 存在（须无 BOM UTF-8）")
            fails += 1
        else:
            print("  [OK]   无 BOM")
        if crlf:
            print("  [FAIL] CRLF 行尾（须 LF）")
            fails += 1
        else:
            print("  [OK]   LF 行尾")
        if args.no_compile or GPP is None:
            continue
        # 提取含 int main 的 cpp demo 编译复验
        text = p.read_text(encoding='utf-8')
        demos = extract_cpp_demos(text)
        compiled = 0
        waived = 0
        for fence_line, code in demos:
            if 'int main' not in code:
                continue
            compiled += 1
            with_pthread = ('<thread>' in code or 'std::thread' in code
                            or '#include <pthread' in code or 'pthread_' in code)
            # 命中 compile_exempt.json（CROSS_BLOCK 等）：CI 已放行，不计入 fails
            bidx = cpp_block_index(text, fence_line)
            if (Path(rel).name, bidx) in EXEMPT:
                print(f"  [WAIVED] L{fence_line} demo 命中 compile_exempt.json "
                      f"block#{bidx}（跨块依赖，CI 已放行）")
                waived += 1
                waived_total += 1
                continue
            d = tempfile.mkdtemp(dir=str(tmp_root))
            ok, err = compile_cpp(code, with_pthread, Path(d))
            shutil.rmtree(d, ignore_errors=True)
            if ok:
                print(f"  [OK]   L{fence_line} demo 编译通过"
                      + (" (+pthread)" if with_pthread else ""))
            else:
                print(f"  [FAIL] L{fence_line} demo 编译失败:")
                for e in err:
                    print(f"          {e}")
                fails += 1
        if compiled == 0:
            print("  [INFO] 无含 int main 的 cpp demo 可编译复验")
        elif waived:
            print(f"  [INFO] {waived} 个 demo 命中豁免（不计入失败）")

    # ---- cpp 基准源文件检查 ----
    for rel in cpps:
        p = ROOT / rel if not Path(rel).is_absolute() else Path(rel)
        if not p.exists():
            print(f"\n### cpp: {rel}\n  [SKIP] 不存在")
            continue
        print(f"\n### cpp: {rel}")
        bom, crlf, even, fc, _ = text_health(p)
        if bom:
            print("  [FAIL] BOM 存在"); fails += 1
        else:
            print("  [OK]   无 BOM")
        if crlf:
            print("  [FAIL] CRLF 行尾"); fails += 1
        else:
            print("  [OK]   LF 行尾")
        if args.no_compile or GPP is None:
            continue
        code = p.read_text(encoding='utf-8')
        with_pthread = ('<thread>' in code or 'std::thread' in code
                        or '#include <pthread' in code or 'pthread_' in code)
        d = tempfile.mkdtemp(dir=str(tmp_root))
        ok, err = compile_cpp(code, with_pthread, Path(d))
        shutil.rmtree(d, ignore_errors=True)
        if ok:
            print("  [OK]   编译通过" + (" (+pthread)" if with_pthread else ""))
        else:
            print("  [FAIL] 编译失败:")
            for e in err:
                print(f"          {e}")
            fails += 1

    # 清理临时目录
    shutil.rmtree(tmp_root, ignore_errors=True)

    print("\n" + "=" * 72)
    if fails == 0:
        print(f"复验通过 ✅  0 失败（md {len(mds)}, cpp {len(cpps)}"
              + (f"，{waived_total} 个命中豁免" if waived_total else "") + "）")
    else:
        print(f"复验失败 ❌  {fails} 项须修（md {len(mds)}, cpp {len(cpps)}"
              + (f"，{waived_total} 个命中豁免" if waived_total else "") + "）")
    print("=" * 72)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
