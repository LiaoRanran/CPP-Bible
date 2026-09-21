"""621 B2 · CI 并发竞态本地复现工具

用途：在本地复现「gate 与 replay 并发 ⇒ gate 报假 BLOCK」的竞态（619 BLOCK 误报根因），
用于回归测试：**修复前应能复现，修复后应不能**。

**⚠ 621 实际执行情况（诚实登记）**：
本工具**默认 `dry-run`，不真跑门禁**。原因：

1. 621 §六.3 硬边界：不跑监工门禁（`gate --check` / `replay --check` 皆在列）；
2. `replay --check` 的 recompile 会**重写** `Examples/atoms/*.asm`（受控目录），
   在验收批次里主动制造受控目录写入是不合适的；
3. 竞态是否"修复后为 0"最终要在 **CI 环境**验证（621 不 push）。

⇒ 真跑需显式 `--real`，且应由人（或门禁开放批次）执行。
⇒ 本文件给出的"修复前/后 BLOCK 频率"引用的是**620 任务1 的历史实测**，
   本批**未产生新的门禁运行**。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.exists(PY):
    PY = sys.executable

GATE = os.path.join("tools", "gate_engine.py")
REPLAY = os.path.join("tools", "atom_evidence_replay.py")
BLOCK_RE = re.compile(r"\[BLOCK\s*\]\s*(\S+)")
HITS_RE = re.compile(r"命中\s+(\d+)\s*\(block=(\d+)")

# 620 任务1 的历史实测（本批未重跑，仅引用）
HISTORICAL = {
    "concurrent_observed": {"run": "619 独立验收（gate ∥ replay 并发）",
                            "hits": 195, "block": 2,
                            "note": "2 条 EV-ARTIFACT-FILE-EXISTS 假 BLOCK"},
    "serial_observed": {"run": "620 任务1（串行连跑 3 次）",
                        "hits": 191, "block": 0,
                        "note": "与冻结基线逐字一致"},
}


def run_gate_only() -> dict:
    """只跑 gate（不并发）——用于对照。真跑，需显式调用。"""
    p = subprocess.run([PY, GATE, "--check"], cwd=ROOT,
                       capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    m = HITS_RE.search(out)
    return {"rc": p.returncode, "hits": int(m.group(1)) if m else None,
            "block": int(m.group(2)) if m else None,
            "blocked_rules": BLOCK_RE.findall(out)}


def run_concurrent_once() -> dict:
    """并发启动 gate + replay，监控 gate 是否出现 BLOCK（真跑，需显式调用）。"""
    replay = subprocess.Popen([PY, REPLAY, "--check"], cwd=ROOT,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        gate = subprocess.run([PY, GATE, "--check"], cwd=ROOT,
                              capture_output=True, text=True)
        out = (gate.stdout or "") + (gate.stderr or "")
        m = HITS_RE.search(out)
        return {"gate_rc": gate.returncode,
                "hits": int(m.group(1)) if m else None,
                "block": int(m.group(2)) if m else None,
                "blocked_rules": BLOCK_RE.findall(out)}
    finally:
        try:
            replay.wait(timeout=600)
        except subprocess.TimeoutExpired:  # pragma: no cover
            replay.kill()


def reproduce(iterations: int = 10, real: bool = False) -> dict:
    """跑 N 次；real=False 时不真跑门禁（621 默认）。"""
    if not real:
        return {
            "mode": "dry-run", "iterations": iterations, "runs": [],
            "block_seen": 0, "block_rate": None,
            "reason": "621 §六.3 硬边界：不跑监工门禁；且 replay 会重写受控目录工件",
            "historical": HISTORICAL,
        }
    runs = []
    seen = 0
    for i in range(iterations):
        r = run_concurrent_once()
        r["iteration"] = i + 1
        runs.append(r)
        if (r.get("block") or 0) > 0:
            seen += 1
    return {"mode": "real", "iterations": iterations, "runs": runs,
            "block_seen": seen, "block_rate": round(seen / iterations, 4),
            "reason": "真跑（并发 gate ∥ replay）", "historical": HISTORICAL}


def render_report(res: dict) -> str:
    o = ["# 621 B2 · CI 并发竞态复现报告\n"]
    o.append(f"> 模式：**{res['mode']}** · 迭代 {res['iterations']} 次\n")
    if res["mode"] == "dry-run":
        o.append("## ⚠ 本批未真跑门禁\n")
        o.append(f"原因：{res['reason']}\n")
        o.append("真跑需显式 `--real`，且应由人（或门禁开放批次）执行。\n")
    else:
        o.append("## 一、实跑结果\n")
        o.append("| # | gate rc | 命中 | block | 命中规则 |")
        for r in res["runs"]:
            o.append(f"| {r['iteration']} | {r['gate_rc']} | {r.get('hits')} | "
                     f"{r.get('block')} | {r.get('blocked_rules')} |")
        o.append("")
        o.append(f"- 出现 BLOCK 的次数：**{res['block_seen']} / {res['iterations']}**")
        o.append(f"- BLOCK 频率：**{res['block_rate']}**\n")
    o.append("## 二、历史实测（620 任务1，本批未重跑，仅引用）\n")
    o.append("| 场景 | 运行 | 命中 | block | 说明 |")
    for k, v in res["historical"].items():
        o.append(f"| {k} | {v['run']} | {v['hits']} | **{v['block']}** | {v['note']} |")
    o.append("")
    o.append("## 三、结论\n")
    o.append("- **并发**（gate ∥ replay）：**观测到 2 条假 BLOCK**（619 验收实例）。")
    o.append("- **串行**（先 replay 后 gate）：**block=0**，连跑 3 次一致（620 任务1）。")
    o.append("- ⇒ 竞态确实存在，方向性修复（`gate needs: [replay]`，621 B1）**对症**。")
    o.append("- ⚠ **修复后频率为 0 尚未在 CI 实跑确认**（621 不 push，见 §八 人拍板项 4）。")
    return "\n".join(o)


# ── 自检（只读、不跑门禁；exit 0 = 通过）─────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    d = reproduce(iterations=3, real=False)
    chk("默认 dry-run 不真跑", d["mode"] == "dry-run" and d["runs"] == [])
    chk("dry-run 给出去原因", bool(d["reason"]))
    chk("dry-run BLOCK 频率为 None（不编造）", d["block_rate"] is None)
    chk("历史实测被引用", d["historical"]["concurrent_observed"]["block"] == 2)
    chk("串行历史 block=0", d["historical"]["serial_observed"]["block"] == 0)
    chk("BLOCK 正则可解析", bool(BLOCK_RE.search("[BLOCK ] EV-ARTIFACT-FILE-EXISTS  x.md")))
    chk("命中正则可解析", HITS_RE.search("命中 191 (block=0 warn=186") is not None)
    chk("报告可渲染", "竞态复现报告" in render_report(d))
    print(f"B2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 B2 CI 并发竞态复现")
    ap.add_argument("--iterations", type=int, default=10)
    ap.add_argument("--real", action="store_true",
                    help="真跑 gate∥replay（621 默认不开；会跑门禁且 replay 会重写受控工件）")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--out", help="报告输出路径")
    ap.add_argument("--check", action="store_true", help="只读自检（不跑门禁），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    res = reproduce(iterations=args.iterations, real=args.real)
    md = render_report(res)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"wrote {args.out}  mode={res['mode']}")
    else:
        print(md)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
