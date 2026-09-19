#!/usr/bin/env python3
"""B0 阴夹具生成器（535 批次2 · 一次性，带前置断言；不静默写错）。

变换 = 对阳夹具 `Examples/atoms/_atom_fence_vs_atomic.cpp` 做**定点删除**：
删掉 `spin_signal_fence` 循环体内那一行零指令屏障（同名文本在别的函数里也出现 ⇒
只能按函数区间删，文本替换会连别人一起删——这正是探针要能识别"定点"的原因）。
产物 `Examples/atoms/_atom_fence_vs_atomic.nc1.cpp` 必须可见地只差这一行。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import viso_diff as vd  # noqa: E402

YANG = ROOT / "Examples" / "atoms" / "_atom_fence_vs_atomic.cpp"
YIN = ROOT / "Examples" / "atoms" / "_atom_fence_vs_atomic.nc1.cpp"
FENCE = "        __atomic_signal_fence(__ATOMIC_SEQ_CST);\n"
ANCHOR = "spin_signal_fence"
REMOVE = "__atomic_signal_fence(__ATOMIC_SEQ_CST);"
RETAIN = ["while (!s_sf_b)", "return s_sf_a;"]

src = vd.norm_nl(YANG.read_text(encoding="utf-8"))
# 实测：8 空格缩进形态只出现 1 次（anchor 内）；而**去掉缩进后的同一行文本**出现 3 次
# （writer_signal_fence / spin_signal_fence / spin_fence_outside）⇒ 文本替换无法定位，
# 必须按函数区间定点删除（533 §1.3 的说法在此精确化：同文本、不同缩进）。
assert src.count(FENCE) == 1, f"前置断言：8 空格形态应恰 1 次，实测 {src.count(FENCE)}"
assert src.count(FENCE.strip()) == 3, f"前置断言：同文本应 3 次，实测 {src.count(FENCE.strip())}"
head, body = src.split(f"int {ANCHOR}()\n{{", 1)          # Allman：`{` 单独一行
assert body.count(FENCE) == 1, "anchor 体内应恰有 1 行 fence"
out = head + f"int {ANCHOR}()\n{{" + body.replace(FENCE, "", 1)
assert out != src and out.count(FENCE.strip()) == 2, "变换未生效或删错位置"

v = vd.judge_min_diff(src, out, anchor=ANCHOR, remove_text=REMOVE, retain=RETAIN,
                      probe_symbol="_Z17spin_signal_fencev")
assert v.ok, f"判据不过：{v.reasons}"
assert v.metrics["code_deleted_lines"] == 1 and v.metrics["anchor_coverage"] == 1.0, v.metrics
YIN.write_text(out, encoding="utf-8", newline="\n")
print(f"[nc1] 已生成 {YIN.relative_to(ROOT)}："
      f"deleted={v.metrics['deleted_code']} tokens_changed={v.metrics['tokens_changed']} "
      f"ratio={v.metrics['token_change_ratio']}")
