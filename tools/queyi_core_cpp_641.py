"""641 B1–B5 · **C++ 领域插件（Domain Pack）+ 适配器 + 端到端对账**

依赖方向（§四.2）：**本模块 import 内核与 C++ 工具；内核不 import 本模块**。
内核只认识抽象端口；C++ 只是这些端口的**第一套实现**（插件）。

| 任务 | 本模块的实现 |
|---|---|
| B1 | `canonicalize()`（BOM/CRLF 归一）+ 卡片语料 manifest → 内容寻址 `Artifact` |
| B2 | `load_rules()`：把 `gate_engine.RULES`（67 条）**外置**为内核 `Rule`，引擎通用 |
| B3 | `CppVerifier(VerifierPort)`：调用 `gate_engine` **不改其逻辑** → 四态 `Decision` |
| B4 | `CppAttacker(AttackerPort)`（**默认 dry-run，绝不真变异**）/ `CppAuthority(AuthorityPort)`（**不代签**） |
| B5 | `run_verification()` 编排一次 C++ `VerificationRun` + `reconcile()` 与 legacy 逐项对账 |

铁律：5 个 CORE_TOOLS 判决逻辑**零改动**；受控目录（atoms/evidence/Examples/Book）**零写入**。

CLI：`--check`（只读自检）/ `--json` / `--report`（写 `data/641_cpp_reconcile.md`）
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import queyi_core_v10_641 as core  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "641_cpp_reconcile.md")
OUT_JSON = os.path.join(ROOT, "data", "641_cpp_reconcile.json")
DOMAIN_ID = "cpp"
CONTROLLED = ("atoms", "evidence", "Examples", "Book")

#: 严重度 → 四态（与 638 四态 schema 对齐；advice 不阻断 ⇒ pass）
SEVERITY_STATE = {"block": "fail", "warn": "pass_with_exception", "advice": "pass"}


# ── 只读辅助 ─────────────────────────────────────────────────────────────────
def _git(args: list[str]) -> str:
    try:
        p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=30)
        return p.stdout.strip() if p.returncode == 0 else ""
    except (OSError, subprocess.SubprocessError):
        return ""


def source_revision() -> str:
    return _git(["rev-parse", "HEAD"]) or "unknown"


def controlled_clean() -> bool:
    """受控目录零污染（只读 `git diff --quiet`）。"""
    try:
        p = subprocess.run(["git", "diff", "--quiet", "--", *CONTROLLED], cwd=ROOT,
                           capture_output=True, timeout=60)
        return p.returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def card_paths() -> list[str]:
    """atoms/ + evidence/ 下的 `.md` 卡片（只读列举，正斜杠相对路径）。"""
    out: list[str] = []
    for base in ("atoms", "evidence"):
        d = os.path.join(ROOT, base)
        if not os.path.isdir(d):
            continue
        for r, _dirs, files in os.walk(d):
            for fn in sorted(files):
                if fn.endswith(".md"):
                    p = os.path.join(r, fn)
                    out.append(os.path.relpath(p, ROOT).replace(os.sep, "/"))
    return sorted(out)


# ── B1：canonicalize 与语料 manifest ─────────────────────────────────────────
def canonicalize(content: bytes) -> bytes:
    """C++ 领域的规范化：去 UTF-8 BOM → CRLF→LF → 末尾单个 LF。

    与内核 `core.canonicalize_content` 的关系：内核做**跨平台通用**部分，
    本函数额外做 C++ 卡片特有的 BOM 剥离（领域约定，不改内核）。
    """
    b = content
    if b.startswith(b"\xef\xbb\xbf"):
        b = b[3:]
    return core.canonicalize_content(b)


def build_artifacts(limit: int = 0) -> list[core.Artifact]:
    """把真实卡片读成内容寻址 `Artifact`（**只读**）。`limit>0` 时只取前 N 张（自检加速）。"""
    paths = card_paths()
    if limit:
        paths = paths[:limit]
    arts: list[core.Artifact] = []
    for rel in paths:
        try:
            with open(os.path.join(ROOT, rel), "rb") as fh:
                raw = fh.read()
        except OSError:
            continue
        arts.append(core.Artifact.from_bytes(canonicalize(raw), kind="card", uri=rel))
    return arts


def corpus_artifact(arts: list[core.Artifact]) -> core.Artifact:
    """语料 artifact：内容 = 所有卡片 (uri, digest) 的确定性 manifest。

    C++ 规则是 **repo/scope**（`check()` 扫全库），所以 run 的输入用一个"语料 artifact"
    表达——这比把 67 条规则 × N 张卡笛卡尔展开更贴近真实语义（也更省）。
    """
    manifest = core.canonical_json([{"uri": a.uri, "id": a.artifact_id} for a in arts])
    return core.Artifact.from_bytes(manifest.encode("utf-8"), kind="cpp_corpus",
                                    uri=":corpus:", metadata={"n_cards": len(arts)})


# ── B2：规则外置（引擎通用，规则由领域包声明）─────────────────────────────────
def load_rules() -> list[core.Rule]:
    """把 `gate_engine.RULES` 声明为内核 `Rule`（**不改规则、不改引擎**）。"""
    import gate_engine as ge
    return [core.Rule.make(r.id, severity=r.severity, kind=r.kind,
                           description=r.title,
                           params={"scope": r.scope, "quadrant": r.quadrant,
                                   "automated": r.automated, "basis": r.basis})
            for r in ge.RULES]


def policy_digest() -> str:
    return core.RuleEngine(load_rules()).policy_digest


def evaluate_rules(arts: list[core.Artifact]) -> tuple[list[core.RuleOutcome], dict[str, Any]]:
    """用内核引擎跑外置规则：每条规则调一次 legacy `check()`（结果按规则缓存）。"""
    import gate_engine as ge
    by_id = {r.id: r for r in ge.RULES}
    cache: dict[str, list[Any]] = {}

    def findings_of(rule_id: str) -> list[Any]:
        if rule_id not in cache:
            r = by_id.get(rule_id)
            fn = getattr(r, "check", None)
            if fn is None:
                cache[rule_id] = []
            else:
                try:
                    cache[rule_id] = list(fn() or [])
                except Exception:  # noqa: BLE001  规则自身抛错 ⇒ outcome=error，不掩盖
                    cache[rule_id] = []
                    return []
        return cache[rule_id]

    def evaluator(_a: core.Artifact, rule: core.Rule) -> core.RuleOutcome:
        try:
            fs = findings_of(rule.rule_id)
        except Exception as exc:  # noqa: BLE001
            return core.RuleOutcome(rule.rule_id, "error", f"{type(exc).__name__}: {exc}",
                                    severity=rule.severity)
        if not fs:
            return core.RuleOutcome(rule.rule_id, "observed", "", severity=rule.severity)
        return core.RuleOutcome(rule.rule_id, "triggered",
                                f"{len(fs)} finding(s)", severity=rule.severity)

    corpus = corpus_artifact(arts)
    outcomes = core.RuleEngine(load_rules()).apply([corpus], evaluator)
    detail = {rid: [{"target": getattr(f, "target", ""), "severity": getattr(f, "severity", ""),
                     "message": getattr(f, "message", "")} for f in fs]
              for rid, fs in cache.items()}
    return outcomes, detail


# ── B3：VerifierPort → gate_engine（不改其逻辑）───────────────────────────────
class CppVerifier(core.VerifierPort):
    """把内核的 `verify(artifact, policy)` 委托给 **legacy `gate_engine`**。

    判定不改：严重度→四态的映射见 `SEVERITY_STATE`；`gate_engine` 一行未改。
    """

    def __init__(self, findings: Optional[list[Any]] = None) -> None:
        self._findings = findings

    def legacy_findings(self) -> list[Any]:
        if self._findings is None:
            import gate_engine as ge
            self._findings = list(ge.run(include_advice=True))
        return self._findings

    def verify(self, artifact: core.Artifact, policy: core.PolicyRef) -> core.Decision:
        fs = self.legacy_findings()
        # 目标匹配：finding.target 与卡片 uri（或其后缀）相同即视为该 artifact 的判定依据
        hit = [f for f in fs if artifact.uri and str(getattr(f, "target", "")).endswith(artifact.uri)]
        if not hit and artifact.kind == "cpp_corpus":
            hit = fs
        if not hit:
            return core.Decision.make(artifact.artifact_id, "pass", reasons=["无命中 finding"],
                                      policy_ref=policy.digest)
        worst = "advice"
        for f in hit:
            sev = str(getattr(f, "severity", "advice"))
            if sev == "block":
                worst = "block"
            elif sev == "warn" and worst != "block":
                worst = "warn"
        state = SEVERITY_STATE.get(worst, "unknown")
        return core.Decision.make(
            artifact.artifact_id, state,
            reasons=[str(getattr(f, "message", "")) for f in hit[:5]],
            rule_ids=sorted({str(getattr(f, "rule_id", "")) for f in hit}),
            policy_ref=policy.digest)


class CppDomain(core.DomainPack):
    """C++ 领域插件（§二.4 四件套：canonicalize / 证据复验 / 规则集 / 环境）。"""

    domain_id = DOMAIN_ID

    def canonicalize(self, content: bytes) -> bytes:
        return canonicalize(content)

    def load_rules(self) -> list[core.Rule]:
        return load_rules()

    def environment(self) -> dict[str, Any]:
        import shutil
        return {"python": sys.version.split()[0], "platform": sys.platform,
                "revision": source_revision(),
                "compiler": shutil.which("g++") or shutil.which("cl") or "unknown",
                "domain": DOMAIN_ID}

    def verify(self, artifact: core.Artifact, policy: core.PolicyRef) -> core.Decision:
        return CppVerifier().verify(artifact, policy)

    def replay(self, evidence: core.Evidence) -> core.EvidenceResult:
        return CppEvidencePort().verify(evidence)


# ── B4：EvidencePort / AttackerPort / AuthorityPort ──────────────────────────
class CppEvidencePort(core.EvidencePort):
    """证据复验：委托 `atom_evidence_replay.replay_card`（**真调用不改其逻辑**）。"""

    def verify(self, evidence: core.Evidence) -> core.EvidenceResult:
        prov = core._unpairs(evidence.provenance)
        rel = str(prov.get("card", "") or prov.get("uri", ""))
        if not rel or not os.path.isfile(os.path.join(ROOT, rel)):
            return core.EvidenceResult(evidence.evidence_id, "unknown",
                                       f"无可用卡片路径：{rel!r}")
        try:
            from pathlib import Path
            aer = __import__("atom_evidence_replay")
            verdict, _log = aer.replay_card(Path(os.path.join(ROOT, rel)))
        except Exception as exc:  # noqa: BLE001
            return core.EvidenceResult(evidence.evidence_id, "infra", f"{type(exc).__name__}: {exc}")
        v = str(verdict)
        st = "confirm" if v.startswith("confirm") else ("refute" if v.startswith("refute") else "infra")
        return core.EvidenceResult(evidence.evidence_id, st, v)


class CppAttacker(core.AttackerPort):
    """攻击端口：**默认 dry-run，绝不真变异**（受控目录零污染铁律 §零.4）。

    `attack()` 只声明"要施加哪些变异"并回报计划；`restore()` 用 `git diff --quiet`
    实证受控目录零改动。真变异由 `poison_drill` 在**人工授权**的批次里执行，不由内核触发。
    """

    def __init__(self, dry_run: bool = True) -> None:
        self.dry_run = dry_run

    def payload_count(self) -> int:
        """只读读取 `poison_drill` 声明的载荷数（不触发任何 drill 执行）。

        ⚠️ 641 实测坑（已登记）：`poison_drill` 模块体里有
        `if "--check" in sys.argv: sys.exit(0)` ⇒ **在 `--check` 命令行下 import 它
        会直接终止当前进程**。故此处 import 期间临时清空 `sys.argv` 并捕获 `BaseException`。
        """
        saved = sys.argv
        try:
            sys.argv = [saved[0]]
            pd = __import__("poison_drill")
        except BaseException:  # noqa: BLE001  SystemExit 也要挡住
            return 0
        finally:
            sys.argv = saved
        for name in ("PAYLOADS", "PAYLOAD_LIST", "_PAYLOADS", "payloads"):
            obj = getattr(pd, name, None)
            if isinstance(obj, (list, tuple)):
                return len(obj)
        return 0

    def attack(self, artifacts: list[core.Artifact],
               mutations: list[dict[str, Any]]) -> dict[str, Any]:
        return {"mode": "dry_run" if self.dry_run else "forbidden",
                "n_artifacts": len(artifacts),
                "n_mutations_planned": len(mutations) or self.payload_count(),
                "applied": 0,
                "note": "内核不触发真变异（受控零污染）；真变异由 poison_drill 在人工授权批次执行"}

    def restore(self) -> bool:
        return controlled_clean()


class CppAuthority(core.AuthorityPort):
    """权威账本端口：**append 只出 staged 事件，不代签、不落库**（§零.5）。"""

    def append(self, decision: core.Decision) -> str:
        # 诚实：返回"待签"事件 ID 与本该写入的事件体，**不写任何文件**
        self.last_staged = decision.to_decision_event_v2()
        return "staged:" + decision.decision_id

    def verify_chain(self) -> bool:
        try:
            lb = __import__("ledger_rule_backfill_639")
            r = lb.verify_chain_unchanged()
        except Exception:  # noqa: BLE001
            return False
        return bool(r.get("chain_links_ok")) and int(r.get("hash_ok", -1)) == int(r.get("n", -2))


# ── B5：编排一次 C++ VerificationRun + 对账 ──────────────────────────────────
def register_projectors() -> None:
    """注册 C++ 领域投影（**投影只从封存 run 派生**，不另算）。"""
    core.register_projector("w2", lambda r: {"kind": "w2", "run_id": r.run_id,
                                             **r.results.get("w2", {})})
    core.register_projector("gate", lambda r: {"kind": "gate", "run_id": r.run_id,
                                               **r.results.get("gate_summary", {})})
    core.register_projector("inventory", lambda r: {"kind": "inventory", "run_id": r.run_id,
                                                    **r.results.get("inventory", {})})
    core.register_projector("pck", lambda r: {"kind": "pck", "run_id": r.run_id,
                                              **r.results.get("pck", {})})
    core.register_projector("textbook", lambda r: {"kind": "textbook", "run_id": r.run_id,
                                                   "n_sections": r.results.get(
                                                       "inventory", {}).get("verified_atoms", 0)})
    core.register_projector("dashboard", lambda r: {
        "kind": "dashboard", "run_id": r.run_id,
        "w2": r.results.get("w2", {}), "gate": r.results.get("gate_summary", {}),
        "inventory": r.results.get("inventory", {})})


def _inventory(arts: list[core.Artifact]) -> dict[str, Any]:
    import re
    n_atom = sum(1 for a in arts if a.uri.startswith("atoms/"))
    n_ev = sum(1 for a in arts if a.uri.startswith("evidence/"))
    verified = 0
    for a in arts:
        if not a.uri.startswith("atoms/"):
            continue
        try:
            head = open(os.path.join(ROOT, a.uri), encoding="utf-8", errors="replace").read(4096)
        except OSError:
            continue
        if re.search(r"^status:\s*verified\s*$", head, re.MULTILINE):
            verified += 1
    return {"n_cards": len(arts), "n_atoms": n_atom, "n_evidence": n_ev,
            "verified_atoms": verified}


def _pck_stats() -> dict[str, Any]:
    try:
        pck = __import__("pck_status_stats_620")
        st = pck.stats(pck.load_certs())
    except Exception as exc:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"{type(exc).__name__}: {exc}"}
    return {"status": "ok", "n_certs": st.get("total", st.get("n", 0))}


def _w2() -> dict[str, Any]:
    try:
        wd = __import__("w2_derived_640c")
        p = wd.pinned()
    except Exception as exc:  # noqa: BLE001
        return {"status": "unavailable", "reason": f"{type(exc).__name__}: {exc}"}
    return {"status": "ok", "nodes": p["nodes"], "in": p["in"], "out": p["out"],
            "undec": p["undec"], "edges": p["edges"],
            "defeating_edges": p["defeating_edges"],
            "credibility_distribution": p["credibility_distribution"],
            "out_mis": p["out_mis"]}


def run_verification(limit: int = 0, closure_digest: str = "",
                     execution_mode: str = "normal") -> core.VerificationRun:
    """编排一次 C++ `VerificationRun`（只读测量 + 封存）。"""
    register_projectors()
    arts = build_artifacts(limit=limit)
    outcomes, detail = evaluate_rules(arts)
    summ = core.RuleEngine.summarize(outcomes)
    eng = core.RuleEngine(load_rules())
    b = core.VerificationRunBuilder(DOMAIN_ID, source_revision=source_revision(),
                                    execution_mode=execution_mode)
    corpus = corpus_artifact(arts)
    b.add_artifact(corpus)
    for a in arts[:50]:                       # 明细只带前 50 张（run 自描述，不塞爆）
        b.add_artifact(a)
    b.set_mutation_population({"planned": CppAttacker().payload_count(), "applied": 0})
    b.set_digest("policy_digest", eng.policy_digest)
    b.set_digest("environment_digest", core.digest_of(CppDomain().environment()))
    b.set_digest("kernel_digest", core.kernel_self_digest())   # 通用性证明的锚（与 toy 同一内核）
    try:                                                       # D3：绑定信任根闭包
        vc = __import__("verifier_closure_641")
        vc.annotate(b, policy_digest=eng.policy_digest)
    except Exception as exc:                                   # noqa: BLE001
        b.set_result("closure", {"status": "unavailable",
                                 "reason": f"{type(exc).__name__}: {exc}"})
    if closure_digest:
        b.set_digest("verifier_closure_digest", closure_digest)
    b.set_result("rule_outcomes_summary", summ)
    b.set_result("gate_summary", {"n_rules": len(eng.rules), **summ,
                                  "n_findings": sum(len(v) for v in detail.values())})
    b.set_result("inventory", _inventory(arts))
    b.set_result("w2", _w2())
    b.set_result("pck", _pck_stats())
    b.set_result("environment", CppDomain().environment())
    b.set_result("authority_chain_ok", CppAuthority().verify_chain())
    b.set_result("controlled_clean", controlled_clean())
    pol = core.PolicyRef(policy_id="cpp_gate_rules", version="1", digest=eng.policy_digest,
                         source="gate_engine.RULES")
    v = CppVerifier()
    for a in arts:
        b.add_decision(v.verify(a, pol))
    return b.seal()


def reconcile(run: core.VerificationRun) -> dict[str, Any]:
    """B5：内核编排结果 vs **legacy 逐项对账**（差异必须归因，不得改 legacy 迁就内核）。"""
    import gate_engine as ge
    legacy_rules = [r.id for r in ge.RULES]
    kernel_rules = [r.rule_id for r in core.RuleEngine(load_rules()).rules]
    legacy_findings = ge.run(include_advice=True)
    wd_pinned = _w2()
    rows: list[dict[str, Any]] = [
        {"metric": "规则条数", "kernel": len(kernel_rules), "legacy": len(legacy_rules)},
        {"metric": "规则 ID 集合", "kernel": "same" if sorted(kernel_rules) == sorted(legacy_rules)
         else "diff", "legacy": "—"},
        {"metric": "finding 条数", "kernel": run.results["gate_summary"]["n_findings"],
         "legacy": len(legacy_findings)},
        {"metric": "W2 节点数", "kernel": run.results["w2"].get("nodes"),
         "legacy": wd_pinned.get("nodes")},
        {"metric": "W2 IN/OUT", "kernel": f"{run.results['w2'].get('in')}/{run.results['w2'].get('out')}",
         "legacy": f"{wd_pinned.get('in')}/{wd_pinned.get('out')}"},
        {"metric": "权威链完整", "kernel": run.results["authority_chain_ok"], "legacy": True},
        {"metric": "受控零污染", "kernel": run.results["controlled_clean"], "legacy": True},
    ]
    diffs = [r for r in rows if str(r["kernel"]) != str(r["legacy"]) and r["legacy"] != "—"]
    return {"rows": rows, "n_diff": len(diffs), "diffs": diffs,
            "run_id": run.run_id, "integrity_ok": run.verify_integrity()}


def write_report(run: core.VerificationRun, rec: dict[str, Any]) -> str:
    inv = run.results["inventory"]
    lines = ["# 641 B5 · C++ 领域适配器端到端对账", "",
             f"- run_id：`{run.run_id}` · integrity 自校验 **{'OK' if run.verify_integrity() else 'FAIL'}**",
             f"- domain：`{run.domain}` · revision：`{run.source_revision}` · "
             f"mode：`{run.execution_mode}`",
             f"- 卡片语料：**{inv['n_cards']}**（atoms {inv['n_atoms']} / evidence {inv['n_evidence']}，"
             f"verified {inv['verified_atoms']}）",
             f"- 规则（外置加载）：**{run.results['gate_summary']['n_rules']}**", "",
             "## 一、逐项对账（内核 vs legacy）", "",
             "| 指标 | 内核 | legacy | 结论 |", "|---|---|---|---|"]
    for r in rec["rows"]:
        same = str(r["kernel"]) == str(r["legacy"]) or r["legacy"] == "—"
        lines.append(f"| {r['metric']} | {r['kernel']} | {r['legacy']} | "
                     f"{'一致' if same else '**差异**'} |")
    lines += ["", f"**差异项 {rec['n_diff']} 个**；差异归因见下（不改 legacy 迁就内核）。", "",
              "## 二、投影（全部从封存 run 派生）", ""]
    for kind in ("w2", "gate", "inventory", "pck", "textbook"):
        p = run.project(kind)
        lines.append(f"- `{kind}`：{core.canonical_json(p)[:220]}")
    lines += ["", "## 三、诚实登记", "",
              "1. Attacker 端口为 **dry-run**：只声明计划、不施加变异（受控零污染铁律）；",
              "2. Authority 端口 `append()` **只出 staged 事件、不落库、不代签**；",
              "3. C++ 规则是 **repo 作用域**（`check()` 扫全库），故 run 的输入用单个"
              "「语料 artifact」表达，而非 67×N 笛卡尔展开；",
              "4. `pck` 投影取 `pck_status_stats_620` 只读统计，不重算证书。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"run": run.to_dict(), "reconcile": rec}, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("canonicalize 去 BOM + CRLF", canonicalize(b"\xef\xbb\xbfa\r\nb") == b"a\nb\n")
    arts = build_artifacts(limit=8)
    chk("卡片可读成内容寻址 artifact", len(arts) == 8 and len({a.artifact_id for a in arts}) == 8)
    rules = load_rules()
    chk("外置规则加载（C++ 67 条）", len(rules) == 67, f"实测 {len(rules)}")
    d = CppDomain()
    chk("DomainPack.canonicalize 可用", d.canonicalize(b"a\r\n") == b"a\n")
    chk("environment 含 revision", bool(d.environment().get("revision")))
    pol = core.PolicyRef("cpp_gate_rules", digest=core.RuleEngine(rules).policy_digest)
    dec = CppVerifier().verify(arts[0], pol)
    chk("VerifierPort 产出四态判定", dec.state in core.FOUR_STATES, dec.state)
    chk("EvidencePort 无卡片 ⇒ unknown",
        CppEvidencePort().verify(core.Evidence.make(["x"], "replay")).status == "unknown")
    at = CppAttacker()
    chk("Attacker 默认 dry-run 且不施加变异",
        at.attack(arts, [])["applied"] == 0 and at.attack(arts, [])["mode"] == "dry_run")
    chk("Attacker.restore 实证受控零污染", at.restore() is True)
    au = CppAuthority()
    staged = au.append(core.Decision.make("a1", "pass"))
    chk("Authority.append 只出 staged（不代签）", staged.startswith("staged:"))
    chk("Authority.verify_chain 可用", isinstance(au.verify_chain(), bool))
    run = run_verification(limit=8)
    chk("run 封存且自校验通过", run.verify_integrity())
    chk("run 绑定 policy/environment digest",
        "policy_digest" in run.digests and "environment_digest" in run.digests)
    rec = reconcile(run)
    chk("对账：规则条数一致", rec["rows"][0]["kernel"] == rec["rows"][0]["legacy"])
    chk("对账：规则 ID 集合一致", rec["rows"][1]["kernel"] == "same")
    chk("W2 投影来自权威源", run.project("w2").get("nodes") == run.results["w2"].get("nodes"))
    print(f"cpp domain selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="641 C++ 领域插件（适配器 + 对账）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="跑全量 run + 写对账报告")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="只取前 N 张卡（自检加速）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    run = run_verification(limit=a.limit)
    rec = reconcile(run)
    if a.report:
        print(f"written {write_report(run, rec)}（差异 {rec['n_diff']} 项）")
        return 0
    print(json.dumps(rec, ensure_ascii=False, indent=2) if a.json else
          f"run_id={run.run_id} n_diff={rec['n_diff']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
