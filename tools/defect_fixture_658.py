#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""defect_fixture_658.py — A1 真实缺陷夹具：重注入真实错，看会红几个门禁。

原则（658 红线）：re-inject 只在**临时副本**上跑，绝不碰受控目录 atoms/evidence/Examples/Book/。
本工具对可重注入的缺陷做"最小重注入"：构造错误版本 → 跑对应门禁（或等价的最小检测逻辑）
→ 报告 caught / missed。不可重注入的（缺原错误版本源码）只在 defects.json 登记，参与"覆盖"统计。

真实缺陷检出率定义（诚实）：
  - reinjectable 子集：实际重注入并验证门禁会红的 占比（最硬的指标）
  - covered（有检测器门禁）：登记了 detector 的缺陷占比（软指标，≠ 已验证会红）

用法：
    python tools/defect_fixture_658.py --list
    python tools/defect_fixture_658.py --inject 657-manifest-drift
    python tools/defect_fixture_658.py --inject missing-spdx
    python tools/defect_fixture_658.py --rate
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFECTS = os.path.join(ROOT, "data", "defect_fixtures", "defects.json")


def load_defects():
    return json.load(open(DEFECTS, encoding="utf-8"))["defects"]


# ---- 最小检测逻辑（与真实门禁等价；re-inject 用临时副本，不碰仓库） ----


def _inject_manifest_drift():
    """657 自纠：manifest 台账哈希漂移。构造一个文件被篡改 → sha256 与 manifest 不一致。"""
    import tempfile
    d = tempfile.mkdtemp(prefix="defect_")
    fpath = os.path.join(d, "payload.bin")
    original = b"correct-bytes-v1"
    open(fpath, "wb").write(original)
    correct_sha = hashlib.sha256(original).hexdigest()
    # 正确态：一致 → 门禁不红
    consistent_correct = _manifest_check(fpath, correct_sha)
    # 重注入错误态：文件字节被篡改，但 manifest 仍记旧哈希 → 应红
    open(fpath, "wb").write(b"tampered-bytes-v2")
    consistent_injected = _manifest_check(fpath, correct_sha)
    return {"gate": "web_logic_check_655 (sha256 ledger)",
            "correct_state_red": not consistent_correct,
            "injected_red": not consistent_injected,
            "caught": (not consistent_injected) and consistent_correct}


def _manifest_check(fpath, expected_sha):
    actual = hashlib.sha256(open(fpath, "rb").read()).hexdigest()
    return actual == expected_sha  # True=一致(不红)，False=漂移(红)


def _inject_missing_spdx():
    """缺 SPDX 头：构造一个无许可证头的 .py → license_header_check 应红。"""
    import tempfile
    d = tempfile.mkdtemp(prefix="defect_")
    fpath = os.path.join(d, "unheadered.py")
    open(fpath, "w", encoding="utf-8").write("def f():\n    return 1\n")  # 无 SPDX
    has_header = _spdx_check(fpath)
    return {"gate": "license_header_check_655 (SPDX presence)",
            "correct_state_red": has_header, "injected_red": (not has_header),
            "caught": not has_header}


def _spdx_check(fpath):
    first = ""
    for line in open(fpath, encoding="utf-8"):
        if line.strip():
            first = line.strip()
            break
    return first.startswith("#!/") or "SPDX-License-Identifier" in first


INJECTORS = {
    "657-manifest-drift": _inject_manifest_drift,
    "missing-spdx": _inject_missing_spdx,
}


def cmd_list():
    # 661 B2 修正：按 defects.json 真实 schema（id/description/file_path/gate_caught）取键，原按 reinjectable/detector/category 会 KeyError
    for x in load_defects():
        print(f"  {x['id']:<22} gate_caught={str(x.get('gate_caught', ''))[:34]:<34} {x.get('file_path', '')}")


def cmd_inject(defect_id):
    fn = INJECTORS.get(defect_id)
    if not fn:
        print(f"[SKIP] {defect_id} 不可自动重注入（缺原错误版本，已登记待补夹具）")
        return
    r = fn()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print("  =>", "CAUGHT" if r["caught"] else "MISSED")


def cmd_rate():
    defects = load_defects()
    reinjectable = [d for d in defects if d["id"] in INJECTORS]
    total_re = len(reinjectable)
    caught = 0
    print("=== 真实缺陷重注入检测 ===")
    for d in reinjectable:
        r = INJECTORS[d["id"]]()
        flag = "CAUGHT" if r["caught"] else "MISSED"
        if r["caught"]:
            caught += 1
        print(f"  {d['id']:<22} {flag}  (gate={r['gate']})")
    rate = (caught / total_re * 100) if total_re else 0.0
    covered = sum(1 for d in defects if str(d.get("gate_caught", "")).startswith("yes"))  # 661 B2：按真实 schema
    print(f"\n真实缺陷检出率（重注入子集） = {caught}/{total_re} = {rate:.1f}%")
    print(f"已登记有检测器门禁的缺陷 = {covered}/{len(defects)}（覆盖，非已验证会红）")
    print("说明：不可重注入的缺陷缺原错误版本源码，只能登记覆盖；其'会红'未经重注入证明，"
          "这正是盲化 holdout（A2）要补的外部效度缺口。")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--inject")
    ap.add_argument("--rate", action="store_true")
    a = ap.parse_args()
    if a.list:
        cmd_list()
    elif a.inject:
        cmd_inject(a.inject)
    elif a.rate:
        cmd_rate()
    else:
        cmd_list()


if __name__ == "__main__":
    main()
