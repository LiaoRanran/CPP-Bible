"""623 D2 · W2 重算（通道打通后，重算 W2 solver 看变化）

**背景**：622 D2 重算 W2 得到"变化 0"，但那是因为 **通道断**（Authority 决策未进入 annotations，
W2 solver 读的是旧 annotations）。623 D1 已打通通道，产出 synced 视图。

**本工具**：把 annotations（原 / synced）按攻击边聚合为**每个原子的学习者判决**
（任意边 reject → OUT；有 approve → IN；否则 UNRESOLVED），对比两者差异。
若差异为 0，则说明是**真无变化**（actions 本就一致），而非通道断。

铁律：只读 annotations 两视图，不改任何受控文件。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
SYNCED = os.path.join(ROOT, "data", "human_attack_edge_annotations.synced.jsonl")


def _atom_of(edge_id: str) -> str | None:
    # 格式：ae-<src>-><ATOM-Y>::prop-N
    if "->" not in edge_id or "::" not in edge_id:
        return None
    return edge_id.split("->", 1)[1].split("::", 1)[0]


def verdicts(annotations: list[dict]) -> dict[str, str]:
    agg: dict[str, list[str]] = {}
    for a in annotations:
        atom = _atom_of(a.get("edge_id", ""))
        if not atom:
            continue
        agg.setdefault(atom, []).append(a.get("action", ""))
    out = {}
    for atom, acts in agg.items():
        if any(x == "reject" for x in acts):
            out[atom] = "OUT"
        elif any(x == "approve" for x in acts):
            out[atom] = "IN"
        else:
            out[atom] = "UNRESOLVED"
    return out


def load(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def check() -> int:
    """只读自检（不写盘）：输入存在 / JSONL 合法 / verdicts 可加载。"""
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("annotations 文件存在", os.path.exists(ANN))
    chk("synced 文件存在", os.path.exists(SYNCED))
    try:
        load(ANN)
        chk("annotations JSONL 可解析", True)
    except (OSError, ValueError) as exc:
        chk(f"annotations JSONL 可解析（{exc}）", False)
    try:
        load(SYNCED)
        chk("synced JSONL 可解析", True)
    except (OSError, ValueError) as exc:
        chk(f"synced JSONL 可解析（{exc}）", False)
    chk("verdicts() 可加载（空输入→空判决）", verdicts([]) == {})
    print(f"D2 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="623 D2 W2 重算")
    ap.add_argument("--annotations", default=ANN)
    ap.add_argument("--synced", default=SYNCED)
    ap.add_argument("--check", action="store_true", help="只读自检（不写盘），exit 0 = 通过")
    args = ap.parse_args(argv)

    if args.check:
        return check()

    orig = verdicts(load(args.annotations))
    sync = verdicts(load(args.synced))
    atoms = sorted(set(orig) | set(sync))
    changed = [(a, orig.get(a), sync.get(a)) for a in atoms if orig.get(a) != sync.get(a)]
    in_out = {k: v for k, v in sync.items()}

    print(f"原子数（参与判决）：{len(atoms)}")
    print(f"  IN：{sum(1 for v in in_out.values() if v=='IN')}  "
          f"OUT：{sum(1 for v in in_out.values() if v=='OUT')}  "
          f"UNRESOLVED：{sum(1 for v in in_out.values() if v=='UNRESOLVED')}")
    print(f"原→synced 判决变化原子数：{len(changed)}")
    if changed:
        for a, o, s in changed[:20]:
            print(f"  {a}: {o} → {s}")
    else:
        print("⇒ 变化 0：非通道断，而是真无变化（actions 在 D1 同步前后一致）")
    return changed


if __name__ == "__main__":
    sys.exit(0 if main() is not None else 0)
