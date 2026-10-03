#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_E.py — 676c-E 扩样并发高级：Task B（编译校验）+ Task C（检测器复现）。

零修改 tools/holdout_reveal_661.py：本脚本只在**运行时**做三件事——

1. `hr.ATOMS = data/expansion_676c_E`
   任务卡「任务 C 步骤 1」明确授权的 monkeypatch。这样 detect() 会去临时目录里
   拷贝样本编译，不会碰 Examples/atoms/（expA 的做法要往 atoms/ 里拷临时文件）。

2. 包一层 `hr._wsl`，做两件**不改变判定语义**的适配：
   a) exe 名去冲突：检测器固定用 /tmp/rv_bin_O0 / /tmp/rv_bin_O2，
      并发跑多个样本会互相覆盖二进制。按 worker 把 `/tmp/rv_bin_` 重写成
      `/tmp/rv_bin_<tag>_`，仅改文件名，不改编译参数、不改判定。
   b) 运行超时：任务卡「环境注意事项 5」要求死锁样本 `timeout 5`。
      检测器默认给运行 120s，35 个死锁样本 × 2 档 = 8400s 会把验证挂死。
      这里给**运行命令**加 `timeout N` 前缀（编译命令不加），并把 subprocess
      超时压到 15s。超时退出码 124 会被单独记录，交给 reconcile 判成
      「阻塞/死锁触发」。
   除此之外 detect() 的命中判据一字未动。

3. 记录 raw rc，供稳定性复跑与超时统计使用。

用法：
    python verify_E.py --stage syntax
    python verify_E.py --stage detect --workers 8
    python verify_E.py --stage stability --seed 6761
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
TOOLS = os.path.join(REPO, "tools")
ATOMS_REL = os.path.join("data", "expansion_676c_E").replace("\\", "/")
RESULTS = os.path.join(HERE, "verify_results.json")

#: 运行命令的墙钟上限（秒）。任务卡要求死锁样本 5s；这里给 6s 留一点
#: ASan/TSan 启动与退出报告的余量。
RUN_TIMEOUT = 6
SUBPROC_TIMEOUT = 20

#: 每类的备用检测资产：主资产 unknown/不可用时用它复核，避免因单资产不可用
#: 就把样本整体淘汰（card：TSan 在 WSL 不稳定是已知问题，不要因此淘汰）。
SECONDARY = {
    "memory_order": "asan",
    "atomic_ub": "ubsan",
    "deadlock": "asan",
    "aba_problem": "tsan",
    "lock_priority_inversion": "asan",
    "condition_variable": "asan",
}

_local = threading.local()
_tag_lock = threading.Lock()
_tag_seq = [0]


def _new_tag() -> str:
    with _tag_lock:
        _tag_seq[0] += 1
        return f"w{_tag_seq[0]}"


def _load_detector():
    spec = importlib.util.spec_from_file_location(
        "holdout_reveal_661", os.path.join(TOOLS, "holdout_reveal_661.py"))
    hr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hr)
    hr.ATOMS = os.path.join(REPO, ATOMS_REL)          # 授权的 monkeypatch
    return hr


HR = _load_detector()
RAW_RC: dict = {}
_RAW_LOCK = threading.Lock()

_orig_wsl = HR._wsl


def _patched_wsl(cmd: str, timeout=180):
    """见模块 docstring 第 2 点：exe 去冲突 + 运行加 timeout。"""
    tag = getattr(_local, "tag", None) or "w0"
    sid = getattr(_local, "sid", None) or "?"
    cmd2 = cmd.replace("/tmp/rv_bin_", f"/tmp/rv_bin_{tag}_")
    is_run = cmd2.lstrip().startswith(("setarch", "/tmp/rv_bin_"))
    if is_run:
        cmd2 = f"timeout {RUN_TIMEOUT} {cmd2}"
        timeout = SUBPROC_TIMEOUT
    rc, out = _orig_wsl(cmd2, timeout=timeout)
    exe = re.search(r"/tmp/rv_bin_[A-Za-z0-9_]+", cmd2)
    if is_run and exe:
        with _RAW_LOCK:
            RAW_RC.setdefault(sid, []).append(rc)
        _orig_wsl(f"rm -f {exe.group(0)}", timeout=30)   # 及时回收，避免 /tmp 堆积
    return rc, out


HR._wsl = _patched_wsl


def local_syntax(cpp: str):
    try:
        r = subprocess.run(["g++", "-std=c++17", "-O0", "-Wall", "-Wextra",
                            "-fsyntax-only", "-pthread", cpp],
                           capture_output=True, text=True, timeout=180)
    except Exception as e:  # noqa: BLE001
        return -1, f"local_error:{e}", []
    out = r.stdout + r.stderr
    warns = [ln.strip() for ln in out.splitlines() if "warning:" in ln]
    return r.returncode, out.strip(), warns


def _timeout_hit(note: str) -> bool:
    """detect() 的 note 里带 (rc=124) ⇒ 那一档被 timeout 杀掉 ⇒ 程序挂起。"""
    return "rc=124" in note


def run_detector(sid: str, kind: str):
    """返回 (verdict, note, hung)。hung=True 表示两档都因超时被杀（=阻塞/死锁）。"""
    if not hasattr(_local, "tag"):
        _local.tag = _new_tag()
    _local.sid = sid
    fname = f"sample_{sid}.cpp"
    try:
        verdict, note = HR.detect(kind, [fname])
    except Exception as e:  # noqa: BLE001
        return "unknown", f"detect_exception:{e}", False
    hung = _timeout_hit(note)
    if verdict == "miss" and hung:
        # 任务卡：「死锁样本超时挂起：视为 catch（死锁触发）」
        return "catch", f"[{kind}] 运行超时(rc=124) ⇒ 阻塞/死锁触发 | {note}", True
    return verdict, note, hung


def reconcile(expected: str, verdict: str, note: str):
    """返回 (pooled, 调和结论)。

    口径严格照任务卡「任务 C · 步骤 4」：
      - 一致                        -> 通过
      - 死锁样本超时挂起             -> 视为 catch（由 run_detector 先做rc=124 转换）
      - 真实盲区（实测 miss 而非 catch）-> **改标 miss，在 notes 里说明**，不淘汰
    淘汰只发生在卡片「淘汰标准」列出的情形：语法/编译失败、死锁不稳定、
    检测器不可用（unknown）。本函数只管判定调和，淘汰由 pooled=False 表达。
    """
    if verdict == "catch":
        if expected == "miss":
            return True, "updated_to_catch"
        return True, "consistent"
    if verdict == "miss":
        if expected == "miss":
            return True, "consistent_blindspot"
        # 预期 catch 实测 miss：卡片要求改标 miss（真实盲区），不是淘汰
        return True, "downgraded_to_miss_real_blindspot"
    return False, f"detector_{verdict}"


def stage_syntax(ids):
    out = {}
    for sid in ids:
        cpp = os.path.join(HERE, f"sample_{sid}.cpp")
        rc, msg, warns = local_syntax(cpp)
        out[sid] = {"syntax_rc": rc, "syntax_warnings": warns[:5],
                    "syntax_head": msg[:200]}
        print(f"  {sid} syntax_rc={rc} warn={len(warns)}", flush=True)
    return out


def stage_detect(ids, workers: int):
    res: dict = {}

    def job(sid):
        jp = os.path.join(HERE, f"sample_{sid}.json")
        meta = json.load(open(jp, encoding="utf-8"))
        primary = (meta.get("expected_detectors") or ["tsan"])[0]
        v1, n1, h1 = run_detector(sid, primary)
        rec = {"primary_kind": primary, "primary_verdict": v1,
               "primary_note": n1[:400], "hung": h1}
        pooled, rec_ = reconcile(meta["expected_verdict"], v1, n1)
        rec["reconcile"] = rec_
        rec["pooled"] = pooled
        # 主资产不可用 → 用备用资产复核（记录，不掩盖）
        if v1 == "unknown":
            sec = SECONDARY.get(meta["defect_type"], "asan")
            if sec != primary:
                v2, n2, h2 = run_detector(sid, sec)
                rec["secondary_kind"] = sec
                rec["secondary_verdict"] = v2
                rec["secondary_note"] = n2[:400]
                rec["hung"] = rec["hung"] or h2
                pooled2, rec2 = reconcile(meta["expected_verdict"], v2, n2)
                if pooled2 and not pooled:
                    rec["reconcile"] = f"{rec_}->{rec2}(via {sec})"
                    rec["pooled"] = True
        with _RAW_LOCK:
            rec["raw_rc"] = list(RAW_RC.get(sid, []))
            RAW_RC.pop(sid, None)
        rec["elapsed_s"] = None
        return sid, rec

    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for sid, rec in ex.map(job, ids):
            res[sid] = rec
            print(f"  {sid} {rec['primary_kind']}={rec['primary_verdict']:<8} "
                  f"hung={rec['hung']} pooled={rec['pooled']} "
                  f"({rec['reconcile']})", flush=True)
    return res


def stage_stability(ids, seed: int, workers: int, rounds: int):
    """对给定子集重复跑主资产，统计同一 verdict 的重复一致率。"""
    res: dict = {}

    def job(sid):
        meta = json.load(open(os.path.join(HERE, f"sample_{sid}.json"),
                             encoding="utf-8"))
        kind = (meta.get("expected_detectors") or ["tsan"])[0]
        seen = []
        hung = []
        for _ in range(rounds):
            v, n, h = run_detector(sid, kind)
            seen.append(v)
            hung.append(h)
        return sid, {"kind": kind, "verdicts": seen, "hung": hung,
                     "stable": len(set(seen)) == 1}

    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for sid, rec in ex.map(job, ids):
            res[sid] = rec
            print(f"  {sid} {rec['kind']} {rec['verdicts']} "
                  f"stable={rec['stable']}", flush=True)
    return res


def load_results():
    if os.path.isfile(RESULTS):
        return json.load(open(RESULTS, encoding="utf-8"))
    return {}


def save_results(r):
    json.dump(r, open(RESULTS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def all_ids():
    ids = []
    for f in sorted(os.listdir(HERE)):
        m = re.fullmatch(r"sample_(E\d{3})\.json", f)
        if m:
            ids.append(m.group(1))
    return ids


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True,
                    choices=["syntax", "detect", "stability", "flaky"])
    ap.add_argument("--ids", default="",
                    help="flaky 阶段用：逗号分隔的 sample id 列表")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed", type=int, default=6761)
    ap.add_argument("--ratio", type=float, default=0.2)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=200)
    a = ap.parse_args()

    ids = [f"E{i:03d}" for i in range(a.start, a.end + 1)
           if f"E{i:03d}" in all_ids()]
    print(f"[stage={a.stage}] 样本 {len(ids)} 个，workers={a.workers}", flush=True)
    t0 = time.time()
    r = load_results()

    if a.stage == "syntax":
        syn = stage_syntax(ids)
        for sid, rec in syn.items():
            r.setdefault(sid, {}).update(rec)
    elif a.stage == "detect":
        det = stage_detect(ids, a.workers)
        for sid, rec in det.items():
            r.setdefault(sid, {}).update(rec)
    elif a.stage == "flaky":
        sub = [s.strip() for s in a.ids.split(",") if s.strip()]
        print(f"[flaky] 复跑 {len(sub)} 个样本 x {a.rounds} 轮", flush=True)
        stab = stage_stability(sub, a.seed, a.workers, a.rounds)
        for sid, rec in stab.items():
            r.setdefault(sid, {})["flakiness"] = rec
        for sid in sub:
            rec = stab[sid]
            n_c = sum(1 for v in rec["verdicts"] if v == "catch")
            print(f"  {sid} {rec['kind']:<6} catch {n_c}/{a.rounds} "
                  f"verdicts={rec['verdicts']}", flush=True)
    else:
        pool = [s for s in ids
                if r.get(s, {}).get("pooled") or r.get(s, {}).get("stage")]
        random.seed(a.seed)
        sub = sorted(random.sample(pool, max(1, int(len(pool) * a.ratio))))
        print(f"[stability] 抽 {len(sub)}/{len(pool)} 个复跑 {a.rounds} 轮", flush=True)
        stab = stage_stability(sub, a.seed, a.workers, a.rounds)
        for sid, rec in stab.items():
            r.setdefault(sid, {}).update({"stability": rec})
        print(json.dumps({"subset": sub}, ensure_ascii=False))

    save_results(r)
    print(f"[stage={a.stage}] 用时 {time.time()-t0:.1f}s -> {RESULTS}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
