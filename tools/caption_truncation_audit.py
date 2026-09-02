"""示例标题截断审计与修复：检测并重建 `> **示例 N** ... · TAG` 行的生成期截断污染。

污染特征（生成器按字节预算在标题中部硬切）：
  1. 未闭合括号：TAG 中 [ 或 （ 未闭合
  2. 断词：TAG 以技术词的前缀结尾（如 allocatortrai / stdca / Learni）
  3. 悬挂标点：以 / 、· ： + 等连接符结尾

修复策略：截断标签若是同章某小节标题的（规范化）子串，则用标题自锚点起的
剩余文本补全。置信度分级：
  HIGH——标签即标题开头（去章节序号后）
  MED ——标签锚定在章节序号（①⑩ N. 等）之后
  LOW ——标签锚定在标题中部（截断可能连开头一起切掉），
        修复用去章节序号后的完整标题

用法：
  python tools/caption_truncation_audit.py             # 审计报告
  python tools/caption_truncation_audit.py --fix       # 应用全部标题补全（幂等）
  python tools/caption_truncation_audit.py --fix high  # 只应用 HIGH 置信度
  python tools/caption_truncation_audit.py --check     # 门禁模式：存在确定性截断即退出 1
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "Book"
BUILD = ROOT / "build"

CAPTION_RE = re.compile(r"^> \*\*示例 \d+\*\* <span class=\"badge badge-exp\">难度")
SPLIT = "</span> · "

SECTION_MARKERS = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳.0123456789、"

KNOWN_PREFIX_TARGETS = [
    "allocator_traits", "polymorphic_allocator", "atomic_wait", "unsynchronized_pool_resource",
    "monotonic_buffer_resource", "scoped_allocator_adaptor", "memory_resource",
    "forward_like", "copy_elision", "initializer_list", "lock_guard", "scoped_lock",
    "shared_lock", "unique_lock", "lower_bound", "upper_bound", "push_heap", "pop_heap",
    "make_heap", "inclusive_scan", "exclusive_scan", "adjacent_find", "find_if",
    "search_n", "exchange_weak", "compare_exchange", "always_lock_free", "is_always_lock_free",
    "co_await", "co_yield", "co_return", "await_ready", "await_suspend", "unhandled_exception",
    "return_void", "return_value", "error_code", "error_category", "dynamic_cast",
    "static_cast", "unique_ptr", "shared_ptr", "weak_ptr", "destroying_delete",
    "polymorphic", "stdcall", "fastcall", "vectorcall", "thiscall", "cdecl",
    "override", "delete", "default", "constexpr", "consteval", "constinit",
    "concept", "concepts", "designated_initializers", "flat_map", "flat_set",
    "std::meta", "enumerators_of", "vcpkg", "brew", "pacman", "choco",
    "clang-format", "clang-tidy", "libclang", "LLVM", "GCC", "Clang", "MSVC",
    "Windows", "Linux", "macOS", "x86-64", "ARM64", "Learning", "Practical",
    "Effective", "Standard", "Sutter", "Stroustrup", "Meyers", "telescoping",
    "anti-patterns", "anti-pattern", "RocksDB", "LevelDB", "Abseil", "Chromium",
    "Eigen", "Unreal", "UObjectBase", "fmt", "upstream", "iostream", "printf",
    "GIMPLE", "SCCP", "GVN", "DCE", "LTO", "PGO", "ABI", "RCU", "urcu",
    "ASIO", "asio", "boost", "initializerlist", "allocatortype", "get_default",
    "set_default", "bad_alloc", "restrict", "assume_aligned", "hardware_interference_size",
    "assume", "alias", "alignof", "alignas", "allocator", "new",
    "MSBuild", "CMake", "find_package", "optiona", "optional", "variant",
    "any", "expected", "string_view", "span", "subspan", "emplace", "mov",
    "swap", "exchange", "invoke", "function", "bind", "lamb", "lambda",
    "duration", "time_point", "clock", "vtable", "vbptr", "vbase", "offset",
    "thunk", "RVO", "NRVO", "Itanium", "zero-cost", "COW", "MOC", "signal",
    "slot", "GoF", "Factory", "Method", "Abstract", "Builder", "Policy",
    "tag", "dispatch", "SFINAE", "enable_if", "if_constexpr", "if constexpr",
    "modules", "import", "export", "pragma", "GCC15", "MS STL", "libc++",
    "libstdc++", "gnucxx", "cxx11", "seq_cst", "acquire", "release",
    "memory_order", "data race", "cache", "line", "padding", "SIMD", "SSE",
    "AVX", "NEON", "mm256", "flathashmap", "unordered",
    "atomic", "BigStruct", "benchmark", "profile", "gener", "std",
]


# 这些尾部片段本身是完整词（如 range-for 的 for），不判为断词
COMPLETE_FRAGMENTS = {"for"}


def tag_signals(tag: str) -> list[str]:
    reasons = []
    if "[" in tag and tag.count("[") > tag.count("]"):
        reasons.append("未闭合[")
    if "（" in tag and tag.count("（") > tag.count("）"):
        reasons.append("未闭合（")
    if re.search(r"[/·：+、]$", tag):
        reasons.append("悬挂标点")
    m = re.search(r"([A-Za-z_:./<>-]+)$", tag)
    if m and m.group(1) not in COMPLETE_FRAGMENTS:
        frag = m.group(1)
        for target in KNOWN_PREFIX_TARGETS:
            if frag != target and target.startswith(frag) and len(frag) >= 2:
                reasons.append(f"断词→{target}")
                break
    return reasons


def _norm_indexed(s: str) -> tuple[str, list[int]]:
    """规范化（去空白/强调符+小写），同时保留每个保留字符在原串的下标。"""
    chars, idxs = [], []
    for i, ch in enumerate(s):
        if ch in " \t`*_\\":
            continue
        chars.append(ch.lower())
        idxs.append(i)
    return "".join(chars), idxs


def _after_section_marker(heading: str) -> int:
    """返回去掉前导章节序号（⑫ / 2.5 / 一、 等）后的起始下标。"""
    m = re.match(r"^[①-⑳0-9.、]+\s*", heading)
    return m.end() if m else 0


def repair_from_heading(tag: str, heading: str) -> tuple[str, str] | None:
    """返回 (补全文本, 置信度)；无法从标题补全则 None。"""
    nh, hidx = _norm_indexed(heading)
    nt, _ = _norm_indexed(tag)
    if not nt or len(nh) <= len(nt):
        return None
    if nh.startswith(nt):
        conf = "HIGH"
        anchor = hidx[0] if hidx else 0
    else:
        idx = nh.find(nt)
        if idx < 0:
            return None
        before = nh[idx - 1] if idx > 0 else ""
        anchor = hidx[idx]
        if idx == 0 or before in SECTION_MARKERS:
            conf = "MED"
        else:
            # LOW：锚点位于标题中部，说明截断可能连开头一起切掉，
            # 修复用去章节序号的完整标题，避免丢前缀。
            conf = "LOW"
            anchor = _after_section_marker(heading)
    while anchor > 0 and heading[anchor - 1] in "`:":
        anchor -= 1
    repair = heading[anchor:].strip()
    prev = None
    while prev != repair:
        prev = repair
        repair = re.sub(r"\s*<span class=\"badge[^>]*>[^<]*</span>\s*$", "", repair)
    repair = re.sub(r"\s*\{#[^}]*\}\s*$", "", repair)
    if not repair:
        return None
    rnorm, _ = _norm_indexed(repair)
    if rnorm == nt:
        return None
    return repair, conf


BADGE_CITATIONS = {"标准": "[标准]", "经验": "[经验]"}
BADGE_RE = re.compile(r"<span class=\"badge[^\"]*\">([^<]*)</span>")
TRAILING_BRACKET_RE = re.compile(r"\s*\[[^\]]*$")
IMPL_CITATION_RE = re.compile(r"\[实现·[^\]]+\]")


def _file_impl_citation(lines: list[str]) -> str:
    """章节内出现最多的完整 [实现·XXX] 引注，作为实现徽章的限定词投票。"""
    counts: dict[str, int] = {}
    for ln in lines:
        for c in IMPL_CITATION_RE.findall(ln):
            counts[c] = counts.get(c, 0) + 1
    if not counts:
        return ""
    return max(counts, key=counts.get)


def bracket_repair(tag: str, headings: list[tuple[int, str]], impl_citation: str):
    """引注截断修复：剥掉尾部不完整 [xxx 碎片后按标题匹配，
    方括号引注由标题徽章推导（实现徽章取章节多数投票的限定词）。
    返回 (补全文本, 置信度, 标题) 或 None。"""
    m = TRAILING_BRACKET_RE.search(tag)
    if not m:
        return None
    base = tag[: m.start()].strip()
    nt, _ = _norm_indexed(base)
    if not nt:
        return None
    for _, h in headings:
        badges = BADGE_RE.findall(h)
        if not badges:
            continue
        h_text = BADGE_RE.sub("", h).strip()
        citation = ""
        for b in badges:
            if b in BADGE_CITATIONS:
                citation = BADGE_CITATIONS[b]
                break
            if b == "实现" and impl_citation:
                citation = impl_citation
                break
        if not citation:
            continue
        nh, hidx = _norm_indexed(h_text)
        idx = nh.find(nt)
        if idx < 0:
            continue
        if idx == 0:
            conf, anchor = "HIGH", (hidx[0] if hidx else 0)
        elif nh[idx - 1] in SECTION_MARKERS:
            conf, anchor = "MED", hidx[idx]
        else:
            conf, anchor = "LOW", _after_section_marker(h_text)
        while anchor > 0 and h_text[anchor - 1] in "`:":
            anchor -= 1
        repair = h_text[anchor:].strip()
        if not repair:
            continue
        return f"{repair} {citation}", conf, h
    return None


def scan_file(path: Path) -> list[dict]:
    hits = []
    lines = path.read_text(encoding="utf-8").split("\n")
    headings = [
        (i, ln.lstrip("#").strip()) for i, ln in enumerate(lines, 1) if ln.startswith("#")
    ]
    impl_citation = _file_impl_citation(lines)
    for i, ln in enumerate(lines, 1):
        if not CAPTION_RE.match(ln) or SPLIT not in ln:
            continue
        tag = ln.split(SPLIT, 1)[1]
        reasons = tag_signals(tag)
        if not reasons:
            continue
        # 最近标题优先：示例标题几乎总指向其所属小节，按距离排序、
        # 同距离时前向（上方）标题优先，避免误配同名远端标题。
        ordered = sorted(headings, key=lambda t: (abs(t[0] - i), t[0] > i))
        best = None
        for _, h in ordered:
            r = repair_from_heading(tag, h)
            if r:
                best = (r[0], r[1], h)
                break
        if best is None and "未闭合[" in reasons:
            best = bracket_repair(tag, ordered, impl_citation)
        hits.append({
            "loc": f"{path.relative_to(ROOT)}:{i}",
            "tag": tag,
            "reasons": reasons,
            "repair": best[0] if best else "",
            "confidence": best[1] if best else "",
            "heading": best[2] if best else "",
        })
    return hits


def apply_fixes(hits: list[dict], min_conf: str) -> int:
    """按 loc 分组重写文件；min_conf: 'high' 仅HIGH，'med' HIGH+MED，'low' 全部。保留各文件行尾。"""
    order = {"HIGH": 0, "MED": 1, "LOW": 2}
    threshold = order[min_conf.upper()]
    by_file: dict[Path, dict[int, str]] = {}
    for h in hits:
        if not h["repair"] or order[h["confidence"]] > threshold:
            continue
        fp, _, lineno = h["loc"].rpartition(":")
        by_file.setdefault(ROOT / fp, {})[int(lineno)] = h["repair"]

    applied = 0
    for fp, fixes in sorted(by_file.items()):
        raw = fp.read_bytes()
        crlf = b"\r\n" in raw
        eol = "\r\n" if crlf else "\n"
        lines = raw.decode("utf-8").replace("\r\n", "\n").split("\n")
        for lineno, repair in fixes.items():
            ln = lines[lineno - 1]
            if SPLIT not in ln:
                continue
            lines[lineno - 1] = ln.split(SPLIT, 1)[0] + SPLIT + repair
            applied += 1
        fp.write_bytes(eol.join(lines).encode("utf-8"))
    return applied


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="门禁模式：存在确定性截断则退出 1")
    parser.add_argument("--fix", nargs="?", const="low", choices=["high", "med", "low"],
                        help="应用标题补全修复（high=仅HIGH+MED，low=全部；幂等）")
    args = parser.parse_args()

    all_hits = []
    for p in sorted(BOOK.rglob("*.md")):
        all_hits.extend(scan_file(p))

    repairable = [h for h in all_hits if h["repair"]]
    print(f"确定性截断总数: {len(all_hits)}")
    for conf in ("HIGH", "MED", "LOW"):
        n = sum(1 for h in repairable if h["confidence"] == conf)
        print(f"  标题补全 {conf}: {n}")
    print(f"  需人工重建（无标题锚点）: {len(all_hits) - len(repairable)}")

    if args.fix:
        applied = apply_fixes(all_hits, args.fix)
        print(f"\n[FIX] 已应用 {applied} 处补全（min_conf={args.fix}）")

    BUILD.mkdir(exist_ok=True)
    manual = [h for h in all_hits if not h["repair"]]
    with open(BUILD / "caption_truncation_manual.txt", "w", encoding="utf-8") as f:
        for h in manual:
            f.write(f"{h['loc']} {'/'.join(h['reasons'])} |{h['tag']}|\n")
    print(f"人工重建清单 → build/caption_truncation_manual.txt（{len(manual)} 条）")

    if args.check and all_hits:
        print(f"\n[CHECK] 存在 {len(all_hits)} 处确定性截断，门禁不通过")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
