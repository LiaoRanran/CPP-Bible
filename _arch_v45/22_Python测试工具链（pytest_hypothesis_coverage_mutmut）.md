# 方向 22：Python 测试工具链（pytest / hypothesis / coverage / mutmut）

## 核心结论
1. QueYi 内核是 C++，但其**测试编排、corpus 管理、报告生成几乎必然用 Python**——pytest + hypothesis + coverage + mutmut 是这套外围的标准组合，直接影响"可复现性"与"变异分数"的可信度。
2. 分工：pytest 管用例与 CI；hypothesis 做 PBT（方向 21）；coverage.py 报行/分支覆盖；mutmut 对**Python 外围**做变异测试（C++ 内核用方向 20 的 C++ mutator）。
3. 对审稿人：展示"外围 Python 也有 coverage + mutation 报告"说明工程严谨；但不应把 Python mutation score 与 C++ 的 97.3% 混为一谈（分清楚两层）。

## 精确数字与案例
- **pytest**：事实标准， fixture/parametrize/plugin 生态（pytest-xdist 并行、pytest-cov 集成 coverage）。
- **hypothesis**：PBT，见方向 21；与 pytest 集成 `from hypothesis import given`。
- **coverage.py**：行覆盖 + 分支覆盖；`coverage run -m pytest && coverage report --show-missing`；可设阈值门禁（如 <80% 失败）。
- **mutmut**：Python 变异测试，基于同套算子（常量/逻辑/控制流）；`mutmut run` 生成变异，`mutmut junitxml` 出报告。注意 mutmut 慢（每个变异重跑全测）。
- **组合案例**：CI 流程 = `pytest -n auto`（并行）→ `coverage` 门禁 → `hypothesis` 跑满 → nightly `mutmut`。QueYi 可将 C++ 内核通过 pytest 子进程调用，统一报告。
- **开销**：mutmut 全量变异可能比普通测试慢 10–100x；建议只对核心模块跑。

## 对阙疑的 3 条具体行动
1. **外围 Python 上 coverage 门禁**：QueYi 的 corpus/账本/报告脚本加 `pytest+coverage`，CI 要求行覆盖 ≥80%，作为工程质量证据。
2. **分层报告**：稿里明确"C++ 内核 mutation score 97.3%（用 C++ mutator）；Python 外围 coverage 85%（用 coverage.py）"——两层分开报，防 reviewer 混淆。
3. **hypothesis 跑 corpus 生成**：用 hypothesis 随机生成 C++ 片段喂给 QueYi，统计"判决分布"，作为稳定性证据（配合方向 21 性质）。

## 盲区（诚实标注）
- QueYi 是否已用 Python 外围未知；若全 C++，则本方向的 coverage/mutmut 不适用，需调整为 C++ 工具（方向 19/20）。
- mutmut 对 pytest 版本敏感，需固定版本锁。
- Python 覆盖率不能直接代表 C++ 内核质量，勿夸大。

## 来源
- [1] pytest — https://docs.pytest.org/
- [2] hypothesis — https://hypothesis.works/
- [3] coverage.py — https://coverage.readthedocs.io/
- [4] mutmut — https://mutmut.readthedocs.io/
