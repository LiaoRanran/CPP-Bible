# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""673b A3 · 全仓种子审计与「同种子连跑两次结果一致」硬测试。

为什么单开一个文件（而不是扩 671i 的扫描测试）：
  671i 的判据是「全局 `random.seed()` 有没有被调用」，于是把
  `random.Random(seed)`（**带固定默认种子的局部 RNG**）一律判成 NO_SEED(WARN)；
  而 673b 的判据是「**结果能不能复现**」——
    ① 抽样随机必须有**种子来源**（全局 seed 或带固定默认值的局部 RNG）；
    ② 同一入口连跑两次，产物必须**逐字节相同**（哈希相等）；
    ③ 安全用途的 `secrets.*` 属于**理应不可预测**，显式豁免并登记（不是漏网）。
"""
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, str(TOOLS / f"{name}.py"))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── 判据表（审计口径写死在测试里，改判据必须改这里并被 review） ──────────────────
SAMPLING_FUNCS = (
    "random|randint|randrange|choice|choices|shuffle|sample|uniform|gauss|normalvariate"
    "|triangular|betavariate|expovariate|getrandbits|randbytes"
)
USE_RE = re.compile(r"\b(random|np\.random|numpy\.random|torch)\.(%s)\s*\(" % SAMPLING_FUNCS)
LOCAL_RNG_RE = re.compile(r"\brandom\.Random\(\s*(\w+)")
GLOBAL_SEED_RE = re.compile(r"\b(random|np\.random|numpy\.random)\.seed\(")
SECRETS_RE = re.compile(r"\bsecrets\.\w+\(")

#: 安全用途（安全令牌/签名 nonce）：**不得**固定种子，显式豁免（逐条登记，不是通配）
SECRETS_EXEMPT = {
    "tools/observability.py": "trace/span id 用 token_hex ⇒ 必须不可预测",
    "tools/task_queue.py": "任务 id 用 token_hex ⇒ 必须不可预测",
    "tools/vsa_asymmetric_signer_629.py": "签名 nonce 用 secrets.randbelow ⇒ 必须不可预测",
}

#: 「局部 RNG + 固定默认种子」的六个文件：默认值写死在签名里 ⇒ 不传参也可复现
FIXED_DEFAULT_SEED_PARAMS = {
    "tools/confidence_sequence.py": "monte_carlo_peek",
    "tools/eprocess_671g.py": "type1_simulation",
    "tools/learner_behavior_logger.py": "simulate",
    "tools/learner_state.py": "simulate",
    "tools/metrics_collector.py": None,     # seed 由调用方给（本文件常量 SEED 固定）
    "tools/trajectory_floor_check_671g.py": "pick_sample",
}


def _scan() -> list[dict]:
    out = []
    for p in sorted(TOOLS.rglob("*.py")):
        text = p.read_text(encoding="utf-8", errors="replace")
        uses = [(m.group(1) + "." + m.group(2), text.count("\n", 0, m.start()) + 1)
                for m in USE_RE.finditer(text)]
        secrets_hits = [text.count("\n", 0, m.start()) + 1 for m in SECRETS_RE.finditer(text)]
        if not uses and not secrets_hits:
            continue
        out.append({
            "rel": p.relative_to(ROOT).as_posix(),
            "text": text,
            "uses": uses,
            "secrets_lines": secrets_hits,
            "global_seed": bool(GLOBAL_SEED_RE.search(text)),
            "local_rng": LOCAL_RNG_RE.findall(text),
        })
    return out


# ── 1 · 全仓审计：抽样随机必须能指出「种子从哪来」 ────────────────────────────────

def test_every_sampling_file_has_a_seed_source():
    bad = []
    for r in _scan():
        if not r["uses"]:
            continue
        if r["global_seed"] or r["local_rng"]:
            continue
        bad.append(f"{r['rel']}: {r['uses'][0][0]}@L{r['uses'][0][1]}")
    assert not bad, "以下文件用了抽样随机却找不到种子来源（全局 seed 或 random.Random(seed)）：\n" + "\n".join(bad)


def test_secrets_usage_is_explicitly_exempted_and_registered():
    for r in _scan():
        if not r["secrets_lines"] or r["uses"]:
            continue
        assert r["rel"] in SECRETS_EXEMPT, (
            f"{r['rel']} 用了 secrets.* 但未登记豁免——安全令牌**必须**不可预测，"
            f"请把理由写进 SECRETS_EXEMPT 再放行")
    # 反向：登记表里的文件确实还在用 secrets（防登记腐烂）
    live = {r["rel"] for r in _scan() if r["secrets_lines"] and not r["uses"]}
    stale = set(SECRETS_EXEMPT) - live
    assert not stale, f"SECRETS_EXEMPT 里有已不存在的条目（登记腐烂）：{sorted(stale)}"


def test_local_rng_files_have_fixed_default_seeds():
    """六个「局部 RNG」文件的默认种子必须是**写死的整数**，不能是 None/时间/随机。"""
    for rel in FIXED_DEFAULT_SEED_PARAMS:
        text = (ROOT / rel).read_text(encoding="utf-8")
        sigs = re.findall(r"def \w+\([^)]*seed\s*:\s*int\s*=\s*(\w+)[^)]*\)", text, re.DOTALL)
        if sigs:
            assert all(re.fullmatch(r"\d+", s) for s in sigs), f"{rel} 的 seed 默认值不是整数常量：{sigs}"
            continue
        # 没有 seed 形参 ⇒ 必须有模块级整数常量（如 SEED = 20260930）
        assert re.search(r"^\s*(SEED|MC_SEED)\s*[:=]\s*\d+", text, re.MULTILINE), \
            f"{rel} 既没有固定默认 seed 形参，也没有模块级整数种子常量"
        # 且不得出现「用当前时间/None 当种子」的写法
        assert not re.search(r"Random\(\s*(None|time\.time\(\)|datetime)", text), \
            f"{rel} 出现了不可复现的种子来源"


def test_seed_defaults_are_deviation_free_sample():
    """抽样核对：六个文件的默认种子在**跨进程**下也一致（写死常量，不是运行时生成）。"""
    for rel, fn in FIXED_DEFAULT_SEED_PARAMS.items():
        if not fn:
            continue
        mod = _load(Path(rel).stem)
        sig = inspect.signature(getattr(mod, fn))
        if "seed" in sig.parameters:
            d = sig.parameters["seed"].default
            assert isinstance(d, int) and d > 0, f"{rel}::{fn} 的 seed 默认值应为正整数，实际 {d!r}"


# ── 2 · 「连跑两次结果哈希一致」（A3 验收项） ────────────────────────────────────

def test_trajectory_floor_pick_sample_is_deterministic():
    mod = _load("trajectory_floor_check_671g")
    a = mod.pick_sample(137)
    b = mod.pick_sample(137)
    c = mod.pick_sample(137, seed=999)      # 换种子**应当**不同（否则说明 seed 没接线）
    assert a == b and len(a) == 10
    assert a != c


def test_eprocess_type1_simulation_reproducible():
    mod = _load("eprocess_671g")
    fn = getattr(mod, "type1_simulation")
    h = []
    for _ in range(2):
        out = fn(0.5, n=40, reps=60)
        h.append(hashlib.sha256(json.dumps(out, sort_keys=True, default=str).encode()).hexdigest())
    assert h[0] == h[1], "type1_simulation 两次运行哈希不一致 ⇒ 仍有未固定的随机源"
    out2 = fn(0.5, n=40, reps=60, seed=12345)
    assert json.dumps(out2, sort_keys=True, default=str) != json.dumps(
        fn(0.5, n=40, reps=60), sort_keys=True, default=str), "换 seed 结果未变化 ⇒ seed 未接线"


def test_confidence_sequence_monte_carlo_reproducible():
    mod = _load("confidence_sequence")
    fn = getattr(mod, "monte_carlo_peek")
    one = fn(reps=20, nmax=60, step=20)
    two = fn(reps=20, nmax=60, step=20)
    assert one == two, "monte_carlo_peek 两次运行结果不一致"


def test_mutation_and_baseline_scripts_seed_globally():
    """672f 固定过种子的两个脚本：全局 seed 必须还在（防回退）。"""
    for rel, expect in (("tools/mutation_test_656.py", "20260930"),
                        ("tools/verify_baseline_672g.py", None)):
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert re.search(r"random\.seed\(SEED\)", text), f"{rel} 的全局 random.seed(SEED) 不见了"
        m = re.search(r"^\s*SEED\s*[:=]\s*(\d+)", text, re.MULTILINE)
        assert m, f"{rel} 缺少模块级 SEED 常量"
        if expect:
            assert m.group(1) == expect, f"{rel} 的 SEED 被改成了 {m.group(1)}（约定值 {expect}）"


# ── 3 · 交叉核对：671i 扫描器口径与 673b 口径的关系（防两套判据互相打脸） ──────────

def test_671i_scanner_reports_zero_errors_on_real_repo():
    sc = _load("seed_check_671i")
    # 只扫 tools/（扫仓库根会把 .venv / .pytest_tmp 里的第三方文件也算进来，不是本仓的账）
    res = sc.run_all(str(TOOLS))
    errs = [i for i in res["issues"] if i["severity"] == "ERROR"]
    assert not errs, f"671i 扫描器报 ERROR：{[e['card'] for e in errs]}"
    warns = [i for i in res["issues"] if i["severity"] == "WARN"]
    # WARN 允许存在（工具/日志类），但必须全部是「有 seed 来源也要登记」的那类；
    # 这里断言数量与 673b 的豁免/登记表一致，防止 WARN 无界增长。
    assert len(warns) <= 8, f"WARN 数异常增长（{len(warns)}）⇒ 有人加了未固定种子的脚本：{[w['card'] for w in warns]}"


def test_no_stray_scratch_files_in_tests_dir():
    """673b A3：tests/ 里不得留 `_x.py` 之类 scratch（671i 的测试曾把它写进仓库 ⇒ ruff 门禁红）。"""
    stray = [p.name for p in (ROOT / "tests").glob("_*.py")]
    assert not stray, f"tests/ 下有 scratch 文件（会被 ruff/门禁判红）：{stray}"
