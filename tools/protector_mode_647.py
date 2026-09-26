"""647 B5（公共件）· **保护器全局模式开关**（一键回滚到 642 灰度）。

647 把五个保护器从「灰度（只标记）」推到「真上岗（会拦/会冻/会降级）」，
**风险是误拦**。因此给一个**单一开关**：

```
QUEYI_PROTECTOR_MODE = enforce | shadow     # 默认 enforce（647 上岗）
```

* `enforce`：保护器的**强制动作**生效（block / 冻结 / 强制盲化 / 降级 / 拒绝上线）；
* `shadow`：退化成 642 的灰度行为（**只标记，不改判决**）—— 回滚成本为零。

读取顺序（高 → 低）：环境变量 `QUEYI_PROTECTOR_MODE` > 模式文件 `data/647_protector_mode.json`
> 默认 `enforce`。`--rollback` 写模式文件为 `shadow`（**可逆**：`--enforce` 写回）。

**诚实登记**：模式文件是**本机状态**（未入 git 也能生效），
它的存在意味着「保护器上岗与否」是**运行期可切**的 —— 这正是回滚设计，也是审计时必须一并记录的状态。

CLI：`--check`（只读自检）/ `--status` / `--rollback`（切 shadow）/ `--enforce`（切回 enforce）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MODE_FILE = os.path.join(ROOT, "data", "647_protector_mode.json")
ENV = "QUEYI_PROTECTOR_MODE"
MODE_ENFORCE = "enforce"
MODE_SHADOW = "shadow"
MODES = (MODE_ENFORCE, MODE_SHADOW)
DEFAULT_MODE = MODE_ENFORCE


def _from_env() -> Optional[str]:
    v = os.environ.get(ENV, "").strip().lower()
    return v if v in MODES else None


def _from_file() -> Optional[str]:
    try:
        with open(MODE_FILE, encoding="utf-8") as fh:
            v = str(json.load(fh).get("mode", "")).strip().lower()
        return v if v in MODES else None
    except (OSError, ValueError, TypeError):
        return None


def mode() -> str:
    """当前模式（env > 文件 > 默认 enforce）。"""
    return _from_env() or _from_file() or DEFAULT_MODE


def is_enforce() -> bool:
    """是否处于**真上岗**（会拦截）模式。所有强制动作前都必须先问这一句。"""
    return mode() == MODE_ENFORCE


def source() -> str:
    if _from_env():
        return f"环境变量 {ENV}"
    if _from_file():
        return f"模式文件 {os.path.relpath(MODE_FILE, ROOT).replace(os.sep, '/')}"
    return "默认值"


def set_mode(m: str) -> str:
    """写模式文件（**运行期状态**，不碰代码）。返回写入后的模式。"""
    if m not in MODES:
        raise ValueError(f"模式非法：{m!r} ∉ {MODES}")
    os.makedirs(os.path.dirname(MODE_FILE), exist_ok=True)
    with open(MODE_FILE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"mode": m, "env_override": ENV,
                   "note": "647 保护器全局开关；shadow = 一键回滚到 642 灰度"}, fh,
                  ensure_ascii=False, indent=2)
        fh.write("\n")
    return m


def rollback() -> str:
    """**一键回滚**：切成 shadow（保护器只标记、不拦截）。"""
    return set_mode(MODE_SHADOW)


def enforce() -> str:
    """切回 enforce（撤销回滚）。"""
    return set_mode(MODE_ENFORCE)


def status() -> dict:
    return {"mode": mode(), "source": source(), "default": DEFAULT_MODE,
            "env": os.environ.get(ENV, ""), "mode_file": os.path.relpath(MODE_FILE, ROOT).replace(os.sep, "/"),
            "mode_file_exists": os.path.isfile(MODE_FILE)}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("默认是 enforce（647 上岗）", DEFAULT_MODE == MODE_ENFORCE)
    chk("环境变量优先", MODES == ("enforce", "shadow"))
    saved = os.environ.get(ENV)
    try:
        os.environ[ENV] = MODE_SHADOW
        chk("env=shadow ⇒ is_enforce False", is_enforce() is False and source().startswith("环境变量"))
        os.environ[ENV] = MODE_ENFORCE
        chk("env=enforce ⇒ is_enforce True", is_enforce() is True)
        os.environ[ENV] = "bogus"
        chk("非法 env 忽略（回落文件/默认）", mode() in MODES)
    finally:
        if saved is None:
            os.environ.pop(ENV, None)
        else:
            os.environ[ENV] = saved
    chk("非法模式写入被拒", _raises(lambda: set_mode("nope")))
    s = status()
    chk("status 字段齐", {"mode", "source", "default"} <= set(s))
    return 0 if ok else 1


def _raises(fn) -> bool:
    try:
        fn()
        return False
    except ValueError:
        return True


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 保护器全局模式开关（enforce | shadow）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--status", action="store_true", help="打印当前模式")
    ap.add_argument("--rollback", action="store_true", help="一键回滚：切 shadow（只标记不拦截）")
    ap.add_argument("--enforce", action="store_true", help="切回 enforce")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    if a.rollback:
        print(json.dumps({"rolled_back_to": rollback(), "note": "保护器已回到 642 灰度行为"},
                         ensure_ascii=False))
        return 0
    if a.enforce:
        print(json.dumps({"mode": enforce()}, ensure_ascii=False))
        return 0
    print(json.dumps(status(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
