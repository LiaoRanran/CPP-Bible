# C2 · holdout 管理规范（666 批）

> 适用：`data/holdout/holdout.json`（canonical 合并视图）、`data/holdout_reveal_*_*.json`（每轮 reveal 冻结产物）、
> 以及一切"用来证明验证器有效"的样本集合。
> **一句话**：holdout 的全部价值来自**它在被看之前是盲的**；任何"看过之后再补样本"的操作都必须留下
> "这批样本不具盲态"的登记，且**不得**用来 Claim 外部效度。

## 1. 状态机（不可逆）

```
sealed  ──reveal()──▶  revealed  ──(永不回退)──▶  revealed
                          │
                          └── 之后追加的样本：hidden=true 且 revealed=true（**无盲态**，仅用于增大分母）
```

- `.revealed` 标记**不得**清除：`holdout_reveal_*` 工具只写报告，不改标记。
- 追加样本必须显式写 `"hidden": true, "revealed": true`，让"无盲态"在数据里**看得见**（666 C1 的 10 条即如此）。

## 2. 谁能看

| 角色 | 能看 sealed 样本 | 能跑 reveal |
|---|---|---|
| 维护者（人） | ✅ | ✅ |
| 引擎/Agent | ❌（只能跑 `--selftest` 与既有 reveal 报告） | ❌（reveal 由人触发） |
| CI | ❌ | ❌（reveal 不进 CI；CI 只跑"已 reveal 的报告"一致性） |

## 3. 新增样本怎么做

1. **写夹具**：`--write-fixtures`，夹具内容 sha256 落进 `fixtures_sha256`（同一夹具跨轮可比）。
2. **写真值**：每条必须给 `planted`（真错 / 对照）+ `basis`（判据出处：标准条款 / 实测命令）。
   没有 `basis` 的样本**不许进** holdout —— 否则真值会退化成"作者觉得"。
3. **写 atom_ref**：指向原子卡；**禁止**引用受控目录 `Examples/`（`--selftest` 有断言拦）。
4. **幂等**：`merged()` 重复调用不得重复追加；旧样本逐字保留（顺序、字段不重排）。
5. **更新分母**：新样本加入后，`count == len(seeds)` 一致性锁**放宽下界**但**不许撤锁**。

## 4. 版本管理

| 文件 | 角色 | 可否覆盖 |
|---|---|---|
| `data/holdout/holdout.json` | canonical 合并视图（旧工具兼容入口） | 由 `holdout_extend_*` 重写（幂等） |
| `data/holdout_665.json` | 665 扩样后的 canonical（20+10） | 同上 |
| `data/holdout_reveal_2_662.json` / `_3_665.json` | **每轮 reveal 的冻结产物** | ❌ **永不覆盖**（历史证据） |

新轮次 reveal 必须新建 `holdout_reveal_<N>_<批次>.json`，并在报告里写
`compare_reveal_<N-1>`（**只描述样本构成变化，不解释为"变好/变差"**）。

## 5. 统计口径（写死在工具里，不许口头改）

- **分母** = `catch + miss`（可测样本）；`unknown`（检测器不可用）**不计入分母**；
  `not_error`（对照样本）单独统计误报。
- **必须分层**：A 层（本机可跑）/ B 层（跨编译器或测量）/ C 层（本机无检测器）**分开报**，
  禁止把三层合并成一个数字。
- **档位必须写清**：666 A5 起 sanitizer 检测器**先 -O0、再 -O2**，任一档报出即 catch；
  只有两档都不可用才记 unknown。**换档位 = 换口径** —— 换口径必须作废旧数字（见 C6）。

## 6. 红线清单（每条都有血）

| 红线 | 由来 |
|---|---|
| reveal 后追加的样本不得用于 Claim 外部效度 | 665 C1 的 10 条（无盲态），论文里显式声明 |
| 不得把 unknown 合进 miss | MSan 全缺 / TSan 在 WSL 间歇 FATAL ⇒ 会把"没仪表"读成"仪表失灵" |
| 不得用单一档位的结论否定检测器能力 | 666 A5：5 个 miss 里 3 个换 `-O0` 就被抓住 |
| 不得为"数字好看"合并分母 | 7 个样本时 80%、17 个时 66.7% —— 分母构成变了，不是能力变了 |
