# 615 B3 · 判决尺子全集入根报告

> 依据 `_arch_v19/03_元验证层.md`（11 关键尺子中 8 个裸露）与探针 `p03`。铁律：只跑 `tool_integrity.py --update`（唯一允许的 integrity 命令）。

## 一、保护集变化
| | 前 | 后 |
|---|---|---|
| 受保护文件 | **12** | **22** |
| 分节 | core 5 + test_config 2 + supply_chain 5 | 同上 **+ ruler 10** |
| `.tool_checksums` 行数 | 15 | **25** |

## 二、新增判决尺子（ruler 节 · 10 个）与理由
| 尺子 | 为什么是判决尺子 |
|---|---|
| `mutation_fuzz.py` | 变异**发现器**：改它可让逃逸样本消失（攻击面定义） |
| `golden_lock.py` | 决定**质量基线**：改它可让恶化不红 |
| `replay_invariants.py` | 决定 **replay 不变量**（pass/fail 判据） |
| `d5_compile_gate.py` | D5 **编译门**（判据） |
| `d5_runtime_gate.py` | D5 **运行门**（判据） |
| `d5_source_integrity.py` | D5 **源完整性**（判据） |
| `attack_edge_generator.py` | **攻击边生成**：决定 W2 论证图结构 |
| `bkt_solver.py` | **BKT 求解**：决定学习者掌握度判决 |
| `learner_mastery_update_613.py` | **掌握度更新**：决定学习者判决 |
| `tool_integrity.py` | **元校验器自身**（"怎么算"即可被篡改） |

## 三、口径
- ruler 节**内容变更或缺失都算红**（同上 test_config 节；尺子必须存在且不被静默改）。
- `--check` 默认同时校验 core + supply_chain + **ruler**（+ Merkle 根）。
- 旧格式基准（无 `# ruler` 节）⇒ 只**警告**（向后兼容），跑 `--update` 补齐。

## 四、仍未保护及原因
- 其余 `tools/*.py`（204 个中的辅助工具）：只生成报告不决定判决，纳入成本高、收益低。
- `.tool_checksums` **自身**不纳入（递归无解）——其可信度依赖 git 历史。
- **自举悖论**（诚实）：`tool_integrity.py` 校验别人也校验自己，扩大 checksum 只是把信任根再挪一格
  （挪到 git/本地）；单用户无密钥下信任根不可真正闭环——元验证提高攻击成本，不创造新信任主体。

## 五、重要声明
> **纳入保护后，这些尺子的任何修改都必须同 commit 运行 `python tools/tool_integrity.py --update` 重钉
> `.tool_checksums`**，否则 `--check` 会红（这是设计目标：改判定核心必须显式留痕）。

## 六、边界
- 本批**只**改 `tools/tool_integrity.py`（加 ruler 节）并 `--update`；**未跑 `--check`**（615 铁律）。
- 未改 CORE_TOOLS 的其他文件；未改受控目录。
