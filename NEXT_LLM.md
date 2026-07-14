# NEXT_LLM.md — 接手即跑，零上下文启动

> **读这个文件 = 知道一切。不需要读其他文件就能开始干活。**

---

## 30 秒速览

| 问题 | 答案 |
|------|------|
| 什么项目？ | 《现代 C++ 终极圣经》— 150 章 C++ 技术书 |
| 在哪？ | `C:/CodeLearnling/note/note/C++/CPP-Bible/` |
| 当前阶段？ | 第三阶段：质量收尾 + 高含金量升级 |
| 下一步做什么？ | **按 P0→A→B→C 顺序，读完 STATE.json 取第一个未完成项** |
| 做到什么时候？ | 额度燃尽或所有任务完成。**不要问用户，一直做** |
| 需要什么工具？ | GCC15：`C:/Qt/Tools/mingw1530_64/bin/g++.exe`；Python：`C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe` |
| 怎么提交？ | `git -c http.sslBackend=schannel push`（PAT 从项目记忆/工作记忆获取，不写死在文件中） |

---

## 🚀 启动序列（每次接手必跑）

```bash
cd C:/CodeLearnling/note/note/C++/CPP-Bible

# 1. 读状态文件
cat STATE.json

# 2. 跑门禁确认基线
python3 tools/consistency_check.py

# 3. 检查 git 状态
git status
git log --oneline -5
```

---

## 📋 任务队列（严格按此顺序执行）

所有任务在 `WORKLIST_v4.md` 中有详细子项拆分。STATE.json 记录完成状态。

### P0 级（不做完不往下）

| 序号 | 任务 | 类型 | 关键文件 |
|------|------|------|----------|
| **P0-2** | 编译器版本矩阵表 | 扫描→建表→注入 | `docs/compiler-matrix.md` |
| **P0-3** | 反例/UB 库（3 批 × 5 例） | 写代码→编译+sanitizer→写文档 | `Book/appendix_ub/` |
| **P0-1** | 性能实测化（3 批） | 装 Google Benchmark→重写→跑→注入 | `Benchmarks/` |
| **A1** | 交叉引用审计 | 扫描→修复 | `tools/crossref_audit.py` |
| **A2** | CI 豁免消化 | 审计→修复→更新豁免清单 | `tools/compile_exempt.json` |

### P1 级（P0 全部完成后再碰）

| B2 | Interview 嵌入式分类 | `Interview/embedded/` |
| B3 | WG21 提案跟踪表 | `WG21/TRACKER.md` |
| B4 | 汇编实证扩展 | Book/ 追加附录 H |
| B1 | v1.1.0 发布 | CHANGELOG + tag + Release |

### P2 级（最后做）

| C1-C3 | 术语/Mermaid/编号 | 扫描→修复 |

---

## 🔧 每种任务的标准化流水线

### 类型 A：纯文档任务（P0-2 / B2 / B3 / C1-C3）

```
1. 读 WORKLIST_v4.md 对应子项 → 确认具体文件/脚本
2. 写/改文件
3. 跑 consistency_check.py → 必须 0/0
4. git add + commit（含任务说明）
5. git push
6. 更新 STATE.json（标记完成）
7. 追加记忆日志 .workbuddy/memory/YYYY-MM-DD.md
8. 读 STATE.json → 取下一个未完成任务 → 继续
```

### 类型 B：编译+实证任务（P0-3 UB 库 / P0-1 benchmark / B4 汇编）

```
1. 读 WORKLIST_v4.md 对应子项 → 确认目标章节
2. 写 .cpp 测试文件到对应目录
3. 编译：g++ -std=c++23 -O2 -c -o X.o X.cpp（或加 -fsanitize=address,undefined）
4. 运行/反汇编：objdump -d X.o（或 ./X.exe for sanitizer）
5. 捕获输出 → 写入 Book/ 附录
6. 跑 consistency_check.py → 必须 0/0
7. git add + commit + push
8. 更新 STATE.json
9. 追加记忆日志
10. 继续下一个
```

### 类型 C：扫描+修复任务（A1 交叉引用 / A2 CI 豁免）

```
1. 跑对应审计脚本
2. 收集问题列表
3. 逐项修复（每修复一项 verify 一次）
4. consistency_check.py final
5. git add + commit + push
6. 更新 STATE.json
7. 继续
```

---

## 🚫 关键规则

1. **不询问用户**：不要问"要不要继续？""这个方向对吗？"——直接做
2. **不跳过门禁**：每次 commit 前必须 consistency_check.py 0/0
3. **不扩章**：150 章上限不变，新内容追加到附录或独立文件
4. **Book/*.md 最简洁**：正文保持精简，不要装饰性前言/水词
5. **每批 5 章/5 例**：保持今天已验证的节奏
6. **状态及时存**：每完成一个子项立即更新 STATE.json
7. **额度燃尽时**：先 commit+push 当前进度，再更新 STATE.json，最后停下来

---

## 📁 文件速查

| 文件 | 作用 | 接手必读 |
|------|------|----------|
| `NEXT_LLM.md` | **本文件 —— 接手入口** | ✅ |
| `STATE.json` | 进度状态 | ✅ |
| `WORKLIST_v4.md` | 45 子项详细清单 | 需要时 |
| `AGENT.md` | 项目宪法（工具链/红线） | 需要时 |
| `ROADMAP_v3.md` | 历史路线 + 阶段规划 | 需要时 |
| `HANDOVER.md` | 快照 | 需要时 |
| `Book/` | 150 章正文 | 按任务 |
| `tools/` | 30+ 工具脚本 | 按任务 |
| `_asm_demo/` | 汇编实证产物 | 不需要 |
| `Benchmarks/` | 性能测试 | P0-1 需要 |

---

## ⚡ 快速恢复

如果模型中途被打断（context 刷新 / 额度耗尽），新模型接手只需：

```
1. 读 NEXT_LLM.md
2. 读 STATE.json
3. 跑 consistency_check.py
4. 从第一个 status=pending 的任务继续
5. 不回头重做已完成的任务
```

---

_最后更新：2026-07-14 19:00 — 第三阶段启动_
_预期下次模型接手时间：2026-07-15_
