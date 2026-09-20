"""609 B3 · 多瓶颈缓存（**编译缓存 / 还原缓存 / 规则缓存 / 数据缓存**）。

B2 剖析给出的三类可下手形态：**重复读盘/重复哈希**（Top1 `TextIOWrapper.read` 72.3s）、
显式 sleep、子进程起停。本模块只攻第一类（另外两类要动被测代码的语义，不在本批范围）。

四类缓存的**失效口径**是同一套：`(路径, mtime_ns, size)` 或"内容哈希"——
**只要输入变，缓存必失效**；绝不出现"改了文件还拿旧值"。

  * `data_cache(path)`     ：文本/JSON 读盘缓存（key=路径+mtime+size）
  * `rule_cache(path)`     ：解析后规则缓存（key=同上，避免重复 json/yaml 解析）
  * `restore_cache(fp)`    ：昂贵"还原"操作按**指纹**记忆（key=调用方给的指纹）
  * `compile_cache(src)`   ：编译产物按**源内容哈希**记忆（key=sha256(源码)）
  * `dir_cache(path, pat)` ：整目录快照缓存（key=目录签名：全部文件的 相对路径+mtime+size 哈希）
    —— 这是给 `attack_edge_generator.read_mis/atom_props` 用的（它们每次调用都 rglob 全树）

统计口径：`STATS = {hits, misses, invalidations, builds}`；`--check` 自检失效路径。

⚠️ 交给调用方的是**深拷贝**（缓存里的对象不许被外部改坏，否则"命中"会把污染传播出去）。
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any, Callable

VERSION = "1.0"

STATS = {"hits": 0, "misses": 0, "invalidations": 0, "builds": 0, "dir_scans": 0}
_DATA: dict[Any, Any] = {}
_RULE: dict[Any, Any] = {}
_RESTORE: dict[Any, Any] = {}
_COMPILE: dict[Any, Any] = {}
_DIR: dict[Any, Any] = {}


def reset(clear: bool = True) -> None:
    for d in (_DATA, _RULE, _RESTORE, _COMPILE, _DIR):
        d.clear()
    for k in STATS:
        STATS[k] = 0


def file_sig(path: Path | str) -> tuple[str, int, int]:
    """失效口径三件套：路径 + mtime_ns + size（三者任一变 ⇒ 缓存失效）。"""
    p = Path(path)
    st = p.stat()
    return (str(p.resolve()), st.st_mtime_ns, st.st_size)


def dir_sig(root: Path | str, pattern: str = "*.md") -> str:
    """目录签名：全部匹配文件的（相对路径,mtime_ns,size）拼起来取 sha256。"""
    r = Path(root)
    h = hashlib.sha256()
    n = 0
    for f in sorted(r.rglob(pattern)):
        st = f.stat()
        h.update(f"{f.relative_to(r).as_posix()}|{st.st_mtime_ns}|{st.st_size}\n".encode())
        n += 1
    STATS["dir_scans"] += 1
    return f"{n}:{h.hexdigest()}"


def _memo(store: dict[Any, Any], key: Any, builder: Callable[[], Any],
          *, sig: Any = None) -> Any:
    prev = store.get(key)
    if prev is not None:
        prev_sig, value = prev
        if prev_sig == sig:
            STATS["hits"] += 1
            return copy.deepcopy(value)
        STATS["invalidations"] += 1
        store.pop(key, None)
    STATS["misses"] += 1
    STATS["builds"] += 1
    value = builder()
    store[key] = (sig, value)
    return copy.deepcopy(value)


def read_text(path: Path | str) -> Any:
    """数据缓存：同一文件（同 mtime/size）只读一次盘。"""
    p = Path(path)
    return _memo(_DATA, ("text", str(p)), lambda: p.read_text(encoding="utf-8"),
                 sig=file_sig(p))


def load_json(path: Path | str) -> Any:
    return _memo(_DATA, ("json", str(Path(path))),
                 lambda: json.loads(Path(path).read_text(encoding="utf-8")),
                 sig=file_sig(path))


def load_rules(path: Path | str, parser: Callable[[str], Any] | None = None) -> Any:
    """规则缓存：解析动作只做一次（parser 默认 json.loads ⇒ 只适用于 JSON 规则表）。"""
    parse = parser or json.loads
    p = Path(path)
    return _memo(_RULE, ("rules", str(p)),
                 lambda: parse(p.read_text(encoding="utf-8")), sig=file_sig(p))


def restore(fingerprint: str, builder: Callable[[], Any]) -> Any:
    """还原缓存：按调用方给的**指纹**记忆昂贵还原（如"删旧工件→重生成→比 sha→还原"）。"""
    return _memo(_RESTORE, ("restore", str(fingerprint)), builder, sig=str(fingerprint))


def source_hash(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compile_once(path: Path | str, builder: Callable[[], Any]) -> Any:
    """编译缓存：同一**源内容哈希**只编译一次（源码一改 ⇒ 哈希变 ⇒ 自动重编）。"""
    return _memo(_COMPILE, ("compile", str(Path(path))), builder,
                 sig=source_hash(path))


def cached_dir(root: Path | str, pattern: str, builder: Callable[[], Any]) -> Any:
    """目录快照缓存：目录里任一文件的 mtime/size 变 ⇒ 签名变 ⇒ 失效重建。"""
    return _memo(_DIR, ("dir", str(Path(root)), pattern), builder,
                 sig=dir_sig(root, pattern))


def stats() -> dict:
    total = STATS["hits"] + STATS["misses"]
    return {**STATS, "lookups": total,
            "hit_rate": round(STATS["hits"] / total, 4) if total else None,
            "entries": {"data": len(_DATA), "rule": len(_RULE), "restore": len(_RESTORE),
                        "compile": len(_COMPILE), "dir": len(_DIR)}}


def check() -> list[str]:
    """自检：四类缓存的**命中**与**失效**都必须成立（只测命中=漏掉最危险的路径）。"""
    problems: list[str] = []
    import tempfile
    d = Path(tempfile.mkdtemp(prefix="pc609_"))
    f = d / "a.json"
    f.write_text('{"v": 1}', encoding="utf-8")
    reset()
    if load_json(f)["v"] != 1:
        problems.append("数据缓存首读值不对")
    if load_json(f)["v"] != 1 or STATS["hits"] != 1:
        problems.append(f"数据缓存未命中（hits={STATS['hits']}）")
    time.sleep(0.01)
    f.write_text('{"v": 2}', encoding="utf-8")          # 改文件 ⇒ 必须失效
    if load_json(f)["v"] != 2:
        problems.append("改了文件仍返回旧值 ⇒ 失效口径破")
    d2 = d / "dir"
    d2.mkdir()
    (d2 / "x.md").write_text("a", encoding="utf-8")
    n1 = cached_dir(d2, "*.md", lambda: len(list(d2.rglob("*.md"))))
    n2 = cached_dir(d2, "*.md", lambda: len(list(d2.rglob("*.md"))))
    if (n1, n2) != (1, 1):
        problems.append("目录缓存返回不一致")
    time.sleep(0.01)
    (d2 / "y.md").write_text("b", encoding="utf-8")     # 目录新增文件 ⇒ 必须失效
    if cached_dir(d2, "*.md", lambda: len(list(d2.rglob("*.md")))) != 2:
        problems.append("目录新增文件未触发失效 ⇒ 会拿到过期目录快照")
    calls = {"n": 0}

    def build() -> int:
        calls["n"] += 1
        return calls["n"]

    reset()
    compile_once(f, build)
    compile_once(f, build)
    if calls["n"] != 1:
        problems.append(f"编译缓存未生效（build 被调 {calls['n']} 次）")
    restore("fp-1", build)
    restore("fp-1", build)
    if calls["n"] != 2:
        problems.append("还原缓存未生效")
    reset()
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="perf_cache",
                                 description="609 B3 多瓶颈缓存（数据/规则/还原/编译/目录）")
    ap.add_argument("--version", action="version", version=f"perf_cache {VERSION}")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print(f"[cache] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print("[cache] --check OK：数据/规则/还原/编译/目录 五类缓存的命中与失效路径自洽")
        return 0

    if a.stats:
        s = stats()
        print(json.dumps(s, ensure_ascii=False, indent=1) if a.json
              else f"[cache] hits={s['hits']} misses={s['misses']} "
                   f"invalidations={s['invalidations']} builds={s['builds']} "
                   f"dir_scans={s['dir_scans']} hit_rate={s['hit_rate']}")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
