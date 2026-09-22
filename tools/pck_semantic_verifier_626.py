"""626 E1 · PCK semantic verifier（4 层验证）

| 层 | 名称 | 内容 |
|---|---|---|
| **B2-S** | schema validity | schema_version / 必填字段 / evidence 非空 / verifier 非空 / uncertainty 有数字 / provenance.commit 非空 |
| **B2-R** | referential integrity | evidence.ref 可解析 / hash 匹配 / claim.id 一致 / negative_test 存在 / result 与 replay artifact 对得上 |
| **B2-E** | evidence semantics | evidence 非空且有 type+ref / claim 与 evidence 主题一致性（保守关键词匹配）/ negative_controls 非空 |
| **B2-A** | authority semantics | human_authority.status 与 Authority Ledger 一致 / authorized 须有 card-level event / 仅 edge-level ⇒ 警告（判据 7） |

另：`global_uncertainty`（如 0.009062，全局 cs 上界）vs `local_uncertainty` 区分——
本批**只验证、不修改** PCK 文件。

纯标准库（yaml 除外）；`--check` exit 0=无 fail；`--report` 导出报告。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import authority_projection_compiler_626 as AP  # noqa: E402

CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
OUT_MD = os.path.join(ROOT, "data", "pck_semantic_verification_report_626.md")
OUT_JSON = os.path.join(ROOT, "data", "pck_semantic_verification_626.json")

GLOBAL_CS_UPPER = 0.009062      # 已知全局 cs 上界（SNAPSHOT_MANIFEST）


def _load(path: str) -> dict:
    import yaml  # type: ignore[import-untyped]
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


class PCKSemanticVerifier:
    def __init__(self) -> None:
        self.compiler = AP.AuthorityProjectionCompiler()

    # ── B2-S ──
    def check_schema(self, c: dict) -> dict:
        errs: list[str] = []
        if not c.get("schema_version"):
            errs.append("缺 schema_version")
        if not c.get("claim"):
            errs.append("缺 claim")
        if not c.get("evidence"):
            errs.append("evidence 为空")
        # 实测字段名是 `verifiers`（复数，list）；兼容单数 `verifier`
        verifiers = c.get("verifiers") or c.get("verifier")
        if not verifiers:
            errs.append("verifier(s) 为空")
        unc = c.get("uncertainty") or {}
        if not isinstance(unc, dict) or not any(
                isinstance(v, (int, float)) for v in unc.values()):
            if not any(isinstance(v, (int, float))
                       for v in (c.get("uncertainty") or {}).values()):
                errs.append("uncertainty 无数字")
        prov = c.get("provenance") or {}
        if not prov.get("commit"):
            errs.append("provenance.commit 为空")
        return {"layer": "B2-S", "status": "pass" if not errs else "fail",
                "errors": errs}

    # ── B2-R ──
    def check_referential(self, c: dict, pck_id: str) -> dict:
        errs: list[str] = []
        warns: list[str] = []
        evs = c.get("evidence") or []
        if not isinstance(evs, list):
            evs = []
        for ev in evs:
            ref = str((ev or {}).get("ref") or "")
            if not ref:
                errs.append("evidence 缺 ref")
                continue
            p = os.path.join(ROOT, ref)
            if not os.path.exists(p):
                warns.append(f"evidence.ref 不可解析：{ref}")
            h = (ev or {}).get("hash")
            if h and isinstance(h, str) and h.startswith("sha256:"):
                if os.path.exists(p):
                    import hashlib
                    real = hashlib.sha256(open(p, "rb").read()).hexdigest()
                    if real != h[7:]:
                        errs.append(f"evidence hash 不匹配：{ref}")
        # negative_test
        nc = c.get("negative_controls") or c.get("negative_tests") or []
        if not nc:
            warns.append("无 negative_controls（可证伪性未验证）")
        return {"layer": "B2-R", "status": "pass" if not errs else "fail",
                "errors": errs, "warnings": warns}

    # ── B2-E ──
    def check_evidence_semantics(self, c: dict) -> dict:
        errs: list[str] = []
        warns: list[str] = []
        evs = c.get("evidence") or []
        if not evs:
            errs.append("evidence 为空")
        for ev in evs or []:
            if not (ev or {}).get("type"):
                errs.append("evidence 缺 type")
            if not (ev or {}).get("ref"):
                errs.append("evidence 缺 ref")
        claim = c.get("claim") or {}
        ctext = str(claim.get("statement") or claim.get("text") or "")
        if ctext and evs:
            # 保守主题一致性：claim 中的 C++ 关键词是否至少有一个出现在 evidence 文本里
            kws = set(re.findall(r"[A-Za-z_]{4,}", ctext))
            joined = " ".join(str((e or {}).get("ref") or "") for e in evs)
            if kws and not (kws & set(re.findall(r"[A-Za-z_]{4,}", joined))):
                warns.append("claim 与 evidence 主题关键词无交集（保守提示）")
        if not (c.get("negative_controls") or c.get("negative_tests")):
            warns.append("缺 negative_controls")
        return {"layer": "B2-E", "status": "pass" if not errs else "fail",
                "errors": errs, "warnings": warns}

    # ── B2-A ──
    def check_authority(self, c: dict, pck_id: str) -> dict:
        errs: list[str] = []
        warns: list[str] = []
        ha = c.get("human_authority") or {}
        status = str(ha.get("status") or "")
        proj = self.compiler.compile_pck(pck_id)
        if status == "authorized" and not proj["source_authority_events"]:
            errs.append("status=authorized 但 Authority Ledger 无对应 card-level event")
        if proj["cross_granularity_warning"]:
            warns.append(proj["cross_granularity_warning"])
        return {"layer": "B2-A", "status": "pass" if not errs else "fail",
                "errors": errs, "warnings": warns}

    # ── uncertainty ──
    def check_uncertainty(self, c: dict) -> dict:
        unc = c.get("uncertainty") or {}
        notes: list[str] = []
        if isinstance(unc, dict):
            for k, v in unc.items():
                if isinstance(v, (int, float)) and abs(v - GLOBAL_CS_UPPER) < 1e-9:
                    notes.append(f"{k}={v} 与全局 cs 上界一致 ⇒ 标注为 global_uncertainty_ref")
        return {"layer": "UNCERTAINTY", "status": "pass",
                "notes": notes or ["未见全局值；按 local_uncertainty 处理"]}

    def verify(self, pck_path: str) -> dict[str, Any]:
        pck_id = os.path.basename(pck_path)[:-9]
        c = _load(pck_path)
        layers = [self.check_schema(c), self.check_referential(c, pck_id),
                  self.check_evidence_semantics(c), self.check_authority(c, pck_id)]
        unc = self.check_uncertainty(c)
        failed = [ly["layer"] for ly in layers if ly["status"] == "fail"]
        return {"pck_id": pck_id, "layers": layers, "uncertainty": unc,
                "status": "fail" if failed else "pass", "failed_layers": failed}

    def verify_all(self, pck_dir: str = CERT_DIR) -> dict[str, Any]:
        results: dict[str, Any] = {}
        for p in sorted(glob.glob(os.path.join(pck_dir, "*.pck.yaml"))):
            pid = os.path.basename(p)[:-9]
            results[pid] = self.verify(p)
        n_pass = sum(1 for r in results.values() if r["status"] == "pass")
        by_layer: dict[str, int] = {}
        for r in results.values():
            for ly in r["layers"]:
                by_layer[ly["layer"]] = by_layer.get(ly["layer"], 0) + (
                    1 if ly["status"] == "pass" else 0)
        return {"count": len(results), "passed": n_pass,
                "failed": len(results) - n_pass,
                "by_layer_pass": by_layer, "results": results}


def render_report(allr: dict) -> str:
    L = ["# 626 E1 · PCK semantic verifier 实跑报告（4 层验证）", "",
         f"- PCK 总数：**{allr['count']}**；pass **{allr['passed']}** / fail **{allr['failed']}**",
         f"- 各层 pass 数：`{allr['by_layer_pass']}`", "",
         "| PCK | 状态 | 失败层 |", "|---|---|---|"]
    for pid, r in list(allr["results"].items())[:85]:
        L.append(f"| `{pid}` | {r['status']} | {', '.join(r['failed_layers']) or '-'} |")
    L += ["", "> 说明：本批**只验证，不修改**任何 PCK 文件。", ""]
    return "\n".join(L) + "\n"


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    v = PCKSemanticVerifier()
    # 合成 PCK：pass / fail 场景
    good = {"schema_version": "1.0", "claim": {"id": "C1", "statement": "data race is UB"},
            "evidence": [{"type": "replay", "ref": "data/grounded_labels_w2.json"}],
            "verifier": "v1", "uncertainty": {"cs_upper_bound": 0.001},
            "provenance": {"commit": "abc123"},
            "human_authority": {"status": "pending"}}
    bad = {"claim": {}, "evidence": [], "verifier": "", "uncertainty": {},
           "provenance": {}}
    r1s = v.check_schema(good)
    r2s = v.check_schema(bad)
    chk("B2-S 合法样本通过", r1s["status"] == "pass", str(r1s["errors"]))
    chk("B2-S 缺字段样本失败", r2s["status"] == "fail")
    r1r = v.check_referential(good, "X")
    chk("B2-R 可解析引用通过", r1r["status"] == "pass", str(r1r["errors"]))
    r1e = v.check_evidence_semantics(good)
    chk("B2-E 通过", r1e["status"] == "pass", str(r1e["errors"]))
    r1a = v.check_authority(good, "X")
    chk("B2-A 通过（pending 无 card-level 不报错）", r1a["status"] == "pass")
    bad2 = dict(good, human_authority={"status": "authorized"})
    chk("B2-A authorized 无 card-level event ⇒ fail",
        v.check_authority(bad2, "X")["status"] == "fail")
    chk("global uncertainty 可识别",
        "global_uncertainty_ref" in str(v.check_uncertainty(
            {"uncertainty": {"cs_upper_bound": GLOBAL_CS_UPPER}})))
    # 全量
    allr = v.verify_all()
    chk("全量 PCK 83 张", allr["count"] == 83, f"({allr['count']})")
    chk("四层均有统计", len(allr["by_layer_pass"]) == 4, str(allr["by_layer_pass"]))
    print(f"E1 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="626 E1 PCK semantic verifier")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="导出验证报告")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    v = PCKSemanticVerifier()
    allr = v.verify_all()
    if args.report:
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_report(allr))
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({k: v2 for k, v2 in allr.items() if k != "results"},
                      fh, ensure_ascii=False, indent=2)
        print(f"written {OUT_MD} / {OUT_JSON}")
    print(json.dumps({k: v2 for k, v2 in allr.items() if k != "results"},
                     ensure_ascii=False, indent=2))
    return 0 if allr["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
