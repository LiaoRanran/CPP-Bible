#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
597 探针：Merkle 树 / 哈希链 数据完整性（方向 6 可信计算 / 方向 9 数据完整性）
纯标准库，只读。遍历 atoms/ 与 misconceptions/ 的 .md，构建 Merkle 树与哈希链，
验证 (a) 根哈希可代表整个数据集、(b) 单文件篡改能被检测。
输出：本探针报告 JSON（写入 _arch_v15/probes/，属调研产出，非仓库正式文件）。
"""
import hashlib, json, sys
from pathlib import Path

ROOT = Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible")
OUT  = Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible\_arch_v15\probes")

def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def merkle_root(leaves):
    """自底向上两两哈希；奇数个时复制最后一个。返回根哈希与树高。"""
    if not leaves:
        return sha(b""), 0
    cur = list(leaves)
    h = 0
    while len(cur) > 1:
        if len(cur) % 2:
            cur.append(cur[-1])
        cur = [sha(cur[i].encode() + cur[i+1].encode()) for i in range(0, len(cur), 2)]
        h += 1
    return cur[0], h

def main():
    targets = []
    for pat in ("atoms/**/*.md", "misconceptions/**/*.md"):
        targets += sorted(ROOT.glob(pat))
    targets = [p for p in targets if p.is_file()]
    # 跳过不存在的目录（纯只读，不报错）
    leaves, chain_files, chain_prev = [], [], "0"*64
    for p in targets:
        data = p.read_bytes()
        h = sha(data)
        leaves.append(h)
        chain_files.append({"file": str(p.relative_to(ROOT)), "hash": h,
                            "prev": chain_prev, "selfchain": sha((chain_prev + h).encode())})
        chain_prev = chain_files[-1]["selfchain"]
    root, height = merkle_root(leaves)
    # 篡改检测：把第一个文件读入内存改一个字节，重算其叶，看根是否变
    tampered_leaves = list(leaves)
    first = targets[0].read_bytes()
    tampered = first[:-1] + bytes([first[-1] ^ 0x01])
    tampered_leaves[0] = sha(tampered)
    tampered_root, _ = merkle_root(tampered_leaves)
    # 哈希链尾部
    chain_tail = chain_files[-1]["selfchain"] if chain_files else "0"*64

    report = {
        "tool": "probe_merkle_integrity.py", "mode": "read-only",
        "scanned": len(targets),
        "merkle_root": root, "merkle_height": height,
        "chain_tail": chain_tail,
        "tamper_detected": root != tampered_root,
        "tamper_example_file": str(targets[0].relative_to(ROOT)),
        "feasibility": "纯标准库即可实现；无需硬件/外部服务。可立即作为 tool_integrity 的增强层。",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "merkle_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
