# 622 F1 · 621 交人项处理 + 化债

> 来源：`data/621_acceptance_report.md` §五（11 条交人项）+ 本批新发现的债

---

## 一、621 交人项处理状态（11 条）

| # | 621 交人项 | 类别 | 622 处理 | 状态 |
|---|---|---|---|---|
| 1 | 新 mutation 是否纳入 v8 基线 | 人拍板 | 622 又生成 30 条（两轮共 80 条）；**是否入 v8 仍待人拍板** | ⏸ 留人 |
| 2 | ABSTAIN 是否对外展示（写入渲染） | 人拍板 | C3 更新了 `uncertainty.abstain_state`（83 张），但**未重渲染** `data/pck/rendered/` | ⏸ 留人 |
| 3 | **30 条逐条人审是否执行** | 人拍板→已授权 | ✅ **622 D1 已执行**（按 615 清单 + 用户授权，日志 388→418） | ✅ **已化** |
| 4 | **CI 竞态修复是否 push** | 人拍板→已授权 | ✅ **622 B1 已 push**（`d2f412b..96fc0b8`，43 commit） | ✅ **已化** |
| 5 | 人审脱敏数据是否开源 | 人拍板 | 621 D3 已产出 776 条脱敏；**是否开源仍待人拍板** | ⏸ 留人 |
| 6 | schema 文档升级（`abstain_state` 等） | 可机器 + 人拍板 | ⚠ **仍未做**：619 B1 schema 是冻结件，改需人审；622 C3 已是"实现先行、文档滞后" | 🟡 未完成 |
| 7 | 原子卡是否补 `verdict` | 人拍板 | 622 C2 已**提取**（27 张 → SUPPORTED），**未写回原始卡**（硬边界） | 🟡 半完成 |
| 8 | `quality` 加 needs 增加 CI wall 是否接受 | 人拍板 | 622 B2 已**实测**（#627 总 243s，与 #626 相同，但缺对照） | 🟡 数据已备 |
| 9 | 攻击目标权重拍板（W1 vs W2） | 人拍板 | 未变；622 A4 继续用 W2 | ⏸ 留人 |
| 10 | Authority 是否启用替换现有人审通道 | 人拍板 | 622 D1 **已实际写入 Authority 日志**（418 条）⇒ **部分启用**；是否"正式替换"仍待人拍板 | 🟡 半完成 |
| 11 | **沙箱 apply API（VFDR 恒 0 的根本瓶颈）** | 人拍板→已实现 | ✅ **622 A1 已实现**（apply/run_gate/restore/apply_and_run + 6 重护栏），A2/A4 实跑 80 条 | ✅ **已化** |

**小计**：✅ 已化 3 条（#3 #4 #11）· 🟡 半完成/数据已备 4 条（#6 #7 #8 #10）· ⏸ 留人 4 条（#1 #2 #5 #9）

### 1.1 三条"已化"的意义

1. **#11 沙箱 apply API** —— 620/621 **连续两批**登记的**核心瓶颈**，622 解除。
   直接后果：verdict 从"v7 先验预测"变为**真实 gate 判决**（80 条实跑）。
2. **#4 push** —— 让 620/621 的 ci.yml 修改首次在远程 CI 实跑，
   并**验证了竞态修复有效**（gate 在 replay 结束后 2s 才启动，无 BLOCK 误报）。
3. **#3 30 条人审** —— 按用户授权把 615 决策清单落进**append-only + 哈希链**的决策日志。

## 二、本批化债内容

### 2.1 沙箱 apply API（A 线，核心）

| 项 | 内容 |
|---|---|
| 新工具 | `tools/sandbox_apply_622.py` |
| 护栏 | 字节级备份 / finally 必还原 / sha256 校验 / 并发锁 / 30s 超时 / 路径白名单 |
| 判决口径 | **diff-based**（新增 block=blocked / 检测消失=escaped / 新增非 block=detected_nonblock / 否则 neutral） |
| 实测 | A2：50 条（blocked 13 / neutral 14 / infra 23 / **escaped 0**）；A4：30 条（blocked 15 / nonblock 8 / neutral 2 / infra 5 / **escaped 0**） |
| 受控目录 | 跑完 80 条后 `git status -- atoms evidence` **为空** ✅ |

### 2.2 CI 竞态修复的远程验证（B 线）

- push `d2f412b..96fc0b8`（43 commit）；`concurrency-safety` job **首次上线即 success**。
- **gate 在 replay 结束时（05:27:22）之后 2 秒（05:27:24）才启动** ⇒ `needs` 强制生效。
- **gate conclusion = success，无 BLOCK 误报** ⇒ 619 的误报未复现。

### 2.3 ABSTAIN 与 Authority 对齐（C 线）

- 升级分类器 v2（verdict 识别 + Authority 交叉验证 + `basis` 溯源）。
- 提取 27 张原子卡 verdict（`status`/`evidence`/`claim_type`）→ 全部 SUPPORTED。
- 重新分类 83 张：**SUPPORTED 83 / 弃权 0**；**`UNDECIDED×approved` 从 27 → 0**（反相关消除）。
- ⚠ 已显式登记：原子卡的对齐**部分构造性**（依赖人审的 `status` 字段）。

### 2.4 人审执行与 W2（D 线）

- 30 条执行入库（388→418，哈希链通过），每条标注 `source=615_decision_list` +
  `authorized_by=user_authorization_2026-09-21` + `review_method=item_by_item_executed`。
- W2 重算：**IN114 / OUT7 / UNDEC0**，与 620 一致（**变化 0**），三层原因已实证。

### 2.5 雷7 Verification Horizon（E 线）

- 定义 + 测量工具 + v1–v7 曲线。
- **Horizon ≈ 60**；60-80 桶检出率 **0%**（断崖）。
- v1→v7 逃逸率 **23.74% → 0.64%**（能力确在进化，但集中在低复杂度带）。
- ⚠ 发现 **Horizon 指标本身不敏感**（v1–v7 恒为 60-80），建议改用"最低桶检出率"。

## 三、⚠ 本批新发现的债（来自 B2，**均非 622 引入**）

| # | 债 | 证据 | 影响 | 修复路径（留 623） |
|---|---|---|---|---|
| 1 | **治理 manifest 未同步** | CI pytest 失败；本地复现 `test_governance_doc_guard_591` 报 15 项新增（`_arch_v21/*`、`_auto/inbox/*`） | CI pytest job 红 | `python tools/governance_doc_guard.py update --force`（属治理动作，需人确认） |
| 2 | **`tools/` 存量 ruff 债** | CI quality 在 Ruff 步骤失败；本地复现 6 处（618/619 文件） | CI quality job 红 | 修 6 处（安全修改）；按 CI 钉的 `ruff==0.6.9` 复核精确集合 |
| 3 | **各批只对本批新文件跑 ruff** | 618–622 均如此；CI 跑 `ruff check tools/`（整目录） | 存量债长期不可见 ⇒ CI 长期红 | 在收工门禁里加"**整目录** ruff"检查 |
| 4 | **CI 日志不可读**（无鉴权） | annotations 仅给通用 exit code | 失败根因需本地复现推断 | 交人：是否配 CI 日志访问 |
| 5 | **Authority 日志与 annotations 未打通** | solver 读 annotations；D1 写 Authority 日志 | 30 条人审不影响 W2 | 投影通道（治理动作，需人拍板） |
| 6 | **ABSTAIN 未写入渲染件** | `data/pck/rendered/` 仍是 620 生成 | 渲染件看不到 abstain_state | 重渲染（是否展示 = 人拍板） |

## 四、仍然留交人的项（汇总）

1. **新 mutation 是否纳入 v8 基线**（两轮共 80 条已生成并实跑）
2. **ABSTAIN 是否对外展示**（写入 PCK 渲染）
3. **人审脱敏数据（776 条）是否开源**
4. **攻击目标权重拍板**（W1 保守 vs W2 校准）
5. **Authority 是否正式替换现有人审通道**（当前已"部分启用"）
6. **PCK 是否成为权威源**
7. **沙箱 apply API 是否纳入 CORE_TOOLS**（622 §八.1）
8. **新逃逸是否修复** —— 本批 **0 逃逸**，故**暂无待修项**；但 Horizon 暴露的
   "**60 以上仅 warn 兜底**"是否要**升为 block**，属规则变更 ⇒ **需人拍板**（622 §八.2）
9. **原子卡 `verdict` 是否写回原始卡**（622 §八.3）
10. **30 条执行结果是否最终认可**（622 §八.4）
11. **W2 判决变化是否接受** —— 本批**无变化**，故**无需接受**；但"打通两条通道后是否接受变化"需预留决策（622 §八.5）
12. **Verification Horizon 是否纳入核心 metrics**（622 §八.6）
13. **CI 存量债（治理 manifest / ruff）如何处置**（本批新增，建议 623 优先）
