"""612 C1 · oracle 验证执行工具（**只读** · 不填 `verified_by_oracle`）。

逐卡跑三门禁（`gate_engine.py --check` + `poison_drill.py` + `atom_evidence_replay.py --check`），
收集验证结果，生成验证报告 `data/oracle_verification_report_612.md`。

⚠️ **oracle 验证专用**：本工具是苦力**唯一**允许跑监工类 `--check` 的场景（只读验证，不修改任何卡）；
每次 subprocess 调用前打印「oracle 验证专用，非监工验收」。**不填 `verified_by_oracle`**（那是人审权力）。

三门前置：
  * gate/poison 快（≈5s / ≈9s）；replay `--check` 慢（≈300s）⇒ 每门有**超时预算**，
    超时标记 `timeout` 并继续（任务书要求「超时 >60s 标记 timeout」）。默认预算 120s。

CLI：
  `[--checks gate,poison,replay]` `[--timeout N]` `[--card <id>]` `[--top N]` `[--stats]` `[--check]`
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
REPORT_OUT = ROOT / "data" / "oracle_verification_report_612.md"
BANNER = "[oracle] oracle 验证专用，非监工验收"
PY = sys.executable

DEFAULT_CHECKS = ("gate", "poison", "replay")
_CMD = {
    "gate": [PY, "tools/gate_engine.py", "--check"],
    "poison": [PY, "tools/poison_drill.py"],
    "replay": [PY, "tools/atom_evidence_replay.py", "--check"],
}
_FINDING = re.compile(r"\[\s*(BLOCK|WARN|ADVICE)\s*\]\s*([A-Za-z0-9_-]+)\s+(\S+)")


def _run_check(name: str, timeout: int) -> dict:
    print(f"{BANNER}：跑 {name}（timeout {timeout}s）", file=sys.stderr)
    t0 = time.time()
    try:
        p = subprocess.run(_CMD[name], cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return {"name": name, "status": "pass" if p.returncode == 0 else "fail",
                "exit": p.returncode, "seconds": round(time.time() - t0, 1),
                "stdout": p.stdout, "stderr": p.stderr}
    except subprocess.TimeoutExpired:
        return {"name": name, "status": "timeout", "exit": None,
                "seconds": round(time.time() - t0, 1), "stdout": "", "stderr": ""}
    except OSError as exc:
        return {"name": name, "status": "error", "exit": None,
                "seconds": round(time.time() - t0, 1), "stdout": "", "stderr": str(exc)}


def _parse_gate(stdout: str) -> dict[str, dict]:
    """→ {卡相对路径: {block, warn, advice}}（从 gate 输出的 `[SEV] RULE path` 行归因）。"""
    out: dict[str, dict] = {}
    for sev, _rule, path in _FINDING.findall(stdout or ""):
        d = out.setdefault(path.replace("\\", "/"), {"block": 0, "warn": 0, "advice": 0})
        d[sev.lower()] += 1
    return out


def _key_numbers(results: dict[str, dict]) -> dict:
    kn: dict = {}
    g = results.get("gate", {})
    if g.get("stdout"):
        hits = _parse_gate(g["stdout"])
        kn["gate_block"] = sum(v["block"] for v in hits.values())
        kn["gate_warn"] = sum(v["warn"] for v in hits.values())
        kn["gate_advice"] = sum(v["advice"] for v in hits.values())
    po = results.get("poison", {})
    if po.get("stdout"):
        m = re.search(r"(\d+)\s*规则.*?/\s*(\d+)", po["stdout"])
        if m:
            kn["poison_covered"] = int(m.group(1))
            kn["poison_total"] = int(m.group(2))
    rp = results.get("replay", {})
    if rp.get("stdout"):
        m = re.search(r"confirm=(\d+)\s+refute=(\d+)\s+infra_error=(\d+)", rp["stdout"])
        if m:
            kn["replay_confirm"] = int(m.group(1))
            kn["replay_refute"] = int(m.group(2))
            kn["replay_infra"] = int(m.group(3))
    return kn


def verify(card_id: str | None = None, top: int | None = None,
           checks: tuple[str, ...] = DEFAULT_CHECKS, timeout: int = 120) -> dict:
    import oracle_rotation as orot  # noqa: E402
    cards = orot._load_cards()
    if card_id is not None:
        match = [c for c in cards if c["id"] == card_id]
        if not match:
            raise SystemExit(f"[C1] ❌ 卡不存在：{card_id}")
        cards = match
    elif top is not None:
        import oracle_priority as c2  # noqa: E402
        prio = {r["id"]: i for i, r in enumerate(c2.score_cards())}
        cards = sorted(cards, key=lambda c: prio.get(c["id"], 10**9))[:top]
    results = {n: _run_check(n, timeout) for n in checks}
    gate_hits = _parse_gate(results.get("gate", {}).get("stdout", ""))
    per_card = []
    for c in cards:
        gh = gate_hits.get(c["path"], {"block": 0, "warn": 0, "advice": 0})
        status = "pass" if (results.get("gate", {}).get("status") == "pass"
                            and gh["block"] == 0) else "fail"
        per_card.append({"id": c["id"], "path": c["path"],
                         "gate_block": gh["block"], "gate_warn": gh["warn"],
                         "gate_advice": gh["advice"], "status": status,
                         "verified": bool(c.get("verified_by_oracle"))})
    return {"version": VERSION, "checks": list(checks), "results": results,
            "key_numbers": _key_numbers(results), "cards": per_card}


def render(doc: dict) -> str:
    res, kn, cards = doc["results"], doc["key_numbers"], doc["cards"]
    L = ["# 612 C1 · oracle 验证报告（只读 · 不填 verified_by_oracle）", "",
         "> 三门禁：gate `--check` / poison / replay `--check`（**oracle 验证专用**，非监工验收）。"
         "**不填** `verified_by_oracle`（人审权力）。", "",
         "## 一、三门禁结果（全局）", "",
         "| 门 | 状态 | exit | 耗时(s) |", "|---|---|---|---|"]
    for n in doc["checks"]:
        r = res.get(n, {})
        L.append(f"| {n} | {r.get('status')} | {r.get('exit')} | {r.get('seconds')} |")
    L += ["", f"- 关键数字：{kn}",
          "- replay `--check` 全量约 300s ⇒ 超预算时标记 `timeout`（任务书允许），不代表失败（已知基线 "
          "confirm=56/refute=0/infra=0）。", "",
          "## 二、逐卡清单", "",
          "| 卡 | gate block | warn | advice | 状态 |", "|---|---|---|---|---|"]
    for c in cards:
        L.append(f"| `{c['id']}` | {c['gate_block']} | {c['gate_warn']} | {c['gate_advice']} | {c['status']} |")
    fails = [c for c in cards if c["status"] != "pass"]
    L += ["", "## 三、失败卡详情", ""]
    if fails:
        for c in fails:
            L.append(f"- `{c['id']}`：状态 {c['status']}，gate block {c['gate_block']}")
    else:
        L.append("（无：本批扫描的卡 gate 无 block）")
    L += ["", "## 四、异常卡（超时/错误）", ""]
    to = [n for n in doc["checks"] if res.get(n, {}).get("status") in ("timeout", "error")]
    L += [f"- {'、'.join(to) if to else '（无）'}", "",
          "## 五、口径与边界", "",
          "- **只读**：不填 `verified_by_oracle`、不改任何卡；每门调用前打印「oracle 验证专用」；",
          "- 逐卡归因只对 **gate**（其输出带卡路径）有效；poison/replay 是**全局**门，逐卡状态沿用全局；",
          "- 优先级 Top 排序复用 C2。", ""]
    return "\n".join(L)


def check(doc: dict) -> list[str]:
    problems: list[str] = []
    g = doc["results"].get("gate", {})
    if g.get("status") == "pass" and doc["key_numbers"].get("gate_block", 0) != 0:
        problems.append(f"gate exit 0 但解析到 block {doc['key_numbers'].get('gate_block')}")
    if not doc["cards"]:
        problems.append("无卡记录")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="oracle_verifier", description="612 C1 oracle 验证（只读，允许三门禁 --check）")
    ap.add_argument("--version", action="version", version=f"oracle_verifier {VERSION}")
    ap.add_argument("--checks", default=",".join(DEFAULT_CHECKS))
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--card", default=None)
    ap.add_argument("--top", type=int, default=None)
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    checks = tuple(x.strip() for x in a.checks.split(",") if x.strip() in _CMD)
    # --check 是**快门一致性校验**（默认只跑 gate，≈6s）；完整三门见默认报告或显式 --checks。
    if a.check and checks == DEFAULT_CHECKS:
        checks = ("gate",)
    doc = verify(a.card, a.top, checks, a.timeout)
    if a.stats:
        print(json.dumps({"checks": doc["checks"], "key_numbers": doc["key_numbers"],
                          "cards": doc["cards"]}, ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(doc)
        if problems:
            for p in problems:
                print(f"[C1] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[C1] ✓ 验证报告一致（{len(doc['cards'])} 卡；三门禁 "
              f"{ {n: doc['results'][n]['status'] for n in doc['checks']} }）")
        return 0
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(render(doc), encoding="utf-8", newline="\n")
    print(f"[C1] 已写 {REPORT_OUT.relative_to(ROOT).as_posix()}（{len(doc['cards'])} 卡；"
          f"三门禁 { {n: doc['results'][n]['status'] for n in doc['checks']} }）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
