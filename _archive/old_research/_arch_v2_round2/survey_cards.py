#!/usr/bin/env python3
"""533 轮勘察：56 张证据卡的机验结构盘点（只读，不改正式文件）。

输出每张 EV 卡：kind / fixture / artifact / run_match / artifact_assert 结构，
以及引用它的原子命题 claim_type。为 V-iso 阴面迁移分批提供真实数据。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import atom_evidence_replay as R  # noqa: E402

EVIDENCE = ROOT / "evidence"
ATOMS = ROOT / "atoms"


def load(p: Path) -> dict:
    return R.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))


def main() -> None:
    # EV 卡索引
    cards = {}
    for p in sorted(EVIDENCE.rglob("EV-*.md")):
        m = load(p)
        eid = str(m.get("id") or p.stem)
        actual = m.get("actual") if isinstance(m.get("actual"), dict) else {}
        asserts = m.get("artifact_assert") or []
        akinds = {}
        for a in asserts:
            if isinstance(a, dict):
                akinds[a.get("kind")] = akinds.get(a.get("kind"), 0) + 1
        cards[eid] = {
            "path": p.relative_to(ROOT).as_posix(),
            "kind": m.get("kind"),
            "fixture": m.get("fixture"),
            "artifact": m.get("artifact"),
            "rm_file": actual.get("run_match_file"),
            "rm_keys": actual.get("run_match_keys") or [],
            "n_assert": len(asserts),
            "akinds": akinds,
            "props": [],
        }
    # 原子命题引用
    for p in sorted(ATOMS.rglob("ATOM-*.md")):
        m = load(p)
        aid = str(m.get("id") or p.stem)
        for pr in (m.get("claim_structured") or []):
            if not isinstance(pr, dict):
                continue
            ct = pr.get("claim_type")
            for ev in (pr.get("evidence") or []):
                ev = str(ev)
                if ev in cards:
                    cards[ev]["props"].append(f"{aid}/{pr.get('id')}:{ct}")
    # 打印
    print(f"共 {len(cards)} 张 EV 卡")
    hdr = ("ev", "kind", "fixture?", "rm", "nA", "assert_kinds", "props")
    print("\t".join(hdr))
    n_obs = n_inf = n_mix = 0
    for eid, c in cards.items():
        types = {x.rsplit(":", 1)[-1] for x in c["props"]}
        if types == {"observation"}:
            n_obs += 1
        elif types == {"inference"}:
            n_inf += 1
        elif types:
            n_mix += 1
        ak = ",".join(f"{k}:{v}" for k, v in sorted(c["akinds"].items()))
        row = (
            eid,
            str(c["kind"]),
            "Y" if c["fixture"] else "-",
            f"{len(c['rm_keys'])}" if c["rm_file"] else "-",
            str(c["n_assert"]),
            ak,
            ";".join(c["props"]),
        )
        print("\t".join(row))
    print(f"\n仅observation引用={n_obs} 仅inference={n_inf} 混合/无命题={n_mix}")


if __name__ == "__main__":
    main()
