# DCO — Developer Certificate of Origin（贡献者原创声明）

> 本仓库**不用** CLA（Contributor License Agreement），采用 **DCO 1.1**：
> 贡献者在每个 commit 上签一行 `Signed-off-by`，声明自己有权提交该内容且同意以本仓库许可证（Apache-2.0）分发。
> 逐字原文见下（来自 <https://developercertificate.org/>，1.1 版）。

## 一、怎么签（两条命令）

```bash
# 1) 单次提交时签
git commit -s -m "tools: 修复 xxx"

# 2) 已经提交了、忘了签（只补签最近一次）
git commit --amend -s --no-edit
```

签名行形如（**真名/常用名 + 可联系邮箱**，须与 `git config user.name` / `user.email` 一致）：

```
Signed-off-by: 张三 <zhangsan@example.com>
```

一条 commit 里若有多位作者，每人各签一行。提交 PR 时，PR 模板会要求勾选"所有 commit 均已签名"。

## 二、为什么要签

- 让**贡献的来源可追溯**：谁写的、以什么身份授权本项目使用；
- 让**许可证链不断**：Apache-2.0 第 5 节规定，除非显式声明，主动提交的贡献默认按本许可证授权 —— DCO 就是这个"显式声明"的落地形式；
- 与本书的治理取向一致：本仓库要求**每条知识、每个判决都可复核**，贡献的来源同样如此。

## 三、DCO 1.1 原文

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

## 四、自动化检查（现状）

- **已有**：本文档 + PR 模板勾选项（人工确认）。
- **未做（诚实登记）**：**CI 未强制**校验 `Signed-off-by`。可选实现是加一个 `tools/dco_check_*.py`
  （对 `git log origin/master..HEAD --format=%B` 逐条要求存在 `Signed-off-by:`），等维护者决定是否要求**全部历史
  commit** 都补签（历史 100+ commit 无签名，若强制需一次大规模 `rebase --signoff`，本批不做）。
