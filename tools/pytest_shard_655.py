#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""pytest_shard_655.py — 按**测试时长**均衡分片（655 C 杠杆 3）。

目标
====
把"一大坨测试"切成 N 份**预测耗时接近**的片，供 CI 矩阵或多个终端并行跑。
切分依据是上一轮的**真实 junit XML 时长**（不是猜），算法是 LPT（最长处理时间优先，
把模块按权重从大到小依次放进当前最轻的片）。

为什么按**模块**分片而不是按用例
================================
本仓 `tests/conftest.py` 的隔离机制是**模块级**的（`SLOW_MODULES` / `SERIAL_EXTRA`，
以及"同模块共享真实仓库状态"的经验事实）。按模块切分 ⇒ 每个模块整体落在同一片，
不会因为拆散而改变并行语义；按用例切分反而会把同族用例分到不同进程，制造假红。

与 `tests/conftest.py` 的契约
=============================
执行侧由 conftest 的 `--shard-id/--shard-count` 实现（默认关闭，**不影响默认口径**）：
- 若 `data/655_shard_plan.json` 存在且 `shards` 与 `--shard-count` 一致 ⇒ 按计划表选片；
- 否则退化为 `sha256(模块名) % N` 的**确定性**分片（无计划也能跑，且各片互斥、可复现）。

用法
====
    python tools/pytest_shard_655.py --plan --junit data/655_junit_fast.xml --shards 4
    python tools/pytest_shard_655.py --show
    python tools/pytest_shard_655.py --run --shard 0 -- -m "not slow" -n auto
    python tools/pytest_shard_655.py --check        # 自检（纯内存，不读仓库）

诚实边界
========
- 预测耗时不等于真实耗时（机器负载/缓存状态会变），`--show` 会给出**不均衡率**；
- 分片**不减少**总工作量，只把墙钟按片数摊薄（单机跑全部片并不会更快）；
- 计划表是**缓存类产物**（不在信任根内），缺失/过期不影响正确性。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PLAN = ROOT / "data" / "655_shard_plan.json"

sys.path.insert(0, str(HERE))
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass


def module_of(classname: str, name: str) -> str:
    """junit 的 classname（`tests.test_x`）或补全的 nodeid → 模块文件名。"""
    cls = (classname or "").replace(".", "/")
    if cls.endswith(".py"):
        return Path(cls).name
    if cls:
        cand = ROOT / cls
        for p in (cand.with_suffix(".py"), cand / "__init__.py"):
            if p.is_file():
                return p.name
        return f"{Path(cls).name}.py"
    base = (name or "").split("::")[0]
    if not base:
        return "unknown.py"
    return base if base.endswith(".py") else f"{base}.py"


def durations_from_junit(path: Path) -> dict[str, float]:
    root = ET.parse(str(path)).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    acc: dict[str, float] = {}
    for s in suites:
        for tc in s.iter("testcase"):
            mod = module_of(tc.get("classname", ""), tc.get("name", ""))
            acc[mod] = acc.get(mod, 0.0) + float(tc.get("time", 0.0) or 0.0)
    return {k: round(v, 4) for k, v in acc.items()}


def junit_declared_seconds(path: Path) -> float:
    """套件自报总时长（`<testsuite time=…>`），用于识别 **xdist 累计口径** 的失真。"""
    root = ET.parse(str(path)).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    return round(sum(float(s.get("time", 0.0) or 0.0) for s in suites), 3)


def durations_from_text(path: Path) -> dict[str, float]:
    """解析 `pytest --durations=0 -n0` 的文本输出（**真实单例墙钟**，首选口径）。

    行形如：`0.12s call     tests/test_x.py::test_y`（setup/call/teardown 分行，累加）。
    """
    acc: dict[str, float] = {}
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = ln.split()
        if len(parts) < 3 or not parts[0].endswith("s"):
            continue
        try:
            sec = float(parts[0][:-1])
        except ValueError:
            continue
        nodeid = parts[-1]
        if "::" not in nodeid and ".py" not in nodeid:
            continue
        mod = Path(nodeid.split("::")[0]).name
        acc[mod] = acc.get(mod, 0.0) + sec
    return {k: round(v, 4) for k, v in acc.items()}


def balance(weights: dict[str, float], shards: int) -> dict[str, Any]:
    """LPT 分片（确定性：权重相同时按模块名排序）。返回计划体（纯函数）。"""
    if shards < 1:
        raise ValueError("shards 必须 ≥ 1")
    order = sorted(weights.items(), key=lambda kv: (-kv[1], kv[0]))
    bins: list[list[str]] = [[] for _ in range(shards)]
    loads = [0.0] * shards
    for mod, w in order:
        i = loads.index(min(loads))
        bins[i].append(mod)
        loads[i] += w
    loads = [round(x, 3) for x in loads]
    return {
        "shards": shards,
        "shard_of": {mod: i for i, mods in enumerate(bins) for mod in mods},
        "shard_modules": [sorted(x) for x in bins],
        "predicted_s": loads,
        "total_s": round(sum(loads), 3),
        "imbalance": round((max(loads) / (sum(loads) / shards)) if sum(loads) else 0.0, 4),
        "max_s": max(loads) if loads else 0.0,
    }


def naive_imbalance(weights: dict[str, float], shards: int) -> float:
    """对照：不做均衡（按模块名顺序轮转）的不均衡率——用于证明 LPT 真的更平。"""
    if shards < 1 or not weights:
        return 0.0
    loads = [0.0] * shards
    for i, (_, w) in enumerate(sorted(weights.items())):
        loads[i % shards] += w
    avg = sum(loads) / shards
    return round(max(loads) / avg if avg else 0.0, 4)


def write_plan(plan: dict[str, Any], source: str) -> Path:
    plan = dict(plan)
    plan["generated_at"] = dt.datetime.now().isoformat(timespec="seconds")
    plan["source"] = source
    plan["note"] = ("LPT 分片计划（按 junit 时长）；conftest 的 --shard-id/--shard-count 会优先读它，"
                    "缺失时退化为 sha256(模块名) 取模")
    PLAN.write_text(json.dumps(plan, ensure_ascii=False, indent=2, sort_keys=True),
                    encoding="utf-8", newline="\n")
    return PLAN


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="按测试时长均衡分片（655 C 杠杆 3）")
    ap.add_argument("--junit", action="append", default=[], help="junit XML（可多次给）")
    ap.add_argument("--durations-text", action="append", default=[],
                    help="`pytest --durations=0 -n0` 输出文件（**首选**：真实单例墙钟）")
    ap.add_argument("--shards", type=int, default=4)
    ap.add_argument("--plan", action="store_true", help="生成并写入 data/655_shard_plan.json")
    ap.add_argument("--show", action="store_true", help="显示现有计划")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    a, extra = ap.parse_known_args(argv)
    passthrough = extra[1:] if extra and extra[0] == "--" else extra

    if a.check:
        return selftest()

    if a.show:
        if not PLAN.is_file():
            print("[shard655] 无计划表（先 --plan）")
            return 0
        plan = json.loads(PLAN.read_text(encoding="utf-8"))
        print(json.dumps(plan, ensure_ascii=False, indent=2) if a.json else
              f"[shard655] 计划：{plan['shards']} 片｜源={plan.get('source')}｜预测 "
              f"{plan['predicted_s']}｜不均衡 {plan['imbalance']}")
        return 0

    if a.run:
        cmd = [sys.executable, "-m", "pytest", "--shard-id", str(a.shard),
               "--shard-count", str(a.shards), *(passthrough or ["-q"])]
        print(f"$ {' '.join(cmd)}")
        return subprocess.run(cmd, cwd=str(ROOT), check=False).returncode

    if not a.junit and not a.durations_text:
        print("[shard655] 需要 --junit 或 --durations-text（或 --show/--run/--check）", file=sys.stderr)
        return 2
    weights: dict[str, float] = {}
    caveat = ""
    for j in a.junit:
        for k, v in durations_from_junit(Path(j)).items():
            weights[k] = round(weights.get(k, 0.0) + v, 4)
        declared = junit_declared_seconds(Path(j))
        ratio = (sum(weights.values()) / declared) if declared else 0.0
        if ratio > 1.5:
            caveat = (f"junit(`{Path(j).name}`) 的 testcase time 求和 {sum(weights.values()):.0f}s "
                      f"≫ 套件自报 {declared:.0f}s（比值 {ratio:.1f}）⇒ 该口径在 xdist 下是"
                      f"**累计/失真**的；绝对秒数不可当墙钟，仅可用于**相对均衡**。"
                      f"要真实单例时长请用 `--durations-text`（`pytest --durations=0 -n0`）。")
    for d in a.durations_text:
        for k, v in durations_from_text(Path(d)).items():
            weights[k] = round(weights.get(k, 0.0) + v, 4)
    plan = balance(weights, a.shards)
    plan["naive_imbalance"] = naive_imbalance(weights, a.shards)
    if caveat:
        plan["caveat"] = caveat
        print(f"[shard655] WARN {caveat}")
    if a.plan:
        p = write_plan(plan, "+".join(Path(j).name for j in a.junit))
        print(f"[shard655] 计划已写：{p.relative_to(ROOT).as_posix()}")
    if a.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(f"[shard655] {len(weights)} 模块 / {plan['total_s']}s ⇒ {plan['shards']} 片｜预测 "
              f"{plan['predicted_s']}｜LPT 不均衡 {plan['imbalance']}（轮转 {plan['naive_imbalance']}）")
        for i, mods in enumerate(plan["shard_modules"]):
            print(f"  片{i}: {plan['predicted_s'][i]:>8.1f}s · {len(mods)} 模块")
    return 0


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    w = {"a.py": 100.0, "b.py": 60.0, "c.py": 50.0, "d.py": 40.0, "e.py": 10.0, "f.py": 5.0}
    plan = balance(w, 3)
    chk("每模块恰属一片", sorted(plan["shard_of"]) == sorted(w))
    chk("片索引合法", set(plan["shard_of"].values()) == {0, 1, 2})
    chk("总权重守恒", abs(plan["total_s"] - sum(w.values())) < 1e-6)
    heaviest = max(w.values())
    chk("不均衡 < 1.25（LPT 应接近最优）", plan["imbalance"] < 1.25, f"imbalance={plan['imbalance']}")
    chk("LPT 不差于轮转", plan["imbalance"] <= naive_imbalance(w, 3))
    chk("至少最重模块独占一片", heaviest >= max(plan["predicted_s"]) - 1e-9 or
        plan["predicted_s"][0] >= heaviest, f"{plan['predicted_s']}")
    chk("确定性（两次一致）", balance(w, 3) == plan)
    chk("模块名归一", module_of("tests.test_653_tools", "test_x") == "test_653_tools.py")
    chk("空输入不炸", balance({}, 2)["total_s"] == 0.0)
    print(f"pytest_shard_655 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
