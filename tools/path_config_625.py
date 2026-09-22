"""625 C1 · QueYi Core 路径配置（路径解耦第一步）

**目的**：让核心/辅助工具**不再写死** CPP-Bible 特定路径（`atoms/`、`evidence/`、`data/` …），
而由本模块统一解析，便于 QueYi Core 剥离后换靶场（触发标准⑤）。

**加载顺序**（后者覆盖前者）：
1. **默认值**（CPP-Bible 仓根 = `tools/` 的父目录）；
2. **配置文件** `queyi_config.json`（仓根或 `$QUEYI_CONFIG` 指定）；
3. **环境变量**（`QUEYI_ROOT` / `QUEYI_ATOMS_DIR` / `QUEYI_EVIDENCE_DIR` / `QUEYI_DATA_DIR` /
   `QUEYI_EXAMPLES_DIR` / `QUEYI_BOOK_DIR`）。

**向后兼容（硬要求）**：不设环境变量/配置文件时，解析结果与当前**完全一致**（默认 = 仓根派生）。

铁律：只做路径解析，不含任何业务逻辑；必有 `--check`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = HERE.parent


def _load_file_config() -> dict:
    """读 `queyi_config.json`（`$QUEYI_CONFIG` 优先，否则仓根）。缺失/损坏 ⇒ 空。"""
    cand = os.environ.get("QUEYI_CONFIG")
    p = Path(cand) if cand else (DEFAULT_ROOT / "queyi_config.json")
    if not p.is_file():
        return {}
    try:
        with open(p, encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _resolve(env: str, conf_key: str, default: Path) -> Path:
    if os.environ.get(env):
        return Path(os.environ[env])
    conf = _load_file_config()
    if conf.get(conf_key):
        return Path(str(conf[conf_key]))
    return default


def root() -> Path:
    """仓根：`QUEYI_ROOT` > config.root > 默认（tools 父目录）。"""
    return _resolve("QUEYI_ROOT", "root", DEFAULT_ROOT)


def atoms_dir() -> Path:
    return _resolve("QUEYI_ATOMS_DIR", "atoms_dir", root() / "atoms")


def evidence_dir() -> Path:
    return _resolve("QUEYI_EVIDENCE_DIR", "evidence_dir", root() / "evidence")


def data_dir() -> Path:
    return _resolve("QUEYI_DATA_DIR", "data_dir", root() / "data")


def examples_dir() -> Path:
    return _resolve("QUEYI_EXAMPLES_DIR", "examples_dir", root() / "Examples")


def book_dir() -> Path:
    return _resolve("QUEYI_BOOK_DIR", "book_dir", root() / "Book")


def tools_dir() -> Path:
    return root() / "tools"


# ---- 解析函数（按 id/文件名 → 路径）----

def resolve_atom_path(atom_id: str) -> Path:
    return atoms_dir() / f"{atom_id}.md"


def resolve_evidence_path(evidence_id: str) -> Path:
    return evidence_dir() / f"{evidence_id}.md"


def resolve_mutation_path(mutation_id: str) -> Path:
    return data_dir() / "mutation" / f"{mutation_id}.json"


def resolve_data_path(filename: str) -> Path:
    return data_dir() / filename


def validate() -> list[str]:
    """路径存在性/可写性自检；返回问题清单（空 = 通过）。"""
    problems: list[str] = []
    r = root()
    if not r.is_dir():
        problems.append(f"根目录不存在：{r}")
    for name, d in (("atoms", atoms_dir()), ("evidence", evidence_dir()), ("data", data_dir())):
        if not d.is_dir():
            problems.append(f"{name} 目录不存在：{d}")
    # 可写性：data 目录
    dd = data_dir()
    if dd.is_dir() and not os.access(dd, os.W_OK):
        problems.append(f"data 目录不可写：{dd}")
    return problems


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("默认 root = tools 父目录", root() == DEFAULT_ROOT)
    chk("默认 atoms/evidence/data 派生自 root", atoms_dir() == root() / "atoms"
        and evidence_dir() == root() / "evidence" and data_dir() == root() / "data")
    chk("resolve_atom_path 派生正确", resolve_atom_path("ATOM-X") == atoms_dir() / "ATOM-X.md")
    chk("resolve_data_path 派生正确", resolve_data_path("a.json") == data_dir() / "a.json")
    chk("路径自检可调用", isinstance(validate(), list))
    print(f"C1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="625 C1 QueYi Core 路径配置")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--show", action="store_true", help="打印解析后的路径")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.show:
        print(json.dumps({"root": str(root()), "atoms": str(atoms_dir()),
                          "evidence": str(evidence_dir()), "data": str(data_dir()),
                          "examples": str(examples_dir()), "book": str(book_dir())},
                         ensure_ascii=False, indent=2))
        return 0
    problems = validate()
    print(json.dumps({"problems": problems}, ensure_ascii=False))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
