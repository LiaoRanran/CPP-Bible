# 705-B · 失败模式结构化分类体系（Failure-Mode Taxonomy）

> 口径：基于 683 冻结检测矩阵（110 条真实缺陷，8 资产 OR 判定）与 683/688/692 归因。
> 所有失败案例均来自 `or_verdict == miss` 的 **45** 条；分类为 AI 启发式（a–f 归因）归纳，
> 逐条可复核。**这是 110 条样本上观察到的模式，不声称覆盖所有失败模式。**

## 一级分类（6 类）

| 一级 | 定义 | 在 110 条 miss 中的样本数 | 占 miss 比 |
|---|---|---:|---:|
| 逻辑型 | 缺陷是逻辑/协议/状态机错误，内存动作与 UB 事件层无可观测信号 | 30 | 66.7% |
| 并发型 | data race / 跨线程非同步访问，需 tsan + 压力重现 | 1 | 2.2% |
| 配置依赖型 | UB 子类检查未启用（无符号回绕/alignment/strict-aliasing 等） | 8 | 17.8% |
| 语义复杂型（语境保真损失） | 真实跨模块/长生命周期形态在单 TU 重构下保真度损失 | 6 | 13.3% |
| 环境依赖型 | 测量环境 profile 改变导致部分资产不可用→捕获丢失（692 配对实验） | 跨样本（见统计） | — |
| 平台特定型 | 资产可用性受 OS/工具链约束（wunsequenced/compile-time 恒 unknown；linker 仅多 TU 触发） | 结构性 | — |

## 二级分类与案例

### 逻辑型（30 条）
- **协议/状态机误判**：CVE-2021-41773（Apache 路径规范化绕过）、CVE-2021-22946（curl STARTTLS 降级）、CVE-2022-32221（curl 307 改方法）
- **身份认证/权限绕过**：CVE-2018-15473（OpenSSH 用户枚举时序 oracle）、CVE-2019-13272（Linux ptrace suid）、CVE-2022-26691（CUPS 前缀匹配）
- **解析/资源语义**：CVE-2016-3714（ImageMagick ImageTragick 命令注入）、CVE-2016-1897（FFmpeg 任意文件读）、CVE-2022-1941（protobuf 递归深度绕过）
- **非终止/挂起**：CVE-2022-0778（OpenSSL BN_mod_sqrt 无限循环→超时 miss）

### 并发型（1 条）
- **跨线程 data race**：CVE-2016-8655（Linux AF_PACKET setsockopt race，tsan 在单 TU 重构下亦未触发）

### 配置依赖型（8 条）
- **整数溢出子类未启用**：CVE-2018-13785（libpng height*rowbytes）、CVE-2021-33909（Linux seq_file size_t 下溢）、CVE-2021-3490（Linux eBPF ALU32）、CVE-2012-2677（Boost pool 乘积溢出）
- **type punning / alignment 未启用**：CVE-2023-0286（OpenSSL X.400 联合体）、CVE-2021-30551（Chromium/V8 Map 混淆）、CVE-2020-16040（Chromium/V8 整数回绕假设）

### 语义复杂型（语境保真损失）（6 条）
- **真实跨模块 OOB 重构损失**：CVE-2023-4911（glibc Looney Tunables）、CVE-2021-23017（nginx resolver CNAME 越界）、CVE-2022-0185（Linux legacy_parse_param）

### 环境依赖型（692 配对实验，跨样本）
- 同 OS 换编译器几乎无感（689：一致率 93.5%、Δ≤2pp）；换 **deployment profile** 是灾难性的：
  A5 566 帧 catch 60.07% → 24.74%（−35.34pp），真实靶场 110 catch 59.09% → 23.64%（−35.45pp）。
- 丢失的捕获里 200/340（A5）与 39/65（真实靶场）是同一工具在声明 profile 下**能抓到的真阳性**——
  静默退化的指纹是 `Δunknown = 0.00pp`（"没测"被写成"测了没中"）。

### 平台特定型（结构性）
- `wunsequenced`/`compile-time` 在 8 资产池中**恒 unknown**（本机 MinGW 不认 -Wunsequenced / 无本地检测器），对 OR 零贡献。
- `linker` 在真实靶场 110 条（均为单 TU 重构）上 **0 catch**——其触发面（ODR/多定义）缺失，属"资产适用面收窄"的坦白项。

## 诚实边界
- 一/二级分类为启发式归纳；环境依赖型与平台特定型是**跨样本/结构性**失败模式，不以单条案例计数。
- 不声称"找到所有失败模式"——仅声明"在 110 条样本中观察到上述 N 种模式"。
