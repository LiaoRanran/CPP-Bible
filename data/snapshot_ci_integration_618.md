# SNAPSHOT CI 集成方案（618 D3）

> 配套 D1（数字治理）。本方案定义如何在 CI 中集成 SNAPSHOT 校验，防回归数字漂移（评审 #6/#7）。

## 一、目标
- 每次 PR / push，CI 自动校验 `data/SNAPSHOT_MANIFEST.json` 与当前 git/filesystem 实值一致 ⇒ 任何手填或漂移立即失败。
- 不引入新 manifest 批次后缀（见 D1），统一收敛到 `data/SNAPSHOT_MANIFEST.json`。

## 二、CI Job 设计（建议，不修改 ci.yml，交人项）
```yaml
  snapshot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }   # 需完整历史以 rev-list --count
      - uses: actions/setup-python@v5
        with: { python-version: "3.13" }
      - run: python tools/snapshot_manifest.py --check-clean   # 要求工作区干净 + 重写 manifest
      - name: verify consistency
        run: |
          python - <<'PY'
          import json, subprocess, sys
          # 重算 live_counts 并与已入库 manifest 比对
          # （实际实现读取 tools/snapshot_manifest.build_manifest 与仓库内 manifest 逐项 diff）
          PY
```
- `--check-clean`：要求工作区干净（无未提交改动）再生成，避免"本地脏"被误提交。
- 一致性门：重算 `live_counts` 与仓库内 `SNAPSHOT_MANIFEST.json` 的 `live_counts` + `head_commit` 逐项比对，不一致 ⇒ `exit 1`。

## 三、约束（铁律）
- CI 的 `snapshot` job **只跑 SNAPSHOT 校验**（读 manifest + git/filesystem 重算），**不跑监工门禁**（gate/poison/replay/tool_integrity `--check`）——与 617/618 任务书 §五 一致。
- CI 不得修改 `verification_baseline_frozen`（冻结数字改由监工门禁产出，CI 只读校验）。
- `fetch-depth: 0` 是 `git rev-list --count HEAD` 正确计数的前提；shallow clone 会给出错误 commit 数。

## 四、与现有 CI 的关系
- 现有 CI 四 job（gate/quality/metrics/ci-verify）中，`metrics`/`ci-verify` 已部分覆盖；`snapshot` 作为独立轻量 job 补强"计数漂移"专项。
- 614 已修复 gate/quality job 缺 `pip install pyyaml` 的根因；snapshot job 纯标准库，无此依赖。

## 五、交付与交人项
- 本方案文档（D3）。
- 实际修改 `ci.yml` 落地 `snapshot` job 属交人项（任务书明确"禁止修改 ci.yml"），本批只给方案，不实施。
