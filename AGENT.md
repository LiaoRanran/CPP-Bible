# AGENT.md — C++ Bible 永恒入口

> **接手者优先读 `NEXT_LLM.md`**（一键接手）→ 本文件是项目宪法，仅供参考。
> **进度追踪**：读 `STATE.json` 获取当前任务状态。
> **详细任务**：读 `WORKLIST_v4.md` 获取 45 子项完整拆分。

## 核心理念

```
第三阶段：质量收尾 + 高含金量升级（2026-07-14 启动）
前两阶段（密度深化 + I.实战 + 汇编实证）已竣工。
当前目标：提升可信度——把编造的数字变成真实数据。
每批 5 项，不间断推进，直到额度燃尽。
```

## 🚨 五条红线（禁止事项）

1. **禁止编造数据**：[示意] 标记的数据必须替换为真实 benchmark 结果
2. **禁止增加章节数**：150 上限，新内容追加到附录或独立文件
3. **禁止幻觉**：WG21 提案号、库版本、平台差异必须可查证
4. **禁止批量单行追加**：每条新内容 ≥5 行，有信息增量
5. **禁止伪造汇编**：书中 asm 块必须来自真实 objdump 产物（`_asm_demo/`）

## 🎯 当前方向（第三阶段 P0 优先）

| 任务 | 说明 | 状态 |
|------|------|------|
| P0-2 编译器矩阵 | 218 处对比 → `docs/compiler-matrix.md` | ⬜ |
| P0-3 UB 库 | 15 例反例 + sanitizer 输出 | ⬜ |
| P0-1 实测化 | 353 处 [示意] → Google Benchmark | ⬜ |
| A1 交引审计 | 147 章全量引用修复 | ⬜ |
| A2 CI 豁免 | 35 豁免审计消化 | ⬜ |

## 🛠 核心命令

```bash
python3 tools/consistency_check.py          # 门禁，每批必跑，期望 0/0
python3 tools/chapter_compile_check.py Book/partXX/chYYY.md  # 单章编译
python3 tools/compile_all.py --main-only     # 全量编译（非 P0 任务可跳过）
python3 tools/crossref_audit.py              # 交引完整性

# 编译器
C:/Qt/Tools/mingw1530_64/bin/g++.exe -std=c++23 -O2 -c -o X.o X.cpp
C:/Qt/Tools/mingw1530_64/bin/g++.exe -std=c++23 -O2 -fsanitize=address,undefined X.cpp -o X.exe
C:/Qt/Tools/mingw1530_64/bin/objdump.exe -d X.o
```

## 📋 工具链速查

| 工具 | 作用 | 第三阶段是否用 |
|------|------|:---:|
| `consistency_check.py` | 门禁：每批必跑 | ✅ 每次 |
| `chapter_lint.py` | 单章质量 | 🔲 按需 |
| `crossref_audit.py` | 交引完整性 | ✅ A1 用 |
| `compile_classify.py` | 编译分类 | 🔲 A2 用 |
| `density_audit.py` | v3 密度审计 | 🔲 最终验收 |
| `chapter_compile_check.py` | 单章编译 | 🔲 P0-3 用 |
| `compile_all.py` | 全量编译 | 🔲 A2 修复后 |

## 📁 文档矩阵

```
NEXT_LLM.md          ← 🆕 一键接手入口（明天模型先读这个）
STATE.json            ← 🆕 进度状态追踪
WORKLIST_v4.md        ← 🆕 第三阶段 45 子项完整清单
AGENT.md             ← 项目宪法（本文件）
ROADMAP_v3.md        ← 历史路线 + §10 阶段规划
HANDOVER.md          ← 快照（较旧，可略）
```

## ⚙️ 工作纪律（第三阶段）

- **接手后**：读 NEXT_LLM.md → 读 STATE.json → 跑 consistency_check.py
- **每完成一批**：跑门禁 → git commit + push → 更新 STATE.json → 追加记忆日志
- **不中断**：完成一批后立即读 state.json 取下一个任务，不问用户
- **额度燃尽**：先 commit+push 当前进度 → 更新 STATE.json → 停下来

## 🏁 接续模型行动指南（精简版）

1. **读 `NEXT_LLM.md`** → 30 秒速览，知道自己在哪
2. **读 `STATE.json`** → 知道什么已完成、什么正在进行
3. **跑 `consistency_check.py`** → 确认基线 100/100
4. **从 `execution_order` 数组取第一个 `status=pending` 的任务** → 开始做
5. **做 → 验证 → 提交 → 更新 state → 下一个** → 循环直到燃尽

## 📊 当前状态（2026-07-14 终检）

| 类别 | 数值 | 状态 |
|------|------|:--:|
| 章节 | 150 章，148,529 行 | ✅ |
| 代码块 | 6,845 cpp（91% 有意义） | ✅ |
| 密度 v3 | avg 24.9/30, shallow=0, 十维全非零 | ✅ |
| I.实战 | 63/150 章覆盖 | ✅ |
| 汇编实证 | 8 例 GCC15 真实 objdump | ✅ |
| 编译通过 | 112/150 (35 豁免) | 🟡 |
| 一致性 | 31 次连续 100/100 | ✅ |
| [示意] 残量 | 353 处待替换 | 🔴 |
| WORKLIST 进度 | 0/45 子项 | ⬜ |

**结论**：规模与结构已就位，可信度是唯一短板——353 个编造数字是当前最大质量问题。第三阶段核心工作：用真实数据替换每一个 [示意]。

---

_最后更新：2026-07-14 19:05 — 第三阶段启动，NEXT_LLM.md + state.json 就位_
_代际：第 5 代 Agent（WorkBuddy → Hy3 → Phase3-Auto）_
