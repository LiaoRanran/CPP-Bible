# 653 验收报告（修假保护器 + 前端 P0 三样 + 收尾）

- 批次：653　状态：awaiting_review　日期：2026-09-27
- 仓库：**queyi-core**（A 修保护器，+1 提交）／**CPP-Bible**（B 前端 + C 收尾，+3 提交）
- 门禁：`python tools/run_653_gate.py` → **9/9 全 PASS**（fast / full / ruff / mypy /
  web_data selftest / **前端产物** / **跨仓保护器联调** / 受控零污染 / 信任根）

---

## 一、阶段完成

### 阶段 0 ✅ `data/653_baseline.md`
开工诊断（**实测，非猜测**）：`budget_guard` 是**真·假开关**（从不抛异常、`halted()` 与 mode 无关）；
`shadow_mode` 是**探针假象**（652 用 age=0 新规则 ⇒ 两档都 `record_only`），其真缺口是**没有拦截面**。

### A 修假保护器 ✅（最高优先级）
| 保护器 | 653 A 之前（假在哪） | 653 A 之后（真修） |
|---|---|---|
| `budget_guard_649` | `consume()` 超额只 `return allowed=False`，**从不抛**；`halted()` 与 mode 无关 | **`enforce` 超额 ⇒ 抛 `BudgetExceeded`（真·自动停）**；`halted()` **mode 感知**；新增**审计留痕** `records` |
| `shadow_mode_649` | 只有 `decide()` **给建议**，**无拦截面**（"enforce 才拦"没实现） | 新增 **`gate()` 真拦截面**：窗口内/全局 shadow ⇒ `record_only`（放行+记录）；出窗口且 enforce ⇒ **`blocked=True`**；`blocked_count` 记账 |

- **差分测试**（同输入两档行为必须不同）：新增 `tests/test_653_protector_fix.py`（8 例）+
  `test_budget_guard_649.py` 内 `test_653_differential_enforce_vs_shadow`；
  实测 `enforce=(抛,停)=(True,True)` vs `shadow=(不抛,不停)=(False,False)`。
- **B7-B10 全部真上岗验证**：`protector_rollout_652 --verify` ⇒
  `mode_switch_effective = [tool_gate_649, shadow_mode_649, circuit_breaker_649, budget_guard_649]`，**not_effective = []**。
- **连带诚实更新**：更正 652 关于 `shadow_mode` 的口径（探针假象）；更新 650/652 依赖旧语义的测试与断言；
  **补 652 遗漏**的 baseline 计数（tools 88→89、test_files 51→52，652 加了文件却未同步）。

### B 前端 P0 三样 ✅（`web/` 静态站，无后端、无构建）
**数据全部真实生成**（`tools/web_data_653.py` 从台账现算，**不造演示数据**）：
| 项 | 交付 | 真实数据 |
|---|---|---|
| **星图 hero** | `starmap.html` + `starmap.js`（+ `index.html` 首屏会动） | W2 接地模型：**178 节点**（47 卡 + 89 命题 + 42 误解）、**388 条攻击边**、**194 条被击败**、616 防御边；**声明计数与物化边精确一致**（自检断言 388 / 194） |
| **现场验哈希** | `verify.html` + `verify.js` | **Web Crypto** 浏览器内现算 sha256，与本机现算的台账（16 条真实工件）逐字节比对；**离线可用、文件不出本机** |
| **landing** | `index.html` | 首屏=**真数据渲染的会动接地图**（非截图）；暗色克制（无渐变光斑/粒子） |

**三通道编码**（任务要求）：**色=四态**（pass/pass_with_exception/fail/unknown，实测四态齐备 116/10/42/10）、
**形=类型**（大圆卡 / 小圆命题 / 方块误解）、**光=credibility**（1.0 / 0.72 / 0.5）。

**真实渲染 vs 降级**：优先 `cosmos.gl v3`（CDN, GPU）；CDN 不可达/离线 ⇒ **自动降级 2D canvas**（同一套编码与交互），
页面左下角**显式标注降级**（不假装 GPU）。

**验证**：本地 `python -m http.server` 实测 9 个资产全 **200**；3 个 JS 模块 `node --check` 全 **OK**；
graph.json 结构校验 **0 缺键 / 0 悬空边**。

### C 收尾 ✅
- `tools/run_653_gate.py` **9/9 PASS**（含前端产物检查与跨仓保护器联调）。
- 全量 pytest：**尽力跑，超时记录** —— fast 阶段 **420s 仅 9%**（与 652 的 600s→20% 一致 ⇒ 估 ~50-75 min），
  仍超 idle-timeout（证据 `data/653_fast.txt`）。
- 信任根 `--check` **4/4 OK**；受控 atoms 指纹前后一致（零污染）。

---

## 二、关键诚实登记

1. **652 的一条结论被本批更正**：`shadow_mode_649` 并非"假开关"，652 的差分探针用了 **age=0 的新规则**
   （两档都 `record_only`）⇒ **探针无法区分**。它在 653 A 之前的**真缺口是"无拦截面"**（建议有了、执行没有）。
   `budget_guard` 的"假"才是真的（从不抛异常）。两者**修法不同**，已分别修复。
2. **连带修正不藏着**：650/652 的旧断言（含"两档不可区分"的断言）已随修复更新；
   652 遗忘的 baseline 计数（tools/test_files）已补齐并注明。
3. **前端不造数据**：星图的节点/边、验哈希的台账全部来自真实文件；四态派生口径在 `graph.json.meta.four_state_rule` 里写死可查。
4. **未做**（诚实）：`canary` 真比例灰度（标签差异，G11）、全量两阶段跑完（时长，G4/652）、
   OTS 真上链（无 `ots`，G1）——与 652 的 gaps 清单一致，本批**不新增虚假完成**。

## 三、交人项
- [ ] **G11**：是否需要给保护器加 **真比例灰度**（canary 采样）——目前 canary 与 enforce 行为相同。
- [ ] 前端是否要**接入更多真实数据**（如 67 规则、PCK 证书全景）与部署（GitHub Pages / 内网静态托管）。
- [ ] 652 结转：G1 OTS 上链 / G9 challenger 接全量 67 规则 / G17 存量脏文件 / G14 verified_at 口径 / 651 三项。
- [ ] 星图"误解节点"是否应显式区分**已被击败 vs 未被击败**的图形语义（当前靠边高亮表达）。

## 四、门禁明细（9/9）
fast / full / ruff（2 文件）/ mypy（2 文件）/ `web_data_653 --check` / **前端产物（9 资产 + JSON 解析 + node --check）** /
**跨仓保护器联调（四保护器全 effective）** / 受控 atoms 零漂移 / 信任根 `--check`。
