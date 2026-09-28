# 657 D6 · CI 杠杆清单（可加可不加，成本/收益明示）

> 结论先行：本仓 CI（`ci.yml` + 本批新增 `dco.yml`）已经很重（quality / pytest / replay /
> gate / compile / site / pdf / epub / deploy 九路并行门禁）。657 在 CI 上的动作**克制**：
> 只新增了「DCO 报告态」这一条可离线复算的杠杆；其余一律**先列清楚成本/收益**，不擅自加硬门禁。

## 一、本批已落地的杠杆

| 杠杆 | 文件 | 形态 | 为何是这个形态 |
|---|---|---|---|
| DCO sign-off 检查 | `.github/workflows/dco.yml` | **报告态**（`continue-on-error: true`） | 655 交人项 2 明确「是否上 CI 强制」待裁决；历史提交绝大多数无签名，直接转硬会让**下次 push 立刻红**（与 `.gitattributes` 里记的「门禁狼来了」同构）。故先交付可离线复算的检查器（`tools/dco_check_657.py`，纯 git+stdlib，零外部 action），把不合规提交逐条打印为注解，但**不阻断**；裁决后把 `continue-on-error` 改 `false` 即转硬。 |

## 二、候选杠杆（按推荐度排序，均未强制实施）

### 杠杆 A：变异覆盖率地板（CI 跑 `mutation_test_656 --compare`）⭐ 推荐
- **做法**：CI 里加一步 `python tools/mutation_test_656.py --limit 400 --scope core --compare`，
  解析 `data/656_mutation_report_core.json` 的 `kill_rate_on_scored`，`core < 80%` 或 `all < 60%` ⇒ 红。
- **收益**：把 657 C 段达成的 97.3% / 81.5% 固化，防止核心判决逻辑被改软而无人察觉（这正是
  657 任务书的硬指标）。
- **成本**：每次 push 多跑 ~数分钟（变异体子进程启动）；且**变异体偶发超时/导入崩**会抖动
  （本批 5 超时 + 61 导入崩单列，不计入分母，但采样偶发可能让数字小幅波动）。缓解：`--seed` 固定 + 用 `kill_rate_on_scored`（排除超时/导入崩）判定。
- **建议**：作为**软门禁**（报告 + 仅当跌幅 >5pt 才红）先观察一轮，再转硬。

### 杠杆 B：CRLF 漂移报告入 CI artifact（non-blocking）
- **做法**：CI 加一步 `python tools/crlf_convergence_657.py --report`，把
  `data/657_crlf_convergence.md` 作为 artifact 上传。
- **收益**：让「索引 LF + 工作树 CRLF」的真实数量**可见**（本批实测 1745 个），驱动
  「碰到即转」策略推进。
- **成本**：`git ls-files --eol` 秒级，几乎零；non-blocking ⇒ 不会误红。
- **建议**：直接做（成本极低、纯增益）。

### 杠杆 C：前端 DOM 冒烟转硬（`web_smoke_655` ⇒ `continue-on-error: false`）
- **收益**：防前端回归（D7 已证明它能抓到 5 处真实缺陷）。
- **成本**：**当前会红**——D7 实跑 5 处断言失败 + 1 处台账哈希漂移（见 `data/657_web_smoke_report.md`），
  全是 pre-existing 前端债，非 657 引入。转硬会让门禁恒红直到 E 段修完。
- **建议**：**等 E 段修完 §三 的 5 条后再转硬**；此刻保持软（现状已是软）。

### 杠杆 D：PR 体量告警（变更文件数 / 行数阈值）
- **收益**：控制 review 负担。
- **成本**：**误伤大批量化债提交**——657 本身就是大批量（边界三元组 + 许可证头 + 变异补测）。
  阈值难定，易「狼来了」。
- **建议**：不做（与 657 这类批量批次冲突）。

### 杠杆 E：PR 也强制全量 replay（当前仅 `tools/` 变更才全量）
- **收益**：更严（PR 不依赖「是否动了 tools/」也能全量校验证据）。
- **成本**：每次 PR 多跑 `atom_evidence_replay.py --rebuild-manifest`（56 卡真编译，数分钟~十分钟）。
- **建议**：观察 runner 负载后决定；当前增量优先的默认已合理。

## 三、明确**不做**（带裁决记录）

1. **一次性 CRLF renormalize**：`.gitattributes` 2026-09-13 的监工裁决原文「暂不 renormalize」，
   理由两条（437 文件假 M 淹没真实改动 / 曾让工作树清洁检查恒红变狼来了）。657 D1 只执行裁决写明的
   **「碰到即转」**，不擅自动全量（连同 Merkle 根 / `artifact_sha256` 的连带重建与 OTS 重锚登记为交人）。
2. **DCO 硬门禁**：见 §一，待 655 交人项 2 裁决（历史批量补签 / 明确豁免口径）。

## 四、本批对 CI 文件的实际改动
- 新增 `.github/workflows/dco.yml`（DCO 报告态；见 §一）。
- `ci.yml` 本批**未改**（保持九路门禁原样）；任何新硬门禁都走 §二的「观察一轮再转硬」纪律。
