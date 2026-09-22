"""620 B3 · PCK 证书状态统计 + 批量渲染

读取全量 83 张 certificate，做三类分布统计，并用 619 B4 渲染器批量渲染成可读 markdown。

**5 级状态口径**（本工具定义，对应 C1 Authority 接口的四权力 + 未决）：

| 级别 | 含义 | 当前来源 |
|---|---|---|
| `authorized` | 人已正式接受 | `human_authority.status == approved` |
| `conditionally_authorized` | 附条件接受 | 预留（当前 0） |
| `disputed` | 有争议 / 已否决 | `human_authority.status == rejected` |
| `abstain` | 人明确弃权 | 预留（当前 0） |
| `unverified` | 尚未经人判定 | `human_authority.status == pending` |

> 诚实说明：619 B1 schema 的 `human_authority.status` 只有 `pending/approved/rejected` 三值，
> 5 级中的 `conditionally_authorized` 与 `abstain` **当前恒为 0**（schema 尚未支持），
> 属 620 C1 接口定义的**前瞻分级**，此处如实登记为 0，不虚报。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import pck_certificate_verifier_619 as B2  # noqa: E402
import pck_renderer_619 as B4  # noqa: E402

DEFAULT_CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
DEFAULT_RENDER_DIR = os.path.join(ROOT, "data", "pck", "rendered")

STATUS_MAP = {
    "approved": "authorized",
    "rejected": "disputed",
    "pending": "unverified",
}
FIVE_LEVELS = ("authorized", "conditionally_authorized", "disputed", "abstain", "unverified")


def load_certs(cert_dir: str = DEFAULT_CERT_DIR) -> list[tuple[str, dict]]:
    out = []
    for path in sorted(glob.glob(os.path.join(cert_dir, "*.pck.yaml"))):
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        import yaml
        cert = yaml.safe_load(text)
        out.append((os.path.basename(path), cert))
    return out


def stats(certs: list[tuple[str, dict]]) -> dict:
    by_status = {k: 0 for k in FIVE_LEVELS}
    by_cs: dict[str, int] = {}
    by_verifiers: dict[int, int] = {}
    validation_ok = 0

    for _fname, cert in certs:
        ha = (cert.get("human_authority") or {})
        lvl = STATUS_MAP.get(str(ha.get("status") or ""), "unverified")
        by_status[lvl] = by_status.get(lvl, 0) + 1

        cs = (cert.get("uncertainty") or {}).get("cs_upper_bound")
        key = str(cs)
        by_cs[key] = by_cs.get(key, 0) + 1

        n = len(cert.get("verifiers") or [])
        by_verifiers[n] = by_verifiers.get(n, 0) + 1

        if B2.validate_cert(cert)["ok"]:
            validation_ok += 1

    return {
        "total": len(certs),
        "by_status": by_status,
        "by_cs_upper_bound": dict(sorted(by_cs.items())),
        "by_verifier_count": dict(sorted(by_verifiers.items())),
        "validation_ok": validation_ok,
        "validation_fail": len(certs) - validation_ok,
    }


def render_all(certs: list[tuple[str, dict]], out_dir: str = DEFAULT_RENDER_DIR) -> list[str]:
    os.makedirs(out_dir, exist_ok=True)
    written = []
    for fname, cert in certs:
        md = B4.render(cert)
        out_name = fname.replace(".pck.yaml", ".md")
        path = os.path.join(out_dir, out_name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        written.append(out_name)
    return written


def render_report(st: dict, written: list[str]) -> str:
    o = ["# 620 B3 · PCK 证书状态统计 + 批量渲染\n"]
    o.append(f"> 证书总数：**{st['total']}** · B2 验证通过 {st['validation_ok']} / 失败 {st['validation_fail']}\n")
    o.append("## 一、5 级状态分布\n")
    o.append("| 状态级别 | 张数 | 占比 |")
    for k in FIVE_LEVELS:
        v = st["by_status"].get(k, 0)
        pct = f"{100 * v / st['total']:.1f}%" if st["total"] else "—"
        o.append(f"| {k} | {v} | {pct} |")
    o.append("")
    o.append("## 二、按 uncertainty.cs_upper_bound 分布\n")
    o.append("| cs_upper_bound | 张数 |")
    for k, v in st["by_cs_upper_bound"].items():
        o.append(f"| {k} | {v} |")
    o.append("")
    o.append("## 三、按 verifiers 数量分布\n")
    o.append("| verifiers 数 | 张数 |")
    for k, v in st["by_verifier_count"].items():
        o.append(f"| {k} | {v} |")
    o.append("")
    o.append(f"## 四、渲染产物\n- 目录：`data/pck/rendered/`\n- 文件数：**{len(written)}**\n")
    return "\n".join(o)


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    sample = B4._sample_cert()
    st = stats([("a.pck.yaml", sample)])
    chk("单张统计总数=1", st["total"] == 1)
    chk("approved 映射为 authorized", st["by_status"]["authorized"] == 1)
    pending = dict(sample)
    pending["human_authority"] = {"status": "pending", "review_method": "batch_authorization"}
    chk("pending 映射为 unverified", stats([("b", pending)])["by_status"]["unverified"] == 1)
    rejected = dict(sample)
    rejected["human_authority"] = {"status": "rejected", "review_method": "batch_authorization"}
    chk("rejected 映射为 disputed", stats([("c", rejected)])["by_status"]["disputed"] == 1)
    chk("5 级键齐全", set(st["by_status"]) == set(FIVE_LEVELS))
    chk("cs_upper_bound 分桶", st["by_cs_upper_bound"].get("0.009062") == 1)
    chk("verifiers 计数分桶", st["by_verifier_count"].get(1) == 1)
    chk("报告可渲染", "状态分布" in render_report(st, []))
    print(f"B3 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="620 B3 PCK 状态统计 + 批量渲染")
    ap.add_argument("--cert-dir", default=DEFAULT_CERT_DIR)
    ap.add_argument("--render-dir", default=DEFAULT_RENDER_DIR)
    ap.add_argument("--out", help="统计报告输出路径（不传则打印）")
    ap.add_argument("--no-render", action="store_true", help="只统计不渲染")
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return selftest()

    certs = load_certs(args.cert_dir)
    st = stats(certs)
    written = [] if args.no_render else render_all(certs, args.render_dir)
    md = render_report(st, written)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"wrote {args.out}  certs={st['total']} rendered={len(written)}")
    else:
        print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
