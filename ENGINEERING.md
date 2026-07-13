# ENGINEERING — 工程实践指南

> 关联: GOVERNANCE.md ⟶ CONVENTIONS.md ⟶ knowledge_graph.json

## 编码规范速查

| 规则 | 详情 |
|---|---|
| 头文件 | 缺失 `<print>` `<mdspan>` `<flat_map>` `<flat_set>` (GCC13) |
| UDL | `operator"" _x` (空格必须) |
| 版本宏 | `__cplusplus >= 202002L` |
| 折叠丢弃 | `((void)x, ...)` |
| 立场标签 | `[标准]` `[实现·GCC13]` `[平台·x86-64]` `[经验]` |

## 构建流水线

```
make check    → consistency_check.py (门禁)
make compile  → chapter_compile_check.py (编译校验)
make full     → check + compile + crossref
make graph    → 知识图谱验证
make report   → 综合项目报告
make clean    → 清理临时文件
```

## 质量门禁

| 检查项 | 工具 | 阈值 |
|---|---|---|
| 结构 | consistency_check.py | ≥30cpp + 20圈码 + 0禁词 |
| 编译 | chapter_compile_check.py | GCC13 -std=c++23 0 fail |
| 引用 | crossref_audit.py | 0断链 |
| 术语 | glossary.json | 有效JSON + 无重复ID |

## 目录约定

```
Book/partXX/chYY_topic.md    章节文件（不可改名）
tools/                        工具链（Python+MD）
memory/                       项目记忆
benchmarks/                   基准测试
examples/                     独立示例
*.md                          基础设施模块
*.json                        数据文件
```

## 禁止操作

- 覆盖已有章节文件
- 删除 `_legacy_*` 目录
- 修改章节编号
- 重命名 part 目录
- 破坏已建立的交叉引用
