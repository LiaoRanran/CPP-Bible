#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 ch151 验证过的论文级图表范式推广到其它有真实基准数字的 D5 附录章。

- 用 academic_chart.vertical_chart 生成竖向条形 SVG（与 ch151 图2 风格一致）。
- 在每章最后一个 `### D5.` 段之后注入 `## 基准数字可视化速读（本机 GCC 实测）` 段：
  引导引用块 + SVG + 图注 + 兜底数据表（满足三模式安全：SVG 不渲染时表即兜底）。
- 放置位置与 ch151 一致（独立 ## 段，不进入 ### D5.x，故不触发 D5 结构审计）。
- 落盘一律 LF（write_text newline="\n"），幂等（已注入则跳过）。
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from academic_chart import vertical_chart  # noqa: E402

ROOT = os.path.dirname(HERE)  # 仓库根

# ---- 各章数据 ----
# bars: (短标签, 值, 是否异常强调)
# ref:  (参考值, 参考线标签) 或 None
# intro / caption / table 为章节专属文本。
CHAPTERS = [
    {
        "path": "Book/part06_templates/ch60_template_basics.md",
        "title": "图 1　模板回调 vs std::function 分派开销（ms，越低越好）",
        "y_title": "耗时（ms）",
        "unit": "ms",
        "bars": [("模板回调", 5.79, False), ("std::function", 45.24, True)],
        "ref": None,
        "x_caption": "编译期单态化 vs 运行期类型擦除",
        "intro": "本章 D5 的立场是『编译期已知类型，就别付运行期间接代价』。下面把 D5.1 的基准画成图——重点不是绝对毫秒（随机器而变），而是 **std::function 慢多少×** 与 **慢在哪一层**。",
        "caption": "std::function 慢 ~7.8× 的代价来自**三重间接**：类型擦除封装、SBO 判定、函数指针间接调用；模板回调 `run_template<F>` 的 `F` 在编译期确定，`operator()` 被 `-O2` 完全内联，整个循环退化成 `add + lea`，零间接跳转。代价是**每种 `F` 实例化一份代码**（code bloat）——热路径排序比较器、数值积分核等编译期已知回调类型处，模板参数化可换 ~7.8× 加速；需运行期存储/替换异质回调（事件系统、回调队列）才用 std::function。颜色仅作区分，数值标签已写明。",
        "table_head": "| 策略 | 分派方式 | 耗时 (ms) | 相对 |",
        "table_sep":  "|------|----------|-----------|------|",
        "table_rows": [
            "| 模板 `run_template<F>` | 单态化 + 内联 | 5.79 | 1.00x (基线) |",
            "| `std::function<int(int)>` | 类型擦除 + 间接调用 | 45.24 | ~7.8x 慢 |",
        ],
    },
    {
        "path": "Book/part08_algorithms/ch97_search.md",
        "title": "图 1　查找容器：sorted vector / set / unordered_set（ms，越低越好）",
        "y_title": "耗时（ms）",
        "unit": "ms",
        "bars": [("sorted vector", 643.5, False), ("set", 2593.9, True), ("unordered_set", 154.4, False)],
        "ref": (154.4, "最快 154 ms"),
        "x_caption": "400 万键 / 200 万次查询全命中（mt19937 随机键）",
        "intro": "同为『找一个键』，三种容器的差距却是一个数量级。下面把 D5.1 的基准画成图——重点看 **离散节点查找的瓶颈在缓存，而非算法阶数**。",
        "caption": "同为 O(log N) 二分，`set` 比 `sorted vector` 慢 **4.03×**：红黑树每步是随机指针追逐（400 万节点 × 40+ 字节控制块，缓存命中率极低）；`sorted vector` 数据连续、末几步同 cache line，预取器能掩盖延迟。`unordered_set` 快在 **O(1) 桶直达**（约 77ns/查询，被内存延迟而非哈希主导）。工程决策：只查不改/批量建 → sorted vector；需有序遍历+频繁增删 → set；纯点查 → unordered_set。与 ch83「map vs unordered_map 22.5×」互证——离散节点查找瓶颈在缓存。颜色仅作区分，数值标签已写明。",
        "table_head": "| 场景 | 耗时 ms | 加速比 |",
        "table_sep":  "|---|---|---|",
        "table_rows": [
            "| sorted vector + `lower_bound` | 643.5 | 1.00×（基准） |",
            "| `set::find` | 2593.9 | 0.25×（比 lower_bound 慢 4.03×） |",
            "| `unordered_set::find` | 154.4 | 4.17×（比 lower_bound 快 4.17×，比 set 快 16.8×） |",
        ],
    },
    {
        "path": "Book/part06_templates/ch62_specialization.md",
        "title": "图 1　编译期路由 vs 运行期 if/else 链（ms，越低越好）",
        "y_title": "耗时（ms）",
        "unit": "ms",
        "bars": [("if constexpr", 14.19, False), ("if/else 链", 147.79, True)],
        "ref": None,
        "x_caption": "随机洗排 tag → 分支预测器无法学习",
        "intro": "ch61 量化了『间接调用 ~4.3×』，本章进一步量化『分支预测失败 ~10.4×』——两类运行期开销量级不同。下面把 D5.1 的基准画成图。",
        "caption": "if/else 链慢 ~10.4× 的最大单项是**分支预测失败（misprediction），不是间接调用**：随机洗排的 3 路 tag 令预测命中率约 33%，每次 misprediction 触发流水线冲刷（~15-20 周期）。`if constexpr` 在编译期消除所有分支，每个 batch 是单态化直线代码，零条件跳转。`10.4× > ch61 的 4.3×` 量化了『分支预测惩罚 >> 间接调用惩罚』——工程上消除不可预测分支的收益通常大于消除间接调用。tag 编译期已知用 if constexpr/特化；不可预测但操作集合封闭用 jump table（间接调用 4.3× 远好于分支失败 10.4×）。颜色仅作区分，数值标签已写明。",
        "table_head": "| 策略 | 分派方式 | 耗时 (ms) | 相对 |",
        "table_sep":  "|------|----------|-----------|------|",
        "table_rows": [
            "| `if constexpr` 编译期路由 | 单态化 + 无分支 | 14.19 | 1.00x (基线) |",
            "| 运行期 if/else 链 | 随机 tag → 高 misprediction | 147.79 | ~10.4x 慢 |",
        ],
    },
    {
        "path": "Book/part14_perf/ch158_perf_antipatterns.md",
        "title": "图 1　行优先 vs 列优先遍历（ms，越低越好）",
        "y_title": "耗时（ms）",
        "unit": "ms",
        "bars": [("行优先", 3.795, False), ("列优先", 41.152, True)],
        "ref": None,
        "x_caption": "同一份 64MB 数据，仅交换循环嵌套顺序",
        "intro": "『反模式』不是修辞，而是 10.84× 的真实代价。下面把 D5.1 的基准画成图——证明 **算法复杂度相同 ≠ 运行期相同**。",
        "caption": "列优先慢 **10.84×** 的根因：`int` 每行 4096×4 = 16 KB，远大于 64 B 缓存行；列优先每读一个元素就跳 16 KB 到下一行同列，几乎每次访存未命中 L1/L2，退化为内存带宽受限（本机 L3 仅 16 MB，64 MB 工作集早已溢出）。**『反模式』的定量定义就是 cache miss rate**——同一数据、同一套指令，仅交换循环嵌套顺序就差一个数量级。修复极廉价：写对 `for i for j`（行优先）即可，无需改数据结构。颜色仅作区分，数值标签已写明。",
        "table_head": "| 遍历顺序 | 耗时 (ms) | 相对 |",
        "table_sep":  "|----------|-----------|------|",
        "table_rows": [
            "| 行优先（顺序访问，缓存友好） | 3.795 | 1.00× (基线) |",
            "| 列优先（跨步访问，缓存失效反模式） | 41.152 | 10.84× 更慢 |",
        ],
    },
    {
        "path": "Book/part03_language/ch27_cast.md",
        "title": "图 1　static_cast vs dynamic_cast 下转开销（ms，越低越好）",
        "y_title": "耗时（ms）",
        "unit": "ms",
        "bars": [("static_cast", 11.02, False), ("dynamic_cast", 113.81, True)],
        "ref": None,
        "x_caption": "单继承链下转（工厂隐藏动态类型，阻止去虚化）",
        "intro": "dynamic_cast 的 ~10× 开销全部来自 RTTI 验证，不是虚调用本身。下面把 D5.1 的基准画成图——精确隔离出『运行期类型判别』的代价。",
        "caption": "两条路径执行相同的虚调用 `d->id()`，唯一差异是 `static_cast<D4*>`（编译期指针偏移，单继承链零偏移、零运行期指令）vs `dynamic_cast<D4*>`（运行期遍历 type_info 继承链比对）。**10.3× 的差距精确隔离了 RTTI 验证开销**——且 dynamic_cast 每次调用都付，随继承深度增长。选型：编译期已知下转用 static_cast（零开销，但以放弃安全检查换）；运行期才知下转首选 `std::variant`+`std::visit`，次选 dynamic_cast（移出热路径，一次性验证后缓存）。颜色仅作区分，数值标签已写明。",
        "table_head": "| 策略 | 分派方式 | 耗时 (ms) | 相对 |",
        "table_sep":  "|------|----------|-----------|------|",
        "table_rows": [
            "| `static_cast<D4*>` | 编译期指针偏移 | 11.02 | 1.00x (基线) |",
            "| `dynamic_cast<D4*>` | RTTI type_info 验证 | 113.81 | ~10.3x 慢 |",
        ],
    },
    {
        "path": "Book/part05_oo/ch45_oop_object_model.md",
        "title": "图 1　虚函数 vs CRTP 分派开销（ms，越低越好）",
        "y_title": "耗时（ms）",
        "unit": "ms",
        "bars": [("virtual", 43.88, True), ("CRTP", 4.94, False)],
        "ref": None,
        "x_caption": "运行期多态基线 vs 编译期单态化（noinline 工厂阻止去虚化）",
        "intro": "『虚函数一定慢』只在『类型对编译器不可见』时成立。下面把 D5.1 的基准画成图——CRTP 快 ~8.9× 的根源是消除两次间接。",
        "caption": "CRTP 快 ~8.9× 的根源是消除**两次间接**：vtable 取指（`mov rax,[rdi]`）+ 函数指针间接跳转（`call [rax+offset]`）；`static_cast<Derived const*>(this)->work_impl(x)` 在编译期单态化，`work_impl` 被 `-O2` 完全内联，零间接跳转。编译器**去虚化**会使差距缩小（本基准用 `[[gnu::noinline]]` 工厂隐藏动态类型，强制保留真正 vtable 间接）——这解释了生产代码虚函数实测开销方差大。**代价**是编译期耦合与晦涩模板报错；`final` 能在不牺牲可读性下帮助去虚化，是中间方案。颜色仅作区分，数值标签已写明。",
        "table_head": "| 策略 | 分派方式 | 耗时 (ms) | 相对 |",
        "table_sep":  "|------|----------|-----------|------|",
        "table_rows": [
            "| `virtual work()` | vtable 间接调用 | 43.88 | 1.00x (基线) |",
            "| CRTP `work_impl` | 编译期内联单态化 | 4.94 | ~8.9x 快 |",
        ],
    },
    {
        "path": "Book/part06_templates/ch61_template_overload.md",
        "title": "图 1　编译期分派 vs 函数指针表（ms，越低越好）",
        "y_title": "耗时（ms）",
        "unit": "ms",
        "bars": [("if constexpr", 13.99, False), ("函数指针表", 59.66, True)],
        "ref": None,
        "x_caption": "随机 tag → BTB 可缓存固定目标地址",
        "intro": "函数指针表比 if/else 链温和（4.3× vs 10.4×），因为目标地址固定紧凑、BTB 能缓存。下面把 D5.1 的基准画成图。",
        "caption": "函数指针表慢 ~4.3× 的根源是**间接调用阻止内联 + 分支预测惩罚**：`table[tags[i]](v[i])` 每次迭代取索引、取地址、间接 `call`，阻止 `op_*` 内联，且随机 tag 令 BTB 难稳。但因三个目标地址固定且紧凑，`4.3× < ch62 的 10.4×`——前者是『间接调用 + 无内联』，后者叠加『分支预测失败』。**代价**是每种 Tag 实例化一份代码（mangled 名参与，独立实例化）。选型：操作集合编译期已知且封闭用 if constexpr/重载；运行期动态决定（插件、命令分派）才用函数指针表。颜色仅作区分，数值标签已写明。",
        "table_head": "| 策略 | 分派方式 | 耗时 (ms) | 相对 |",
        "table_sep":  "|------|----------|-----------|------|",
        "table_rows": [
            "| `if constexpr` 编译期分派 | 单态化 + 内联 | 13.99 | 1.00x (基线) |",
            "| 函数指针表 `table[tag](x)` | 运行期间接调用 | 59.66 | ~4.3x 慢 |",
        ],
    },
    {
        "path": "Book/part07_stl/ch90_ranges.md",
        "title": "图 1　手写循环 vs ranges 管道（ms，越低越好）",
        "y_title": "耗时（ms）",
        "unit": "ms",
        "bars": [("手写 for", 4.98, False), ("ranges for_each", 4.95, False), ("ranges 管道", 26.79, True)],
        "ref": None,
        "x_caption": "单算法/单视图 vs 多阶段 | 适配",
        "intro": "ranges 是『真零开销抽象』还是『免费午餐』？答案分两层。下面把 D5.1 的基准画成图——单算法逐 ns 等价，多阶段管道才暴露常数开销。",
        "caption": "`ranges::for_each` 与手写循环**逐 ns 等价**（4.95 vs 4.98 ms ≈ 1.00×）：views 与算法 lazy、零开销，迭代器调用被同构内联进主循环，是『真零开销抽象』实测铁证。但 `filter | transform` 多阶段管道慢 **5.38×**：(1) 每层 view iterator 适配链解包；(2) `filter` 不可预测跳过致分支失败 + cache miss；(3) 早期『0.87× 更快』假象来自优化器闭式求值消除，改随机数据后暴露真实常数开销。**ranges 非免费午餐**——单算法/单视图几乎零成本，每多叠一层 `|` 适配就多一层迭代器链解包；热点循环里手写或合并单 pass 更划算。颜色仅作区分，数值标签已写明。",
        "table_head": "| 场景 | 耗时 ms | 相对 |",
        "table_sep":  "|---|---|---|",
        "table_rows": [
            "| 手写 for 循环遍历 + 变换（基线） | 4.98 | 基准 1.00× |",
            "| ranges `for_each` 单算法 | 4.95 | 1.00×（几乎无差） |",
            "| ranges `filter \\| transform` 管道 | 26.79 | **5.38×**（慢） |",
        ],
    },
]


def build_section(spec):
    svg = vertical_chart(spec["title"], spec["y_title"], spec["unit"],
                         spec["bars"], ref=spec["ref"], x_caption=spec["x_caption"])
    table = [spec["table_head"], spec["table_sep"]] + list(spec["table_rows"])
    lines = []
    lines.append("## 基准数字可视化速读（本机 GCC 实测）")
    lines.append("")
    lines.append("> " + spec["intro"])
    lines.append("")
    lines.append(svg)
    lines.append("")
    lines.append("> **图注**：" + spec["caption"])
    lines.append("")
    lines.extend(table)
    lines.append("")
    lines.append("> 表注：以上数字取自本章 D5.1 基准（本机 GCC 实测，绝对毫秒随机器/编译选项而变），"
                 "**相对值/加速比才是可移植信号**。三模式渲染下若矢量图不显示，本表即兜底数据来源。")
    return "\n".join(lines)


def inject(path_rel, section):
    path = os.path.join(ROOT, path_rel)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    if "## 基准数字可视化速读" in text:
        print(f"  [skip] 已注入: {path_rel}")
        return False
    lines = text.split("\n")
    # 找最后一个 ### D5. 行
    last_d5 = -1
    for i, ln in enumerate(lines):
        if re.match(r"^###\s+D5\.", ln):
            last_d5 = i
    if last_d5 < 0:
        print(f"  [skip] 未找到 D5 段: {path_rel}")
        return False
    # 找 last_d5 之后第一个 ^## 行
    insert_at = None
    for j in range(last_d5 + 1, len(lines)):
        if re.match(r"^##\s+", lines[j]):
            insert_at = j
            break
    sec_lines = section.split("\n")
    if insert_at is None:
        # 末尾追加：确保在末尾空行后插入，且文件以单换行结尾
        # 去掉尾部空行再追加
        while lines and lines[-1].strip() == "":
            lines.pop()
        new_lines = lines + [""] + sec_lines
    else:
        new_lines = lines[:insert_at] + [""] + sec_lines + [""] + lines[insert_at:]
    out = "\n".join(new_lines)
    if not out.endswith("\n"):
        out += "\n"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print(f"  [ok] 注入: {path_rel} (D5@{last_d5}, insert@{insert_at})")
    return True


def main():
    changed = 0
    for spec in CHAPTERS:
        print(f"[chapter] {spec['path']}")
        sec = build_section(spec)
        if inject(spec["path"], sec):
            changed += 1
    print(f"=== done: {changed} chapter(s) modified ===")


if __name__ == "__main__":
    main()
