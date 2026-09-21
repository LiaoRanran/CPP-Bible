#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
602 探针：编译可复现性实证（只读 / 临时目录，不碰 Examples/ 正式夹具）。

验证目标（对应方向 5）：
  A. 同一源 + 同一命令 + 同一编译器 → 两次编译的二进制 sha 是否一致（确定性编译）。
  B. 含 __DATE__/__TIME__/__FILE__ 宏的夹具（_ch161_macro/loc/full.cpp）编译两次，
     sha 是否变化 —— 这类宏会向 .rodata 注入时间戳，破坏逐字节可复现。

全部落 %TEMP%，不写仓库任何正式文件。
"""
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent  # .../CPP-Bible
EXAMPLES = REPO / "Examples"


def resolve_gpp() -> str:
    """优先复用仓库 toolchain，否则回退 PATH 上的 g++。"""
    for cand in ("toolchain", "tools.toolchain"):
        try:
            mod = __import__(cand, fromlist=["resolve_gpp"])
            g = mod.resolve_gpp()
            if g and Path(g).is_file():
                return g
        except Exception:
            pass
    g = shutil.which("g++")
    return g or ""


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def compile_twice(gpp: str, src: Path, ext: str, extra_flags: list[str]) -> dict:
    """同一源编译两次到临时目录，返回两次输出的 sha 与是否一致。"""
    out = {}
    for i in (1, 2):
        d = Path(tempfile.mkdtemp(prefix=f"repro_{i}_"))
        outp = d / f"o.{ext}"
        cmd = [gpp, "-std=c++20", "-O2", *extra_flags, str(src), "-o", str(outp)]
        r = subprocess.run(cmd, capture_output=True, text=True, errors="replace", cwd=str(d))
        out[i] = {
            "rc": r.returncode,
            "sha": sha(outp) if outp.is_file() else None,
            "stderr_head": (r.stderr or "")[:200],
        }
    same = out[1]["sha"] is not None and out[1]["sha"] == out[2]["sha"]
    return {"src": src.name, "runs": out, "sha_equal": same}


def main() -> int:
    gpp = resolve_gpp()
    print(f"g++ 解析结果: {gpp!r}")
    if not gpp or not Path(gpp).is_file():
        print("[SKIP] 未解析到 g++，无法实跑（仅记录方法）")
        return 0
    ver = subprocess.run([gpp, "-dumpfullversion"], capture_output=True, text=True)
    print(f"g++ 版本: {ver.stdout.strip() or '?.?'}")
    print("=" * 60)

    # A. 普通确定性编译：内存放一个极小源（不依赖 Examples）
    tiny = Path(tempfile.gettempdir()) / "_repro_tiny.cpp"
    tiny.write_text("int main(){int s=0;for(int i=0;i<10;++i)s+=i;return s;}\n")
    r_a = compile_twice(gpp, tiny, "exe", [])
    print("A. 极小程序 两次编译可执行 sha 一致?", r_a["sha_equal"],
          "| run1", (r_a["runs"][1]["sha"] or "")[:12],
          "| run2", (r_a["runs"][2]["sha"] or "")[:12])

    # B. 含时间/文件宏的夹具（仅拷贝到临时目录，不改动 Examples）
    print("-" * 60)
    macro_fixtures = ["_ch161_macro.cpp", "_ch161_loc.cpp", "_ch161_full.cpp"]
    for name in macro_fixtures:
        f = EXAMPLES / name
        if not f.is_file():
            print(f"B. {name}: 仓库内未找到，跳过"); continue
        tmp = Path(tempfile.gettempdir()) / f"_repro_{name}"
        tmp.write_bytes(f.read_bytes())  # 拷贝到临时目录编译
        # 用 -S 出汇编（与仓库 .asm 工件形态一致），-O2
        r = compile_twice(gpp, tmp, "s", ["-S"])
        print(f"B. {name} 两次汇编 sha 一致?", r["sha_equal"],
              "| run1", (r["runs"][1]["sha"] or "NA")[:12],
              "| run2", (r["runs"][2]["sha"] or "NA")[:12])
    print("=" * 60)
    print("结论提示：A 不一致→编译器非确定性（异常）；B 不一致→__DATE__/__TIME__ 宏注入时间戳。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
