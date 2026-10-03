"""spotcheck_F.py — 任务 D 质量抽检（676c-F）。

规格：用固定种子 6761 从 200 个候选中抽取 20%（=40）个样本，
做“人工级”字段完整性与语义检查：
  - 全部必填字段存在
  - defect_location 含 line/function/description
  - planted == true
  - expected_verdict ∈ {catch, miss}
  - platform_dependent 为布尔；若为 True 则 platform_notes 非空
  - expected_detectors 非空且为已知 kind
  - 对应 .cpp 存在且含 main、能定位缺陷行
不合格率 > 10% 则提示提高到 50%（本脚本不自动扩抽，仅报告）。
"""
import os, json, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
SEED = 6761
FRAC = 0.20
TOTAL = 200
N = int(TOTAL * FRAC)  # 40

REQUIRED = [
    "sample_id", "defect_type", "defect_location", "severity", "planted",
    "expected_verdict", "expected_detectors", "trigger_condition",
    "platform_dependent", "platform_notes", "notes",
]
KNOWN_KINDS = {"ubsan", "asan", "tsan", "compiler-warn", "wunsequenced",
               "cross-compile", "linker"}
VALID_TYPES = {"alignment", "endianness", "volatile_misuse", "bit_operation",
               "interrupt_safety", "register_ub"}


def check_one(idx):
    sid = f"F{idx:03d}"
    jpath = os.path.join(HERE, f"sample_{sid}.json")
    cpath = os.path.join(HERE, f"sample_{sid}.cpp")
    problems = []

    if not os.path.isfile(jpath):
        return False, ["json 缺失"], None
    if not os.path.isfile(cpath):
        return False, ["cpp 缺失"], None

    meta = json.load(open(jpath, encoding="utf-8"))

    # 必填字段
    for f in REQUIRED:
        if f not in meta:
            problems.append(f"缺字段 {f}")
    # planted
    if meta.get("planted") is not True:
        problems.append("planted 不为 true")
    # expected_verdict
    ev = meta.get("expected_verdict")
    if ev not in ("catch", "miss"):
        problems.append(f"expected_verdict 非法: {ev!r}")
    # defect_type
    if meta.get("defect_type") not in VALID_TYPES:
        problems.append(f"defect_type 非法: {meta.get('defect_type')!r}")
    # defect_location 结构
    dl = meta.get("defect_location") or {}
    for k in ("line", "function", "description"):
        if k not in dl or dl.get(k) in (None, ""):
            problems.append(f"defect_location.{k} 缺失/空")
    # platform_dependent 布尔 + notes
    pd = meta.get("platform_dependent")
    if not isinstance(pd, bool):
        problems.append("platform_dependent 非布尔")
    elif pd is True and not (meta.get("platform_notes") or "").strip():
        problems.append("platform_dependent=True 但 platform_notes 空")
    # expected_detectors
    ed = meta.get("expected_detectors") or []
    if not ed:
        problems.append("expected_detectors 空")
    else:
        for k in ed:
            if k not in KNOWN_KINDS:
                problems.append(f"expected_detectors 含未知 kind: {k}")
    # notes / trigger_condition / platform_notes 非空
    for f in ("notes", "trigger_condition", "platform_notes"):
        if not (meta.get(f) or "").strip():
            problems.append(f"{f} 空")
    # cpp 含 main
    cpp = open(cpath, encoding="utf-8").read()
    if not re.search(r"\bint\s+main\s*\(", cpp):
        problems.append("cpp 无 main")
    # 缺陷行存在（PLANTED 标记）
    if "<<PLANTED-DEFECT>>" not in cpp:
        problems.append("cpp 无 PLANTED 缺陷标记")
    # defect_location.line 与标记行一致
    marked = [i + 1 for i, ln in enumerate(cpp.splitlines()) if "<<PLANTED-DEFECT>>" in ln]
    if marked and dl.get("line") not in marked:
        problems.append(f"defect_location.line={dl.get('line')} 与标记行 {marked} 不一致")

    return (len(problems) == 0), problems, meta


def main():
    rng = random.Random(SEED)
    idxs = sorted(rng.sample(range(1, TOTAL + 1), N))
    print(f"种子 {SEED} 抽取 {len(idxs)} 个样本（20%）：")
    print(", ".join(f"F{i:03d}" for i in idxs))
    print("-" * 60)
    fails = []
    for idx in idxs:
        ok, probs, meta = check_one(idx)
        if ok:
            print(f"  F{idx:03d}  ✓  type={meta['defect_type']:<14} verdict={meta['expected_verdict']}")
        else:
            print(f"  F{idx:03d}  ✗  " + "; ".join(probs))
            fails.append((idx, probs))
    rate = len(fails) / len(idxs)
    print("-" * 60)
    print(f"抽检 {len(idxs)} 个，不合格 {len(fails)} 个，不合格率 {rate:.1%}")
    if rate > 0.10:
        print("⚠️ 不合格率 > 10%，按规格应将抽检比例提高到 50%。")
    else:
        print("✓ 不合格率 ≤ 10%，抽检通过，无需扩抽。")


if __name__ == "__main__":
    main()
