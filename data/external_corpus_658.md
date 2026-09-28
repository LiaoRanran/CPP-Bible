# 658 A4 · 外部 corpus 登记清单（第四层外部效度）

> 状态：本批**只登记清单，不实际引入**（任务书明确）。每类标注可引入的真实源与获取方式。

## 可引入的外部真实错误源（D4 数据集候选）

| 类别 | 真实源 | 引入方式 | 价值 |
|---|---|---|---|
| 历史 compiler bug | GCC Bugzilla、LLVM/Clang issue tracker | 抓取"wrong-code / miscompile"已确认 bug + 复现用例 | 测验证器能否抓编译器相关断言错误 |
| 标准库缺陷 | libstdc++ / libc++ 已知 bug 列表 | 取已修复的 UB/错行为 + 最小复现 | 跨标准库版本断言 |
| 已知 UB 案例 | C++ 标准"未定义行为"示例集、llvm UndefinedBehaviorSanitizer 用例 | 直接作为断言负例 | 验证器是否识破 UB 表述 |
| 标准歧义案例 | CWG / EWG 待决议题、标准 defect reports | 取"实现定义/未指定"边界 | 测语义 scope 标注准确性（C 段） |
| 跨编译器差异 | gcc vs clang 同代码不同结果案例 | 收集真实差异用例 | 测 semantic scope 平台/编译器边界 |
| 公开教材错误 | 知名 C++ 教材勘误表、社区 long-standing 错误 | 收集已被纠正的错误断言 | 测对"常识错误"的免疫力 |
| 社区长期争议 | StackOverflow 高票但错误的 C++ 回答、isocpp 邮件列表争议 | 抓取高票错误答案 | 测对"看似合理"错误的捕获 |

## 登记原则

- 引入时**必须**走 Authority Ledger 裁定，且纳入冻结 holdout（A2）而非开发集。
- 每条外部样本需带 provenance（来源 URL / issue id / 日期）与 semantic scope（C 段）。
- 不追求数量；先建 1 条/类的最小可引入样本，验证 pipeline 跑通后再扩。

## 口径提醒

外部 corpus 引入的是**真实世界错误分布**，与变异库（self-made distribution）性质不同：
mutation score 97% 不外延到外部 corpus（见 A5 / F）。
