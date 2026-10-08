# 692-A · EnvironmentProfile 形式化与 measurement_context_id

- 批次：692｜执行：CodeBuddy（AI）｜生成：2026-10-08
- 配套：`data/692_environment_paired_experiment.json`（现算数值）、`data/692_environment_report.md`（科学发现叙述）、
  `tools/analyze_692_environment.py`（确定性复算，**不调用 detect()**）
- 上游：`data/689_environment_experiment_design.md`（三组件口径首次落地）、
  `data/688_reproducibility_quantification.json`（无 WSL 聚合数）

---

## 0. 一句话

> **环境不是复现细节，是测量的一个坐标。** 一条不含环境坐标的测量记录，
> 既无法与另一条记录比较，也无法知道自己**是否真的测了**。

两轮外部评审把"WSL 依赖"从工程瑕疵抬升为科学问题：**省略环境信息的协议会让不完整测量冒充有效测量**。
本条形式化的目标就是让"省略"变成**语法上不可能**：任何一条测量记录都必须携带完整的环境坐标。

---

## 1. EnvironmentProfile（15 字段，缺一即不完整）

| # | 字段 | 语义 | `wsl-gcc-13.3`（E1，实测） | `windows-native-mingw`（E2，实测） |
|---|---|---|---|---|
| 1 | `os` | 操作系统与发行版 | Ubuntu 24.04.4 LTS (WSL2) | Windows 11 (10.0.26200) |
| 2 | `kernel` | 内核标识 | 6.18.33.2-microsoft-standard-WSL2 | NT 10.0.26200 |
| 3 | `architecture` | 架构 | x86_64 | x86_64 (AMD64) |
| 4 | `compiler` | 编译器产品 | g++ (Ubuntu 13.3.0-6ubuntu2~24.04.1) | g++ (MinGW-Builds x86_64-posix-seh-rev1) + clang 22.1.8 |
| 5 | `compiler_version` | 版本 | 13.3.0 | 13.1.0 / 22.1.8 |
| 6 | `stdlib` | C++ 标准库 | libstdc++ (GCC 13.3) | libstdc++ (MinGW 13.1.0) |
| 7 | `libc` | C 运行库 | glibc 2.39-0ubuntu8.9 | msvcrt（target x86_64-w64-mingw32） |
| 8 | `sanitizer_runtime` | sanitizer 运行时 | libasan/libubsan/libtsan (GCC 13) | **无**（MinGW 不带 ASan 动态运行时） |
| 9 | `linker` | 链接器 | GNU ld (binutils) 2.42 | GNU ld (MinGW binutils) |
| 10 | `optimization` | 优化档位 | {-O0, -O2} | {-O0, -O2} |
| 11 | `compile_flags` | 编译期标志 | `-std=c++17 -g -fsanitize=<asset> -fno-omit-frame-pointer` | `-std=c++17 -Wall` |
| 12 | `runtime_flags` | 运行期标志 | `ASAN_OPTIONS/UBSAN_OPTIONS/TSAN_OPTIONS`（688 档位） | 不适用 |
| 13 | `timeout_s` | 超时 | 60 | 60 |
| 14 | `resource_limits` | 资源限制 | 未设硬限（进程内超时） | 未设硬限 |
| 15 | `container_image` | 容器镜像 | `null`（未容器化） | `null`（未容器化） |

**附加两个非环境字段（协议元数据，参与哈希但语义不同）**：
`supported_assets`（该 profile 下**环境实际支持**的资产集）、
`provenance`（指纹来源命令，可复核：`wsl -d Ubuntu -- bash -c 'uname -r; g++ --version; ldd --version; ld --version'`）。

> **`container_image = null` 是诚实登记**：两条 profile 都未容器化（本机无 Docker，687 已登记）。
> 因此"可复现"的强度上限是**指纹级**（记录 + 命令可复核），不是**镜像级**（sha256 可重建）。

---

## 2. measurement_context_id

```
measurement_context_id =
    "mc1_" + sha256( canonical_json{
        sample_hash,                    # 样本字节的 sha256（不是文件名）
        asset,                          # "<asset_id>@<asset_version>"，如 "asan@gcc-13"
        environment_profile,            # §1 的 15 字段 + supported_assets
        configuration,                  # 该次调用的档位/检查集/超时，如 {"optimization":"-O2","timeout_s":60}
        protocol_version                # "queyi-measurement-protocol/692"
    } )[:32]
```

规范化规则（写死，否则哈希无意义）：
1. `json.dumps(..., sort_keys=True, separators=(",", ":"), ensure_ascii=False)`；
2. 文本 UTF-8 编码；无 BOM；
3. 字段**只增不改**：新增字段必须同时进 `protocol_version` 的版本号，否则旧 id 语义漂移。

### 2.1 不变式（本批实测，见 JSON `measurement_context_id.invariants`）

| 不变式 | 结果 |
|---|---|
| 同一语境 ⇒ 同一 id | ✅ 同 profile 同资产同配置重复计算一致 |
| 换环境 ⇒ id 变 | ✅ `wsl-gcc-13.3` = `mc1_68cad50a…` vs `windows-native-mingw` = `mc1_7a1269cf…` |
| 只换优化档 ⇒ id 变 | ✅ `-O2` = `mc1_68cad50a…` vs `-O0` = `mc1_d2494545…` |
| 只换样本字节 ⇒ id 变 | ✅ `sample_hash` 进哈希 |

**语义**：同 id ⇒ 同一条测量记录，结论可继承；**id 不同 ⇒ 旧结论对新语境不继承**。
这条规则是 666 事件（"改了代码没重跑、数字还被引用"）在**语境**维度的推广：
那类事故的根因是"报表只对字段、不对语境"。

---

## 3. 两类缺口必须分开（本批最容易被搞混的一点）

8 资产池里，缺失的资产有两种**性质完全不同**的来源：

| 类别 | 资产 | 性质 | 在两个 profile 中的表现 | 是否改变结论 |
|---|---|---|---|---|
| **静态未实现** | `wunsequenced`、`compile-time` | 项目**本来就没有实现**（声明性资产） | E1/E2 都记 **asset-level unknown = 100%**，冻结矩阵逐资产可见 | **不改**（已公开登记的能力边界） |
| **环境门控** | `asan`、`ubsan`、`tsan` | 实现了，但需要 Linux 运行时 | E1 全支持；E2 **未运行** | **改**（unaware 协议下被静默写成 miss） |

形式化：

```
P          = 声明 profile 的资产集（本项目为 8 资产）
S(prof)    = 该环境下**实际支持**的资产集（capability closure）
G_env      = (P ∩ ENV_GATED) \ S(prof)   # 环境门控缺口 —— 只有这一项造成「静默退化」
G_static   = P \ (ENV_GATED ∪ S(prof))   # 静态未实现缺口 —— 两 profile 同等缺，逐资产可见
```

**记账规则（本批的核心新规则）**：

```
or_verdict(per_asset, S, aware):
    if 任一 a ∈ S 的 verdict == catch:            return catch
    if aware 且 G_env ≠ ∅:                        return unknown   # ← 缺测量，不是缺检出
    if 全部 a ∈ S 的 verdict == unknown:           return unknown
    return miss
```

`aware=False` 时为**冻结矩阵逐字口径**（`data/a5_676f_detection_matrix.json.aggregation`：
"任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss（unknown 不当 miss）"）——
本批在真实 110 上复算得 65/26，与 688 记录的 `full_or_catch=65` / `cross_platform_or_catch=26` **逐位一致**
（见 JSON `anchor_check_vs_688.pass = true`），证明本脚本与上游同口径。

**为什么静态未实现缺口不触发 aware 规则**：它是**已知且公开**的能力边界，逐资产可见，
两个 profile 一视同仁；把它也算成"不可信负例"会让连 E1 都失去可信负例，
从而**掩盖**真正要研究的环境门控缺口。这是刻意选择，不是疏漏。

---

## 4. 三组件指标的定义（aware / unaware 两套记账共用）

| 指标 | 定义 | 分母为 0 时 |
|---|---|---|
| `catch_rate` | `catch / total` | — |
| `unknown_rate` | `unknown / total` | — |
| `conditional_recall` | `catch / (catch + miss)` | **定义为「不可计算」**（不是 0%，也不是 100%） |

**`conditional_recall` 是本文最脆弱的一个数字**：它是"工具在能测的东西上抓到了多少"，
一旦环境把负例变成 unknown，分母只剩"可信负例"。当 `G_env ≠ ∅` 时：
- 若按 aware 严格记账 ⇒ 分母 = 0 ⇒ **不可计算**（唯一诚实的答案）；
- 若只按"能力相关的缺失"筛负例 ⇒ 分母被**筛到只剩 0** ⇒ 数字反而变成 **100%**（分母病理的反向形态，见报告 §4）。

⇒ **单一 recall 数不足以描述一次测量**。最小充分口径 = 三组件向量 + 能力边界声明。

---

## 5. 与论文 measurement tuple 的挂接（**只写建议，不改正文**）

| 论文位置 | 建议 |
|---|---|
| §2 measurement tuple | 把 `e`（environment）从"复现细节"升为正式分量；附 §1 的 15 字段表 |
| §2 | 给出 `measurement_context_id` 公式与不变式（§2.1），作为"记录可继承性"的语法判据 |
| §5.3 Finding 3 | 引用 692 配对结果（E1/E2 三组件 + ΔE/ΔU + McNemar），并注明 `conditional_recall` 在 E2 **不可计算** |
| §7 威胁 T3 | 环境有效性：`container_image = null`（指纹级而非镜像级）、MSVC 缺失、E2 的负面不可信 |
| 附录 | §3 的两类缺口表 + §4 记账规则伪码 |

正文修改由统一批次合并；本文件只是**给统一批次的输入**（红线 2 已遵守：本批 0 处正文改动）。

---

## 6. 复算与诚实边界

- 复算：`python tools/analyze_692_environment.py`（标准库、无随机数、只读冻结矩阵、不跑 detect）；
- 断点：E2 的 3 个可用资产是**实测**（在 Windows 上真跑过并冻结进矩阵）；
  E2 的 `unknown` 是**协议层判定**（"声明了但没测"），**不是**对未运行资产行为的推断；
- `container_image = null`、MSVC/clang-cl 缺失、Docker 未实测 —— 三项均为**已知缺口**，用户如需可复查，但**不要当成已解决**；
- `type-relevant` 可信性分析（报告 §4）用的是 **derivation split 估能力图、evaluation split 上评**，
  仍是**探索性**指标（同源样本，非独立），不作为主结论。
