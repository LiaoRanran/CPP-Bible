"""l2_state.py — L2 深耕覆盖状态机（摆脱 MEMORY 文本记账）。

L2 真机深耕按章清理「纯注释型 cpp 块」。此前每章状态（剩几个、哪个 commit 清的）
只记在 MEMORY 手记里，会漂移（历史估数多次与实扫不符）。本工具把它落成
**可提交、可校验**的状态文件 `tools/l2_state.json`：

- `sync`   重新测量并写入状态；章由「有残留」变为 0 时记录 cleared_commit
- `check`  与快照比对：回潮/新增/未同步一律报出，退出码 1（可挂 CI）
- `report` 状态看板：剩余总量、已清零章（含 commit）、残留 Top

口径与 `comment_blocks.py` / `compile_all.extract_blocks` 完全一致（只认 ```cpp 围栏）。

用法：
    python tools/l2_state.py sync|check|report
"""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path
from typing import Any, Sequence, cast

from comment_blocks import BOOK, is_pure_comment, iter_md_files, parse

HERE = Path(__file__).resolve().parent
STATE_FILE = HERE / "l2_state.json"
SCHEMA = "cppbible-l2-state/1.0"


def git_head() -> str:
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, cwd=str(BOOK.parent))
        return r.stdout.strip() if r.returncode == 0 else "unknown"
    except Exception:
        return "unknown"


def measure() -> dict[str, int]:
    """返回 {相对路径: 该章纯注释块数}（只含 >0 的章）。"""
    out: dict[str, int] = {}
    for p in iter_md_files(BOOK):
        pure = sum(1 for b in parse(p) if is_pure_comment(b.body))
        if pure:
            out[p.relative_to(BOOK).as_posix()] = pure
    return out


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {"schema": SCHEMA, "updated": "", "commit": "", "chapters": {}}
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"l2_state.json 解析失败: {e}") from e
    if not isinstance(data, dict):
        raise SystemExit("l2_state.json 顶层必须是对象")
    return cast(dict[str, Any], data)


def save_state(state: dict[str, Any]) -> None:
    payload = json.dumps(state, ensure_ascii=False, indent=1) + "\n"
    STATE_FILE.write_bytes(payload.encode("utf-8"))


def cmd_sync(_a: argparse.Namespace) -> int:
    live = measure()
    state = load_state()
    chs: dict[str, Any] = state.get("chapters", {})
    head = git_head()
    newly = 0
    cleared = 0
    for rel, cnt in live.items():
        e = chs.get(rel, {})
        e["pure"] = cnt
        e["status"] = "remaining"
        e["cleared_commit"] = None
        e["seen_commit"] = head
        if not e.get("opened_commit"):
            e["opened_commit"] = head
        chs[rel] = e
        newly += 1
    for rel, e in list(chs.items()):
        if rel not in live and e.get("pure", 0) > 0:
            # 该章已无残留 -> 记为已清零
            e["pure"] = 0
            e["status"] = "cleared"
            e["cleared_commit"] = e.get("cleared_commit") or head
            chs[rel] = e
            cleared += 1
    state.update({"schema": SCHEMA, "updated": date.today().isoformat(),
                  "commit": head, "chapters": chs})
    save_state(state)
    print(f"[sync] remaining chapters = {len(live)} | total pure = {sum(live.values())}")
    print(f"[sync] newly-cleared this run = {cleared} | saved {STATE_FILE.name}")
    return 0


def cmd_check(_a: argparse.Namespace) -> int:
    live = measure()
    state = load_state()
    chs: dict[str, Any] = state.get("chapters", {})
    drifts: list[tuple[str, str, int, int]] = []  # kind, rel, snap, live
    for rel, e in chs.items():
        snap = int(e.get("pure", 0))
        now = live.get(rel, 0)
        if now != snap:
            if snap == 0 and now > 0:
                kind = "REGRESSED(回潮)"
            elif now > snap:
                kind = "REGRESSED"
            else:
                kind = "IMPROVED(需 sync)"
            drifts.append((kind, rel, snap, now))
    for rel, cnt in live.items():
        if rel not in chs:
            drifts.append(("NEW(未记录)", rel, 0, cnt))
    print(f"[check] live remaining = {len(live)} ({sum(live.values())} blocks) | "
          f"snapshot chapters = {len(chs)}")
    for kind, rel, snap, now in sorted(drifts):
        print(f"  [{kind}] {rel}: snapshot={snap} live={now}")
    if not drifts:
        print("[check] OK 无漂移")
        return 0
    print(f"[check] 发现 {len(drifts)} 处漂移 —— 确认后运行 `l2_state.py sync` 更新快照")
    return 1


def cmd_report(_a: argparse.Namespace) -> int:
    state = load_state()
    chs: dict[str, Any] = state.get("chapters", {})
    remaining = {r: int(e.get("pure", 0)) for r, e in chs.items() if int(e.get("pure", 0)) > 0}
    cleared = {r: e for r, e in chs.items() if int(e.get("pure", 0)) == 0}
    print(f"l2_state.json  updated={state.get('updated','')} commit={state.get('commit','')}")
    print(f"残留章节 {len(remaining)} | 纯注释块合计 {sum(remaining.values())} | "
          f"已清零章节 {len(cleared)}")
    print("\n残留 Top（降序）：")
    for rel, cnt in sorted(remaining.items(), key=lambda x: -x[1])[:20]:
        print(f"  {cnt:4}  {rel}")
    if cleared:
        print("\n已清零章节（含 clear commit）：")
        for rel, e in sorted(cleared.items()):
            print(f"  {e.get('cleared_commit', '?'):8} {rel}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="L2 深耕覆盖状态机")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("sync", help="重新测量并写入 tools/l2_state.json").set_defaults(func=cmd_sync)
    sub.add_parser("check", help="与快照比对，有漂移退出码 1").set_defaults(func=cmd_check)
    sub.add_parser("report", help="打印覆盖看板").set_defaults(func=cmd_report)
    a = ap.parse_args(argv)
    rc: int = a.func(a)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
