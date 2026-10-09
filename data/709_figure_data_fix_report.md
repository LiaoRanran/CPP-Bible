# 709 Task C — figure_data 预存失败修复报告

- 日期：2026-10-09
- 文件：`tools/figure_data_check_670c2.py`
- 结果：**FAIL（2 项：未找到 Fig.3/Fig.4 坐标块）→ PASS（图 2 张 / 数据图 0 / 示意图 2，失败 0）**

## 1. 检查器原设计在查什么

`figure_data_check_670c2.py`（670c2 B3）假设论文里有 **pgfplots 数据图**：
- **Fig.3**（核心结果柱状图）：`coordinates{...}` 里的 holdout / external 值必须等于 `reveal_update_672h.json` 的现算值；
- **Fig.4**（演化曲线）：`coordinates{...}` 里的 660/665/666/668/669 每个值必须能在历史产物或回溯文档中找到出处。

它对论文做正则 `coordinates\s*\{...\}` 抽取——**抽不到就判 FAIL**。

## 2. 根因：v1.1 的排版里没有 pgfplots 数据图（检查器过时）

实测（709）：

- 论文 `\usepackage{pgfplots}`（L70）**只在导言区**，正文无 `\addplot`、**0 个 `coordinates{}`**；
- 论文的 **2 张图都是 tikz 示意图**（`node`/`draw`，无数据坐标）：
  - `fig:belnap` —— 四态平面（support × refutation 两个轴的四个象限），L220–234；
  - `fig:loop` —— 口径/循环示意（box + arrow），L961–982；
- 结果数据在论文中一律用**表格**呈现（16 张表），不画数据图。

⇒ 原检查器要求"图里必须有 pgfplots 坐标块"，对**一台合理排版选择**（用表不用数据图）**假 FAIL**。706 已核验：`coordinates` 在**改造前的 HEAD 原稿里同样 0 命中** ⇒ 预存问题，非 706/709 引入。

## 3. 修法（选任务书的"修检查器"分支；且**加强**而非放宽）

**修检查器**，把"假设有数据图"改为**图感知**判据：

| 新判据 | 内容 |
|--------|------|
| 1. **图完整性**（新增，更强） | 每张 `figure` 必须有 `\label`（能被 `\ref` 引用）；缺 label 即 FAIL |
| 2. **数据图溯源**（原判据，条件生效） | **只要**存在含数据构件（`coordinates{` / `\addplot` / `\datapoint`）的图，就按原 Fig.3/Fig.4 判据**逐点溯源**；解析不出坐标对也 FAIL |
| 3. **示意图声明**（新增） | 不含数据构件的图被明确登记为 *schematic（无硬编码数据）*，**给出显式说明而非假 FAIL** |

⇒ 不是把检查变成空转：**未来任何人往论文里加数据图，溯源判据会自动生效**；而"确实没有数据图"时会如实说明。

## 4. 验证

```
[figure-data] 图 2 张（数据图 0 / 示意图 2），通过 3，失败 0
  [OK ] 第 1 张 figure 有 label：['fig:belnap']
  [OK ] 第 2 张 figure 有 label：['fig:loop']
  [OK ] 2 张图为**示意图**（无 coordinates/\addplot 数据构件）⇒ 无硬编码数据需溯源：['fig:belnap', 'fig:loop']
[figure-data] PASS
```
`ruff check`：All checks passed。

## 5. 诚实边界

- 本任务**未改论文**（没有为通过而"补画 pgfplots 图"）；结论是**检查器过时**，按任务书"修检查器"分支处理。
- 原 Fig.3/Fig.4 的溯源判据**完整保留**（代码路径与阈值未改），只是从"无条件执行"改为"有数据图才执行"。
- 未删除任何溯源数据源（`holdout_reveal_3_665.json` / `external_corpus_reveal_665.json` / `reveal_update_672h.json` / `docs/667_回溯反思.md`）的装载。
- 未把"示意图"当作"数据已溯源"——它是**另一类**声明，报告中分开计数（data_figures=0 / schematic_figures=2）。

## 6. 产物

- 修改：`tools/figure_data_check_670c2.py`（图感知重写，+70 行）
- 本报告
