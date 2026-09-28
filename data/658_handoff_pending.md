# 658 · 交人项（handoff pending）

> 658 已落地的见各段提交。以下为**本批未做/未做完、需后续批次或人工裁决**的项，按 658 红线与预算诚实登记。

## E2 657 交人清理（部分）

| 项 | 状态 | 说明 |
|---|---|---|
| DCO 转硬 | ✅ 已做 | dco.yml `continue-on-error: false`；658 各提交已 `git commit -s`（全区间 0 不合规） |
| 前端缺陷 #1 | ⏳ 交人 | verify.js 分类语义：未列台账的 tampered 文件判「无台账」还是「不一致」需人定语义（657 报告 §三 #1）。修前需决策 |
| 前端缺陷 #4 | ⏳ 交人 | starmap.html 未标记受攻击卡节点；需接 `web/data/status.json` 的 attack 标记 + graph_core.js 渲染（657 §三 #4） |
| 前端缺陷 #5 | ⏳ 交人 | index.html 星图按钮文案现算仍 FAIL（line 229-230 已接 `c.nodes`，疑似 `c` 作用域/时序，需浏览器真跑定位） |
| rebuild-manifest | ⏳ 交人 | `atom_evidence_replay.py --rebuild-manifest`：56 卡真 replay 重算台账哈希；耗时长，需独立批次 |
| CRLF 全量 renormalize | ⏳ 交人 | `.gitattributes` 设 LF 后全量 renormalize；657 监工裁决曾否决（437 文件假 M 风险）；与本批 .gitattributes 冲突，需单独批次 + OTS 重锚 |
| slow 测试去写死数字 | ⏳ 交人 | 慢测试里的写死常量改为现算（与 D5 同源） |
| queyi-verifier 全量 move + 双仓 push | ⏳ 交人 | 需新建目标仓库 + push 权限；本批未动 |

## A3 独立生成
- 三 Agent（A/B/C）真实生成未跑（无独立会话）；协议见 docs/independent_generation_658.md。

## C4 semantic scope 落到卡 frontmatter
- atoms 受控零改动，本批只读提取 provenance；semantic scope 26/26 缺失，待 Authority 批准后再动 atoms。

## 口径差（E1）
- 规则数 67/63、节点数 178/121 待权威源；已登记容忍（见 docs/caliber_convergence_658.md）。
