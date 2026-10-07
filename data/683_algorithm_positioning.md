# 683-C3 · 算法创新性诚实定位（基于全枚举消融 + 7 基线）

- 生成：2026-10-07｜依据：`data/683_operator_ablation.json`、`data/683_baseline_comparison.json`
- 判定矩阵：676f 冻结（1137×8）；池 A/B/C 与 677c 相同；统计原语 673p 未改动

## 1. 事实（先摆数据，再下定位）

主预算 k=4 检出率（评估集 566，OR 口径）：

| 方法/配置 | Pool A | Pool B | 选择（A） |
|---|---:|---:|---|
| Oracle（评估集穷举，**不可达上界**） | 56.0071% | 56.0071% | asan,cw,tsan,ubsan |
| Greedy（set-cover 残余覆盖） | **56.0071%** | **56.0071%** | asan,ubsan,tsan,cw |
| E（fd_only，w_failure=1） | **56.0071%** | **56.0071%** | asan,ubsan,tsan,cw |
| E（完整四分量，等权 fncr） | **56.0071%** | **56.0071%** | asan,cw,tsan,ubsan |
| FD top-k（676f 基线） | 54.5936% | 54.5936% | asan,ubsan,tsan,cross |
| Frequency | 54.5936% | 54.5936% | 同 FD top-k |
| InfoGain | 54.5936% | 54.5936% | 同 FD top-k |
| Random（预注册单点） | 54.5936% | 39.3993% | tsan,ubsan,cross,asan |
| Static | 24.0283% | 24.735% | compiler-warn,cross(-,linker) |

（完整四分量（等权 `fncr`）与 fd_only（`fxxx`）在 A 池选择同一集合 {asan, compiler-warn,
tsan, ubsan}（顺序不同）；三个 56.0071% 与 oracle 上界并列，精确值见 JSON。
本表所有数字均可由 `python tools/analyze_683_oc.py --stage all` 复算。）

等价性（14 个 (池,k) 块的全量验证）：

- `fd_only ≡ greedy`：**14/14** 块成立（E 在 w1=1 且 novel≡failure 时**数学上就是**
  迭代残余覆盖贪心——这不是相似，是同一个算法）；
- `literal novel ≡ failure`（权重平移 `(w_f,w_n)≡(w_f+w_n,0)`）：**14/14** 块成立；
- `unique novel` 变体：11/14 块改变选择（让 novelty 成为独立信号的最小修复生效）。

## 2. 定位（诚实结论）

**主判定：增量（incremental）+ 治理（governance）为主，不是"新算法理论"。**

理由（逐条可复核）：

1. **核心选择机制等价于教科书方法**：E 的 failure 分量在迭代式中与 set-cover greedy
   完全同构（同一算法）；6/7 个基线与 FD top-k 在本数据模型下也退化为同一排序键
   （Frequency ≡ FD top-k；InfoGain 同分退化为 id 序）。这**不是需要掩饰的弱点，
   而是必须公开的事实**——它把"新颖性"从"排序公式"移到了别处。
2. **novelty 分量的字面定义与 failure 数学等价**（已给一行证明）；unique 变体是修复，
   但它带来的是"选择等价类的移动"而非检出率上界突破（5 个配置并列 56.01% = oracle 水平）。
3. **真正的贡献在别处**（这是论文主张的落点）：
   - **四态判决 + 不可达 unknown 的口径治理**：detector 不可用是 unknown 而非 miss——
     该口径直接改变"检出率"这一指标的定义域（本项目 2/8 资产恒 unknown，任何将其计入
     miss 的实现都会把结论压低 ~23pp）；
   - **失败驱动迭代的可执行化 + 可审计**：E 是确定性算子（同分 id 升序、浮点 12 位消噪），
     每步 trace 可审计，全部输入只来自派生集（无 oracle 泄漏）；
   - **全枚举消融 + 精确 Shapley + 255 子集**：把"组合选择"的可证伪性做到极致
     （这也是本批 32 配置消融的动机——不是为了找一个更高分，而是为了把等价类钉死）。
4. **不允许的表述**（自查清单，写论文时禁用）：
   - ❌ "我们提出了新的贪心算法"（等价于 set-cover）；
   - ❌ "novelty 带来独立增益"（literal 定义下不成立）；
   - ❌ "优于 SOTA 检测器组合方法"（无同类外部系统在同一矩阵上的数字——不可比）；
   - ❌ 把 oracle 的 56.01% 当作"方法达到上界"的证据（oracle 是评估集穷举，不可达）。

## 3. 对论文的处置建议（不改正文既有结论）

- 附录新增 `Operator Ablation (All 16 Configurations)` 小节：放本批 32 配置 + 7 基线的
  并排表与三条等价性（字数受限则只放 fd_only≡greedy 与 novel≡failure 两条）。
- 正文 Method 的既有表述**不动**（683 红线 3）；`Claim Boundary` 一节已含"治理为主"
  的表述，本批为其提供消融级证据。
- Related Work 建议在附录补一句：set-cover greedy 是经典方法，E 的失败分量与之同构
  已被本批显式验证（14/14 块）——把"相似性"变成"已验证的等价性"。
