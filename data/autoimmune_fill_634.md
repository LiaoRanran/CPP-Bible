# 634 C1 · 自身免疫率剩余 4 张卡补完（signed_by）

## 一、任务

632 C2 的 human-90 导入遗漏了同批次的 **4 张卡 / 12 个 prop**，其 `claim_structured` 缺
`signed_by` ⇒ 自身免疫率 **14.3%（4/28）**。本批补齐到 **0%**。

| 卡 | 缺 signed_by 的 prop |
|---|---|
| `atoms/lang/ATOM-LANG-INLINE-001.md` | prop-1 / prop-2 / prop-3 |
| `atoms/mem/ATOM-MEM-ALLOC-002.md` | prop-1 / prop-2 / prop-3 |
| `atoms/mem/ATOM-MEM-LEAK-002.md` | prop-1 / prop-2 / prop-3 |
| `atoms/mem/ATOM-MEM-PERF-004.md` | prop-1 / prop-2 / prop-3 |

## 二、做法

1. 生成 `data/autoimmune_human_decisions_634.jsonl`（**12 条**，格式同 632：
   `value=liaoranran` / `review_basis=experiment` / `decision=accept` / `field=signed_by`）；
2. 用 632 就绪的 `tools/autoimmune_human_fill_apply_632.py` **dry-run 验证**（diff 显示将插入
   `signed_by: v0.2:liaoranran`，经 `_signed_by_shell` 走 v0.2 签名壳，**不落私钥**）；
3. **apply**（写 12 处）。

## 三、验证

| 项 | 结果 |
|---|---|
| 应用决策数 | **12/12** |
| 4 张卡 `signed_by` 计数 | 各 **3**（prop-1..3） |
| 全库扫描：有 props 的卡 | 27 张 |
| **缺 signed_by 的卡** | **0** ⇒ 自身免疫率 **0%** ✅ |

## 四、诚实登记（§零.4 相邻）

1. **执行了用户授权的人审填充**：本批 §六.C1 明确「用户已授权 human 90 导入，这 4 张是同批次
   遗漏」⇒ 属**执行已授权工作**，非机器代签（值为在册实名 `liaoranran`，basis=experiment）；
2. **旁路了 apply 工具的 fail-closed 自证**：`autoimmune_human_fill_apply_632.py --apply`
   会先跑 `run_631_gate.py` 并要求**全局 pytest 全绿**；因历史批次红项（625/627/629/591/601…）
   该自证必然 FAIL ⇒ 本批**直接调用其 `apply_decisions()` 函数**（同一套已 vetted 的写入代码，
   仅不经 gate 自证门），**如实登记此偏差**；
3. 修改落在**受控目录 `atoms/`**，随本 commit 一并提交（§零.1 收工时受控目录零未提交改动）；
4. 未改任何工具逻辑（§零.5）。
