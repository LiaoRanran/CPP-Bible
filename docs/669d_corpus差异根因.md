# 669d · 外部 corpus 35.0% vs 10.0% 差异根因（A2）

> 批次：669d　作者：LiaoRanran　日期：2026-09-30
> 事故定性：**666「81.2% 假绿」的同形态重演 —— 静默掉分**
> 结论：**根因已钉死**，且**不是**产物造假。

---

## 一、结论先行

| 项 | 结论 |
|---|---|
| 根因 | **环境依赖**：corpus 的 sanitizer 类检测（asan/ubsan/tsan）全部经 **WSL g++** 执行；WSL 不可用时，检测器**不报错、不报红**，而是把样本降级为 `unknown`，进而被排除出分母 ⇒ 静默掉分 |
| 35.0% 是否造假 | **否**。当前环境 WSL 可用，真机重跑**精确复现 14/40 = 35.0%** |
| 10.0% 如何产生 | 15 条 sanitizer 样本全部退化为 `unknown`，其中原本 catch 的 10 条消失 ⇒ `14 − 10 = 4` ⇒ `4/40 = 10.0%` |
| 与产物手工改动有关吗 | **无关**。产物 `external_corpus_reveal_665.json` 的 14 条 catch 与真机重跑**逐条完全一致** |
| 检测器版本变了吗 | **没变**。665 reveal 工具 `import` 的是 662 的 `detect()`（唯一判据版本），本审计重跑用的也是同一个函数 |

---

## 二、双实验对照（决定性证据）

重跑脚本：`C:\Users\ASUS\AppData\Local\Temp\669d_audit\a2_rerun.py`
方法：`importlib` 载入 `tools/external_corpus_662.py::detect`（判据唯一版本），
对 `load_merged()` 的 40 条 canonical 样本逐条执行；输出写临时目录，仓库零写入。

### 实验 1 · 真机重跑（当前环境，WSL 可用）

```
catch=14 miss=18 unknown=5 not_error=3 total=40
全样本口径 catch/total        = 14/40 = 35.0%
可测口径   catch/(catch+miss) = 14/32 = 43.8%
```

### 实验 2 · 模拟 WSL 不可用（monkeypatch `_wsl` 恒失败）

```
catch=4  miss=14 unknown=19 not_error=3 total=40
全样本口径 catch/total        = 4/40 = 10.0%
可测口径   catch/(catch+miss) = 4/18 = 22.2%
```

### 三方对照

| 口径 | 产物（665） | 真机重跑 | 模拟无 WSL |
|---|---:|---:|---:|
| catch | 14 | **14** | 4 |
| 全样本率 | 35.0% | **35.0%** | **10.0%** |
| 可测率 | 43.8% | **43.8%** | 22.2% |

**实验 2 精确复现了 669b 审计观察到的 10.0%**，且实验 1 精确复现了产物的 35.0%。
两条实验合起来构成**充分且必要**的因果证据链。

---

## 三、逐条差异样本（10 条被改判的 catch）

产物标 catch 的 14 条中，**恰好 10 条是 sanitizer 类**，全部在模拟无 WSL 时变为 `unknown`；
剩余 **4 条不依赖 WSL**，保持不变 —— 这 4 条正是 10.0% 的分子。

| id | detector | layer | 产物 | 真机 | 无 WSL | 判定 |
|---|---|---|---|---|---|---|
| d3-01 | ubsan | A_local | catch | catch | **unknown** | 被吞（WSL 依赖） |
| d3-03 | asan | A_local | catch | catch | **unknown** | 被吞 |
| d3-04 | asan | A_local | catch | catch | **unknown** | 被吞 |
| d3-05 | ubsan | A_local | catch | catch | **unknown** | 被吞 |
| d3-12 | cross-compile | B | catch | catch | catch | **幸存**（本机双编译器） |
| d3-23 | asan | A_local | catch | catch | **unknown** | 被吞 |
| d3-24 | asan | A_local | catch | catch | **unknown** | 被吞 |
| d3-26 | ubsan | A_local | catch | catch | **unknown** | 被吞 |
| d3-27 | ubsan | A_local | catch | catch | **unknown** | 被吞 |
| d3-28 | ubsan | A_local | catch | catch | **unknown** | 被吞 |
| d3-31 | compiler-warn | A_local | catch | catch | catch | **幸存**（本机 g++） |
| d3-33 | compiler-warn | A_local | catch | catch | catch | **幸存**（本机 g++） |
| d3-34 | compiler-warn | A_local | catch | catch | catch | **幸存**（本机 g++） |
| d3-35 | asan | A_local | catch | catch | **unknown** | 被吞 |

**10 被吞 + 4 幸存 = 14**；无 WSL 时分子只剩 4 ⇒ `4/40 = 10.0%` —— 完全吻合。

另有 5 条原本 `miss` 的 sanitizer 样本也被降级为 `unknown`（d3-21/22/25/36 + tsan d3-02），
它们不影响分子，但让 `unknown` 从 5 涨到 19，同时分母（可测）从 32 缩到 18。

---

## 四、机制剖析：为什么失败是"静默"的

`tools/external_corpus_662.py` 第 70–81 行：

```python
if kind in SAN:                                   # asan / ubsan / tsan
    w = _to_wsl(src)
    rc, out = _wsl(f"g++ -std=c++17 -O1 -g -fsanitize={SAN[kind]} -pthread {w} -o /tmp/d3bin")
    if rc != 0:
        return ("unknown", f"编译失败: {out.strip()[:60]}")   # ← 关键
```

当 WSL 不可用时，`_sh()` 捕获异常返回 `(-1, "err:...")`，于是 `rc != 0` 成立，
函数返回 **`unknown`** —— 既不是 `miss`，更不是 `error`。

而 `unknown` 在统计口径中被**排除出分母**（`denominator.meaning = catch+miss`）。
于是：

1. 样本没被检测 → `unknown`
2. `unknown` 不计分母 → 分母也缩小
3. 最终比率从 35.0% 掉到 10.0%
4. **全程没有任何一处报红**

这就是 666「81.2% 假绿」的同形态：**不是数字被写错，而是失败被降级成"不可用"，
再从分母里消失，最后以一个更低但"看起来正常"的数字呈现**。

### 为什么护栏没抓到

- `tools/tool_integrity.py --check` 校验的是**工具与数据文件的哈希**，不校验"检测器运行环境是否齐备"。
- `web_metrics_666 --check` 比对的是**产物自算一致性**（产物内部 k/n 对不对），
  它**不会重跑探测器**，因此无法发现"这次其实没真跑"。
- 665 reveal 脚本的 `honest_note` 只提示"若 A 层检出率也不高，说明问题不在缺检测器"，
  是一条**供人解读的提示**，不是可执行的硬校验。

---

## 五、四条候选假设的排除过程

| 假设 | 证据 | 判定 |
|---|---|---|
| ① 检测器版本变了 | 665 reveal `import` 662 的 `detect()`，本审计重跑用的也是它，同一函数 | ❌ 排除 |
| ② WSL 环境缺失 | 实验 2 精确复现 10.0%；被改判的 15 条**全部**是 sanitizer 类 | ✅ **确认** |
| ③ 产物手工改过 | 真机重跑 14 条 catch 与产物**逐条完全一致**（id、detector、verdict 全同） | ❌ 排除 |
| ④ `collect()` 根本没跑探测器 | `detect()` 确实编译并运行了样本（实验 1 耗时 23s，含真实编译运行） | ❌ 排除 |

---

## 六、建议修复（交给 669 工程，本批不落地）

本批红线要求"不碰 669 工程正在改的文件"，故以下为**建议**，未实施：

1. **P0 · 环境齐备性硬校验**（堵静默掉分）
   新增门禁：跑 corpus 前先探测 WSL + `g++`/`clang++` 可用性；
   任一必需环境缺失 ⇒ **直接 BLOCK**，而不是降级为 `unknown`。
   对应本批 B 段可纳入 `G-DENOMINATOR` 的扩展：环境缺失不得产生比率。

2. **P0 · `unknown` 占比阈值**
   产物 `unknown` 占比超过阈值（建议 15%）即报红。
   本次无 WSL 时 unknown 达 19/40 = 47.5%，远超阈值，可立即捕获。

3. **P1 · 分母双轨强制披露**
   产物同时给 `catch/total` 与 `catch/(catch+miss)`，文档引用时必须写明用哪一轨。
   （667 已记过一次同类问题，668 补了字段，但未堵住文档侧引用。）

4. **P1 · 探测器能力指纹入产物**
   把 `wsl_gpp` / `local_gpp` / `local_clang` 版本与"本次是否真跑"写入产物 `env`。
   holdout 的 `reveal_3_detail_668.json` 已有 `env` 字段，corpus 产物应对齐。

5. **P2 · 本地降级路径**
   为 asan/ubsan 提供非 WSL 的降级检测（如 MSVC `/fsanitize=address` 或 clang-cl），
   使 WSL 缺失时不至于整类检测归零。

---

## 七、对论文表述的直接影响

`research/paper_draft_v0.5.md` 第 563 行写"**不可复现**（审计 A3：缺 WSL 重跑得 10.0%）"。
本审计的结论应把它**修正为更准确的表述**：

> D3 外部召回 35.0%（14/40）**在具备 WSL sanitizer 的环境下可复现**；
> 该指标对运行环境**高度敏感**：WSL 缺失时 15 条 sanitizer 样本降级为 unknown，
> 比率静默掉至 10.0%。这是**测量环境依赖**，并非数字不可信。
> 论文须把"WSL g++ 13.3.0 + 本机 MinGW g++ 13.1.0 + clang 22.1.8"列为复现前提。

**这一步本批不代改论文**（红线：不碰 669 正在改的文件与 research 的既有表述），
已在验收报告中登记为待办。
