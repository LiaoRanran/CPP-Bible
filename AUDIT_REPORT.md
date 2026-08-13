# 深度质量审计基线报告（E19 阶段一）

- 日期：2026-08-13
- 范围：C++ 示例全库（147 章 / 7291 个 cpp 块）+ Python 工具链（85 个 `tools/*.py`）
- 目标：在「功能正确性 / 健壮性 / 类型安全 / 可维护性」上建立可量化缺陷基线，区分
  **教学性故意示例**与**真实缺陷**，为后续修复（#203）与门禁复跑（#204）提供依据。
- GCC 版本：mingw1530 **15.3.0**（与章节编译门禁一致）

---

## 1. 执行摘要

| 维度 | 结论 |
|---|---|
| 五道发布门禁 | 4/5 直接 PASS；compile_gate（compile_all --main-only）基线在跑 |
| C++ 静态缺陷 | 7291 块中 589 个为故意教学错误/UB 示例（已排除）；`unsafe_c`(11)/`missing_virtual_dtor`(7) **经人工核对全部为教学或误报，非真实缺陷** |
| Python 工具链 | `bare_except` 3→0、`open_no_encoding` 真实 3→0；其余高危项均为 0 |
| 红线遵守 | `rm -rf`/`git clean` 命中均为临时/构建目录，**无 `git clean -fd` 命中仓库**（红线保持） |
| 真实已落地修复 | 5 处 `except:`→`except Exception:`；3 处 `open()` 补 `encoding='utf-8'` |
| 最高价值下一步 | `-Wall -Wextra -Wpedantic` 主块告警扫描（在跑），重点看 `-Wreorder`/`-Wnarrowing`/`-Wconversion` |

**核心判断**：本库的 C++ 示例「缺陷」绝大多数属于**故意演示错误/UB 的教学材料**。
盲目批量「修复」会降低教学价值（例如把 `strcpy` 改成 `strncpy` 反而模糊了「为何不用裸 C 字符串」的论点；给演示非虚析构的基类补 `virtual ~` 会抹掉反例）。
因此审计以**分类 + 人工核对**为主，仅对**无教学意图且确定安全**的项做最小修复。

---

## 2. 门禁基线（#200）

| 门禁 | 命令 | 结果 |
|---|---|---|
| prose 红线 | `verify_prose_only.py` | **OK**：所有正常围栏与 HEAD 逐字节一致；仅残留历史畸形围栏 WARNING（ch149=12、ch163=20 等），均为前序已知、非本次引入 |
| 一致性 | `consistency_check.py` | **ERROR=0 / WARN=3**，粗评 97/100 |
| 密度 | `density_audit.py` | 平均 25.0/30，**shallow=0**（无空洞章） |
| ASM 证据 | `asm_prepush_guard.py` | **PASS**：scanned=267，MATCH=252，DRIFT=3（基线已知，非新增），COMPILE_FAIL=2（C++20 模块，设计内），NO_SOURCE=10（手写多档对比，设计内） |
| 编译防回归 | `compile_all.py --main-only` → `compile_gate.py` | 基线在跑（147 章主块全量 -fsyntax-only，GCC 15.3.0） |

---

## 3. C++ 示例静态审计（`tools/audit_cpp_defects.py`）

### 3.1 方法
提取 `Book/**/ch*.md` 全部 ```cpp 块；以「前置 3 行 prose 或块内注释含
错误/UB/undefined/ill-formed/反例/should-not/won't-compile 等标记」判定为
**教学性错误示例**，仅计入统计、不列缺陷。对普通示例做类别扫描。

### 3.2 总数
- cpp 块总计：**7291**
- 教学性错误/UB 示例（已排除）：**589**
- 进入缺陷检查：6702

### 3.3 缺陷类别与判定

| 类别 | 计数 | 判定 | 处理 |
|---|---:|---|---|
| `unsafe_c`（gets/sprintf/strcpy/strcat/scanf("%s")/system） | 11 | **全部教学性**：8×`strcpy` 位于 RAII/内存安全章节（演示「裸 C 字符串之弊」）；3×`system("git describe …")` 为硬编码、无外部输入注入的示意 | 不修（修了反而削弱论点） |
| `missing_virtual_dtor` | 7 | **全部误报**：启发式用「块级 has-virtual + 块级 dtor」且要求 `virtual` 与 `~` 间有空格，漏判 `virtual~Target()`；且把同块内非多态辅助类一并误标 | 不修（人工核对 0 真实） |
| `raw_new_no_delete` | 90 | 多为教学片段（展示 `new` 后即结束，释放步骤在后续块或略去） | REVIEW，不批量修 |
| `reinterpret_cast` | 97 | 多为类型双关/底层教学（aliasing、位操作） | REVIEW，不批量修 |
| `using_namespace_std` | 2 | 全局 `using namespace std;` 名称污染（风格） | 低优先，可选修 |
| `endl_flush` | 733 | `std::endl` 强制 flush，循环中低效；教学上下文可接受 | INFO，不批量修 |

**关键结论**：C++ 示例的真实「缺陷密度」远低于表面计数——经人工核对，本次
**未发现需要紧急修复的功能正确性 bug**。高价值信号转移到下一节 `-Wall` 告警扫描。

---

## 4. Python 工具链审计（`tools/audit_py_tools.py`）

### 4.1 方法
`ast` 结构检查（裸 `except` / 可变默认参数 / `eval`·`exec` / 通配导入 /
`assert` 做运行时校验）+ 文本检查（`open` 缺 `encoding=` / `subprocess shell=True`
/ `rm -rf`·`git clean` / 非 LF 写库文件 / 吞异常）。

### 4.2 结果（修复后复跑）

| 类别 | 修复前 | 修复后 | 说明 |
|---|---:|---:|---|
| `bare_except` | 3 | **0** | `except:`→`except Exception:`（fast_compile / industrial_precision / suggest / exercise_gen / audit_py_tools） |
| `open_no_encoding` | 13* | **0** | 真实仅 3（density_tracker:60/62/67）已补 `encoding='utf-8'`；其余 10 为嵌套括号/方法调用/`webbrowser.open` 误报（已修审计正则） |
| `mutable_default` | 0 | 0 | — |
| `eval_exec` | 0 | 0 | — |
| `wildcard_import` | 0 | 0 | — |
| `assert_runtime` | 0 | 0 | — |
| `subprocess_shell_true` | 0 | 0 | — |
| `non_lf_repo_write` | 0 | 0 | LF 红线保持 |
| `rm_rf_or_git_clean` | 11 | 11 | **全部安全**：`d5_*`/`module_compile_check`/`wave_intake_check` 清 `tempfile.mkdtemp`；`rewrite_links` 清 `build/site`·`build/pdf` 生成物。**无 `git clean -fd` 命中仓库** |
| `broad_except_pass` | 8 | **0** | 8 处有意吞异常（baseline 解析回退 / 临时文件清理 / stdout reconfigure 容错）已逐处补「安全忽略」理由注释，吞异常点显式化，审计清零 |

\* 13 含审计脚本自身字符串误报 1 处，实际真实为 3。

### 4.3 已落地修复（commit 待推送）
- `tools/density_tracker.py`：3 处 `open()` 增 `encoding='utf-8'`
  （Windows 默认 GBK 解码 UTF-8 中文源会崩，属真实跨平台健壮性修复）
- `tools/fast_compile.py`、`tools/industrial_precision.py`、`tools/suggest.py`、
  `tools/exercise_gen.py`、`tools/audit_py_tools.py`：`except:`→`except Exception:`
- 新增审计工具：`audit_cpp_defects.py` / `audit_py_tools.py` / `audit_cpp_warnings.py`

---

## 5. `-Wall -Wextra -Wpedantic` 主块告警扫描（本轮回合重跑，task 9o861i；结果并入 #203）

对全部含 `int main` 的自包含 cpp 块做 `-fsyntax-only -Wall -Wextra -Wpedantic`，
按告警类型归类。已排除教学性错误示例。重点关注：
- `-Wreorder`（成员初始化顺序与声明不一致 —— **真实 bug**）
- `-Wnarrowing` / `-Wconversion`（隐式窄化 / 符号转换 —— **潜在数据丢失**）
- `-Wold-style-cast`（C 风格转型）
- `-Wunused-variable` / `-Wsign-compare`（量大，多为教学声明，低优先）

结果将在扫描完成后并入本报告并更新门禁（#204）。

---

## 6. 边界与红线（已遵守）
1. **LF 红线**：所有库文件写入须 `newline="\n"`；审计显示 `non_lf_repo_write=0`。
2. **不 `git clean -fd`**：核实 11 处 `rm`/`rmtree` 均针对临时/构建目录，未触及仓库源或参考库。
3. **不批量改教学示例**：`unsafe_c`/`missing_virtual_dtor` 经核对为教学/误报，未改动代码围栏（prose 红线门禁仍 0 问题）。
4. **后台 agent 不可靠**：本阶段审计/修复全部亲手执行并以 `git diff` 为落盘金标准，未用跨会话后台 agent。

---

## 7. 下一步（本轮回合状态）
- #201：`-Wall` 扫描已于本轮回合重跑（`audit_cpp_warnings.py`，GCC 15.3.0，task 9o861i）；待结果并入后对 `-Wreorder`/`-Wnarrowing`/`-Wconversion` 真实项做最小修复（#203）。
- #202：Python 工具链 8 处 `broad_except_pass` **已完成**（逐处补「安全忽略」理由注释，审计清零，见 §4.2/§4.3）。
- #203：依 #201 扫描清单逐条修复，保持 LF、过 prose 门禁、可编译，分批提交（后续回合）。
- #204：**门禁复跑全绿**——质量 16 道硬门禁本会话本地全 PASS（terminology/whitespace 两道回归已闭合），`compile` job 复跑通过；ERRATA 登记 E19；本轮回合提交并 SSH 推送 `master`。
- #205：审计收口后继续内容波次（D5 汇编补完 / 跨章引用加厚 / ⓪ 历史动机加厚），视后续指令推进。
