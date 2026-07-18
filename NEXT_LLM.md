# NEXT_LLM.md — Phase APP 铺路文档（接手即跑，零上下文）

> **本文件是唯一入口。读完就能开始干活。不需要读 AGENT.md / HANDOVER.md / ROADMAP_v3.md。**

---

## 30 秒速览

| 问题 | 答案 |
|------|------|
| 什么项目？ | 《现代 C++ 终极圣经》— 147 章 C++ 技术书，仓库 `LiaoRanran/CPP-Bible` |
| 根目录？ | `C:/CodeLearnling/note/note/C++/CPP-Bible/` |
| 当前阶段？ | **Phase APP 应用层增强**：把全书的通用模板习题替换为章主题对齐的难度阶梯（★★/★★★/★★★★），每章追加「用法演绎」附录 |
| 做到哪了？ | **APP1–14 已完成（83 章批次 / 唯一 80 章），剩余 67 章** |
| 下一步？ | **APP15**：从 `STATE.json` 的 `execution_order` 追加 `APP15`，选下一批剩余章（见 §剩余规划） |
| HEAD？ | `eec614d`（已推送 `LiaoRanran/CPP-Bible` master，APP14 元数据提交） |
| 编译器？ | MinGW GCC 15.3：`C:/Qt/Tools/mingw1530_64/bin/g++.exe -std=c++23` |
| Python？ | `C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/python.exe` |
| PAT？ | 从项目 `.workbuddy/memory/MEMORY.md` 获取（push 用 URL 内联，remote 无 token） |

---

## 启动序列

```bash
cd C:/CodeLearnling/note/note/C++/CPP-Bible

# 1. 确认 HEAD 与远程一致
git log --oneline -3
git fetch origin master 2>/dev/null || true

# 2. 跑门禁确认基线（期望 ERROR=0 WARN=0 100/100）
python C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/python.exe tools/consistency_check.py

# 3. 检查 git 状态（应该干净，或仅有注入产生的 Book/ 修改）
git status --short
```

---

## Phase APP 核心理念

之前完成的"密度深化"（v3 审计 24.9/30）已把 147 章信息密度推到天花板，但所有章的练习题为通用模板（`max_safe` / `integral_add` / `constexpr_fact`），与章主题错配。

**Phase APP 的目标**：不是继续堆密度，而是**提升实用性**：
1. **APP-A 习题重写**：3 道难度阶梯题（★★/★★★/★★★★），每一道都跟章的核心主题绑定
2. **APP-C 用法演绎**：每章追加 `## 附录：用法演绎（从选型到落地）`，2 个工程场景
3. **APP-B 工业深挖**：少数核心章补工业实现分析（上游源码 / 编译器行为 / 性能基准）

**已完成章**通过 ## 附录：用法演绎 标记识别（grep 验证）。

---

## 🔧 添加一批新章的标准流水线

### 步骤 1：选章

从剩余章列表中选 5–8 章（一次太多会推高失败风险）。**优先选代码密集章**（STL 容器、算法、并发），延后纯叙事章（历史、版本矩阵）。

### 步骤 2：探查章结构

```bash
cd Book/partNN/
for f in ch*.md; do
  ex=$(grep -n '### 练习 1（难度' "$f" | head -1 | cut -d: -f1)
  apps=$(grep -n '^## 附录' "$f")
  echo "$f | 练习1锚点行=$ex | 附录=..."
done
```

关键判断：**附录在锚点之前还是之后？**
- **之前**（大部分章）→ 简单替换模式（锚点→EOF），天然保留附录
- **之后** → preserve 模式（需要尾边界精确截断，见 §preserve 模式）

### 步骤 3：写数据文件 `_app15_data.py`

模板参考 `_app14_data.py`（5 章示例）。每章一个 dict key，值是一个 `r"""..."""` 字符串：

```
APP15 = {
"ch76_vector": r"""### 练习 1（难度 ★★）
...（3 道习题 + 答案）...
## 附录：用法演绎（从选型到落地）
### 演绎 1：...
### 演绎 2：...
""",
...
}
```

**硬约束**（否则门禁必翻车）：
- 所有 ` ```cpp ` 块自包含、显式写全 `#include`（CI 无 PRELUDE，漏头文件 = 编译失败）
- 所有 cpp 块含 `int main`（独立可编译可抄可跑）
- 仅用 GCC 13.1 `-std=c++23` **已实现**的标准库特性（不用 C++26 / 实验性头）
- 编译错误类反例→用 ` ```text ` 围栏，运行时/逻辑错误→写成自包含可编译反例程序
- 每个 `### 练习 N（难度 ★...）` 用 `[标准] 结论：` 收尾

**代码块风格**（与历史批复一致）：
- `#include` 顺序：C 标准库→C++ 标准库，按字母序
- 类型名大写（`Buffer`/`FileGuard`），变量名小写下划线
- 用 `using` 别名或 `typedef` 不做缩写
- 禁用 `new`/`delete`（用 `unique_ptr`/`make_unique`）；禁用裸 `NULL`（用 `nullptr`）；禁用 C 风格 cast（用 `static_cast`）

**主题选择**（按章类型）：
- 语言特性章（auto/lambda/move/concepts）→ 习题聚焦特性的语法+语义+工程含义
- 容器章（vector/map/unordered_map）→ 习题聚焦性能特征/内存布局/适用场景
- 算法章（sort/find/partition）→ 习题聚焦复杂度保证/比较器/迭代器要求
- 工具链章 → 习题聚焦命令行/构建脚本/诊断工具
- 历史/叙事章 → 习题聚焦标准条款/版本对照/迁移路径

### 步骤 4：写注入脚本 `_inject_app15.py`

直接复制 `_inject_app14.py` 改三行：import 源文件、BOOK 路径、FILES 映射。

### 步骤 5：确保干净态并注入

```bash
git checkout HEAD -- Book/partNN/    # 恢复干净态（非幂等！）
python _inject_app15.py
```

### 步骤 6：双门禁验证（推送前权威）

```bash
# 门禁 1：独立全链接校验（无 PRELUDE，include-hoist，含 main 全链接）
python _verify_app15_standalone.py   # 期望：注入区全部 cpp 块 0 fail

# 门禁 2：CI 模拟（main-only -fsyntax-only，比对编译豁免清单）
python _verify_app15_ci.py           # 期望：0 新增回归
```

**首次写新批次的 verify 脚本**：直接复制最新版本（如 `_verify_app14_standalone.py`），改 FILES 列表和批次编号即可。

**如果是并发章**（part09_concurrency）：部分注入块用 `atomic`/`mutex`，独立全链接需要 `-pthread -mcx16 -latomic`。复制 `_verify_app10_standalone.py` 作为模板。

### 步骤 7：一致性门禁

```bash
python tools/consistency_check.py    # 期望：147章 ERROR=0 WARN=0
```

### 步骤 8：提交 + 推送

```bash
# 内容提交
git add Book/partNN/
git -c commit.gpgsign=false commit -m "feat(APP15): partNN 章习题重写+用法演绎 (chXX-YY)"
# ↑ 消息中注明覆盖的章号和主题范围

# 元数据回填（分两步，保证原子性）
python _update_state_app15.py        # 写 STATE.json
# 手动改 WORKLIST_v4.md（插入新的 Batch 段 + 进度表行 + 合计更新）
# 手动改 ROADMAP_v3.md（插入新的 Batch 段 + 更新滚动计划计数）
git add STATE.json WORKLIST_v4.md ROADMAP_v3.md
git -c commit.gpgsign=false commit -m "docs(state): Phase APP batch15 元数据回填"

# 推送（URL 内联 PAT）
git push "https://<FROM_PROJECT_MEMORY>@github.com/LiaoRanran/CPP-Bible.git" master
git update-ref refs/remotes/origin/master HEAD   # 同步跟踪引用
```

### 步骤 9：监测 CI

```bash
# 获取新 CI run ID
curl -sS "https://api.github.com/repos/LiaoRanran/CPP-Bible/actions/runs?per_page=1" | python -c "import sys,json;d=json.load(sys.stdin);print(d['workflow_runs'][0]['id'],d['workflow_runs'][0]['status'])"

# 启动后台 monitor（每 2 分钟轮询一次）
# 参考 /tmp/monitor_app14b.sh 模板
```

### 步骤 10：更新记忆

```bash
# 追加 .workbuddy/memory/YYYY-MM-DD.md
# 更新 .workbuddy/memory/MEMORY.md 的"当前进度"行
```

---

## 🛠 Phase APP 工具清单

| 脚本 | 作用 | 频率 |
|------|------|------|
| `_appNN_data.py` | 新批次习题+演绎数据（你手工写的） | 每批新建 |
| `_inject_appNN.py` | 注入脚本：读数据文件→替换章中锚点→EOF | 每批新建（复制上批改三行） |
| `_verify_appNN_standalone.py` | 独立全链接校验器（无 PRELUDE，include-hoist） | 每批新建 |
| `_verify_appNN_ci.py` | CI 模拟器（main-only -fsyntax-only，exempt-aware） | 每批新建 |
| `_update_state_appNN.py` | STATE.json 程序化更新（动态读 git rev-parse） | 每批新建 |

**其他非跟踪脚本**（开发记录，可能有用）：
- `_verify_app3_blocks.py`, `_verify_app4_targeted.py`～`_verify_app9_targeted.py` — 旧版靶向编译（有 PRELUDE，已被 standalone 取代）
- `_inject_app3_ch*.py` — 旧版单章注入（已被批注入取代）
- `_diag_app12.py` — 诊断脚本（行号比对，偶用）

---

## 🔬 双门禁方法论详解

### 门禁 1：独立全链接校验（`_verify_appNN_standalone.py`）

**目的**：证明注入的每个 cpp 块都可以**抄下来独立编译+链接运行**。这是"读者可抄"的红线。

**严格程度**：最高。无 PRELUDE（不预置头文件），include-hoist（标准头提升到全局，不裹命名空间），真全链接。

**工作原理**：
1. 从章文件中提取注入区（锚点→尾边界，尾边界用 `^## 附录：.*真机汇编实证` 精确匹配避免误截断）
2. 逐 cpp 块解析：找到 `#include` 行提升到文件顶部（include-hoist），去掉命名空间包裹
3. 含 `int main` 的块 → `g++ -std=c++23 -O2 -Wall -Wextra x.cpp -o x.exe`（真全链接）
4. 不含 `int main` 的块 → `g++ -std=c++23 -O2 -Wall -Wextra -c x.cpp`（仅编译，产出临时 .o）
5. **不裹命名空间**：`#include <vector>` 放 `namespace chk_x { ... }` 内非法，故必须 include-hoist

**关键修复点**：
- Windows 上 `-o os.devnull` 报 `can't create nul` → 用真实临时 .o 文件，finally 块清理
- TAIL_RE 必须精确：`^## 附录：.*真机汇编实证`，而不是宽松的 `^## 附录`（否则会误匹配注入区的 `## 附录：用法演绎` 而截断漏校验）

### 门禁 2：CI 模拟（`_verify_appNN_ci.py`）

**目的**：精确复刻 CI `compile_all.py --main-only` 的行为——仅含 `int main` 的块、原样编译无 PRELUDE、`-std=c++23 -O0 -fsyntax-only`，比 `tools/compile_exempt.json` 判定豁免。

**严格程度**：与 CI 完全一致。CI 跑的是全量 147 章，这个脚本只跑指定几章以加速——推送前确保不会引入 CI 回归。

**豁免判定逻辑**：
1. 先查 `compile_exempt.json`（64 条手动豁免 + MULTI_FILE/WINDOWS/POSIX/EXT_LIB/MODULE/MSVC/GUARDED_COMPILE 自动模式豁免）
2. 不在豁免清单中的编译失败 = 回归
3. 因正文块产生的失败（非注入区）= INTENTIONAL_ERROR（不阻挡）

---

## ⚠️ 常见陷阱与经验

### 🔴 CRLF / `core.autocrlf` 导致整文件伪 diff（最危险）
- **现象**：注入后 `git diff --stat` 显示全章 2000+ 行变更（如 ch80 `2143 +++`），实际只改了习题尾部
- **根因 A（注入器）**：用 `open().read().split("\n")` + `"\n".join()` 会把 CRLF 文件正文整文件转 LF，产生混合行尾
- **根因 B（仓库配置）**：本仓库 markdown blob 是 **CRLF**（部分章是 LF），但 `core.autocrlf=true` 让 `git add` 把工作树 clean-filter 成 LF → 与 CRLF blob 比出整文件 hunk
- **修复**：
  1. 注入器改读 bytes → 检测 `b"\r\n"` → 逐行 `replace("\r","")` 归一化 → 按检测到的行尾 join → 写 bytes（`_app_driver.py` 已修）
  2. **`git config core.autocrlf false`**（仓库级，一次性）→ 所有未来批次的 whole-file diff 消失
- **验证（必须做）**：注入后 `git add` 完跑 `git diff --cached --numstat Book/partNN/chXX.md`，确认是局部变更（如 ch80 应 ~58/35，**绝不**是 1083/1060）。`git diff`（工作树 vs 索引）在 autocrlf 下会显示整文件，看 `--cached` 才准
- **预防**：每次开新仓库/新会话先 `git config core.autocrlf` 确认 = false

### 注入脚本非幂等
- **现象**：对已注入章重复运行 → 生成多份 ## 附录：用法演绎 副本
- **修复**：`git checkout HEAD -- Book/partNN/chXX.md` 恢复干净态后**单次**注入
- **预防**：注入前先检查 `git status --short Book/partNN/` 是否干净

### preserve 模式需要精确尾边界
- **场景**：章有尾随汇编实证附录（## 附录：XX 真机汇编实证），练习锚点之后还有附录
- **错误做法**：用 `^## 附录` 作 TAIL_RE → 会误匹配注入区的 `## 附录：用法演绎` → 实际只校验了习题部分
- **正确做法**：TAIL_RE = `^## 附录：.*真机汇编实证`（仅在 part03_language 的 ch24/ch32 和 part05_oo 的 ch48/ch52 出现）
- **简单替换模式**（附录在锚点前）：TAIL_RE 用 `^## 附录` 即可（锚点后无附录，实际为 EOF）

### 缺失 `#include` 被 PRELUDE 版校验掩盖
- **现象**：旧靶向校验（`_verify_app9_targeted.py`）用 PRELUDE 预置了 22 个头文件，漏写 `#include <algorithm>` 也编译通过
- **CI 真相**：CI 的 `compile_all.py --main-only` 无 PRELUDE → 漏头文件 = FAIL
- **教训**：推送前必须用 `_verify_appNN_ci.py`（无 PRELUDE）而非 `_verify_appNN_targeted.py`（有 PRELUDE）

### ch08/09（C++23/26 特性章）GCC13.1 编译受限
- **原因**：GCC 13.1 对 C++23/26 特性支持不完整（部分用 `-std=c++2b` / `-std=c++26` 才可用，CI 用 `-std=c++23`）
- **策略**：ch08（C++23）和 ch09（C++26）放在靠后批次，届时仔细甄选能在 `-std=c++23` 下编译的子集特性
- **已覆盖**：C++20 特性（concepts/ranges/span/`<=>`/指派初始化）在 ch07 已全覆盖，均 GCC13.1 可编译

### `_update_state_appNN.py` 的 HEAD 硬编码
- **正确做法**：用 `subprocess.check_output(["git","rev-parse","HEAD"])` 动态读，不硬编码 SHA
- **原因**：元数据 commit 与内容 commit 在不同时间点执行，HEAD 会变

### STATE.json 手动 Edit 的 JSON 尾数据问题
- **现象**：手动 Edit 写 STATE.json → `Extra data` JSON 解析错误
- **正确做法**：始终用 Python 脚本程序化更新（`json.load` → 改 dict → `json.dump`）

### OO 章 / 并发章的 independent compile flags
- **语言章 / 工具链章 / 历史章**：`-std=c++23 -O2 -Wall -Wextra` 即可
- **并发章**（part09）：需要 `-pthread -mcx16 -latomic`，且 `-latomic` 在源文件之后（链接器左→右解析，放前面会被忽略）
- **调用方**：`-latomic` 是静态库，GCC 的 `libatomic.a` 在 MinGW 提供

---

## 📊 剩余规划

### 已覆盖章（91 批次 / 88 唯一章）

| 批次 | Part | 章号 |
|------|------|------|
| APP1 | part03/04/05/06/07 | 20/27/41/47/77/78/93/96 |
| APP2 | part03/04/05/06/09 | 21/31/39/42/43/44/50/51 |
| APP3 | part03/04/05/08/09 | 27/41/96/110/133 (工业深挖) |
| APP4 | part06 | 60/62/63/64/65/66/67/68 |
| APP5 | part06 | 61/69/70/71/72 |
| APP6 | part04 | 35/36/37/38/40 |
| APP7 | part03 | 19/22/23/25/28 |
| APP8 | part07 | 95/97/98/99/100 |
| APP9 | part10 | 118/119/120/121/122 |
| APP10 | part09 | 107/108/109/111/112/113 |
| APP11 | part05 | 45/46/48/49/52 |
| APP12 | part03 | 24/26/29/30/32 |
| APP13 | part02 | 11/12/13/14/15/16/17/18 |
| APP14 | part01 | 3/4/5/6/7 |
| APP15 | part07 | 79/80/81/82/83/84/85/86 |

### 剩余 59 章（推荐推进顺序）

| 优先级 | Part | 章号 | 数量 | 说明 |
|--------|------|------|:---:|------|
| **1** | part07 STL 余 | 76, 87–92, 94 | **10** | 代码密集，编译友好，价值最高 |
| 2 | part01 余 | 1, 2, 8, 9, 10 | 5 | 叙事章，习题以论述/查表为主（ch08/09 GCC13 受限） |
| 3 | part08 余 | 101 | 1 | |
| 4 | part09 余 | 110 | 1 | |
| 5 | part10 余 | 115, 116, 117, 123 | 4 | |
| 6 | part11 | 124–134 | 11 | |
| 7 | part12 | 135–143 | 9 | |
| 8 | part13 | 144–151 | 8 | |
| 9 | part14 | 152–158 | 7 | |
| 10 | part15 | 159–164 | 6 | 案例章，代码少 |
| 11 | part16 | 165 | 1 | 阅读清单，无代码 |

**建议**：APP16 继续取 **part07 STL 余**（ch76 queue_stack / ch87–92 容器与算法 / ch94 某 STL 章）——全书核心内容，编译约束最少，收益最大。

---

## 🚫 红线（不可违）

1. **不增章**：147 章上限锁定，新内容一律入附录
2. **Book/*.md 正文保持最简洁**：不加水封面/装饰性前辅文/与教学无关的导读
3. **不擅自扩写正文**：实证/习题/演绎统统入附录
4. **所有汇编必须真实编译+objdump**：绝不伪造（本文件所指为既有 _asm_demo/ 中的 53 例实证；Phase APP 不涉汇编）
5. **不编造标准/API/论文/版本号**：不确定时诚实标注
6. **不跳过门禁**：consistency_check.py 必须在每次 commit 前通过
7. **不批量推进**：每批 5–8 章，推送等 CI 绿再启动下一批（本地可并行准备但不上传）

---

## 📁 关键文件速查

| 文件 | 作用 | 接手必读 |
|------|------|:--:|
| **NEXT_LLM.md** | **本文件 —— 铺路入口（最新，唯一权威）** | ✅ |
| `STATE.json` | 进度状态 + execution_order + metrics | ✅ |
| `WORKLIST_v4.md` | Phase APP 批次明细表 + 进度总览 | 需要时 |
| `ROADMAP_v3.md` | 历史路线 + 每批回填段 + 滚动计划 | 每次改 |
| `tools/consistency_check.py` | 门禁：必跑，期望 0/0 | ✅ |
| `tools/compile_all.py` | CI 用全量编译脚本（main-only -fsyntax-only） | 不直接跑 |
| `tools/compile_gate.py` | CI 防回归门禁（比 compile_exempt.json） | 不直接跑 |
| `tools/compile_exempt.json` | 64 条编译豁免 + AUTO_PATTERNS | 参考 |
| `_app14_data.py` | 最新一批数据文件模板 | 参考 |
| `_inject_app14.py` | 最新注入脚本模板 | 复制改 |
| `_verify_app14_standalone.py` | 最新独立校验器模板 | 复制改 |
| `_verify_app14_ci.py` | 最新 CI 模拟器模板 | 复制改 |
| `_update_state_app14.py` | 最新 STATE 更新器模板 | 复制改 |
| Book/part*/ch*.md | 147 章正文 | 按批 |

---

## ⚡ 快速恢复

如果模型中途被打断（context 刷新 / 额度耗尽），新模型接手：

```
1. 读本文件（NEXT_LLM.md）
2. 读 STATE.json 确认当前 HEAD 和 execution_order
3. 跑 consistency_check.py 确认基线 100/100
4. 从 execution_order 找到最后一个 completed 的 APP 批次
5. 选下一批章（见 §剩余规划），新编 APP15 → APP16 → ... 号
6. 按 §标准流水线 走完全程
7. 不要回头重做已完成批次
```

---

_铺路时间：2026-07-17 06:48 — Phase APP 应用层增强 APP14 后_
_预计下次接手：APP15 启动（part07 STL 首批 8 章）_
_上次 CI：29503878607（APP14，HEAD eec614d）= completed success_
_前文档 NEXT_LLM.md（第三阶段 P0 任务，已作废）被本文件全面替换_
