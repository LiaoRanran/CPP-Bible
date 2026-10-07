# 688 · C3 arXiv 投稿准备与备选方案

- **批次**：688 ｜ **来源**：arXiv 官方 2026-01-21 endorsement 政策更新（实时抓取，2026-10-07）
  - 政策原文：<https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/>
  - 说明：<https://info.arxiv.org/help/endorsement.html>

## 1. 当前阻塞状态
- 2026-01-21 起，**新提交者（首次投某类别）**不再接受"机构邮箱"作为唯一资格，须满足：
  - **路径一（双自动条件）**：同时持有 (a) 机构邮箱 **且** (b) 在目标**背书领域**内作为已录用 arXiv 论文作者（声明 paper ownership）；或
  - **路径二（个人背书）**：由同领域资深 arXiv 作者给予 **personal endorsement**。
- **无机构邮箱作者**：政策**不提供豁免**；即使有 prior authorship 也不满足 (a)，**只能走路径二**（找背书人）。
- arXiv 工作人员**不代为 waiver、不提供背书**；唯一官方渠道是反馈表单。

## 2. 本作者（LiaoRanran）的具体情况
- 身份：合肥大学软工大三学生；GitHub `LiaoRanran`；**无 arXiv 历史论文** → 不满足路径一 (b)。
- 机构邮箱：作为在校生**可能有** `.edu.cn` 邮箱，但即使有，仍缺 (b) prior authorship → **仍须个人背书**。
- 结论：**arXiv 投稿当前被个人背书门槛阻塞**。

## 3. 备选方案（按可行性排序）
1. **找个人背书人（首选）**
   - 途径：C++/程序验证/SE 社区的资深研究者（在 cs.SE / cs.CR / cs.PL / cs.LG 有 arXiv 历史）；通过导师、会议、邮件礼貌请求。
   - 合适类别：本论文可投 **cs.SE**（软件工程）或 **cs.PL**（编程语言）或 **cs.CR**（安全）——选与背书人领域一致的类别。
   - 注意：选 cs.LG 需论文确有 ML 内容（当前薄弱），不推荐。

2. **以合作者署名（次选）**
   - 与一位已有 arXiv 背书的合作者共同署名，由其在对应领域提交（满足路径一或路径二代理）。

3. **先投会议/期刊再回 arXiv**
   - 先中稿 TMLR/SE 会议，获得该领域 paper ownership 后，arXiv 新类别投稿更易过（路径一 (b) 满足）。

4. **改用无背书的预印本平台（绕开 arXiv）**
   - **TechRxiv**（IEEE 旗下，开放给所有技术论文，**无需 endorsement**，给 DOI）：<https://www.techrxiv.org/>
   - 领域预印本：engrXiv（工程）等。
   - 作用：先在公开平台获可引用 DOI，弥补"无 arXiv"的可见性缺口；后续拿到背书再补 arXiv。

5. **等学术邮箱 + 未来 authorship**
   - 若走科研路径（考研/读研），未来以研究生身份 + 机构邮箱 + 新 authorship 自然解锁——但**非短期方案**。

## 4. arXiv 投稿后的注意事项（一旦解锁）
- **版本管理**：v1 匿名稿；后续修订 v2/v3；避免频繁大改。
- **版权**：arXiv 为非排他性存档，不影响会议/期刊投稿（须确认目标 venue 的 preprint 政策；NeurIPS/TMLR 均允许 preprint）。
- **类别选择**：选 cs.SE/cs.PL/cs.CR 而非 cs.LG（除非补 ML 内容）。
- **匿名**：post 前移除 LiaoRanran 身份与 GitHub 直链（与 NeurIPS 双盲一致）。

## 5. 实操序列（建议）
1. 立即：清理仓库身份、准备匿名稿与代码托管（并行于 TMLR）。
2. 短期：联系潜在背书人 / 导师；同步 post 到 **TechRxiv** 拿 DOI（无门槛）。
3. 中期：拿到背书后 post arXiv（cs.SE 类）。
4. 长期：以 arXiv/TechRxiv DOI 作为对外可见锚点，喂 NeurIPS 2027 / TMLR。

## 6. 诚实边界
- "arXiv 录取率"不适用（预印本不审录用）；above 为政策事实，来源见官方博客。
- 个人背书能否拿到取决于社区关系，**非技术可控**；故 TechRxiv 作为无门槛保底必须列入。
- 勿把"arXiv 待 endorsement"写成"已发布"——仍属未公开状态，对外仅可称"preprint in preparation"。
