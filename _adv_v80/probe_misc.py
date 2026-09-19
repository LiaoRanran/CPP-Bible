"""v5 对抗复测（misc）：E09 并发 / E16 闪卡 draft 导出 / E08 poison 退出码 / E14 无锚点。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge  # noqa: E402

PROBE = ROOT / "_adv_v80" / "probes"
LOCK = ROOT / "_adv_v80" / ".replay_lock"
replay._REPLAY_LOCK = LOCK


def line(tag: str, verdict: str, note: str = "") -> None:
    print(f"[{tag:<24}] {verdict}" + (f"  | {note}" if note else ""))


# ── E09：并发同卡（P0-G1 声称串行化防假失败）────────────────────────────
card = PROBE / "EV-ADV80-N3.md"
script = (
    "import sys, pathlib\n"
    f"sys.path.insert(0, r'{ROOT / 'tools'}')\n"
    "import atom_evidence_replay as replay\n"
    f"replay._REPLAY_LOCK = pathlib.Path(r'{LOCK}')\n"
    f"v, log = replay.replay_card(pathlib.Path(r'{card}'), do_sanitizer=False)\n"
    "print(v)\n")
ps = [subprocess.Popen([sys.executable, "-c", script],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
      for _ in range(2)]
outs = [p.communicate(timeout=300) for p in ps]
vs = [o[0].strip().split("\n")[-1] if o[0].strip() else f"ERR:{o[1][:60]}" for o in outs]
line("E09 并发同卡（2 进程）", f"{vs}",
     "假失败=未修" if any(v not in ("confirm",) for v in vs) else "串行化成功（无假失败）")

# ── E16：闪卡导出是否含 draft/未验证原子 ─────────────────────────────────
import flashcard_export as fe  # noqa: E402
cards = fe.build_cards()
statuses = {}
for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
    statuses[str(ge._meta(p).get("id"))] = str(ge._meta(p).get("status"))
draft_in = [c["id"] for c in cards
            if c["type"] == "atom_claim" and statuses.get(c["id"], "") != "verified"]
line("E16 闪卡 draft 导出",
     f"总卡 {len(cards)}，非 verified 原子卡 {len(draft_in)}",
     "逃逸（未验证内容直达学习者）" if draft_in else "已拦")

# ── E08：poison 退出码（未覆盖规则时是否 exit 1）─────────────────────────
try:
    from gate_engine import gate_exit_code  # type: ignore
    full = gate_exit_code(52, 52, [])
    uncov = gate_exit_code(52, 52, ["SOME-RULE"])
    failed = gate_exit_code(51, 52, [])
    line("E08 poison 退出码",
         f"全过={full} 有未覆盖={uncov} 有失败={failed}",
         "已修（未覆盖/失败均非零）" if (uncov != 0 and failed != 0 and full == 0)
         else "仍逃逸")
except ImportError:
    line("E08 poison 退出码", "无 gate_exit_code 函数（已改名/移除）")

# ── E14：451 无锚点数字（文档层：grep 是否仍无源）────────────────────────
hits = 0
for rel in ("References/architecture_架构演进/451_*.md",):
    for p in ROOT.glob(rel):
        t = p.read_text(encoding="utf-8", errors="replace")
        hits += t.count("4%")
line("E14 451 无锚点数字", f"451 中 '4%' 出现 {hits} 次",
     "仍存在（文档层洞，无机器检查）" if hits else "已修")
