# 方向 26：CI/CD 最小配置（GitHub Actions）

## 核心结论
1. 对 QueYi 这种"可复现性是卖点"的项目，CI 不是可选而是**审稿硬证据**：一条 GitHub Actions 工作流跑"三编译器矩阵 +  sanitizers + 变异测试 + 发布 benchmark 报告"，等于把"可复现"自动化证明给 reviewer 看。
2. 最小可用配置 = 一个 `ci.yml`：on push/PR → 矩阵(GCC/Clang/MSVC) → 编译 → 跑 48 卡 + 15 夹具 → 输出 `report.json`；再一个 nightly 跑 TSan/变异（慢，不阻塞）。
3. 对单人作者，CI 还扮演"免费算力 + 防回归保镖"：你改一行，CI 立刻告诉你 0.59ms/卡是否退化——这是备考期"冻结项目"也能保质量的关键（方向 44）。

## 精确数字与案例
- **最小 ci.yml 结构**：
  ```yaml
  name: ci
  on: [push, pull_request]
  jobs:
    build-test:
      strategy: { matrix: { compiler: [gcc, clang, msvc] } }
      runs-on: ${{ matrix.compiler == 'msvc' && 'windows' || 'ubuntu' }}
      steps:
        - uses: actions/checkout@v4
        - run: cmake -B build && cmake --build build
        - run: ./build/queyi eval --all --out report.json
  ```
- **sanitizer job**：`CXXFLAGS="-fsanitize=address,undefined"` 单独 job，确保内核无内存 UB（方向 19）。
- **nightly 变异**：cron 每晚跑 C++ mutator（方向 20），结果上传 artifact，不阻塞合并。
- **报告产物**：benchmark `report.json` 作为 workflow artifact，审稿人可下载核对 80%/100%/97.3%。
- **开销**：GitHub Actions 免费额度（私有库 2000 分钟/月，公开库无限）；QueYi 公开库无成本压力。

## 对阙疑的 3 条具体行动
1. **立即加 ci.yml**：矩阵 GCC 13 / Clang 17 / MSVC 19，push 即跑 48 卡 + 15 夹具，失败则红——这是 artifact 评测（方向 05）的基础门票。
2. **sanitizer 门禁**：加 `-fsanitize=address,undefined` job，0 报错才绿；在稿里写"内核过 ASan+UBSan"。
3. **benchmark 报告自动贴**：CI 把 `report.json` 存 artifact 并在 PR 评论摘要，rebuttal 时直接甩链接证可复现（方向 04）。

## 盲区（诚实标注）
- 上面 yml 为示意，需按 QueYi 实际 build 系统（CMake/Make/Bazel）调整；MSVC 矩阵需 Windows runner 且路径语法不同。
- 变异测试 nightly 若用 Mull/muCPP 需预装，GitHub Actions 需 cache 或容器。
- 三编译器结果若不一致（方向 17），CI 应记录差异而非简单失败——需设计"差异报告"而非"全绿"。

## 来源
- [1] GitHub Actions 文档 — https://docs.github.com/actions
- [2] CMake + Actions 示例 — https://github.com/features/actions
- [3] ASan in CI — 方向 19 来源
- [4] C++ 变异 mutator — 方向 20 来源
