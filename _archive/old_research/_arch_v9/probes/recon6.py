"""582 只读侦察⑥：读 _arch_v4/560_E 的 E1/E2/E3 正文（核实任务书引用的前轮结论）。"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "_arch_v4/560_E_外置检索记忆知识层.md"
src = p.read_text(encoding="utf-8").splitlines()
print(f"总行数 {len(src)}")
for a, b in [(19, 40), (52, 72), (72, 100)]:
    print(f"===== {a}-{b} =====")
    for j in range(a - 1, min(len(src), b)):
        print(f"{j+1:4}|{src[j][:118]}")
