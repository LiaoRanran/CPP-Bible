# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671i-C4 · 随机种子固定检查测试（≥5 条）。"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
spec = importlib.util.spec_from_file_location("seed_check_671i", str(TOOLS / "seed_check_671i.py"))
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)


def _w(tmp: Path, name: str, body: str):
    p = tmp / name
    p.write_text(body, encoding="utf-8")
    return p


def test_scan_use_and_seed(tmp_path):
    # 673b A3：此前这里把 `tests/_x.py` **写进仓库目录**且不清理 —— 残留文件会被
    # `ruff check tools/ tests/` 判 I001 ⇒ 625 的 ruff 门禁在跑过本测试后必红。
    # 现在一律写在 pytest 的 tmp_path 里（仓库零写）。
    p1 = _w(tmp_path, "no_seed.py", "import random\nx=random.randint(0,9)\n")
    assert sc.scan_file(str(p1))[0] is True
    p2 = _w(tmp_path, "s.py", "import random\nrandom.seed(42)\nx=random.randint(0,9)\n")
    uses, seed = sc.scan_file(str(p2))
    assert uses and seed


def test_experimental_no_seed_is_error(tmp_path):
    _w(tmp_path, "experiment_foo.py", "import random\nprint(random.random())\n")
    res = sc.run_all(str(tmp_path))
    errs = [i for i in res["issues"] if i["severity"] == "ERROR"]
    assert any(i["code"] == "NO_SEED" for i in errs)


def test_utility_no_seed_is_warn(tmp_path):
    _w(tmp_path, "helper.py", "import random\nprint(random.random())\n")
    res = sc.run_all(str(tmp_path))
    warns = [i for i in res["issues"] if i["severity"] == "WARN"]
    errs = [i for i in res["issues"] if i["severity"] == "ERROR"]
    assert any(i["code"] == "NO_SEED" for i in warns)
    assert not errs


def test_seeded_file_no_issue(tmp_path):
    _w(tmp_path, "experiment_bar.py", "import numpy as np\nnp.random.seed(0)\nx=np.random.rand()\n")
    res = sc.run_all(str(tmp_path))
    assert res["issues"] == []


def test_run_all_zero_errors_when_all_seeded(tmp_path):
    _w(tmp_path, "experiment_a.py", "import random\nrandom.seed(1)\nrandom.random()\n")
    res = sc.run_all(str(tmp_path))
    assert res["errors"] == []


def test_cli_exit_one_on_experimental_no_seed(tmp_path):
    _w(tmp_path, "baseline_xyz.py", "import random\nrandom.random()\n")
    assert sc.main(["--tools", str(tmp_path)]) == 1


#: 673b A3 实测：这 6 个文件都**不是**未固定种子 —— 它们用 `random.Random(seed)`
#: （带固定默认种子的局部 RNG，见 tests/test_seed_audit_673b.py 的连跑两次哈希断言）。
#: 扫描器只认全局 `random.seed()`，故把它们记成 WARN 属于**口径限制**，不是真缺口。
#:
#: 673s 追加（同为「口径限制」类，非新缺口）：`tools/selection_strategies_673p.py`
#: 用 `random.Random(seed).sample(...)`（seed 由 CLI 传入、默认 20260930）——与上面 6 个
#: 完全同一形态。673s 另修掉一处**真误报**：`tools/verifier_pool_673p.py` 此前仅在
#: **注释/报错文案**里出现 `random.sample` 字样、代码里零随机性，已改写文案使其不再被扫中。
KNOWN_LOCAL_RNG_WARNS = sorted([
    "tools/confidence_sequence.py",
    "tools/eprocess_671g.py",
    "tools/learner_behavior_logger.py",
    "tools/learner_state.py",
    "tools/metrics_collector.py",
    "tools/selection_strategies_673p.py",
    "tools/trajectory_floor_check_671g.py",
])


def test_real_repo_seed_state_is_locked():
    """673b A3 修订（诚实登记）：本测试原本断言「真实仓库应有 ≥6 个未固定种子的实验脚本」。

    实测（673b）：真实仓库 **ERROR = 0** —— 那 6 个文件全部是 `random.Random(seed)` 的
    固定默认种子用法，结果可复现（哈希级验证见 test_seed_audit_673b.py）。
    于是改为锁定**当前真话**：0 个 ERROR + WARN 集合 == 已知 6 个；
    任何**新增**未固定种子的脚本都会改变集合 ⇒ 本测试仍然会红（保住护栏语义）。
    """
    res = sc.run_all(str(TOOLS))
    exp_errs = [i for i in res["errors"] if i["severity"] == "ERROR"]
    assert exp_errs == [], f"出现未固定种子的实验脚本（必须修或登记）：{[i['card'] for i in exp_errs]}"
    warns = sorted(i["card"].replace("\\", "/") for i in res["issues"]
                   if i["severity"] == "WARN")
    assert warns == KNOWN_LOCAL_RNG_WARNS, (
        f"WARN 集合与登记不一致（新增未固定种子脚本 / 旧脚本被修好 / 文件被改名）：\n"
        f"  实际 {warns}\n  登记 {KNOWN_LOCAL_RNG_WARNS}")
