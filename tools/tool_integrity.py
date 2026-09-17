#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tool_integrity.py — 核心工具完整性校验（498 任务 3 / P1-10 / 488 安全性与信任模型）。

为什么（488）：门禁的全部可信度最终落在 5 个核心工具上——它们能改写"什么算通过"。
若工具被静默篡改（供应链攻击 / 本地误改未察觉），后续所有 replay/gate 结论都不可信。
本工具给这 5 个文件建 sha256 基准，把"被改过"变成一条可复现命令。

用法与退出码
============
    python tools/tool_integrity.py --update   # 计算 sha256 写 tools/.tool_checksums，exit 0
    python tools/tool_integrity.py --check    # 独立验证：全匹配 exit 0 / 有改动 exit 1 / 缺基准 exit 2
    python tools/tool_integrity.py            # 同上（无参数的默认动作就是比对，--check 是显式别名）

567 任务 1：`--check` 是**独立验证入口**（此前只有 `--update`，"钉完无法独立复核"）。
567 任务 2：`enforce()` 供**判定入口**（gate_engine / atom_evidence_replay / poison_drill 的
`main()` 首行）强制调用——核心被改动且未重钉就 **fail-loud 拒绝运行**，而不是照跑规则把
"判定核心已被改"静默放行（564 PoC#1/#2 的实锤根因）。

诚实边界：`.tool_checksums` 自身**不纳入校验**（否则要签它自己，递归无解）——
它的可信度依赖 git 历史（谁改了基准会留痕）。基准的更新必须在**功能改动 commit 之后**
执行（498 的顺序依赖：任务 2 改 gate_engine.py ⇒ 任务 3 才生成基准）。
由 567 起，改这五个文件后**必须** `--update` 重钉，否则下次任何判定入口自红——这是设计目标
（改判定核心必须显式留痕），不是 bug。
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from utf8_console import ensure_utf8

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
CHECKSUMS = TOOLS / ".tool_checksums"

# 核心工具（改它们就等于改"什么算通过"）
CORE_TOOLS: tuple[str, ...] = (
    "gate_engine.py",
    "atom_evidence_replay.py",
    "poison_drill.py",
    "toolchain.py",
    "cppbible.py",
)


def sha256_of(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()


def compute(tools_dir: Path | None = None,
            names: tuple[str, ...] = CORE_TOOLS) -> dict[str, str]:
    d = tools_dir or TOOLS
    return {n: sha256_of(d / n) for n in names if (d / n).is_file()}


def write_baseline(path: Path | None = None, tools_dir: Path | None = None,
                   names: tuple[str, ...] = CORE_TOOLS) -> Path:
    """写基准。`names` 可覆盖（测试用假工具目录时必须传，否则算出来是空基准）。"""
    dst = path or CHECKSUMS
    rows = compute(tools_dir, names)
    dst.write_text("".join(f"{h}  {n}\n" for n, h in sorted(rows.items())),
                   encoding="utf-8")
    return dst


def load_baseline(path: Path | None = None) -> dict[str, str] | None:
    """解析 `<sha256>  <filename>`；缺失 → None（调用方须 exit 2，不静默放行）。"""
    src = path or CHECKSUMS
    if not src.is_file():
        return None
    out: dict[str, str] = {}
    for line in src.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) == 2:
            out[parts[1]] = parts[0]
    return out


def verify(path: Path | None = None, tools_dir: Path | None = None
           ) -> tuple[list[tuple[str, str, str]], list[str], int]:
    """返回 (changed[(name, want, got)], missing_names, exit_code)。"""
    base = load_baseline(path)
    if base is None:
        return [], [], 2
    d = tools_dir or TOOLS
    changed: list[tuple[str, str, str]] = []
    missing: list[str] = []
    for name, want in sorted(base.items()):
        f = d / name
        if not f.is_file():
            missing.append(name)
            continue
        got = sha256_of(f)
        if got != want:
            changed.append((name, want, got))
    return changed, missing, (0 if not changed and not missing else 1)


def enforce(tool_name: str, path: Path | None = None, tools_dir: Path | None = None) -> None:
    """**判定入口强制自检**（567 任务 2）：校验不过 ⇒ 立刻 fail-loud 拒绝运行。

    调用纪律（三个判定入口都把这一行放在 `main()` 的**第一句**）：
      * **顺序**：必须在**读库 / 编译 / 跑任何规则之前**——否则"已跑一半才发现核心被改"；
      * **fail-closed**：缺基准（exit 2）/ 文件缺失 / **校验自身异常**一律当"不可信"⇒ 拒绝运行。
        绝不因为校验代码自己出错而静默放行——那会把"没查"伪装成"查过且通过"；
      * **不掩盖真红灯**：拒绝时只报完整性问题（SystemExit(1)），不影响调用方原有的失败路径
        （它根本走不到），也不吞掉任何输出。
    通过时**静默返回**（不打印），免得污染各入口的 stdout 契约（`--json` 等）。
    """
    try:
        changed, missing, code = verify(path, tools_dir)
    except Exception as e:                      # noqa: BLE001 —— 校验自身异常也必须 fail-closed
        print(f"[integrity] ❌ 自检自身异常（{type(e).__name__}: {e}）⇒ 保守拒绝运行",
              file=sys.stderr)
        raise SystemExit(1) from None
    if code == 0:
        return
    lines = [f"[integrity] ❌ 判定核心被改动且未重钉，拒绝运行（{tool_name} 不执行任何规则/判决）"]
    if code == 2:
        lines.append("    缺基准 tools/.tool_checksums ⇒ 无法自证 ⇒ 一律拒绝（不得静默放行）")
    for name, want, got in changed:
        lines.append(f"    {name}：期望 {want[:12]}… 实际 {got[:12]}…")
    for name in missing:
        lines.append(f"    {name}：基准里有、磁盘上缺失")
    lines.append("    修法：确认改动**有意为之**后跑 "
                 "`.venv\\Scripts\\python.exe tools/tool_integrity.py --update` 重钉"
                 "（改判定核心必须显式留痕 —— 这正是本机制的设计目标）")
    print("\n".join(lines), file=sys.stderr)
    raise SystemExit(1)


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="核心工具完整性校验（498 任务 3 / 567 任务 1-2）")
    ap.add_argument("--update", action="store_true",
                    help="计算并写入 tools/.tool_checksums（须在功能改动 commit 之后跑）")
    ap.add_argument("--check", action="store_true",
                    help="独立验证（= 无参数的默认动作）：全匹配 exit 0 / 改动或缺失 exit 1 / 缺基准 exit 2")
    a = ap.parse_args(argv)

    if a.update:
        dst = write_baseline()
        n = len(compute())
        print(f"[tool_integrity] 基准已更新：{dst.relative_to(ROOT).as_posix()}（{n} 个文件）")
        return 0

    changed, missing, code = verify()
    if code == 2:
        print("[tool_integrity] 缺基准文件 tools/.tool_checksums —— "
              "先跑 `python tools/tool_integrity.py --update`", file=sys.stderr)
        return 2
    for name, want, got in changed:
        # 567 任务 1：按提示词只打**前缀**（12 位足够人眼比对/贴工单；全量哈希在 .tool_checksums 里）
        print(f"[tool_integrity] ❌ {name} 被改动（期望 {want[:12]}… 实际 {got[:12]}…）")
    for name in missing:
        print(f"[tool_integrity] ❌ {name} 缺失（基准里有、磁盘上没有）")
    if code == 0:
        print(f"[tool_integrity] OK：{len(compute())} 个核心工具与基准一致")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
