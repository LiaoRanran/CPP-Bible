# GOVERNANCE — 项目治理框架

> 版本: 0.2.0 | 生效: 2026-07-09 | 参照: LLVM Developer Policy / Chromium Design Docs / Qt Governance Model

## 一、项目定位

《现代 C++ 终极圣经》是一个**长期演进的知识工程**，非一次性交付的书籍项目。
其生命周期以年为单位，内容规模以百万字为目标。

## 二、决策原则（优先级从高到低）

1. **可维护性** — 任何贡献必须能被未来的维护者理解和修改，不依赖特殊工具或个人知识
2. **可扩展性** — 架构必须能线性扩展到 200+ 章、10,000+ cpp 块、百万字
3. **自动化** — 重复性工作必须有脚本；手动流程必须文档化
4. **模块化** — 每章是独立可编译单元；工具间松耦合；知识图谱驱动关联
5. **复用性** — 模板、脚本、规则必须可跨章复用
6. **一致性** — 命名、格式、标签、交叉引用风格全局统一

## 三、目录结构约定（不可破坏）

```
CPP-Bible/
├── Book/              # 内容产出（按 part 分目录）
│   ├── part01_history/   ~ part16_reading/
│   └── _legacy_*/        # 废弃版本（SKIP_DIRS 排除，永不删除）
├── tools/             # 工具链（Python 脚本 + 配置）
├── memory/            # 项目级记忆（每日 checkpoint，与 workbuddy 独立）
├── benchmarks/        # 独立基准测试
├── examples/          # 独立编译示例
├── CONVENTIONS.md     # 编写规范（权威来源）
├── INDEX.md           # 全书章目（权威来源）
├── GOVERNANCE.md      # 本文件
├── PROGRESS.md        # 完成度矩阵
├── TASKS.md           # 任务看板
├── ISSUES.md          # 问题跟踪
├── REVIEW.md          # 审阅队列
├── CROSSREF.md        # 交叉引用索引
├── REFERENCES.md      # 外部参考资料
├── CONTRIBUTING.md    # 贡献指南
├── glossary.json      # 术语表
├── knowledge_graph.json # 知识图谱
└── make.bat           # 主构建脚本
```

## 四、变更流程

### 4.1 内容变更（章节修改/新增）
1. 确保 `tools/consistency_check.py` → 0 ERROR
2. 确保 `tools/chapter_compile_check.py` → 0 fail（目标章）
3. 更新 `PROGRESS.md` 对应条目
4. 若新增章，追加到 `knowledge_graph.json` 的 part 定义
5. 若添加新术语，追加到 `glossary.json`

### 4.2 工具变更
1. 新工具写入 `tools/`，含 `#!/usr/bin/env python3` 头 + argparse 接口
2. 在 `tools/ROADMAP.md` 的工具清单追加条目
3. 更新 `make.bat` 对应 target（如有必要）

### 4.3 基础设施变更
1. 新增模块（如 PROGRESS.md）：直接创建，使用 Write 工具
2. **禁止**：覆盖已有文件、重命名目录、修改章节编号、删除 `_legacy_*`
3. 所有新文件通过 HEADER 注释声明创建日期和依赖关系

## 五、质量标准

| 维度 | 门禁 | 工具 |
|---|---|---|
| 结构 | ≥30cpp + 20圈码 + 0禁词 | consistency_check.py |
| 编译 | 所有cpp块 GCC13 -std=c++23 0fail | chapter_compile_check.py |
| 引用 | 所有⟶目标存在 | crossref_audit.py |
| 术语 | glossary.json 有效 JSON + 无重复id | consistency_check.py |

## 六、版本策略

- 主版本号：门禁 0 ERROR 0 WARN 时递增
- 次版本号：每完成一个 part 的交叉引用回填
- 构建号：每次 `make.bat full` 通过后自动生成

当前版本: v0.2.0-alpha（141章落盘，门禁ERROR=0，WARN未清零）
