# 715 · Part 3：push 记录

- 批次：715 ｜ 任务：Part 3.1 / 3.2 ｜ 日期：2026-10-10
- 红线遵守：**未使用 `--no-verify`**；pre-push 钩子全部通过后才推送（日志见 §4）。

---

## 1. 任务 3.1：push 前检查清单（逐项实测）

### 1.1 待 push 提交（`git log origin/master..HEAD --oneline`）

**源仓库 `CPP-Bible`：13 个提交**

| # | commit | 批次 | 主题（截断） |
|---|---|---|---|
| 1 | `9d32b6cb` | 715-B | equal-marginal substitution experiment（$2^4$ 全因子）+ Part-1 报告 |
| 2 | `ab488ec6` | 715-A | caliber 定义统一 + A8 状态同步 + Related Work 升级 + 17 条降级 |
| 3 | `6cf4c358` | 712-G | 712 验收报告 |
| 4 | `c4859e8b` | 712-F | 贡献收窄 + 工程建设 + 科研深化 |
| 5 | `be2dfc1c` | 712-E | 干净克隆复现路径对齐 |
| 6 | `8e0b29aa` | 714-E | 24 条逐节修改建议 + 验收报告 |
| 7 | `133cc0d6` | 714-B/C/D | 论文 2 非重复论证 + 3 篇相邻工作确认 + IAA 试点登记 |
| 8 | `1d7c8d02` | 714-A | 诚实性复查（27 处过度主张） |
| 9 | `f35858ca` | 713-D | 工程修复专项报告 |
| 10 | `25176c64` | 712-D | 匿名性审查 + 匿名副本构建 |
| 11 | `11707f81` | 712-C | 数字审计器 `or → all` 修复 |
| 12 | `a2b470d2` | 712-A | 出路探索 |
| 13 | `ef55a43e` | 712-B | 内容创作 |

### 1.2 DCO 核验

```
9d32b6cb DCO=YES   ab488ec6 DCO=YES   6cf4c358 DCO=YES   c4859e8b DCO=YES
be2dfc1c DCO=YES   8e0b29aa DCO=YES   133cc0d6 DCO=YES   1d7c8d02 DCO=YES
f35858ca DCO=YES   25176c64 DCO=YES   11707f81 DCO=YES   a2b470d2 DCO=YES
ef55a43e DCO=YES
缺失：无
```

### 1.3 是否裹挟其它批次的在途文件

逐提交列出改动文件（`git show --name-only`），**13 个提交共涉及 42 个文件，全部属于
`data/712_* / 713_* / 714_* / 715_*`、`research/latex/*`、`tools/*`、`tests/test_712.py`**。
对照工作区里仍处于未提交状态的其它批次文件（`data/640_*`、`647_*`、`656_*`、`658_*`、
`669d_*`、`authority_v2_mode.json` 等 **21 个**），**无一个被本次 push 的提交包含**。

⇒ **未裹挟**。（全部提交使用显式路径 `git add <file>`，从未 `git add -A`。）

### 1.4 论文 tex/bib 的修改是否为预期

| 文件 | 提交 | 是否预期 |
|---|---|---|
| `research/latex/queyi_neurips2027_v1.1.tex` | `ab488ec6`（715-A） | ✅ 715 任务 1.1–1.6 的论文修改 |
| `research/latex/paper2_measurement_drift.tex` | `ab488ec6` | ✅ 同上 |
| `research/latex/queyi_refs.bib` | `ab488ec6` | ✅ 新增 `chen2026judge`；`freiesleben` 键改 2026 |
| `research/latex/paper2_refs.bib` | `ab488ec6` | ✅ 同上（键名） |

**期望外的论文改动：无。** 编译验证：两篇 0 error / 0 undefined；论文 1 门禁 6/6。

---

## 2. 任务 3.2：push 执行结果

### 2.1 源仓库 `CPP-Bible`

| 项 | 值 |
|---|---|
| 命令 | `git push origin master` |
| **结果** | ✅ **成功** |
| 推送提交数 | **13** |
| 远端 `refs/heads/master` | `9d32b6cbbe48f5068b0069ba290026bca00cbb60` |
| 本地 `HEAD` | `9d32b6cbbe48f5068b0069ba290026bca00cbb60`（**相等**） |
| push 后 `git log origin/master..HEAD` | **0**（验收标准 9 满足） |

### 2.2 过渡包 `queyi-audit`

| 项 | 值 |
|---|---|
| 命令 | `git push origin main` |
| **结果** | ✅ **成功**，`7442f54..de5356e  main -> main`（退出码 0） |
| 推送提交数 | **6**（`da1015a` 712 修复 + `3ffa42b` 713-A + `39f3a16` 713-B + `fb09345` 713-C + `d1c0da2` + `de5356e`） |
| 远端 `refs/heads/main` | `de5356e0ea884ee13109c2c4a3f49882168caaba` |
| 本地 `HEAD` | 同值（**相等**）；`git log origin/main..HEAD` = **0** |
| DCO | 6/6 全部 `Signed-off-by: LiaoRanran <1026708211@qq.com>` |

### 2.3 匿名副本

**未推送**（且**没有 remote**）——按 Part 2 的建议，等用户拍板发布路线后再处理。

---

## 3. 本次 push 遇到的环境问题（必须写下来，因为它会误导判断）

前两次 `git push` **在 git 层面报错**，但第一次**其实已经成功**：

```
$ git push origin master          # 第 1 次
[prepush] ✅ 全部快校验通过，可 push
error: RPC failed; curl 35 schannel: failed to receive handshake, SSL/TLS connection failed
send-pack: unexpected disconnect while reading sideband packet
fatal: the remote end hung up unexpectedly          ← 看起来完全失败

$ git push origin master          # 第 2 次（重试）
[prepush] ✅ 全部快校验通过，可 push
error: RPC failed; curl 56 schannel: server closed abruptly (missing close_notify)
```

**根因诊断（实测）**：

```
$ git config --get https.proxy
http://127.0.0.1:65532                       ← 本机有一个出口代理
$ git ls-remote origin HEAD                   → schannel: failed to receive handshake（失败）
$ git -c https.proxy= ls-remote origin HEAD   → 9d32b6cb…（直连成功）
```

⇒ 失败发生在**本地出口代理与 GitHub 之间的 TLS 握手**，与仓库、钩子、提交内容无关。
直连（`-c https.proxy=`）后一切正常。

**教训（值得写进操作手册）**：

1. **"push 报错" ≠ "没推上去"**：TLS 在服务端接收后断开时，git 会报 failed 而远端已经更新。
   判断真实状态的唯一可靠方法是**查远端 ref**：`git ls-remote origin refs/heads/<branch>`，
   或 `git fetch` 后看 `git status -sb` / `git log origin/<branch>..HEAD`。
2. 本机出口代理 `127.0.0.1:65532` 对 github.com 的 TLS 握手不稳定；`git -c https.proxy=`
   可绕过。**但绕过代理会改变流量路径，是否长期采用属于用户决策**，本批只用于完成本次 push。
3. 两次 push 期间 pre-push 钩子**每次都完整跑过并通过**（§4），所以"钩子失败"不是本次的原因。

---

## 4. pre-push 钩子输出（两次完全一致，全绿）

```
[✅] quality: ────────────────────────────────────────
[✅] consistency: ============================================================
[✅] metrics: [gen-metrics] ✅ 全部文档数字与事实源一致
[✅] compile_gate: [gate] PASS: 无新增回归。
[✅] exempt_audit: [audit] PASS: 全部豁免仍有效, 无内容漂移.
[✅] expected(changed): no changed Book files
[✅] star_h2: [star-check] ✅ 星级格全合规
[✅] hygiene: 无未提交根级编译产物（根目录定向扫描，非全仓 --ignored）
[✅] worktree: 受控目录干净（Examples/ atoms/ evidence/ golden_state.json）

[prepush] ✅ 全部快校验通过，可 push
```

**未使用 `--no-verify`**（红线 4）：钩子在两次失败尝试中都是**自然通过**的，不需要绕过。

---

## 5. 推送后的即刻状态（2026-10-10）

| 仓库 | HEAD | 远端分支 | 待推送 | 备注 |
|---|---|---|---|---|
| `C:\CodeLearnling\note\note\C++\CPP-Bible` | `9d32b6cb` | `origin/master` = 同 | **0** | 公开 |
| `C:\CodeLearnling\queyi-audit` | `de5356e` | `origin/main` = 同 | **0** | 公开，**含真名账号**（见 Part 2.3 建议 private 化） |
| `C:\CodeLearnling\queyi-audit-anon` | `3b3c9cb` | 无 remote | — | **未发布** |

---

## 6. 与 Part 2 建议的冲突（诚实登记，需用户裁决）

**本次 push 使两份匿名投稿论文的 LaTeX 源码以真名账号公开**（`LiaoRanran/CPP-Bible`）。
这与 Part 2 §3 的建议（投稿期把源仓库设为 private）**方向相反**：

- 任务卡 Part 3 明确要求 push，本批照做；
- 但**论文 1/2 正在双盲投稿**（或即将投稿），公开的源码 + 真名账号 = 双盲失效风险；
- 缓解：这两篇论文的 tex **在本次 push 之前就已经在公开仓库里**（711 及更早批次已 push），
  所以本次 push **没有新增**这一类暴露，只是继续了既有状态。

**建议（用户拍板）**：若投稿尚未完成，**优先执行 Part 2 §3.4 的 private 化步骤**；
这一步与本次 push 不冲突，且可随时撤销。
