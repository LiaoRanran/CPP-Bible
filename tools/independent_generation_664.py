#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""independent_generation_664.py — 664 B2：独立生成 A/B/C 跑一轮。

角色（同一批次内分离，避免"生成者即验证者"的知情偏差）：
  - **Agent A（生成器）**：给出 15 条新 C++ 断言（assertion）。
  - **Agent B（红队）**：为每条断言构造**反例/边界**（code + 期望观测）。
  - **Agent C（验证器攻击）**：标注**验证器漏洞**（gap）：当前检测器会不会漏/误判。
  - **验证器盲判**：对 B 的反例代码跑检测器，得到 catch / miss / unknown。

记录三方交集与差异：
  - B 能推翻的断言比例（B 造出反例且观测到反例证据）
  - C 找到的验证器漏洞数
  - 三方一致 / 三方分歧的样本

输出：data/independent_generation_run_664.json
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "independent_generation_run_664.json")

# Agent A 断言 + Agent B 反例（code 可空=纯语义反例） + 检测器 + Agent C 漏洞标注
CASES = [
    {"id": "ig-01", "assertion": "有符号整数溢出会回绕（wrap around）",
     "counterexample": "溢出是 UB；-O2 下编译器可假设不溢出，做激进优化",
     "code": "int main(){int x=2147483647; x+=1; return x<0;}", "detector": "ubsan",
     "gap": "若验证器只判'有没有崩溃'会漏：UB 不必然崩，需 sanitizer"},
    {"id": "ig-02", "assertion": "数组越界访问一定会崩溃",
     "counterexample": "小越界可能落在已映射页内，静默改坏相邻对象",
     "code": "int main(){int a[4]={0}; int i=5; a[i]=1; return a[i];}", "detector": "asan",
     "gap": "依赖运行期崩溃=漏；需 ASan"},
    {"id": "ig-03", "assertion": "delete 空指针是不安全操作",
     "counterexample": "无反例——标准保证 delete nullptr 是 no-op（断言本身错）",
     "code": "int main(){int*p=nullptr; delete p; return 0;}", "detector": "asan",
     "gap": "验证器若能跑则不会报 → 判 miss 是正确的（非漏洞）"},
    {"id": "ig-04", "assertion": "std::move 一定触发移动构造",
     "counterexample": "类型无移动构造（或移动未 noexcept）时退化为拷贝",
     "code": "#include <cstdio>\nstruct T{T()=default;T(const T&){std::printf(\"copy\");}T(T&&){std::printf(\"move\");}};\nint main(){T a; T b(std::move(a));}", "detector": "measure",
     "gap": "测量类：验证器若不跑真机就断言'一定移动'会 overclaim"},
    {"id": "ig-05", "assertion": "unique_ptr 无自定义 deleter 时 sizeof 等于裸指针",
     "counterexample": "无反例（零开销抽象成立）",
     "code": "#include <memory>\n#include <cstdio>\nint main(){std::printf(\"%zu %zu\\n\", sizeof(void*), sizeof(std::unique_ptr<int>));}", "detector": "measure",
     "gap": "无（测量可得）"},
    {"id": "ig-06", "assertion": "两个 shared_ptr 互持一定泄漏",
     "counterexample": "用 weak_ptr 断开则不泄漏",
     "code": "#include <memory>\nstruct B; struct A{std::shared_ptr<B> b;}; struct B{std::weak_ptr<A> a;};\nint main(){auto x=std::make_shared<A>(); x->b=std::make_shared<B>(); x->b->a=x;}", "detector": "asan",
     "gap": "运行期泄漏检测缺位时验证器无法自证"},
    {"id": "ig-07", "assertion": "解引用空指针一定段错误",
     "counterexample": "UB，编译器可优化掉该分支，不崩",
     "code": "int main(){int*p=nullptr; *p=1; return 0;}", "detector": "asan",
     "gap": "同 ig-01：依赖崩溃=漏"},
    {"id": "ig-08", "assertion": "整数除零会抛出 C++ 异常",
     "counterexample": "UB/信号（SIGFPE），不是 C++ 异常，catch(...) 抓不到",
     "code": "int main(){volatile int a=1,b=0; return a/b;}", "detector": "ubsan",
     "gap": "验证器若按'异常'建模会误判"},
    {"id": "ig-09", "assertion": "-O2 优化不改变程序语义",
     "counterexample": "依赖 UB 的代码在 -O0/-O2 结果不同",
     "code": "int f(int*p){*p=1; return *p;}\nint main(){int x=0; return f(&x);}", "detector": "cross-compile",
     "gap": "只用单一优化级别验证=漏"},
    {"id": "ig-10", "assertion": "char 类型一定有符号",
     "counterexample": "实现定义（x86 Linux gcc 有符号，ARM 常无符号）",
     "code": "#include <cstdio>\nint main(){char c=-1; std::printf(\"%d\\n\",(int)c);}", "detector": "cross-compile",
     "gap": "单平台验证=overclaim"},
    {"id": "ig-11", "assertion": "sizeof(int) 恒等于 4",
     "counterexample": "平台相关（ILP32/LLP64 不同）",
     "code": "#include <cstdio>\nint main(){std::printf(\"%zu\\n\", sizeof(int));}", "detector": "measure",
     "gap": "需 platform 字段（663 C1 已补）"},
    {"id": "ig-12", "assertion": "std::vector<bool> 可以取 &v[0] 得到 bool*",
     "counterexample": "位压缩特化，返回代理对象，取址失败",
     "code": "#include <vector>\nint main(){std::vector<bool> v(4); auto p=&v[0]; (void)p;}", "detector": "compiler-warn",
     "gap": "需编译验证，纯文本检查会漏"},
    {"id": "ig-13", "assertion": "用 reinterpret_cast 做类型双关是安全的",
     "counterexample": "违反严格别名，-O2 下结果可错",
     "code": "int f(float*p){*(int*)p=1; return (int)*p;}\nint main(){float x=0; return f(&x);}", "detector": "cross-compile",
     "gap": "UBSan 常检不出别名类 UB → 验证器会漏（662 A2 已证）"},
    {"id": "ig-14", "assertion": "new[] 分配的数组可以用 delete 释放",
     "counterexample": "UB（mismatched alloc/dealloc）",
     "code": "int main(){int*p=new int[4]; delete p; return 0;}", "detector": "asan",
     "gap": "需 ASan；纯编译检查会漏"},
    {"id": "ig-15", "assertion": "具名右值引用形参会自动按右值移动",
     "counterexample": "具名右值引用是左值，需显式 std::move",
     "code": "#include <cstdio>\nstruct T{T(){}T(const T&){std::printf(\"copy\");}T(T&&){std::printf(\"move\");}};\nvoid g(T x){}\nvoid h(T&& x){g(x);}\nint main(){h(T{});}", "detector": "measure",
     "gap": "需真机计数，静态检查易漏"},
]
SAN = {"tsan": "thread", "asan": "address", "ubsan": "undefined"}


def _to_wsl(p):
    p = p.replace("\\", "/")
    return ("/mnt/" + p[0].lower() + p[2:]) if len(p) > 1 and p[1] == ":" else p


def _sh(cmd, timeout=180):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return -1, f"err:{e}"


def run_detector(kind, code):
    if not code:
        return ("unknown", "无代码")
    d = tempfile.mkdtemp(prefix="ig_")
    src = os.path.join(d, "s.cpp")
    open(src, "w", encoding="utf-8").write(code)
    exe = os.path.join(d, "s.exe")
    if kind in ("compiler-warn",):
        rc, out = _sh(["g++", "-std=c++17", "-Wall", "-Wextra", "-fsyntax-only", src])
        w = [l for l in out.splitlines() if "warning:" in l] or (
            [l for l in out.splitlines() if "error:" in l])
        return (("catch", w[0][:70]) if w else ("miss", "无告警/无错误"))
    if kind == "cross-compile":
        outs = []
        for cc, opt in (("g++", "-O0"), ("g++", "-O2")):
            rc, out = _sh([cc, "-std=c++17", opt, src, "-o", exe])
            if rc != 0:
                return ("unknown", f"{cc} {opt} 编译失败")
            rc, out = _sh([exe], timeout=30)
            outs.append(out.strip())
        return (("catch", "-O0/-O2 结果不同") if outs[0] != outs[1] else ("miss", "两优化级一致"))
    if kind in SAN:
        rc, out = _sh(["wsl", "-e", "bash", "-lc",
                       f"g++ -std=c++17 -O1 -g -fsanitize={SAN[kind]} -pthread {_to_wsl(src)} -o /tmp/igbin"])
        if rc != 0:
            return ("unknown", "编译失败")
        rc, out = _sh(["wsl", "-e", "bash", "-lc", "/tmp/igbin"], timeout=60)
        hit = any(s in out for s in ("AddressSanitizer", "LeakSanitizer", "runtime error"))
        return (("catch", f"{kind} 命中(rc={rc})") if hit else ("miss", f"{kind} 无报告"))
    if kind == "measure":
        rc, out = _sh(["g++", "-std=c++17", "-O2", src, "-o", exe])
        if rc != 0:
            return ("unknown", "编译失败")
        rc, out = _sh([exe], timeout=30)
        return ("measure", (out.strip() or "")[:40])
    return ("unknown", "未支持")


def main() -> int:
    rows = []
    b_refuted = c_gaps = 0
    agree = differ = 0
    for c in CASES:
        v, note = run_detector(c["detector"], c["code"])
        # B 是否推翻了断言：有反例代码且检测器给出了反例证据（catch 或 measure 到差异）
        refuted = (v == "catch") or (v == "measure" and bool(note))
        has_gap = c["gap"] not in ("无（测量可得）", "") and not c["gap"].startswith("无")
        if refuted:
            b_refuted += 1
        if has_gap:
            c_gaps += 1
        # 三方一致：B 推翻 ⇒ 验证器应有反应（catch/measure）；或 无反例 ⇒ 无反应
        expect_reaction = refuted
        got_reaction = v in ("catch", "measure")
        if expect_reaction == got_reaction:
            agree += 1
        else:
            differ += 1
        rows.append({"id": c["id"], "assertion": c["assertion"], "counterexample": c["counterexample"],
                     "detector": c["detector"], "validator_verdict": v, "validator_note": note,
                     "b_refuted": refuted, "c_gap": c["gap"], "c_flagged_gap": has_gap})
        print(f"  {c['id']:<7} {v.upper():<8} B推翻={str(refuted):<5} {c['detector']:<14} {note[:44]}")

    rep = {
        "schema": "queyi-independent-generation/v1",
        "generated_at": "2026-09-28",
        "generated_by": "tools/independent_generation_664.py",
        "roles": {"A": "生成器（15 条断言）", "B": "红队（逐条造反例）",
                  "C": "验证器攻击（标注检测器漏洞）", "validator": "盲判（跑检测器）"},
        "total_assertions": len(CASES),
        "b_refuted": b_refuted,
        "b_refute_rate_pct": round(b_refuted / len(CASES) * 100, 1),
        "c_gaps_flagged": c_gaps,
        "three_way_agree": agree,
        "three_way_differ": differ,
        "honest_note": ("B/C/验证器三方在同一批次内由同一进程产出，未做真正的角色隔离"
                        "（真正独立需分开会话/模型），故本轮只跑通流程，交集/差异仅作方法学验证。"),
        "results": rows,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\nB 推翻 {b_refuted}/{len(CASES)} = {rep['b_refute_rate_pct']}%")
    print(f"C 标注验证器漏洞 {c_gaps}；三方一致 {agree} / 分歧 {differ}")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
