import shlex
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, "tools")
import atom_evidence_replay as rp

YANG = "Examples/atoms/_x.cpp"
YIN = "Examples/atoms/_x.nc1.cpp"

print("== 1) 现状：new_out 含空格 ==")
tmp = Path(tempfile.mkdtemp())
spaced = tmp / "has space"
spaced.mkdir()
new_out = rp._nc_path(spaced / "nc_nc1.s")
line = f"g++ -std=c++17 -O2 -S {YANG} -o build/_x.asm"
rl = rp._nc_rewrite(line, YANG, YIN, new_out)
print("  line    :", line)
print("  new_out :", new_out)
print("  rewrite :", rl)
print("  shlex   :", shlex.split(rl, posix=True))
print("  _nc_o_target(原行) =", repr(rp._nc_o_target(line)))

print("== 2) 现状：原目标带引号 ==")
line_q = f'g++ -std=c++17 -O2 -S {YANG} -o "build/_x.asm"'
print("  line    :", line_q)
print("  _nc_o_target =", repr(rp._nc_o_target(line_q)))
print("  rewrite :", rp._nc_rewrite(line_q, YANG, YIN, new_out))

print("== 3) 现状：new_out 含反斜杠（_nc_path 之前） ==")
raw = str(tmp / "sub" / "nc_nc1.s")
print("  raw     :", raw)
print("  rewrite :", rp._nc_rewrite(line, YANG, YIN, raw))
print("  shlex   :", shlex.split(rp._nc_rewrite(line, YANG, YIN, raw), posix=True))

print("== 4) 真编译：产物到底落在哪 ==")
(tmp / "_x.cpp").write_text("int f(){return 1;}\n", encoding="utf-8")
(tmp / "_x.nc1.cpp").write_text("int f(){return 0;}\n", encoding="utf-8")
cwd = Path.cwd()
before = {p.name for p in cwd.glob("*.s")}
cmd = f"g++ -std=c++17 -O2 -S {tmp.as_posix()}/_x.cpp -o {tmp.as_posix()}/build/_x.asm"
rl2 = rp._nc_rewrite(cmd, f"{tmp.as_posix()}/_x.cpp",
                     f"{tmp.as_posix()}/_x.nc1.cpp", new_out)
print("  rewrite :", rl2)
argv = shlex.split(rl2, posix=True)
print("  argv    :", argv)
res = rp.run_commands([rl2], cwd=tmp, env=dict(__import__("os").environ))
print("  rc      :", [r[1] for r in res[0]])
after = {p.name for p in cwd.glob("*.s")}
print("  落在 spaced 目录? ", (spaced / "nc_nc1.s").is_file())
print("  CWD 新增 *.s :", sorted(after - before))
for n in sorted(after - before):
    (cwd / n).unlink()
