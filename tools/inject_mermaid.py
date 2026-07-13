#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mermaid 图注入器（可复用、幂等）
==============================
向指定章节注入一张准确的架构/流程 Mermaid 图，增强可视化（不增字注水）。

设计约束（来自 AGENT.md 红线 + 用户偏好）：
  - 仅注入到「当前缺 Mermaid 且架构/流程含量高」的章；已有图的章不重复注入。
  - 图必须技术准确（不编造 API/语义），自包含、零外部依赖（纯 Mermaid 代码）。
  - 不触碰 cpp 块计数（门禁只统计 ```cpp，Mermaid 为 ```mermaid，不影响）。
  - 幂等：若目标章已含本小节标题则跳过，可安全重跑。

插入位置：章首「概述」小节（第 1 个 ##）之后，即在第 2 个 ## 之前插入，
保证图示紧随概述、早期可见；不干扰文末「自测练习 / 相关章节」结构。

用法:
    python tools/inject_mermaid.py
    python tools/inject_mermaid.py --check     # 仅报告哪些已注入/待注入
"""

import argparse
import re
import sys
from pathlib import Path

SUBSECTION = "## 架构与流程图示（Mermaid）"

# (相对路径, 一句准确说明, mermaid 代码)
TARGETS = [
    ("Book/part02_toolchain/ch11_compilers.md",
     "下图给出 C++ 源文件经编译器到可执行文件的标准流水线，每个阶段产出明确的 IR 或产物。",
     """flowchart LR
    SRC["源代码 .cpp"] --> CPP["预处理器<br/>宏展开 / 头文件包含"]
    CPP --> LEX["词法分析 Lexer<br/>token 流"]
    LEX --> PAR["语法分析 Parser<br/>AST 抽象语法树"]
    PAR --> SEM["语义分析 Sema<br/>类型检查 / 模板实例化"]
    SEM --> IR["中间表示 IR<br/>GIMPLE / LLVM IR"]
    IR --> OPT["优化 Pass<br/>内联 / 常量折叠 / 循环优化"]
    OPT --> CG["代码生成 CodeGen<br/>目标汇编 .s"]
    CG --> AS["汇编 Assembler<br/>目标文件 .o"]
    AS --> LD["链接器 Linker<br/>符号解析 / 重定位"]
    LD --> EXE["可执行文件 / 库"]"""),

    ("Book/part04_memory/ch35_memory_layout.md",
     "下图按地址从高到低给出典型进程虚拟地址空间布局；栈向下增长、堆向上增长，二者在中间相遇。",
     """flowchart TD
    K["kernel space（高地址）"]
    S["stack 栈（向低地址增长）"]
    M["mmap / 共享库"]
    H["heap 堆（向高地址增长）"]
    B["bss 未初始化全局变量"]
    D["data 已初始化全局变量"]
    R["rodata 只读数据（字面量 / const）"]
    T["text 代码段（低地址）"]
    K --> S --> M --> H --> B --> D --> R --> T"""),

    ("Book/part04_memory/ch39_raii_rule.md",
     "RAII 的核心保证：资源在构造时获取、在析构时释放，且析构无论正常退出还是异常都会执行。",
     """flowchart TD
    A["对象构造 ctor"] --> B["获取资源<br/>RAII：构造即获取"]
    B --> C["正常使用资源"]
    C --> D{"作用域结束 或 异常?"}
    D -->|"无论正常或异常"| E["析构 dtor 自动调用"]
    E --> F["释放资源（构造的逆序）"]
    F --> G["资源绝不泄漏"]"""),

    ("Book/part04_memory/ch41_smart_pointers.md",
     "三类智能指针的所有权语义：unique_ptr 独占、shared_ptr 共享（经控制块计数）、weak_ptr 仅观察不增引用。",
     """flowchart TD
    U["unique_ptr 独占所有权<br/>不可拷贝，只能 move"]
    SP["shared_ptr 共享所有权"]
    CB["控制块 control block<br/>strong_count + weak_count"]
    WP["weak_ptr 观察者<br/>不增加 strong_count"]
    SP -->|"1 个 shared_ptr 引用"| CB
    SP2["另一 shared_ptr"] -->|"共享同一"| CB
    WP -->|"lock() 提升为 shared_ptr"| SP
    WP -.->|"仅观察"| CB
    U -->|"std::move"| SP"""),

    ("Book/part06_templates/ch65_type_traits.md",
     "Type Traits 通过编译期布尔常量在重载决议中分派不同实现，下图为其决策骨架。",
     """flowchart TD
    Start["类型 T 入参"] --> Q1{"trait 满足?"}
    Q1 -->|"是"| Br1["分支 A：true_type 重载"]
    Q1 -->|"否"| Q2{"次 trait 满足?"}
    Q2 -->|"是"| Br2["分支 B"]
    Q2 -->|"否"| Br3["分支 C：默认实现"]
    Br1 --> R["编译期分派实现"]
    Br2 --> R
    Br3 --> R"""),

    ("Book/part07_stl/ch81_string.md",
     "std::string 依长度在「内联小缓冲区（SSO）」与「堆分配」两种布局间切换，避免短字符串的堆开销。",
     """flowchart TD
    S["std::string s"]
    SMALL["短字符串（size 不超过 SSO 阈值，通常 15 或 22 字节）<br/>字符数据内联在对象本体的小缓冲区<br/>无堆分配，无间接访问"]
    LARGE["长字符串（size 超过阈值）<br/>对象本体存：data 指针 + size + capacity<br/>字符数据在堆上"]
    S -->|"size 小"| SMALL
    S -->|"size 大"| LARGE"""),

    ("Book/part09_concurrency/ch107_atomic.md",
     "释放-获取同步：生产者以 release 写 flag，消费者以 acquire 读 flag；一旦观测到，之前的写入对消费者可见。",
     """flowchart LR
    P["生产者线程<br/>data = 1 （relaxed）<br/>flag.store(true, 释放)"]
    F["原子变量 flag"]
    C["消费者线程<br/>if flag.load(获取) 为真<br/>则读到 data == 1"]
    P -->|"释放 建立同步"| F
    F -->|"获取 观测到"| C"""),

    ("Book/part09_concurrency/ch113_coroutine.md",
     "协程体被挂起点切分为多个恢复段；初始挂起后按需恢复，最终挂起后对象不由协程帧自动销毁。",
     """stateDiagram-v2
    [*] --> InitialSuspend
    InitialSuspend --> Resume: "co_await / co_yield"
    Resume --> Suspend: "遇到挂起点"
    Suspend --> Resume: "awaiter.resume() 恢复"
    Resume --> FinalSuspend: "协程体结束"
    FinalSuspend --> [*]: "不自动销毁（返回值句柄持有）"
"""),

    ("Book/part10_modern/ch118_modules.md",
     "模块接口单元导出声明、导入方形成依赖图；与文本包含不同，宏不跨模块边界泄漏。",
     """flowchart TD
    A["module A （interface A.cppm）<br/>导出 foo()"]
    B["module B （interface B.cppm）<br/>导入 A，导出 bar()"]
    C["module C （interface C.cppm）<br/>导入 A 与 B"]
    M["main.cpp<br/>import A; import C"]
    A -->|"export"| B
    A -->|"export"| C
    B -->|"export"| C
    M -->|"import"| A
    M -->|"import"| C"""),

    ("Book/part12_patterns/ch135_patterns_intro.md",
     "GoF 23 种设计模式按意图分为创建型、结构型、行为型三大类，下图给出分类骨架。",
     """graph TD
    Root["设计模式（GoF 23 种）"]
    Root --> C["创建型 Creational（5）<br/>工厂方法 / 抽象工厂 / 建造者 / 原型 / 单例"]
    Root --> S["结构型 Structural（7）<br/>适配器 / 桥接 / 组合 / 装饰 / 门面 / 享元 / 代理"]
    Root --> B["行为型 Behavioral（11）<br/>策略 / 模板方法 / 观察者 / 命令 / 状态 / 职责链 / 迭代器 / 中介 / 访问者 / 备忘录 / 解释器"]"""),
]


def find_book_root(explicit=None):
    if explicit:
        return Path(explicit).resolve()
    here = Path(__file__).resolve().parent
    for p in (here.parent, here):
        if (p / "Book").is_dir():
            return p
    return here.parent


def inject_one(root: Path, rel: str, intro: str, mermaid: str):
    p = root / rel
    if not p.exists():
        print(f"[SKIP] 不存在: {rel}")
        return "skip"
    text = p.read_text(encoding="utf-8")
    if SUBSECTION in text:
        return "already"
    lines = text.split("\n")
    idx = None
    cnt = 0
    for i, l in enumerate(lines):
        if l.startswith("## "):
            cnt += 1
            if cnt == 2:
                idx = i
                break
    block = f"\n{SUBSECTION}\n\n{intro}\n\n```mermaid\n{mermaid}\n```\n"
    if idx is None:
        # 退化：插到「自测练习」之前，或文末
        for i, l in enumerate(lines):
            if "自测练习" in l:
                idx = i
                break
        if idx is None:
            idx = len(lines)
    lines.insert(idx, block)
    p.write_text("\n".join(lines), encoding="utf-8")
    return f"inserted@{idx}"


def main():
    ap = argparse.ArgumentParser(description="Mermaid 图注入（幂等）")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true", help="仅报告状态，不写入")
    args = ap.parse_args()
    root = find_book_root(args.root)

    mre = re.compile(r"^```mermaid", re.M)
    for rel, intro, mermaid in TARGETS:
        p = root / rel
        has = p.exists() and mre.search(p.read_text(encoding="utf-8", errors="ignore") or "")
        if args.check:
            print(f"[{'HAVE' if has else 'NEED'}] {rel}")
            continue
        if has:
            print(f"[SKIP] 已含 mermaid: {rel}")
            continue
        res = inject_one(root, rel, intro, mermaid)
        print(f"[{res}] {rel}")


if __name__ == "__main__":
    main()
