# 阙疑 QueYi · 可被独立验收的 C++ 知识验证器

> 一句话定位：**每条 C++ 知识结论都绑定「证据 + 复现命令 + 四态判决」，任何人可以重算、可以指出哪一环不成立 —— 而不需要先信任我们。**

这不是又一份"教程"，而是一套**可被打断的信任链**：断言 → 证据（真机编译/运行输出）→ 复现清单（版本串+命令+输入哈希+期望输出）→ 判决（pass / pass_with_exception / fail / unknown）。任意一环你都能自己验证。

---

## 核心数字（现算，非目标值）

| 指标 | 值 | 口径 / 来源 |
|---|---|---|
| 知识卡（实卡） | **42** | `web/data/cards_index.json` 52 张 − 草稿 10 张 |
| 教学台账卡 | 47 | `web/data/cards.json`（与上表**不是同一张表**，勿混） |
| 门禁规则 | **67** | `tools/gate_engine.py::RULES`（与 `data/_gate_rules.json` 交叉核对一致） |
| 权威账本事件 | **452** | 零改（红线） |
| holdout 检出率 | **87.5%** | 14/16，可测口径，双档（-O0/-O2 任一报出即 catch） |
| external 检出率 | **35.0%** / 43.75% | 14/40 全样本 / 14/32 可测口径 |
| 反事实算子精度 | 1.0 | 10/10 带标签案例 |
| 变异杀死率 | **97.35%** / 81.5% | core 110/113 / all（on_scored，内部自证） |
| 逃逸率 | 0.0711% | 1/1406 变体（冻结为内部对照） |
| 判决记录 | **31** | pass 12 / pass_with_exception 0 / fail 0 / unknown 19 |
| 知识图谱 | **178 节点 / 1093 边** | 卡 47 · 命题 89 · 误解 42；7 个 domain 聚类 |

> 数字**全部现算自真实台账**，前端只渲染、不写死。口径与分母一并给出，避免"43.8% 误读"类问题。
> 670c 起由 `tools/drift_watch_670c.py` 监控上述关键数字：**变化超 ±10% 且无实验记录就标红**（输出 `data/drift_report_670c.json`）。
>
> **671g 双口径声明（数字真实性）**：表中 87.5%（14/16）/ 43.75%（14/32）是**盲测冻结值**（支撑外部效度 claim）。
> 671a 扩样后的**累计值**（新样本非盲、corpus 检测口径变更，**不得用于外部效度 claim**）：holdout 81.0%（17/21）、
> corpus 54.2%（26/48，分层 19/24、6/14、1/10）。两者并列、逐样本可独立重数，复算与口径见
> `data/671g_数字真实性核查.md` + `tools/numbers_671g.py --check`。

---

## 架构（文字版）

```
                  ┌─────────────────────────────────────────────┐
   原始真理源      │ atoms/ (C++ 知识断言)  evidence/ (真机证据)    │
   （人审 + 机器）  │ data/authority/decision_event_v2_ledger.jsonl │
                  └───────────────┬─────────────────────────────┘
                                  │ 内核 = 薄 wrapper（importlib 解析到 canonical）
                  ┌───────────────▼─────────────────────────────┐
   验证器内核      │ queyi-verifier（独立仓，可被第三方单独拉取）   │
   （单一实现）    │   · 四态判决（半格 + 冲突仲裁）               │
                  │   · 变异测试 / 逃逸率 / 保护器                │
                  └───────────────┬─────────────────────────────┘
                                  │ Merkle 根 + 哈希清单（可离线复核）
                  ┌───────────────▼─────────────────────────────┐
   可验证前端      │ web/ 静态站（无后端、无追踪）                  │
   （纯展示，不    │   总览 · 卡库 · 学习台 · 实验结果 · 星图 ·    │
    替结论背书）   │   验哈希 · 判决与数字                         │
                  └───────────────┬─────────────────────────────┘
                                  │ 论文 + 实验 + 复现 kit
                  ┌───────────────▼─────────────────────────────┐
   学术产出        │ research/paper_v0.6.md（投向 NeurIPS E&D）    │
                  │ REPLICATION.md + tools/reproduce_all_670c.py │
                  └─────────────────────────────────────────────┘
```

**拆分边界（670c 实测登记）**：内核层（`queyi_core_*.py` ×7 + `queyi_data_models_645.py`）在 CPP-Bible 侧是约 2.7KB 的**薄 wrapper**，运行期解析到 `queyi-verifier/tools/` 的 canonical（单一实现、两处入口）；判决/变异层（`gate_engine.py` / `verifier_closure_*.py` / `mutation_*.py` 共 10 个文件）**两侧都是完整实现且逐字节相同** —— 这是 647 方案 §六 明确**留交人裁决**的已知债务，`tools/check_split_670c.py` 会检查它**是否漂移**（两侧同名字节不一致即 FAIL）。

设计准则（见 `web/css/design-tokens.css`）：**纯中性灰阶底 + 单一沉静蓝强调色**（671d 起；此前暖中性底 + 橙强调色已弃）、深/浅双主题、8px 基数、圆角只 4/6/8 三档、**无渐变 / 无毛玻璃 / 无辉光 / 无多阴影**、WCAG 2.2 AA 对比度**现算**、移动端 44px 触控、尊重 `prefers-reduced-motion`。
670c 起对比度审计工具化：`web/js/contrast_check.js` 覆盖 27 组配对 × 深/浅两主题，全部 ≥ 4.5:1（`npm run test:contrast`）。

---

## 快速开始（3 步跑起来）

```bash
# 1) 拿代码
git clone <repo-url> && cd CPP-Bible

# 2) 起一个本地静态服务器（前端是零构建纯静态站，但需要 http 协议才能 fetch JSON）
python -m http.server 8000 --directory web

# 3) 打开
#    浏览器访问 http://localhost:8000/index.html
```

> 不需要 Node、不需要构建、不需要后端。所有数据在 `web/data/`，所有图表零依赖（自研 SVG/Canvas，不引 ECharts 以保证离线 + 体量）。
> 唯一例外：`data/experiments/` 与 `data/baseline.json` 在**仓库根**，页面以 `web/` 为文档根取不到 ⇒ 跑一次 `python tools/web_experiments_sync_670c.py` 同步进 `web/data/`（670c 新增，已接进构建管线）。

---

## 想复现结论？

**先读 [REPLICATION.md](REPLICATION.md)** —— 环境要求（含 **WSL 必须**的原因）、安装步骤、数据位置、逐条复现命令与预期数字+CI、常见问题。

```bash
python tools/reproduce_all_670c.py            # 一键：门禁 → holdout → corpus → 变异 → 反事实 → fast 测试
python tools/reproduce_all_670c.py --skip-slow
```

产物：`data/reproduction_report_670c.json`（逐步记录命令/退出码/输出摘要/是否匹配预期；**某步失败不中断**，最后给复现报告）。
数据完整性用 `data/dataset_hashes_670c.json`（SHA256 + 生成时间 + commit）核对；数据集元数据见 `data/croissant_670c.json`（Croissant 格式，E&D track 要求）。

---

## 三个入口

| 想看什么 | 去哪 |
|---|---|
| **怎么复现** | [REPLICATION.md](REPLICATION.md) |
| **论文 / 方法 / Claim 边界** | `research/paper_v0.6.md`（670b 交付；仓库另有 v0.7 草稿） |
| **实验结果图表**（检出率/变异率/演化） | `web/experiments.html` |
| **交互前端**（卡库/学习台/星图/验哈希/判决） | `web/index.html` |
| **前端完成度与已知限制** | [docs/670c_前端完成度.md](docs/670c_前端完成度.md) |
| **调研消化资产**（669/669b/669c 规划） | `docs/669_调研消化/` |

前端 8 个页面（总览 / 卡库 / 学习 / 实验 / 判决 / 星图 / 验哈希 / 卡片）共 **888 条 Node 真求值断言 + 8 页 jsdom 结构冒烟**，全绿：`cd web && npm test`。

**前端工程化（670c → 670c5 五批）**：
- **健壮性**（670c3）：8/8 页面 `noscript` 纯 HTML 降级（≤500B/页）；入口页 loading/error/empty 三态；`window.onerror`+`unhandledrejection` 全局兜底横幅。
- **可访问性**（670c4）：WCAG 2.1 AA **8 页 0 问题**（`tools/a11y_audit_670c4.py`）；对比度 27 组 0 失败；`header/nav/main/section/footer` 语义；一页一 `h1` 不跳级。
- **键盘导航**（670c4/670c5）：`g`+`h/c/l/e/v/s` 全局跳转、`?` 帮助弹窗、`Esc` 关闭；卡库 `/` 聚焦搜索、`j/k` 移动、`Enter` 打开；学习页 `1-4` 评分；弹窗焦点陷阱 + 回位。
- **响应式**（670c5）：320–1440px 无横向滚动；触控目标 ≥44px；断点令牌 `sm640/md768/lg1024/xl1280`（`web/css/responsive.css`）。
- **性能**（670c5）：首页 **gzip 76.3KB**（预算 120KB）；无外部 CDN 依赖；全部 `<script type="module">`；DOM 标签每页 ≤238。
- **构建**：`node web/build.mjs` 重建 `dist/`；`python tools/dist_verify_670c2.py` 验证（8 HTML / 引用 0 缺失）。

## Baseline 三臂对比（670a 现算 · `data/experiments/baseline_*.json`）

| 指标 | Static（rule-only，**口径重分箱**） | Random†（**仪器级代理**） | **Failure-driven** | Δ(static→FD) |
|---|---|---|---|---|
| holdout 检出 | 6.2% (1/16) [0.2, 30.2] | 6.2% (1/16) | **87.5% (14/16) [61.7, 98.4]** | **+81.3pp** |
| corpus 可测 | 12.5% (4/32) [3.5, 29.0] | 3.1% (1/32) | **43.8% (14/32) [26.4, 62.3]** | **+31.3pp** |
| defect 重注入 | 100% (6/6) | N/A | 100% (6/6) | 0 |

- 配对精确 **McNemar p ≤ 0.002**，**Cohen's h ≥ 0.72**；Δ 下界 **≥31.5pp**。
- **诚实边界**：Static 是**口径重分箱**（非重跑）、Random† 是**代理**（非真 B3）；真 B3/`detect_static` 需拆仓接口，**BLOCKED**。样本量 n=16/32 ⇒ 只读**方向**，不读幅度。
- 复算：`.\.venv\Scripts\python.exe tools\baseline_670a.py --run`（详见 `docs/670a_实验结果.md`）。

## 论文与投稿（v0.8）

- 中文稿 `research/paper_v0.8.md`；LaTeX 投稿版 `research/latex/queyi_neurips2027.tex`（NeurIPS D&B 匿名格式，主文 ≤9 页）。
- 论文管线 5 工具（数字同步 / BibTeX 审计 / 图表溯源 / 匿名化 / 质量门禁）已挂进 `run_master_gate_670c.py`（L1 阶段 `670g/paper-*`）。
- 新增 6 条 P0 门禁 `tools/gate_rules_670g.py`（论文/baseline 维度）。

---

## 贡献指南（DCO）

本项目采用 **DCO（Developer Certificate of Origin）**，而非 CLA：

- 每次提交必须签名：`git commit -s -m "your message"`，会在 commit message 末尾加上
  `Signed-off-by: Your Name <you@example.com>`。
- 原则：**不修改账本红线**（452 事件零改）、**不替结论背书**（只渲染现算值）、**门禁优先**（新增断言先过 `gate_engine`）。
- 新断言的标准路径：写 atom → 配 evidence（真机输出）→ 写复现清单 → 过门禁 → 进卡库。
- 改完核心工具记得重跑产物：`tools/guard_rerun_670c.py` 会对 `CORE_TOOLS` 做「源码语义哈希变了但产物哈希没变」检查（670c 新增，已并入主门禁）。

---

## 门禁与工程纪律

| 入口 | 作用 |
|---|---|
| `python tools/run_658_gate.py --check` | 658 阶段门禁（只读） |
| `python tools/run_669d_gate.py` | 669d 六条门禁（G-RATE-CONSISTENCY / G-DENOMINATOR / G-STATS-FROZEN / G-BOUNDARY-REQUIRED / G-BASELINE-EXISTS / G-IRR） |
| `python tools/run_master_gate_670c.py --check` | **670c 主门禁**：658 + 669d 六条 + 重跑护栏 + 漂移监控合并，输出 `overall` / L0·L1 分层 / 未登记 BLOCK 数 |
| `python tools/check_split_670c.py` | 拆分完整性（wrapper 是否真解析到 canonical / 复制层是否漂移） |
| `python tools/drift_watch_670c.py` | 关键数字漂移监控 |
| `python tools/guard_rerun_670c.py` | 「改了代码没重跑产物」护栏 |
| `python tools/gate_rules_671g.py` | **671g 14 条纪律门禁**：数字真实性/口径 4 + 方法学 D1/D3/D4/D6/D8/D9/D10 + 跨学科 E2/E3/E4（已并入主门禁 L0；清单见 `docs/discipline/门禁清单.md`） |
| `python tools/numbers_671g.py --check` | 全量实验数字单一复算源（盲测/累计双口径，逐样本独立重数） |
| `python tools/env_probe_671g.py --check` | 实验环境探测（编译器/WSL/ASLR/优化档），缺关键环境的产物标 UNVERIFIED |

**671g 工程纪律文档**：`docs/discipline/`（术语表、规则钉扎、序贯检验、PAP、胸腺、LLM 通道/投毒、
账本不变式、ITT、过拟合、证据链、不确定度、单人 DSMB/IRR/floor-check；门禁与工具清单各一篇）。

---

## 诚实声明（Why you can trust the limits）

- **unknown ≠ fail**：检测器不可用或测量配置错的样本记为 unknown，绝不悄悄降级为通过。
- **低分常是测量配置错**：3 个"假 miss"换编译档位（-O0/-O2 双档）即抓住；旧值作废而非静默替换。
- **外部 corpus 无盲态**：665 扩样样本在 reveal 后加入，不得用于 Claim 外部效度（见论文 §5）。
- **baseline / ablation 仍待生成**：实验页的 baseline 对比与 ablation 六组尚未落盘（对应规划任务 A03/A04），页面按设计显示"待670a生成"占位并**不编造数字**（字段契约见前端完成度文档）。
- **实测查出的不一致如实登记**：
  - 670c 曾观测到 `web/data/status.json` 与 `web/data/verdicts_667.json` 对卡数给出不同值（37/47 vs 42/52）——根因是 **status.json 是陈旧产物**；跑一次 `web_data_pipeline_656.py --build` 后两者一致（42/52）。**陈旧产物会伪装成"数据矛盾"**，这也是 670c 加漂移监控的动因之一。
  - 知识图谱里 **0/47 张卡带攻击边**（攻击边只存在于 misconception↔prop 之间），因此既有冒烟里"存在受攻击的卡节点"一条在**改动前后同样 FAIL** —— 未为了让冒烟变绿去改数据或改别人的脚本。
- **拆分不是"全拆完"**：见上文「拆分边界」，判决/变异层仍是两侧各一份完整实现（逐字节相同但无人阻止其漂移）。

详见 `docs/669_调研消化/`（消化自 v37–v47 共 9 轮调研）、`docs/670c_前端完成度.md` 与 `research/paper_v0.6.md`。
