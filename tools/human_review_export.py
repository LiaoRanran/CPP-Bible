"""610 A3 · 人审数据导出（JSON / CSV / Markdown / 单 MIS，**只读**、纯标准库）。

导出的每条记录都**用候选边补全了结构信息**（source/target/direction），否则外部拿到一堆
`ae-xxx->yyy` 无从分析；补全一律来自 `data/attack_edges_candidates.jsonl`，不做推断。

列口径（CSV 表头固定，顺序即文档）：
    edge_id, source, target, direction, kind, verdict, confidence, reviewer, reviewed_at, reason_len, reason

  * `kind` = 候选边的 kind（`misconception_refutation` / `related_atom`）；
  * `verdict` = 注解的 `action`（approve/modify/reject）；
  * `confidence` = 注解的 `new_confidence`（modify 才有），否则留空 —— 不拿边的原档冒充人工改档；
  * `reason` 原样导出（**不做裁剪**）；`reason_len` 便于外部过滤 rubber-stamp 风险。

隐私边界：只导出**人审与其对象**相关字段（reviewer 是用户授权保留的审查人署名）；
不导出任何环境/凭据/本机路径信息。

CLI：
    json <out>            导出 JSON 数组
    csv  <out>            导出 CSV（表头见上）
    markdown <out>        导出 Markdown 摘要（按 MIS 分组）
    by-mis <mis> <out>    导出单个 MIS 的记录（JSON）
    --check [--dir D]     校验导出件与源数据一致（不一致 ⇒ exit 2）
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402
import human_review_cli as hrc  # noqa: E402

VERSION = "1.0"
DEFAULT_ANN = hrc.DEFAULT_ANN
DEFAULT_EDGES = aeg.DEFAULT_OUT
DEFAULT_DIR = ROOT / "data" / "human_review_export"

CSV_COLUMNS = ("edge_id", "source", "target", "direction", "kind", "verdict",
               "confidence", "reviewer", "reviewed_at", "reason_len", "reason")


def load_annotations(path: Path | str | None = None) -> list[dict]:
    return hrc.load_annotations(path if path else DEFAULT_ANN)


def edge_index(edges_path: Path | str | None = None) -> dict[str, dict]:
    return {str(e["id"]): e for e in aeg.load_edges(edges_path if edges_path else DEFAULT_EDGES)}


def enrich(annotations: list[dict], edges_path: Path | str | None = None) -> list[dict]:
    """把注解补全成导出记录（结构信息取自候选边；取不到 ⇒ 显式标 UNKNOWN）。"""
    idx = edge_index(edges_path)
    out: list[dict] = []
    for a in annotations:
        eid = str(a.get("edge_id", ""))
        e = idx.get(eid)
        reason = str(a.get("reason", ""))
        out.append({
            "edge_id": eid,
            "source": str(e["source"]) if e else "UNKNOWN",
            "target": str(e["target"]) if e else "UNKNOWN",
            "direction": str(e.get("direction")) if e else "UNKNOWN",
            "kind": str(e.get("kind")) if e else "UNKNOWN",
            "verdict": hrc.kind_of(a),
            "confidence": (a.get("new_confidence") or a.get("confidence") or ""),
            "reviewer": str(a.get("reviewer", "")),
            "reviewed_at": str(a.get("timestamp") or a.get("reviewed_at") or ""),
            "reason_len": len(reason),
            "reason": reason,
        })
    return out


def export_json(annotations: list[dict], path: Path | str, *,
                edges_path: Path | str | None = None) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    rows = enrich(annotations, edges_path)
    p.write_text(json.dumps(rows, ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")
    return p


def export_csv(annotations: list[dict], path: Path | str, *,
               edges_path: Path | str | None = None) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(CSV_COLUMNS), extrasaction="ignore",
                       lineterminator="\n")
    w.writeheader()
    for row in enrich(annotations, edges_path):
        w.writerow(row)
    p.write_text(buf.getvalue(), encoding="utf-8", newline="\n")
    return p


def mis_of_row(row: dict) -> str:
    return str(row["source"]) if row["direction"] == "mis_to_prop" else str(row["target"])


def export_markdown_summary(annotations: list[dict], path: Path | str, *,
                            edges_path: Path | str | None = None) -> Path:
    rows = enrich(annotations, edges_path)
    groups: dict[str, Counter] = {}
    for r in rows:
        groups.setdefault(mis_of_row(r), Counter())[r["verdict"]] += 1
    lines = ["# 人审记录摘要（按 MIS 分组）", "",
             f"- 记录 **{len(rows)}** 条 · MIS **{len(groups)}** 个", "",
             "| MIS | 总条数 | approve | modify | reject |", "|---|---:|---:|---:|---:|"]
    for mid in sorted(groups, key=lambda m: (-sum(groups[m].values()), m)):
        c = groups[mid]
        lines.append(f"| `{mid}` | {sum(c.values())} | {c.get('approve', 0)} | "
                     f"{c.get('modify', 0)} | {c.get('reject', 0)} |")
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return p


def export_by_mis(annotations: list[dict], mis_id: str, path: Path | str, *,
                  edges_path: Path | str | None = None) -> Path:
    rows = [r for r in enrich(annotations, edges_path) if mis_of_row(r) == str(mis_id)]
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"mis_id": str(mis_id), "count": len(rows), "records": rows},
                            ensure_ascii=False, indent=1) + "\n",
                 encoding="utf-8", newline="\n")
    return p


def export_all(out_dir: Path | str | None = None, *,
               annotations: list[dict] | None = None,
               edges_path: Path | str | None = None) -> dict[str, Path]:
    anns = annotations if annotations is not None else load_annotations()
    d = Path(out_dir) if out_dir else DEFAULT_DIR
    return {"json": export_json(anns, d / "human_review.json", edges_path=edges_path),
            "csv": export_csv(anns, d / "human_review.csv", edges_path=edges_path),
            "markdown": export_markdown_summary(
                anns, d / "human_review_summary.md", edges_path=edges_path)}


def check(out_dir: Path | str | None = None, *, annotations: list[dict] | None = None,
          edges_path: Path | str | None = None) -> list[str]:
    """导出件必须与源数据**逐字段一致**（条数 + 内容重算对比）。"""
    problems: list[str] = []
    anns = annotations if annotations is not None else load_annotations()
    d = Path(out_dir) if out_dir else DEFAULT_DIR
    jp, cp, mp = (d / "human_review.json", d / "human_review.csv",
                  d / "human_review_summary.md")
    if not jp.is_file():
        return [f"JSON 导出缺失：{jp}（先跑 export_all / json 子命令）"]
    rows = json.loads(jp.read_text(encoding="utf-8"))
    if len(rows) != len(anns):
        problems.append(f"JSON 条数 {len(rows)} ≠ 源 {len(anns)}")
    if rows != enrich(anns, edges_path):
        problems.append("JSON 内容与源数据重算结果不一致")
    if cp.is_file():
        lines = [x for x in cp.read_text(encoding="utf-8").splitlines() if x.strip()]
        if len(lines) - 1 != len(anns):
            problems.append(f"CSV 数据行 {len(lines) - 1} ≠ 源 {len(anns)}")
        if lines and lines[0].rstrip("\r") != ",".join(CSV_COLUMNS):
            problems.append(f"CSV 表头不符：{lines[0]!r}")
    else:
        problems.append(f"CSV 导出缺失：{cp}")
    if mp.is_file():
        n_mis = len({mis_of_row(r) for r in enrich(anns, edges_path)})
        body = mp.read_text(encoding="utf-8")
        if f"MIS **{n_mis}** 个" not in body:
            problems.append(f"Markdown 摘要里的 MIS 数 ≠ {n_mis}")
    else:
        problems.append(f"Markdown 导出缺失：{mp}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="human_review_export",
                                 description="610 A3 人审数据导出（JSON/CSV/Markdown/单 MIS）")
    ap.add_argument("--version", action="version", version=f"human_review_export {VERSION}")
    ap.add_argument("--annotations", default=None)
    ap.add_argument("--edges", default=None)
    ap.add_argument("--dir", default=None, help="导出目录（默认 data/human_review_export/）")
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sp = sub.add_parser("json")
    sp.add_argument("out", nargs="?", default=None)
    sp = sub.add_parser("csv")
    sp.add_argument("out", nargs="?", default=None)
    sp = sub.add_parser("markdown")
    sp.add_argument("out", nargs="?", default=None)
    sp = sub.add_parser("by-mis")
    sp.add_argument("mis_id")
    sp.add_argument("out", nargs="?", default=None)
    sp = sub.add_parser("all")
    a = ap.parse_args(argv)

    if a.check:
        problems = check(a.dir, edges_path=a.edges)
        if problems:
            print(f"[hrexport] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 2
        d = Path(a.dir) if a.dir else DEFAULT_DIR
        print(f"[hrexport] --check OK：{d} 下 JSON/CSV/Markdown 与源数据逐字段一致")
        return 0

    if a.cmd is None:
        ap.print_help()
        return 2

    anns = load_annotations(a.annotations)
    d = Path(a.dir) if a.dir else DEFAULT_DIR
    if a.cmd == "all":
        made = export_all(d, annotations=anns, edges_path=a.edges)
        print("[hrexport] " + " · ".join(f"{k}={v.name}" for k, v in made.items()))
        return 0
    out = Path(a.out) if getattr(a, "out", None) else None
    if a.cmd == "json":
        p = export_json(anns, out or d / "human_review.json", edges_path=a.edges)
    elif a.cmd == "csv":
        p = export_csv(anns, out or d / "human_review.csv", edges_path=a.edges)
    elif a.cmd == "markdown":
        p = export_markdown_summary(anns, out or d / "human_review_summary.md",
                                   edges_path=a.edges)
    else:
        p = export_by_mis(anns, a.mis_id, out or d / f"{a.mis_id}.json", edges_path=a.edges)
    print(f"[hrexport] 已写 {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
