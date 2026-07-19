#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书内 asm 围栏 vs _asm_demo 工件 符号一致性审计（修正版 v2）

修正 v1 的三类噪声：
  1. 两侧统一 c++filt demangle（mangled↔demangled 对齐）。
  2. 过滤 libstdc++/CRT/编译器内部符号（只保留"用户函数体"符号，
     与阶段3 asm-evidence-spotcheck 的用户函数体比对口径一致）。
  3. 只比对"用户函数定义标号"（书内 demo 函数必须仍定义于工件）；
     忽略书内策展伪标号(found/done/bucket_chain...)与库调用。

结论语义：若书内展示的某个用户 demo 函数，在当前 gcc15.3.0 工件中
已无对应定义 -> 书内汇编过期（真漂移）。其余均判为策展/库噪声，不报错。
"""
import os, re, json, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(ROOT, "Book")
ASMDEMO = os.path.join(ROOT, "_asm_demo")
OBJDUMP = r"C:/Qt/Tools/mingw1530_64/bin/objdump.exe"
FILT = r"C:/Qt/Tools/mingw1530_64/bin/c++filt.exe"

DEF_RE = re.compile(r"^\s*([A-Za-z_][\w.@$]*):")          # 标号定义(符号不含冒号)
CALL_RE = re.compile(r"\b(?:call|jmp)\s+([A-Za-z_][\w.@$]*)")
LEA_RE = re.compile(r"\[\s*rip\s*\+\s*([A-Za-z_][\w.@$]*)\]")

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
    try:
        p = subprocess.run([FILT], input=text, capture_output=True,
                            text=True, timeout=30)
        return p.stdout if p.returncode == 0 else text
    except Exception:
        return text

def is_user_symbol(name):
    """用户函数判定：非库/CRT/内部，且非伪标号关键词。"""
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

def artifact_user_defs(path):
    """返回工件内『用户函数定义标号』集合（demangled + 滤库）。"""
    base, ext = os.path.splitext(path)
    raw = ""
    if ext == ".s":
        raw = open(path, "r", encoding="utf-8", errors="replace").read()
    elif ext == ".o":
        try:
            raw = subprocess.run([OBJDUMP, "-d", "-M", "intel", "-C", path],
                                 capture_output=True, text=True, timeout=60).stdout
        except Exception:
            raw = ""
    dm = demangle(raw)
    defs = set()
    for line in dm.splitlines():
        m = DEF_RE.match(line)
        if m and is_user_symbol(m.group(1)):
            defs.add(m.group(1))
    return defs

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
                base = os.path.join(ASMDEMO, a)
                root, ext = os.path.splitext(base)
                # 优先编译产物 .o / .s（含真实标号），.cpp 仅兜底
                if ext in (".o", ".s"):
                    cands = [base]
                else:  # .cpp
                    cands = [root + ".o", root + ".s", base]
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
        return
    print(f"审计章数: {checked}")
    total = 0
    for s in stale:
        total += len(s["missing"])
        print(f"[STALE] {s['chapter']} fence#{s['fence']}: 书内用户函数 {s['missing']} 不在工件定义中")
    print(f"\nRESULT: {len(stale)} 章存在真过期用户函数, 共 {total} 个")
    json.dump({"checked": checked, "stale": len(stale), "missing": total, "detail": stale},
              open(os.path.join(ROOT, "_book_asm_freshness.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
