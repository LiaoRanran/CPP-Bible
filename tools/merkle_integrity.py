#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merkle_integrity.py — 目录级 Merkle 完整性层（601 任务1；600 调研阶段1，性价比最高的一层）。

为什么：`tool_integrity` 钉的是**几个文件**的 hash；600 调研指出 585 攻击1 的真盲点是
"信任根数据不在覆盖范围内"。Merkle 树把**整个目录**压成一个根 hash：
  * 目录里任何一个字节变化 ⇒ 根变 ⇒ 一行命令可复现地检出；
  * 可对**单个文件**出**对数规模**证明（`prove`/`verify`），不必把整棵树给别人；
  * 是后续阶段（in-toto layout / OpenTimestamps）的信任根输入。

哈希口径（**本工具自定义**，`ALGO` 标记，写进台账便于将来换代）：
  * 叶 = `sha256(b"\\x00" + 相对路径 + b"\\x00" + 文件内容)` —— **路径绑定**：只绑内容的话，
    把 A 的内容搬到同名位置/互相换名可以骗过根（内容集合没变），绑路径后不可；
  * 内节点 = `sha256(b"\\x01" + u64(左子树叶数) + u64(右子树叶数) + 左hash + 右hash)`
    —— **子树规模绑定**：否则"3 叶的树"和"4 叶的树"可能同根（形状歧义），绑了规模即不可；
  * 奇数个节点 ⇒ 末位**提升**到上一层（不做"复制末位"，那会引入 CVE-2012-2459 类歧义）；
  * **空目录** ⇒ 根 = `sha256(b"")`（明确定义，见 EMPTY_ROOT）。

纪律：纯标准库；**只读**被覆盖目录（唯一写动作是 `--output` 台账 / 证明文件）；
幂等（同输入 ⇒ 同根，`generated_at` 默认 null，打点走 `--now`）；大文件分块读；不许裸 `except Exception`。

覆盖目录（任务书 601 任务1.1；避免易变产物：忽略 `.exe/.log/.bak` 这些 gitignore 掉的生成物；
`data/mutation` 只盖 `full_baseline_v*.json` —— 该目录还有一堆未跟踪的临时探针 JSON）：
  atoms · evidence · Examples · Book · data/mutation（仅 full_baseline_v*.json）

用法：
    python tools/merkle_integrity.py build <dir> [--output PATH] [--now ISO]
    python tools/merkle_integrity.py build-all [--output data/supply_chain/merkle_roots.json] [--now ISO]
    python tools/merkle_integrity.py prove <dir> <file> [--output PATH]
    python tools/merkle_integrity.py verify <file> <proof.json> <root_hash>
    python tools/merkle_integrity.py consistency --old OLD.json --new NEW.json [--output PATH]
    python tools/merkle_integrity.py stats [dir] [--json]
    python tools/merkle_integrity.py --check          # 全部已存根 vs 当前目录（exit 0/1/2）
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = "1.0"
ALGO = "sha256-path-bound-count-bound-v1"
ROOTS_PATH = ROOT / "data" / "supply_chain" / "merkle_roots.json"
EMPTY_ROOT = hashlib.sha256(b"").hexdigest()      # 空目录的根（明确定义，不是"未定义"）
CHUNK = 1 << 20                                    # 分块读取（1 MiB）
_LEAF_PREFIX = b"\x00"
_NODE_PREFIX = b"\x01"
#: 覆盖目录：`(台账键, 目录, include, exclude)`。include/exclude 都是相对路径的 glob。
COVERED_DIRS: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
    ("atoms", "atoms", "**/*", ()),
    ("evidence", "evidence", "**/*", ()),
    ("Examples", "Examples", "**/*", ("**/*.exe", "**/*.log", "**/*.bak")),
    ("Book", "Book", "**/*", ()),
    ("mutation_baselines", "data/mutation", "full_baseline_v*.json", ()),
)


# ── 基础原语 ───────────────────────────────────────────────────────────────────
def _u64(n: int) -> bytes:
    return int(n).to_bytes(8, "big")


def leaf_hash(rel_path: str, file_path: Path) -> str:
    """叶节点 hash：`sha256(0x00 || rel_path || 0x00 || content)`（分块读，路径绑定）。"""
    h = hashlib.sha256()
    h.update(_LEAF_PREFIX)
    h.update(rel_path.encode("utf-8"))
    h.update(b"\x00")
    with Path(file_path).open("rb") as f:
        while True:
            buf = f.read(CHUNK)
            if not buf:
                break
            h.update(buf)
    return h.hexdigest()


def _node_hash(left: tuple[str, int], right: tuple[str, int]) -> tuple[str, int]:
    """内节点：`sha256(0x01 || u64(左叶数) || u64(右叶数) || 左 || 右)`，返回 (hash, 叶数)。"""
    h = hashlib.sha256()
    h.update(_NODE_PREFIX)
    h.update(_u64(left[1]))
    h.update(_u64(right[1]))
    h.update(bytes.fromhex(left[0]))
    h.update(bytes.fromhex(right[0]))
    return h.hexdigest(), left[1] + right[1]


def match_glob(rel: str, pattern: str) -> bool:
    """glob 匹配（相对路径 + 退到**文件名**匹配）。

    为什么要这层包装：`fnmatch` 的 `*` 跨 `/`、但 `**/*` 的正则**要求路径里有 `/`**
    ⇒ 顶层文件（`Examples/foo.cpp` 的 rel 是 `foo.cpp`）会被 `**/*` 漏掉（601 实测踩到：
    Examples 只盖了 120/1552）。这里把 `**/x` 显式展开为"x 或 任意目录/x"。
    """
    if pattern in ("**/*", "*", ""):
        return True
    if pattern.startswith("**/"):
        return match_glob(rel, pattern[3:])
    return fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(Path(rel).name, pattern)


def iter_files(directory: Path | str, include: str = "**/*",
               exclude: tuple[str, ...] = ()) -> list[tuple[str, Path]]:
    """目录内的文件 ⇒ `[(相对路径 posix, 绝对路径)]`，按相对路径**字典序**排序（跨平台一致）。"""
    d = Path(directory)
    out: list[tuple[str, Path]] = []
    for p in d.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(d).as_posix()
        if not match_glob(rel, include):
            continue
        if any(match_glob(rel, pat) for pat in exclude):
            continue
        out.append((rel, p))
    out.sort(key=lambda t: t[0])
    return out


# ── 建树 ───────────────────────────────────────────────────────────────────────
def build_tree(directory: Path | str, *, include: str = "**/*",
               exclude: tuple[str, ...] = ()) -> dict:
    """构建目录 Merkle 树 ⇒ `{root, file_count, tree_height, leaves[{path, hash}]}`。

    `tree_height` = 从叶到根的层数（1 个文件 ⇒ 0；空目录 ⇒ 0）。空目录 root = `EMPTY_ROOT`。
    """
    d = Path(directory)
    files = iter_files(d, include, exclude)
    leaves = [{"path": rel, "hash": leaf_hash(rel, p)} for rel, p in files]
    if not leaves:
        return {"root": EMPTY_ROOT, "file_count": 0, "tree_height": 0, "leaves": []}
    cur: list[tuple[str, int]] = [(lf["hash"], 1) for lf in leaves]
    height = 0
    while len(cur) > 1:
        nxt: list[tuple[str, int]] = []
        for i in range(0, len(cur), 2):
            if i + 1 < len(cur):
                nxt.append(_node_hash(cur[i], cur[i + 1]))
            else:
                nxt.append(cur[i])               # 末位**提升**（不复制 ⇒ 无歧义）
        cur = nxt
        height += 1
    return {"root": cur[0][0], "file_count": len(leaves), "tree_height": height,
            "leaves": leaves}


def dir_config(name: str) -> tuple[str, str, tuple[str, ...]]:
    for key, path, inc, exc in COVERED_DIRS:
        if key == name:
            return path, inc, exc
    raise KeyError(f"未配置的覆盖目录：{name}")


def build_all(out: Path | str = ROOTS_PATH, *, now: str | None = None,
              names: tuple[str, ...] | None = None) -> dict:
    """构建全部覆盖目录的根 ⇒ 台账 dict（**不含**时间戳除 `generated_at`）。"""
    doc: dict = {"algo": ALGO, "tool": "merkle_integrity", "version": VERSION,
                 "generated_at": now, "dirs": {}}
    for key, rel, inc, exc in COVERED_DIRS:
        if names is not None and key not in names:
            continue
        d = ROOT / rel
        if not d.is_dir():
            doc["dirs"][key] = {"path": rel, "missing": True}
            continue
        tree = build_tree(d, include=inc, exclude=exc)
        doc["dirs"][key] = {"path": rel, "root": tree["root"],
                            "file_count": tree["file_count"],
                            "tree_height": tree["tree_height"],
                            "generated_at": now}
    return doc


def load_roots(path: Path | str = ROOTS_PATH) -> dict | None:
    p = Path(path)
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def check_all(roots_path: Path | str = ROOTS_PATH) -> tuple[list[str], list[str], int]:
    """已存根 vs 当前目录；返回 (problems, skipped, exit_code)（缺台账 ⇒ exit 2）。"""
    doc = load_roots(roots_path)
    if doc is None:
        return [], [f"缺台账 {_rel(roots_path)}（先跑 build-all）"], 2
    problems: list[str] = []
    skipped: list[str] = []
    for key, rec in sorted((doc.get("dirs") or {}).items()):
        if rec.get("missing"):
            skipped.append(f"{key}：目录不存在 ⇒ 跳过")
            continue
        try:
            rel, inc, exc = dir_config(key)
        except KeyError:
            skipped.append(f"{key}：不在当前 COVERED_DIRS 配置里 ⇒ 跳过（台账比配置新？）")
            continue
        d = ROOT / rel
        if not d.is_dir():
            skipped.append(f"{key}：目录 {rel} 不存在 ⇒ 跳过")
            continue
        tree = build_tree(d, include=inc, exclude=exc)
        if tree["root"] != rec.get("root"):
            problems.append(f"{key}（{rel}）：根不匹配（台账 {str(rec.get('root'))[:12]}… "
                            f"实际 {tree['root'][:12]}…，文件数 {rec.get('file_count')} → "
                            f"{tree['file_count']}）")
    return problems, skipped, (1 if problems else 0)


# ── 证明 ───────────────────────────────────────────────────────────────────────
def rel_in_tree(directory: Path | str, file_path: Path | str) -> str:
    """把 `file_path` 归一到"相对 `directory` 的 posix 路径"。

    同时接受三种写法：① 相对 `directory`（`mem/x.md`）② 相对仓库根/当前目录（`atoms/mem/x.md`）
    ③ 绝对路径 —— 人命令行怎么方便怎么写，工具负责归一。
    """
    d = Path(directory)
    for cand in (Path(file_path), d / Path(file_path)):
        try:
            return cand.resolve().relative_to(d.resolve()).as_posix()
        except (ValueError, OSError):
            continue
    raise FileNotFoundError(f"{file_path} 不在 {directory} 下")


def prove(directory: Path | str, file_path: Path | str, *, include: str = "**/*",
          exclude: tuple[str, ...] = ()) -> dict:
    """生成"某文件在树中"的证明（沿路的兄弟节点 + 方向 + 叶数）。

    叶 hash 绑了**相对 `directory` 的路径** ⇒ 证明自带"文件属于哪个路径"的绑定。
    """
    d = Path(directory)
    rel = rel_in_tree(d, file_path)
    files = iter_files(d, include, exclude)
    idx = next((i for i, (r, _p) in enumerate(files) if r == rel), None)
    if idx is None:
        raise FileNotFoundError(f"{rel} 不在 {d} 的覆盖范围内（include={include}）")
    cur: list[tuple[str, int]] = [(leaf_hash(r, p), 1) for r, p in files]
    leaf = {"path": rel, "hash": cur[idx][0]}
    steps: list[dict] = []
    pos = idx
    while len(cur) > 1:
        sib = pos + 1 if pos % 2 == 0 else pos - 1
        if sib >= len(cur):
            steps.append({"side": "promoted", "hash": None, "count": None})   # 末位提升
        else:
            steps.append({"side": "right" if sib > pos else "left",
                          "hash": cur[sib][0], "count": cur[sib][1]})
        nxt: list[tuple[str, int]] = []
        for i in range(0, len(cur), 2):
            nxt.append(_node_hash(cur[i], cur[i + 1]) if i + 1 < len(cur) else cur[i])
        pos //= 2                                # 折叠后本节点在上一层的下标
        cur = nxt
    return {"algo": ALGO, "root": cur[0][0], "leaf": leaf, "leaf_count": len(files),
            "tree_height": len(steps), "steps": steps}


def verify(file_path: Path | str, proof: dict, root_hash: str) -> tuple[bool, str]:
    """验证"文件在树中"：重算叶 hash（用证明里的相对路径 + 文件内容）⇒ 沿 steps 折到根。"""
    if not isinstance(proof, dict) or "leaf" not in proof or "steps" not in proof:
        return False, "证明格式不对（缺 leaf/steps）"
    if proof.get("algo") != ALGO:
        return False, f"证明算法标记不符：{proof.get('algo')!r} ≠ {ALGO!r}"
    rel = str(proof["leaf"].get("path") or "")
    h = leaf_hash(rel, Path(file_path))
    if h != proof["leaf"].get("hash"):
        return False, f"叶 hash 不匹配：文件内容≠证明（期望 {str(proof['leaf'].get('hash'))[:12]}… 实际 {h[:12]}…）"
    node = (h, 1)
    for i, st in enumerate(proof["steps"], 1):
        side = st.get("side")
        if side == "promoted":
            continue                              # 提升层：本节点直接进上一层
        sib = (str(st.get("hash")), int(st.get("count") or 0))
        if side == "right":
            node = _node_hash(node, sib)
        elif side == "left":
            node = _node_hash(sib, node)
        else:
            return False, f"第 {i} 步方向非法：{side!r}"
    if node[0] != root_hash:
        return False, f"根 hash 不匹配（期望 {str(root_hash)[:12]}… 实际 {node[0][:12]}…）"
    return True, ""


# ── 一致性证明（append-only）───────────────────────────────────────────────────
def consistency_prove(old_tree: dict, new_tree: dict) -> dict:
    """两版一致性的**全叶集**证明：新树包含旧树的每个 (路径, 叶 hash)，且无删改。

    为什么不用 RFC 6962 的对数规模证明：本树的奇数层是**提升**（非完全二叉），RFC 6962 的
    递归定义不适用；全叶集证明在本项目规模（≤ 几千文件，几十 KB）下完全可接受，
    且验证只需 hash、不需要文件内容 ⇒ 仍然可以"只给证明不给文件"。
    """
    return {"algo": ALGO, "kind": "consistency-full-leafset",
            "old": {"root": old_tree.get("root"), "size": old_tree.get("file_count"),
                    "leaves": old_tree.get("leaves", [])},
            "new": {"root": new_tree.get("root"), "size": new_tree.get("file_count"),
                    "leaves": new_tree.get("leaves", [])},
            "removed": []}


def consistency_verify(proof: dict) -> tuple[bool, str]:
    """验证一致性：两版根各自可由其叶集重算；旧叶集 ⊂ 新叶集（同 hash）。"""
    if not isinstance(proof, dict) or proof.get("kind") != "consistency-full-leafset":
        return False, "不是本工具的一致性证明"
    old, new = proof.get("old") or {}, proof.get("new") or {}
    for tag, side in (("old", old), ("new", new)):
        tree = _tree_from_leaves(side.get("leaves") or [])
        if tree["root"] != side.get("root"):
            return False, f"{tag} 根与叶集不自洽（根 {str(side.get('root'))[:12]}… 实际 {tree['root'][:12]}…）"
        if tree["file_count"] != side.get("size"):
            return False, f"{tag} 文件数与叶集不符"
    new_map = {lf["path"]: lf["hash"] for lf in (new.get("leaves") or [])}
    lost = [lf["path"] for lf in (old.get("leaves") or [])
            if new_map.get(lf["path"]) != lf["hash"]]
    if lost:
        return False, f"旧版内容未被新版包含（被删/被改）：{lost[:5]}"
    if (new.get("size") or 0) < (old.get("size") or 0):
        return False, "新版文件数少于旧版 ⇒ 不是 append-only"
    return True, ""


def _tree_from_leaves(leaves: list[dict]) -> dict:
    """由**叶集**（path+hash）重算根（与 build_tree 的折叠规则逐字一致）。"""
    if not leaves:
        return {"root": EMPTY_ROOT, "file_count": 0, "tree_height": 0}
    cur: list[tuple[str, int]] = [(str(lf["hash"]), 1) for lf in leaves]
    height = 0
    while len(cur) > 1:
        nxt: list[tuple[str, int]] = []
        for i in range(0, len(cur), 2):
            nxt.append(_node_hash(cur[i], cur[i + 1]) if i + 1 < len(cur) else cur[i])
        cur = nxt
        height += 1
    return {"root": cur[0][0], "file_count": len(leaves), "tree_height": height}


def _rel(p: Path | str) -> str:
    try:
        return Path(p).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(p).as_posix()


def _tree_summary(directory: Path | str, *, include: str = "**/*",
                  exclude: tuple[str, ...] = ()) -> dict:
    t = build_tree(directory, include=include, exclude=exclude)
    return {"path": _rel(directory), "root": t["root"], "file_count": t["file_count"],
            "tree_height": t["tree_height"]}


# ── CLI ────────────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="目录级 Merkle 完整性层（只读；证明可单独验证）")
    ap.add_argument("--check", action="store_true", help="全部已存根 vs 当前目录（exit 0/1/2）")
    ap.add_argument("--roots", default=str(ROOTS_PATH))
    sub = ap.add_subparsers(dest="cmd")

    b = sub.add_parser("build")
    b.add_argument("directory")
    b.add_argument("--output", default=None)
    b.add_argument("--now", default=None)
    b.add_argument("--include", default="**/*")
    b.add_argument("--json", action="store_true")

    ba = sub.add_parser("build-all")
    ba.add_argument("--output", default=str(ROOTS_PATH))
    ba.add_argument("--now", default=None)

    p = sub.add_parser("prove")
    p.add_argument("directory")
    p.add_argument("file")
    p.add_argument("--output", default=None)

    v = sub.add_parser("verify")
    v.add_argument("file")
    v.add_argument("proof")
    v.add_argument("root")

    c = sub.add_parser("consistency")
    c.add_argument("--old", required=True)
    c.add_argument("--new", required=True)
    c.add_argument("--output", default=None)

    s = sub.add_parser("stats")
    s.add_argument("directory", nargs="?")
    s.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        problems, skipped, code = check_all(a.roots)
        for x in skipped:
            print(f"[merkle] ⚠ {x}")
        for x in problems:
            print(f"[merkle] ❌ {x}")
        if code == 0:
            doc = load_roots(a.roots) or {}
            print(f"[merkle] OK：{len(doc.get('dirs') or {})} 个目录的根与当前内容一致"
                  f"（algo={doc.get('algo')}，警告 {len(skipped)} 条）")
        return code

    if a.cmd == "build":
        tree = build_tree(a.directory, include=a.include)
        rec = {"path": _rel(a.directory), "root": tree["root"],
               "file_count": tree["file_count"], "tree_height": tree["tree_height"],
               "algo": ALGO, "generated_at": a.now}
        if a.output:
            out = Path(a.output)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({"algo": ALGO, "generated_at": a.now, **tree},
                                      ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"[merkle] 已写 {a.output}（root {tree['root'][:12]}…，"
                  f"{tree['file_count']} 文件，高 {tree['tree_height']}）")
        elif a.json:
            print(json.dumps(rec, ensure_ascii=False, indent=1))
        else:
            print(f"[merkle] {rec['path']}：root {tree['root']} · 文件 {tree['file_count']} · "
                  f"树高 {tree['tree_height']}")
        return 0

    if a.cmd == "build-all":
        doc = build_all(a.output, now=a.now)
        out = Path(a.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"[merkle] 已写 {a.output}：{len(doc['dirs'])} 个目录")
        for k, v2 in sorted(doc["dirs"].items()):
            print(f"  - {k}: root {str(v2.get('root'))[:12]}… · 文件 {v2.get('file_count')} · "
                  f"高 {v2.get('tree_height')}")
        return 0

    if a.cmd == "prove":
        proof = prove(a.directory, a.file)
        text = json.dumps(proof, ensure_ascii=False, indent=1)
        if a.output:
            Path(a.output).write_text(text + "\n", encoding="utf-8", newline="\n")
            print(f"[merkle] 证明已写 {a.output}（root {proof['root'][:12]}…，"
                  f"{len(proof['steps'])} 步）")
        else:
            print(text)
        return 0

    if a.cmd == "verify":
        proof = json.loads(Path(a.proof).read_text(encoding="utf-8"))
        ok, why = verify(a.file, proof, a.root)
        print(f"[merkle] {'✓ 验证通过' if ok else '❌ ' + why}")
        return 0 if ok else 1

    if a.cmd == "consistency":
        old = json.loads(Path(a.old).read_text(encoding="utf-8"))
        new = json.loads(Path(a.new).read_text(encoding="utf-8"))
        proof = consistency_prove(old, new)
        ok, why = consistency_verify(proof)
        text = json.dumps(proof, ensure_ascii=False, indent=1)
        if a.output:
            Path(a.output).write_text(text + "\n", encoding="utf-8", newline="\n")
        if not ok:
            print(f"[merkle] ❌ {why}", file=sys.stderr)
            return 1
        print(f"[merkle] ✓ 一致性成立：旧 {proof['old']['size']} → 新 {proof['new']['size']} 文件"
              f"（旧叶集全部被新版包含）")
        return 0

    if a.cmd == "stats":
        if a.directory:
            print(json.dumps(_tree_summary(a.directory), ensure_ascii=False, indent=1))
            return 0
        doc = load_roots(a.roots)
        if doc is None:
            print(f"[merkle] ❌ 缺台账 {a.roots}（先跑 build-all）", file=sys.stderr)
            return 2
        if a.json:
            print(json.dumps(doc, ensure_ascii=False, indent=1))
            return 0
        print(f"[merkle] 台账 {_rel(a.roots)}（algo={doc.get('algo')}）")
        for k, rec in sorted((doc.get("dirs") or {}).items()):
            print(f"  - {k}: {rec.get('path')} · root {str(rec.get('root'))[:16]}… · "
                  f"文件 {rec.get('file_count')} · 高 {rec.get('tree_height')}")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
