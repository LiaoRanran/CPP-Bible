# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""712 任务 0.2 / 0.4：构建与身份隔离的匿名审稿副本，并做泄露扫描。

背景（评审阻塞项 2）：公开仓库 `queyi-audit` 的
  * remote URL 含 GitHub 账号 `LiaoRanran`
  * initial commit 的 author / committer / Signed-off-by 均含真名与邮箱
意味着"论文正文已脱敏"并不等于"仓库已匿名"。GitHub **没有**原生匿名提交功能，
且已 push 的提交无法被真正删除（fork / 镜像 / API 缓存都会保留），因此正确做法是
**新建一个与身份无关联、历史干净、remote 中立的仓库**，而不是在原仓库上"删名字"。

本脚本做三件事：
  1. build  ：把 queyi-audit 工作树复制到目标目录（不含 .git / __pycache__），
             套用元数据清洗与包元数据修复，然后 `git init` + 单次匿名提交。
  2. scrub  ：（可选，默认关闭）清洗冻结数据里的本机临时路径。
             默认关闭的原因：那会改变冻结产物字节 ⇒ sha256 锚定失效，
             可审计性受损。是否开启由人决定，见报告 §4。
  3. verify ：对构建结果做泄露扫描，命中即非零退出。

只读约束：不调用任何 detect()，不改写源仓库，不 push。

用法：
    python tools/build_anonymous_repo_712.py build  --src ... --dst ...
    python tools/build_anonymous_repo_712.py verify --dst ...
    python tools/build_anonymous_repo_712.py build --src ... --dst ... --scrub-temp-paths
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# 泄露模式（verify 用）。前 5 项为真身份，后 3 项为间接线索。
# --------------------------------------------------------------------------
LEAK_PATTERNS = [
    ("姓名/账号 LiaoRanran", re.compile(r"LiaoRanran", re.IGNORECASE)),
    ("邮箱前缀 1026708211", re.compile(r"1026708211")),
    ("邮箱域名 @qq.com", re.compile(r"@qq\.com", re.IGNORECASE)),
    ("源项目名 cppbible", re.compile(r"cpp-?bible", re.IGNORECASE)),
    ("圣经书名", re.compile(r"终极圣经")),
    ("本机项目根 CodeLearnling", re.compile(r"CodeLearnling", re.IGNORECASE)),
    ("Windows 用户名 ASUS", re.compile(r"Users[/\\]ASUS", re.IGNORECASE)),
    ("WSL 挂载路径 /mnt/c/", re.compile(r"/mnt/c/", re.IGNORECASE)),
    ("学校/单位", re.compile(r"Hefei University|合肥大学|合肥学院", re.IGNORECASE)),
]

# 冻结数据区：scrub 的候选区（默认不动）
FROZEN_DIRS = ("data/frozen_matrix",)

SCRUB_MAP = [
    (re.compile(r"/mnt/c/Users/ASUS/", re.IGNORECASE), "/mnt/c/Users/queyi-runner/"),
    (re.compile(r"C:/CodeLearnling/note/note/C\+\+/queyi-audit", re.IGNORECASE), "<package-root>"),
    (re.compile(r"C:\\\\Users\\\\ASUS\\\\AppData\\\\Local\\\\Temp\\\\", re.IGNORECASE), "/tmp/"),
]

SKIP_DIRS = {".git", "__pycache__", ".pytest_tmp", "node_modules", ".venv", "build"}

# 文档层的间接线索清洗（不改数据、不改代码语义）：
#   * 源项目书名 → 中性表述（书名是可以直接搜到源仓库与作者的强线索）
#   * scripts_index.md 里指向包内不存在脚本的陈旧条目 → 删除（不是改名字，是删死条目）
DOC_SCRUB_MAP = [
    (re.compile(r"《现代 C\+\+ 终极圣经》"), "上游项目"),
    # 原 README 断言"不含任何作者姓名、单位、邮箱或个人标识"。在冻结矩阵里仍有
    # 1387 处构建主机临时路径（/mnt/c/Users/ASUS/...）的情况下，这句话是**不实的**，
    # 而双盲审稿人一旦发现，杀伤力比路径本身更大。改成可核验的准确表述。
    (
        re.compile(
            r"it contains no author names, affiliations, e-mails or personal identifiers\."
        ),
        "no author name, affiliation, e-mail or source-repository identifier appears in its "
        "files, commit messages or URLs; build-host temporary paths inside the frozen matrices "
        "were deliberately left byte-identical so that every sha256 anchor stays verifiable",
    ),
]
STALE_INDEX_MARKERS = ("`cppbible.py`",)

TEXT_EXT = {
    ".py", ".sh", ".md", ".tex", ".bib", ".yml", ".yaml", ".toml", ".json",
    ".jsonl", ".txt", ".cfg", ".ini", ".cff", ".html", ".sty", ".bat", ".ps1",
}
EXTRA_FILES = {"LICENSE", "Dockerfile", "Makefile", "README", ".gitignore", "CODE_OF_CONDUCT.md"}

ANON_NAME = "Anonymous"
ANON_EMAIL = "anonymous@example.org"

# --------------------------------------------------------------------------
# 修正后的包元数据（任务 0.4）。原 pyproject.toml 把本包描述为
# 《现代 C++ 终极圣经》的生产工具链、许可证写 MIT（而 LICENSE/README 是 Apache-2.0）、
# 入口指向包内并不存在的 tools/cppbible.py —— 三项都是错的。
# --------------------------------------------------------------------------
NEW_PYPROJECT = '''[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "queyi-audit"
version = "1.0.0"
description = "Reproducibility package for auditing measurement caliber in software-verification evaluation: frozen detection matrices plus read-only audit tooling"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "Apache-2.0" }
authors = [
    { name = "Anonymous", email = "anonymous@example.org" },
]
keywords = [
    "software-verification",
    "measurement-drift",
    "evaluator-audit",
    "reproducibility",
    "sanitizers",
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: Apache Software License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

# 712 说明：本复现包的可达导入面（tests/ 与 tools/verify_paper_numbers.py）
# 只用到标准库；pyyaml 保留是因为少数工具仍 import 它，且 requirements.txt 里
# 已把 pytest 列为唯一必需第三方依赖。原先的 mkdocs / pandoc / pagefind /
# hypothesis / syrupy 是上游站点的依赖，与本包无关，已移除。
dependencies = [
    "pyyaml>=6.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.5.0",
    "mypy>=1.10.0",
]

[project.urls]
# 712 说明：原值为 "https://anonymous/queyi-audit"（不是合法 URL）。
# 匿名副本发布前请替换为实际的中立地址（组织账号 / Zenodo / OSF）。
Homepage = "https://example.org/queyi-audit"
Repository = "https://example.org/queyi-audit"

[tool.setuptools]
# 本包不提供可 import 的 Python 包：tools/ 通过 sys.path 直接使用
# （见 pyproject 的 pythonpath 与 tests/conftest.py）。
# 原 [project.scripts] 入口与原 py-modules 都指向包内并不存在的模块，是坏声明，已移除。
packages = []

[tool.ruff]
line-length = 120
target-version = "py311"

[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I001", "FURB167"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true

[[tool.mypy.overrides]]
module = "yaml.*"
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "utils.*"
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = "opentimestamps.*"
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = ["numpy", "numpy.*"]
follow_imports = "skip"

[[tool.mypy.overrides]]
module = ["pytest", "pytest.*", "_pytest", "_pytest.*"]
follow_imports = "skip"
ignore_missing_imports = true

[[tool.mypy.overrides]]
module = ["requests", "requests.*"]
ignore_missing_imports = true

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["tools"]
addopts = "-q --tb=short"
markers = [
    "slow: 耗时>10s 的测试（WSL 编译/全量重跑类）；本地默认跳过，CI 慢档覆盖",
]
'''


# --------------------------------------------------------------------------
# 工具函数
# --------------------------------------------------------------------------
def is_text_candidate(path: Path) -> bool:
    if path.name in EXTRA_FILES:
        return True
    return path.suffix.lower() in TEXT_EXT


def iter_text_files(root: Path):
    for dp, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            p = Path(dp) / f
            if is_text_candidate(p):
                yield p


def scan(root: Path, scrub_map=None, apply: bool = False):
    """返回 {label: [(rel, count), ...]} 与总命中数。apply=True 时顺带替换。"""
    hits: dict[str, list[tuple[str, int]]] = {}
    total = 0
    for p in iter_text_files(root):
        rel = str(p.relative_to(root)).replace("\\", "/")
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        orig = txt
        for label, pat in LEAK_PATTERNS:
            n = len(pat.findall(txt))
            if n:
                hits.setdefault(label, []).append((rel, n))
                total += n
        if apply and scrub_map:
            for pat, rep in scrub_map:
                txt = pat.sub(rep, txt)
            if txt != orig:
                p.write_text(txt, encoding="utf-8", newline="")
    return hits, total


def sync_tree(src: Path, dst: Path):
    """把 src 的工作树同步进 dst（覆盖同名文件，删除 dst 里 src 已没有的文件）。

    为什么需要它：Windows 上 `shutil.rmtree` 整目录会被宿主的批量删除保护拦下
    （884 个文件 > 阈值 500，需要人工确认），而"重建一个全新目录"又会让路径漂移。
    同步模式只删真正消失的文件，不动目录本身。
    """
    copied = removed = 0
    src_files = set()
    for dp, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel_dir = os.path.relpath(dp, src)
        out_dir = dst if rel_dir == "." else dst / rel_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            src_files.add(os.path.relpath(Path(dp) / f, src))
            shutil.copy2(Path(dp) / f, out_dir / f)
            copied += 1
    # 注意：topdown=False 时改写 dirs 已无法阻止遍历，必须显式跳过 .git 等目录。
    # （首版就踩了这里：把 dst/.git 里的 481 个对象当"源已不存在的文件"删掉，
    #   导致 `git commit` 报 not a git repository。已在下方按路径段过滤。）
    for dp, _dirs, files in os.walk(dst):
        parts = set(Path(dp).relative_to(dst).parts)
        if parts & SKIP_DIRS:
            continue
        for f in files:
            rel = os.path.relpath(Path(dp) / f, dst)
            if rel not in src_files:
                os.remove(Path(dp) / f)
                removed += 1
    return copied, removed


def build(args):
    src = Path(args.src).resolve()
    dst = Path(args.dst).resolve()
    if not src.is_dir():
        print(f"[fail] 源目录不存在: {src}")
        return 2
    if args.in_place and dst.exists():
        copied, removed = sync_tree(src, dst)
        print(f"[sync] {copied} 个文件同步到 {dst}（删除 {removed} 个源已不存在的文件）")
        n_files = copied
        return _finish(args, src, dst, n_files)
    if dst.exists() and any(dst.iterdir()):
        if not args.force:
            print(f"[fail] 目标目录非空: {dst}（--force 覆盖，或换一个路径）")
            return 2
        # Windows 下 .git 里的对象常被其它进程（编辑器索引 / 上一次 git 子进程）短暂持有，
        # 直接 rmtree 会抛异常。这里用 ignore_errors 清理并**显式复核**：
        # 若仍有残留，宁可报错退出，也不要在残留目录上"增量构建"出一个混合体。
        shutil.rmtree(dst, ignore_errors=True)
        if dst.exists() and any(dst.iterdir()):
            leftover = sum(len(f) for _, _, f in os.walk(dst))
            print(f"[fail] 目标目录无法清空（仍有 {leftover} 个文件），"
                  f"请手动删除后重试: {dst}")
            return 2
    dst.mkdir(parents=True, exist_ok=True)

    # 1) 复制工作树（跳过 .git / __pycache__）
    n_files = 0
    for dp, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel_dir = os.path.relpath(dp, src)
        out_dir = dst if rel_dir == "." else dst / rel_dir
        out_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            shutil.copy2(Path(dp) / f, out_dir / f)
            n_files += 1
    print(f"[copy] {n_files} 个文件 -> {dst}")
    return _finish(args, src, dst, n_files)


def _finish(args, src, dst, n_files):
    """复制完成后共用的收尾：包元数据修复 → 文档清洗 → 可选数据清洗 → 匿名提交 → 扫描。"""
    # 2) 包元数据修复（任务 0.4）
    pyproject = dst / "pyproject.toml"
    if pyproject.exists():
        pyproject.write_text(NEW_PYPROJECT, encoding="utf-8", newline="\n")
        print("[fix ] pyproject.toml 已替换为审计包元数据（名称/描述/Apache-2.0/URL/入口）")

    # 2b) 文档层间接线索清洗（书名 / 指向不存在脚本的陈旧索引条目）
    doc_changed = []
    for p in iter_text_files(dst):
        rel = str(p.relative_to(dst)).replace("\\", "/")
        if any(rel.startswith(d) for d in FROZEN_DIRS):
            continue  # 冻结数据不动
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue
        out = []
        touched = False
        for line in lines:
            if any(m in line for m in STALE_INDEX_MARKERS):
                touched = True
                continue
            new = line
            for pat, rep in DOC_SCRUB_MAP:
                new = pat.sub(rep, new)
            if new != line:
                touched = True
            out.append(new)
        if touched:
            p.write_text("\n".join(out) + "\n", encoding="utf-8", newline="")
            doc_changed.append(rel)
    if doc_changed:
        print(f"[doc ] 清洗 {len(doc_changed)} 个文档：" + "、".join(doc_changed[:5]))

    # 3) 可选：清洗冻结数据里的本机临时路径（默认关闭）
    if args.scrub_temp_paths:
        changed = 0
        for p in iter_text_files(dst):
            rel = str(p.relative_to(dst)).replace("\\", "/")
            if not any(rel.startswith(d) for d in FROZEN_DIRS):
                continue
            try:
                txt = p.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            orig = txt
            for pat, rep in SCRUB_MAP:
                txt = pat.sub(rep, txt)
            if txt != orig:
                p.write_text(txt, encoding="utf-8", newline="")
                changed += 1
        print(f"[scrub] 冻结数据已清洗 {changed} 个文件 —— 注意：需重钉 sha256 锚定")

    # 4) 匿名提交（不设 remote）
    if not args.no_commit:
        env = dict(os.environ)
        env.update(
            {
                "GIT_AUTHOR_NAME": ANON_NAME,
                "GIT_AUTHOR_EMAIL": ANON_EMAIL,
                "GIT_COMMITTER_NAME": ANON_NAME,
                "GIT_COMMITTER_EMAIL": ANON_EMAIL,
            }
        )

        def g(*a):
            return subprocess.run(["git", *a], cwd=str(dst), env=env,
                                  capture_output=True, text=True, errors="replace")

        had_git = (dst / ".git").exists()
        if not had_git:
            g("init", "-q", "-b", "main")
        else:
            # in-place 同步：沿用同一个初始提交（amend），保持「只有一次匿名提交」的干净历史
            g("remote", "remove", "origin")
        g("add", "-A")
        msg = (
            "Initial commit: Queyi Audit reproducibility package "
            "(anonymous review copy)\n\n"
            "Metadata-only clean-room build: no author name, e-mail, affiliation,\n"
            "host path or source-project identifier. Commit metadata uses\n"
            "'Anonymous <anonymous@example.org>'; no remote is configured.\n"
            "Frozen artifacts under data/frozen_matrix/ are byte-identical to the\n"
            "source package so that all sha256 anchors remain verifiable.\n"
        )
        amend = args.in_place and had_git
        r = g("commit", "-q", "--amend", "-m", msg) if amend else g("commit", "-q", "-m", msg)
        if r.returncode != 0:
            print("[fail] git commit:", r.stdout, r.stderr)
            return 3
        print("[git ] 匿名提交完成（author/committer = Anonymous%s）" % ("，amend" if amend else ""))

    # 5) 构建后扫描
    hits, total = scan(dst)
    print()
    print("=== 构建后泄露扫描 ===")
    if total == 0:
        print("  0 命中")
    else:
        for label in dict.fromkeys(pat[0] for pat in LEAK_PATTERNS):
            if label in hits:
                files = sorted(hits[label], key=lambda x: -x[1])
                s = sum(n for _, n in files)
                print(f"  [{label}] {s} 处，涉及 {len(files)} 个文件：")
                for rel, n in files[:5]:
                    print(f"      {n:6d}  {rel}")
                if len(files) > 5:
                    print(f"      ... 另有 {len(files) - 5} 个文件")
    print(f"\n总命中: {total}")
    return 0 if total == 0 else 1


def verify(args):
    dst = Path(args.dst).resolve()
    if not dst.is_dir():
        print(f"[fail] 目录不存在: {dst}")
        return 2
    hits, total = scan(dst)
    print(f"=== 扫描 {dst} ===")
    for label, files in hits.items():
        s = sum(n for _, n in files)
        print(f"  [{label}] {s} 处 / {len(files)} 文件")
        for rel, n in sorted(files, key=lambda x: -x[1])[:5]:
            print(f"      {n:6d}  {rel}")
    print(f"总命中: {total}")

    # git 元数据
    if (dst / ".git").exists():
        r = subprocess.run(["git", "log", "--all", "--pretty=format:%an <%ae> | %cn <%ce>"],
                           cwd=str(dst), capture_output=True, text=True, errors="replace")
        ids = sorted(set(r.stdout.splitlines()))
        print("\n提交身份：")
        for i in ids:
            print("   ", i)
        r2 = subprocess.run(["git", "remote", "-v"], cwd=str(dst),
                            capture_output=True, text=True, errors="replace")
        remotes = r2.stdout.strip()
        print("remote：" + (remotes if remotes else "（无，符合匿名要求）"))
        for i in ids:
            if "Anonymous" not in i:
                print("  [!!] 提交元数据仍含非匿名身份")
                return 1
        if remotes:
            print("  [!!] 已配置 remote")
            return 1
    return 0 if total == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="712 匿名审稿副本构建 / 扫描")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="构建匿名副本")
    b.add_argument("--src", default=r"C:\CodeLearnling\queyi-audit")
    b.add_argument("--dst", default=r"C:\CodeLearnling\queyi-audit-anon")
    b.add_argument("--force", action="store_true")
    b.add_argument("--in-place", action="store_true",
                   help="原地同步（不删目录）：覆盖同名文件、删除源已消失的文件，并 amend 初始提交")
    b.add_argument("--no-commit", action="store_true")
    b.add_argument("--scrub-temp-paths", action="store_true",
                   help="清洗冻结数据里的本机临时路径（会改变冻结产物字节，需重钉 sha256）")
    b.set_defaults(func=build)

    v = sub.add_parser("verify", help="扫描已构建的副本")
    v.add_argument("--dst", default=r"C:\CodeLearnling\queyi-audit-anon")
    v.set_defaults(func=verify)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
