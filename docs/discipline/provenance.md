# C3 · provenance 规范（666 批）

> 适用：所有**进入判决**的事实 —— 卡、证据、编译产物、外部语料条目、审计记录。
> **一句话**：一条事实必须能回答三个问题 —— **谁产的**、**凭什么说是真的**、**别人怎么复算**。
> 答不上任意一条，它在这套系统里的状态就是 `unknown`，不是 `pass`。

## 1. 卡面 provenance（字段级）

| 字段 | 谁写 | 含义 | 缺失后果 |
|---|---|---|---|
| `status` | 生成者起草，人签升级 | `draft` → `machine-verified` → `verified` | 缺 ⇒ `ATOM-FM-REQUIRED` 判 warn/block |
| `status_history[]` | 每次状态跃迁追加 | 每步 `{level, at, by}`；`by` 必须写 `machine:writer` / `machine:gate` / `human:<名>` | 缺 ⇒ `ATOM-STATUS-TRANSITION` 判红 |
| `verified_by` | **唯人** | `human:<名>`；机器**不得**写此字段 | 机器自置 ⇒ `ATOM-NO-UNVERIFIED` 判红 |
| `verified_at` | 人 | 与 `verified_by` 同批 | 同上 |
| `sources[]` | 生成者 | `{kind, ref, independent}`：`independent=false` 表示二手转述 | 缺 ⇒ 该断言的证据链降级为 `unknown` |
| `first_hand` | 生成者 | 是否本机实测（不是"书上说"） | 缺 ⇒ 不得作为 L1 证据 |
| `evidence[]` / `evidence_refs[]` | 生成者 + 验证者 | 指向 `evidence/**/EV-*.md` | 缺 ⇒ `OBSERVATION-NEEDS-ARTIFACT` 判红 |

**外部依据必须可点开**：`external_basis` / `sources[].ref` 要给到**条款号或条目**（如 `ISO/IEC 14882:2023 [atomics.order]`），
只写"标准规定"等于没有出处。

## 2. generator / verifier 分离

- **生成者**（`extracted_by: writer`）：产出 `claim` / `claim_structured` / `sources`。
- **验证者**（`machine:gate` 或人）：产出 `verdict` / 证据引用 / 反例。
- **同进程产出的"独立验证"不算独立**：664 的 A/B/C 三方同上下文，自己就登记为"非真正独立"（666 沿用这条判断）。
  真要独立，需要**交互日志**或**盲测**（未做）。

## 3. 证据 provenance（`evidence/**/EV-*.md`）

| 字段 | 含义 | 红线 |
|---|---|---|
| `fixture` | 真实可编译文件（相对路径） | 夹具缺失 ⇒ `EV-ARTIFACT-FILE-EXISTS` 判红 |
| `matrix.{compiler,std,opt,arch}` | 实测口径三元组 | 值域校验（`_RE_MX_OPT` 等）：`-O9` 这类**不存在的档位**判红 |
| `artifact` 声明（producer/version/OUT） | 谁产的、哪个版本、输出在哪 | 未声明 ⇒ `EV-ARTIFACT-PRODUCER` / `EV-OUT-UNDECLARED-KEY` 判红 |
| `serves` | 该证据服务哪些断言 | 指向不存在的断言 ⇒ `EV-SERVES-EXIST` 判红 |

**落盘位置**：`data/evidence_store/`（内容寻址）。**L1 = 多编译器确认**，**L2 = 单编译器** ——
等级由**实际跑过几个编译器**决定，不由作者声明。

## 4. 外部语料条目

- `source` 只写到**类别级**（`verified_source: true/false`）。
- `verified_source=false` 的条目**未在本机验证过** ⇒ 它在结论里只能作**对照样本**，不得作为"外部系统确有此错"的证据。
- 禁止为凑数编造具体 issue 编号（662 的诚实声明，666 沿用）。

## 5. 供应链 provenance

- `data/supply_chain/merkle_roots.json`：目录级 Merkle 根（路径绑定 + 计数绑定），每次受控目录变更后**必须重钉**。
- `data/supply_chain/*.ots`：锚点。**占位 ≠ 锚定**：占位文件没有 attestation，
  必须同时存在 `*.ots.placeholder.md` 登记（含当前台账 sha256 + "未上日历"声明），
  真锚后**删除占位登记**（`test_ots_anchor_656` 的占位通道随之关闭）。
- `data/transparency_log.jsonl`：哈希链 + 在册凭证。VSA 的 **记录完整性（HMAC）** 与
  **输入是否仍等于当前工作区** **必须分列**——后者对历史条目为 false 是正常的（追加式日志记历史），
  混在一起会把"工作区演进"误报成"凭证无效"。

## 6. 反例（这些都不是 provenance）

- ❌ "书上写过" —— 无条款号、无版本、无页码。
- ❌ "我跑过，输出是 X" —— 无命令、无档位、无编译器版本。
- ❌ "LLM 说这是 UB" —— AI 产出必须走 C4 的 AI 使用日志 + 人工验证。
- ❌ "机器已验证" —— `verified` 唯人签；机器只能到 `machine-verified`。
- ❌ "占位 .ots 就是锚定" —— 没有 attestation 就没有时间证明。
