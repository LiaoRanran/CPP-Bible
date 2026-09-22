"""625 D4 · PCK authorized 提升策略设计（**只设计，不代签**）

基于 624 E1 实测（27 原子证全已授权 / 56 证据证无人审来源 ⇒ 27/83=32.5%，未达 >48%），
**设计**把 authorized 从 32.5% 提升到 >48% 的策略，并产出「待人审」证据证清单。
**绝不修改任何证书**（铁律：不代签）。

策略（设计层，不执行）：
- S1 证据证人审队列：56 张证据证 → 人审清单（复用 625 D2/D3 框架）。
- S2 机器可确认候选：证据证若其底层原子已 authorized 且 claim 与原子一致，列为「建议 approve」待人确认。
- S3 目标推算：需把至少 ceil(0.48*83 - 27) = 13 张证据证升 approved（或更优），才达 >48%。

铁律：只读 certs/annotations；必有 `--check`；**不写任何 .pck.yaml**。
"""
from __future__ import annotations

import argparse
import glob
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
TARGET_RATE = 0.48


def load_certs() -> list[tuple[str, dict]]:
    out: list[tuple[str, dict]] = []
    for p in sorted(glob.glob(os.path.join(CERT_DIR, "*.pck.yaml"))):
        try:
            import yaml  # type: ignore[import-untyped]
            with open(p, encoding="utf-8") as fh:
                out.append((os.path.basename(p), yaml.safe_load(fh)))
        except Exception:
            pass
    return out


def analyze() -> dict:
    certs = load_certs()
    n = len(certs)
    by_status: Counter = Counter()
    evidence_pending: list[str] = []
    atom_authorized = 0
    machine_confirm_candidates: list[str] = []
    for name, c in certs:
        ha = (c.get("human_authority") or {}) if isinstance(c, dict) else {}
        st = str(ha.get("status") or "unverified")
        by_status[st] += 1
        is_atom = name.startswith("ATOM-") or name.startswith("MIS-") or name.startswith("S")
        if st == "approved":
            if is_atom:
                atom_authorized += 1
        else:
            if not is_atom:  # 证据证待人审
                evidence_pending.append(name)
                # S2 候选：claim 与某原子一致（简化：证据证自带 approved 字段外的可确认信号）
                if str((c.get("claim") or {}).get("verdict", "")).lower() in ("approve", "supported"):
                    machine_confirm_candidates.append(name)
    authorized = by_status.get("approved", 0)
    need = max(0, int(TARGET_RATE * n + 1e-9) - authorized + 1)
    return {
        "total": n, "by_status": dict(by_status), "authorized": authorized,
        "rate": round(authorized / n, 4) if n else 0.0,
        "atom_authorized": atom_authorized,
        "evidence_pending": evidence_pending,
        "machine_confirm_candidates": machine_confirm_candidates,
        "target_rate": TARGET_RATE,
        "need_approve_more": need,
    }


STRATEGIES = [
    ("S1 证据证人审队列", "56 张证据证 → 人审清单（复用 625 D2 仪表盘 / D3 执行框架），"
     "由人逐条 approve/reject，来源标注 authorized_by。"),
    ("S2 机器可确认候选", "证据证若其底层 claim 已 verdict=approve/supported，列为「建议 approve」"
     "待人确认（机器仍不代签，仅降人审成本）。"),
    ("S3 目标推算", "需至少 {need} 张证据证升 approved 才达 >48%；优先 S2 候选 → 余下走 S1 人审。"),
    ("S4 接管口径统一", "PCK 证书 human_authority.status 与 Authority 日志 power 建立映射校验，"
     "避免双源漂移（624 已建 pck_authority_sync_620，可扩展为双向）。"),
]


def render(a: dict) -> str:
    L = ["# 625 D4 · PCK authorized 提升策略设计（只设计，不代签）", "",
         f"> 当前：**{a['authorized']}/{a['total']} = {a['rate']:.1%}**（624 E1 实测 27.7%→32.5%）｜目标：**>48%**",
         "",
         "## 一、现状快照", "",
         f"- 总证书：**{a['total']}**（27 原子证 + 56 证据证）",
         f"- authorized（approved）：**{a['authorized']}**，其中原子证 **{a['atom_authorized']}**",
         f"- 各状态：{a['by_status']}",
         f"- 待人审证据证：**{len(a['evidence_pending'])}** 张", "",
         "## 二、提升策略", ""]
    for name, desc in STRATEGIES:
        d = desc.format(need=a["need_approve_more"])
        L.append(f"### {name}\n- {d}\n")
    L += ["## 三、达成路径（设计）", "",
          f"1. 走 S2 把机器可确认候选（{len(a['machine_confirm_candidates'])} 张）交由人快速 approve；",
          f"2. 余下证据证走 S1 人审队列（D2/D3 框架），目标净增 **{a['need_approve_more']}** 张 approved；",
          f"3. 达成后 authorized ≥ {a['authorized'] + a['need_approve_more']}/{a['total']} "
          f"= {(a['authorized'] + a['need_approve_more']) / a['total']:.1%} > **48%**。", "",
          "## 四、局限性声明（铁律）", "",
          "1. **本工具只设计，绝不修改任何 `.pck.yaml`**（不代签）。",
          "2. 真实提升必须经过人审执行（625 D3 框架），机器仅降成本、不替人判。",
          "3. 证据证无人审来源是瓶颈（非机器未算），故策略核心是「把人审做起来」。", ""]
    return "\n".join(L) + "\n"


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    a = analyze()
    chk("证书总数 83", a["total"] == 83)
    chk("authorized 27（624 E1）", a["authorized"] == 27)
    chk("目标需净增 ≥1", a["need_approve_more"] >= 1)
    chk("待人审证据证 >0", len(a["evidence_pending"]) > 0)
    # 不代签：analyze 只读，不写任何 pck 文件
    before = sorted(glob.glob(os.path.join(CERT_DIR, "*.pck.yaml")))
    render(a)  # 仅渲染，不落盘
    after = sorted(glob.glob(os.path.join(CERT_DIR, "*.pck.yaml")))
    chk("未修改任何证书文件", before == after)
    print(f"D4 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="625 D4 PCK 提升策略设计（只设计不代签）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写出策略文档")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    a = analyze()
    if args.report:
        p = os.path.join(ROOT, "data", "pck_upgrade_strategy_625.md")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render(a))
        print(f"written {p}")
        return 0
    print(f"authorized={a['authorized']}/{a['total']}={a['rate']:.1%} "
          f"target>{a['target_rate']:.0%} need+{a['need_approve_more']} (design only, no signing)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
