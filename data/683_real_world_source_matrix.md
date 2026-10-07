# 683-A1 · 来源矩阵覆盖（真实靶场）

| 来源渠道 | 目标 | 实际 | 判定依据 |
|---|---:|---:|---|
| CVE（NVD 在线验证） | ≥40 | 110 | 每条 nvd.found=true 且冻结 NVD 应答原文 |
| GitHub Security Advisory 主来源 | ≥20 | 1 | NVD sourceIdentifier=security-advisories@github.com（客观字段） |
| GitHub Issues 链接 | ≥20 | 7 | NVD references 中 github.com/*/issues/* 链接 |
| Bug-fix Commits 链接 | ≥15 | 22 | NVD references 中 github.com/*/commit/* 链接 |
| GHSA advisory 链接 | ≥0 | 1 | references 中 /advisories/GHSA |
| Pwn/CTF 场景（source_type=pwn） | ≥5 | 0 | 竞赛/靶场常考的真实漏洞（Pwn2Own 等） |

## 按 source_type 分布

- `cve`: 110

## 诚实登记

- 来源矩阵是**收集渠道统计**，同一条样本可能同时具备多种链接（如同时有 commit 与 issue 链接）；各行计数按'有该类链接的样本数'计。
- GHSA 主来源条数若显著低于 20：这是**如实数据**（NVD 记录中 C++ 生态 CVE 以项目公告为主），不凑数、不伪造；GHSA advisory 链接与 commit/issue 链接的覆盖已一并报告。
