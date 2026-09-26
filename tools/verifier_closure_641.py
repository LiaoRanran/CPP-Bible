"""641 D1–D3 · **Verifier Closure**（信任根闭包）+ 缺失即 FAIL + run 绑定 digest

§D1：从最终 verifier 出发，传递闭包**所有影响 verdict 的代码/规则/配置/schema/环境**，
闭包带 digest ⇒ 第三方凭 run + 闭包即可复验。

§D2：**缺失即 FAIL（新模式）**——信任根文件/schema/依赖缺失由 warning 改为 failure
（**只在新 core 口径下**启用，不强行全局切换，§八.5）。判据：闭包里任一文件缺失 ⇒ FAIL。

§D3：把 `verifier_closure_digest` / `policy_digest` / `source_revision` 落到
`VerificationRun.digests`，使 run 能自述"用哪版内核、哪版规则跑的"。

攻击测试：`simulate_missing()` **不真删文件**（受控/信任根零破坏），而是"假装某文件缺失"
计算判定 ⇒ 必须 FAIL；单测用 tmp 副本验证真实删除路径。

CLI：`--check`（只读自检）/ `--json` / `--report`（写 `data/641_verifier_closure.md`）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from typing import Any, Iterable, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import queyi_core_v10_641 as core  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "641_verifier_closure.md")
OUT_JSON = os.path.join(ROOT, "data", "641_verifier_closure.json")

#: 闭包起点：内核 + C++ 适配器（本轮新增的并行层）
CLOSURE_ROOTS = ("queyi_core_v10_641", "queyi_core_cpp_641", "queyi_core_toy_641")
#: 5 个 CORE_TOOLS：判决逻辑本体（本轮零改动，但必须进闭包）
CORE_TOOLS = ("gate_engine", "poison_drill", "atom_evidence_replay", "toolchain", "cppbible")
#: 配置/schema 类信任根（相对 repo 根）
TRUST_ROOT_GLOBS = ("pyproject.toml", "tools/.tool_checksums",
                    "data/supply_chain/merkle_roots.json")


def sha256_file(path: str) -> Optional[str]:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def module_path(name: str) -> Optional[str]:
    p = os.path.join(HERE, name + ".py")
    return p if os.path.isfile(p) else None


def _rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def closure_files(include_core_tools: bool = True) -> list[str]:
    """传递闭包：从 `CLOSURE_ROOTS` 出发，沿 import 图（只跟 **repo 内** tools/*.py）展开，
    再并入 5 个 CORE_TOOLS 本体与配置类信任根。返回**排序去重**的**相对路径**列表。"""
    seen: set[str] = set()
    stack = [n for n in CLOSURE_ROOTS]
    if include_core_tools:
        stack += list(CORE_TOOLS)
    files: set[str] = set()
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        p = module_path(name)
        if not p:
            continue
        files.add(_rel(p))
        for dep in core.module_imports(p):
            dp = module_path(dep)
            if dp and dep not in seen:
                stack.append(dep)
    for rel in TRUST_ROOT_GLOBS:
        files.add(rel)
    # data/supply_chain/ 下的其余信任根文件
    sc = os.path.join(ROOT, "data", "supply_chain")
    if os.path.isdir(sc):
        for fn in sorted(os.listdir(sc)):
            fp = os.path.join(sc, fn)
            if os.path.isfile(fp):
                files.add(_rel(fp))
    return sorted(files)


def build_closure(missing: Iterable[str] = ()) -> dict[str, Any]:
    """构建闭包。

    `missing` = 假装缺失的相对路径（**攻击测试用，不真删**）。缺失项会被记入
    `missing` 列表，并在 `status` 上体现为 **FAIL**（D2：缺失即 FAIL）。
    """
    miss = set(missing)
    entries: list[dict[str, str]] = []
    missing_list: list[str] = []
    for rel in closure_files():
        if rel in miss:
            missing_list.append(rel)
            continue
        p = os.path.join(ROOT, rel)
        d = sha256_file(p)
        if d is None:
            missing_list.append(rel)
            continue
        entries.append({"path": rel, "sha256": d})
    entries.sort(key=lambda e: e["path"])
    missing_list.sort()
    digest = core.digest_of(entries)
    return {"schema": "verifier_closure/1.0",
            "status": "FAIL" if missing_list else "OK",
            "n_files": len(entries), "n_missing": len(missing_list),
            "missing": missing_list, "files": entries, "digest": digest}


def closure_digest() -> str:
    return str(build_closure()["digest"])


def source_revision() -> str:
    try:
        p = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=30)
        return p.stdout.strip() if p.returncode == 0 else "unknown"
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def annotate(builder: core.VerificationRunBuilder,
             closure: Optional[dict[str, Any]] = None,
             policy_digest: str = "") -> core.VerificationRunBuilder:
    """D3：把闭包/政策/环境/版本 digest 绑定到 run。"""
    cl = closure or build_closure()
    builder.set_digest("verifier_closure_digest", cl["digest"])
    builder.set_digest("closure_status", cl["status"])
    builder.set_digest("closure_n_files", str(cl["n_files"]))
    if policy_digest:
        builder.set_digest("policy_digest", policy_digest)
    builder.set_digest("source_revision", source_revision())
    builder.set_result("closure", {"n_files": cl["n_files"], "status": cl["status"],
                                   "missing": cl["missing"], "digest": cl["digest"]})
    return builder


def simulate_missing(rels: Iterable[str]) -> dict[str, Any]:
    """D2 攻击测试：**假装**这些信任根缺失（不真删），判定必须为 FAIL。"""
    return build_closure(missing=list(rels))


def write_report(cl: dict[str, Any]) -> str:
    lines = ["# 641 D1–D3 · Verifier Closure（信任根闭包）", "",
             f"- 状态：**{cl['status']}** · 闭包文件 **{cl['n_files']}** 个 · 缺失 **{cl['n_missing']}**",
             f"- closure_digest：`{cl['digest']}`",
             f"- source_revision：`{source_revision()}`", "",
             "## 一、闭包构成", "",
             f"- 起点（新增并行层）：{', '.join(CLOSURE_ROOTS)}",
             f"- CORE_TOOLS（判决逻辑本体，本轮零改动）：{', '.join(CORE_TOOLS)}",
             f"- 配置/schema 信任根：{', '.join(TRUST_ROOT_GLOBS)} + `data/supply_chain/*`", "",
             "## 二、缺失即 FAIL（D2）", "",
             "```",
             f"simulate_missing(['pyproject.toml']) ⇒ {simulate_missing(['pyproject.toml'])['status']}",
             "```", "",
             "## 三、诚实登记", "",
             "1. 闭包只跟 **repo 内 `tools/*.py`** 的 import；第三方依赖（如 PyYAML）"
             "以 `pyproject.toml` 声明进闭包，**不递归进 site-packages**；",
             "2. 「缺失即 FAIL」只作用于 **新 core 口径**，未强行切换任何既有流程（§八.5）；",
             "3. 闭包完整性的**强度**仍取决于本机信任根未外移（外部 KMS/第三方签名留交人裁决）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cl, fh, ensure_ascii=False, indent=2)
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    cl = build_closure()
    paths = [e["path"] for e in cl["files"]]
    chk("闭包非空", cl["n_files"] > 0, str(cl["n_files"]))
    chk("闭包含内核与适配器", "tools/queyi_core_v10_641.py" in paths
        and "tools/queyi_core_cpp_641.py" in paths)
    for t in CORE_TOOLS:
        chk(f"闭包含 CORE_TOOL {t}", f"tools/{t}.py" in paths)
    chk("闭包含配置信任根", "pyproject.toml" in paths and "tools/.tool_checksums" in paths)
    chk("真实仓库闭包状态 OK（无缺失）", cl["status"] == "OK", str(cl["missing"]))
    chk("closure_digest 确定性", build_closure()["digest"] == cl["digest"])
    # D2：缺失即 FAIL（不真删）
    att = simulate_missing(["pyproject.toml"])
    chk("假装缺失信任根 ⇒ FAIL（不是 warning）", att["status"] == "FAIL")
    chk("缺失项被点名", att["missing"] == ["pyproject.toml"], str(att["missing"]))
    chk("缺失会改变 digest", att["digest"] != cl["digest"])
    # D3：绑定
    b = annotate(core.VerificationRunBuilder("cpp", source_revision="x"), policy_digest="p1")
    run = b.seal()
    chk("run 绑定 verifier_closure_digest", run.digests["verifier_closure_digest"] == cl["digest"])
    chk("run 绑定 policy_digest", run.digests["policy_digest"] == "p1")
    chk("run 绑定 source_revision", run.digests["source_revision"] == source_revision())
    chk("绑定后 run 自校验通过", run.verify_integrity())
    print(f"closure selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="641 Verifier Closure（信任根闭包）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写闭包报告 + JSON")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--simulate-missing", default="",
                    help="假装该相对路径缺失（逗号分隔），验证缺失即 FAIL")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.simulate_missing:
        rels = [x.strip() for x in a.simulate_missing.split(",") if x.strip()]
        r = simulate_missing(rels)
        print(json.dumps({"status": r["status"], "missing": r["missing"]}, ensure_ascii=False))
        return 0 if r["status"] == "FAIL" else 1
    cl = build_closure()
    if a.report:
        print(f"written {write_report(cl)}（{cl['status']}，{cl['n_files']} 文件）")
        return 0
    print(json.dumps(cl, ensure_ascii=False, indent=2) if a.json else
          f"closure status={cl['status']} n_files={cl['n_files']} digest={cl['digest']}")
    return 0 if cl["status"] == "OK" else 1


if __name__ == "__main__":
    sys.exit(main())
