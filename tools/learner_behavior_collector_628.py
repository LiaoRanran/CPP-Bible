"""628 D1 · 真实学习行为采集器（只读，不修改任何源文件）

为 Learner Twin（学习者镜像）开门做前置准备。门未开（真实学习事件 0/50），
本批**不建设镜像**，只做**采集器 + 门状态监控**。

采集来源（全部只读）：
1. `git log --name-only -- Book atoms evidence Examples`（哪些提交动了学习内容）
2. `_auto/inbox/` + `_auto/outbox/`（批次记录）
3. `Book/ atoms/ evidence/` 文件 mtime（文件系统侧候选）
4. 会话日志存储位置探测（CodeBuddy / Trae 等候选路径）

**"真实学习事件"判定标准**（可复现、可审计）：
事件必须满足「用户**主动**修改了学习内容」且**不属于** AI 批次/工具流水线产物。
流水线标识正则见 `AGENT_PAT`（任务号、批次、`feat(...)` 等约定式提交前缀）。
判定结果落在事件字段 `agent_assisted`：
- `True`  → 流水线产物（候选，**不计入**门）
- `False` → 用户亲手学习行为（**计入**门）
- `None` → 不可判定（如 mtime），**不计入**门

输出：`data/learner_behavior_events.jsonl`（append-only、按 `event_id` 去重、重跑幂等）
`--check`：采集器可运行且事件数 ≥ 0、文件 append-only 幂等。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from typing import Optional, cast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

EVENTS = os.path.join(ROOT, "data", "learner_behavior_events.jsonl")
INBOX = os.path.join(ROOT, "_auto", "inbox")
OUTBOX = os.path.join(ROOT, "_auto", "outbox")

LEARNING_PATHS = ["Book", "atoms", "evidence", "Examples"]
LEARNING_DIRS = ["Book", "atoms", "evidence"]

# AI 批次/工具流水线标识：命中即视为 agent 协作产物，不计入真实学习事件
AGENT_PAT = re.compile(
    r"^\d{3}[：:\s]|任务[A-Z0-9]|批次|(?i:batch)|P[0-9]-[A-Z]|W[12]\b|"
    r"^(feat|fix|refactor|style|chore|docs|test|perf|build|ci)(\(|:)|"
    r"^G[0-9]|^ch[0-9]+|^CI\b|^B[0-9]\b|^[A-Z]{2,6}-[0-9]{3}|"
    r"监工|质检|红队|流水线|三权分立|原子化|批量生产|签署|人审|回填|门禁|"
    r"开工|收尾|处置|入库|首跑|矩阵|固化|自检"
)

# 人类亲手学习的**正向信号**：只有命中才判为真实学习事件（保守判定）
HUMAN_PAT = re.compile(
    r"学习记录|学习笔记|读书笔记|我的笔记|错题本|复习笔记|手写笔记|"
    r"(?i:study[ _-]?log|learning[ _-]?log)"
)

SESSION_CANDIDATES = [
    os.environ.get("APPDATA", "") + r"\CodeBuddy CN\User\globalStorage\tencent-cloud.coding-copilot",
    os.environ.get("APPDATA", "") + r"\Trae\User\globalStorage",
    os.path.expanduser("~") + r"\.codebuddy\projects",
]


def _git(args: list[str]) -> str:
    p = subprocess.run(["git", *args], capture_output=True, text=True, cwd=ROOT,
                       timeout=300, check=False)
    return p.stdout if p.returncode == 0 else ""


def _eid(kind: str, ref: str) -> str:
    return hashlib.sha256(f"{kind}|{ref}".encode("utf-8")).hexdigest()[:16]


def classify(subject: str) -> Optional[bool]:
    """三态判定：True=流水线产物 / False=人类亲手学习 / None=不可判定（保守不计入门）。"""
    if AGENT_PAT.search(subject):
        return True
    if HUMAN_PAT.search(subject):
        return False
    return None


def _event(eid: str, kind: str, source: str, ref: str, agent: Optional[bool],
           detail: str, ts: str) -> dict:
    return {"event_id": eid, "kind": kind, "source": source, "ref": ref,
            "agent_assisted": agent, "detail": detail, "observed_at": ts}


# ── 来源 1：git 提交 ─────────────────────────────────────────────

def collect_git(ts: str) -> list[dict]:
    raw = _git(["log", "--name-only", "--format=\x01%H|%an|%ae|%ct|%s",
                "--", *LEARNING_PATHS])
    events: list[dict] = []
    cur: Optional[dict] = None
    for line in raw.splitlines():
        if line.startswith("\x01"):
            if cur:
                events.append(cur)
            h, an, ae, ct, subj = line[1:].split("|", 4)
            cur = {"sha": h, "an": an, "ae": ae, "ct": ct, "subj": subj, "files": []}
        elif line.strip() and cur is not None:
            cast(list, cur["files"]).append(line.strip())
    if cur:
        events.append(cur)
    out: list[dict] = []
    for e in events:
        files = [str(f) for f in cast(list, e["files"])]
        sha, subj = str(e["sha"]), str(e["subj"])
        scoped = [f for f in files if f.split("/", 1)[0] in LEARNING_PATHS]
        if not scoped:
            continue
        out.append(_event(
            _eid("git", sha), "git_commit", "git_log", sha, classify(subj),
            f'{e["ct"]}|{e["an"]}|{subj}|files={len(scoped)}', ts))
    return out


# ── 来源 2：批次记录 ─────────────────────────────────────────────

def collect_batches(ts: str) -> list[dict]:
    out = []
    for folder, tag in ((INBOX, "inbox"), (OUTBOX, "outbox")):
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            p = os.path.join(folder, name)
            if not os.path.isfile(p):
                continue
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            out.append(_event(_eid("batch", rel), "batch_record", f"_auto/{tag}",
                              rel, True, "批次记录（AI 协作流程产物）", ts))
    return out


# ── 来源 3：文件系统 mtime ───────────────────────────────────────

def collect_mtime(ts: str) -> list[dict]:
    out = []
    for d in LEARNING_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            for fn in sorted(files):
                p = os.path.join(dirpath, fn)
                rel = os.path.relpath(p, ROOT).replace("\\", "/")
                mt = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(os.path.getmtime(p)))
                out.append(_event(_eid("mtime", rel), "file_mtime", "filesystem",
                                  rel, None, f"mtime={mt}", ts))
    return out


# ── 来源 4：会话日志探测 ─────────────────────────────────────────

def probe_session_stores() -> list[dict]:
    found = []
    for c in SESSION_CANDIDATES:
        if c and os.path.isdir(c):
            try:
                n = sum(len(fs) for _r, _d, fs in os.walk(c))
            except OSError:
                n = -1
            found.append({"path": c, "files": n})
    return found


# ── append-only 写入 ─────────────────────────────────────────────

def load_events() -> list[dict]:
    if not os.path.exists(EVENTS):
        return []
    return [json.loads(ln) for ln in open(EVENTS, encoding="utf-8") if ln.strip()]


def append_events(new: list[dict]) -> int:
    """按 event_id 去重后追加，返回**新增**条数（重跑幂等）。"""
    known = {e["event_id"] for e in load_events()}
    fresh = [e for e in new if e["event_id"] not in known]
    if not fresh:
        return 0
    os.makedirs(os.path.dirname(EVENTS), exist_ok=True)
    with open(EVENTS, "a", encoding="utf-8", newline="\n") as fh:
        for e in fresh:
            fh.write(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n")
    return len(fresh)


def collect(ts: Optional[str] = None) -> dict:
    ts = ts or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    git_ev = collect_git(ts)
    batch_ev = collect_batches(ts)
    mtime_ev = collect_mtime(ts)
    all_ev = git_ev + batch_ev + mtime_ev
    added = append_events(all_ev)
    return {"stamp": ts, "candidates": len(all_ev), "added": added,
            "by_kind": _by_kind(load_events()),
            "real_learning_events": count_real(load_events()),
            "sessions": probe_session_stores()}


def _by_kind(events: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for e in events:
        out[str(e["kind"])] = out.get(str(e["kind"]), 0) + 1
    return out


def count_real(events: list[dict]) -> int:
    """真实学习事件 = agent_assisted 明确为 False 的事件。"""
    return sum(1 for e in events if e.get("agent_assisted") is False)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r1 = collect()
    chk("采集器可运行", r1["candidates"] >= 0, f'(候选 {r1["candidates"]})')
    n_after_first = len(load_events())
    r2 = collect()
    chk("append-only 幂等（重跑不新增）", r2["added"] == 0, f'(第二次 added={r2["added"]})')
    chk("事件文件条数不变", len(load_events()) == n_after_first, f'({n_after_first})')
    chk("事件数 ≥ 0", n_after_first >= 0)
    kinds = _by_kind(load_events())
    chk("含 git/批次/mtime 三类来源",
        all(k in kinds for k in ("git_commit", "batch_record", "file_mtime")), f'({kinds})')
    git_ev = [e for e in load_events() if e["kind"] == "git_commit"]
    tri: dict[str, int] = {}
    for e in git_ev:
        tri[str(e["agent_assisted"])] = tri.get(str(e["agent_assisted"]), 0) + 1
    chk("git 提交完成三态分类", bool(git_ev) and sum(tri.values()) == len(git_ev), f"({tri})")
    chk("classify 三态判定正确",
        classify("学习笔记：模板偏特化") is False
        and classify("628 A1：flag 真接入") is True
        and classify("无标识的普通描述") is None)
    chk("真实学习事件计数可算", count_real(load_events()) >= 0,
        f'({count_real(load_events())})')
    print(f"D1 collector check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 D1 学习行为采集器")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--json", action="store_true", help="打印 JSON 摘要")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    r = collect()
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"candidates={r['candidates']} added={r['added']} "
              f"real_learning_events={r['real_learning_events']} by_kind={r['by_kind']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
