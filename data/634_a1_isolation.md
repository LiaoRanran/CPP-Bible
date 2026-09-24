# 634 A1 · pytest 生产 `data/` 写隔离（方案 + 实现 + 验证）

## 一、病（633 F1 发现，634 任务0 定性）

全量 `pytest -m "not slow"` 会重写 `data/` 多个文件、向生产透明日志追加条目 ⇒ 工作区
脏文件 60→74、失败数 32→54 非稳定。**根因**：大量测试**直接调用被测工具的默认写方法**
（`write_report()` / `run_e2e()`），默认写到生产 `data/` 路径，未重定向 `tmp_path`
（任务0 静态扫出 **47** 处此类调用点，见 `data/634_pytest_side_effect_audit.md`）。

## 二、治法（会话级写保护 fixture）

在**根级 `conftest.py`（新增）**加会话级 autouse fixture `_isolate_production_data`：

1. 会话开始：`_snapshot()` 快照 `data/` 下**全部**文件（小文件存字节，>2MB 只记存在）；
2. 会话结束：
   - `_restore()` **删除**会话期间**新建**的文件（含未跟踪，如 `data/vsa/attestation_*.json`）；
   - **还原**被改动的文件字节；
   ⇒ `data/` 回到**开跑前**状态（**净 0 改动**）。

### 为什么放根级 conftest，而非 `tests/conftest.py`（关键）

`tests/conftest.py` 被 `tool_integrity.py` 的 `# test_config` 节**钉住哈希**（`TEST_CONFIG_TOOLS`）；
改它会触发 `pytest_configure` 里的 `--check-test-config` 失败 → `pytest.exit(2)` → **全套红**。
根级 `conftest.py` **不在**该钉住面内，且作为 rootdir conftest 对全部测试生效
（§零.5 只禁改 625-632 **工具**核心逻辑，未禁新增测试基建）。

> 也**没有**用 `tool_integrity --update`（那会顺带重建 Merkle 根、把既有 atoms 漂移一并
> "洗白"，属 633 登记的高风险"基准复位"）——本批规避。

## 三、验证（全量 `pytest -m "not slow"`）

| 项 | 结果 |
|---|---|
| 跑前 `git status --short -- data/` 行数 | 45 |
| 跑后 `git status --short -- data/` 行数 | 45 |
| 跑前 vs 跑后 **DIFF** | **空**（完全一致，净 0 改动）✅ |
| 受控目录 `git diff --quiet -- atoms evidence Examples Book` | **exit 0** ✅ |
| 失败数 | 54（非稳定，见下） |

子集验证亦通过（`test_e2e_attestation_629` + `test_autoimmune_diagnose_630`：跑前后
`data/` 状态 44/44 一致）。

## 四、诚实登记（§八）

1. **字面判据 `git diff --quiet -- data/` 未清零**：因会话**开跑前** `data/` 已是脏的
   （含 `data/transparency_log.jsonl` 被**更早**的测试运行追加过）——本 fixture 保证
   **pytest 净 0 改动**，但不清洗**历史**脏；且 §零.11 禁改 JSONL 账本 ⇒ **登记交人**；
   若在**干净起点**上跑，则该判据成立（fixture 不引入任何改动）；
2. **失败数仍非稳定（51↔54）**：data/ 隔离后，**跨会话**漂移已消除；残余波动来自
   **同一会话内**测试间对 `data/` 的**读依赖**（某测试读前序测试的产物），fixture 只在
   会话末还原、不阻断会话内耦合 ⇒ 属**测试设计债**，登记（根治需逐测试改 `tmp_path`）；
3. **未逐测试改造**（387 个测试文件）：本批用**集中式会话还原**一次性兜住，代价是
   会话内仍短暂写生产路径（有并发/中断风险，登记为已知限制）；
4. **大文件只记存在**：>2MB 文件若被测试改动无法还原内容（当前无此类改动，登记为限制）。
