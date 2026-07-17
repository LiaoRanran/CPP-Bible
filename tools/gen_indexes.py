#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CPP-Bible 索引生成器 (gen_indexes.py)
====================================
一次生成三份导航索引，全部落在 Book/ 下、路径相对 Book/：

  1. Book/SUMMARY.md      — 147 章全链目录（按 part 分组，MkDocs/GitBook 风格）
  2. Book/GLOSSARY.md     — 术语 → 章节（关键词匹配真实章标题，0 匹配即丢弃，不臆造）
  3. Book/PREREQUISITES.md— 依赖建议（真实 `前置：` 元数据 + part 级阅读链）

设计原则（与全书红线一致）:
  - 章标题、路径、章号全部来自文件系统，确定性生成，可复跑。
  - GLOSSARY 只收录能匹配到真实章节的术语；宁缺毋滥。
  - PREREQUISITES 的逐章 `前置` 仅来自章内真实元数据；part 级链条明确标注为启发式建议。

用法:
  python3 tools/gen_indexes.py           # 生成三份索引
  python3 tools/gen_indexes.py --check   # 只校验是否与磁盘一致（CI 可用），不写文件
"""
import os, re, sys, argparse

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(HERE, "Book")

CHFILE = re.compile(r"ch(\d+)_")
# 章内元数据 `前置：...` （出现在 `> ...｜前置：xxx｜后续：...` 或 `/ 前置：xxx /`）
PRE_RE = re.compile(r"前置[：:]\s*([^｜|/]+)")
# 从前置文本里抽章号（兼容 `ch01（..）`、`⟶ Book/..chNN_..md`）
CHNUM  = re.compile(r"ch(\d+)")

PART_NAMES = {
    "part01_history":     "第一部分　历史与演进",
    "part02_toolchain":   "第二部分　工具链与构建",
    "part03_language":    "第三部分　语言核心",
    "part04_memory":      "第四部分　内存管理",
    "part05_oo":          "第五部分　面向对象",
    "part06_templates":   "第六部分　模板与泛型",
    "part07_stl":         "第七部分　标准模板库（STL）",
    "part08_algorithms":  "第八部分　算法",
    "part09_concurrency": "第九部分　并发与多线程",
    "part10_modern":      "第十部分　现代 C++ 特性",
    "part11_source":      "第十一部分　源码剖析",
    "part12_patterns":    "第十二部分　设计模式",
    "part13_engineering": "第十三部分　工程实践",
    "part14_perf":        "第十四部分　性能优化",
    "part15_cases":       "第十五部分　实战案例",
    "part16_reading":     "第十六部分　进阶阅读",
}

# 术语 → 匹配关键词（在“章标题 + 文件名 stem”里做子串/正则匹配）
# 仅当匹配到真实章节时才收录该术语，避免臆造。
GLOSSARY_TERMS = [
    ("RAII / 资源管理",        r"raii|资源|rule"),
    ("智能指针",               r"smart_pointer|智能指针|unique|shared|weak"),
    ("移动语义",               r"move|移动"),
    ("完美转发",               r"forward|转发"),
    ("拷贝省略 / RVO",         r"copy_elision|省略|rvo|nrvo"),
    ("引用与指针",             r"reference|pointer|引用|指针"),
    ("const / 常量性",         r"const|常量"),
    ("类型转换 (cast)",        r"cast|转换|转型"),
    ("初始化",                 r"initializ|初始化|init"),
    ("对象生命周期",           r"lifetime|生命周期|悬垂"),
    ("模板",                   r"template|模板"),
    ("变参模板",               r"variadic|变参|参数包"),
    ("模板元编程",             r"metaprog|元编程|sfinae|concept|约束"),
    ("虚函数 / 多态",          r"virtual|vtable|多态|polymorph"),
    ("继承",                   r"inherit|继承|derived|base"),
    ("异常安全",               r"exception|异常"),
    ("STL 容器",               r"vector|list|deque|map|set|unordered|array|容器|container"),
    ("迭代器",                 r"iterator|迭代器"),
    ("算法库",                 r"algo|算法|sort|find"),
    ("ranges / 视图",          r"ranges|range|视图|view"),
    ("lambda 表达式",          r"lambda|闭包|closure"),
    ("并发与线程",             r"thread|concurren|并发|线程"),
    ("原子操作 / 内存序",      r"atomic|memory_order|原子|内存序"),
    ("互斥与锁",               r"mutex|lock|锁|互斥"),
    ("协程",                   r"coroutine|协程|co_await"),
    ("编译期计算 / constexpr", r"constexpr|consteval|编译期|compile_time"),
    ("Concepts / 约束",        r"concept|约束|requires"),
    ("Modules 模块",           r"module|模块"),
    ("设计模式",               r"pattern|模式"),
    ("内存模型 / 布局",        r"memory|布局|layout|对齐|align|段"),
    ("性能优化 / 缓存",        r"perf|性能|cache|缓存|优化|优化"),
    ("未定义行为 (UB)",        r"\bub\b|未定义|undefined|aliasing|别名"),
    ("链接与编译",             r"link|compil|toolchain|编译|链接|odr"),
]


def load_chapters():
    """返回 {part: [(ch, stem, title, relpath)], ...}，part/章号有序。"""
    parts = {}
    for part in sorted(os.listdir(BOOK)):
        pdir = os.path.join(BOOK, part)
        if not os.path.isdir(pdir) or part.startswith("_"):
            continue
        rows = []
        for fn in sorted(os.listdir(pdir)):
            m = CHFILE.match(fn)
            if not fn.endswith(".md") or not m:
                continue
            ch = int(m.group(1))
            title = ""
            pre_raw = ""
            with open(os.path.join(pdir, fn), encoding="utf-8") as f:
                for line in f:
                    if not title and line.startswith("# "):
                        title = line[2:].strip()
                    if not pre_raw:
                        pm = PRE_RE.search(line)
                        if pm:
                            pre_raw = pm.group(1).strip()
                    if title and pre_raw:
                        break
            rows.append({"ch": ch, "stem": fn[:-3], "title": title,
                         "rel": f"{part}/{fn}", "pre": pre_raw})
        if rows:
            parts[part] = sorted(rows, key=lambda r: r["ch"])
    return parts


def clean_title(t):
    """去掉标题里可能的尾随 '（C++）' 之类噪声，保留主体。"""
    return t.strip()


def gen_summary(parts):
    out = ["# 目录（SUMMARY）", ""]
    out.append("> 本文件由 `tools/gen_indexes.py` 自动生成，请勿手改。")
    total = sum(len(v) for v in parts.values())
    out.append(f"> 全书 {len(parts)} 部分 / {total} 章。链接路径相对本目录（Book/）。")
    out.append("")
    for part, rows in parts.items():
        out.append(f"## {PART_NAMES.get(part, part)}")
        out.append("")
        for r in rows:
            out.append(f"- [{clean_title(r['title'])}]({r['rel']})")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def gen_glossary(parts):
    # 建 (ch, title, rel, haystack)
    idx = []
    for part, rows in parts.items():
        for r in rows:
            hay = (r["title"] + " " + r["stem"]).lower()
            idx.append((r["ch"], r["title"], r["rel"], hay))
    idx.sort()
    out = ["# 术语表（GLOSSARY）", ""]
    out.append("> 本文件由 `tools/gen_indexes.py` 自动生成，请勿手改。")
    out.append("> 术语 → 讲解该主题的章节。仅收录能匹配到真实章节的术语。")
    out.append("")
    kept = 0
    for term, kw in GLOSSARY_TERMS:
        pat = re.compile(kw, re.I)
        hits = [(ch, title, rel) for ch, title, rel, hay in idx if pat.search(hay)]
        if not hits:
            continue
        kept += 1
        links = "；".join(f"[ch{ch}]({rel})" for ch, title, rel in hits[:8])
        more = f" 等 {len(hits)} 章" if len(hits) > 8 else ""
        out.append(f"- **{term}**：{links}{more}")
    out.insert(4, f"> 共 {kept} 条术语。")
    out.append("")
    return "\n".join(out).rstrip() + "\n"


def gen_prerequisites(parts):
    out = ["# 前置依赖建议（PREREQUISITES）", ""]
    out.append("> 本文件由 `tools/gen_indexes.py` 自动生成，请勿手改。")
    out.append("")
    out.append("## 一、Part 级阅读链（启发式建议）")
    out.append("")
    out.append("> 按全书 part 编号的自然递进顺序，前序 part 是后续 part 的软前置；"
               "可按需跳读，非强制。")
    out.append("")
    order = list(parts.keys())
    for i, part in enumerate(order):
        name = PART_NAMES.get(part, part)
        if i == 0:
            out.append(f"- {name} —— 入口，无前置。")
        else:
            prev = PART_NAMES.get(order[i - 1], order[i - 1])
            out.append(f"- {name} —— 建议先读：{prev} 及之前各部分。")
    out.append("")
    out.append("## 二、逐章显式前置（来自各章真实元数据 `前置：`）")
    out.append("")
    out.append("> 下列条目直接摘自章内元数据，只列出确实声明了前置的章节。")
    out.append("")
    # 反查 ch → title/rel
    ch2meta = {}
    for part, rows in parts.items():
        for r in rows:
            ch2meta[r["ch"]] = r
    count = 0
    for part, rows in parts.items():
        for r in rows:
            if not r["pre"]:
                continue
            pres = sorted(set(int(x) for x in CHNUM.findall(r["pre"])))
            pres = [c for c in pres if c in ch2meta and c != r["ch"]]
            if not pres:
                continue
            count += 1
            links = "、".join(
                f"[ch{c}]({ch2meta[c]['rel']})" for c in pres)
            out.append(f"- [ch{r['ch']}]({r['rel']}) {clean_title(r['title'])}"
                       f"　←　前置：{links}")
    out.insert(2, f"> 共 {count} 章声明了显式前置依赖。")
    out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="只校验磁盘内容是否与生成结果一致，不写文件；不一致退出 1")
    args = ap.parse_args()

    parts = load_chapters()
    files = {
        "SUMMARY.md":       gen_summary(parts),
        "GLOSSARY.md":      gen_glossary(parts),
        "PREREQUISITES.md": gen_prerequisites(parts),
    }

    if args.check:
        stale = []
        for name, content in files.items():
            path = os.path.join(BOOK, name)
            cur = ""
            if os.path.isfile(path):
                cur = open(path, encoding="utf-8").read()
            if cur != content:
                stale.append(name)
        if stale:
            print("[FAIL] 索引与磁盘不一致，请重跑 gen_indexes.py：", stale)
            sys.exit(1)
        print("[PASS] 三份索引均与磁盘一致。")
        sys.exit(0)

    for name, content in files.items():
        path = os.path.join(BOOK, name)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        n = content.count("\n")
        print(f"写入 Book/{name}  ({n} 行)")
    print("完成。")


if __name__ == "__main__":
    main()
