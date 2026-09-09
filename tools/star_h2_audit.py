#!/usr/bin/env python3
"""星级格审计（star）+ H2 数量基线（h2）。

⚠️ 命名说明：仓库已有 `tools/structure_audit.py`（围栏感知结构缺陷扫描器：
stray H1 / 标题跳级 / 参差表格，由 cppbible quality 以 `--check` 调用）——
**不要改名或覆盖它**。本工具专注「示例头星级格」与「H2 基线」，独立命名。

方法论同 l2_state：先把存量债显性化并冻结基线，门禁只防恶化；
内容级重构（H2 主线/扩展分层）留给专门的写作波次。

星级规范（2026-09-09 起）：
  * 示例头行：`> **示例 N** <span class="badge badge-exp">难度 ★{k}☆{5-k}</span> · 主题`
    —— 统一 span badge 风格 + 5 格制（历史方括号风格 `[难度 ★…☆…] [主题：…]`
    已由 `fix-star` 全量归一，此后禁止回潮）。
  * 练习标题：`### 练习 N（难度 ★{k}）` —— 实心个数制（1..5），**不含 ☆**。
  * 围栏 title：`title="示例 N · ★{k}☆{5-k}"` 必须与同号示例头行星级一致。

H2 基线：`h2-sync` 把每章 `^## ` 计数写入 tools/h2_state.json；
`h2-check` 只在「H2 数量增加（恶化）」时 exit 1，减少（合并/拆分改善）提示 sync。

用法：
    python tools/star_h2_audit.py check --star      # 星级门禁（CI 硬门禁）
    python tools/star_h2_audit.py fix-star          # 方括号 → span 归一（字节安全）
    python tools/star_h2_audit.py scan --star       # 只盘点不落盘
    python tools/star_h2_audit.py h2-sync           # H2 基线快照
    python tools/star_h2_audit.py h2-check          # H2 防恶化门禁
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Sequence

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from comment_blocks import iter_md_files  # noqa: E402

ROOT = HERE.parent
BOOK = ROOT / "Book"
STATE_PATH = HERE / "h2_state.json"

HEAD_BRACKET = re.compile(
    r"^(> \*\*示例 \d+\*\* )\[难度 ([★☆]{5})\] \[主题：(.*)$")
HEAD_SPAN = re.compile(
    r"^>\s*\*\*示例 (\d+)\*\*\s*<span class=\"badge badge-exp\">难度 ([★☆]{5})</span>")
HEAD_BAD = re.compile(r"^>\s*\*\*示例 \d+\*\*")          # 示例头行（任何风格）
EXERCISE = re.compile(r"^### 练习 \d+（难度 ([★☆]+)）\s*$")
TITLE = re.compile(r"^```(?:cpp|bash)\s+title=\"示例 (\d+) · ([★☆]{5})\"")

SPAN_PREFIX = '<span class="badge badge-exp">难度 '


def _read_bytes(path: Path) -> str:
    """原始字节解码，不做换行翻译（R4 铁律：防 Windows 行尾伪 diff）。"""
    return path.read_bytes().decode("utf-8")


def _write_bytes(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


def star_scan(fix: bool = False) -> tuple[list[str], int]:
    """扫全库示例头；fix=True 时把方括号风格原位归一为 span 风格。

    返回 (违规明细, 变更文件数)。违规类：
      bracket   —— 仍为方括号风格（fix 后应为 0）
      exercise  —— 练习头含 ☆ 或实心数越界
      title     —— 围栏 title 星级与同号头行不一致
    """
    violations: list[str] = []
    changed = 0
    for p in iter_md_files(BOOK):
        rel = p.relative_to(BOOK).as_posix()
        text = _read_bytes(p)
        lines = text.split("\n")
        head_star: dict[str, str] = {}
        dirty = False
        for i, ln in enumerate(lines):
            if fix:
                m = HEAD_BRACKET.match(ln)
                if m:
                    rest = m.group(3)
                    if rest.endswith("]"):        # [主题：…] 的闭合括号（变体 B 无）
                        rest = rest[:-1]
                    lines[i] = (m.group(1) + SPAN_PREFIX + m.group(2)
                                + "</span> · " + rest.rstrip())
                    dirty = True
                    ln = lines[i]
            hm = HEAD_SPAN.match(ln)
            if hm:
                head_star[hm.group(1)] = hm.group(2)
                continue
            if HEAD_BAD.match(ln):
                violations.append(f"bracket   {rel}:{i+1} {ln.strip()[:96]}")
                continue
            em = EXERCISE.match(ln)
            if em:
                s = em.group(1)
                if "☆" in s or not 1 <= s.count("★") <= 5:
                    violations.append(f"exercise  {rel}:{i+1} {ln.strip()[:96]}")
                continue
            tm = TITLE.match(ln)
            if tm:
                want = head_star.get(tm.group(1))
                if want and want != tm.group(2):
                    violations.append(
                        f"title     {rel}:{i+1} 示例{tm.group(1)} 头行 {want} != title {tm.group(2)}")
        if dirty:
            new_text = "\n".join(lines)
            if new_text != text:
                _write_bytes(p, new_text)
                changed += 1
    return violations, changed


def h2_counts() -> dict[str, int]:
    out: dict[str, int] = {}
    for p in iter_md_files(BOOK):
        n = sum(1 for ln in _read_bytes(p).split("\n") if re.match(r"^##\s", ln))
        out[p.relative_to(BOOK).as_posix()] = n
    return out


def h2_sync() -> str:
    snap = h2_counts()
    STATE_PATH.write_text(
        json.dumps({"schema": "cppbible-h2/1.0", "h2": snap},
                   ensure_ascii=False, indent=1, sort_keys=True) + "\n",
        encoding="utf-8")
    return f"[h2-sync] {len(snap)} 章基线已写入 {STATE_PATH.name}"


def h2_check() -> int:
    if not STATE_PATH.exists():
        print("[h2-check] 无基线，先跑 h2-sync")
        return 2
    base = json.loads(STATE_PATH.read_text(encoding="utf-8"))["h2"]
    now = h2_counts()
    worse = [f for f in now if f in base and now[f] > base[f]]
    newf = [f for f in now if f not in base]
    improved = [f for f in now if f in base and now[f] < base[f]]
    print(f"[h2-check] 章={len(now)} 恶化={len(worse)} 改善={len(improved)} 新增={len(newf)}")
    for f in worse[:10]:
        print(f"  WORSE {f}: {base[f]} -> {now[f]}")
    if improved:
        print("  （有改善：跑 h2-sync 更新基线）")
    return 1 if worse else 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="星级格审计 / H2 基线")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ck = sub.add_parser("check", help="门禁模式")
    p_ck.add_argument("--star", action="store_true")
    p_ck.add_argument("--json", dest="json_path")

    p_fx = sub.add_parser("fix-star", help="方括号示例头 → span 归一")
    p_fx.add_argument("--dry-run", action="store_true")

    p_sc = sub.add_parser("scan", help="只盘点")
    p_sc.add_argument("--star", action="store_true")

    sub.add_parser("h2-sync", help="写 H2 基线")
    sub.add_parser("h2-check", help="H2 防恶化门禁")

    a = ap.parse_args(argv)

    if a.cmd == "h2-sync":
        print(h2_sync())
        return 0
    if a.cmd == "h2-check":
        return h2_check()

    if a.cmd == "fix-star":
        if a.dry_run:
            v, _ = star_scan(fix=False)
            b = [x for x in v if x.startswith("bracket")]
            print(f"[fix-star dry-run] 方括号头行 {len(b)} 处待归一")
            return 0
        v, changed = star_scan(fix=True)
        remain = [x for x in v if x.startswith("bracket")]
        print(f"[fix-star] 归一 {changed} 个文件；残留方括号 {len(remain)}")
        for x in remain[:10]:
            print("  " + x)
        return 1 if remain else 0

    v, _ = star_scan(fix=False)
    if a.cmd == "scan":
        kinds: dict[str, int] = {}
        for x in v:
            kinds[x.split()[0]] = kinds.get(x.split()[0], 0) + 1
        print(f"[star-scan] 违规 {len(v)}：{kinds}")
        for x in v[:10]:
            print("  " + x)
        return 0
    for x in v[:40]:
        print("  " + x)
    if a.json_path:
        Path(a.json_path).write_text(
            json.dumps(v, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[star-check] {'✅ 星级格全合规' if not v else f'✗ {len(v)} 处违规'}")
    return 0 if not v else 1


if __name__ == "__main__":
    raise SystemExit(main())
