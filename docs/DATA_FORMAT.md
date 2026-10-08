# DATA_FORMAT · 数据格式说明

> 本文回答：**`data/` 下的文件长什么样、每个字段什么意思、口径是什么。**
> 规范（SCHEMA）见 `data/holdout_expansion/SCHEMA.md`；数据卡见 `data/holdout_expansion/DATASHEET.md`。

---

## 1. 冻结检测矩阵（1147 × 8）

**文件**：`data/blindspot_676g_detection_matrix.json`（681 标签修复后版本）

### 1.1 顶层字段

| 字段 | 含义 |
|---|---|
| `schema` | `queyi-blindspot-matrix/676g` |
| `assets` | 八资产：`asan` `ubsan` `tsan` `compiler-warn` `wunsequenced` `cross-compile` `linker` `compile-time` |
| `asset_availability` | 资产的可用性声明（哪些在本机恒 `unknown`，**必须读**） |
| `environment` | 生成环境：`local_gcc` 13.1.0 / `local_clang` 22.1.8 / `wsl_gcc` 13.3.0 / `os` win32 |
| `n_samples` | 1147 |
| `qa_verify` | 复用与挂起池的复跑一致率（80/80、10/11） |
| `matrix` | `{uid: {asset: verdict}}` 的扁平视图 |
| `samples` | 逐样本完整记录（见下） |

### 1.2 逐样本记录 `samples[]`

```jsonc
{
  "uid": "holdout:h41",
  "sample_id": "h41",
  "source_batch": "holdout",          // holdout | corpus | exp_stratified | …
  "defect_type": "other_ub",          // 34 项闭集之一
  "planted": true,                     // 是否人工植入
  "expected_verdict": "catch",         // 声明可检出性（八资产实测 OR）
  "hung_flag": false,
  "run_mode": "reuse_673r",            // reuse_673r | fresh | …
  "files": ["ub_use_after_free.cpp"],
  "per_asset": {
    "asan": {
      "verdict": "catch",              // catch | miss | unknown | contradiction
      "source": "reuse_673r",
      "wall_seconds": 1.598,
      "note": "asan 命中[...]（档位 -O0,-O2）"
    }
    // … 其余七资产
  },
  "or_verdict_available6": "catch",    // 六可用资产 OR
  "or_verdict_all8": "catch",          // 八资产 OR（含恒 unknown 的两项）
  "tsan_stability": { … },
  "qa_rerun": { … }
}
```

### 1.3 四态语义（**最关键**）

| 值 | 含义 | 能不能当负例 |
|---|---|---|
| `catch` | 至少一个资产产出诊断 | — |
| `miss` | **测了，没中** | ✅ 可以 |
| `unknown` | **没测**（资产不可用 / 判定不可行） | ❌ **不可以** |
| `contradiction` | 证据自相矛盾 | ❌ 不可以 |

> **这是本项目最容易误用的地方。** `unknown` 折叠进 `miss` 会让"能力撤退"看起来像
> "性能下降"，从而得出完全错误的结论。692 已量化：unaware 协议下 E2 报出的负例里有
> **46.95%（200/426）**其实是抓得到的。

### 1.4 两个口径的检出率

| 口径 | 分母 | 值 |
|---|---|---|
| OR 口径（全样本） | 1147 | **61.6%**（707 catch） |
| 条件 recall（expected=catch） | 674 | **94.21%**（635 catch） |

两个数字**都对**，只是分母不同。论文里必须写清用的是哪个。

---

## 2. 真实靶场矩阵（110 × 8）

**文件**：`data/683_real_world_detection_matrix.json`

结构与 §1 同构，差别：

- `source_batch` 为真实靶场批次；
- 每条带**溯源字段**（CVE ID / issue / commit URL）；
- PoC 为**单文件 <200 行**的缺陷最小重构，位于 `data/real_world/RW-*.cpp`。

> ⚠ **重构 ≠ 原始项目上下文**。真实靶场测的是"这个缺陷模式在隔离后的可检出性"，
> 不等于"该 CVE 在原始项目里的可检出性"。693-E1 正在做这一差距的量化。

配套文件：

| 文件 | 内容 |
|---|---|
| `data/683_real_world_project_matrix.json` | 按项目聚合 |
| `data/683_real_world_type_matrix.json` | 按缺陷类型聚合 |
| `data/683_real_world_candidates_verified.json` | NVD 在线验证（109/109 FOUND，应答原文冻结） |

---

## 3. 缺陷类型词表（34 项闭集）

**位置**：`data/676m_sample_manifest_corrected.json::vocabulary`
**归一化映射**：`data/681_归一化映射表.md`（56 legacy 取值 → 34 规范项）

| 粗粒度组 | 类型 |
|---|---|
| `memory_lifetime` | `memory_safety` `use_after_free` `double_free` `memory_leak` `smart_pointer` `raii_violation` `move_semantics` |
| `out_of_bounds` | `out_of_bounds` |
| `null_deref` | `null_pointer_deref` |
| `uninitialized_read` | `uninitialized_read` |
| `integer_ub` | `integer_overflow` `bit_operation` |
| `type_alias_alignment` | `type_punning` `strict_aliasing` `alignment` `endianness` `linker_odr` |
| `data_race` | `data_race` |
| `concurrency_order` | `atomic_ub` `memory_order` |
| `liveness` | `deadlock` `condition_variable` |
| `stl_iterator` | `iterator_invalidation` `stl_container_ub` `string_ub` `algorithm_misuse` |
| `virtual_or_oop` | `virtual_function` `lambda_capture` |
| `logic_or_api` | `cross_tu_ub` `logic_error` |
| `embedded_platform` | `volatile_misuse` `register_ub` `interrupt_safety` |
| `generic_ub` | `other_ub` |

> `other_ub` 是**兜底类**，不是"未知类"。693-A 的分歧分析显示 `other_ub`（n=65）贡献了
> 21/31 的分歧——这是词表分辨率不足的信号，不是标注者的问题。

---

## 4. 人类标注材料包

**位置**：`data/annotation_package/`

| 文件 | 内容 |
|---|---|
| `sample_list.csv` | 145 条匿名样本清单（`anon_id` / 文件 / 依赖） |
| `sources/S001.cpp … S145.cpp` | 去标识化源码（注释净化、标识符中性化；2 个配套 `.h`） |
| `annotation_template.csv` | 标注者填写的模板 |
| `annotation_guidelines.md` | 判定规则手册 |
| `calibration/` | 10 条校准题 + 答案 |

**密钥**：`data/689_annotation_key_mapping.json`（`anon_id` → `uid` / `defect_type` /
`expected_verdict` / `planted`）。**该文件不发给标注者**。

**693 新增**：

| 文件 | 内容 |
|---|---|
| `data/693_ai_double_label.json` | AI 双标结果（A=实测 / B=静态判读）+ κ + 分歧清单 |
| `data/693_human_adjudication_package.csv` | 31 条分歧的裁决表（`human_verdict` **留空**） |
| `data/693_annotation_guide.md` | 裁决指南（34 类定义 + 四态 + 边界 case） |
| `data/693_calibration_examples.md` | 10 条校准题（5 条有答案 + 5 条开放裁决） |

> ⚠ **已知缺陷（自曝）**：145 条里有 **13 条**源码注释残留 `expected_verdict:` 原文，
> 689 的净化脚本漏了。裁决表里标 `leak_suspected=yes`，κ 带/不带各报一次。

---

## 5. 冻结产物完整性清单

**文件**：`data/693_data_manifest.sha256`（14 项）+ `data/693_data_manifest.json`（机读）

```bash
python tools/gen_693_manifest.py            # 重写清单
python tools/gen_693_manifest.py --check    # 校验（CI 用这个）
sha256sum -c data/693_data_manifest.sha256  # 或用系统工具
```

覆盖：1147×8 冻结矩阵、A5 矩阵、真实靶场三类矩阵、34 类词表清单、类型统计、
标注密钥、reveal 产物、452 条权威账本。

---

## 6. 机器可读元数据

| 文件 | 规范 | 状态 |
|---|---|---|
| `data/croissant.json` | Croissant core 1.0 + RAI 1.0（同文件） | 官方 `mlcroissant` 加载通过（4 recordSet / 13 FileObject） |
| `data/rai_metadata.json` | RAI 展开版（与上者同源同值） | 自检 C6「同源」逐字段比对通过 |

---

## 7. 口径纪律（改数据前必读）

1. **已冻结的矩阵不改**。要改就在新批次里产出新文件，旧文件保留可追溯。
2. **新增字段要进 SCHEMA**。`data/holdout_expansion/SCHEMA.md` 是规范源。
3. **`unknown` 永不折叠进 `miss`**。
4. **分母必须写清**。61.6%（分母 1147）与 94.21%（分母 674）是同一个矩阵的两个合法读数。
5. **改了冻结产物就更新 sha256 清单**，并在验收报告里写明为什么改。
