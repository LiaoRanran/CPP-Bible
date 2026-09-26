# 647 C1 · 仓库拆分**沙箱验证**（原仓库零改动）

- 结论：**通过**
- core 文件数（声明的路径清单）：**116**

## 一、方案：为什么不是 `git subtree split`

645 D 阶段调研写的是 `git subtree split`。实测口径问题：**subtree split 只能按一个 prefix 拆**，而 core 文件**分散在 `tools/` 多处**（内核 / 证据层 / 智能层 / 保护器 / 耦合层）⇒ 按 `--prefix=tools` 拆会把 500+ 个非 core 工具一起带走。

647 改用 **`git fast-export --all -- <paths> | git fast-import`**：
- 单趟 C 实现（比 `filter-branch` 快一个数量级，且不需要为每个 commit 起 shell）；
- **只保留 core 路径**，且**这些文件的提交历史完整保留**；
- 路径清单由 `core_files()` 显式生成 ⇒ **可审计、可复算**。

## 二、沙箱三步与结果

| 步骤 | 结果 |
|---|---|
| ① `git clone` 到临时目录 | 成功（原仓库**零改动**） |
| ② fast-export/import 造 queyi-core | 提交 **164**，HEAD `90f768dd909d` |
| ③ 独立可跑（内核 import + selftest） | import=True，kernel `--check` rc=0 |
| ④ 测试可跑（collect-only） | rc=0 |
| ⑤ 历史保留（探针文件提交数） | 拆分仓库 **1** vs 原仓库 **1** ⇒ 相同=True |

```json
{
  "ok": true,
  "n_core_files": 116,
  "split": {
    "ok": true,
    "dest": "C:\\Users\\ASUS\\AppData\\Local\\Temp\\queyi_split_647_74eelczy\\queyi-core",
    "n_commits": 164,
    "head": "90f768dd909d",
    "n_files_declared": 116
  },
  "standalone": {
    "import_ok": true,
    "import_tail": "ok",
    "kernel_check_rc": 0,
    "kernel_check_tail": "d 排序（确定性） \n  [ok] policy_digest 稳定 \n  [ok] 规则引擎遍历数 = 规则数 × artifact 数 \n  [ok] 汇总计数正确 \n  [ok] run_id 确定性（不含时间戳） \n  [ok] input_manifest_digest 自动补齐 \n  [ok] integrity 自校验通过 \n  [ok] 封存后只读（改字段抛错） \n  [ok] 篡改 results ⇒ integrity 失效 \n  [ok] summary 投影计数正确 \n  [ok] 投影确定性 \n  [ok] manifest 投影含 digests \n  [ok] 未注册投影 ⇒ KeyError（fail-loud） \n  [ok] 内置投影 3 个 \n  [ok] 内核 AST 扫描零领域 import []\nv1.0 core selftest: PASS\n"
  },
  "tests": {
    "collect_rc": 0,
    "n_error_files": 0,
    "error_files": [],
    "conftest_used": "最小 conftest（沙箱临时写入）",
    "tail": "estmark = pytest.mark.slow\n\ntests\\test_loop_r5_runner_645.py:14\n  C:\\Users\\ASUS\\AppData\\Local\\Temp\\queyi_split_647_74eelczy\\queyi-core\\tests\\test_loop_r5_runner_645.py:14: PytestUnknownMarkWarning: Unknown pytest.mark.slow - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html\n    pytestmark = pytest.mark.slow\n\n-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html\n215 tests collected in 1.85s\n"
  },
  "history": {
    "probe": "tests/test_anti_windup_647.py",
    "in_split": "1",
    "in_origin": "1",
    "same": true
  },
  "tmp": "C:\\Users\\ASUS\\AppData\\Local\\Temp\\queyi_split_647_74eelczy"
}
```

## 三、沙箱实测踩到的四个坑（都是真的，不是设想）

| # | 现象 | 根因 | 处理 |
|---|---|---|---|
| 1 | `fast-export` 退出 **128**：`tag ... tags unexported object` | 仓库里有指向**未被导出对象**的 tag | 加 `--tag-of-filtered-object=drop`（拆分仓库不需要这些 tag） |
| 2 | `fast-export` 退出 **128**：`encountered commit-specific encoding gbk` | 早期 Windows 提交带 `encoding gbk` 头 | 加 `--reencode=yes`（只动 commit message 编码声明） |
| 3 | 拆完 `pytest tests` **收集期全错** | `tests/conftest.py` 会去调 `tools/tool_integrity.py` 校验 test_config，**强耦合整仓** | 该文件与 `pyproject.toml` **不迁移**；queyi-core 用**自己的最小 conftest**（只注入 sys.path） |
| 4 | 拆完测试仍大面积 `ImportError` | 保护器 647 **import 它们的前身**（642 灰度 / 636 影子），而种子模式只覆盖 `*_647.py` | 清单改为 **种子模式 ∪ repo 内 import 传递闭包**（复用内核 `module_imports()`，与 647 闭包同一套机制） |

## 四、风险与回滚

| 风险 | 触发条件 | 回滚动作 |
|---|---|---|
| `fast-export --all -- <paths>` 只**保留触及这些路径的提交** ⇒ 某些 commit 会变成空提交被丢弃（历史是「核心文件视角」的，不是全量） | 有人期望拆分仓库的提交数与原仓库相同 | 报告里同时给出**原仓库**与**拆分仓库**的提交数（不掩饰差值） |
| core 文件**分散在 `tools/` 多处** ⇒ 用 `git subtree split --prefix=tools` 会带上大量非 core | 按 645 备忘直接用 subtree split | 改用 fast-export/import 显式路径清单（本工具做法）；清单可审计（`core_files()`） |
| 拆分后 core 与 CPP-Bible **重复**（两份同名工具） | CPP-Bible 继续改工具，而 queyi-core 不跟 | 本批**不**把 queyi-core 合并回 CPP-Bible 子目录（见 647 §十.7 交人项）；先把拆分产物放仓库外，观察一轮再决定 |
| 沙箱验证**不等于**生产可用（临时目录删掉了，没有长期回归） | 把沙箱通过当成「已经拆好」 | C3 只建**本地**仓库、不 push；是否长期维护由人裁决 |

## 诚实登记

1. **沙箱在原仓库之外**（`tempfile.mkdtemp`）⇒ 原仓库**一个字节都没改**；
2. **历史是「核心文件视角」**：不触及 core 路径的 commit 被丢弃（报告给了两侧提交数）；
3. **沙箱验证 ≠ 生产可用**：临时目录用完即删，没有长期回归；
4. **core 路径清单是本批的定义**（`CORE_PATTERNS`）—— 若人认为该清单不对，拆分结果随之变化（清单可审计）；
5. **未 push、未改 CPP-Bible 工作树**。
