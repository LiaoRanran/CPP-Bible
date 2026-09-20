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
    * **warn 会计制度：停止"整体 accept"**（2026-09-15，530 任务5）：`--accept` 必须同时给
      `--classify 规则ID=real|false_positive|legacy|accepted[,...]`，**无分类一律 exit 非 0**。
      四桶语义：
        real            真债——规则对、内容真有问题，须修内容（挂债台账）
        false_positive  误报——规则口径过宽，须修规则
        legacy          历史遗留——口径迁移期名单，约定清零期限
        accepted        已接受——明确认可为长期现状（如命题签署回填的中间态）
      每个 warn 规则只准落一桶；分类结果存 `warn_classify`，`check`/`buckets` 按桶复算。

用法：
    python tools/golden_lock.py sync                    # 达标时固化快照
    python tools/golden_lock.py check                   # 比对（CI / prepush 用）
    python tools/golden_lock.py check --accept "理由" \
        --classify "RID=real,OTHER=legacy"              # 显式接受恶化（必须分类，留痕）
    python tools/golden_lock.py buckets                 # 四桶只读盘点
    python tools/golden_lock.py show
"""

# mypy: ignore-errors
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

# warn 归属四桶（530 任务5）。顺序 = 输出顺序，也是"该修谁"的优先级：真债在最前。
CLASSES: tuple[str, ...] = ("real", "false_positive", "legacy", "accepted")
# 未分类不是合法的"桶"，而是**尚未做人审**的显式状态——它必须在输出里可见，
# 否则"未分类"会被静默塞进某一桶，等于变相整体 accept。
UNCLASSIFIED = "unclassified"


def _parse_classify(spec: str | None) -> dict[str, str]:
    """解析 `--classify A=real,B=legacy`。任何一项非法 → ValueError（调用方转 exit 非 0）。

    拒不接受"空分类"：`--classify` 存在但解析出 0 条 = 没分类，与不给参数同罪。
    """
    out: dict[str, str] = {}
    for item in (spec or "").split(","):
        item = item.strip()
        if not item:
            continue
        rid, sep, cls = item.partition("=")
        if not sep:
            raise ValueError(f"分类项缺 `=`：{item!r}"
                             f"（格式 规则ID={'|'.join(CLASSES)}）")
        rid, cls = rid.strip(), cls.strip()
        if not rid:
            raise ValueError(f"分类项缺规则 ID：{item!r}")
        if cls not in CLASSES:
            raise ValueError(f"未知分类 {cls!r}（合法：{'|'.join(CLASSES)}）")
        out[rid] = cls
    if not out:
        raise ValueError("--classify 未解析出任何分类（形如 -classify RID=real）")
    return out


def warn_buckets(findings: Sequence[Any] | None = None) -> dict[str, dict[str, int]]:
    """把当前 warn 命中**按规则**分进四桶（+ 未分类），供 `check`/`buckets` 复算。

    分类表来自快照的 `warn_classify`（旧快照无此键 → 全落未分类，不崩）。
    """
    import gate_engine as ge

    if findings is None:
        findings = ge.run(include_advice=False)
    by_rule: dict[str, int] = {}
    for f in findings:
        if getattr(f, "severity", "") == "warn":
            rid = str(getattr(f, "rule_id", "?"))
            by_rule[rid] = by_rule.get(rid, 0) + 1
    cmap = _load().get("warn_classify")
    cmap = cmap if isinstance(cmap, dict) else {}
    out: dict[str, dict[str, int]] = {c: {} for c in (*CLASSES, UNCLASSIFIED)}
    for rid in sorted(by_rule):
        cls = str(cmap.get(rid) or "")
        out[cls if cls in CLASSES else UNCLASSIFIED][rid] = by_rule[rid]
    return out


def _bucket_n(buckets: dict[str, dict[str, int]], key: str) -> int:
    return sum(buckets.get(key, {}).values())


def _print_buckets(buckets: dict[str, dict[str, int]]) -> None:
    """四桶只读盘点（人可复核：桶 → 规则(条数)）。"""
    print("[golden] warn 四桶："
          + " · ".join(f"{c} {_bucket_n(buckets, c)}" for c in CLASSES)
          + f" · 未分类 {_bucket_n(buckets, UNCLASSIFIED)}")
    for key in (*CLASSES, UNCLASSIFIED):
        rows = buckets.get(key) or {}
        if rows:
            detail = "、".join(f"{rid}({n})" for rid, n in sorted(rows.items()))
            print(f"  {key}: {detail}")


# ── 568 任务 2（T2a 侦察后）：复用 replay 已落盘的增量结论，不再整权重放真编译 ────────
# 病：`measure()` 逐卡直调 `replay.replay_card()`，而 replay 的 CLI 有 498 增量 manifest
# （指纹 = sha256(卡 ‖ 夹具 ‖ 工件)，未变且上次 confirm ⇒ skip）⇒ golden 把 replay 刚做过的
# 真编译**整权重放**（560 实测：replay 126.9s + golden 131s，纯重复）。
# 治：把"该跑 / 该复用"的判定**原样交给 replay 自己的纯函数** `select_incremental`——
#   不自造规则、不看时间戳：只有"内容指纹一致且上次 verdict 就是 confirm"才复用；
#   其余（无记录 / 指纹变了 / 上次非 confirm / 指纹 MISSING / manifest 缺失或损坏）**一律真编译**。
# 独立性边界（诚实声明，见 _worklog_568.md）：复用后 golden 对**未变内容**不再独立重编译，
#   这与 498 给 replay CLI 的既有语义一致；输入一变指纹就变 ⇒ 必然回到真编译。
#   要审计/对照时用 `golden_lock.py check --no-reuse` 强制逐卡真编译（两态三数逐字一致，有回归锁）。
REUSE_REPLAY_MANIFEST = True


def _select_replay(cards: list[Any], replay_mod: Any) -> tuple[list[Any], list[Any]]:
    """返回 (真编译列表, 复用列表)。任何"拿不准"都回退真编译（fail-closed）。"""
    if not REUSE_REPLAY_MANIFEST:
        return list(cards), []
    try:
        manifest = replay_mod.load_manifest()   # 用 replay 自己的读法（缺失/损坏 ⇒ {} ⇒ 全量）
    except Exception:                      # noqa: BLE001 读不动 ⇒ 全量真编译
        return list(cards), []
    if not manifest:
        return list(cards), []
    return replay_mod.select_incremental(list(cards), manifest)


def measure(findings: Sequence[Any] | None = None) -> dict[str, int]:
    """全部指标现场复算（不读任何手工数字）。

    `findings` 可由调用方传入（避免 `check` 里为了分桶把 gate 跑第二遍）。
    """
    import atom_evidence_replay as replay
    import gate_engine as ge

    if findings is None:
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
    to_run, reused = _select_replay(evids, replay)      # 568 任务 2：能复用就不重编译
    if reused:
        import sys as _sys
        print(f"[golden] 复用 replay 增量结论 {len(reused)}/{len(evids)} 卡"
              f"（指纹未变且上次 confirm）；其余 {len(to_run)} 卡真编译", file=_sys.stderr)
    for p in to_run:
        verdict, _ = replay.replay_card(p, do_sanitizer=False)
        if verdict == "confirm":
            confirm += 1
        elif verdict.startswith("infra_error:"):
            infra += 1
    confirm += len(reused)      # 复用项按定义**只能是** confirm（select_incremental 的规则）

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


def cmd_sync(json_flag: bool = False) -> int:
    real_out = sys.stdout
    if json_flag:
        sys.stdout = sys.stderr
    state = _load()
    commit, dirty = _git_provenance()
    state.update({"schema": SCHEMA, "updated": _dt.date.today().isoformat(),
                  "commit": commit, "dirty": dirty, "metrics": measure()})
    _save(state)
    print(f"[golden] 快照已固化：{state['metrics']}"
          f"（commit={commit or '?'} dirty={dirty}）")
    if json_flag:
        real_out.write(json.dumps({
            "tool": "golden_lock", "version": "v6.1",
            "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
            "status": "pass", "summary": dict(state["metrics"]),
            "findings": [], "infra_errors": [], "accepted": False,
        }, ensure_ascii=False, indent=1) + "\n")
    return 0


def cmd_check(accept: str | None, classify: str | None = None,
              json_flag: bool = False) -> int:
    real_out = sys.stdout
    if json_flag:
        sys.stdout = sys.stderr
    # 停止"整体 accept"（530 任务5）：先验分类，再谈接受——不合规就别浪费一次全量测量。
    if accept and not classify:
        print("[golden] ✗ --accept 必须同时给 --classify（已停止整体 accept）：\n"
              "        --classify 规则ID=real|false_positive|legacy|accepted[,...]\n"
              "        四桶：real=真债须修内容 / false_positive=规则过宽须修规则 / "
              "legacy=口径迁移期名单 / accepted=明确认可的长期现状")
        return 2
    cls_map: dict[str, str] = {}
    if classify:
        try:
            cls_map = _parse_classify(classify)
        except ValueError as exc:
            print(f"[golden] ✗ --classify 非法：{exc}")
            return 2
    state = _load()
    base = state.get("metrics") or {}
    if not base:
        print("[golden] 无基线——先跑 `sync` 固化当前达标状态")
        if json_flag:
            real_out.write(json.dumps({
                "tool": "golden_lock", "version": "v6.1",
                "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
                "status": "fail", "summary": {}, "findings": [],
                "infra_errors": [], "accepted": False,
            }, ensure_ascii=False, indent=1) + "\n")
        return 2
    import gate_engine as ge

    findings = ge.run(include_advice=False)   # 只跑一次：测指标与分桶共用同一批命中
    now = measure(findings)
    buckets = warn_buckets(findings)
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
    _print_buckets(buckets)   # 530 任务5：warn 归属四桶（只读、可与 accept 的 classify 对账）

    def _emit(status: str, accepted: bool) -> None:
        findings = [{"rule": "golden_lock", "severity": "block",
                     "file": w.split(":")[0], "message": w} for w in worse]
        summary = dict(now)
        summary.update({f"warn_{c}": _bucket_n(buckets, c) for c in CLASSES})
        summary[f"warn_{UNCLASSIFIED}"] = _bucket_n(buckets, UNCLASSIFIED)
        real_out.write(json.dumps({
            "tool": "golden_lock", "version": "v6.1",
            "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
            "status": status, "summary": summary, "findings": findings,
            "infra_errors": [], "accepted": accepted,
        }, ensure_ascii=False, indent=1) + "\n")

    if worse:
        if accept:
            commit, dirty = _git_provenance()
            state.setdefault("accepted", []).append(
                {"ts": _dt.datetime.now().isoformat(timespec="seconds"),
                 "reason": accept,
                 "classify": dict(cls_map),  # 逐规则分类（530 任务5：停止整体 accept）
                 "worse": worse,            # 机器自动生成：与当期测量同源（非人手输）
                 "metrics_after": now,      # 机器勾稽：接受后的基线快照，可与 metrics 对账
                 "commit": commit, "dirty": dirty})
            # 分类表随接受合并进快照：下轮 `check`/`buckets` 才能按桶复算同一批 warn
            cmap = state.get("warn_classify")
            merged = dict(cmap) if isinstance(cmap, dict) else {}
            merged.update(cls_map)
            state["warn_classify"] = merged
            # 接受即同步基线：否则"接受了但基线仍旧"，下一轮 check 重复报同一条恶化
            state["metrics"] = now
            state["updated"] = _dt.date.today().isoformat()
            state["commit"] = commit
            state["dirty"] = dirty
            _save(state)
            print(f"[golden] 已显式接受并留痕（{len(state['accepted'])} 条审计记录）；"
                  f"分类 {cls_map}；"
                  f"基线已同步至当期测量（commit={commit or '?'} dirty={dirty}）")
            if json_flag:
                _emit("fail", True)
            return 0
        print("[golden] ✗ 指标恶化——修复，或 "
              "`check --accept \"理由\" --classify \"RID=real,...\"` 显式留痕")
        if json_flag:
            _emit("fail", False)
        return 1
    if improved:
        print("[golden] 有改善：跑 `sync` 更新基线（把进步锁进黄金快照）")
    print("[golden] ✅ 无恶化")
    if json_flag:
        _emit("pass", False)
    return 0


def cmd_buckets(json_flag: bool = False) -> int:
    """四桶只读盘点（530 任务5）：warn 归属 real/false_positive/legacy/accepted + 未分类。

    永远 exit 0——这是**盘点**不是门禁（门禁仍是 `check`）。`--json` 时四桶以
    `warn_<桶>` 形式进 summary，明细进 findings。
    """
    real_out = sys.stdout
    if json_flag:
        sys.stdout = sys.stderr
    buckets = warn_buckets()
    _print_buckets(buckets)
    n_un = _bucket_n(buckets, UNCLASSIFIED)
    if n_un:
        print("[golden] ⚠ 未分类 warn 不计入任何桶——分类是**人审**动作（agent 不得代签），"
              "`check --accept` 时逐规则给 --classify")
    if json_flag:
        summary = {f"warn_{c}": _bucket_n(buckets, c) for c in CLASSES}
        summary[f"warn_{UNCLASSIFIED}"] = n_un
        findings = [{"rule": rid, "severity": cls, "file": "",
                     "message": f"{rid}: {n} 条 warn → {cls}"}
                    for cls in (*CLASSES, UNCLASSIFIED)
                    for rid, n in sorted((buckets.get(cls) or {}).items())]
        real_out.write(json.dumps({
            "tool": "golden_lock", "version": "v6.1",
            "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
            "status": "pass", "summary": summary, "findings": findings,
            "infra_errors": [], "accepted": False,
        }, ensure_ascii=False, indent=1) + "\n")
    return 0



def cmd_show() -> int:
    state = _load()
    print(json.dumps(state, ensure_ascii=False, indent=1))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="S4 黄金非回归锁")
    sub = ap.add_subparsers(dest="cmd", required=True)
    _pj = argparse.ArgumentParser(add_help=False)
    _pj.add_argument("--json", nargs="?", const=True, default=False,
                     help="结构化 JSON 输出到 stdout")
    _pj.add_argument("--no-reuse", action="store_true",
                     help="568：不复用 replay 增量 manifest，强制逐卡真编译（审计/对照用）")
    sub.add_parser("sync", parents=[_pj], help="固化当前状态为快照").set_defaults(
        fn=lambda a: cmd_sync(getattr(a, "json", False)))
    p_ck = sub.add_parser("check", parents=[_pj], help="比对快照，恶化即 exit 1")
    p_ck.add_argument("--accept", help="显式接受恶化（必须给理由；且必须同时给 --classify）")
    p_ck.add_argument("--classify",
                      help="强制逐规则分类：规则ID=real|false_positive|legacy|accepted[,...]"
                           "（无分类拒绝 accept，530 任务5）")
    p_ck.set_defaults(
        fn=lambda a: cmd_check(a.accept, a.classify, getattr(a, "json", False)))
    sub.add_parser("buckets", parents=[_pj],
                   help="四桶只读盘点 warn 归属（real/false_positive/legacy/accepted）"
                   ).set_defaults(fn=lambda a: cmd_buckets(getattr(a, "json", False)))
    sub.add_parser("show", parents=[_pj], help="查看快照").set_defaults(fn=lambda _a: cmd_show())
    a = ap.parse_args(argv)
    if getattr(a, "no_reuse", False):           # 568 任务 2：审计/对照开关（全局，一次一进程）
        global REUSE_REPLAY_MANIFEST
        REUSE_REPLAY_MANIFEST = False
    return int(a.fn(a))


if __name__ == "__main__":
    raise SystemExit(main())
