#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
书内 asm 围栏 vs _asm_demo 工件 符号一致性审计（CI 可移植版 v6）

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
# 编译器文本汇编(demangle 后)标号: "square(int):" / "v_dispatch(ShapeV const&) const:"
#   注意：g++ -S 文本标号经 c++filt 后形如 foo(args):，既不被 OBJLABEL_RE(<foo()>:)
#   也不被 DEF_RE(foo:) 匹配 -> 此前被静默漏提，导致纯 .s 证据章被门禁跳过。
#   允许尾饰 const/volatile/noexcept 与 [clone .cold]/[part] 标记，兼容成员函数/克隆体。
PAREN_RE = re.compile(
    r"^\s*([A-Za-z_][\w.@$]*)\s*\([^)]*\)"   # 函数名 + 参数列表
    r"(?:\s+[A-Za-z_][\w.@$]*)*"             # 尾饰: const / volatile / noexcept / final ...
    r"(?:\s*\[[^\]]*\])?"                     # 可选 [clone .cold] / [part .text] 标记
    r"\s*:"
)
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
            nm = m.group(1).split("(")[0].split("@")[0].strip()  # 去参数列表与 @plt/@section
            if nm and is_user_symbol(nm):
                defs.add(nm)
            continue
        m = PAREN_RE.match(line)
        if m:
            nm = m.group(1).split("@")[0].strip()  # 去 @plt 等 ELF 后缀
            if nm and is_user_symbol(nm):
                defs.add(nm)
            continue
        m = DEF_RE.match(line)
        if m:
            nm = m.group(1).split("@")[0].strip()
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
    """书内围栏展示的『用户函数定义标号』（demangled + 滤库/伪标号）。

    v4 起与工件侧共用 _extract_defs：既提取编译器文本汇编标号(_Z...: / foo():),
    也提取 objdump 反汇编函数标号(<make_short()>:)。修复前本函数仅用 DEF_RE，
    读不了 demangled 的 <foo()>: 形态，导致全书约半数 asm 围栏被静默跳过、
    fence 侧近乎空转（覆盖缺口）。对称化后双侧口径一致，比对才真正生效。
    """
    return _extract_defs(fence_text)

def main():
    """围栏—工件『局部绑定』审计（v6）。

    演进：
      v4  对称化围栏侧符号提取(复用 _extract_defs)。
      v5  整章 union -> 围栏局部绑定（消除示意性围栏与无关工件的假阳性比对）。
      v6  三处精炼：
           1) 符号提取补 PAREN_RE：捕获 g++ -S demangle 后的 foo(args): 标号，
              修复此前 32/72 跟踪 .s 工件标号静默漏提、纯 .s 证据章被门禁跳过的盲点；
           2) 小节窗口改为 Markdown 层级『外围祖先小节』区间
              [section_start, section_end)（section_end = 围栏后首个同级/更高级标题），
              修正子标题下围栏把父小节引言里的工件引用切掉、又把后续小节引用漏入的误绑定；
           3) 工件解析候选补 _gcc15.o/_gcc15.s 后缀（部分工件以此命名，否则回退 .cpp 占位误判）；
              真实函数判定排除 std 成员调用（前置 '.' '>'），并仅当用户函数真实存在于
              本章源码才判为漂移——纯教学标号移出范围，不误报。

    语义：仅当用户函数真实存在于本章某 _asm_demo 源码、且不在其绑定工件的 GCC15.3.0
    产物符号集中时，才报为真过期（真·函数消失/改名/被内联致标号缺失）。
    """
    print(f"[asm-freshness] c++filt={FILT or 'MISSING'} objdump={OBJDUMP or 'MISSING'}")
    stale = []
    checked = 0        # 真·绑定围栏所在小节数（已实际比对）
    oos = 0            # 示意性/out-of-scope 围栏数（无就近工件引用）
    illustrative = 0   # 教学标号(全章源码无对应函数)移出范围数
    FENCE_RE = re.compile(r"```asm\n(.*?)```", re.S)
    REF_RE = re.compile(r"_asm_demo/([A-Za-z0-9_.\-]+)\.(?:cpp|s|o)")
    HEAD_RE = re.compile(r"^(#{1,6})\s", re.M)
    SRC_FUNC_RE = re.compile(r"\b([A-Za-z_]\w*)\s*\(")
    SRC_STOP = set(LIB_NAMES) | {"if","for","while","switch","return","sizeof","decltype",
        "catch","template","typename","operator","std","void","int","char","bool","auto",
        "class","struct","public","private","protected","static","const","unsigned","long",
        "short","do","else","new","delete","throw","try","namespace","using","typedef",
        "constexpr","noinline","noexcept","inline","virtual","explicit","friend","mutable"}
    for dp, _, fns in os.walk(BOOK):
        for fn in fns:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(dp, fn)
            txt = open(p, "r", encoding="utf-8", errors="replace").read()
            fences = list(FENCE_RE.finditer(txt))
            if not fences:
                continue
            refs = list(REF_RE.finditer(txt))
            heads = [(m.start(), len(m.group(1))) for m in HEAD_RE.finditer(txt)]
            # 本章所有 _asm_demo 源码里的『真实函数名』集合：仅这些才可能是漂移对象
            chapter_real_funcs = set()
            for rm in refs:
                cpp = os.path.join(ASMDEMO, rm.group(1) + ".cpp")
                if os.path.exists(cpp):
                    src = open(cpp, encoding="utf-8", errors="replace").read()
                    for m in SRC_FUNC_RE.finditer(src):
                        nm = m.group(1)
                        if nm in SRC_STOP or not is_user_symbol(nm):
                            continue
                        # 仅当该名『非成员调用』(前置非 '.' '>') 才视为真实用户函数：
                        # 排除 fl.push_front(1) 这类 std 方法调用被误判为用户定义函数。
                        pre = src[m.start() - 1] if m.start() > 0 else ""
                        if pre in (".", ">"):
                            continue
                        chapter_real_funcs.add(nm)
            for i, fm in enumerate(fences):
                fenc = fm.group(1)
                fs = fm.start()
                # 外围祖先小节区间 [section_start, section_end)：
                #   section_start = 围栏之前最后一个『层级 <= 当前最小层级』的标题（最外层祖先）
                #   section_end   = 围栏之后第一个『层级 <= 小节层级』的标题
                # 避免子标题下的围栏把父小节引言里的工件引用切掉、又把后续小节的引用漏进来。
                section_start = 0
                min_lv = 99
                for hp, hlv in heads:
                    if hp >= fs:
                        break
                    if hlv <= min_lv:
                        section_start = hp
                        min_lv = hlv
                sec_lv = next((hlv for hp, hlv in heads if hp == section_start), 99)
                section_end = len(txt)
                for hp, hlv in heads:
                    if hp > fs and hlv <= sec_lv:
                        section_end = hp
                        break
                ctx_lo, ctx_hi = section_start, section_end
                # 就近工件引用（仅本小节内）
                local_arts = []
                seen = set()
                for rm in refs:
                    if ctx_lo <= rm.start() < ctx_hi:
                        a = rm.group(1)
                        if a in seen:
                            continue
                        seen.add(a)
                        local_arts.append(a)
                if not local_arts:
                    oos += 1
                    continue
                universe = set()
                for a in local_arts:
                    root = os.path.join(ASMDEMO, a)
                    # 优先级: .o > .s > _gcc15.o > _gcc15.s > .cpp
                    # 部分工件以 _gcc15.s/.o 命名(重生成留痕), 须纳入解析否则回退 .cpp 占位致误判
                    cands = [root + ".o", root + ".s", root + "_gcc15.o",
                             root + "_gcc15.s", root + ".cpp"] if OBJDUMP \
                            else [root + ".s", root + "_gcc15.s", root + ".cpp"]
                    for c in cands:
                        if os.path.exists(c):
                            universe |= artifact_user_defs(c)
                            break
                if not universe:
                    continue
                checked += 1
                fdefs = fence_user_defs(fenc)
                if not fdefs:
                    continue
                missing = sorted(fdefs - universe)
                if missing:
                    # 仅当缺失符号『真实存在于本章某源码』才判为漂移（真·函数消失/改名）；
                    # 纯教学标号(全章源码均无该函数)属示意性, 移出范围, 不误报。
                    real_missing = [m for m in missing if m in chapter_real_funcs]
                    if real_missing:
                        stale.append({"chapter": os.path.relpath(p, ROOT),
                                       "fence": i + 1,
                                       "local_artifacts": local_arts,
                                       "missing": real_missing,
                                       "all_fence_defs": sorted(fdefs)})
                    else:
                        illustrative += 1
    if not stale:
        print(f"真·绑定围栏小节数(已比对): {checked}  示意性/out-of-scope 围栏: {oos}  教学标号移出: {illustrative}")
        print("RESULT: 0 真过期 — 所有『绑定工件』的真实用户函数均仍定义于对应 GCC15.3.0 工件")
        json.dump({"checked": checked, "out_of_scope": oos,
                   "illustrative_out_of_scope": illustrative, "stale": 0, "detail": []},
                  open(os.path.join(ROOT, "_book_asm_freshness.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        return 0
    print(f"真·绑定围栏小节数(已比对): {checked}  示意性/out-of-scope 围栏: {oos}  教学标号移出: {illustrative}")
    total = 0
    for s in stale:
        total += len(s["missing"])
        print(f"[STALE] {s['chapter']} fence#{s['fence']} (就近工件={s['local_artifacts']}): "
              f"真实用户函数 {s['missing']} 不在工件定义中")
    print(f"\nRESULT: {len(stale)} 处绑定围栏存在真过期用户函数, 共 {total} 个")
    json.dump({"checked": checked, "out_of_scope": oos,
               "illustrative_out_of_scope": illustrative, "stale": len(stale),
               "missing": total, "detail": stale},
              open(os.path.join(ROOT, "_book_asm_freshness.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return 1

if __name__ == "__main__":
    sys.exit(main())
