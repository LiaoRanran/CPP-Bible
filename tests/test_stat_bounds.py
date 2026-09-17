"""565 Part 1 · `tools/stat_bounds.py` 的四重锚点 + 边界 fail-loud 回归锁。

为什么是"四重锚点"而不是"跟 scipy 对拍"：本仓核心依赖只有 pyyaml，`.venv` 里 scipy/numpy
**实测未安装**；为对拍把它们加进核心依赖是反向依赖。故用**互相独立的四条证据链**自证：
  ① 解析解：k=0 闭式 `1-(1-conf)^(1/n)`；k=n 与 k=0 的**对称关系** `lo(k)=1-hi(n-k)`；
  ② 独立第二实现：**二项尾和**（直接求和，与工具里的不完全 Beta 连分式完全不同的算法）
     数值反解同一分位，两法在随机 (k,n,conf) 网格上偏差 <1e-7；
  ③ 公开锚点：56 卡 0 误伤 95% 上界 ≈0.05209（且**紧于** rule-of-three 3/56=0.05357）、
     n=100,k=0 ⇒ ≈0.0295；
  ④ 样本量闭式：eps=5%@95% ⇒ 59；eps=2%@95% ⇒ 149。

外加：**边界必须 fail-loud**（n=0 / k>n / k<0 / conf∉(0,1) 一律 ValueError）——"没测"与
"确实没发生"是两件事，静默钳值会把前者伪装成后者（563 N9 误报的教训）。
"""
from __future__ import annotations

import importlib.util
import json
import math
import random
from pathlib import Path

import pytest
import stat_bounds as sb

REPO = Path(__file__).resolve().parent.parent


# ── ① 解析解与对称性 ─────────────────────────────────────────────────────────
def test_k0_closed_form_matches_numeric():
    """k=0：C-P 上界必须等于解析解 `1 - (1-conf)^(1/n)`（数值法误差 <1e-9）。"""
    for n in (1, 7, 56, 100, 1000):
        for conf in (0.90, 0.95, 0.99):
            exact = 1 - (1 - conf) ** (1 / n)
            assert abs(sb.cp_upper(0, n, conf) - exact) < 1e-9, (n, conf)


def test_kn_symmetry_and_edges():
    """k=n：上界为 1；且区间满足 C-P 对称性 `lo(k) == 1 - hi(n-k)`。"""
    for n in (5, 56, 100):
        assert sb.cp_upper(n, n, 0.95) == 1.0
        assert sb.cp_interval(n, n, 0.95)[1] == 1.0
        assert sb.cp_interval(0, n, 0.95)[0] == 0.0
        for k in range(0, n + 1):
            lo_k, hi_k = sb.cp_interval(k, n, 0.95)
            lo_m, hi_m = sb.cp_interval(n - k, n, 0.95)
            assert abs(lo_k - (1 - hi_m)) < 1e-9, (k, n)
            assert abs(hi_k - (1 - lo_m)) < 1e-9, (k, n)
    # 双侧闭式（注意用 alpha/2）：hi(0,n) == 1-(alpha/2)^(1/n)；lo(n,n) == (alpha/2)^(1/n)
    for n in (7, 56):
        half = (1 - 0.95) / 2
        assert abs(sb.cp_interval(0, n, 0.95)[1] - (1 - half ** (1 / n))) < 1e-9
        assert abs(sb.cp_interval(n, n, 0.95)[0] - half ** (1 / n)) < 1e-9
    # 单侧口径：k=0 处 cp_upper 与 cp_upper_one_sided **同值**（都是 1-alpha^(1/n)）；
    # k>0 处两者**不同**（alpha vs alpha/2）——这正是 cp_upper 的口径警告所锁的行为
    assert abs(sb.cp_upper(0, 56) - sb.cp_upper_one_sided(0, 56)) < 1e-12
    assert sb.cp_upper(10, 56) > sb.cp_upper_one_sided(10, 56) > 0
    assert abs(sb.cp_upper_one_sided(0, 56) - (1 - 0.05 ** (1 / 56))) < 1e-12


# ── ② 独立第二实现：二项尾和（与不完全 Beta 完全不同的算法）────────────────────
def _binom_cdf(k: int, n: int, p: float) -> float:
    """P(X ≤ k)，X~B(n,p)：直接逐项求和（对数空间避免溢出）。"""
    if p <= 0.0:
        return 1.0
    if p >= 1.0:
        return 0.0
    lp, lq = math.log(p), math.log1p(-p)
    tot = 0.0
    for i in range(k + 1):
        tot += math.exp(math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
                        + i * lp + (n - i) * lq)
    return tot


def _cp_bound_by_binom_tail(k: int, n: int, conf: float, *, one_sided: bool) -> float:
    """C-P 上界 = 使 P(X≤k; n, p) = (1-conf)[单侧] 或 (1-conf)/2[双侧] 的 p（二分反解尾和）。"""
    target = (1 - conf) if one_sided else (1 - conf) / 2
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if _binom_cdf(k, n, mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def test_cross_implementation_binom_tail():
    """两套独立算法（不完全 Beta 连分式 vs 二项尾和求和）在随机网格上偏差 <1e-7。

    单侧对单侧（`cp_upper_one_sided`）、双侧对双侧（`cp_interval` 的 hi）——
    绝不拿一个口径去对另一个口径（那正是 563 N9 误报的形态）。
    """
    rng = random.Random(20260917)
    for _ in range(40):
        n = rng.randint(1, 200)
        k = rng.randint(0, n)
        conf = rng.choice([0.90, 0.95, 0.99])
        got1 = sb.cp_upper_one_sided(k, n, conf)
        ref1 = _cp_bound_by_binom_tail(k, n, conf, one_sided=True)
        assert abs(got1 - ref1) < 1e-7, ("单侧", k, n, conf, got1, ref1)
        got2 = sb.cp_interval(k, n, conf)[1]
        ref2 = _cp_bound_by_binom_tail(k, n, conf, one_sided=False)
        assert abs(got2 - ref2) < 1e-7, ("双侧", k, n, conf, got2, ref2)


def test_wilson_z_matches_known_constant():
    """Wilson 在 conf=0.95 时 z 必须 ≈1.959964（与 563 探针硬编码常量一致）。"""
    assert abs(sb.normal_quantile(0.975) - 1.959963984540054) < 1e-9
    lo, hi = sb.wilson(0, 56, 0.95)
    assert lo < 1e-12, lo                              # k=0：下界为 0（浮点残差忽略）
    # k=0 时 Wilson 上界 = z²/(n+z²) ≈ 0.0642（与 C-P 双侧 0.0638 略不同 —— 两法不同源，
    # 差在千分位属正常；本断言只锁"量级与闭式值"，不主张两法同值）
    assert abs(hi - (1.959963984540054 ** 2) / (56 + 1.959963984540054 ** 2)) < 1e-9, hi


# ── ③ 公开锚点 ───────────────────────────────────────────────────────────────
def test_public_anchors():
    """56 卡 0 误伤 ⇒ 95% 上界 ≈0.05209，且**紧于** rule-of-three 3/56≈0.05357。"""
    up56 = sb.cp_upper(0, 56, 0.95)
    assert abs(up56 - 0.05209) < 1e-4, up56
    assert abs(3 / 56 - 0.05357) < 1e-4
    assert up56 < 3 / 56, "精确 C-P 上界必须紧于 rule-of-three 经验式"
    assert abs(sb.cp_upper(0, 100, 0.95) - 0.0295) < 1e-4


def test_interval_contains_point_and_ordering():
    """区间自洽：0 ≤ lo ≤ k/n ≤ hi ≤ 1，且 conf 越高区间越宽（单调性）。"""
    for k, n in ((0, 56), (615, 956), (207, 207), (2, 13), (729, 956)):
        lo, hi = sb.cp_interval(k, n, 0.95)
        assert 0.0 <= lo <= k / n <= hi <= 1.0, (k, n, lo, hi)
    w90 = sb.cp_interval(615, 956, 0.90)
    w99 = sb.cp_interval(615, 956, 0.99)
    assert (w99[1] - w99[0]) > (w90[1] - w90[0]) > 0


# ── ④ 样本量闭式 ─────────────────────────────────────────────────────────────
def test_sample_size_formulas():
    assert sb.n_for_upper_bound_zero(0.05, 0.95) == 59
    assert sb.n_for_upper_bound_zero(0.02, 0.95) == 149
    assert sb.n_for_upper_bound_zero(0.10, 0.95) == 29
    assert sb.n_for_upper_bound_zero(0.05, 0.99) == 90
    # 闭式与"零失效上界"互为逆运算：n 取到 59 ⇒ 上界 ≤ 5%
    assert sb.cp_upper(0, 59, 0.95) <= 0.05
    assert sb.cp_upper(0, 58, 0.95) > 0.05


def test_n_for_proportion_is_monotone():
    """样本量随目标精度收紧而增大（量级估计，只验方向与量级）。"""
    coarse = sb.n_for_proportion(1, 2, 0.10)
    fine = sb.n_for_proportion(1, 2, 0.02)
    assert coarse < fine
    assert sb.n_for_proportion(1, 2, 0.05) == 385          # z²·0.25/0.05² ≈ 384.15 → 385


# ── 边界 fail-loud（禁止静默返回）────────────────────────────────────────────
@pytest.mark.parametrize("bad", [
    (0, 0), (-1, 56), (57, 56),
])
def test_boundary_fail_loud_k_n(bad):
    k, n = bad
    for fn in (sb.cp_upper, sb.cp_interval, sb.wilson, sb.proportion):
        with pytest.raises(ValueError):
            fn(k, n) if n == 0 or k < 0 or k > n else fn(k, n)
    with pytest.raises(ValueError):
        sb.proportion(0, 0)


@pytest.mark.parametrize("conf", [0.0, 1.0, -0.5, 1.5])
def test_boundary_fail_loud_conf(conf):
    for fn in (sb.cp_upper, sb.cp_interval, sb.wilson, sb.proportion):
        with pytest.raises(ValueError):
            fn(0, 56, conf)
    with pytest.raises(ValueError):
        sb.n_for_upper_bound_zero(0.05, conf)
    with pytest.raises(ValueError):
        sb.n_for_proportion(1, 2, 0.05, conf)


@pytest.mark.parametrize("eps", [0.0, 1.0, -0.1, 1.1])
def test_boundary_fail_loud_eps(eps):
    with pytest.raises(ValueError):
        sb.n_for_upper_bound_zero(eps)
    with pytest.raises(ValueError):
        sb.n_for_proportion(1, 2, eps)


def test_proportion_block_carries_denominator():
    """Part 2 口径底座：比率块**必须**自带分子/分母（禁止无分母的裸比率）。"""
    blk = sb.proportion(615, 956, 0.95)
    assert set(blk) >= {"numerator", "denominator", "point", "cp_low", "cp_high", "conf"}
    assert blk["numerator"] == 615 and blk["denominator"] == 956
    assert abs(blk["point"] - 0.6433) < 1e-4


# ── 与 563 探针逐值一致（验收项）─────────────────────────────────────────────
def _load_probe():
    p = REPO / "_arch_v6" / "probe_bounds.py"
    if not p.is_file():
        pytest.skip("_arch_v6/probe_bounds.py 不在（探针未随仓保留）")
    spec = importlib.util.spec_from_file_location("probe_bounds_563", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_matches_563_probe_values():
    """与 `_arch_v6/probe_bounds.py` 在随机网格上**逐值一致**（<1e-12，同算法同精度）。"""
    pb = _load_probe()
    rng = random.Random(565)
    for _ in range(30):
        n = rng.randint(1, 300)
        k = rng.randint(0, n)
        conf = rng.choice([0.90, 0.95, 0.99])
        assert abs(sb.cp_upper(k, n, conf) - pb.cp_upper(k, n, conf)) < 1e-12, (k, n)
        a, b = sb.cp_interval(k, n, conf)
        c, d = pb.cp_interval(k, n, conf)
        assert abs(a - c) < 1e-12 and abs(b - d) < 1e-12, (k, n)
    for eps, conf, want in ((0.05, 0.95, 59), (0.02, 0.95, 149)):
        assert sb.n_for_upper_bound_zero(eps, conf) == pb.n_for_upper_bound_zero(eps, conf)
        assert sb.n_for_upper_bound_zero(eps, conf) == want


# ── CLI（人读 + 机器可读）────────────────────────────────────────────────────
def test_cli_cp_and_json(capsys):
    assert sb.main(["cp", "--k", "0", "--n", "56"]) == 0
    out = capsys.readouterr().out
    assert "0/56" in out and "C-P" in out
    assert sb.main(["cp", "--k", "0", "--n", "56", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["numerator"] == 0 and data["denominator"] == 56
    # `cp_high` 是**双侧**区间上界（0.0638）；单侧上界（0.05209）另见 cp_upper_one_sided
    assert abs(data["cp_high"] - 0.06375) < 1e-4
    assert abs(sb.cp_upper_one_sided(0, 56) - 0.05209) < 1e-4


def test_cli_wilson_and_n_needed(capsys):
    assert sb.main(["wilson", "--k", "207", "--n", "207"]) == 0
    assert "wilson" in capsys.readouterr().out
    assert sb.main(["n-needed", "--eps", "0.05", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["n"] == 59
    # 非法参数 ⇒ rc=2 + stderr（不静默）
    assert sb.main(["cp", "--k", "5", "--n", "0"]) == 2
    assert "参数非法" in capsys.readouterr().err
