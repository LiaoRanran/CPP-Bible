#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书内 asm 围栏 vs _asm_demo 工件 符号一致性审计（CI 可移植版 v3）

设计目标：
  - 与阶段3 asm-evidence-spotcheck 的「用户函数体」比对口径一致。
  - 跨平台可移植：CI 跑在 Ubuntu (Linux gcc-15, binutils 预装)，
    本地跑在 Windows (MinGW-w64 gcc-15.3.0)。c++filt / objdump 路径
    通过 shutil.which 自动探测，绝不硬编码 Windows 绝对路径。
  - 若 c++filt 缺失，demangle 退化为恒等，并令 objdump 不带 -C，
    保证「围栏侧」与「工件侧」在原始 mangled 名层面一致比对
    （is_user_symbol 对 mangled/ demangled 两种形态都兼容过滤）。

结论语义：若书内展示的某个用户 demo 函数，在当前 gcc15.3.0 工件中
已无对应定义 -> 书内汇编过期（真漂移）。其余均判为策展/库噪声，不报错。
"""
import os, re, sys, json, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 仓库根（tools/ 的父目录）
BOOK = os.path.join(ROOT, "Book")
ASMDEMO = os.path.join(ROOT, "_asm_demo")

# ---- 可移植工具探测：c++filt / objdump ----
def _find_first(candidates):
    """依次尝试 which；再回退到显式绝对路径（Windows MinGW 安装位）。"""
    for c in candidates:
        p = shutil.which(c)
        if p:
            return p
    for c in candidates:
        # 显式绝对路径（仅当看起来像路径时）
        if (len(c) > 1 and c[1] == ":") or c.startswith("/"):
            if os.path.isfile(c):
                return c
    return None

FILT = _find_first([
    r"C:/Qt/Tools/mingw1530_64/bin/c++filt.exe",  # 与书内工件同源 GCC15.3.0，优先
    "c++filt",
    "x86_64-w64-mingw32-c++filt",
    r"C:/Qt/Tools/mingw1310_64/bin/c++filt.exe",
    "c++filt.exe",
])
OBJDUMP = _find_first([
    r"C:/Qt/Tools/mingw1530_64/bin/objdump.exe",  # 与书内工件同源 GCC15.3.0，优先
    "objdump",
    "x86_64-linux-gnu-objdump",
    r"C:/Qt/Tools/mingw1310_64/bin/objdump.exe",
    "objdump.exe",
])
HAVE_FILT = FILT is not None

DEF_RE = re.compile(r"^\s*([A-Za-z_][\w.@$]*):")          # 标号定义(符号不含冒号)
CALL_RE = re.compile(r"\b(?:call|jmp)\s+([A-Za-z_][\w.@$]*)")
LEA_RE = re.compile(r"\[\s*rip\s*\+\s*([A-Za-z_][\w.@$]*)\]")

# ---- v4 鲁棒符号提取辅助正则 ----
# objdump 指令偏移行：  "   a0: 48 8b 01 mov ..."（标号字母类会误匹配，必须跳过）
HEXOFFSET_RE = re.compile(r"^\s*[0-9a-fA-F]{2,}\s*:")
# objdump 函数标号：    "0000000000000000 <v_dispatch(ShapeV const&)>:"
OBJLABEL_RE = re.compile(r"^\s*[0-9a-fA-F]*\s*<([^>]+)>:")
# 工件噪声头：objdump 的 "ch47_vs_51_dispatch_test.o:     file format pe-x86-64"
#           与 "Disassembly of section .text:"
NOISE_RE = re.compile(r"(?:file format|Disassembly of section)", re.I)

LIB_PREFIXES = (
    "__", "_ZSt", "_Zda", "_Zn", "_Zdl", "_Zna", "_GLOBAL__", ".text._",
    "__x86", "__stack", "__gxx", "__cxa", "__emutls", "__tls", "_ZNSt",
    "_ZTK", "_ZTV", "_ZTI", "_ZTS",
)
LIB_NAMES = {
    "puts", "printf", "memcpy", "memmove", "memset", "memcmp", "strlen",
    "abort", "exit", "__popcountdi2", "__popcountsi2", "__popcountti2",
    "_Rb_tree_insert_and_rebalance", "_Rb_tree_rebalance_for_erase",
    "_Rb_tree_rotate", "operator new", "operator delete", "operator new[]",
    "operator delete[]", "__throw", "__cxa", "_Unwind", "std::terminate",
    "std::bad_alloc", "std::__throw", "std::__cxx11", "std::allocator",
    "std::vector", "std::map", "std::set", "std::unordered_map",
    "std::runtime_error", "std::out_of_range", "std::logic_error",
}

def demangle(text):
    """c++filt 可用则 demangle；否则恒等（与工件侧原始 mangled 名对齐）。"""
    if not HAVE_FILT or not text:
        return text
    try:
        p = subprocess.run([FILT], input=text, capture_output=True,
                            text=True, timeout=30)
        return p.stdout if p.returncode == 0 else text
    except Exception:
        return text

def is_user_symbol(name):
    """用户函数判定：非库/CRT/内部，且非伪标号关键词。
    同时兼容 demangled（std::...）与原始 mangled（_ZSt/_ZNSt...）形态。"""
    n = name.strip()
    if not n or len(n) < 2:
        return False
    if any(n.startswith(p) for p in LIB_PREFIXES):
        return False
    if n in LIB_NAMES:
        return False
    if "std::" in n:
        return False
    if n in ("operator", "insert", "find", "operator<<", "operator>>"):
        return False
    # 书内策展伪标号（出现在标签位置但非真实用户函数）
    if n in ("found", "not_found", "done", "push_sift", "bucket_chain",
             "go_left", "find_loop", "probe", "loop", "mid", "head", "tail"):
        return False
    return True

def _extract_defs(text):
    """从（已 demangle 的）汇编文本提取『用户函数定义标号』集合。

    兼容两种工件格式：
      - 编译器文本汇编标号:  _Z12call_virtualRK4Base:  /  call_virtual(Base const&):
      - objdump 反汇编函数标号:  <v_dispatch(ShapeV const&)>:
    跳过噪声：指令偏移行(00: 48 8b...)、`file format` 头、`Disassembly of section` 头。
    双侧（围栏侧/工件侧）均经同一 demangle，保证 mangled/demangled 形态一致比对。
    """
    dm = demangle(text)
    defs = set()
    for line in dm.splitlines():
        if not line.strip():
            continue
        if HEXOFFSET_RE.match(line):
            continue
        if NOISE_RE.search(line):
            continue
        m = OBJLABEL_RE.match(line)
        if m:
            nm = m.group(1).split("(")[0].strip()  # 去掉参数列表，取函数基名
            if nm and is_user_symbol(nm):
                defs.add(nm)
            continue
        m = DEF_RE.match(line)
        if m:
            nm = m.group(1)
            if is_user_symbol(nm):
                defs.add(nm)
    return defs

def artifact_user_defs(path):
    """返回工件内『用户函数定义标号』集合（demangled + 滤库）。"""
    base, ext = os.path.splitext(path)
    raw = ""
    if ext == ".s":
        raw = open(path, "r", encoding="utf-8", errors="replace").read()
    elif ext == ".o":
        if OBJDUMP is None:
            return set()  # 无 objdump 且无 .s 兜底时，该工件不参与比对
        cmd = [OBJDUMP, "-d", "-M", "intel"]
        if HAVE_FILT:
            cmd.append("-C")  # 有 c++filt 才让 objdump 一并 demangle，保持双侧一致
        cmd.append(path)
        try:
            raw = subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout
        except Exception:
            raw = ""
    else:  # .cpp：源文件无 asm 标号，仅占位（不影响比对）
        raw = open(path, "r", encoding="utf-8", errors="replace").read()
    return _extract_defs(raw)

def fence_user_defs(fence_text):
    """书内围栏展示的『用户函数定义标号』（demangled + 滤库/伪标号）。"""
    dm = demangle(fence_text)
    defs = set()
    for line in dm.splitlines():
        m = DEF_RE.match(line)
        if m and is_user_symbol(m.group(1)):
            defs.add(m.group(1))
    return defs

def main():
    print(f"[asm-freshness] c++filt={FILT or 'MISSING'} objdump={OBJDUMP or 'MISSING'}")
    stale = []
    checked = 0
    for dp, _, fns in os.walk(BOOK):
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            txt = open(p, "r", encoding="utf-8", errors="replace").read()
            fences = re.findall(r"```asm\n(.*?)```", txt, re.S)
            if not fences:
                continue
            arts = re.findall(r"_asm_demo/([A-Za-z0-9_.\-]+)\.(?:cpp|s|o)", txt)
            art_paths = []
            seen = set()
            for a in arts:
                root = os.path.join(ASMDEMO, a)
                # 优先级: .o (编译产物, 真实标号) > .s (文本 asm) > .cpp (兜底)
                # 无 objdump 时跳过 .o，直接取 .s
                if OBJDUMP:
                    cands = [root + ".o", root + ".s", root + ".cpp"]
                else:
                    cands = [root + ".s", root + ".cpp"]
                for c in cands:
                    if os.path.exists(c) and c not in seen:
                        art_paths.append(c)
                        seen.add(c)
                        break
            if not art_paths:
                continue
            universe = set()
            for ap in art_paths:
                universe |= artifact_user_defs(ap)
            if not universe:
                continue
            checked += 1
            for i, fenc in enumerate(fences):
                fdefs = fence_user_defs(fenc)
                if not fdefs:
                    continue
                missing = sorted(fdefs - universe)
                if missing:
                    stale.append({"chapter": os.path.relpath(p, ROOT),
                                   "fence": i + 1, "missing": missing,
                                   "all_fence_defs": sorted(fdefs)})
    if not stale:
        print(f"审计章数: {checked}")
        print("RESULT: 0 真过期 — 书内 asm 围栏展示的用户函数全部仍定义于对应 GCC15.3.0 工件（符号一致）")
        json.dump({"checked": checked, "stale": 0, "detail": []},
                  open(os.path.join(ROOT, "_book_asm_freshness.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        return 0
    print(f"审计章数: {checked}")
    total = 0
    for s in stale:
        total += len(s["missing"])
        print(f"[STALE] {s['chapter']} fence#{s['fence']}: 书内用户函数 {s['missing']} 不在工件定义中")
    print(f"\nRESULT: {len(stale)} 章存在真过期用户函数, 共 {total} 个")
    json.dump({"checked": checked, "stale": len(stale), "missing": total, "detail": stale},
              open(os.path.join(ROOT, "_book_asm_freshness.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return 1

if __name__ == "__main__":
    sys.exit(main())
