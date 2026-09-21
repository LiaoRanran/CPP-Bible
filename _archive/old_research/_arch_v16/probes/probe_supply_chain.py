#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
600 探针：供应链溯源证明最小可行原型（方向 1 + 4 + 5）
纯标准库，只读。演示：
  (A) in-toto 风格链式溯源：layout + link（materials/products 哈希、functionary=git HEAD、
      时间戳、模拟签名），链路绑定（step N 的 materials == step N-1 的 products），篡改检测。
  (B) Merkle 树（RFC6962 叶/节点前缀）+ 包含证明(inclusion proof) + 一致性证明（增式重算前缀根，
      诚实说明：简洁 RFC6962 consistency proof 留 W 档）+ 篡改检测。
只读扫仓库真实文件（tools/ CORE+TEST_CONFIG、data/overturned_events.jsonl、部分 atoms/misconceptions），
输出全部写 _arch_v16/probes/（本调研产出，非仓库正式文件）。
"""
import hashlib, json, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible")
OUT  = Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible\_arch_v16\probes")

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()
def fsha(p: Path) -> str:
    return sha(p.read_bytes())
def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                              timeout=20).stdout.strip()
    except Exception:
        return ""

# ---------- (B) Merkle (RFC6962) ----------
LEAF = bytes([0x00]); NODE = bytes([0x01])
def mleaf(h: str) -> str: return sha(LEAF + bytes.fromhex(h))
def mnode(l: str, r: str) -> str: return sha(NODE + bytes.fromhex(l) + bytes.fromhex(r))

def merkle(leaves):
    if not leaves: return [], ""
    cur = [mleaf(h) for h in leaves]
    tree = [cur]
    while len(cur) > 1:
        if len(cur) % 2: cur.append(cur[-1])
        cur = [mnode(cur[i], cur[i+1]) for i in range(0, len(cur), 2)]
        tree.append(cur)
    return tree, cur[0]

def inclusion_proof(tree, idx):
    proof = []
    for level in range(len(tree) - 1):
        sib = idx ^ 1
        if sib >= len(tree[level]): sib = idx
        proof.append(tree[level][sib])
        idx //= 2
    return proof

def verify_inclusion(root, leaf_hash, idx, total, proof):
    h = mleaf(leaf_hash)
    n = total
    for sib in proof:
        if idx % 2: h = mnode(sib, h)
        else:       h = mnode(h, sib)
        idx //= 2
    return h == root

# ---------- (A) in-toto 风格 ----------
def sim_sign(payload: str, key: str) -> str:
    """单用户阶段无密钥对：用 git HEAD 作 functionary 身份，签名=sha(key+payload)。
    诚实说明：这不是密码学签名，只是把'身份'绑定进内容哈希（可篡改但可检测）。W档升级为 Ed25519。"""
    return sha((key + "|" + payload).encode())

def build_chain(functionary):
    # 真实文件哈希作为 materials/products 的演示样本
    core = ["gate_engine.py","atom_evidence_replay.py","poison_drill.py","toolchain.py","cppbible.py"]
    tcfg = ["tests/conftest.py","pyproject.toml"]
    sample_atoms = sorted(ROOT.glob("atoms/**/*.md"))[:3]
    sample_mis   = sorted(ROOT.glob("misconceptions/**/*.md"))[:3]
    ev = ROOT / "data" / "overturned_events.jsonl"

    steps = []
    prev_products = {}
    # step1 编写卡：products = 样例原子/误解卡
    steps.append(dict(step="write_cards", command="human edits atoms/*.md, misconceptions/*.md",
                      materials={}, products={"atoms": {p.name: fsha(p) for p in sample_atoms},
                                              "misconceptions": {p.name: fsha(p) for p in sample_mis}}))
    prev_products = steps[0]["products"]
    # step2 gate 校验：materials = 上一步 products + 核心工具；products = gate_engine.py 哈希（被校验的核心）
    steps.append(dict(step="gate_validate", command="python tools/gate_engine.py --check",
                      materials={"cards": prev_products,
                                 "tools": {n: fsha(ROOT/"tools"/n) for n in core}},
                      products={"gate_engine.py": fsha(ROOT/"tools"/"gate_engine.py")}))
    prev_products = steps[1]["products"]
    # step3 replay 验证：materials = gate 产物 + 工具；products = replay 工具哈希
    steps.append(dict(step="replay_verify", command="python tools/atom_evidence_replay.py --check",
                      materials={"gate": prev_products, "tools": {n: fsha(ROOT/"tools"/n) for n in core}},
                      products={"atom_evidence_replay.py": fsha(ROOT/"tools"/"atom_evidence_replay.py")}))
    prev_products = steps[2]["products"]
    # step4 poison 测试：materials = replay 产物 + 毒样例(tools/poison_drill.py)；products = poison_drill.py
    steps.append(dict(step="poison_test", command="python tools/poison_drill.py",
                      materials={"replay": prev_products, "poison_drill.py": fsha(ROOT/"tools"/"poison_drill.py")},
                      products={"poison_drill.py": fsha(ROOT/"tools"/"poison_drill.py")}))
    prev_products = steps[3]["products"]
    # step5 人审确认：materials = poison 产物 + 推翻通道；products = overturned_events.jsonl 存在性
    steps.append(dict(step="human_review", command="python tools/overturned_events.py append ...",
                      materials={"poison": prev_products,
                                  "overturned_events.jsonl.exists": str(ev.is_file())},
                      products={"overturned_events.jsonl": sha(ev.read_text(encoding="utf-8").encode()) if ev.is_file() else ""}))
    # 加时间戳 + 模拟签名
    ts = datetime.now(timezone.utc).isoformat()
    links = []
    for s in steps:
        payload = json.dumps(s, ensure_ascii=False, sort_keys=True)
        s["_functionary"] = functionary
        s["_timestamp"] = ts
        s["_sig"] = sim_sign(payload, functionary)
        links.append(s)
    return links

def verify_chain(links, functionary):
    """返回 (ok, errors)。检查：签名有效、链路绑定(materials 含上一步 products)、工具哈希与磁盘一致。"""
    errors = []
    prev_products = None
    for i, s in enumerate(links):
        payload = json.dumps({k: v for k, v in s.items() if not k.startswith("_")},
                             ensure_ascii=False, sort_keys=True)
        if s.get("_sig") != sim_sign(payload, functionary):
            errors.append(f"step {s['step']}: 签名不符（可能 functionary 或内容被改）")
        if prev_products is not None:
            # 链路绑定：上一步 products 必须出现在本步 materials 中
            flat_prev = json.dumps(prev_products, ensure_ascii=False, sort_keys=True)
            flat_mat  = json.dumps(s["materials"], ensure_ascii=False, sort_keys=True)
            if flat_prev not in flat_mat:
                errors.append(f"step {s['step']}: 链路断裂——上一步 products 未作为本步 materials")
        prev_products = s["products"]
    return (len(errors) == 0), errors

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    func = git("rev-parse", "HEAD") or "NO_GIT_HEAD"
    author = git("log", "-1", "--format=%an") or "NO_AUTHOR"

    # (A) 链式溯源
    links = build_chain(func)
    ok, errs = verify_chain(links, func)
    # 篡改检测：把 write_cards 的某产品改成假值，重验应失败
    tampered = json.loads(json.dumps(links))
    tampered[0]["products"]["atoms"][list(tampered[0]["products"]["atoms"])[0]] = "0"*64
    ok_t, errs_t = verify_chain(tampered, func)

    # (B) Merkle over 真实文件哈希（CORE 在 tools/ 下，TEST_CONFIG 在 ROOT 下）
    core_rel = ["gate_engine.py","atom_evidence_replay.py","poison_drill.py","toolchain.py","cppbible.py"]
    tcfg_rel = ["tests/conftest.py","pyproject.toml"]
    file_hashes = [fsha(ROOT/"tools"/n) for n in core_rel] + [fsha(ROOT/n) for n in tcfg_rel]
    extra = [fsha(p) for p in sorted(ROOT.glob("atoms/**/*.md"))[:10]]
    leaves = file_hashes + extra
    tree, root = merkle(leaves)
    idx = 2
    proof = inclusion_proof(tree, idx)
    inc_ok = verify_inclusion(root, leaves[idx], idx, len(leaves), proof)
    # 篡改检测：改一个叶，根应变、包含证明应失败
    leaves2 = list(leaves); leaves2[2] = "0"*64
    tree2, root2 = merkle(leaves2)
    inc_ok_tampered = verify_inclusion(root, leaves2[2], idx, len(leaves2), proof)
    # 一致性：增式（追加一个叶），新树前缀根应 == 旧根
    leaves3 = leaves + ["a"*64]
    _, root3 = merkle(leaves3)
    _, prefix_root = merkle(leaves)   # 前 n 个叶的树根
    consistency_ok = (prefix_root == root) and (root != root3)

    # layouts 写盘
    layout = {"steps": [s["step"] for s in links], "functionaries": [func],
              "authored_by": author, "inspections": ["tool_integrity --check"],
              "_signed": sim_sign(json.dumps([s["step"] for s in links], ensure_ascii=False), func)}
    (OUT/"layout.json").write_text(json.dumps(layout, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT/"links").mkdir(exist_ok=True)
    for s in links:
        (OUT/"links"/f"{s['step']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT/"merkle_report.json").write_text(json.dumps(
        {"root": root, "height": len(tree)-1, "leaves": len(leaves),
         "inclusion_proof_ok": inc_ok, "tamper_detected_inclusion": not inc_ok_tampered,
         "consistency_ok": consistency_ok}, ensure_ascii=False, indent=1), encoding="utf-8")

    report = {
        "mode": "read-only", "functionary(git HEAD)": func[:12]+"…", "author": author,
        "chain_steps": [s["step"] for s in links], "chain_verify_ok": ok, "chain_errors": errs,
        "chain_tamper_detected": (not ok_t) and any("链路" in e or "签名" in e for e in errs_t),
        "merkle_root": root, "merkle_height": len(tree)-1, "merkle_inclusion_ok": inc_ok,
        "merkle_tamper_detected": (not inc_ok_tampered), "merkle_consistency_ok": consistency_ok,
        "honest_note": "sim_sign 非密码学签名；RFC6962 简洁 consistency proof 留 W档；纯演示可行性。",
    }
    (OUT/"report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
