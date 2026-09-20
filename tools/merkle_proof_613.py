#!/usr/bin/env python3
"""613 任务E3 · Merkle **包含证明**（per-file）生成与验证。

`merkle_integrity.py` 已给出目录级 Merkle 根（信任根台账）；本工具补上**单文件级**证明：
对覆盖目录（atoms / evidence / Examples / Book / mutation_baselines）内的代表性文件，
生成"此文件在此树中"的包含证明并**当场验证**，证明某个文件确实属于某个已承诺的根。

证明结构（来自 merkle_integrity.prove）：叶 hash 绑定**相对目录的路径** ⇒ 证明自带
"文件属于哪个路径"的绑定，不能拿 A 文件的证明去套 B 文件。

产物：`data/merkle_proof_613.md`（每文件：目录 / 相对路径 / 步数 / 根 / 验证结果）。

CLI：
  python tools/merkle_proof_613.py             # 每目录取前 N 个文件出证明并验证
  python tools/merkle_proof_613.py --per-dir 2 # 自定义每目录抽样数
  python tools/merkle_proof_613.py --check     # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import merkle_integrity as mi  # noqa: E402

OUT = ROOT / "data" / "merkle_proof_613.md"
DEFAULT_PER_DIR = 2


def load_roots() -> dict:
    doc = mi.load_roots()
    if doc is None:
        raise SystemExit("[E3] 缺 Merkle 根台账（先跑 merkle_integrity build-all）")
    return doc


def sample_files(key: str, per_dir: int) -> list[Path]:
    """iter_files 返回 `[(相对路径, 绝对路径)]`（不是裸路径）⇒ 取绝对路径。"""
    rel, inc, exc = mi.dir_config(key)
    d = ROOT / rel
    if not d.is_dir():
        return []
    return [abs_p for _rel, abs_p in mi.iter_files(d, inc, exc)[:per_dir]]


def build_proofs(per_dir: int) -> list[dict]:
    doc = load_roots()
    rows = []
    for key, rec in (doc.get("dirs") or {}).items():
        if rec.get("missing") or not rec.get("root"):
            continue
        rel, inc, exc = mi.dir_config(key)
        d = ROOT / rel
        for fp in sample_files(key, per_dir):
            fp = Path(fp)
            if not fp.is_file():
                continue
            proof = mi.prove(d, fp, include=inc, exclude=exc)
            ok, msg = mi.verify(fp, proof, rec["root"])
            rows.append({"dir": key, "file": fp.relative_to(ROOT).as_posix(),
                         "steps": len(proof.get("steps", [])),
                         "root": rec["root"][:16] + "…", "verified": ok, "msg": msg})
    return rows


def render(rows: list[dict], doc: dict) -> str:
    n_ok = sum(1 for r in rows if r["verified"])
    L = ["# 613 · Merkle 包含证明（E3）", "",
         f"> 生成：`python tools/merkle_proof_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         "> 来源：`data/supply_chain/merkle_roots.json`（目录级 Merkle 根）+ "
         "`merkle_integrity.prove/verify`。", "",
         "## 一、总览", "",
         "| 项 | 值 |", "|---|---|",
         f"| 证明条数 | {len(rows)} |",
         f"| 验证通过 | **{n_ok}** |",
         f"| 验证失败 | {len(rows) - n_ok} |",
         f"| 覆盖目录 | {', '.join((doc.get('dirs') or {}).keys())} |", "",
         "## 二、逐条证明", "",
         "| 目录 | 文件 | 证明步数 | 根（前16） | 验证 |", "|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['dir']} | `{r['file']}` | {r['steps']} | `{r['root']}` "
                 f"| {'✅' if r['verified'] else '❌ ' + r['msg']} |")
    L += ["", "## 三、证明能做/不能做什么", "",
          "- ✅ 能证明：**该文件（含其相对路径）确实被计入该目录的 Merkle 根**。",
          "- ❌ 不能证明：文件内容「正确」、或该根在某个时刻已存在（后者需 E1 的 OTS 上链，"
          "而 E1 当前 attestation 仍 pending）。",
          "- 叶 hash 绑定相对路径 ⇒ 无法把 A 文件的证明套到 B 文件上。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 E3 · Merkle 包含证明")
    ap.add_argument("--per-dir", type=int, default=DEFAULT_PER_DIR)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        errs = []
        doc = mi.load_roots()
        if doc is None:
            errs.append("缺 Merkle 根台账")
        else:
            rows = build_proofs(1)
            if not rows:
                errs.append("未能生成任何证明")
            bad = [r for r in rows if not r["verified"]]
            if bad:
                errs.append(f"{len(bad)} 条证明验证失败：{bad[0]['file']} {bad[0]['msg']}")
            page = render(rows, doc)
            if "Merkle 包含证明" not in page:
                errs.append("报告渲染异常")
        for e in errs:
            print(f"[E3] ✗ {e}")
        print("[E3] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    doc = load_roots()
    rows = build_proofs(a.per_dir)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(rows, doc), encoding="utf-8", newline="\n")
    n_ok = sum(1 for r in rows if r["verified"])
    print(f"[E3] 写入 {OUT.relative_to(ROOT).as_posix()}（{len(rows)} 条证明 / 通过 {n_ok}）")
    return 0 if n_ok == len(rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
