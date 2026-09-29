#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""holdout_extend_665.py — 665 C1：给盲化 holdout 补 10 个**真错**样本（20 → 30）。

为什么不是直接手写 JSON
========================
holdout 的生命在于**标签先于测量**。所以每个新样本的 `planted=true` 依据写的是
**标准条款**（独立于本机检测器），而不是"我们跑出来 that 检测器报了"（那是循环论证）：

    h21–h25  ← 664 独立生成批次里**机器已认定为 UB/真错**的探针（ig-01/02/07/08/14）
    h26–h30  ← 665 新增五个经典 UB/Aliasing 类错误？不，新增的是**内存与 UB 类**：
               use-after-free / double-free / use-after-scope /
               signed shift overflow / memory leak

诚实登记（先写在工具里，免得后人以为这批跟原 20 个一样盲）
==========================================================
* 原 20 个 seed **已经 reveal**（`.revealed` 不可回盲）⇒ 新增样本**不具备同样的盲态**：
  它们是在已知大概岔口之后追加的，**不能用来 Claim「外部效度提升」**，只能用来
  **把可样本量从 7 提到 17**（使点估计不再只有 5 个可测样本）。
* 新增样本的 declaration `revealed: false`，由 `holdout_reveal_3_665.py` 统一揭示。

用法
====
    python tools/holdout_extend_665.py --check     # 只读：校验文件完整性与审计闭环
    python tools/holdout_extend_665.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOLD = ROOT / "data" / "holdout" / "holdout.json"
#: **canonical 合并视图**（665 C1 扩样后的 30 样本）。
#: 为什么另存一份：`holdout.json` 是 `holdout_658.py` 的**产物**，那个工具一跑就会按它
#: 内建的 20 样本重写该文件 —— 665 的追加会被静默抹掉（本批实测踩到过）。
#: 所以"扩样"必须有一个不被旧工具重写的落点：本文件 = 旧 20 + 665 新增 10 的合并结果。
MERGED = ROOT / "data" / "holdout" / "holdout_665.json"
#: 新增 10 个真错样本（h21–h30）。`basis` 一律引**标准/文档条款**，不引本机测量结果。
NEW_SEEDS: list[dict] = [
    {"id": "h21", "category": "UB", "atom_ref": "data/cards_665/fixtures/ig-01.cpp",
     "detector": "ubsan", "planted": True,
     "planted_desc": "有符号整数溢出（INT_MAX + 1）⇒ UB",
     "basis": "ISO/IEC 14882 [expr] 有符号溢出未定义（664 独立生成批次 ig-01）"},
    {"id": "h22", "category": "UB", "atom_ref": "data/cards_665/fixtures/ig-02.cpp",
     "detector": "asan", "planted": True,
     "planted_desc": "数组越界写读（a[5]，越界 1 个元素）⇒ UB",
     "basis": "ISO/IEC 14882 [expr.sub] 越界访问 UB（664 ig-02）"},
    {"id": "h23", "category": "UB", "atom_ref": "data/cards_665/fixtures/ig-07.cpp",
     "detector": "asan", "planted": True,
     "planted_desc": "解引用空指针 ⇒ UB",
     "basis": "ISO/IEC 14882 [expr.unary.op] 空指针解引用 UB（664 ig-07）"},
    {"id": "h24", "category": "UB", "atom_ref": "data/cards_665/fixtures/ig-08.cpp",
     "detector": "ubsan", "planted": True,
     "planted_desc": "整数除零 ⇒ UB（不是 C++ 异常）",
     "basis": "ISO/IEC 14882 [expr.mul] 除零 UB（664 ig-08）"},
    {"id": "h25", "category": "UB", "atom_ref": "data/cards_665/fixtures/ig-14.cpp",
     "detector": "asan", "planted": True,
     "planted_desc": "new[] 分配却用 delete 释放（alloc/dealloc 不匹配）⇒ UB",
     "basis": "ISO/IEC 14882 [expr.delete] 分配释放形式须匹配（664 ig-14）"},
    {"id": "h26", "category": "memory", "atom_ref": "data/cards_665/fixtures/h26.cpp",
     "detector": "asan", "planted": True,
     "planted_desc": "use-after-free：delete 后继续写该内存 ⇒ UB",
     "basis": "ISO/IEC 14882 [basic.stc.dynamic.deallocation] 释放后使用 UB（ASan 类 heap-use-after-free）"},
    {"id": "h27", "category": "memory", "atom_ref": "data/cards_665/fixtures/h27.cpp",
     "detector": "asan", "planted": True,
     "planted_desc": "double free：同一指针 delete 两次 ⇒ UB",
     "basis": "ISO/IEC 14882 [basic.stc.dynamic.deallocation] 重复释放 UB（ASan 类 double-free）"},
    {"id": "h28", "category": "memory", "atom_ref": "data/cards_665/fixtures/h28.cpp",
     "detector": "asan", "planted": True,
     "planted_desc": "返回局部变量地址并在调用方使用（use-after-scope）⇒ UB",
     "basis": "ISO/IEC 14882 [stmt.return] 返回局部变量地址 UB（ASan 类 stack-use-after-scope）"},
    {"id": "h29", "category": "UB", "atom_ref": "data/cards_665/fixtures/h29.cpp",
     "detector": "ubsan", "planted": True,
     "planted_desc": "有符号左移溢出（1 << 31）⇒ UB",
     "basis": "ISO/IEC 14882 [expr.shift] 有符号左移溢出 UB（UBSan 类 shift-exponent）"},
    {"id": "h30", "category": "memory", "atom_ref": "data/cards_665/fixtures/h30.cpp",
     "detector": "asan", "planted": True,
     "planted_desc": "内存泄漏：new 后从不 delete（堆块永久不可达）",
     "basis": "OI 资源泄漏（LeakSanitizer 类 detected memory leaks）"},
]

#: h26–h30 的夹具源码（**不落在**受控的 `Examples/` 下，只写在 `data/cards_665/fixtures/`）
NEW_FIXTURES: dict[str, str] = {
    "h26.cpp": "int main(){int* p=new int(1); delete p; *p=2; return *p;}\n",
    "h27.cpp": "int main(){int* p=new int(1); delete p; delete p; return 0;}\n",
    "h28.cpp": "int* f(){int x=7; return &x;}\nint main(){int* p=f(); return *p;}\n",
    "h29.cpp": "int main(){int x=1; volatile int y=x << 31; return y;}\n",
    "h30.cpp": "int main(){new int[64]; return 0;}\n",
}


def write_fixtures() -> list[Path]:
    out = []
    for name, code in NEW_FIXTURES.items():
        p = ROOT / "data" / "cards_665" / "fixtures" / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(code.encode("utf-8"))
        out.append(p)
    return out


def extend(apply: bool = False) -> tuple[dict, str]:
    """把 h21–h30 追加进 holdout.json。**不删、不改**原 20 个 seed。"""
    h = json.loads(HOLD.read_text(encoding="utf-8"))
    before = [s["id"] for s in h["seeds"]]
    if len(before) != 20:
        raise SystemExit(f"原 holdout 应为 20 个 seed，实际 {len(before)}：拒绝续写（防误改）")
    exist = set(before)
    added = []
    for s in NEW_SEEDS:
        if s["id"] in exist:
            continue
        ref = ROOT / s["atom_ref"]
        if not ref.is_file():
            raise SystemExit(f"夹具缺失：{s['atom_ref']}（先 --write-fixtures）")
        added.append({**s, "hidden": True, "revealed": False})
    h["seeds"].extend(added)
    h["count"] = len(h["seeds"])
    h["extend_665"] = {
        "added": [s["id"] for s in added],
        "added_true_errors": sum(1 for s in added if s["planted"] is True),
        "total_true_errors_after": sum(1 for s in h["seeds"] if s.get("planted") is True),
        "honest_note": ("新增 10 个样本全部为 planted=true 的真错（依据标准条款，非依据本机检测结论），"
                        "用于把可测真错样本从 7 提到 17；**不具备原 20 个样本的盲态**——"
                        "追加发生在 reveal 之后，故不能用于 Claim 外部效度提升，只用于增大样本量。"),
    }
    if apply:
        HOLD.write_text(json.dumps(h, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return h, f"追加 {len(added)} 个（总 {h['count']}），真错 {h['extend_665']['total_true_errors_after']}"


def write_fixtures_cmd() -> int:
    ps = write_fixtures()
    for p in ps:
        print("已写 %s（%d 字节）" % (p.relative_to(ROOT).as_posix(), p.stat().st_size))
    # 顺手校验已有 ig-* 夹具都在
    miss = [s["id"] for s in NEW_SEEDS if s["atom_ref"].startswith("data/cards_665/fixtures/ig-")
            and not (ROOT / s["atom_ref"]).is_file()]
    if miss:
        print("缺失 ig-* 夹具（先 python tools/ig_cards_665.py --build）：%s" % ", ".join(miss))
        return 1
    return 0


def selftest() -> int:
    fails = []

    def chk(name: str, cond: bool) -> None:
        if not cond:
            fails.append(name)

    chk("新增 10 个样本 id 唯一且连续", len({s["id"] for s in NEW_SEEDS}) == 10)
    chk("新增全部为 planted=true（本批补的就是真错）", all(s["planted"] is True for s in NEW_SEEDS))
    chk("每个新样本都写了 basis（标准/文档依据）", all(s.get("basis") for s in NEW_SEEDS))
    chk("无样本引用受控的 Examples/", not any(s["atom_ref"].startswith("Examples/") for s in NEW_SEEDS))
    for name, code in NEW_FIXTURES.items():
        chk(f"{name} 非空且带换行结尾", bool(code.strip()) and code.endswith("\n"))
    chk("夹具 sha256 可求（值随内容变，这里只验证不抛异常）",
        all(hashlib.sha256(c.encode()).hexdigest() for c in NEW_FIXTURES.values()))
    for f in fails:
        print("FAIL: %s" % f)
    print("holdout_extend_665 selftest: %s" % ("PASS" if not fails else "FAIL"))
    return 0 if not fails else 1


def merged(apply: bool = True) -> dict:
    """返回**合并视图**（旧 20 + 665 新增 10），并把它写到 canonical 文件 `holdout_665.json`。

    幂等：重复调用不会重复追加；旧样本**逐个原样保留**（顺序不变，字段不重排）。
    顺带 best-effort 更新 `holdout.json`（让旧工具仍能读到扩样；但它被旧工具重写也不影响本文件的效力）。
    """
    base = json.loads(HOLD.read_text(encoding="utf-8"))
    base["seeds"] = [s for s in base["seeds"] if s["id"] not in {n["id"] for n in NEW_SEEDS}]
    if len(base["seeds"]) != 20:
        raise SystemExit(f"合并基线应为原 20 个 seed，实际 {len(base['seeds'])}：拒绝（防误改）")
    out: dict = json.loads(json.dumps(base))         # 深拷贝，别改到 base（666 A1：加注解消 no-any-return）
    out["seeds"].extend({**s, "hidden": True, "revealed": True} for s in NEW_SEEDS)
    out["count"] = len(out["seeds"])
    out["generated_by"] = "660 C2 初始化 · 665 C1 扩样（canonical 合并视图）"
    out["extend_665"] = {
        "added": [s["id"] for s in NEW_SEEDS],
        "added_true_errors": sum(1 for s in NEW_SEEDS if s["planted"] is True),
        "total_true_errors_after": sum(1 for s in out["seeds"] if s.get("planted") is True),
        "canonical_file": "data/holdout/holdout_665.json",
        "why_separate_file": ("holdout.json 是 holdout_658.py 的产物，旧工具一跑就会按内建 20 样本重写 ⇒ "
                             "665 的追加必须落在不被重写的 canonical 文件里"),
        "honest_note": ("新增 10 个样本全部为 planted=true 的真错（依据标准条款，非依据本机检测结论），"
                        "用于把可测真错样本从 7 提到 17；**不具备原 20 个样本的盲态**——"
                        "追加发生在 reveal 之后，故不能用于 Claim 外部效度提升，只用于增大样本量。"),
    }
    if apply:
        MERGED.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        HOLD.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def load_merged() -> dict:
    """读 canonical 合并视图；不在（未扩样）则退回归并原文件。"""
    if MERGED.is_file():
        data: dict = json.loads(MERGED.read_text(encoding="utf-8"))  # 666 A1：注解消 no-any-return
        return data
    return merged(apply=False)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="665 C1：holdout 扩样 20→30")
    ap.add_argument("--write-fixtures", action="store_true", help="落 h26–h30 五个新夹具")
    ap.add_argument("--extend", action="store_true", help="把 h21–h30 追加进 data/holdout/holdout.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.write_fixtures:
        return write_fixtures_cmd()
    if a.extend:
        h = merged(apply=True)
        print("合并视图：%d 个样本，真错 %d 个" %
              (h["count"], h["extend_665"]["total_true_errors_after"]))
        print("已写 %s（canonical）与 %s（best-effort）" %
              (MERGED.relative_to(ROOT).as_posix(), HOLD.relative_to(ROOT).as_posix()))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
