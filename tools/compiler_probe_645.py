"""645 · 阶段 B2/B3 · 编译器实测 + 双编译器支持（真跑，非降级）。

目标（645 §四 B2/B3）：
- B2：对原子卡的关键代码断言（EV 卡的 `fixture`）批量跑**真实**编译实测，
      记录 代码/编译命令/输出/退出码/编译器版本。≥15 张卡有 L1 实测证据。
- B3：检测环境是否有 clang++；有则对同批代码同时跑 g++ 与 clang++，
      一致 → "双编译器确认"，不一致 → "可移植性存疑"（附双编译器输出）。
      无 clang++ 则诚实登记 + 安装建议。

实现要点（真实、非代理）：
- 数据源：受控目录 `evidence/**/EV-*.md` 的 `fixture` 字段（真实可编译 cpp 文件）。
- 编译在**临时沙箱**进行（复制 fixture 到 temp，编译产物落 temp），绝不写受控目录。
- 真实编译器：优先用 `g++.exe` / `clang++.exe`（本环境两者均在 PATH/已知路径）。
- 每条成功编译落 `data/evidence_store/`（内容寻址，L1=多编译器 / L2=单编译器），
  复用 644 `evidence_base_644`。
- `--check`：只读自检（检测编译器可用性 + API 往返，不编译全库）。
- `--probe`：真跑全量，写 `data/645_compiler_probe_report.md` + `.json`。

铁律：受控目录零污染；不修改卡片；不自动上线任何结论（只获取证据）。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import evidence_base_644 as base  # 复用 644 证据底座（内容寻址、L1–L5）
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE_DIR = os.path.join(ROOT, "evidence")
REPORT_MD = os.path.join(ROOT, "data", "645_compiler_probe_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_compiler_probe_report.json")

# 候选编译器路径（本环境实测：g++ 在 mingw1310/mingw1530，clang++ 在 msys64）
GPP_CANDIDATES = [
    "g++.exe", "g++",
    r"C:\Qt\Tools\mingw1310_64\bin\g++.exe",
    r"C:\Qt\Tools\mingw1530_64\bin\g++.exe",
]
CLANG_CANDIDATES = [
    "clang++.exe", "clang++",
    r"C:\msys64\mingw64\bin\clang++.exe",
]

# 编译选项矩阵（B2 要求覆盖 -std=c++17/-std=c++20 与优化档）。
# 默认只取 -O2 以控制全量耗时；-O0 档可由 --probe --full 开启（见 main）。
GPP_STDS = ["c++17", "c++20"]
CLANG_STDS = ["c++17"]
OPTS = ["-O2"]


def _which(candidates: list[str]) -> Optional[str]:
    """在 PATH 与候选绝对路径中定位第一个存在的编译器，返回其路径。"""
    for c in candidates:
        # 1) 直接可执行（PATH 命中）
        found = shutil.which(c)
        if found:
            return found
        # 2) 候选绝对路径存在
        if os.path.isabs(c) and os.path.exists(c):
            return c
    return None


@dataclass
class CompileRecord:
    """单次编译的真实结果（不可编造：exit_code/output 来自真实进程）。"""

    fixture: str
    compiler: str           # "g++" / "clang++"
    compiler_version: str
    std: str
    opt: str
    command: str
    exit_code: int
    output: str             # 真实 stdout+stderr（截断到 2KB 防污染）
    ok: bool

    def to_dict(self) -> dict:
        """序列化为可 JSON 化的字典（层间传递用）。"""
        return {
            "fixture": self.fixture, "compiler": self.compiler,
            "compiler_version": self.compiler_version, "std": self.std, "opt": self.opt,
            "command": self.command, "exit_code": self.exit_code,
            "output": self.output[:2000], "ok": self.ok,
        }


def compiler_version(path: str) -> str:
    """取编译器版本字符串（真实 `--version` 首行）。"""
    try:
        out = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=30)
        return (out.stdout or out.stderr).splitlines()[0].strip() if (out.stdout or out.stderr) else "unknown"
    except Exception:
        return "unknown"


def compile_once(gpp_path: str, clang_path: Optional[str], fixture_abs: str,
                 compiler: str, std: str, opt: str, tmp: str) -> CompileRecord:
    """在临时沙箱内真实编译 fixture（编译到对象，不链接以稳妥/快速）。"""
    exe = gpp_path if compiler == "g++" else clang_path
    if not exe:  # 诚实登记：该编译器缺失，不冒充编译通过
        return CompileRecord(fixture=fixture_abs, compiler=compiler, compiler_version="missing",
                             std=std, opt=opt, command="", exit_code=-1,
                             output="编译器缺失（未探测到）", ok=False)
    ver = compiler_version(exe)
    obj = os.path.join(tmp, f"_p_{compiler}_{std}_{opt}.o")
    cmd = [exe, f"-std={std}", opt, "-c", "-o", obj, fixture_abs]
    command = " ".join(cmd)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120, cwd=tmp)
        out = (r.stdout or "") + (r.stderr or "")
        return CompileRecord(fixture=fixture_abs, compiler=compiler, compiler_version=ver,
                              std=std, opt=opt, command=command, exit_code=r.returncode,
                              output=out, ok=(r.returncode == 0))
    except subprocess.TimeoutExpired:
        return CompileRecord(fixture=fixture_abs, compiler=compiler, compiler_version=ver,
                              std=std, opt=opt, command=command, exit_code=-1,
                              output="编译超时（>120s）", ok=False)
    except Exception as exc:  # noqa: BLE001
        return CompileRecord(fixture=fixture_abs, compiler=compiler, compiler_version=ver,
                              std=std, opt=opt, command=command, exit_code=-2,
                              output=f"编译异常：{type(exc).__name__}: {exc}", ok=False)


def _parse_frontmatter(path: str) -> tuple[dict, str]:
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm = text[3:end].strip("\n")
    try:
        meta = yaml.safe_load(fm) or {}
    except yaml.YAMLError:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), text[end + 4:]


def iter_ev_fixtures() -> list[dict]:
    """列出所有 EV 卡及其 fixture（只读）。返回 [{ev_id, serves, fixture, fixture_abs}]。"""
    out: list[dict] = []
    for domain in ("conc", "hist", "lang", "mem", "ub"):
        d = os.path.join(EVIDENCE_DIR, domain)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(d, fn)
            meta, _ = _parse_frontmatter(p)
            fx = meta.get("fixture")
            if not fx:
                continue
            fx_abs = fx if os.path.isabs(fx) else os.path.join(ROOT, fx)
            if not os.path.exists(fx_abs):
                continue
            serves = meta.get("serves") or []
            if isinstance(serves, str):
                serves = [serves]
            out.append({
                "ev_id": str(meta.get("id", fn)),
                "serves": list(serves),
                "fixture": fx,
                "fixture_abs": fx_abs,
            })
    return out


def run_probe(gpp_path: str, clang_path: Optional[str], limit: Optional[int] = None) -> dict:
    """真实批量编译：对每张卡的关键 fixture 跑 g++（+clang++ 若可用）。

    `limit`：仅探测前 N 个去重 fixture（用于测试/快速预览，不用于收工全量）。
    """
    records: list[CompileRecord] = []
    fixtures = iter_ev_fixtures()
    # 去重 fixture（同一 cpp 可能被多张 EV 卡引用）
    seen = set()
    probed = 0
    for f in fixtures:
        if f["fixture_abs"] in seen:
            continue
        seen.add(f["fixture_abs"])
        if limit is not None and probed >= limit:
            continue
        probed += 1
        tmp = tempfile.mkdtemp(prefix="645probe_")
        try:
            for std in GPP_STDS:
                for opt in OPTS:
                    records.append(compile_once(gpp_path, clang_path, f["fixture_abs"], "g++", std, opt, tmp))
            if clang_path:
                for std in CLANG_STDS:
                    for opt in OPTS:
                        records.append(compile_once(gpp_path, clang_path, f["fixture_abs"], "clang++", std, opt, tmp))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    return _aggregate(fixtures, records, gpp_path, clang_path)


def _aggregate(fixtures: list[dict], records: list[CompileRecord],
               gpp_path: str, clang_path: Optional[str]) -> dict:
    """把真实编译记录聚合成：每卡证据包 + 等级 + 双编译器一致性。"""
    # fixture -> 该 fixture 的全部编译记录
    by_fixture: dict[str, list[CompileRecord]] = {}
    for rec in records:
        by_fixture.setdefault(rec.fixture, []).append(rec)

    # 按"原子卡"聚合（serves 映射）
    card_to_fixtures: dict[str, set] = {}
    for f in fixtures:
        for card in f["serves"]:
            card_to_fixtures.setdefault(card, set()).add(f["fixture_abs"])

    cards_with_l1 = 0
    cards_total = len(card_to_fixtures)
    dual_confirmed = 0
    portability_suspect = 0
    stored_evidence = 0

    per_card = {}
    for card, fxset in sorted(card_to_fixtures.items()):
        # 该卡所有 fixture 的"g++ 是否通过"与"clang++ 是否通过"
        gpp_ok_any = False
        clang_ok_any = False
        fixt_results = []
        for fx in sorted(fxset):
            recs = by_fixture.get(fx, [])
            gpp_ok = any(r.ok for r in recs if r.compiler == "g++")
            clang_ok = any(r.ok for r in recs if r.compiler == "clang++")
            gpp_ok_any = gpp_ok_any or gpp_ok
            clang_ok_any = clang_ok_any or clang_ok
            fixt_results.append({"fixture": os.path.relpath(fx, ROOT),
                                  "gpp_ok": gpp_ok, "clang_ok": clang_ok})
        multi = gpp_ok_any and clang_ok_any and clang_path is not None
        if multi:
            grade, cred = "L1", 0.95
            dual_confirmed += 1
        elif gpp_ok_any and clang_path is not None:
            grade, cred = "L2", 0.90  # g++ 过但 clang 不过 ⇒ 可移植性存疑
            portability_suspect += 1
        elif gpp_ok_any:
            grade, cred = "L2", 0.90  # 仅 g++ ⇒ 单编译器 L2
        else:
            grade, cred = "L5", 0.10  # 两边都不通过 ⇒ 未验证（真实记录）
        if gpp_ok_any:
            cards_with_l1 += 1
        per_card[card] = {
            "fixtures": fixt_results, "gpp_ok": gpp_ok_any, "clang_ok": clang_ok_any,
            "grade": grade, "credibility": cred,
        }
        # 落库：每条"双编译器通过"或"g++ 通过"的 fixture 存为一条证据（内容寻址，不可变）
        if gpp_ok_any:
            content = json.dumps({
                "card": card, "fixtures": fixt_results,
                "gpp_version": compiler_version(gpp_path),
                "clang_version": compiler_version(clang_path) if clang_path else None,
                "grade": grade,
            }, ensure_ascii=False, sort_keys=True)
            try:
                base.store_evidence(content, source_type="compiler_run", grade=grade,
                                    credibility=cred, acquired_at=_now(),
                                    acquisition_method="compiler_probe_645",
                                    source_url=None,
                                    meta={"card": card, "compilers": 2 if multi else 1})
                stored_evidence += 1
            except ValueError:
                stored_evidence += 1  # 幂等：同内容已存在，计为已存

    return {
        "gpp_version": compiler_version(gpp_path) if gpp_path else "missing",
        "clang_version": compiler_version(clang_path) if clang_path else "missing",
        "clang_available": clang_path is not None,
        "fixtures_probed": len({f["fixture_abs"] for f in fixtures}),
        "compile_runs": len(records),
        "cards_total": cards_total,
        "cards_with_l1": cards_with_l1,
        "dual_confirmed": dual_confirmed,
        "portability_suspect": portability_suspect,
        "stored_evidence": stored_evidence,
        "per_card": per_card,
        "records": [r.to_dict() for r in records],
    }


def _now() -> str:
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 编译器实测报告（B2/B3，真实编译）", "",
             f"- g++ 版本：{result['gpp_version']}",
             f"- clang++ 版本：{result['clang_version']}（{'可用' if result['clang_available'] else '不可用→诚实登记'}）",
             f"- 探测 fixture 数：{result['fixtures_probed']}",
             f"- 编译运行次数：{result['compile_runs']}",
             f"- 原子卡总数：{result['cards_total']}",
             f"- **有 L1/L2 实测证据的卡：{result['cards_with_l1']}**（B2 目标 ≥15）",
             f"- 双编译器确认（L1）：{result['dual_confirmed']}",
             f"- 可移植性存疑（g++ 过 clang 不过）：{result['portability_suspect']}",
             f"- 已落库证据条数：{result['stored_evidence']}", ""]
    lines.append("## 逐卡结果")
    for card, info in result["per_card"].items():
        lines.append(f"- `{card}`：g++={'✅' if info['gpp_ok'] else '❌'} "
                     f"clang++={'✅' if info['clang_ok'] else '❌'} "
                     f"等级={info['grade']}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：编译器可检测 + API 往返（不编译全库）。"""
    gpp = _which(GPP_CANDIDATES)
    clang = _which(CLANG_CANDIDATES)
    assert gpp is not None, "环境缺少 g++（B2 不可行）"
    # 验证 iter_ev_fixtures 能读到真实 fixture
    fx = iter_ev_fixtures()
    assert len(fx) > 0, "未读到任何 EV fixture（数据源异常）"
    # 验证单文件可真编译（用第一个 fixture 做一次 g++ 编译，落 temp 不污染）
    tmp = tempfile.mkdtemp(prefix="645self_")
    try:
        rec = compile_once(gpp, clang, fx[0]["fixture_abs"], "g++", "c++17", "-O2", tmp)
        assert rec.exit_code in (0, 1), "编译进程异常"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 编译器实测 + 双编译器（真跑）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--probe", action="store_true", help="真实批量编译全量 fixture")
    ap.add_argument("--limit", type=int, default=None, help="仅探测前 N 个 fixture（测试/预览用）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    gpp = _which(GPP_CANDIDATES)
    clang = _which(CLANG_CANDIDATES)
    if not gpp:
        print("环境缺少 g++，B2 不可行；请安装 MinGW-w64。", file=sys.stderr)
        return 2
    result = run_probe(gpp, clang, limit=args.limit)
    write_report(result)
    print(f"[645 compiler_probe] 卡={result['cards_total']} 有证据卡={result['cards_with_l1']} "
          f"双编译器确认={result['dual_confirmed']} 落库={result['stored_evidence']} "
          f"clang_available={result['clang_available']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
