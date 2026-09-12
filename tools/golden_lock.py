#!/usr/bin/env python3
"""S4 黄金非回归锁：达标状态固化为快照，任何指标**恶化** → exit 1。

底座 = ADR-0005（`l2_state.py` 的快照-漂移三件套：measure → save → check）。

指标（全部机器可复算，禁止手工填写）：
    block_findings   gate_engine 的 block 级命中数（↑ = 质量下降 → 红）
    warn_findings    warn 级命中数（↑ = 记债增加 → 红）
    atoms_total      原子数（↓ = 回滚 → 红）
    evidence_total   证据卡数（↓ = 证据被删 → 红）
    verified_atoms   已验证原子总数（三级合计，↓ = 降级 → 红）
    human_verified   human-verified 级（含历史别名 verified）（↓ = 降级 → 红）
    red_team_verified red-team-verified 级（↓ = 降级 → 红）
    machine_verified machine-verified 级（↓ = 降级 → 红）
    dal_gap          DAL A/B 却非人级验证的原子数（↑ = 越权放行 → 红）
    replay_confirm   证据卡机器复算通过数（↓ = 证据失效 → 红）
    replay_infra_error 证据卡复算的环境层故障数（↑ = 环境恶化/有人在借 infra 逃逸 → 红）

语义：
    * 恶化 → 红；改善（数量↑ / 命中↓）→ 提示 `sync` 更新基线。
    * 口径/阈值变更**不得静默**：`check --accept "理由"` 显式接受并写入快照审计字段。
    * **接受即同步基线**（2026-09-12，369 任务7）：accept 时把**当期测量**写入 `metrics`
      （否则"接受了但基线仍旧"，下一轮 check 会重复报同一条恶化、台账膨胀）。
    * **provenance 机器填写**（369 任务7）：`commit` = `git rev-parse --short HEAD`，
      `dirty` = 工作树是否非空——sync/accept 常在未提交改动之后发生，单记 commit 会记错
      "哪份工作树"；两条审计字段一律机器写，不让人手输。

用法：
    python tools/golden_lock.py sync                    # 达标时固化快照
    python tools/golden_lock.py check                   # 比对（CI / prepush 用）
    python tools/golden_lock.py check --accept "理由"    # 显式接受恶化（留痕）
    python tools/golden_lock.py show
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any, Sequence, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

STATE = ROOT / "tools/golden_state.json"
SCHEMA = "cppbible-golden-lock/1.0"

# key → True 表示「上升是恶化」，False 表示「下降是恶化」
WORSE: dict[str, bool] = {
    "block_findings": True,
    "warn_findings": True,
    "atoms_total": False,
    "evidence_total": False,
    "verified_atoms": False,
    "replay_confirm": False,
    # G6 四级状态（2026-09-12）：按级别分列——任一级下降即降级 = 恶化。
    # 只盯总数会被"人级掉 1 / 红队级涨 1"这类置换掩盖（总数不变、保证级别其实降了）。
    "human_verified": False,
    "red_team_verified": False,
    "machine_verified": False,
    # DAL A/B 却非人级验证 = 硬约束破口，上升即恶化（放权不得从这条缝漏出去）
    "dal_gap": True,
    # G6 §4.1：infra_error 不污染 replay_confirm（否则环境抖动会拉低基线、掩盖真实退化），
    # 但它**必须被单独盯住**——否则"把夹具写坏 ⇒ 落到 infra ⇒ confirm 不降"就是新的逃生舱。
    # 故拆成两列：confirm 下降是恶化，infra 上升也是恶化，中间没有缝。
    "replay_infra_error": True,
}


def measure() -> dict[str, int]:
    """全部指标现场复算（不读任何手工数字）。"""
    import gate_engine as ge
    import atom_evidence_replay as replay

    findings = ge.run(include_advice=False)
    atoms_root, evid_root = Path(ge.ATOMS), Path(ge.EVIDENCE)
    atoms = sorted(atoms_root.rglob("ATOM-*.md")) if atoms_root.exists() else []
    evids = sorted(evid_root.rglob("EV-*.md")) if evid_root.exists() else []

    def _status(p: Path) -> str:
        try:
            return str(replay.parse_frontmatter(
                p.read_text(encoding="utf-8", errors="replace")).get("status") or "")
        except ValueError:
            return ""

    def _dal(p: Path) -> str:
        try:
            return str(replay.parse_frontmatter(
                p.read_text(encoding="utf-8", errors="replace")).get("dal") or "").strip().upper()
        except ValueError:
            return ""

    # 级别分列口径与 gate_engine 保持一致（`verified` = 历史别名 → human 级）
    tier_of = {"human-verified": "human", "verified": "human",
               "red-team-verified": "redteam", "machine-verified": "machine"}
    tiers = {"human": 0, "redteam": 0, "machine": 0}
    dal_gap = 0
    for p in atoms:
        tier = tier_of.get(_status(p))
        if not tier:
            continue
        tiers[tier] += 1
        if tier != "human" and _dal(p) in ("A", "B"):
            dal_gap += 1

    confirm = infra = 0
    for p in evids:
        verdict, _ = replay.replay_card(p, do_sanitizer=False)
        if verdict == "confirm":
            confirm += 1
        elif verdict.startswith("infra_error:"):
            infra += 1

    return {
        "block_findings": sum(1 for f in findings if f.severity == "block"),
        "warn_findings": sum(1 for f in findings if f.severity == "warn"),
        "atoms_total": len(atoms),
        "evidence_total": len(evids),
        "verified_atoms": sum(tiers.values()),
        "human_verified": tiers["human"],
        "red_team_verified": tiers["redteam"],
        "machine_verified": tiers["machine"],
        "dal_gap": dal_gap,
        "replay_confirm": confirm,
        "replay_infra_error": infra,
    }


def _load() -> dict[str, Any]:
    if not STATE.exists():
        return {"schema": SCHEMA, "updated": "", "commit": "", "metrics": {},
                "accepted": []}
    return cast(dict[str, Any], json.loads(STATE.read_text(encoding="utf-8")))


def _save(state: dict[str, Any]) -> None:
    payload = json.dumps(state, ensure_ascii=False, indent=1) + "\n"
    STATE.write_bytes(payload.encode("utf-8"))


def _git_provenance() -> tuple[str, bool]:
    """返回 (HEAD 短哈希, 工作树是否脏)——机器填写，不让人手输（369 任务7）。

    `dirty=True` 表示该快照对应"HEAD + 尚未提交的改动"（sync/accept 常发生在改完规则
    但还没 commit 时，单记 commit 会把"哪份工作树"记错）。
    """
    import subprocess
    commit, dirty = "", False
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT),
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=10, check=False)
        if r.returncode == 0:
            commit = (r.stdout or "").strip()
        d = subprocess.run(["git", "status", "--porcelain"], cwd=str(ROOT),
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=10, check=False)
        dirty = bool((d.stdout or "").strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return commit, dirty


def cmd_sync() -> int:
    state = _load()
    commit, dirty = _git_provenance()
    state.update({"schema": SCHEMA, "updated": _dt.date.today().isoformat(),
                  "commit": commit, "dirty": dirty, "metrics": measure()})
    _save(state)
    print(f"[golden] 快照已固化：{state['metrics']}"
          f"（commit={commit or '?'} dirty={dirty}）")
    return 0


def cmd_check(accept: str | None) -> int:
    state = _load()
    base = state.get("metrics") or {}
    if not base:
        print("[golden] 无基线——先跑 `sync` 固化当前达标状态")
        return 2
    now = measure()
    worse: list[str] = []
    improved: list[str] = []
    for key, up_is_worse in WORSE.items():
        b, n = base.get(key, 0), now.get(key, 0)
        if (n > b) if up_is_worse else (n < b):
            worse.append(f"{key}: {b} → {n}")
        elif (n < b) if up_is_worse else (n > b):
            improved.append(f"{key}: {b} → {n}")
    print(f"[golden] 恶化 {len(worse)} · 改善 {len(improved)}")
    for w in worse:
        print(f"  WORSE {w}")
    for i in improved:
        print(f"  BETTER {i}")
    if worse:
        if accept:
            commit, dirty = _git_provenance()
            state.setdefault("accepted", []).append(
                {"ts": _dt.datetime.now().isoformat(timespec="seconds"),
                 "reason": accept,
                 "worse": worse,            # 机器自动生成：与当期测量同源（非人手输）
                 "metrics_after": now,      # 机器勾稽：接受后的基线快照，可与 metrics 对账
                 "commit": commit, "dirty": dirty})
            # 接受即同步基线：否则"接受了但基线仍旧"，下一轮 check 重复报同一条恶化
            state["metrics"] = now
            state["updated"] = _dt.date.today().isoformat()
            state["commit"] = commit
            state["dirty"] = dirty
            _save(state)
            print(f"[golden] 已显式接受并留痕（{len(state['accepted'])} 条审计记录）；"
                  f"基线已同步至当期测量（commit={commit or '?'} dirty={dirty}）")
            return 0
        print("[golden] ✗ 指标恶化——修复，或 `check --accept \"理由\"` 显式留痕")
        return 1
    if improved:
        print("[golden] 有改善：跑 `sync` 更新基线（把进步锁进黄金快照）")
    print("[golden] ✅ 无恶化")
    return 0


def cmd_show() -> int:
    state = _load()
    print(json.dumps(state, ensure_ascii=False, indent=1))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="S4 黄金非回归锁")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sync", help="固化当前状态为快照").set_defaults(fn=lambda _a: cmd_sync())
    p_ck = sub.add_parser("check", help="比对快照，恶化即 exit 1")
    p_ck.add_argument("--accept", help="显式接受恶化（必须给理由，审计留痕）")
    p_ck.set_defaults(fn=lambda a: cmd_check(a.accept))
    sub.add_parser("show", help="查看快照").set_defaults(fn=lambda _a: cmd_show())
    a = ap.parse_args(argv)
    return int(a.fn(a))


if __name__ == "__main__":
    raise SystemExit(main())
