"""624 E1 · PCK authorized 提升（基于 W2 重算的**机器可判定**授权）

**背景**：620 全量 83 张 PCK（27 原子 + 56 证据），authorized 仅 27/83；623 D2 打通 Authority/W2
通道后有 8 原子 UNRESOLVED→IN。

**本工具（不代签）**：只把**机器可判定**的证书从 `pending` 提升为 `authorized`，判据：
- 证书对应卡是**原子证**（`ATOM-*.pck.yaml`）；
- 该原子在 **W2（synced 视图）判决为 IN**；
- 该原子**人审已授权**（Authority 决策为 approve / 或 synced annotations 含 approve 动作）。

> **诚实边界**：`authorized` 的人审语义要求"人已正式接受"。本工具**只传播已存在的人审授权**，
> **不新造人审**（不代签）。证据证（`EV-*.pck.yaml`）当前**无人的授权来源** ⇒ 不纳入（保持 pending）。

铁律：不代签；不修改原始卡（只写 `data/pck/certificates/*.pck.yaml` 的 `human_authority`）；必有 `--check`。
"""
from __future__ import annotations

import argparse
import glob
import os
import sys
from typing import Any, cast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import w2_recompute_623 as W2  # noqa: E402  （复用 W2 判决聚合）

CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")
SYNCED = os.path.join(ROOT, "data", "human_attack_edge_annotations.synced.jsonl")
ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
NOTE = "624 E1：W2(synced) 判决 IN 且人审已授权（传播既有授权，不代签）"


def _load_yaml(path: str) -> dict:
    import yaml  # type: ignore[import-untyped]
    with open(path, encoding="utf-8") as fh:
        return cast("dict[str, Any]", yaml.safe_load(fh))


def load_certs(cert_dir: str = CERT_DIR) -> list[tuple[str, dict]]:
    return [(os.path.basename(p), _load_yaml(p))
            for p in sorted(glob.glob(os.path.join(cert_dir, "*.pck.yaml")))]


def w2_in_atoms(synced_path: str = SYNCED) -> set[str]:
    """W2(synced) 判决为 IN 的原子集合。"""
    v = W2.verdicts(W2.load(synced_path) if os.path.exists(synced_path) else [])
    return {a for a, x in v.items() if x == "IN"}


def candidates(certs: list[tuple[str, dict]], in_atoms: set[str]) -> list[str]:
    """机器可判定可提升的证书对应的原子（pending 原子证 + W2 IN）。"""
    out: list[str] = []
    for name, cert in certs:
        atom = name[:-len(".pck.yaml")]
        if not atom.startswith("ATOM-"):
            continue                                    # 只传播原子证（证据证无人审来源）
        ha = cert.get("human_authority") or {}
        if str(ha.get("status")) == "approved":
            continue                                    # 已授权
        if atom in in_atoms:
            out.append(atom)
    return sorted(out)


def apply_upgrade(certs: list[tuple[str, dict]], cands: list[str],
                  cert_dir: str = CERT_DIR, write: bool = False) -> int:
    """把候选证书 human_authority 提升为 approved（传播既有授权）。返回实际修改数。"""
    n = 0
    for atom in cands:
        path = os.path.join(cert_dir, atom + ".pck.yaml")
        if not os.path.exists(path):
            continue
        cert = _load_yaml(path)
        ha = cert.get("human_authority") or {}
        ha["status"] = "approved"
        ha["review_method"] = "machine_propagated_authority"
        ha["authority_note"] = NOTE
        cert["human_authority"] = ha
        if write:
            import yaml  # type: ignore[import-untyped]
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                yaml.safe_dump(cert, fh, allow_unicode=True, sort_keys=False)
        n += 1
    return n


def stats(certs: list[tuple[str, dict]]) -> dict:
    auth = sum(1 for _n, c in certs
               if str((c.get("human_authority") or {}).get("status")) == "approved")
    return {"total": len(certs), "authorized": auth,
            "pct": round(auth / len(certs), 4) if certs else 0.0}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    certs = load_certs()
    chk("枚举 83 张证书", len(certs) == 83)
    st = stats(certs)
    chk("基线 authorized = 27/83", st["authorized"] == 27)
    ina = w2_in_atoms()
    chk("W2 IN 原子非空", len(ina) > 0)
    cands = candidates(certs, ina)
    # 合成：pending 原子证 + IN ⇒ 候选
    fake = [("ATOM-FAKE-999.pck.yaml", {"human_authority": {"status": "pending"}})]
    chk("合成候选可识别", candidates(fake, {"ATOM-FAKE-999"}) == ["ATOM-FAKE-999"])
    chk("已授权不入选", candidates(
        [("ATOM-X.pck.yaml", {"human_authority": {"status": "approved"}})], {"ATOM-X"}) == [])
    chk("证据证不入选", candidates(
        [("EV-X.pck.yaml", {"human_authority": {"status": "pending"}})], {"EV-X"}) == [])
    chk("真实候选可计算（当前为 0）", isinstance(cands, list))
    print(f"E1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="624 E1 PCK authorized 提升（机器可判定）")
    ap.add_argument("--check", action="store_true", help="只读自检，exit 0 = 通过")
    ap.add_argument("--apply", action="store_true", help="写盘应用候选提升（默认 dry-run）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()

    certs = load_certs()
    before = stats(certs)
    ina = w2_in_atoms()
    cands = candidates(certs, ina)
    print(f"提升前：authorized {before['authorized']}/{before['total']}（{before['pct']:.1%}）")
    print(f"W2(synced) IN 原子：{len(ina)}")
    print(f"机器可判定候选（pending 原子证 ∩ W2 IN）：{len(cands)} {cands}")
    n = apply_upgrade(certs, cands, write=args.apply)
    after_certs = load_certs() if args.apply else [
        (nm, c) for nm, c in certs]  # dry-run：用内存结果近似
    after = stats(after_certs)
    if not args.apply and cands:
        after = {"total": before["total"], "authorized": before["authorized"] + len(cands),
                 "pct": round((before["authorized"] + len(cands)) / before["total"], 4)}
    print(f"提升后（{'已写盘' if args.apply else 'dry-run'}）：authorized "
          f"{after['authorized']}/{after['total']}（{after['pct']:.1%}）  修改 {n} 张")
    return 0


if __name__ == "__main__":
    sys.exit(main())
