# _auto/ — 苦力-监工自动化协议

> 本目录是苦力（Trae/Cline）与监工（豆包）之间的自动化通信层。
> 双方通过文件系统通信，无需人工中转。

## 目录结构

```
_auto/
├── inbox/        ← 监工写提示词，苦力读取
│   └── NNN.md    # 第 NNN 批提示词
├── outbox/       ← 苦力写报告，监工读取
│   └── NNN.md    # 第 NNN 批完成报告
├── status.json   ← 状态机（双方都读写）
└── README.md     ← 本文件
```

## 状态机

```
idle ──(监工写inbox/NNN.md, state=awaiting_prompt)──→ awaiting_prompt
  ↑                                                          │
  │                                                          ▼
  │                                                   (苦力读取并开始执行,
  │                                                    state=running)
  │                                                          │
  │                                                          ▼
  │                                                     running
  │                                                          │
  │                                                          ▼
  │                                              (苦力完成, 写outbox/NNN.md,
  │                                               state=awaiting_review)
  │                                                          │
  │                                                          ▼
  │                                              awaiting_review
  │                                                          │
  │                                                          ▼
  │                                              (监工cron触发, 验收报告,
  │                                               写下一批inbox/NNN+1.md,
  │                                               state=awaiting_prompt)
  │                                                          │
  └──────────────────────────────────────────────────────────┘
```

## 苦力端协议（写在每批提示词末尾，苦力必须遵守）

1. **开始执行前**：读取 `_auto/status.json`，确认 `state == "awaiting_prompt"` 且 `current_batch` 与本批号一致；将 `state` 改为 `"running"`，填入 `worker_model`。
2. **执行过程中**：正常建设，每任务一 commit。
3. **完成后**：
   - 将完整报告写入 `_auto/outbox/{batch号}.md`（格式同以往 worklog）
   - 更新 `_auto/status.json`：`state = "awaiting_review"`，`last_completed_batch = {batch号}`，`history` 追加一条
   - **不要**自己写下一批提示词，不要 push
4. **异常处理**：如果中途失败，将失败原因写入 `_auto/outbox/{batch号}_FAILED.md`，`state = "awaiting_review"`，`consecutive_errors += 1`。

## 监工端协议（cron 每 15 分钟触发）

1. 读取 `_auto/status.json`。
2. 如果 `state != "awaiting_review"`：什么都不做，退出。
3. 如果 `state == "awaiting_review"`：
   - 读取 `_auto/outbox/{last_completed_batch}.md`
   - 验收：跑关键门禁（gate/poison/replay/integrity），核对数字
   - 写下一批提示词到 `_auto/inbox/{batch+1}.md`
   - 更新 `status.json`：`state = "awaiting_prompt"`，`current_batch = {batch+1}`，`last_prompt_batch = {batch+1}`
   - 如果验收发现严重问题：在提示词里写明回退/修复要求
4. 如果 `consecutive_errors >= 3`：暂停循环，在 status 里写 `paused = true`，等人工介入。

## 用户操作（Phase 1）

用户只需做一件事：**把 `_auto/inbox/NNN.md` 的内容复制粘贴给 Trae/Cline**。

Trae 执行完后会自动把报告写到 outbox，监工会自动验收并写下一批。用户不需要看报告、不需要写提示词、不需要验收。

## Phase 2 升级（苦力端自动投喂）

在 Trae/Cline 中设置启动指令：
```
每 5 分钟检查 C:\CodeLearnling\note\note\C++\CPP-Bible\_auto\inbox\ 目录。
如果有新文件且 status.json 的 state == "awaiting_prompt"，
读取该文件作为任务指令并执行。执行完按 _auto/README.md 的苦力端协议写报告。
```
设置后用户完全零操作。
