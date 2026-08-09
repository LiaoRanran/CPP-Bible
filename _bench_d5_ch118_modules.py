# -*- coding: utf-8 -*-
"""Wave8 ch118 D5 基准：C++20 模块的「编译期」加速（GCC 15.3.0, Windows/mingw）。
模块的性能维度是【编译时间】而非运行时间——传统 #include 在每个 TU 重解析
整个头，模块只需读取一次预构建的 BMI。本脚本复现这一差异：

  传统:   g++ -std=c++23 -c user_inc.cpp   （user_inc.cpp #include "heavy.h"）
  模块:   g++ -std=c++23 -fmodules -c heavy.cppm -o heavy.o   (一次性构建, 摊销)
           g++ -std=c++23 -fmodules -c user_imp.cpp -o imp.o  (每 TU, 只读 BMI)

结论取 5 轮中位。模块构建（heavy.o）为一次性固定成本，后续每个 TU 仅付 imp.o 成本。
运行: python3 _bench_d5_ch118_modules.py
"""
import subprocess, tempfile, os, time, statistics

GPP = r"C:/Qt/Tools/mingw1530_64/bin/g++.EXE"
N = 1000  # 声明数量，模拟一个「重量级」头

def gen():
    h, cm = ["#pragma once"], ["export module heavy;"]
    for i in range(N):
        decl = f"inline int f{i}(int x){{ int r=x; for(int k=0;k<{i%16};++k) r+=k; return r+{i}; }}"
        h.append("inline int f%d(int x){ int r=x; for(int k=0;k<%d;++k) r+=k; return r+%d; }" % (i, i % 16, i))
        cm.append("export " + h[-1])
    h_txt = "\n".join(h)
    cm_txt = "\n".join(cm)
    inc = '#include "heavy.h"\nint main(){ return f0(0) + f%d(1); }\n' % (N - 1)
    imp = 'import heavy;\nint main(){ return f0(0) + f%d(1); }\n' % (N - 1)
    return h_txt, cm_txt, inc, imp

def run(args, cwd):
    t0 = time.perf_counter()
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    dt = (time.perf_counter() - t0) * 1000.0
    return r, dt

def main():
    d = tempfile.mkdtemp()
    h, cm, inc, imp = gen()
    open(os.path.join(d, "heavy.h"), "w").write(h)
    open(os.path.join(d, "heavy.cppm"), "w").write(cm)
    open(os.path.join(d, "user_inc.cpp"), "w").write(inc)
    open(os.path.join(d, "user_imp.cpp"), "w").write(imp)

    # 一次性模块构建
    r_build, t_build = run([GPP, "-std=c++23", "-fmodules", "-c", "heavy.cppm", "-o", "heavy.o"], d)
    print(f"[module build] rc={r_build.returncode} {t_build:.1f} ms (一次性, 摊销到所有 TU)")
    if r_build.returncode != 0:
        print("MODULE BUILD FAILED:", r_build.stderr); return

    inc_times, imp_times = [], []
    for _ in range(5):
        r1, t1 = run([GPP, "-std=c++23", "-c", "user_inc.cpp", "-o", "inc.o"], d)
        if r1.returncode == 0: inc_times.append(t1)
        r2, t2 = run([GPP, "-std=c++23", "-fmodules", "-c", "user_imp.cpp", "-o", "imp.o"], d)
        if r2.returncode == 0: imp_times.append(t2)

    mi, mm = statistics.median(inc_times), statistics.median(imp_times)
    print(f"[traditional per-TU] #include 中位 = {mi:.1f} ms")
    print(f"[modules     per-TU] import   中位 = {mm:.1f} ms")
    print(f"[ratio] 传统较模块慢 = {mi/mm:.2f}x  (模块每 TU 快 {mi/mm:.2f}x)")
    print(f"[setup] 声明数 N={N}; 模块一次性构建 {t_build:.1f} ms（等价于 ~{t_build/mm:.0f} 个 TU 的摊销门槛）")

if __name__ == "__main__":
    main()
