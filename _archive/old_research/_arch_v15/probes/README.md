# probes/ — 597 手搓实验索引

> 全部为纯标准库、只读探针；只读扫仓库 atoms/ misconceptions/ data/，输出本目录下的调研产物（非仓库正式文件）。

## probe_merkle_integrity.py
- **验证理论**：方向 6（可信计算 / 供应链溯源）+ 方向 9（数据完整性 / Merkle 树）。
- **做法**：只读遍历 `atoms/**/*.md` 与 `misconceptions/**/*.md`（共 108 个文件），逐文件 sha256，自底向上构建 Merkle 树，并构建哈希链；随后在内存中将首文件末字节翻转，验证根哈希是否变化（篡改检测）。
- **实测结果**（见 `merkle_report.json`）：
  - scanned = 108
  - merkle_root = `27c22968f25d0c0f116713f32db28b0b849a752bf8fd8a3e9901fa653cb87fff`
  - merkle_height = 7
  - tamper_detected = **true**（改一字节根即变）
  - chain_tail = `612b962872ac7ea13b14e69685f9b06d911ad3bb250fd63e4707b4b23f46e07e`
- **结论**：Merkle 完整性根可纯标准库实现、无需硬件/外部服务，可立即作为 `tool_integrity` 的增强层，并被 in-toto 风格 attestation 消费（见 06/09/11 组合 B）。
- **运行**：`python _arch_v15/probes/probe_merkle_integrity.py`（需仓库 `.venv` 或系统 Python3，无第三方依赖）。

## 未做但可做的探针（留给后续）
- 属性测试 mini-QuickCheck（方向 8）：对命题 YAML 随机扰动测不变量 —— 已列入 N 档路线图（13），本次未实跑以控制范围。
- W2 公理证明草图（方向 3）：纯文本证明，非代码探针。
