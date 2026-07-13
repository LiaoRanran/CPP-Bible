# C++ Bible 接力手册 (PROJECT_HANDBOOK)

> **这是接续模型的圣经**。读这一份,胜过读其他任何文档。

## 一、当前基线（铁数据）

| 指标 | 数值 | 验证方法 |
|---|---|---|
| 章节 | 147/147 | `find Book -name "ch*.md" \| wc -l` |
| 行数 | 144,399 | `python3 -c "import os; print(sum(len(open(...).read().splitlines()) ...))"` |
| cpp块 | 7,132 | `grep -r "^\`\`\`cpp" Book/ \| wc -l` |
| 表格 | 1,648 | `grep -r "|---" Book/ \| wc -l` |
| 交引 | 1674 | `grep -r "Book/part" Book/ \| wc -l` |
| Parts | 17 | `ls Book/ \| grep -v Examples \| wc -l` |
| **v3密度** | **30.0/30** | `python3 tools/density_audit.py 1` |
| **v4真实质量** | **21.4/30** | `python3 tools/deduplication_audit.py 1` |
| **编译通过率** | **73.5% (324/441)** | `python3 tools/fast_compile.py 8` |
| 门禁 | 100/100 | `python3 tools/consistency_check.py` |

## 二、🚨 三大真相（后续模型必读）

### 真相1: v3密度=30是注水极值
v3只看关键词覆盖。水词模板如"本附录提供GCC/Clang/MSVC实现"能轻松得30分。
**v4审计**已证明: 实际质量均分仅21.4/30。

### 真相2: 代码编译通过率仅73.5%
441个cpp块中117个无法编译。失败原因:
- 缺`int main` (片段代码)
- 缺头文件(`<optional>` `<string>`)
- 缺分号/语法错误
- 用了C++23特性但GCC13不支持

### 真相3: 70%章节有重复段落
v4检测: 70+章节存在Jaccard相似度>60%的段落。典型是末尾附录模板重复。

## 三、工具链（10个核心）

```
tools/
├── consistency_check.py     门禁, 20元素/章 → 100/100
├── density_audit.py v3      关键词密度 → 30/30天花板 (已到顶)
├── deduplication_audit.py   真实质量 (工业引用+深度信号-水词)
├── fast_compile.py          并行编译验证, 8worker, 73.5% pass
├── chapter_compile_check.py 单章编译
├── compile_all.py           顺序编译（慢,留作fallback）
├── crossref_audit.py        交引完整性, 0断链
├── suggest.py               智能建议（已弃用,v3达成）
├── density_tracker.py       历史快照
├── knowledge_connect.py     知识连接表
├── chapter_template.md      章节模板
├── ROADMAP.md               6月规划
└── last_v4_report.json      v4完整排名（147条）
```

## 四、四条红线 + 四条绿线

### 🚨 红线（禁止）
1. **禁止注水提升v3分**（关键词堆砌、附录模板批量追加）
2. **禁止增加章节数**（147是合理规模）
3. **禁止幻觉**（WG21提案号PxxxxRxx/库版本/平台差异必须可查证）
4. **禁止批量单行追加**（每条新内容≥5行,必须信息增量）

### 🟢 绿线（核心方向）
1. **代码编译验证** (Phase 1): `fast_compile.py`跑全量,修复117个失败
2. **去水词v4审计** (Phase 1): 已有工具,需要降权重水词
3. **学习路径编排** (Phase 2): 依赖图+前置矩阵
4. **练习题注入** (Phase 2): 每章≥2道

## 五、下一步行动清单（按价值排序）

### P0 - 立即可做（1-2天）
- [ ] 跑全量编译: `python3 tools/fast_compile.py 8 --full` (7132块~30min)
- [ ] 修复缺`int main`问题: 给每个snippet自动wrap
- [ ] 修复缺头文件: 全文加`#include <string>`等基础头
- [ ] 删除模板残留(cpp块只有"```cpp\n```"空块)

### P1 - 1-2周
- [ ] 写`learning_path.py`: 扫描"⟶ Book/partXX/chXX"构建DAG
- [ ] 生成DOT图: `dot -Tsvg tools/learning.dot > learning.svg`
- [ ] 为每章写2-3道练习题(可编译+带答案)
- [ ] 实现`code_lint.py`: 检测伪代码片段(无main/无分号)

### P2 - 1-2月
- [ ] PDF生成实测: `bash tools/generate_pdf.sh`
- [ ] mdbook部署: `mdbook serve`本地预览
- [ ] CI/CD激活: `.github/workflows/ci.yml`配置token
- [ ] 知识图谱可视化: D3.js交互

### P3 - 持续
- [ ] 修复v4审计发现的低质段落
- [ ] 专家审阅
- [ ] 读者反馈-FAQ

## 六、关键技术细节

### GCC 13.1.0 限制
- 不支持: `<print>`, `<mdspan>`, `<flat_map>`, `<flat_set>`, `<expected>`
- 支持: `<ranges>`, `<concepts>`, `<coroutine>`, `<stop_token>`, `<barrier>`
- `__cplusplus` = 202100L（C++23）

### 文件命名规范
- `part01_history/ch01_c_history.md` (两位数part + 章节号+名字)
- 不重复: `tools/density_audit.py` 有检测器
- _legacy/ 目录忽略

### 章节元素20个
每章必含: ①..⑳ 标记 + cpp块 + 表格 + 引用 + 立场标签
门禁: 元素20/20 + cpp≥10(part01) 或≥30(其他) + 0禁词

### 编译修复模式
对snippet自动wrap:
```cpp
// 原: template<typename T> T max(T a, T b) { return a>b?a:b; }
// 修: 
struct Wrap {
    template<typename T> T max(T a, T b) { return a>b?a:b; }
};
int main() { return 0; }
```

## 七、记忆与文档

```
~/.workbuddy/MEMORY.md           用户级（个人偏好、跨项目习惯）
/.workbuddy/memory/MEMORY.md     项目级（已存在）
/.workbuddy/memory/2026-07-10.md 今日记录
/.workbuddy/memory/START_HERE.md 快速启动
```

## 八、应急策略

若后续模型被问"如何推分"→ 答:
1. **不要推v3分**（已到顶）
2. **改用v4+编译**真实数据
3. **优先修代码可编译性**（信息增量最大）
4. **加学习闭环**（练习题+依赖图）

## 九、决策原则

```
质量 > 数量
真实 > 完备
闭环 > 开放
可验证 > 可宣称
```

## 十、联系与升级

- 项目根: `C:/CodeLearnling/note/note/C++/CPP-Bible/`
- 用户: 大二软工, 嵌入式方向, 极简中文, 拒绝水词
- 工作模式: 批量Python脚本(不用Edit单行)
- 频率限制: 6个并发可能触发429, 改3-4个安全

---

_这本文档是后续模型的"地图+路标+工具箱+急救包"。_
_更新条件: 工具链有重大变更 / 路线图有调整 / 发现新真相。_

_最后更新: 2026-07-10 10:30_
