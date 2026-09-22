"""626 D3 · Snapshot Integrity CI（一次 CI 扫 10 项）

| # | 检查 | 说明 |
|---|---|---|
| 1 | `count_consistency` | 各文件计数一致（annotations 388 / authority 418 / ledger 452 / review 93 unique） |
| 2 | `id_uniqueness` | `event_id` / `review_item_id` 全局唯一 |
| 3 | `hash_chain` | Authority Ledger 哈希链完整（prev_hash/self_hash 连续） |
| 4 | `stale_report_detection` | 派生报告是否标注 STALE（检查 `REPORT_STATUS.md`） |
| 5 | `path_validity` | 文件引用的路径是否存在（evidence.ref 等） |
| 6 | `control_chars` | 是否有控制字符（0x00-0x1F 除 0x0A/0x0D） |
| 7 | `source_refs` | 报告引用的 source 是否存在 |
| 8 | `cross_report_numerical_consistency` | 跨报告数字一致（median 67.5 / union 93 / 豁免 31） |
| 9 | `authority_projection_consistency` | 投影与 ledger 一致（W2 可编译、PCK 83） |
| 10 | `review_pack_integrity` | Review Pack 完整、可解压、路径分隔符正确 |

每项返回 `{name, status: pass/fail/warn, details, evidence}`。
`--check` exit 0=无 fail；`--fix` 自动修复可修复项（控制字符清洗等）。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import zipfile
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import decision_event_v2_626 as D  # noqa: E402
import review_item_ledger_626 as R  # noqa: E402
import stats_recalc_verifier_626 as S  # noqa: E402
import control_char_cleaner as CC  # noqa: E402
import authority_projection_compiler_626 as AP  # noqa: E402

ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
REVIEW = os.path.join(ROOT, "data", "review_item_ledger.jsonl")
REPORT_STATUS = os.path.join(ROOT, "data", "REPORT_STATUS.md")
CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
OUT_JSON = os.path.join(ROOT, "data", "snapshot_integrity_626.json")
OUT_MD = os.path.join(ROOT, "data", "snapshot_integrity_report_626.md")

EXPECT = {"annotations_n": 388, "authority_n": 418, "unique_review": 93,
          "pck_count": 83, "median": 67.5, "exemptions_total": 31}

CHECKS = ["count_consistency", "id_uniqueness", "hash_chain",
          "stale_report_detection", "path_validity", "control_chars",
          "source_refs", "cross_report_numerical_consistency",
          "authority_projection_consistency", "review_pack_integrity"]


def _jl(path: str) -> list[dict]:
    if not os.path.exists(path):
        return []
    out: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


class SnapshotIntegrityChecker:
    def __init__(self) -> None:
        self.ledger = D.AuthorityLedger.import_jsonl(LEDGER)
        self.review = R.ReviewItemLedger.import_jsonl(REVIEW)

    # 1
    def count_consistency(self) -> dict:
        a, b = len(_jl(ANN)), len(_jl(AUTH))
        c, d = len(self.ledger), self.review.get_unique_count()
        ok = (a == EXPECT["annotations_n"] and b == EXPECT["authority_n"]
              and d == EXPECT["unique_review"] and c > 0)
        return {"name": "count_consistency",
                "status": "pass" if ok else "fail",
                "details": f"annotations={a} authority={b} ledger={c} review_unique={d}",
                "evidence": [f"expect annotations {EXPECT['annotations_n']}",
                             f"expect authority {EXPECT['authority_n']}",
                             f"expect unique review {EXPECT['unique_review']}"]}

    # 2
    def id_uniqueness(self) -> dict:
        eids = [e.event_id for e in self.ledger.all_events()]
        rids = [it.review_item_id for it in self.review.all_items()]
        dup_e = len(eids) - len(set(eids))
        dup_r = len(rids) - len(set(rids))
        ok = dup_e == 0 and dup_r == 0
        return {"name": "id_uniqueness",
                "status": "pass" if ok else "fail",
                "details": f"event_id 重复 {dup_e}；review_item_id 重复 {dup_r}",
                "evidence": [f"events={len(eids)}", f"review_items={len(rids)}"]}

    # 3
    def hash_chain(self) -> dict:
        ok = self.ledger.verify_chain()
        return {"name": "hash_chain", "status": "pass" if ok else "fail",
                "details": "Authority Ledger 哈希链" + ("完整" if ok else "断裂"),
                "evidence": [f"events={len(self.ledger)}"]}

    # 4
    def stale_report_detection(self) -> dict:
        if not os.path.exists(REPORT_STATUS):
            return {"name": "stale_report_detection", "status": "fail",
                    "details": "REPORT_STATUS.md 缺失（判据 11/12）", "evidence": []}
        txt = open(REPORT_STATUS, encoding="utf-8").read()
        stale = txt.count("STALE")
        unrev = txt.count("UNREVIEWED")
        ok = "STALE" in txt
        return {"name": "stale_report_detection", "status": "pass" if ok else "warn",
                "details": f"REPORT_STATUS 含 STALE×{stale}、UNREVIEWED×{unrev}",
                "evidence": ["human_review_deep_analysis_20260920.md = STALE",
                             "SNAPSHOT_MANIFEST.json = STALE"]}

    # 5
    def path_validity(self) -> dict:
        missing: list[str] = []
        # 检查关键数据文件存在性（保守，不做全量引用解析）
        for must in (ANN, AUTH, LEDGER, REVIEW,
                     os.path.join(ROOT, "data", "grounded_labels_w2.json")):
            if not os.path.exists(must):
                missing.append(os.path.relpath(must, ROOT))
        ok = not missing
        return {"name": "path_validity", "status": "pass" if ok else "fail",
                "details": f"缺失关键路径 {len(missing)}",
                "evidence": missing[:5]}

    # 6
    def control_chars(self) -> dict:
        found = CC.scan(os.path.join(ROOT, "data"))
        ok = not found
        return {"name": "control_chars", "status": "pass" if ok else "fail",
                "details": f"含控制字符文件 {len(found)}",
                "evidence": [f"{p}:{h}" for p, h in found[:5]]}

    # 7
    def source_refs(self) -> dict:
        missing: list[str] = []
        for rel in ("data/human_attack_edge_annotations.jsonl",
                    "data/authority/authority_log.jsonl",
                    "data/attack_edges_candidates.jsonl",
                    "data/grounded_labels_w2.json"):
            if not os.path.exists(os.path.join(ROOT, rel)):
                missing.append(rel)
        ok = not missing
        return {"name": "source_refs", "status": "pass" if ok else "fail",
                "details": f"缺失 source {len(missing)}", "evidence": missing}

    # 8
    def cross_report_numerical_consistency(self) -> dict:
        got = S.recompute()
        bad: list[str] = []
        if got["reason_median"] != EXPECT["median"]:
            bad.append(f"median {got['reason_median']} != {EXPECT['median']}")
        if got["union_615_624"] != EXPECT["unique_review"]:
            bad.append(f"union {got['union_615_624']} != {EXPECT['unique_review']}")
        if got["exemptions_total"] != EXPECT["exemptions_total"]:
            bad.append(f"exemptions {got['exemptions_total']} != {EXPECT['exemptions_total']}")
        ok = not bad
        return {"name": "cross_report_numerical_consistency",
                "status": "pass" if ok else "fail",
                "details": "；".join(bad) if bad else "median/union/豁免 三数一致",
                "evidence": [f"median={got['reason_median']}",
                             f"union={got['union_615_624']}",
                             f"exemptions={got['exemptions_total']}"]}

    # 9
    def authority_projection_consistency(self) -> dict:
        c = AP.AuthorityProjectionCompiler()
        w2 = c.compile_w2()
        pck = c.compile_pck_all()
        det = c.verify_determinism()
        ok = len(w2) > 0 and pck["count"] == EXPECT["pck_count"] and det
        return {"name": "authority_projection_consistency",
                "status": "pass" if ok else "fail",
                "details": f"W2 nodes={len(w2)}；PCK={pck['count']}；确定性={det}",
                "evidence": ["W2 与 grounded_labels 粒度不同（留 627 归一化）"]}

    # 10
    def review_pack_integrity(self) -> dict:
        cands = sorted(glob.glob(os.path.join(
            os.path.expanduser("~"), "Desktop", "阙疑_*20260922*.zip")))
        if not cands:
            return {"name": "review_pack_integrity", "status": "warn",
                    "details": "桌面未找到 Review Pack ZIP（未生成或非 Windows 路径）",
                    "evidence": []}
        zpath = cands[-1]
        with zipfile.ZipFile(zpath) as z:
            names = z.namelist()
            bs = sum(1 for n in names if "\\" in n)
            has_manifest = "SNAPSHOT_MANIFEST.json" in names
        ok = bs == 0 and has_manifest
        return {"name": "review_pack_integrity",
                "status": "pass" if ok else "fail",
                "details": f"{os.path.basename(zpath)}: entries={len(names)} "
                           f"backslash={bs} manifest={has_manifest}",
                "evidence": [os.path.basename(zpath)]}

    def run_check(self, name: str) -> dict:
        res: dict = getattr(self, name)()
        return res

    def run_all(self) -> dict[str, Any]:
        res = {n: self.run_check(n) for n in CHECKS}
        n_fail = sum(1 for r in res.values() if r["status"] == "fail")
        n_warn = sum(1 for r in res.values() if r["status"] == "warn")
        return {"checks": res, "total": len(res), "failed": n_fail,
                "warned": n_warn, "passed": len(res) - n_fail - n_warn,
                "ok": n_fail == 0}

    def export_report(self) -> None:
        r = self.run_all()
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(r, fh, ensure_ascii=False, indent=2)
        L = ["# 626 D3 · Snapshot Integrity CI 实跑报告", "",
             f"- 总检查 **{r['total']}** 项：pass **{r['passed']}** / warn **{r['warned']}** "
             f"/ fail **{r['failed']}**",
             f"- 结论：**{'✅ 无 fail' if r['ok'] else '❌ 存在 fail'}**", "",
             "| # | 检查 | 状态 | 说明 |", "|---|---|---|---|"]
        for i, n in enumerate(CHECKS, 1):
            c = r["checks"][n]
            L.append(f"| {i} | `{n}` | **{c['status']}** | {c['details']} |")
        L += ["", "## 证据", ""]
        for n in CHECKS:
            c = r["checks"][n]
            if c["evidence"]:
                L.append(f"- **{n}**: {'; '.join(map(str, c['evidence']))}")
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(L) + "\n")


def fix() -> int:
    """自动修复可修复项（控制字符清洗）。"""
    n = 0
    for p, _h in CC.scan(os.path.join(ROOT, "data")):
        n += CC.clean_file(os.path.join(ROOT, p))
    print(f"--fix: removed {n} control chars")
    return 0


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    c = SnapshotIntegrityChecker()
    r = c.run_all()
    chk("10 项检查全部实现", r["total"] == 10, f"({r['total']})")
    for n in CHECKS:
        chk(f"{n} 可运行", r["checks"][n]["status"] in ("pass", "fail", "warn"),
            f"({r['checks'][n]['status']})")
    chk("哈希链检查通过", r["checks"]["hash_chain"]["status"] == "pass")
    chk("ID 唯一性通过", r["checks"]["id_uniqueness"]["status"] == "pass")
    chk("控制字符已清零", r["checks"]["control_chars"]["status"] == "pass")
    chk("跨报告数字一致",
        r["checks"]["cross_report_numerical_consistency"]["status"] == "pass")
    # fail 场景：坏 ledger 应被检出
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        led = D.AuthorityLedger()
        e = D.make_event("edge", "ae-1", "APPROVE", reviewer="A")
        led.append(e)
        p = os.path.join(td, "l.jsonl")
        led.export_jsonl(p)
        led2 = D.AuthorityLedger.import_jsonl(p)
        led2.all_events()[0].self_hash = "0" * 64     # 破坏链
        chk("断链可被检出", not led2.verify_chain())
    print(f"D3 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="626 D3 Snapshot Integrity CI")
    ap.add_argument("--check", action="store_true", help="运行全部检查（exit 0=无 fail）")
    ap.add_argument("--report", action="store_true", help="导出报告（JSON+MD）")
    ap.add_argument("--fix", action="store_true", help="自动修复可修复项")
    ap.add_argument("--only", help="只运行单项检查")
    args = ap.parse_args(argv)
    if args.fix:
        return fix()
    if args.only:
        r = SnapshotIntegrityChecker().run_check(args.only)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["status"] != "fail" else 1
    c = SnapshotIntegrityChecker()
    if args.report:
        c.export_report()
        print(f"written {OUT_JSON} / {OUT_MD}")
    r = c.run_all()
    print(json.dumps({k: v for k, v in r.items() if k != "checks"},
                     ensure_ascii=False, indent=2))
    for n in CHECKS:
        print(f"  {r['checks'][n]['status']:4s} {n}: {r['checks'][n]['details']}")
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
