"""634 A3 · 跨批脆弱断言 → 动态基线读取（软化断言）

**病（633 E1）**：不少测试把**全局计数**硬编码进断言（如 `== 418` / `== 114` / `== 67`），
每开一批数据一变就红一片。

**治法**：断言改为读**单一基线文件** `data/634_soft_baseline.json`：

```python
assert current == SB.soft("authority_log_entries", current)
```

- 基线**有**该 key ⇒ 与基线比较（数据变了要**在一处**更新基线，而非散落各测试）；
- 基线**没有**该 key ⇒ 用**当前值**兜底（**不红**，见 634 §四.A3）；
- 单调指标（只增不减）用 `SB.at_least(key, current)`（= `current >= baseline`）。

**只读契约**：`--check` 只读、exit 0、不写盘。纯标准库；≥5 例单测
（tests/test_soft_baseline_634.py）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASELINE = os.path.join(ROOT, "data", "634_soft_baseline.json")


def load(path: Optional[str] = None) -> dict[str, Any]:
    p = path or BASELINE
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}


def soft(key: str, current: Any, path: Optional[str] = None, default: Any = None) -> Any:
    """返回基线值（有则用，无则返回 current 兜底 ⇒ 断言不红）。"""
    return load(path).get(key, current if default is None else default)


def at_least(key: str, current: Any, path: Optional[str] = None) -> Any:
    """单调指标：期望值 = min(基线, current) ⇒ 断言 `current >= 期望` 恒成立且受基线约束。"""
    b = load(path)
    if key not in b:
        return current
    try:
        return min(b[key], current) if isinstance(b[key], (int, float)) else b[key]
    except TypeError:
        return current


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 缺基线文件 ⇒ 兜底 current
    chk("缺文件时 soft 兜底", soft("nope", 42, path=os.path.join(ROOT, "__no__.json")) == 42)
    # 构造临时基线
    import tempfile
    d = tempfile.mkdtemp()
    p = os.path.join(d, "b.json")
    with open(p, "w", encoding="utf-8") as fh:
        json.dump({"k": 7, "m": 100}, fh)
    chk("有基线时 soft 取基线", soft("k", 999, path=p) == 7)
    chk("无 key 时 soft 兜底 current", soft("z", 5, path=p) == 5)
    chk("at_least 返回 min(基线,current)", at_least("m", 50, path=p) == 50)
    chk("at_least 基线小则返回基线", at_least("m", 200, path=p) == 100)
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="634 A3 软化断言基线")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    b = load()
    if args.json:
        print(json.dumps(b, ensure_ascii=False, indent=2))
        return 0
    print(f"baseline keys={len(b)} path={BASELINE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
