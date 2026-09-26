"""644 阶段 D · D2 编译器实测获取器。

功能（原型级，§十二.4 仅 g++）：对给定代码片段用本地 g++ 编译运行，记录输出；
支持多个编译选项（-O0/-O2/-std=c++17/-std=c++20）；保存：代码片段 / 编译命令 /
输出 / 退出码 / 编译器版本；存入证据库，**等级 L1**（实测）。

沙箱隔离（§九.5）：编译运行在临时目录，不碰生产；运行后清理。
只读/追加：只写 data/evidence_store/，不碰受控目录。
`--check` 只读幂等；`--probe <file|snippet>` 真正编译运行（需本机 g++）。
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base

OUT_MD = os.path.join(base.ROOT, "data", "644_compiler_probe_report.md")
DEFAULT_OPTS = ["-std=c++17", "-O2"]


def find_compiler(name: str = "g++") -> str | None:
    return shutil.which(name)


def _compiler_version(compiler: str) -> str:
    try:
        out = subprocess.run([compiler, "--version"], capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=20)
        return out.stdout.splitlines()[0] if out.stdout else "unknown"
    except Exception:  # noqa: BLE001
        return "unknown"


def probe(snippet: str, opts: list[str] | None = None, compiler: str = "g++") -> dict[str, Any]:
    """在沙箱临时目录编译运行；返回 {ok, output, exit_code, command, compiler_version, sandbox}。"""
    compiler_path = find_compiler(compiler)
    if compiler_path is None:
        return {"ok": False, "error": f"未找到编译器 {compiler}", "sandbox": None}
    opts = opts or DEFAULT_OPTS
    sandbox = tempfile.mkdtemp(prefix="cppbible_probe_")
    src = os.path.join(sandbox, "snippet.cpp")
    exe = os.path.join(sandbox, "snippet.exe") if os.name == "nt" else os.path.join(sandbox, "snippet")
    try:
        with open(src, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(snippet)
        cmd = [compiler_path, *opts, src, "-o", exe]
        comp = subprocess.run(cmd, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=60, cwd=sandbox)
        if comp.returncode != 0:
            return {"ok": False, "error": comp.stderr, "command": " ".join(cmd),
                    "compiler_version": _compiler_version(compiler_path), "sandbox": sandbox}
        run = subprocess.run([exe], capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=30, cwd=sandbox)
        return {"ok": True, "output": run.stdout, "exit_code": run.returncode,
                "command": " ".join(cmd), "compiler_version": _compiler_version(compiler_path),
                "sandbox": sandbox}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}", "sandbox": sandbox}


def cleanup(sandbox: str | None) -> None:
    if sandbox and os.path.isdir(sandbox):
        import shutil as sh
        sh.rmtree(sandbox, ignore_errors=True)


def make_evidence(snippet: str, result: dict[str, Any]) -> base.EvidenceRecord:
    from datetime import datetime
    content = (f"compiler: {result.get('compiler_version','')}\n"
               f"command: {result.get('command','')}\n"
               f"output: {result.get('output','')}\n"
               f"exit_code: {result.get('exit_code',-1)}\n\n"
               f"```cpp\n{snippet}\n```")
    rec = base.store_evidence(
        content, source_type="compiler_run", grade="L1", credibility=0.95,
        acquired_at=datetime.now().strftime("%Y-%m-%d"),
        acquisition_method="compiler_probe_644", source_url=None,
        meta={"kind": "compiler_run", "compilers": 1,
              "compiler_version": result.get("compiler_version", ""), "grade_note": "单编译器原型(§十二.4)"})
    return rec


def write_report(last: dict[str, Any] | None = None) -> str:
    r = last or {"ok": False, "error": "未执行", "output": "", "command": ""}
    lines = ["# 644 D2 · 编译器实测报告", "",
             f"- 成功：**{r.get('ok')}**", f"- 命令：`{r.get('command','')}`",
             f"- 输出：`{r.get('output','')[:200]}`", "",
             "> 原型仅 g++（§十二.4）；clang/MSVC 未覆盖，可移植性证据不完整。", ""]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    snippet = "#include <iostream>\nint main(){ std::cout << \"42\" << std::endl; return 0; }\n"
    if find_compiler("g++") is None:
        # 无编译器：降级，不崩溃
        r = probe(snippet)
        assert r["ok"] is False and "未找到" in r["error"]
        return 0
    r = probe(snippet)
    assert r["ok"] is True
    assert "42" in r["output"]
    assert r["exit_code"] == 0
    # 多选项支持
    r2 = probe(snippet, ["-std=c++17", "-O0"])
    assert r2["ok"] is True
    # 沙箱隔离：sandbox 目录在运行后存在但可被清理，且不碰生产
    assert r["sandbox"] is not None
    cleanup(r["sandbox"])
    assert not os.path.isdir(r["sandbox"])
    # 等级 L1
    rec = make_evidence(snippet, r)
    assert rec.grade == "L1"
    os.remove(base.store_path(rec.evidence_id))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="644 D2 编译器实测获取器")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--probe", metavar="SNIPPET", help="要编译运行的 C++ 片段")
    ap.add_argument("--opts", metavar="OPTS", help="编译选项（逗号分隔）")
    ap.add_argument("--compiler", default="g++", help="编译器命令（默认 g++）")
    a = ap.parse_args(argv)
    if a.probe:
        opts = a.opts.split(",") if a.opts else None
        r = probe(a.probe, opts, a.compiler)
        if r["ok"]:
            rec = make_evidence(a.probe, r)
            print(f"ok 证据 {rec.evidence_id[:12]}… 输出={r['output'][:80]!r}")
        else:
            print(f"fail: {r.get('error','')[:200]}")
        cleanup(r.get("sandbox"))
        print(f"written {write_report(r)}")
        return 0 if r["ok"] else 2
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
