# 不可压缩事实清单（v6.1）

以下事实**必须写进文件**（卡 frontmatter / 质检报告 / 债务台账），
不能只存在于对话上下文。上下文压缩或切换窗口时，Agent 从文件重新加载。

## 工件层
- [ ] artifact_sha256（每个证据卡）
- [ ] artifact_compiler（编译器+版本+优化档+架构）
- [ ] fixture 文件名与路径
- [ ] command（完整复跑命令，含 WSL 的 setarch -R 前缀）

## 裁决层
- [ ] 红队发现清单（级别+内容+处置：采纳/驳回+理由）
- [ ] claim 修订历史（方向性反转必须留痕，含旧 claim 和反转原因）
- [ ] 人审裁决（DAL 豁免、人签字段）

## 门禁层
- [ ] replay 三分类结果（confirm/refute/infra_error 各自计数）
- [ ] gate block/warn/advice 计数
- [ ] golden_lock 基线（atoms/evidence/replay 数字）
- [ ] 未解决阻断项清单

## 批次层
- [ ] 待办清单（下一个窗口要做什么，精确到文件名）
- [ ] 已知环境边界（哪些工具不可用、哪些平台没测）

## 检查方法
窗口切换后，新 Agent 不读历史对话，仅凭上述文件能否继续工作？
如果不能，说明有事实没持久化——补进文件。
