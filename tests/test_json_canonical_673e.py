#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""673e 任务 B · JCS 规范化的**独立复现 + 覆盖面补齐**（671e 只锁了 3 个站点）。

673e 独立复现的结论（与 671e 一致的部分）：**不存在真实缺陷**——所有把内存 dict 喂进
hash 的站点都用了 `sort_keys=True`。

但 673e 发现 671e 的**覆盖面描述不准**：671e 报告写"唯一 3 处对内存 dict 做
`sha256(json.dumps(...))`"，而 AST 扫描（本文件）实测为 **20 个站点**（18 合规 + 2 处是
671e 自己故意用来演示风险的）。差异根因有两个：

  * 671e 用**正则**匹配 `sha256(\\s*json.dumps(`，看不见 `.encode()` 包装（3 个已知站点
    全都带 `.encode("utf-8")`，只是恰好被宽松正则兜住了）；
  * 正则看不见**经局部变量中转**的站点（如 `blob = json.dumps(...); sha256(blob)`），
    实测有 10 个这样的站点，671e 完全没覆盖。

本文件因此做两件事：
  1. 用 AST 枚举**全部** dict-哈希站点，逐个断言 `sort_keys=True`（白名单只放"故意演示"）；
  2. 锁住"经变量中转"这一类，防止将来新增时漏掉（正则型测试的盲区）。
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

HASH_ATTRS = {"sha256", "sha1", "md5", "sha512", "blake2b", "new"}
WRAPPERS = {"encode", "decode", "str", "bytes", "hexdigest"}

#: "故意不加 sort_keys 来演示风险"的文件白名单。
#: 按**文件**而不按内容白名单：673b 正在改 `test_json_canonical_671e.py`（实测它把演示行
#: 从 `json.dumps(a)` 重构成了 `json.dumps(_shuffled(a))`，内容白名单会因此误报）。
#: 代价：这两个文件内新增未加 sort_keys 的站点不会被本守卫抓到 —— 故下面另加一条
#: "演示站点必须位于演示函数内"的断言，把口子收窄。
DEMO_ALLOWLIST_FILES = (
    "tests/test_json_canonical_671e.py",
    "tests/test_json_canonical_673e.py",
)
#: 允许出现"故意无 sort_keys"的函数名特征。
DEMO_FUNC_HINTS = ("unsorted", "demonstrat", "would_differ", "risk", "shuffled")


def _unwrap(node):
    """剥掉 .encode(...)/.decode(...)/str(...)/bytes(...) 包装，返回最内层调用。

    坑（673e 实测踩到）：`x.encode("utf-8")` 的 `args[0]` 是**编码名**，接收者在
    `node.func.value`。写成 `node.args[0]` 会一路剥到字符串常量，什么都找不到。
    """
    while isinstance(node, ast.Call):
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr in WRAPPERS:
            node = f.value
            continue
        if isinstance(f, ast.Name) and f.id in WRAPPERS and node.args:
            node = node.args[0]
            continue
        return node
    return node


def _is_dumps(node) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    return ((isinstance(f, ast.Attribute) and f.attr == "dumps")
            or (isinstance(f, ast.Name) and f.id == "dumps"))


def _is_hash_call(node) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    if isinstance(f, ast.Attribute) and f.attr in HASH_ATTRS:
        return True
    return isinstance(f, ast.Name) and f.id in HASH_ATTRS


def _sort_keys_true(call) -> bool:
    for k in call.keywords:
        if k.arg == "sort_keys":
            return isinstance(k.value, ast.Constant) and k.value.value is True
    return False


def scan_dict_hash_sites(src: str):
    """返回 `[(lineno, sort_keys_bool, kind, code)]`；kind ∈ {direct, indirect}。"""
    tree = ast.parse(src)
    lines = src.splitlines()
    out = []

    for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))] or [tree]:
        dumps_vars = {}
        for sub in ast.walk(fn):
            if isinstance(sub, ast.Assign) and _is_dumps(_unwrap(sub.value)):
                for t in sub.targets:
                    if isinstance(t, ast.Name):
                        dumps_vars[t.id] = _sort_keys_true(_unwrap(sub.value))
            targets = []
            if _is_hash_call(sub):
                targets = list(sub.args)
            elif (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute)
                  and sub.func.attr == "update"):
                targets = list(sub.args)
            for a in targets:
                inner = _unwrap(a)
                if _is_dumps(inner):
                    out.append((sub.lineno, _sort_keys_true(inner), "direct",
                                lines[sub.lineno - 1].strip()))
                elif isinstance(inner, ast.Name) and inner.id in dumps_vars:
                    out.append((sub.lineno, dumps_vars[inner.id], "indirect",
                                lines[sub.lineno - 1].strip()))
    # 去重（嵌套函数会被重复遍历）
    return sorted(set(out))


def _all_sites():
    sites = []
    for base in ("tools", "tests"):
        for p in sorted((ROOT / base).rglob("*.py")):
            if "__pycache__" in p.parts:
                continue
            try:
                src = p.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            try:
                for ln, ok, kind, code in scan_dict_hash_sites(src):
                    sites.append((str(p.relative_to(ROOT)).replace("\\", "/"), ln, ok, kind, code))
            except SyntaxError:
                continue
    return sites


# ── 1. 核心守卫：任何 dict-哈希站点都必须 sort_keys=True ───────────────────────
def test_no_dict_hash_site_lacks_sort_keys():
    bad = [(f, ln, code) for f, ln, ok, _k, code in _all_sites()
           if not ok and f not in DEMO_ALLOWLIST_FILES]
    assert not bad, ("发现未加 sort_keys=True 的 dict-哈希站点（键序会改变哈希 ⇒ 复算失败）：\n"
                     + "\n".join(f"  {f}:{ln}  {c}" for f, ln, c in bad))


def test_demo_files_only_allow_unsorted_inside_demo_functions():
    """白名单口子收窄：允许无 sort_keys 的站点必须落在"演示用"函数名里。"""
    import re
    offenders = []
    for f in DEMO_ALLOWLIST_FILES:
        p = ROOT / f
        if not p.exists():
            continue
        src = p.read_text(encoding="utf-8")
        for ln, ok, _k, code in scan_dict_hash_sites(src):
            if ok:
                continue
            # 向上找最近的 def 行
            head = "\n".join(src.splitlines()[:ln])
            defs = re.findall(r"^\s*def\s+(\w+)", head, re.M)
            fn = defs[-1] if defs else ""
            if not any(h in fn.lower() for h in DEMO_FUNC_HINTS):
                offenders.append(f"{f}:{ln} in {fn}()  {code}")
    assert not offenders, ("演示文件里出现了非演示函数的无 sort_keys 站点：\n  "
                           + "\n  ".join(offenders))


def test_scanner_actually_finds_the_known_sites():
    """守卫必须"有牙齿"：扫描器得真的看见已知站点，否则空集合也能全绿。"""
    sites = _all_sites()
    assert len(sites) >= 15, f"扫描到的 dict-哈希站点过少（{len(sites)}）⇒ 扫描器可能失效"
    files = {f for f, _l, _o, _k, _c in sites}
    for must in ("tools/authority_projection_compiler_626.py",
                 "tools/e2e_attestation_629.py",
                 "tools/lifecycle_fsm_638.py"):
        assert must in files, f"已知站点所在文件 {must} 未被扫到"


def test_indirect_via_local_variable_sites_are_covered():
    """671e 的正则看不见"经变量中转"的站点；本扫描器必须看见（否则是同一个盲区）。"""
    indirect = [(f, ln) for f, ln, _ok, k, _c in _all_sites() if k == "indirect"]
    assert indirect, "没有扫到任何 indirect 站点 ⇒ 数据流追踪失效（这正是 671e 的盲区）"


def test_regex_would_miss_encode_wrapped_sites():
    """机理演示：正则 `sha256(\\s*json.dumps(` 对 `.encode()` 包装的站点会失手。"""
    import re
    src = (ROOT / "tools" / "authority_projection_compiler_626.py").read_text(encoding="utf-8")
    # 该站点的真实形态是 sha256(\n json.dumps(...)\n .encode("utf-8"))
    loose = re.search(r"sha256\(\s*json\.dumps\(", src, re.S)
    assert loose, "宽松正则（允许跨行空白）能兜住；但换行+encode 的形态更依赖运气"
    # 紧邻形态（不允许多余换行）会失手 —— 记录这个脆弱性
    tight = re.search(r"sha256\(json\.dumps\(", src)
    assert tight is None, "若紧邻正则也能命中，说明该站点形态变了，本注释需更新"


# ── 2. PoC：键序敏感性（风险真实存在）────────────────────────────────────────
def test_unsorted_dumps_is_key_order_sensitive_so_the_risk_is_real():
    a, b = {"b": 1, "a": 2}, {"a": 2, "b": 1}
    assert a == b
    assert json.dumps(a) != json.dumps(b), "两种键序的紧凑序列化应不同"
    assert (hashlib.sha256(json.dumps(a).encode()).hexdigest()
            != hashlib.sha256(json.dumps(b).encode()).hexdigest()), "无 sort_keys ⇒ 哈希随键序变"


def test_sorted_dumps_is_key_order_independent():
    a, b = {"b": 1, "a": 2}, {"a": 2, "b": 1}
    assert (hashlib.sha256(json.dumps(a, sort_keys=True).encode()).hexdigest()
            == hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest())


def test_nested_dict_key_order_also_matters():
    a = {"outer": {"z": 1, "a": 2}}
    b = {"outer": {"a": 2, "z": 1}}
    assert (hashlib.sha256(json.dumps(a, sort_keys=True).encode()).hexdigest()
            == hashlib.sha256(json.dumps(b, sort_keys=True).encode()).hexdigest()), \
        "sort_keys=True 必须递归生效"


# ── 3. 信任产物哈希的对象必须是文件字节 ───────────────────────────────────────
@pytest.mark.parametrize("tool,marker", [
    ("hash_datasets_670c.py", "sha256_file"),
    ("tool_integrity.py", "sha256_of"),
])
def test_trust_artifact_hashes_read_file_bytes(tool, marker):
    src = (ROOT / "tools" / tool).read_text(encoding="utf-8")
    assert marker in src, f"{tool} 应含字节级哈希函数 {marker}"


def test_byte_hash_is_intentionally_key_order_sensitive(tmp_path):
    """字节哈希**应当**对键序敏感——它抓的就是字节级漂移（与 dict 哈希的取向相反）。"""
    p1, p2 = tmp_path / "a.json", tmp_path / "b.json"
    p1.write_text(json.dumps({"b": 1, "a": 2}), encoding="utf-8")
    p2.write_text(json.dumps({"a": 2, "b": 1}), encoding="utf-8")
    h1 = hashlib.sha256(p1.read_bytes()).hexdigest()
    h2 = hashlib.sha256(p2.read_bytes()).hexdigest()
    assert h1 != h2
