# 03 · 自动化证据获取调研（644 阶段 A · A3）

> 任务：调研 web scraping / API 限速 / 编译器实测自动化 / 标准文档解析 / 反例搜索，≥5 种，含可行性评估。

## 一、五种获取方式

### 1. Web scraping 最佳实践
- 尊重 `robots.txt`；设置合理 `User-Agent` 与限速；优先用官方 API 而非裸爬。
- 处理反爬：backoff、缓存、幂等。
- **可行性（阙疑）**：cppreference 有稳定 HTML；但**版权/合规需人审**（§十一.4）。降级方案：网络不通→标记「获取失败」。

### 2. API 速率限制（GitHub API / Stack Exchange API）
- 未认证 60 req/h，认证 5000 req/h；用 `429` + `Retry-After` 退避。
- **可行性**：SO 数据可经 Stack Exchange API 取高赞答案；但需配额，原型期可仅关键词抓取页面。

### 3. 编译器实测自动化（Compiler Explorer / Godbolt）
- Godbolt 有 API（`api.godbolt.org`）可远程编译取 asm；本地则用 `subprocess` 调 g++。
- **可行性（高）**：本地 g++ 实测最可靠，产出 L1 证据。原型仅 g++（§十二.4：clang/MSVC 未覆盖）。

### 4. 标准文档解析（eel.is/c++draft, ISO）
- c++draft 是生成式 HTML，章节锚点稳定；可抓 `[expr]` 等片段。
- **可行性（中）**：结构稳定但 HTML 易变；存「原始内容 + 抓取时间 + 章节锚点」以便漂移检测。

### 5. 反例搜索策略
- 关键词组合 + 标准章节交叉引用：如「UB + 边界」「例外条款 + 关键字」。
- 来源：WG21 issues、cppreference 警告框、编译器 bug 库（GCC/Clang Bugzilla）。
- **可行性（低-中）**：语义相关反例可能漏（§十二.3）；只搜索不判定（D3 铁律：判定留人审）。

## 二、可行性矩阵（原型级，§十二.1）

| 方式 | 可靠性 | 合规风险 | 阙疑落地 |
|---|---|---|---|
| 本地 g++ 实测 | 高 | 无 | D2 已实现 |
| cppreference 抓取 | 中 | 中（需人审） | D1 原型 |
| c++draft 抓取 | 中 | 低 | D1 原型 |
| SO/博客抓取 | 低-中 | 中 | D1 原型（降级） |
| 反例搜索 | 低 | 低 | D3 原型（只搜不判） |

## 三、落到 644 阶段 D 的设计输入

1. **D1 `standard_fetcher_644.py`**：抓 cppreference + c++draft，存原始内容+元数据；网络降级返回失败。
2. **D2 `compiler_probe_644.py`**：本地 g++ 编译运行，多选项（-O0/-O2/-std=c++17/20），沙箱临时目录。
3. **D3 `counterexample_searcher_644.py`**：关键词+章节交叉，输出候选（带来源），不判定。
4. **D4 `cross_validator_644.py`**：聚合 D1/D2/D3 多源对比一致性。
5. **D5 `evidence_acquisition_orchestrator_644.py`**：编排 D1–D4，用 B2 判充分性，N 轮上限防死循环。

> 所有网络工具必须有降级方案（§零.8），沙箱隔离（§九.5）。见 `tools/standard_fetcher_644.py` 等。
