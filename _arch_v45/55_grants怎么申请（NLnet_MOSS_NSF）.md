# 方向 55：grants 怎么申请（NLnet / MOSS / NSF）

## 核心结论
1. **重要坏消息**：NLnet 的 **NGI Zero Commons Fund 已于 2026-06-01 关闭（第 13 次也是最后一次征集）**，不再收新申请；且 NGI 计划在 2025 EU 预算草案中被削减——**传统"单人 FOSS 资助"渠道正在收紧**。
2. 仍可尝试：**NLnet 其他项目（查其 Apply for funding 页）**、**Mozilla MOSS**（开源支持，偏基础设施）、以及**国内/企业资助**（CCF、腾讯/阿里开源计划）。NSF 面向美国机构，**双非本科生基本不可申**（需 PI 隶属）。
3. 对 QueYi：单人 + 无机构 → 现实路径是**小额赞助（GitHub Sponsors/Open Collective）+ 企业场景赞助（如存储厂商）**，而非传统 grant；把"可审计验证"卖给有合规需求的企业。

## 精确数字与案例
- **NLnet / NGI Zero**：Commons Fund 第 13 次征集 **2026-06-01 关闭**；历史上 NGI Zero 资助 **1000+ FOSS 项目**；但 NGI 在 2025 EU 草案中被移出资助计划（postmarketOS 报道），未来不确定。
- **Mozilla MOSS**：资助开源基础设施/安全项目，公开申请（金额数千–数万美元级）。
- **NSF**：需美国机构 PI，个人/境外不可申——**直接排除**。
- **开源资助清单**：GitHub `ralphtheninja/open-funding` 汇总各渠道（含 netidee 等，历史单项目最高约 €50k）。
- **企业赞助**：GitHub Sponsors（个人/企业月付）、Open Collective（透明账本，正好呼应 QueYi 的可审计性）、Tidelift（维护者付费）。
- **案例**：Redox、postmarketOS 等靠 NLnet/NGI 资助多年；但渠道关闭后需转向企业/社区。

## 对阙疑的 3 条具体行动
1. **先做 Open Collective + GitHub Sponsors**：公开账本（与 QueYi 可审计理念一致），门槛低、无需机构；把赞助按钮放 repo README。
2. **找企业场景赞助**：向存储/芯片厂商（长鑫等，方向 43）提案"用 QueYi 做固件代码可审计验证"的小额赞助（几千–几万元），比 grant 更快。
3. **盯 NLnet 新计划**：定期查 `nlnet.nl` 的 Apply for funding，若开新 FOSS 计划立即投（单人可申，NLnet 对个人开放）。

## 盲区（诚实标注）
- NLnet 是否 2026 后开新计划未知（Commons Fund 已关）；需实时查官网。
- Mozilla MOSS 对中国个人申请者的资格/成功率未知，需核实。
- 国内 grant（CCF/企业）具体入口与对本科生的开放度未查清（盲点）。

## 来源
- [1] NLnet Commons Fund（已关闭）— https://www.nlnet.nl/commonsfund
- [2] NGI Zero — https://ngi-0.eu/
- [3] 开源资助清单 — https://github.com/ralphtheninja/open-funding
- [4] postmarketOS on NGI 削减 — https://postmarketos.org/blog/2024/07/17/news-on-grant-applications/
- [5] Mozilla MOSS — https://www.mozilla.org/en-US/moss/
