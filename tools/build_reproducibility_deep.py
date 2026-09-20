"""609 E2 · 编译可复现性深化：**跨时间窗口 12 宏 + 符号表 4 参数 + 段一致性 4 参数 + diff 替代品**。

603 已经做了"同机同日两次编译产物一致"；本工具把口径**加深一层**（仍**不改** replay 本体）：

  1. **跨时间窗口 12 宏**：把 12 个"会随环境/时间变"的预定义宏逐条列出，
     标注它属于 `time`（时间）/ `path`（路径）/ `counter`（序号）/ `env`（工具链）哪一类，
     以及"跨窗口对比时必须先屏蔽还是可忽略"。**没有任何宏"看心情"**——每条都有归类与理由。
  2. **符号表 4 参数**：`nm` 的 4 个参数（`--defined-only` / `--extern-only` /
     `-P`（portable）/ `--no-demangle`）与"为什么必须这么取"。
  3. **段一致性 4 参数**：`objdump` 的 4 个参数（`-h` 段头 / `-s` 段内容 / `-j <段名>` 限定 /
     `--no-show-raw-insn` 反汇编稳定化）与"哪些段落必须逐字节比、哪些只比长度"。
  4. **diffoscope 替代品**：仓里不能引外部 diffoscope（依赖太重）⇒ 提供纯标准库的
     **逐字节差异定位**：首个差异偏移 + 两侧 sha256 + 十六进制上下文 + 差异字节数。

CLI：
    macros                   打印 12 宏矩阵
    symbols                  打印 nm 4 参数
    sections                 打印 objdump 4 参数
    diff A B [--context 16]  逐字节差异定位（exit 0 相同 / 1 有差异 / 2 文件缺失）
    report [--write]         完整方案 Markdown
    --check                  0 结构自洽（12/4/4 齐全且 diff 自检通过）/ 1 破
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "build_reproducibility_deep.md"

#: 12 个跨时间窗口需关注的预定义宏：(宏, 类别, 跨窗口是否必须屏蔽, 理由)
MACROS: tuple[tuple[str, str, bool, str], ...] = (
    ("__DATE__", "time", True, "编译日期字符串 ⇒ 隔天必然不同"),
    ("__TIME__", "time", True, "编译时刻字符串 ⇒ 秒级必然不同"),
    ("__TIMESTAMP__", "time", True, "源文件 mtime 字符串 ⇒ 触盘时间变即变"),
    ("__FILE__", "path", True, "内含路径 ⇒ 不同工作目录/前缀必不同"),
    ("__BASE_FILE__", "path", True, "主源文件名 ⇒ 同上"),
    ("__FILE_NAME__", "path", False, "只含文件名（无目录）⇒ 同仓同文件可复现"),
    ("__LINE__", "counter", False, "行号由源码决定 ⇒ 同源码同值"),
    ("__func__", "counter", False, "函数名由源码决定 ⇒ 同源码同值"),
    ("__INCLUDE_LEVEL__", "counter", False, "包含深度由源码结构决定"),
    ("__COUNTER__", "counter", False, "同 TU 内递增 ⇒ 同源码同展开顺序即同值"),
    ("__STDC_VERSION__", "env", True, "随标准版本/编译器变 ⇒ 跨工具链必不同"),
    ("__GNUC__", "env", True, "随 GCC 主版本变 ⇒ 换工具链必不同"),
)

#: nm 的 4 个参数：(参数, 作用, 为什么必须这么取)
NM_PARAMS: tuple[tuple[str, str, str], ...] = (
    ("--defined-only", "只列本 TU 定义的符号", "未定义符号（外部引用）随链接环境变 ⇒ 不比它"),
    ("--extern-only", "只列外部可见符号", "静态局部符号名可被优化器重命名 ⇒ 噪声源"),
    ("-P", "portable 输出格式（name type value）", "BSD/SysV 三种格式在同一平台都可能出现 ⇒ 必须钉格式"),
    ("--no-demangle", "**不做** C++ 名字还原", "demangle 结果随 libiberty 版本变 ⇒ 比 mangled 名更稳"),
)

#: objdump 的 4 个参数：(参数, 作用, 比对强度)
OBJDUMP_PARAMS: tuple[tuple[str, str, str], ...] = (
    ("-h", "只列段头（名/大小/对齐/标志）", "比**长度与对齐**：段内容可因时间戳变而头部不变"),
    ("-s", "倾印段内容（hex）", "比**逐字节**：对 .text/.rodata 等语义段使用"),
    ("-j <段名>", "限定单个段", "避免把 .comment/.note 等**工具版本印记**段卷进比对"),
    ("--no-show-raw-insn", "反汇编不带机器码", "避免反汇编器版本差异伪装成语义差异"),
)

#: 只比长度、不比逐字节的段（工具链会插版本串/时间戳）
LEN_ONLY_SECTIONS = (".comment", ".note.gnu.build-id", ".note.GNU-stack", ".debug_info")


def diff_bytes(a: Path | str, b: Path | str, context: int = 16) -> dict:
    """纯标准库的 diffoscope 替代品：首个差异偏移 + 双侧 sha256 + 差异字节数 + hex 上下文。"""
    pa, pb = Path(a), Path(b)
    for p in (pa, pb):
        if not p.is_file():
            raise SystemExit(f"[e2] 文件不存在：{p}")
    ra, rb = pa.read_bytes(), pb.read_bytes()
    ha, hb = hashlib.sha256(ra).hexdigest(), hashlib.sha256(rb).hexdigest()
    n = min(len(ra), len(rb))
    off = next((i for i in range(n) if ra[i] != rb[i]), None)
    if off is None:
        if len(ra) == len(rb):
            return {"identical": True, "sha256_a": ha, "sha256_b": hb, "size_a": len(ra),
                    "size_b": len(rb), "first_diff": None, "differing_bytes": 0}
        off = n                                        # 只在长度上分叉
    lo = max(0, off - context)
    return {"identical": False, "sha256_a": ha, "sha256_b": hb,
            "size_a": len(ra), "size_b": len(rb), "first_diff": off,
            "differing_bytes": sum(1 for i in range(n) if ra[i] != rb[i]) + abs(len(ra) - len(rb)),
            "context_a": ra[lo: off + context].hex(),
            "context_b": rb[lo: off + context].hex(),
            "at": f"0x{off:x}"}


def render_report() -> str:
    lines = [
        "# 编译可复现性深化（609 E2）", "",
        "口径定位：603 已锁「同机同日两次编译一致」；本工具把口径**加深一层**"
        "（跨时间窗口/跨工具链），仍**不改** replay 本体。", "",
        "## 一、跨时间窗口 12 宏（每条都有归类，不靠「看心情」）", "",
        "| 宏 | 类别 | 跨窗口必须屏蔽 | 理由 |", "|---|---|---|---|",
    ]
    for name, kind, mask, why in MACROS:
        lines.append(f"| `{name}` | {kind} | {'**是**' if mask else '否'} | {why} |")
    by_kind: dict[str, int] = {}
    for _n, kind, mask, _w in MACROS:
        if mask:
            by_kind[kind] = by_kind.get(kind, 0) + 1
    detail = " + ".join(f"{k} {v}" for k, v in sorted(by_kind.items()))
    lines += ["", f"- 必须屏蔽：**{sum(1 for m in MACROS if m[2])}/{len(MACROS)}**"
                  f"（{detail}）", "",
              "## 二、符号表口径（nm 4 参数）", ""]
    for p, what, why in NM_PARAMS:
        lines.append(f"- `nm {p}` —— {what}；{why}")
    lines += ["", "## 三、段一致性口径（objdump 4 参数）", ""]
    for p, what, why in OBJDUMP_PARAMS:
        lines.append(f"- `objdump {p}` —— {what}；{why}")
    lines += ["", f"- **只比长度**的段：{', '.join(f'`{x}`' for x in LEN_ONLY_SECTIONS)}"
                  "（工具链会插版本串/构建 id ⇒ 逐字节比必假红）", "",
              "## 四、diffoscope 替代品", "",
              "- 仓里不引 diffoscope（依赖重、要外部工具）⇒ 自带 `diff` 子命令：",
              "  首个差异偏移 + 双侧 sha256 + 差异字节数 + 两侧 hex 上下文；",
              "- 定位：**给失败现场用**（谁在哪个字节上变了），不给「全量二进制 diff」能力。", "",
              ]
    return "\n".join(lines) + "\n"


def check() -> list[str]:
    problems: list[str] = []
    if len(MACROS) != 12:
        problems.append(f"宏矩阵不是 12 条（= {len(MACROS)}）")
    if len(NM_PARAMS) != 4:
        problems.append(f"nm 参数不是 4 条（= {len(NM_PARAMS)}）")
    if len(OBJDUMP_PARAMS) != 4:
        problems.append(f"objdump 参数不是 4 条（= {len(OBJDUMP_PARAMS)}）")
    for name, kind, _m, why in MACROS:
        if kind not in ("time", "path", "counter", "env"):
            problems.append(f"{name} 类别非法：{kind}")
        if not why.strip():
            problems.append(f"{name} 缺理由")
    same = diff_bytes(__file__, __file__)
    if not same["identical"] or same["first_diff"] is not None:
        problems.append("diff 自检失败：同一文件应判 identical")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="build_reproducibility_deep",
                                 description="609 E2 编译可复现性深化（12 宏 + 4 nm + 4 objdump + diff 替代）")
    ap.add_argument("--version", action="version", version=f"build_reproducibility_deep {VERSION}")
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("macros")
    sub.add_parser("symbols")
    sub.add_parser("sections")
    sp = sub.add_parser("diff")
    sp.add_argument("a")
    sp.add_argument("b")
    sp.add_argument("--context", type=int, default=16)
    sp.add_argument("--json", action="store_true")
    sp = sub.add_parser("report")
    sp.add_argument("--write", action="store_true")
    sp.add_argument("--out", default=str(REPORT_OUT))
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print(f"[e2] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print(f"[e2] --check OK：12 宏（屏蔽 {sum(1 for m in MACROS if m[2])}）/4 nm/4 objdump "
              f"齐全，diff 自检通过")
        return 0

    if a.cmd == "macros":
        for name, kind, mask, why in MACROS:
            print(f"{name:<22} {kind:<8} 屏蔽={'是' if mask else '否'}  {why}")
        return 0
    if a.cmd == "symbols":
        for p, what, why in NM_PARAMS:
            print(f"nm {p:<18} {what} —— {why}")
        return 0
    if a.cmd == "sections":
        for p, what, why in OBJDUMP_PARAMS:
            print(f"objdump {p:<20} {what} —— {why}")
        print(f"只比长度的段：{', '.join(LEN_ONLY_SECTIONS)}")
        return 0
    if a.cmd == "diff":
        res = diff_bytes(a.a, a.b, a.context)
        if a.json:
            print(json.dumps(res, ensure_ascii=False, indent=1))
        if res["identical"]:
            print(f"[e2] ✓ 逐字节相同（sha256 {res['sha256_a'][:16]}… · {res['size_a']}B）")
            return 0
        print(f"[e2] ✗ 首个差异 @ {res['at']}（偏移 {res['first_diff']}）· "
              f"差异字节 {res['differing_bytes']} · 大小 {res['size_a']} vs {res['size_b']}")
        print(f"  A: {res['context_a']}")
        print(f"  B: {res['context_b']}")
        return 1

    if a.cmd == "report":
        text = render_report()
        if a.write:
            p = Path(a.out)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8", newline="\n")
            print(f"[e2] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}")
            return 0
        print(text)
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
