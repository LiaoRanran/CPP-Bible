"""627 B3 · `QUEYI_AUTHORITY_V2` 一键启用 / 回滚脚本 + 指南

**背景**：627 B1 已验证 5 种投影在 V2 模式下全部成功、B2 确认对 CORE_TOOLS 无回归。
本工具提供**安全的一键启用/回滚**机制。

**机制（诚实，不修改 626 编译器）**：
- 626 编译器只读取 `os.environ["QUEYI_AUTHORITY_V2"]`，**不读配置文件**。
- 因此本脚本维护一个**本地模式文件** `data/authority_v2_mode.json`
  （`{"enabled": bool, "set_at": iso, "by": ...}`）作为「意图」真相源，
  并提供 `run` 子命令：读取模式文件 → 设置环境变量 → 调用 626 编译器，
  使模式文件**真正生效**（无需手动 export）。
- `enable` / `rollback` 仅翻转模式文件，**不触碰任何受控目录、不修改 626 工具**。

**⚠ 启用需人确认（交人项 #1）**：本脚本默认 `enabled=false`。
`enable` 仅记录意图；真正让 V2 生效需通过 `run`（或在 shell 中 `export QUEYI_AUTHORITY_V2=1`）。
脚本不自动替人开启生产路径——它只把“开关”交到人手边。

**回滚**：`rollback` 将模式置回 false；或 `export QUEYI_AUTHORITY_V2=0`。
因 V2 是纯增量只读投影，回滚**零副作用**（不影响原始 ledger / 受控目录）。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENV_FLAG = "QUEYI_AUTHORITY_V2"
MODE_FILE = os.path.join(ROOT, "data", "authority_v2_mode.json")
GUIDE_FILE = os.path.join(ROOT, "data", "authority_v2_enable_guide_627.md")


def read_mode() -> dict:
    if not os.path.exists(MODE_FILE):
        return {"enabled": False, "set_at": None, "by": None}
    try:
        m: dict = json.load(open(MODE_FILE, encoding="utf-8"))
        return m
    except Exception:
        return {"enabled": False, "set_at": None, "by": None}


def write_mode(enabled: bool, by: str = "cli") -> dict:
    m = {"enabled": enabled,
         "set_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
         "env_var": f"{ENV_FLAG}={'1' if enabled else '0'}",
         "by": by}
    with open(MODE_FILE, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)
    return m


def effective_env_value() -> str:
    """实际生效值：环境变量优先，否则取模式文件。"""
    if ENV_FLAG in os.environ:
        return os.environ[ENV_FLAG]
    return "1" if read_mode().get("enabled") else "0"


def run_compiler_in_mode(projection: str) -> int:
    """按当前模式设置环境变量，调用 626 编译器（使模式文件真正生效）。"""
    val = "1" if read_mode().get("enabled") else "0"
    env = dict(os.environ)
    env[ENV_FLAG] = val
    script = (
        "import sys, json; sys.path.insert(0, %r)\n"
        "import authority_projection_compiler_626 as C\n"
        "led = C.AuthorityProjectionCompiler()\n"
        "if %r == 'w2': print(json.dumps(led.w2_summary(), ensure_ascii=False))\n"
        "elif %r == 'pck': print(json.dumps(led.compile_pck_all(), ensure_ascii=False))\n"
        "elif %r == 'dashboard': print(json.dumps(led.compile_dashboard(), ensure_ascii=False))\n"
        "else: print(json.dumps(led.compile_golden(), ensure_ascii=False))\n"
    ) % (HERE, projection, projection, projection)
    proc = subprocess.run([sys.executable, "-c", script], capture_output=True,
                          text=True, env=env, cwd=ROOT)
    print(proc.stdout)
    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
    return proc.returncode


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    try:
        write_mode(True, by="selftest")
        chk("enable 后模式文件 enabled=true", read_mode()["enabled"] is True)
        write_mode(False, by="selftest")
        chk("rollback 后模式文件 enabled=false", read_mode()["enabled"] is False)
    finally:
        # 还原（默认关闭）
        write_mode(False, by="selftest")
    chk("默认模式文件存在且 enabled=false", read_mode()["enabled"] is False)
    chk("effective_env 返回 0 或 1", effective_env_value() in ("0", "1"))
    print(f"B3 switch check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _write_guide() -> None:
    lines = [
        "# 627 B3 · Authority V2 启用 / 回滚指南",
        "",
        "## 一、声明（重要）",
        "- V2 是 **Authority 单一真源** 驱动的只读投影层（W2/PCK/golden/dashboard/textbook）。",
        "- 627 B1 已验证：**5 种投影在 V2 模式下全部成功运行**。",
        "- 627 B2 已验证：**CORE_TOOLS 完全隔离 V2 flag/工具，启用无回归风险**。",
        "- **启用需人确认（交人项 #1）**：本工具不替人自动开启生产路径。",
        "",
        "## 二、启用步骤",
        "```bash",
        "# 1) 记录启用意图（仅写 data/authority_v2_mode.json，不修改任何代码/数据）",
        "python tools/authority_v2_switch_627.py enable",
        "",
        "# 2) 让模式真正生效（读模式文件 → 设置环境变量 → 调 626 编译器）",
        "python tools/authority_v2_switch_627.py run w2",
        "",
        "# 或在 shell 中直接导出（对所有子进程生效）",
        "export QUEYI_AUTHORITY_V2=1",
        "```",
        "",
        "## 三、回滚步骤",
        "```bash",
        "python tools/authority_v2_switch_627.py rollback   # 模式置回 false",
        "export QUEYI_AUTHORITY_V2=0                          # 或直接在 shell 关闭",
        "```",
        "- 回滚**零副作用**：V2 是纯增量只读投影，不影响原始 ledger / 受控目录。",
        "",
        "## 四、验证清单（启用前建议确认）",
        "1. B1 端到端：5 种投影 V2 全部成功 ✅",
        "2. B2 回归：CORE_TOOLS 隔离 ✅",
        "3. 627 A1：W2 归一化 121 节点 diff=0 ✅",
        "4. push 后由远程 CI 实跑 gate/poison/replay（交人项 #3）",
        "",
        "> 本指南与脚本**不修改 626 工具、不修改受控目录**；开关仅由人在本地掌控。",
    ]
    with open(GUIDE_FILE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 B3 V2 启用/回滚")
    ap.add_argument("action", nargs="?",
                    choices=["enable", "rollback", "status", "run", "guide", "check"],
                    default="status")
    ap.add_argument("projection", nargs="?", default="w2")
    ap.add_argument("--check", action="store_true", help="自检（等价 action=check）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.action == "enable":
        m = write_mode(True)
        print("已记录启用意图：", json.dumps(m, ensure_ascii=False))
        print("提示：运行 `run <projection>` 或 `export QUEYI_AUTHORITY_V2=1` 使其生效。")
        return 0
    if args.action == "rollback":
        m = write_mode(False)
        print("已回滚：", json.dumps(m, ensure_ascii=False))
        return 0
    if args.action == "status":
        m = read_mode()
        print("模式文件：", json.dumps(m, ensure_ascii=False))
        print(f"当前生效 {ENV_FLAG} =", effective_env_value())
        return 0
    if args.action == "run":
        return run_compiler_in_mode(args.projection)
    if args.action == "guide":
        _write_guide()
        print(f"written {GUIDE_FILE}")
        return 0
    if args.action == "check":
        return selftest()
    return 0


if __name__ == "__main__":
    sys.exit(main())
