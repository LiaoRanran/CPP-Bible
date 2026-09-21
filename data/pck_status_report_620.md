# 620 B3 · PCK 证书状态统计 + 批量渲染

> 证书总数：**83** · B2 验证通过 83 / 失败 0

## 一、5 级状态分布

| 状态级别 | 张数 | 占比 |
| authorized | 23 | 27.7% |
| conditionally_authorized | 0 | 0.0% |
| disputed | 0 | 0.0% |
| abstain | 0 | 0.0% |
| unverified | 60 | 72.3% |

## 二、按 uncertainty.cs_upper_bound 分布

| cs_upper_bound | 张数 |
| 0.009062 | 83 |

## 三、按 verifiers 数量分布

| verifiers 数 | 张数 |
| 1 | 83 |

## 四、渲染产物
- 目录：`data/pck/rendered/`
- 文件数：**83**


## 五、与 619 的 10 张试点对比

| 维度 | 619 B3 试点（10 张） | 620 B3 全量（83 张） |
|---|---|---|
| authorized（approved） | 4（40%） | **23（27.7%）** |
| unverified（pending） | 6（60%） | **60（72.3%）** |
| disputed / conditionally_authorized / abstain | 0 / 0 / 0 | **0 / 0 / 0** |
| verifiers = 1 | 10（100%） | **83（100%）** |
| cs_upper_bound = 0.009062 | 10（100%） | **83（100%）** |

**解读**：试点 10 张是精选（含已 verified 原子卡），authorized 占比 40%；
全量纳入 56 张 draft 证据卡后降到 27.7%。**全量数字才是真实水平。**

## 六、局限性声明（诚实登记）

1. **verifiers = 1（83/83，100%）**：全部仅 gate_engine 一个验证器
   ⇒ erifier_disagreement 恒 N/A，无独立复核。这是**独立性硬上限**，不是迁移缺陷。
2. **human_authority 绝大部分是 batch_authorization（83/83，100%）**：
   非逐条独立审阅（615 诚实审计结论）。unverified 60 张更是**根本未经人判定**。
3. **uncertainty 全部引用全局 estimand L1 = 0.009062**：
   卡内无本地置信区间，"0.9062%" 是全局上界，**不代表单卡不确定度**。
4. **conditionally_authorized / abstain 恒为 0**：619 B1 schema 的
   human_authority.status 仅支持 pending/approved/rejected 三值，
   5 级分级中的这两级**尚无可表达字段**（620 C1 接口已前瞻定义，schema 升级留后续）。
5. **本统计只反映"结构性派生"结果**：human_authority.status 由卡 frontmatter 的
   status 机械派生，**不表示人真的逐条审过**。

---

> 本文件由 	ools/pck_status_stats_620.py 生成；渲染产物见 data/pck/rendered/（83 个 .md）。
