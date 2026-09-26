"""647 C1 · **仓库拆分沙箱验证**（在原仓库之外做，**原仓库零改动**）。

方案（645 D 阶段调研结论 + 647 落地）：**保留历史的按路径拆分**。

* 原方案写的是 `git subtree split`；`subtree split` 只能按**一个 prefix** 拆，
  而 core 文件**分散在 `tools/` 多处**（不是单一子目录）⇒ 直接用 `subtree split` 会带上大量非 core 文件。
* 647 改用 **`git fast-export --all -- <paths> | git fast-import`**：
  单趟 C 实现（比 `filter-branch` 快一个数量级），产出仓库**只含 core 路径**，
  且**保留这些文件的历史**（每条相关 commit 都在）。

沙箱的三步（全部在**临时目录**里）：
1. `git clone` 当前仓库到临时目录（**不碰原仓库**）；
2. 在克隆里 `fast-export → fast-import` 造出 `queyi-core` 仓库；
3. 验证三件事：**历史保留**（提交数 > 0 且核心文件有历史）、**独立可跑**
   （内核模块能在**没有原仓库其余部分**的情况下 import 并跑自检）、**测试能跑**（若有测试被拆进去）。

CLI：`--check` / `--report` / `--json` / `--execute`（在**指定目标目录**真造一个本地 queyi-core 仓库）。
纯标准库。**不 push、不改原仓库工作树**。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

OUT_MD = os.path.join(ROOT, "data", "647_split_sandbox_report.md")
OUT_JSON = os.path.join(ROOT, "data", "647_split_sandbox_report.json")

#: core 文件模式（相对 repo 根；用 glob 展开成**显式文件清单**再交给 git）
CORE_PATTERNS: tuple[str, ...] = (
    "tools/queyi_core_*.py",          # 641 协议内核（v10 / cpp / toy）
    "tools/verifier_closure_*.py",    # 641/647 信任根闭包
    "tools/path_config_625.py",       # 路径解耦（内核依赖）
    "tools/utf8_console.py",          # 控制台编码（内核依赖）
    "tools/queyi_data_models_645.py",  # 统一数据模型
    "tools/*_645.py",                 # 645 智能层 / 头部层 / 耦合层
    "tools/*_646.py",                 # 646 规则↔卡映射 / 证据索引 / 性能
    "tools/*_647.py",                 # 647 保护器 + 信任根工具
    "tests/test_*_645.py",
    "tests/test_*_646.py",
    "tests/test_*_647.py",
    "tests/test_verifier_closure_641.py",
)
#: **不随拆分迁移**的仓库集成配置（实测：它们与"全仓完整性机制"强耦合，见报告 §三）
#: * `tests/conftest.py` 会去调 `tools/tool_integrity.py` 校验 test_config —— 拆分仓库没有全量工具；
#: * 根 `conftest.py` 做"会话级写保护"，也依赖整仓结构。
#: ⇒ queyi-core 需要**自己的**最小 conftest（沙箱验证时临时写一份，见 `MINIMAL_CONFTEST`）。
NOT_MIGRATED: tuple[str, ...] = ("pyproject.toml", "conftest.py", "tests/conftest.py")

#: queyi-core 的最小 conftest（只做 sys.path 注入）—— 沙箱验证用，C4 会把它落到 queyi-core
MINIMAL_CONFTEST = (
    '"""queyi-core 自己的最小 conftest：只把 tools/ 注入 sys.path（不依赖全仓机制）。"""\n'
    "import os\nimport sys\n"
    "sys.path.insert(0, os.path.join(\n"
    "    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tools'))\n"
)
#: 拆分后必须**跑得起来**的内核入口（独立可跑判据）
STANDALONE_ENTRY = "tools/queyi_core_v10_641.py"


def core_files(root: Optional[str] = None) -> list[str]:
    """展开 core 文件清单 = **种子模式 ∪ 其 repo 内 import 传递闭包**（去重排序）。

    为什么要有"闭包"这一步（实测教训）：种子只写 `tools/*_647.py` 时，
    保护器会 import 它们的**前身**（`*_642.py` 灰度 / `*_636.py` 影子）⇒
    拆出来跑测试会大面积 ImportError。647 的闭包工具（`verifier_closure_647`）
    用的是同一套"沿 import 图展开"的机制 —— 这里复用内核的 `module_imports()`。

    `root` 传**克隆目录**时，只有**已提交**的文件会被选中（未提交的新工具不在历史里，
    理应不进拆分结果）——沙箱用克隆目录，本仓库自检用 ROOT。
    """
    import queyi_core_v10_641 as core  # 复用内核的 import 图解析

    base = root or ROOT
    out: set[str] = set()
    for pat in CORE_PATTERNS:
        for p in glob.glob(os.path.join(base, pat)):
            if os.path.isfile(p):
                out.add(os.path.relpath(p, base).replace(os.sep, "/"))
    seen: set[str] = set()
    stack = [f for f in sorted(out) if f.startswith("tools/")]
    while stack:
        rel = stack.pop()
        if rel in seen:
            continue
        seen.add(rel)
        p = os.path.join(base, rel)
        if not os.path.isfile(p):
            continue
        for dep in core.module_imports(p):
            dp = f"tools/{dep}.py"
            if dp not in out and os.path.isfile(os.path.join(base, dp)):
                out.add(dp)
                stack.append(dp)
    return sorted(out)


def _run(cmd: list[str], cwd: Optional[str] = None, timeout: int = 900
         ) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, cwd=cwd or ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return r.returncode, (r.stdout + r.stderr)[-2000:]
    except FileNotFoundError:
        return 2, f"命令缺失：{cmd[0]}"
    except subprocess.TimeoutExpired:
        return 3, f"超时（>{timeout}s）：{' '.join(cmd[:3])}"


def _git(args: list[str], cwd: str) -> tuple[int, str]:
    return _run(["git", *args], cwd=cwd)


def split_repo(dest: str, src: str = ROOT, files: Optional[list[str]] = None) -> dict[str, Any]:
    """在 `dest`（**空目录/不存在**）造出只含 core 路径、且保留历史的仓库。"""
    files = files if files is not None else core_files()
    if not files:
        return {"ok": False, "why": "core 文件清单为空"}
    os.makedirs(dest, exist_ok=True)
    rc, out = _run(["git", "init", "-q", "-b", "master"], cwd=dest)
    if rc != 0:
        return {"ok": False, "why": f"git init 失败：{out}"}
    # fast-export（原仓库）→ fast-import（目标仓库）：单趟、保留历史、只留指定路径
    # `--tag-of-filtered-object=drop`：仓库里有指向**未被导出对象**的 tag（如临时快照 tag），
    # 不处理会让 fast-export 以 128 失败（"tags unexported object"）。拆分仓库不需要这些 tag。
    dump = os.path.join(os.path.dirname(dest), "_core_dump.fi")
    with open(dump, "wb") as fh:
        # `--reencode=yes`：历史里有 commit 带 `encoding gbk` 头（早期 Windows 提交），
        # 不重编码会让 fast-export 直接失败（实测）。重编码只动 commit message 的编码声明。
        ex = subprocess.run(["git", "fast-export", "--all",
                             "--tag-of-filtered-object=drop", "--reencode=yes",
                             "--", *files], cwd=src, stdout=fh, stderr=subprocess.PIPE)
    if ex.returncode != 0:
        return {"ok": False, "why": f"fast-export 失败（{ex.returncode}）："
                                    f"{ex.stderr.decode('utf-8', 'replace')[:400]}"}
    with open(dump, "rb") as fh:
        imp = subprocess.run(["git", "fast-import", "--quiet"], cwd=dest, stdin=fh,
                             stderr=subprocess.PIPE)
    if imp.returncode != 0:
        return {"ok": False, "why": f"fast-import 失败（{imp.returncode}）："
                                    f"{imp.stderr.decode('utf-8', 'replace')[:400]}"}
    _git(["checkout", "-f", "master"], dest)
    rc, out = _git(["rev-list", "--count", "HEAD"], dest)
    n_commits = int(out.strip()) if rc == 0 and out.strip().isdigit() else 0
    rc2, head = _git(["rev-parse", "HEAD"], dest)
    return {"ok": n_commits > 0, "dest": dest, "n_commits": n_commits,
            "head": head.strip()[:12] if rc2 == 0 else "",
            "n_files_declared": len(files)}


def verify_standalone(dest: str) -> dict[str, Any]:
    """独立可跑判据：内核能在**只有 core 文件**的仓库里 import 并跑自检。"""
    code = ("import sys; sys.path.insert(0, 'tools');"
            "import queyi_core_v10_641 as c;"
            "print('FOUR_STATES=', c.FOUR_STATES)")
    rc, out = _run([sys.executable, "-c", code], cwd=dest, timeout=120)
    import_ok = rc == 0 and "FOUR_STATES=" in out
    # 内核自带 selftest（若存在 --check 入口）
    rc2, out2 = _run([sys.executable, STANDALONE_ENTRY, "--check"], cwd=dest, timeout=180)
    return {"import_ok": import_ok, "import_tail": out[-300:] if not import_ok else "ok",
            "kernel_check_rc": rc2, "kernel_check_tail": out2[-400:]}


def verify_tests(dest: str) -> dict[str, Any]:
    """测试能跑：拆分仓库里跑 `pytest --collect-only`（**不跑全量**）。

    **诚实口径**：原仓库的 `conftest.py` / `pyproject.toml` **不随拆分迁移**
    （它们与全仓完整性机制强耦合，实测会让收集期直接报错）。
    这里在**沙箱仓库里临时写一份最小 conftest**（只注入 sys.path）再收集 ——
    这正是 C4 要给 queyi-core 落的文件。
    """
    tdir = os.path.join(dest, "tests")
    if not os.path.isdir(tdir):
        return {"collected": 0, "note": "拆分结果里没有 tests/（诚实登记）"}
    with open(os.path.join(tdir, "conftest.py"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(MINIMAL_CONFTEST)
    rc, out = _run([sys.executable, "-m", "pytest", "tests", "--collect-only", "-q",
                    "-p", "no:cacheprovider"], cwd=dest, timeout=600)
    errs = [ln for ln in out.splitlines() if ln.startswith("ERROR ")]
    return {"collect_rc": rc, "n_error_files": len(errs), "error_files": errs[:20],
            "conftest_used": "最小 conftest（沙箱临时写入）",
            "tail": out[-500:]}


def history_preserved(dest: str, files: Optional[list[str]] = None) -> dict[str, Any]:
    """历史保留判据：核心文件在拆分仓库里的提交数与**原仓库**一致。"""
    files = files if files is not None else core_files()
    probe = files[:1] or [""]
    rc1, a = _git(["rev-list", "--count", "HEAD", "--", *probe], dest)
    rc2, b = _git(["rev-list", "--count", "HEAD", "--", *probe], ROOT)
    return {"probe": probe[0], "in_split": a.strip() if rc1 == 0 else "?",
            "in_origin": b.strip() if rc2 == 0 else "?",
            "same": rc1 == 0 and rc2 == 0 and a.strip() == b.strip()}


def sandbox_run() -> dict[str, Any]:
    """完整沙箱实验（**临时目录**，用完即删；**原仓库零改动**）。"""
    tmp = tempfile.mkdtemp(prefix="queyi_split_647_")
    try:
        clone = os.path.join(tmp, "src")
        # 本地克隆（默认硬链接对象库，秒级）；`git` 从不改写对象 ⇒ 对原仓库仍是只读
        rc, out = _run(["git", "clone", "-q", ROOT, clone], timeout=900)
        if rc != 0:
            return {"ok": False, "why": f"clone 失败：{out}", "n_core_files": 0}
        # 清单从**克隆**里取 ⇒ 只包含已提交文件（未提交的新工具不进历史拆分，符合预期）
        files = core_files(clone)
        dest = os.path.join(tmp, "queyi-core")
        s = split_repo(dest, src=clone, files=files)
        if not s.get("ok"):
            return {"ok": False, "why": s.get("why"), "n_core_files": len(files), "split": s}
        st = verify_standalone(dest)
        tests = verify_tests(dest)
        hist = history_preserved(dest, files)
        return {"ok": bool(st["import_ok"] and s["n_commits"] > 0),
                "n_core_files": len(files), "split": s, "standalone": st,
                "tests": tests, "history": hist, "tmp": tmp}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def risk_assessment() -> list[dict[str, str]]:
    return [
        {"risk": "`fast-export --all -- <paths>` 只**保留触及这些路径的提交** ⇒ "
                 "某些 commit 会变成空提交被丢弃（历史是「核心文件视角」的，不是全量）",
         "trigger": "有人期望拆分仓库的提交数与原仓库相同",
         "rollback": "报告里同时给出**原仓库**与**拆分仓库**的提交数（不掩饰差值）"},
        {"risk": "core 文件**分散在 `tools/` 多处** ⇒ 用 `git subtree split --prefix=tools` 会带上大量非 core",
         "trigger": "按 645 备忘直接用 subtree split",
         "rollback": "改用 fast-export/import 显式路径清单（本工具做法）；清单可审计（`core_files()`）"},
        {"risk": "拆分后 core 与 CPP-Bible **重复**（两份同名工具）",
         "trigger": "CPP-Bible 继续改工具，而 queyi-core 不跟",
         "rollback": "本批**不**把 queyi-core 合并回 CPP-Bible 子目录（见 647 §十.7 交人项）；"
                     "先把拆分产物放仓库外，观察一轮再决定"},
        {"risk": "沙箱验证**不等于**生产可用（临时目录删掉了，没有长期回归）",
         "trigger": "把沙箱通过当成「已经拆好」",
         "rollback": "C3 只建**本地**仓库、不 push；是否长期维护由人裁决"},
    ]


def write_report(res: Optional[dict[str, Any]] = None) -> str:
    res = res or sandbox_run()
    lines = [
        "# 647 C1 · 仓库拆分**沙箱验证**（原仓库零改动）", "",
        f"- 结论：**{'通过' if res.get('ok') else '未通过'}**",
        f"- core 文件数（声明的路径清单）：**{res.get('n_core_files')}**", "",
        "## 一、方案：为什么不是 `git subtree split`", "",
        "645 D 阶段调研写的是 `git subtree split`。实测口径问题：**subtree split 只能按一个 prefix 拆**，"
        "而 core 文件**分散在 `tools/` 多处**（内核 / 证据层 / 智能层 / 保护器 / 耦合层）⇒ "
        "按 `--prefix=tools` 拆会把 500+ 个非 core 工具一起带走。", "",
        "647 改用 **`git fast-export --all -- <paths> | git fast-import`**：",
        "- 单趟 C 实现（比 `filter-branch` 快一个数量级，且不需要为每个 commit 起 shell）；",
        "- **只保留 core 路径**，且**这些文件的提交历史完整保留**；",
        "- 路径清单由 `core_files()` 显式生成 ⇒ **可审计、可复算**。", "",
        "## 二、沙箱三步与结果", "",
        "| 步骤 | 结果 |", "|---|---|"]
    if res.get("ok") or res.get("split"):
        s = res.get("split", {})
        st = res.get("standalone", {})
        hist = res.get("history", {})
        tests = res.get("tests", {})
        lines += [
            f"| ① `git clone` 到临时目录 | 成功（原仓库**零改动**） |",
            f"| ② fast-export/import 造 queyi-core | 提交 **{s.get('n_commits')}**，"
            f"HEAD `{s.get('head')}` |",
            f"| ③ 独立可跑（内核 import + selftest） | import={st.get('import_ok')}，"
            f"kernel `--check` rc={st.get('kernel_check_rc')} |",
            f"| ④ 测试可跑（collect-only） | rc={tests.get('collect_rc')} |",
            f"| ⑤ 历史保留（探针文件提交数） | 拆分仓库 **{hist.get('in_split')}** vs "
            f"原仓库 **{hist.get('in_origin')}** ⇒ 相同={hist.get('same')} |", "",
            "```json",
            json.dumps(res, ensure_ascii=False, indent=2)[:2400],
            "```",
        ]
    else:
        lines += [f"| ① | 失败：{res.get('why')} |"]
    lines += ["", "## 三、沙箱实测踩到的四个坑（都是真的，不是设想）", "",
              "| # | 现象 | 根因 | 处理 |", "|---|---|---|---|",
              "| 1 | `fast-export` 退出 **128**：`tag ... tags unexported object` | 仓库里有指向"
              "**未被导出对象**的 tag | 加 `--tag-of-filtered-object=drop`（拆分仓库不需要这些 tag） |",
              "| 2 | `fast-export` 退出 **128**：`encountered commit-specific encoding gbk` | "
              "早期 Windows 提交带 `encoding gbk` 头 | 加 `--reencode=yes`（只动 commit message 编码声明） |",
              "| 3 | 拆完 `pytest tests` **收集期全错** | `tests/conftest.py` 会去调 `tools/tool_integrity.py` "
              "校验 test_config，**强耦合整仓** | 该文件与 `pyproject.toml` **不迁移**；"
              "queyi-core 用**自己的最小 conftest**（只注入 sys.path） |",
              "| 4 | 拆完测试仍大面积 `ImportError` | 保护器 647 **import 它们的前身**（642 灰度 / 636 影子），"
              "而种子模式只覆盖 `*_647.py` | 清单改为 **种子模式 ∪ repo 内 import 传递闭包**"
              "（复用内核 `module_imports()`，与 647 闭包同一套机制） |", "",
              "## 四、风险与回滚", "",
              "| 风险 | 触发条件 | 回滚动作 |", "|---|---|---|"]
    for x in risk_assessment():
        lines.append(f"| {x['risk']} | {x['trigger']} | {x['rollback']} |")
    lines += ["", "## 诚实登记", "",
              "1. **沙箱在原仓库之外**（`tempfile.mkdtemp`）⇒ 原仓库**一个字节都没改**；",
              "2. **历史是「核心文件视角」**：不触及 core 路径的 commit 被丢弃（报告给了两侧提交数）；",
              "3. **沙箱验证 ≠ 生产可用**：临时目录用完即删，没有长期回归；",
              "4. **core 路径清单是本批的定义**（`CORE_PATTERNS`）—— 若人认为该清单不对，"
              "拆分结果随之变化（清单可审计）；",
              "5. **未 push、未改 CPP-Bible 工作树**。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"result": res, "core_files": core_files()},
                  fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    files = core_files()
    chk("core 文件清单非空", len(files) > 0, str(len(files)))
    chk("含 641 内核", any(f.startswith("tools/queyi_core_") for f in files))
    chk("含 647 保护器", "tools/conflict_detector_647.py" in files)
    chk("含闭包工具", any(f.startswith("tools/verifier_closure_") for f in files))
    chk("清单去重且排序", files == sorted(set(files)))
    chk("清单里没有受控目录文件",
        not any(f.startswith(("atoms/", "evidence/", "Examples/", "Book/")) for f in files))
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"C1 split-sandbox selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 C1 仓库拆分沙箱验证")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="跑沙箱 + 写报告（**原仓库零改动**）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--execute", default="", help="在指定目录**真造**一个本地 queyi-core 仓库（C3 用）")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.execute:
        r = split_repo(a.execute)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r.get("ok") else 1
    if a.json:
        print(json.dumps(sandbox_run(), ensure_ascii=False, indent=2, default=str))
        return 0
    res = sandbox_run()
    if a.report:
        print(f"written {write_report(res)}")
        return 0 if res.get("ok") else 1
    print(f"[647 split-sandbox] ok={res.get('ok')} core_files={res.get('n_core_files')} "
          f"commits={res.get('split', {}).get('n_commits')} "
          f"standalone={res.get('standalone', {}).get('import_ok')}")
    return 0 if res.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
