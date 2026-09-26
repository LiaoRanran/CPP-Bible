# 647 C4 · 迁移文档（CPP-Bible monorepo → queyi-core 独立仓库）

> 执行记录：647 C3 已把 core 拆到**仓库外**的本地仓库 `C:\CodeLearnling\note\note\queyi-core`
> （**165 提交 + 1 个文档提交 = 166**，**无远端、未 push**）。
> CPP-Bible **工作树零改动**（拆分产物不在仓库内）。

---

## 一、为什么要拆（以及为什么这次**不**合并回去）

- **要拆**：`Atoms/Examples/Book/...` 是 C++ 领域内容，与"阙疑引擎"生命周期完全不同；
  引擎要被复用（C/嵌入式/其它领域）时，不该拖着 1500+ 本领域文件。
- **不合并回去**：用 `git subtree add` 把 `queyi-core` 塞回 CPP-Bible 子目录，会让
  `tools/*.py` 出现**两份同名文件**（一份在 `tools/`、一份在子目录），CPP-Bible 的
  645/646 测试套件会整体红 —— 这正是 647 §零.5「高风险先沙箱」要避免的路径。
  ⇒ **是否合并、何时合并，留交人裁决**（当前状态：两份并列）。

---

## 二、迁移步骤（可复现）

```bash
# 0) 前置：CPP-Bible 工作区状态记录（回滚锚点）
cd <CPP-Bible>
git rev-parse HEAD > /tmp/cppbible_head_before_split.txt

# 1) 沙箱验证（临时目录，原仓库零改动）
python tools/repo_split_sandbox_647.py --report      # 写 data/647_split_sandbox_report.md

# 2) 真拆（目标目录**在仓库之外**）
python tools/repo_split_sandbox_647.py --execute "C:\CodeLearnling\note\note\queyi-core"

# 3) queyi-core 侧：写 README / 最小 conftest / .gitignore，然后本地提交
cd "C:\CodeLearnling\note\note\queyi-core"
git add -A && git commit -m "queyi-core：首版"

# 4) 验证
python tools/queyi_core_v10_641.py --check                 # 内核自检必须 PASS
python -m pytest tests --collect-only -q                   # 收集必须 0 错误
```

**回滚**：`queyi-core` 目录**在 CPP-Bible 之外** ⇒ `rm -rf` 该目录即可；
CPP-Bible 端**什么也不用做**（连工作树都没动过）。

---

## 三、拆分机制（为什么不是 `git subtree split`）

`git subtree split` **只能按一个 prefix 拆**，而 core 文件分散在 `tools/` 多处（内核/证据层/智能层/
保护器/耦合层），按 `--prefix=tools` 会把 500+ 个非 core 工具一起带走。

647 用 **`git fast-export --all -- <paths> | git fast-import`**：

- 单趟 C 实现（不需要为每个 commit 起 shell，比 `filter-branch` 快一个数量级）；
- 只保留指定路径，且**这些文件的提交历史完整保留**；
- 路径清单由 `core_files()` = **种子模式 ∪ repo 内 import 传递闭包** 自动算出（可审计、可复算）。

### 实测踩到的四个坑（必须一起写进迁移手册）

| # | 现象 | 处理 |
|---|---|---|
| 1 | `fast-export` 128：`tag ... tags unexported object` | `--tag-of-filtered-object=drop` |
| 2 | `fast-export` 128：`encountered commit-specific encoding gbk` | `--reencode=yes` |
| 3 | 拆完 `pytest` 收集期**全错** | `conftest.py` / `pyproject.toml` **不迁移**；queyi-core 自带最小 conftest |
| 4 | 只写种子模式 ⇒ 保护器前身模块（642/636）缺失，大面积 ImportError | 清单加 **import 传递闭包** |

---

## 四、接手 queyi-core 后**第一件要做的事**

```bash
cd queyi-core
python tools/tool_integrity.py --update     # 重钉本仓库的完整性基线
```

**为什么必须**：`tools/.tool_checksums` 与 Merkle 根是 **CPP-Bible 的快照**（覆盖那边整个仓库），
**有意没有拆过来**。而 `gate_engine` 等判定入口会在 `main()` 首行调 `tool_integrity.enforce()`
—— **没重钉之前它们会 fail-loud 拒绝运行**。这不是 bug，是设计（改判定核心必须显式留痕）。

---

## 五、拆分后的实测状态（诚实）

| 项 | 结果 |
|---|---|
| 拆分仓库提交数 | **166**（core 文件视角；CPP-Bible 全量是 1900+） |
| 文件数 | 拆分带入 **118** 个 core 文件；加 README/conftest/.gitignore 后 tracked = **121** |
| 内核自检 `queyi_core_v10_641.py --check` | **PASS**（零领域依赖） |
| `pytest --collect-only` | **222 例收集、0 错误** |
| `pytest -k 647` 实跑 | **82 passed / 30 failed**（20s） |
| 30 个失败的原因 | **全部是数据缺失**：`atoms/`（原子卡）、`data/authority/`（账本）、
`data/transparency_log.jsonl`、`tools/.tool_checksums` ⇒ 都是**有意不拆**的东西，**不是拆分缺陷** |
| CPP-Bible 端 | **零改动**（工作树、测试、基线都未受影响） |

---

## 六、交人裁决项

1. **`queyi-core` 是否建远端 / 是否 push**（当前：本地仓库，无远端）；
2. **是否用 `git subtree` 合并回 CPP-Bible 子目录**（当前：**未做**，理由见 §一）；
3. **是否按 `docs/repo_split_final_plan_647.md` §二 重排目录**（当前：扁平 `tools/`）；
4. **30 个数据依赖测试**：是在 queyi-core 里造最小夹具，还是标 `skip`（当前：都不做，如实登记）。
