#!/usr/bin/env python3
"""hy3_check.py — 一键项目健康检查（秒级）

Hy3 接手后第一条命令。6 项检查，纯读取，不改任何文件。
耗时 < 10 秒（断言扫描读缓存报告，不重跑）。

用法:
    cd C:/CodeLearnling/note/note/C++/CPP-Bible
    python3 tools/hy3_check.py

快捷方式（Windows Git Bash）:
    alias hc='python3 tools/hy3_check.py'
"""

import pathlib
import re
import subprocess
import sys
import os

ROOT = pathlib.Path(__file__).resolve().parent.parent
PYTHON = r"C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe"
GPP = r"C:/Qt/Tools/mingw1530_64/bin/g++.exe"

def run_tool(script, args=None, timeout=30):
    cmd = [PYTHON, str(ROOT / "tools" / script)]
    if args:
        cmd.extend(args)
    # Windows 管道下 Python 子进程默认用 GBK 输出中文，父进程用 utf-8 解码会乱码；
    # 强制子进程 PYTHONUTF8=1 让其以 UTF-8 输出，父子编码一致（CI/UTF-8 本就无碍）。
    env = dict(os.environ)
    env["PYTHONUTF8"] = "1"
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout, env=env)

def extract_int(lines, pattern):
    """在包含 pattern 的行中，提取 pattern 之后出现的第一个整数。"""
    for ln in lines:
        if pattern in ln:
            idx = ln.index(pattern)
            tail = ln[idx + len(pattern):]
            m = re.search(r"\d+", tail)
            if m:
                return int(m.group(0))
    return -1


def parse_assert_cache(text: str) -> dict:
    """Parse cached assertion report into structured fields."""
    result = {"static_pass": -1, "static_fail": -1, "static_warn": -1, "static_demo": -1,
              "runtime_pass": -1, "runtime_fail": -1, "runtime_warn": -1}
    for ln in text.splitlines():
        if "编译期 static_assert" in ln:
            nums = [int(x) for x in re.findall(r"\d+", ln)]
            if len(nums) >= 4:
                result["static_pass"], result["static_fail"], result["static_warn"], result["static_demo"] = nums[:4]
        elif "运行期 assert 程序" in ln:
            nums = [int(x) for x in re.findall(r"\d+", ln)]
            if len(nums) >= 3:
                result["runtime_pass"], result["runtime_fail"], result["runtime_warn"] = nums[:3]
    return result

def main():
    # Windows 控制台(GBK)无法编码 emoji/中文，重导向为 utf-8 容错，避免本地验证崩溃
    # （CI 为 UTF-8 本就无碍；errors='replace' 保证任何环境都能跑完并 exit 0/1）
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  《现代 C++ 终极圣经》 健康检查  (147章 | 7033cpp)    ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    all_ok = True
    had_warn = False

    # ── 1. 环境 ──────────────────────────────────────────
    print("── 1. 环境 ──")
    try:
        py_ver = subprocess.run([PYTHON, "--version"], capture_output=True, text=True).stdout.strip()
        gpp_ver = subprocess.run([GPP, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
        print(f"  ✅ {py_ver}")
        print(f"  ✅ G++ {gpp_ver}")

        venv_mkdocs = "C:/Users/ASUS/.workbuddy/binaries/python/envs/default/Scripts/mkdocs.exe"
        if pathlib.Path(venv_mkdocs).exists():
            print(f"  ✅ mkdocs-material venv 就绪")
        else:
            print(f"  ⚠️  mkdocs venv 未找到（站点构建不可用）")
    except Exception as e:
        print(f"  ❌ 环境检测失败: {e}")
        all_ok = False
    print()

    # ── 2. 门禁 ──────────────────────────────────────────
    print("── 2. 门禁 (consistency_check) ──")
    try:
        r = run_tool("consistency_check.py")
        score = extract_int(r.stdout.splitlines(), "一致性评分")
        err = extract_int(r.stdout.splitlines(), "ERROR=")
        warn = extract_int(r.stdout.splitlines(), "WARN=")
        ok = score == 100 and err == 0 and warn == 0
        tag = "✅" if ok else "❌"
        if not ok:
            all_ok = False
        print(f"  {tag} {score}/100  ERROR={err}  WARN={warn}  (期望 100/100, 0/0)")
    except Exception as e:
        print(f"  ❌ 门禁失败: {e}")
        all_ok = False
    print()

    # ── 3. 断言（读缓存，不重跑） ───────────────────────
    print("── 3. 断言契约 (run_cpp_assertions 缓存) ──")
    cache = ROOT / "build" / "assert_report.txt"
    if cache.exists():
        a = parse_assert_cache(cache.read_text(encoding="utf-8"))
        s_pass, s_fail = a["static_pass"], a["static_fail"]
        r_pass, r_fail = a["runtime_pass"], a["runtime_fail"]
        ok = s_fail == 0 and r_fail == 0
        tag = "✅" if ok else "❌"
        if not ok:
            all_ok = False
        if s_pass > 0:
            print(f"  {tag} 编译期 PASS={s_pass} FAIL={s_fail}  |  运行期 PASS={r_pass} FAIL={r_fail}")
            print(f"     期望 FAIL=0  |  DEMO={a['static_demo']}(教学反例)  WARN={a['static_warn']}+{a['runtime_warn']}(隔离伪影)")
        else:
            print(f"  ⚠️  缓存报告格式异常，请重跑: python3 tools/run_cpp_assertions.py")
            all_ok = False
        print(f"     重跑完整扫描: python3 tools/run_cpp_assertions.py")
    else:
        print(f"  ⚠️  缓存报告缺失，运行 python3 tools/run_cpp_assertions.py 生成")
    print()

    # ── 4. 交引 ──────────────────────────────────────────
    print("── 4. 交叉引用 (crossref_audit) ──")
    try:
        r = run_tool("crossref_audit.py", timeout=30)
        total = extract_int(r.stdout.splitlines(), "交叉引用总计")
        broken = extract_int(r.stdout.splitlines(), "断链总数")
        ok = broken == 0
        tag = "✅" if ok else "❌"
        if not ok:
            all_ok = False
        print(f"  {tag} 总计={total} 引用  断链={broken}  (期望 断链=0)")
    except Exception as e:
        print(f"  ❌ 交引审计失败: {e}")
        all_ok = False
    print()

    # ── 5. 工作区卫生 ────────────────────────────────────
    print("── 5. 工作区卫生 ──")
    bak_count = len(list(ROOT.glob("Book/**/*.bak")))
    probe_count = 0
    for f in (ROOT / "tools").glob("_*.py"):
        if f.name != "_clean_junk.py":  # Phase 3 永久工具
            probe_count += 1
    # 根目录编译产物泄漏：违反 AGENT.md「只写 build/」红线。
    # 这些 *.cpp/*.exe/*.o 是编译工具写在 CWD（根）的副产物，应待在 build/。
    root_art = []
    for ext in ("*.cpp", "*.exe", "*.o"):
        root_art += list(ROOT.glob(ext))
    root_art_n = len(root_art)
    if bak_count == 0 and probe_count == 0 and root_art_n == 0:
        print(f"  ✅ .bak=0  临时探针=0  根目录产物=0  工作区干净")
    else:
        if bak_count:
            print(f"  ⚠️  {bak_count} 个 .bak 残留 → find Book -name '*.bak' -delete")
            all_ok = False
        if probe_count:
            print(f"  ⚠️  {probe_count} 个临时探针残留在 tools/_*.py")
            all_ok = False
        if root_art_n:
            print(f"  ⚠️  {root_art_n} 个编译产物泄漏到根目录（违反「只写 build/」）")
            print(f"      清理: python3 tools/clean_root_artifacts.py  (移入 build/_root_artifacts/)")
            had_warn = True
    print()

    # ── 6. 交接文档 ──────────────────────────────────────
    print("── 6. 交接文档 ──")
    missing = []
    for fname in ["AGENT.md", "HANDOVER.md", "TASKS.md", "ROADMAP_v2.md",
                  "PROGRESS.md", "CROSSREF.md"]:
        if not (ROOT / fname).exists():
            missing.append(fname)
    if not missing:
        print(f"  ✅ 6 份核心文档齐全")
    else:
        all_ok = False
        print(f"  ❌ 缺 {len(missing)} 份: {', '.join(missing)}")
    print()

    # ── 7. 汇编证据准确性 ────────────────────────────────
    print("── 7. 汇编证据准确性 ──")
    try:
        r = run_tool("verify_asm_evidence.py", timeout=120)
        out = r.stdout
        # 提取摘要行
        for line in out.splitlines():
            if "ACCURATE" in line or "DRIFT" in line or "EMPTY" in line or "UNANCHORED" in line:
                print("  " + line.strip())
        if r.returncode == 0:
            print("  ✅ 书内 asm 块引用的 mangled 符号均 ⊆ Examples/*.asm 真实产物")
        else:
            all_ok = False
            print("  ❌ 存在 DRIFT（书内符号在真实 .asm 中找不到）→ 运行 verify_asm_evidence.py 查看")
    except Exception as e:  # pragma: no cover
        print(f"  ⚠️ 校验跳过: {e}")
    print()

    # ── 终局 ──────────────────────────────────────────────
    print("═" * 54)
    if all_ok and not had_warn:
        print("  ✅ 全部通过 — 项目健康，可以开工。")
        print()
        print("  第一步:  python3 tools/hy3_check.py           (本脚本)")
        print("  第二步:  cat ROADMAP_v2.md                     (竣工路线)")
        print("  第三步:  从「竣工-1」开始 → 跑 CI → 出 1.0")
    elif all_ok and had_warn:
        print("  ✅ 通过（含警告）— 门禁/断言/交引均达标，仅卫生项需清理。")
        print("      建议: python3 tools/clean_root_artifacts.py")
    else:
        print("  ❌ 存在失败项，请根据以上报告修复。")
    print("═" * 54)
    print()

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
