#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""overturned_events.py — 推翻事件通道（573 任务 A-2 设计的**独立落地**；592 任务2）。

为什么要有这个文件（592 侦察结论）：573 把 `--log-overturned` CLI 与 schema 设计在了
`metrics_collector.py` 里，但 **`data/overturned_events.jsonl` 从未被创建** —— 通道不存在，
`curves.overturned_by_stronger_verifier` 就永远是"0 = 没有通道"而不是"0 = 没有推翻"，
两者含义相反。本模块把通道本身（建/读/校验/写）**独立成工具**，让"通道存在性"可被显式检查，
并把 `metrics_collector` 的同名能力收敛到这里（单一实现，不留两份 fail-closed 逻辑）。

硬不变量（573 立、592 不改）：
  * **系统绝不自动产生推翻** —— 本模块只提供**写入接口**，调用者必须是人或异族的显式动作；
    任何自动检测 / 自动 LLM 推翻路径**不许**调用 `append()`（战略冻结档）。
  * **fail-closed**：缺字段 / 卡解析不到 / git 不可用 / human 名与该卡最后一次 git 提交作者
    不匹配 ⇒ **拒绝写入且不落行**（"无签名的人"不能推翻任何东西）。
  * 只追加：不覆盖、不删除、不改历史行。

schema（与 573 设计一致，一行一条 JSON）：
  {"ts": "ISO8601", "target": "card|proposition|rule", "card": "EV-XXX-001",
   "old_verdict": "confirm|refute|blocked|escaped", "new_verdict": "…",
   "by": "human:<git-author>|adversary:<族>", "reason": "text"}

用法：
    python tools/overturned_events.py ensure      # 幂等建通道（缺失则建空文件；存在则逐行校验）
    python tools/overturned_events.py count       # 事件总数
    python tools/overturned_events.py check       # 校验通道（每行 JSON 合法）
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PATH = ROOT / "data" / "overturned_events.jsonl"

#: 必填字段（`card` 缺省时取 `target`；`ts` 缺省时由 append 填当前时间）。
#: schema 全字段见模块 docstring（`ts, target, card, old_verdict, new_verdict, by, reason`）。
REQUIRED_FIELDS = ("target", "old_verdict", "new_verdict", "by", "reason")


def ensure_channel(path: Path | str | None = None) -> Path:
    """幂等建通道：缺失 ⇒ 建**空文件**；已存在 ⇒ **不写**，只逐行校验 JSON 合法性。

    校验是 fail-loud 的（坏行 ⇒ `ValueError` + 行号）：事件流是审计证据，
    静默跳过坏行等于篡改证据链。文件为空是**合法状态**（= 通道已就绪但还没有推翻事件）。
    """
    p = Path(path) if path else DEFAULT_PATH
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("", encoding="utf-8", newline="\n")
    _validate_lines(p)
    return p


def _validate_lines(p: Path) -> list[dict]:
    out: list[dict] = []
    for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        s = ln.strip()
        if not s:
            continue                       # 尾随空行不算事件（jsonl 常见）
        try:
            ev = json.loads(s)
        except ValueError as exc:
            raise ValueError(
                f"{p} 第 {i} 行不是合法 JSON（{exc}）—— 事件流是审计证据，坏行必须显形，"
                f"不静默跳过") from exc
        if not isinstance(ev, dict):
            raise ValueError(f"{p} 第 {i} 行不是 JSON 对象：{type(ev).__name__}")
        out.append(ev)
    return out


def read_events(path: Path | str | None = None) -> list[dict]:
    """读事件流（只读）。文件缺失 ⇒ `[]`（"通道未建"与"零事件"由 `count` 与
    `ensure_channel` 的状态区分，见 `channel_state()`）。"""
    p = Path(path) if path else DEFAULT_PATH
    if not p.is_file():
        return []
    return _validate_lines(p)


def count(path: Path | str | None = None) -> int:
    """事件总数（= 合法事件行数；空通道 ⇒ 0）。"""
    return len(read_events(path))


def channel_state(path: Path | str | None = None) -> dict:
    """通道状态：`{path, exists, initialized, events}`。

    `initialized` 是**独立于事件数**的事实：文件在 = 通道已初始化（0 事件是真值），
    文件不在 = 没有通道（此时 0 事件是"没量过"，不许当结论用）。
    """
    p = Path(path) if path else DEFAULT_PATH
    return {"path": str(p), "exists": p.is_file(), "initialized": p.is_file(),
            "events": count(p)}


def _resolve_card_path(card: str) -> Path | None:
    """卡 id 或相对路径 ⇒ 文件路径；找不到 ⇒ None（调用方按 fail-closed 处理）。"""
    p = Path(card)
    if p.is_file():
        return p
    for pat in ("atoms/**/%s.md", "evidence/**/%s.md"):
        for f in ROOT.glob(pat % card):
            if f.is_file():
                return f
    return None


def _validate_event(event: dict) -> str:
    """校验事件可写性（**只读、不落盘**）⇒ 返回 `by` 的规范化形态。

    顺序与 573 实现一致（缺字段 → 卡解析 → 签名核验 → by 形态），
    这样错误信息与既有回归锁逐字对齐。
    """
    missing = [k for k in REQUIRED_FIELDS if not str(event.get(k) or "").strip()]
    if missing:
        raise ValueError("target/old_verdict/new_verdict/by/reason 均不可为空"
                         f"（不完整的推翻不予登记）：缺 {missing}")
    target = str(event["target"]).strip()
    card = str(event.get("card") or target).strip()
    by = str(event["by"]).strip()
    cp = _resolve_card_path(card)
    if cp is None:
        raise ValueError(f"卡解析不到（{card}）⇒ 无法核验签署，拒绝写入（fail-closed）")
    if by.lower().startswith("human:"):
        name = by.split(":", 1)[1].strip()
        import gate_engine as ge  # 局部导入：复用卡级同款判据，避免模块级耦合
        author = ge._git_author_for(cp)
        if author is None:
            raise ValueError(f"git 不可用 ⇒ 无法核验推翻者 {name!r}，拒绝写入（fail-closed）")
        if not ge._author_matches(name, author):
            raise ValueError(f"推翻者 {name!r} 不是该卡最后一次 git 提交的作者（{author[0]}）"
                             f"⇒ 无签名，拒绝写入")
    elif not by.lower().startswith("adversary:"):
        raise ValueError("by 须为 `human:<名>` 或 `adversary:<族>`（其它形态不予登记）")
    ts = str(event.get("ts") or "").strip()
    if ts:
        try:
            dt.datetime.fromisoformat(ts)
        except ValueError as exc:
            raise ValueError(f"ts 不是 ISO8601（{ts!r}）：{exc}") from exc
    return by


def append(event: dict, path: Path | str | None = None) -> dict:
    """把一条推翻事件**追加**到通道；返回落盘的那条（含 `ts`/`card`）。

    fail-closed：校验不过 ⇒ `ValueError`，**连空文件都不会建**（不做半个动作）。
    `ts` 缺省 ⇒ 填当前时间；`card` 缺省 ⇒ 取 `target`。

    ⚠️ 谁**不许**调用：任何自动检测 / 自动 LLM 推翻路径（战略冻结档）。
    本函数只接显式的人或异族动作。
    """
    if not isinstance(event, dict):
        raise ValueError(f"事件必须是 dict，实得 {type(event).__name__}")
    by = _validate_event(event)
    ev = {"ts": str(event.get("ts") or "").strip() or dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
          "target": str(event["target"]).strip(),
          "card": str(event.get("card") or event["target"]).strip(),
          "old_verdict": str(event["old_verdict"]).strip(),
          "new_verdict": str(event["new_verdict"]).strip(),
          "by": by, "reason": str(event["reason"]).strip()}
    p = Path(path) if path else DEFAULT_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    return ev


def make_event(target: str, old_verdict: str, new_verdict: str, by: str, reason: str,
               card: str | None = None) -> dict:
    """按 573 的参数形态组事件（给 `metrics_collector.log_overturned` 复用；
    **不落盘** —— 落盘一律走 `append()` 的校验路径）。"""
    return {"target": target, "old_verdict": old_verdict, "new_verdict": new_verdict,
            "by": by, "reason": reason, "card": card or target}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="推翻事件通道（只追加；系统绝不自动产生推翻）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, helptext in (("ensure", "幂等建通道（缺失则建空文件；存在则逐行校验）"),
                           ("count", "事件总数"),
                           ("check", "校验通道每行 JSON 合法")):
        sp = sub.add_parser(name, help=helptext)
        sp.add_argument("--path", default=str(DEFAULT_PATH))
    a = ap.parse_args(argv)
    p = Path(a.path)
    if a.cmd == "ensure":
        ensure_channel(p)
        st = channel_state(p)
        print(f"[overturned] 通道就绪：{p}（initialized={st['initialized']}，事件 {st['events']} 条）")
        return 0
    if a.cmd == "count":
        print(count(p))
        return 0
    # check
    try:
        n = count(p)
    except ValueError as exc:
        print(f"[overturned] ❌ {exc}", file=sys.stderr)
        return 2
    print(f"[overturned] 通道合法：{p}（{n} 条事件）")
    return 0

if __name__ == "__main__":
    if "--check" in sys.argv:
        print("OK: overturned_events --check（只读：加载即校验，不执行任何业务逻辑）")
        sys.exit(0)
    raise SystemExit(main())
