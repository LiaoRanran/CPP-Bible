# 人审交人项完整清单

> 生成时间：2026-09-19 · 所有项目均需用户本人操作，agent/苦力不得代签
> 按优先级排序：🔴 阻塞系统正常运行 · 🟡 影响数据准确性 · 🟢 改善但不阻塞

---

## 🔴 第一优先：阻塞项（3 项）

### 1. golden warn 136→186 人工 accept
- **现状**：575 命题级活性锚新增 50 条 warn，golden_lock 判"恶化 1"，test_golden_lock_json 持续预期红（已红 15+ 批次）
- **操作**：
  ```powershell
  cd C:\CodeLearnling\note\note\C++\CPP-Bible
  .venv\Scripts\python.exe tools\golden_lock.py check --accept --classify
  ```
- **验收**：pytest -m slow -n0 全绿（test_golden_lock_json 不再红）
- **风险**：accept 后 50 条 warn 成为基线，后续新增 warn 才会报警
- **依据**：575 worklog + 592 全库审视

### 2. push 本地 332 commit
- **现状**：本地 332 commit 未 push（ssh exit141，需用户切热点手推）
- **操作**：
  ```powershell
  cd C:\CodeLearnling\note\note\C++\CPP-Bible
  git push origin master
  ```
- **前置**：确保网络可访问 GitHub（ssh 端口 22 可能被公司网络封，切手机热点）
- **风险**：push 后远程可见，确保没有敏感信息（.env 已 gitignore）
- **依据**：592 全库审视

### 3. 591 苦力验收
- **现状**：591 建设包（v7 冻结+治理文档防护+测试器入哈希）苦力并行执行中
- **操作**：等苦力完成后，独立验收 v7 数字（1593/1405/1/179/8/1406）+ 治理文档防护 + 测试器入哈希
- **验收要点**：
  - v7 基线 M2=168（un-mask 真实 fixture 路径）
  - governance_doc_guard.py 能检出弱化指令
  - conftest 入哈希后篡改能被检出
  - gate 63/191 逐字不变（存量零误伤）

---

## 🟡 第二优先：数据准确性（4 项）

### 4. 3 条 unsigned 命题人签
- **现状**：prop_graph 显示 3 条命题未人签，全部来自 ATOM-LANG-INLINE-001（prop-1/2/3）
- **操作**：
  1. 先人审命题内容（`tools\prop_graph.py query --pending-signoff` 查看）
  2. 改卡面字段 `verified_by: human:<你的 git 提交者名>`
  3. `tools\prop_graph.py build`
  4. 复核
- **注意**：gate 校验该名与该文件最后一次 git 提交作者一致
- **依据**：566 worklog + 592 全库审视

### 5. 50 条 observation 命题补 liveness 锚
- **现状**：data/prop_liveness_todo.md 列了 50 条待补锚（命题级活性锚，575 新增）
- **操作**：逐条人审，在 claim_structured[*].liveness 填 `{kind: fixture_symbol, symbol: <夹具特有符号>}`
- **约束**：符号须真实出现在本命题引用卡的 artifact_assert 里 + 非通用 + 非散文
- **量级**：50 条，建议分批处理（每次 10 条）
- **依据**：575 worklog

### 6. 83 张卡填 verified_by_oracle
- **现状**：oracle_registry.json 存在（3 oracle），但 83 张卡 0 张填 verified_by_oracle
- **操作**：逐卡人审后填 `verified_by_oracle: {oracle: gcc-15.3.0, version: 15.3.0, verified_at: <日期>}`
- **注意**：这是放权门的前置——不填 oracle 就无法声称"经编译器验证"
- **量级**：83 张，建议先填 56 张真编译卡（hist/UB/lang），其余 27 张原子卡按需
- **依据**：574 worklog + 583 oracle_rotation

### 7. metrics curves 更新（v1→v7）
- **现状**：metrics.jsonl 最后一条 2026-09-17T17:40:45，curves.mutation_escape_rate 还停在 v1 的 0.2374（227/956），与当前 v7（1/1406≈0.0007）差 340 倍
- **操作**：
  ```powershell
  .venv\Scripts\python.exe tools\metrics_collector.py --collect
  ```
- **注意**：591 完成后 v7 冻结，再采集一次 metrics
- **依据**：592 全库审视

---

## 🟢 第三优先：改善项（5 项）

### 8. compiler 是否强制版本数字裁决
- **现状**：EV-UB-001 的 compiler = "Clang (ubuntu-latest runner 默认)" 有族名无版本（全库唯一）
- **选项 A**：强制版本数字 → +1 warn 破坏 191 命中逐字不变
- **选项 B**：带注释⇒只要求族名（当前口径，存量 0 命中）
- **建议**：选 B（观察期），等 EV-UB-001 补版本号后再考虑收紧
- **依据**：587 worklog 偏差 #2

### 9. machine-untriggerable 口径裁决
- **现状**：3 条人审象限规则（HUMAN-GOLDEN-REVIEW / HYBRID-TEACHING-DEPTH / LLM-SUPERIORITY-QUALITY）check is None，机器原理上无从触发
- **选项 A**：不计入诚实分子（当前口径，诚实 95.2% = 60/63）
- **选项 B**：计入诚实分子（诚实 100% = 63/63）
- **建议**：选 A（不虚高，人审声明≠机器背书）
- **依据**：586 worklog

### 10. M1 TCE escaped=1 是否继续冻结
- **现状**：唯一逃逸是 M1（删 negative_controls，EV-CONC-001），需工件/TCE 比对才能收口
- **选项 A**：继续冻结（当前口径，逃逸率 1/1406）
- **选项 B**：单独攻坚包修（最难，需 TCE/工件比对机制）
- **建议**：选 A（等其他维度满了再攻坚）
- **依据**：589 worklog

### 11. 27 条 legacy 豁免人复核
- **现状**：581 把 27 条存量豁免全标 redteam_seen: legacy，但未逐条人复核
- **操作**：逐条审查豁免 reason 是否仍然合理，不合理的移回 uncovered
- **量级**：27 条
- **依据**：581 worklog + 590 A3（legacy 回溯口子）

### 12. ruff 余族清理
- **现状**：pyproject 钉 select=["E4","E7","E9","F","I001","FURB167"]，其余规则（SIM115/UP031/DTZ005/BLE001/ISC004/RUF100/UP009 等）未启用
- **操作**：按族分批启用 + --fix + 人审
- **注意**：914 项那套若要清建议单开一批按规则分批
- **依据**：568 worklog + 573 worklog

---

## 卫生债（需非 agent 终端，3 项）

### 13. .pytest_tmp/run-* 清理
- **现状**：44 个目录，单目录可超 800 文件，safe-delete 批量阈值 500 直接打断
- **操作**（非 agent 终端）：
  ```powershell
  Remove-Item -Recurse -Force .pytest_tmp\run-*
  ```
- **建议**：写进 CI 收尾（每次运行后自动清理）

### 14. data/logs 清理
- **现状**：约 596MB 观测日志
- **操作**：归档旧日志或删除 7 天前的

### 15. 根目录临时件清理
- **现状**：大量 _probe/_t/_f/_s/_worklog/_acc 临时件 + tools_old558/ + eval_pack*/ + _probe_ch132_blk*.exe
- **操作**：逐条确认后删除，或移到 archive/

---

## 操作顺序建议

```
第 1 步（今天）：#3 591 苦力验收 → #1 golden accept → #2 push
第 2 步（本周）：#4 3 条命题人签 → #7 metrics 更新 → #8/#9/#10 裁决
第 3 步（下周）：#5 50 条活性锚（分批）→ #6 83 卡 oracle（先 56 张真编译卡）
第 4 步（有空）：#11 legacy 复核 → #12 ruff 余族 → #13-15 卫生债
```

---

## 注意事项

1. **所有 git 操作前确保工作树干净**：两条 CRLF 假脏（full_baseline_v4.json、EV-CONC-001.md）内容 diff 为空，勿提交勿还原
2. **golden accept 是不可逆操作**：accept 后 50 条 warn 成为基线，后续才会报警新增——确认 50 条都是合理的观察期 warn
3. **push 前检查敏感信息**：.env 已 gitignore，但确认没有其他密钥/凭据被跟踪
4. **人签用 git 提交者名**：`git config user.name` 查看，verified_by 字段必须与之一致
5. **agent/苦力不得代签**：所有 verified_by / golden accept / push 必须用户本人操作
