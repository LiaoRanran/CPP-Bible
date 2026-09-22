"""626 E2 · Review Pack v2（**两层包** + 自动生成 + 跨平台）

外部大模型指出现有包是"治理决策摘要包"，不是完整证据包。626 拆成两层：

| 包 | 目的 | 体积 | 能否据此下判决 |
|---|---|---|---|
| **Review Pack** | 治理决策摘要 + 审查调度 | 小 | 不能（只够调度） |
| **Evidence Pack** | 对指定 item 打包最小充分证据 | 按 item 数 | **可以**（最小闭环） |

核心改进：
- **自动生成**（脚本打包，不用手动）
- **路径分隔符统一 `/`**（跨平台）
- **控制字符清洗**
- 带 **SNAPSHOT_MANIFEST**（git_sha + dataset_sha256 + generated_at）
- **最小闭环审查页面**：Top-N 高歧义 item 生成自包含 HTML（一屏看全证据）

纯标准库；`--check` 验证现有包。
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import subprocess
import sys
import time
import zipfile
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import authority_projection_compiler_626 as AP  # noqa: E402
import decision_event_v2_626 as D  # noqa: E402
import pack_review_zip as PZ  # noqa: E402
import review_item_ledger_626 as R  # noqa: E402

REVIEW_LEDGER = os.path.join(ROOT, "data", "review_item_ledger.jsonl")
LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
DESKTOP = os.path.join(os.path.expanduser("~"), "Desktop")

TEXT_EXT = PZ.TEXT_EXT
CTRL = PZ.CTRL


def _git_sha() -> str:
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                           text=True, cwd=ROOT, timeout=30)
        return p.stdout.strip() or "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def _clean(b: bytes) -> bytes:
    return bytes(x for x in b if x not in CTRL)


def _write(z: zipfile.ZipFile, name: str, data: bytes) -> None:
    zi = zipfile.ZipInfo(name.replace("\\", "/"), date_time=time.localtime()[:6])
    zi.external_attr = 0o644 << 16
    if name.endswith(TEXT_EXT):
        data = _clean(data)
    z.writestr(zi, data)


class ReviewPackGenerator:
    def __init__(self) -> None:
        self.review = R.ReviewItemLedger.import_jsonl(REVIEW_LEDGER)
        self.ledger = D.AuthorityLedger.import_jsonl(LEDGER)
        self.proj = AP.AuthorityProjectionCompiler()

    # ── 内容生成 ──
    def _readme(self) -> str:
        return "\n".join([
            "# 阙疑 Review Pack v2（治理决策摘要包 + 审查调度包）", "",
            f"- generated_at: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
            f"- git_sha: `{_git_sha()}`",
            f"- 唯一待审 item: **{self.review.get_unique_count()}**"
            f"（记录 {self.review.get_record_count()}）",
            f"- Authority events: **{len(self.ledger)}**",
            f"- 独立人类确认强度: **{self.ledger.independent_human_review_count()}**",
            "", "## ⚠ 包定位",
            "本包**不是完整证据包**，只够「决定审查顺序与提出质疑」。",
            "要对某个 item 独立复核，请使用 **Evidence Pack**（含最小闭环审查页面）。",
            "", "## 内容",
            "- `01_review_items.json` — 93 个唯一待审 item",
            "- `02_decision_points.md` — 8 大决策点摘要",
            "- `03_authority_summary.md` — Authority Ledger 摘要",
            "- `04_w2_summary.json` — W2 投影摘要",
            "- `05_pck_summary.json` — PCK 状态摘要",
            "- `SNAPSHOT_MANIFEST.json` — 快照血缘", "",
        ])

    def _decision_points(self) -> str:
        L = ["# 8 大决策点（需人裁决，机器不代签）", ""]
        pts = [
            "是否承认 388 条为「批量授权」而非「逐条人审」，并在对外口径中更正？",
            "是否对 194 条镜像边做逐条复核（镜像能否安全镜像本身是待证命题）？",
            "是否对 176 条抽样外推做逐条复核（20/20 不能外推到 194 条）？",
            "modify（34 条）口径如何裁决——它决定论证层判决完全不同？",
            "是否授权执行 93 个唯一 item 的逐条人审（当前未执行）？",
            "PCK authorized 提升策略（S1-S4）采纳哪一个？当前 27/83=32.5%。",
            "31 条豁免（27 legacy + 4 HC）到期处置：续期 / 取消 / 补四元组？",
            "QueYi Core 剥离触发标准 ②③（治理裁定）是否满足？当前 2/5。",
        ]
        for i, p in enumerate(pts, 1):
            L.append(f"{i}. {p}")
        return "\n".join(L) + "\n"

    def _authority_summary(self) -> str:
        by_m = self.ledger.count_by_review_method()
        by_o = self.ledger.count_by_decision_origin()
        return "\n".join([
            "# Authority Ledger 摘要", "",
            f"- 事件总数: **{len(self.ledger)}**",
            f"- 哈希链: {'✅ 完整' if self.ledger.verify_chain() else '❌ 断裂'}",
            f"- review_method 分布: `{by_m}`",
            f"- decision_origin 分布: `{by_o}`",
            f"- **独立人类确认强度: {self.ledger.independent_human_review_count()}**"
            "（ITEM_BLIND/ITEM_SECOND_REVIEW + human_observed）", "",
            "> 62b：622 的 30 条为 ITEM_OPEN + user_authorized_execution，**不计入**。", "",
        ])

    def _manifest(self, extra: dict) -> str:
        h = hashlib.sha256()
        for it in sorted(self.review.all_items(), key=lambda x: x.review_item_id):
            h.update(it.review_item_id.encode("utf-8"))
        m = {"generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "git_sha": _git_sha(),
             "dataset_sha256": h.hexdigest(),
             "path_separator": "/",
             "unique_review_items": self.review.get_unique_count(),
             "independent_human_review_count":
                 self.ledger.independent_human_review_count()}
        m.update(extra)
        return json.dumps(m, ensure_ascii=False, indent=2)

    # ── Review Pack ──
    def generate_review_pack(self, output_path: str) -> dict:
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        items = [it.to_dict() for it in self.review.all_items()]
        w2 = self.proj.w2_summary()
        pck = {k: v for k, v in self.proj.compile_pck_all().items() if k != "results"}
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
            _write(z, "00_README.md", self._readme().encode("utf-8"))
            _write(z, "01_review_items.json",
                   json.dumps(items, ensure_ascii=False, indent=2).encode("utf-8"))
            _write(z, "02_decision_points.md", self._decision_points().encode("utf-8"))
            _write(z, "03_authority_summary.md", self._authority_summary().encode("utf-8"))
            _write(z, "04_w2_summary.json",
                   json.dumps(w2, ensure_ascii=False, indent=2).encode("utf-8"))
            _write(z, "05_pck_summary.json",
                   json.dumps(pck, ensure_ascii=False, indent=2).encode("utf-8"))
            _write(z, "SNAPSHOT_MANIFEST.json",
                   self._manifest({"pack_type": "review"}).encode("utf-8"))
        return {"path": output_path, "entries": 6 + 1,
                "size": os.path.getsize(output_path)}

    # ── Evidence Pack ──
    def _item_html(self, it: R.ReviewItem) -> str:
        ev = self.ledger.get_current("edge", it.target_id)
        ev_rows = ""
        if ev is not None:
            ev_rows = (f"<tr><td>当前决定</td><td>{html.escape(ev.result)}</td></tr>"
                       f"<tr><td>review_method</td><td>{html.escape(ev.review_method)}</td></tr>"
                       f"<tr><td>decision_origin</td><td>{html.escape(ev.decision_origin)}</td></tr>"
                       f"<tr><td>event_id</td><td>{html.escape(ev.event_id)}</td></tr>")
        return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{html.escape(it.review_item_id)} · 最小闭环审查</title>
<style>body{{background:#0a0e1a;color:#c9d4ee;font:14px/1.6 system-ui;padding:28px}}
h1{{font-weight:600}}table{{border-collapse:collapse;width:100%}}
th,td{{text-align:left;padding:8px;border-bottom:1px solid #1f2b45}}
th{{color:#7c89a8}}.pill{{padding:2px 9px;border-radius:999px;border:1px solid #3ad6c5;color:#3ad6c5}}
</style></head><body>
<h1>{html.escape(it.review_item_id)}</h1>
<p><span class="pill">{html.escape(it.status)}</span> 歧义度 {it.ambiguity_score} ·
优先级 {html.escape(it.priority)} · 来源批次 {html.escape(it.source_batch or '-')}</p>
<table>
<tr><th>项</th><th>值</th></tr>
<tr><td>target_type</td><td>{html.escape(it.target_type)}</td></tr>
<tr><td>target_id</td><td>{html.escape(it.target_id)}</td></tr>
<tr><td>review_revision</td><td>{it.review_revision}</td></tr>
<tr><td>symmetry_proof_id</td><td>{html.escape(it.symmetry_proof_id or 'null（未验证）')}</td></tr>
{ev_rows}
</table>
<p style="color:#7c89a8">最小闭环：target claim + 当前 Authority 状态已在一屏内；
完整 evidence/negative test/replay 需对照仓库 <code>evidence/</code> 与 <code>build/</code>。</p>
</body></html>"""

    def generate_evidence_pack(self, output_path: str,
                               review_item_ids: Optional[list] = None,
                               top_n: int = 10, html_limit: int = 10) -> dict:
        items = self.review.sorted_by_ambiguity()
        if review_item_ids is not None:
            # 显式传入（含空列表）⇒ 按列表筛选；空列表 ⇒ 空包（不回退到 top_n）
            wanted = set(review_item_ids)
            items = [it for it in items if it.review_item_id in wanted
                     or it.target_id in wanted]
        else:
            items = items[:top_n]
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        n_html = 0
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
            _write(z, "00_README.md",
                   ("# Evidence Pack（最小充分证据）\n\n"
                    f"- item 数: {len(items)}\n"
                    "- 每个 item 的 JSON 在 `items/`，HTML 最小闭环页面在 `pages/`\n"
                    "- 控制字符已清洗；路径分隔符统一 `/`\n").encode("utf-8"))
            for it in items:
                safe = it.review_item_id.replace("/", "_").replace("\\", "_")
                _write(z, f"items/{safe}.json",
                       json.dumps(it.to_dict(), ensure_ascii=False, indent=2).encode("utf-8"))
                if n_html < html_limit:
                    _write(z, f"pages/{safe}.html", self._item_html(it).encode("utf-8"))
                    n_html += 1
            _write(z, "SNAPSHOT_MANIFEST.json",
                   self._manifest({"pack_type": "evidence",
                                   "items": len(items),
                                   "html_pages": n_html}).encode("utf-8"))
        return {"path": output_path, "items": len(items), "html_pages": n_html,
                "size": os.path.getsize(output_path)}

    # ── 验证 ──
    def validate_pack(self, zip_path: str) -> dict:
        if not os.path.exists(zip_path):
            return {"ok": False, "error": "not found"}
        with zipfile.ZipFile(zip_path) as z:
            names = z.namelist()
            bs = sum(1 for n in names if "\\" in n)
            has_manifest = "SNAPSHOT_MANIFEST.json" in names
            ctrl = sum(1 for n in names if n.endswith(TEXT_EXT)
                       and any(b in CTRL for b in z.read(n)))
            bad = z.testzip()
        ok = bs == 0 and has_manifest and ctrl == 0 and bad is None
        return {"ok": ok, "entries": len(names), "backslash": bs,
                "has_manifest": has_manifest, "control_chars": ctrl,
                "bad_crc": bad}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    import tempfile
    g = ReviewPackGenerator()
    chk("唯一 item 93", g.review.get_unique_count() == 93,
        f"({g.review.get_unique_count()})")
    with tempfile.TemporaryDirectory() as td:
        rp = os.path.join(td, "rp.zip")
        r = g.generate_review_pack(rp)
        chk("Review Pack 生成", os.path.exists(rp))
        v = g.validate_pack(rp)
        chk("Review Pack 验证通过", v["ok"], str(v))
        chk("含 SNAPSHOT_MANIFEST", v["has_manifest"])
        chk("路径正斜杠", v["backslash"] == 0)

        ep = os.path.join(td, "ep.zip")
        e = g.generate_evidence_pack(ep, top_n=10)
        chk("Evidence Pack 生成", os.path.exists(ep))
        chk("Evidence Pack item 数 = 10", e["items"] == 10, f"({e['items']})")
        chk("生成了 HTML 页面", e["html_pages"] >= 3, f"({e['html_pages']})")
        v2 = g.validate_pack(ep)
        chk("Evidence Pack 验证通过", v2["ok"], str(v2))

        # 按 id 筛选
        ids = [it.review_item_id for it in g.review.sorted_by_ambiguity()[:2]]
        ep2 = os.path.join(td, "ep2.zip")
        e2 = g.generate_evidence_pack(ep2, review_item_ids=ids)
        chk("按 id 筛选生效", e2["items"] == 2, f"({e2['items']})")

        # 空列表
        ep3 = os.path.join(td, "ep3.zip")
        e3 = g.generate_evidence_pack(ep3, review_item_ids=[])
        chk("空 items 列表不报错", e3["items"] == 0)
    print(f"E2 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="626 E2 Review Pack v2")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--generate-review", action="store_true", help="生成 Review Pack")
    ap.add_argument("--generate-evidence", action="store_true", help="生成 Evidence Pack")
    ap.add_argument("--items", help="逗号分隔的 review_item_id 列表")
    ap.add_argument("--top", type=int, default=10, help="Top-N 高歧义（默认 10）")
    ap.add_argument("--out", help="输出路径")
    ap.add_argument("--validate", help="验证指定 ZIP")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()
    g = ReviewPackGenerator()
    if args.validate:
        print(json.dumps(g.validate_pack(args.validate), ensure_ascii=False, indent=2))
        return 0 if g.validate_pack(args.validate)["ok"] else 1
    if args.generate_review:
        out = args.out or os.path.join(
            DESKTOP, "阙疑_ReviewPack_v2_20260922.zip")
        print(json.dumps(g.generate_review_pack(out), ensure_ascii=False, indent=2))
        return 0
    if args.generate_evidence:
        out = args.out or os.path.join(
            DESKTOP, "阙疑_EvidencePack_Top10_20260922.zip")
        items = args.items.split(",") if args.items else None
        print(json.dumps(g.generate_evidence_pack(out, items, top_n=args.top),
                         ensure_ascii=False, indent=2))
        return 0
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
