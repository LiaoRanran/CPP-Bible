#!/usr/bin/env python3
"""539 Part B · mutation_fuzz：对**真实卡**自动批量变异，找毒样例还没覆盖的新逃逸（L3 第一块）。

**与 `poison_drill` 的边界（互补，不合并）**：
  - `poison_drill.py` = **人工写死的固定载荷**，测"规则有没有覆盖**已知**攻击"（回归锁，红即 CI 红）；
  - `mutation_fuzz.py` = 对真实证据卡/原子卡**自动批量变异**，找"毒样例还没覆盖的**新**逃逸"
    （发现器：escaped 是**产物**，不是 CI 红灯）。
  两者共用同一个沙箱思路与同一套规则引擎，但载荷来源与退出码语义完全不同。

**判决三分类（539 B2，定义写死，不许把 n_a 当 blocked 凑拦截率）**：
  - `blocked`：变异后被 block/refute，**或产生新的命中 warn** ⇒ 守住（warn 只算"可见化"单列）；
  - `escaped`：变异后**仍无任何新 block/warn** ⇒ 逃逸（最高优先输出）；
  - `n_a`    ：该卡本就没有被变异的字段 / 变异文本 YAML 解析失败 / replay 落 infra_error
               ⇒ **不适用**，既不算守住也不算逃逸。
报告同时给两个率：**严格拦截率**（只认 block/refute）与**含 warn 处置率**。

**纪律**：变异全部在 tempfile 沙箱里进行；`atoms/`、`evidence/` 原卡**零改动**（算子只读文本、
纯函数、幂等）。涉及 replay 的算子（M1 改 `artifact_sha256`/`run_match_file`、M7 改 sha/数值）
会额外跑一次 replay——**这不是"额外加分"，而是必需**：只看 gate 会把"删了必需字段"误判成逃逸。

用法：
  python tools/mutation_fuzz.py --limit 5                       # 小批先跑通（默认）
  python tools/mutation_fuzz.py --cards all --operators M1,M7
  python tools/mutation_fuzz.py --cards atoms/**.md --limit 20 --report data/mutation/last.json
"""
# mypy: ignore-errors
# 存量工具：类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import atexit
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from path_config_625 import root as _queyi_root  # noqa: E402  (625 C1 路径解耦)

ROOT = _queyi_root()
sys.path.insert(0, str(Path(__file__).resolve().parent))

import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge  # noqa: E402
import stat_bounds  # noqa: E402  565 Part 2：口径块（纯标准库统计原语）

# 需要额外跑 replay 的算子：M1 动的是 replay 的**裁决输入**（sha/必需字段），M7 动 sha/读数。
# 只跑 gate 会把"删了 artifact_sha256"判成 escaped —— 那是**制造假逃逸**，比漏报更坏。
REPLAY_OPS = frozenset({"M1", "M7"})
OPS = ("M1", "M2", "M3", "M4", "M5", "M6", "M7")
OP_TITLES = {
    "M1": "字段删除（artifact_sha256/run_match_file/negative_controls/signed_by）",
    "M2": "路径变形（大小写翻转/加 ./ /正反斜杠互换）",
    "M3": "断言弱化（contains_in→contains / 去 -Werror / 量化→存在性）",
    "M4": "恒真注入（main/ret/.p2align/.file 这类通用或 ABI 帧符号）",
    "M5": "claim 自标（inference→observation）",
    "M6": "YAML 变形（重复键/缩进提升/全角键名/flow 写法）",
    "M7": "数值/哈希篡改（计数 ±1 / sha256 改一位）",
}


# ── 沙箱（范式抄 poison_drill.sandbox：换 ge.ATOMS/EVIDENCE，finally 还原）─────────
@contextmanager
def sandbox() -> Iterator[Path]:
    """把 `atoms/` + `evidence/` 整树复制进 tempdir 并让规则引擎读副本。

    为什么整树复制而不是只放一张卡：门禁有**跨卡规则**（证据服务关系、清单一致性…），
    只放一张卡会让那些规则全变成假命中。复制两棵树是纯文本量级（56 卡），毫秒级。
    """
    tmp = Path(tempfile.mkdtemp(prefix="mutfuzz_"))
    # 579 任务 1：**工件层也要进沙箱**。只复制卡文本不够——实测全部 124 条 artifact/fixture
    #   路径都落在 `Examples/` 下，而 replay 会在**工件**上 unlink→重编译→还原、写 `build/`、
    #   读写 `manifest`；若这些仍打在真实仓库，紧随其后的 M6 全库扫描就会读到"某张卡的真实工件
    #   正处于删-建窗口"这一非常态 ⇒ finding 随机多出/消失（578b 实测 989/9/185 ↔ 991/7/185）。
    for name in ("atoms", "evidence", "Examples"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, tmp / name)
    (tmp / "build").mkdir(exist_ok=True)     # 空 build：卡命令产物 / manifest 全部落这里
    orig_a, orig_e = ge.ATOMS, ge.EVIDENCE
    ge.ATOMS, ge.EVIDENCE = tmp / "atoms", tmp / "evidence"
    # 跑批根 = tmp：`replay.run_root()` / gate 的工件规则全部改读 tmp（真实 ROOT 零副作用）。
    # 卡文本与工件同一个根内自洽 ⇒ 任何规则都读不到真实仓库的瞬态。
    with replay.batch_root(tmp):
        try:
            yield tmp
        finally:
            ge.ATOMS, ge.EVIDENCE = orig_a, orig_e
            shutil.rmtree(tmp, ignore_errors=True)


def _rel_in_sandbox(card: Path, tmp: Path) -> Path:
    return tmp / card.relative_to(ROOT)


def _findings_key(f: ge.Finding) -> tuple[str, str, str, str]:
    # 578 任务 1（575 定位、578 采用）：键并入**文案** ⇒ 四元组。
    #   旧键 = (规则 id, 严重度, 目标) 的病：同一张卡上**第二条**同规则告警会被"基线里已有该
    #   (规则, 目标)"吞掉 ⇒ 新告警在报告里完全看不见。M5 活雷正是此形态（变异给 prop-2 新增
    #   一条 OBSERVATION-LIVENESS warn，而 prop-1 的同类告警已在基线里 ⇒ 判成 escaped）。
    #   同步改动的解包点：`classify()` 里的 new_block/new_warn，以及两条自造假 new 集的 548 用例
    #   （它们原先按 3 元组构造 ⇒ 必须一起升 4 元组，否则 ValueError）。
    return (f.rule_id, f.severity, str(f.target), f.message)


def _snapshot() -> set[tuple[str, str, str, str]]:
    STATS["ge_runs"] += 1
    return {_findings_key(f) for f in ge.run(include_advice=False)}


# 548 Part 0 · 跑法观测（只计数，不影响判决）：对账"按卡批"到底省了多少次全库扫描 / replay
STATS: dict[str, int] = {"ge_runs": 0, "replay_runs": 0, "replay_skipped": 0}


# ── 七类变异算子（B1：纯函数，输入卡文本 → 返回 [(变异点, 变异后文本)]；绝不改原卡）──
def _drop_key(text: str, key: str) -> str | None:
    """删掉顶层或缩进态下的 `key:`（含其块式 list/scalar 的后续行）。不存在 ⇒ None。"""
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        m = re.match(rf"^(\s*){re.escape(key)}\s*:", ln)
        if not m:
            continue
        ind = len(m.group(1))
        j = i + 1
        while j < len(lines):
            nxt = lines[j]
            if nxt.strip() and (len(nxt) - len(nxt.lstrip())) <= ind:
                break
            j += 1
        return "\n".join(lines[:i] + lines[j:])
    return None


def mut_m1(text: str) -> list[tuple[str, str]]:
    """M1 字段删除：逐个删（各产一个变体）。"""
    out: list[tuple[str, str]] = []
    for key in ("artifact_sha256", "run_match_file", "negative_controls", "signed_by"):
        new = _drop_key(text, key)
        if new is not None and new != text:
            out.append((f"删 {key}", new))
    return out


# 558 Part B1/B2（548 建议）：**门禁真读的字段**——M2/M3 只在这些字段内做变形。
# 依据：gate_engine 里真正被解析的键（命令 / 工件路径 / 夹具 / 声明产出者 / nc 阴夹具 /
# 断言规则本身）。改它们才可能改变判决；落在 claim / 正文 / 注释里的"路径""contains_in"
# 门禁从不读，在那里变异 = **无效提问**（把门禁根本没看的地方算成逃逸，虚增逃逸率
# —— 543 P2 的逐逃逸定性正是为此）。实测：M3 的首个 `contains_in` 在 CONC-003/004/005
# 落在正文，修前被记成 3 条"逃逸"。
GATE_READ_KEYS = ("command", "artifact", "artifact_producer", "fixture", "fixtures",
                  "run_match_file", "artifacts", "negative_controls", "artifact_assert",
                  # 571 任务 1（真 bug 修复）：漏了 `actual` —— 门禁/复算**真读** `actual.run_match_keys`
                  #   （B3 EV-OUT-UNDECLARED-KEY）与 `actual.run_match_file`（replay），而这两个键是
                  #   **嵌套在 `actual:` 下**的 ⇒ 只列顶层键名永远匹配不到 ⇒ 整块 `actual` 被当成
                  #   "门禁不读"，实测 83 卡里 0 卡命中 `run_match_keys`、M3 的 80 条 n_a(out_of_scope)
                  #   相当一部分由此而来（把"没问"记成了"不适用"）。
                  "actual",
                  # 588 任务 2（读取面诚实化）：`check_evidence_matrix`（`gate_engine` 约 2901 行，
                  #   `ge._meta(p).get("matrix")`）**真读** matrix 块（编译器名/标准/优化级/arch）。
                  #   此前漏列 ⇒ matrix 区域被当成"门禁不读"，与 571 的 actual 同类「把没问记成不适用」的
                  #   尺子不诚实。matrix 取值里无路径后缀、也无 contains_in/-Werror/count 等 M2/M3 目标，
                  #   故补列后（单进程、即 classify 同款 `new=_snapshot()-baseline` 逻辑）逐变体零判决影响
                  #   —— 全量 `--jobs 4` 跑偶发的 27 条 M2 判决抖动，已定位为 ge.run 盘缓存 + 并行池陈旧态
                  #   假象（非 matrix 效应，见 _worklog_588.md；invalidate_meta 在单进程已生效，并行池交人）。
                  "matrix")
_PATHP = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:cpp|cc|cxx|py|asm|out|md|json)")


def _gate_read_spans(text: str) -> list[tuple[int, int]]:
    """卡内**门禁读取字段**的值区间（顶格键 → 下一个顶格键；仅在 frontmatter 内）。

    只认顶格 `key:` 开头的键，故缩进的列表项 / 块标量（`command: |` 的多行体）都自动留在
    所属键的区间内；`- item` 这类顶格列表项不当作新键（不会截断区间）。
    """
    spans: list[tuple[int, int]] = []
    pos = 0
    started = False
    cur: tuple[int, str] | None = None
    for ln in text.split("\n"):
        if ln.strip() == "---":
            if started and cur is not None:
                spans.append((cur[0], pos))
                cur = None
            started = not started
            pos += len(ln) + 1
            continue
        if started:
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):", ln)
            if m:
                if cur is not None:
                    spans.append((cur[0], pos))
                cur = (pos, m.group(1)) if m.group(1) in GATE_READ_KEYS else None
        pos += len(ln) + 1
    if started and cur is not None:
        spans.append((cur[0], pos))
    return spans


_COMMENT_HASH_RE = re.compile(r"(?:^|[ \t])#")


def _is_within_yaml_comment(text: str, idx: int) -> bool:
    r"""判断字符偏移 `idx` 是否落在其所在行的 YAML 注释段内。

    YAML 规定 `#` 只有在**行首**或**前面是空白/TAB** 时才开始注释（口径与 M6 里
    `ln.split("#", 1)[0]` 剥注释一致）。**保守**：只认这两种形态，不去猜引号内的 `#`
    （真实路径里的 `#` 前通常紧跟非空白字符，不会误判）。
    """
    ls = text.rfind("\n", 0, idx) + 1          # 本行行首
    return _COMMENT_HASH_RE.search(text[ls:idx]) is not None


def mut_m2(text: str) -> list[tuple[str, str | None]]:
    """M2 路径变形：对**门禁读取字段内**第一个带 `/` 的路径做三种写法变形。

    558 Part B2 收口：只认 `GATE_PATH_KEYS` 区间内的路径。若门禁读取面里没有可变形路径，
    返回**单例 out_of_scope**（`vtext=None`）⇒ 由 `run_fuzz` 计 `n_a(out_of_scope)`，
    **不再**去注释/正文里挑路径造出与门禁无关的"逃逸"。

    589 任务 2：跳过**字段块内注释行**（`   # ...路径...`）里的示意路径——它们落在
    `_gate_read_spans` 区间内，但改的是注释（YAML 解析后丢弃），此前造出 27 条等价伪变异
    （588 实测 9 卡 × 3）。加 `_is_within_yaml_comment`：在 span 内但落在注释里 ⇒ `continue`
    找下一个匹配；遍历完仍无真实路径 ⇒ 维持 out_of_scope 单例语义不变。
    """
    spans = _gate_read_spans(text)
    for m in _PATHP.finditer(text):
        if not any(s <= m.start() < e for s, e in spans):
            continue                       # 门禁不读的字段 / 正文 / 注释 ⇒ 不在提问面内
        if _is_within_yaml_comment(text, m.start()):
            continue                       # 落在字段块内注释行的示意路径 ⇒ 不是可变异目标
        p = m.group(0)
        if "/" not in p or p.startswith("./"):
            continue
        out: list[tuple[str, str]] = []
        for tag, newp in (("路径转大写", p.upper()), ("路径加 ./", "./" + p),
                          ("分隔符换反斜杠", p.replace("/", "\\"))):
            if newp != p:
                out.append((f"{tag}（{p} → {newp}）",
                            text[:m.start()] + newp + text[m.end():]))
        return out
    return [("M2 门禁读取面内无可变形路径（变异点会落在门禁不读的注释/正文）", None)]


def mut_m3(text: str) -> list[tuple[str, str | None]]:
    """M3 断言弱化：区间断言降级成全文存在性；去掉 -Werror；量化读数降成纯存在性。

    558 Part B1/B2：**只在门禁真读字段内**找可弱化点（`GATE_READ_KEYS`）。修前取全文第一个
    `contains_in`，实测 CONC-003/004/005 的首个出现落在**正文**（"contains_in 三条全中…"），
    弱化正文门禁从不读 ⇒ 记成 3 条**假逃逸**。门禁读取面内无可弱化点 ⇒ out_of_scope 单例。
    """
    spans = _gate_read_spans(text)

    def _in_gate(idx: int) -> bool:
        return any(s <= idx < e for s, e in spans)

    out: list[tuple[str, str]] = []
    for old, new, tag in (
            ("contains_in", "contains",
             "contains_in → contains（区间断言降级为全文存在性）"),
            ("absent_in", "absent",
             "absent_in → absent（区间断言降级为全文不存在）")):
        for m in re.finditer(re.escape(old), text):
            if _in_gate(m.start()):
                out.append((tag, text[:m.start()] + new + text[m.end():]))
                break
    m = re.search(r"-Werror", text)
    if m and _in_gate(m.start()):
        out.append(("-Werror 被删（编译告警不再算失败）", text.replace("-Werror", "", 1)))
    for m in re.finditer(r"(?m)^\s*(?:- )?\{?kind:\s*\w+.*?count:\s*\d+.*$", text):
        if _in_gate(m.start()):
            out.append(("量化断言降级（count: N → 纯存在性）",
                        text.replace(m.group(0),
                                     re.sub(r"count:\s*\d+", "", m.group(0)), 1)))
            break
    # ── 571 任务 1（L3 补样）：把 M3 的可判面从"只有 `_in`/`-Werror`/`count:`"扩到**最常见形状** ──
    #   为什么：570 实测 M3 可判样本只有 7（<59）⇒ 无法宣称"错误率有上界"。逐卡量形状后确认
    #   绝大多数卡的读取面里只有**普通断言条目**（flow 式 `{kind: contains, text: …}`），
    #   旧 M3 对它们无变体可产 ⇒ 全落 n_a(out_of_scope)。两条新变体都是**可证的弱化**：
    #     (a) 删掉一条断言条目 —— 卡少查一项（自带保证被削弱）；
    #     (b) 给 `contains` 断言追加一个**样板候选**（`.file` 这类恒真文本）—— 断言可被平凡输出满足。
    #   仍只在门禁读取面内动刀（558 B2 纪律）；带 `symbol:` 的条目留给 `_in` 路径，不互相抢。
    # 588 任务3：正则须**消费**整行行尾 `\r?\n`（而非 `(?=\n)` 前瞻 + 手工 `+1`）——
    #   旧写法在 CRLF 卡上：前瞻撞 `\r` 失配 ⇒ 变体根本不产；即便补前瞻，`+1` 只吃 `\r` 会留一条空行
    #   ⇒ LF/CRLF 同内容卡产出不一致。改为消费行尾后 LF 行为逐字不变（回归 `test_m3_crlf_eq_lf`）。
    for _m in re.finditer(r"(?m)^[ \t]*-[ \t]*\{[^\n}]*\}[ \t]*\r?\n", text):
        if _in_gate(_m.start()):
            out.append(("删掉一条 flow 式断言条目（弱化：卡少查一项）",
                        text[:_m.start()] + text[_m.end():]))
            break
    for _m in re.finditer(r"\{[^\n}]*kind:[ \t]*contains[ \t]*,[^\n}]*\}", text):
        _seg = _m.group(0)
        if not _in_gate(_m.start()) or "contains_any" in _seg or "symbol:" in _seg:
            continue
        _t = re.search(r"text:[ \t]*([^,}\n]+)", _seg)
        if not _t:
            continue
        _new = _seg.replace("kind: contains", "kind: contains_any").replace(
            _t.group(0), f"texts: [{_t.group(1).strip()}, \".file\"]")
        out.append(("contains 追加样板候选（弱化：恒真文本即可满足）",
                    text[:_m.start()] + _new + text[_m.end():]))
        break
    #   (c) 删掉一条 `run_match_keys` 声明 —— 读数键少声明一个；这条有**既有规则**看着
    #       （B3 `EV-OUT-UNDECLARED-KEY`：.out 读数键须在 run_match_keys 声明）⇒ 预期 blocked。
    if re.search(r"(?m)^\s*run_match_keys\s*:", text):
        # 571 实测两种写法都要覆盖：① flow 式内联列表 `run_match_keys: [a, b, c]`（EV-CONC-001
        #   就是这种，没有 `- item` 行 ⇒ 只找列表项会全部漏掉）；② 块式 `- "a"`。
        _mf = re.search(r"(?m)^([ \t]*)run_match_keys:[ \t]*\[([^\]]*)\]", text)
        if _mf and _in_gate(_mf.start()):
            _items = [x.strip() for x in _mf.group(2).split(",") if x.strip()]
            if len(_items) > 1:
                _new = _mf.group(0).replace(_mf.group(2), ", ".join(_items[1:]))
                out.append((f"删掉一条 run_match_keys 声明（弱化：少声明读数键 {_items[0]}）",
                            text[:_mf.start()] + _new + text[_mf.end():]))
        # 注意：列表项常带引号（`- "ab_tu_a"`）——571 实测漏了引号导致本变体对块式卡也不触发。
        for _m in re.finditer(r"(?m)^([ \t]*)-[ \t]*[\"']?([A-Za-z_][\w]*)[\"']?[ \t]*\r?\n",
                              text):
            # 只删"缩进深于 run_match_keys 行"的列表项，且必须落在门禁读取面内
            _k = re.search(r"(?m)^([ \t]*)run_match_keys\s*:", text)
            # 只取"`run_match_keys:` 之后"的列表项：YAML 里序列项与键**同缩进**也合法（实测
            # EV-CONC-001 就是这种写法），故不按缩进比较，改按位置（面内判定仍由 `_in_gate` 兜）。
            if not _k or _m.start() < _k.end():
                continue
            if _in_gate(_m.start()):
                out.append((f"删掉一条 run_match_keys 声明（弱化：少声明一个读数键 {_m.group(2)}）",
                            text[:_m.start()] + text[_m.end():]))
                break
    return out or [("M3 门禁读取面内无可弱化点（`_in`/`-Werror`/`count:`/断言条目/run_match_keys"
                    " 的字面量都在正文/注释）", None)]


def mut_m4(text: str) -> list[tuple[str, str]]:
    r"""M4 恒真注入：往 artifact_assert 里塞通用符号 / ABI 帧符号 / `.file` 类恒真断言。

    588 任务3：锚定正则旧式 `^(\s*)artifact_assert:\s*$` 无尾注释位 ⇒ `artifact_assert:  # 注`
    （全库 6 张：EV-HIST-001 / EV-MEM-001/002/004 / EV-UB-001/002）**整块 0 变体**（与 M6 matrix
    尾注释同类漏网）。改为消费整行行尾 `[ \t]*(?:#[^\n]*)?\r?\n`（兼容 CRLF、允许尾注释）；
    对无尾注释卡 m.end()/插入点等价 ⇒ LF 行为逐字不变（回归 `test_m4_artifact_assert_tail_comment`）。
    """
    m = re.search(r"(?m)^(\s*)artifact_assert:[ \t]*(?:#[^\n]*)?\r?\n", text)
    if not m:
        return []
    ind = m.group(1) + "  "
    out: list[tuple[str, str]] = []
    for tag, line in (
            ("注入通用符号 main", f'{ind}- {{kind: contains_in, symbol: main, text: "main"}}'),
            ("注入通用符号 ret", f'{ind}- {{kind: contains_in, symbol: call, text: "ret"}}'),
            ("注入 ABI 帧符号 .p2align",
             f'{ind}- {{kind: contains_in, symbol: main, text: ".p2align"}}'),
            # 543 P0：`contains_any` 读的是**复数 `texts`（列表）**，不是单数 `text`——
            # 写错字段会让 `_assert_targets` 取空 ⇒ gate 跳过 ⇒ 造出**假逃逸**（542 的教训）。
            ("注入 contains_any: ['.file']（合法形态）",
             f'{ind}- {{kind: contains_any, symbol: main, texts: [".file"]}}')):
        # m.end() 已消费行尾 ⇒ 注入行插在 `artifact_assert:…` 行的**下一行**（LF 下与旧写法逐字等价）
        out.append((tag, text[:m.end()] + line + "\n" + text[m.end():]))
    return out


# 574：M5 尺子 bug 的两个指纹（块定位 + 命题 id 回溯）
_CLAIM_BLOCK_RE = re.compile(r"(?m)^([ \t]*)claim_structured\s*:\s*(?:#.*)?$")
_CLAIM_TYPE_RE = re.compile(r"^([ \t]*)claim_type\s*:\s*(\w+)\s*$")
_PROP_ID_RE = re.compile(r"^([ \t]*)-[ \t]*(?:prop-id|id)\s*:\s*(\S+)\s*$")


def _claim_structured_span(text: str) -> tuple[int, int] | None:
    """`claim_structured:` 块的 (起, 止) 字符区间；块内缩进 > 键行缩进，或空行后遇同级键即止。"""
    m = _CLAIM_BLOCK_RE.search(text)
    if not m:
        return None
    base = len(m.group(1))
    ls = text.split("\n")
    start = m.start()
    # 找到该键所在的字符偏移对应的行，向后扫描到块结束
    pos, idx = 0, 0
    for i, ln in enumerate(ls):
        if pos == m.start():
            idx = i
            break
        pos += len(ln) + 1
    end = pos
    for ln in ls[idx + 1:]:
        if ln.strip() and (len(ln) - len(ln.lstrip())) <= base and not ln.lstrip().startswith("#"):
            break                      # 回到同级（或更浅）的非注释行 ⇒ 块结束
        end += len(ln) + 1
    return (start, min(end, len(text)))


def mut_m5(text: str) -> list[tuple[str, str | None]]:
    """M5 claim 自标：把 `claim_structured` 块里**每个** inference 命题**各自**改成 observation。

    574 修尺子（旧实现的 bug）：旧代码 `re.search(r"^(\\s*)claim_type:...")` 只取**全文第一个**
    `claim_type:` —— 而原子卡的命题写在 `claim_structured:` 列表里，且 **prop-1 几乎总是
    observation** ⇒ 第一个命中就是 observation ⇒ `!= "observation"` 不成立 ⇒ **永远返回空** ⇒
    29 条 inference 命题一条都改不到（v2 实测 M5 = 0/0/83 全 n_a，把"没问到"记成了"不适用"）。

    现在：① 先定位 `claim_structured:` 块（**只改块内**，卡面顶层的 claim_type 不动）；
    ② 块内每一行 `claim_type: inference` 各出一个独立变体（只改该行的值，其余逐字不动）；
    ③ 变体描述带命题 id（回溯最近的 `- id:` / `- prop-id:`）；
    ④ 纯函数、幂等、不碰原卡（与其他算子同范式）；块内无 inference ⇒ out_of_scope 单例。
    """
    out: list[tuple[str, str]] = []
    span = _claim_structured_span(text)
    if span is None:
        return []
    s, e = span
    ls = text.split("\n")
    # 逐行扫描块内，记录字符偏移
    off, lines = 0, []
    for ln in ls:
        lines.append((off, ln))
        off += len(ln) + 1
    for i, (o, ln) in enumerate(lines):
        if not (s <= o < e):
            continue
        m = _CLAIM_TYPE_RE.match(ln)
        if not m or m.group(2) == "observation":
            continue
        # 回溯最近的命题 id 行（同一块内）
        pid = "?"
        for j in range(i - 1, -1, -1):
            po, pln = lines[j]
            if not (s <= po < e):
                break
            pm = _PROP_ID_RE.match(pln)
            if pm:
                pid = pm.group(2)
                break
        new_ln = f"{m.group(1)}claim_type: observation"
        vtext = text[:o] + new_ln + text[o + len(ln):]
        out.append((f"[命题 {pid}] claim_type: {m.group(2)} → observation（自标绕过）", vtext))
    return out or [("M5 claim_structured 块内无 inference 命题（全是 observation ⇒ 无自标可测）",
                    None)]


# 587 任务1：非法值替换的「垃圾值」——逐键取自任务书 1.1（不存在标准/优化级/三元组/编译器）。
# 目的：证明 `check_evidence_matrix` 只看键存在性时这些**全逃逸**；任务 2 加值校验后应全部被 warn 拦。
_ILLEGAL_MATRIX_VALUE = {
    "std": "c++99",                          # 不存在的标准年份
    "opt": "-O9",                            # 不存在的优化级
    "arch": "z80-nonexistent",               # 不存在的架构三元组
    "compiler": "totally-not-a-compiler xyz",  # 无族名、无版本
}


def _illegal_value_line(ln: str, bad: str) -> str | None:
    """把 flow 列表 `  std: [c++11, c++17]` 的**第一个元素**换成非法值，结构与其余元素逐字不动。

    只处理 flow 列表形态（`[...]`）；块式嵌套形态返回 None（不造变体，避免改缩进结构）。
    逗号切分**跳过括号内的逗号**（半角/全角），保证 `Clang (ubuntu-latest runner 默认)` 这类值不被切坏。
    """
    i, j = ln.find("["), ln.rfind("]")
    if i < 0 or j <= i:
        return None
    head, content, tail = ln[:i + 1], ln[i + 1:j], ln[j:]
    depth, cut = 0, None
    for idx, ch in enumerate(content):
        if ch in "(（":
            depth += 1
        elif ch in ")）":
            depth -= 1
        elif ch == "," and depth == 0:
            cut = idx
            break
    rest = content[cut:] if cut is not None else ""      # 含逗号，保留其余元素逐字
    return head + bad + rest + tail


def _mut_matrix_values(text: str) -> list[tuple[str, str]]:
    r"""586 任务2 删键 + **587 任务1 非法值替换** + **588 任务1 放宽键行尾注释 / 块内注释行**：

    - 键行允许尾注释与行尾空白：`^matrix:[ \t]*(?:#[^\n]*)?\\n`（覆盖 `matrix:` / `matrix:   ` /
      `matrix:   # 任意注释` 三种形态）。原 `(matrix:)\\s*\\n` 在键行带 `#` 时失配 ⇒ 整块 0 变体
      （EV-MEM-004 漏网，588 任务0 坐实）。
    - 块体改为「连续的、缩进深于顶格的行」：`(?:[ \\t]+[^\\n]*\\n)+`，遇下一个顶格键 / `---` 自然终止
      （不会多吃后续顶格键，如 `fixture:`）。
    - 遍历时**先剥尾注释再解析键**：`s.split("#", 1)[0].strip()`；剥后为空（纯注释行）跳过；
      再做 partition(":")，避免注释里的冒号被当成 matrix 键。matrix 真实取值（编译器名/标准/优化级/
      arch）不含 `#`，剥注释对正常无注释行 / 值内含括号斜杠的行逐字无副作用（见 tests）。
    """
    out: list[tuple[str, str]] = []
    # `\r?\n` 兼容 CRLF：旧正则用 `\s*\n`（`\s` 含 `\r`）本就 CRLF 安全；本批把 `\s` 收紧为
    # `[ \t]` 后必须显式补 `\r?`，否则 CRLF 卡会在 `matrix:` 行尾 `\r` 处失配（588 任务 3.1 反向利用）。
    m = re.search(r"(?m)^matrix:[ \t]*(?:#[^\n]*)?\r?\n((?:[ \t]+[^\n]*\r?\n)+)", text)
    if not m:
        return out
    block = m.group(1)
    for ln in block.split("\n"):
        # 先剥尾注释（matrix 取值不含 #；值行尾注释随值替换，不影响解析）
        s = ln.split("#", 1)[0].strip()
        if not s or ":" not in s:
            continue
        k, _, v = s.partition(":")
        k = k.strip()
        if k not in ("compiler", "std", "opt", "arch"):
            continue
        # 删键：仅原三键（arch 缺键门禁不拦，删它只会造无意义变体）
        if k in ("compiler", "std", "opt"):
            new_block = block.replace(ln + "\n", "", 1)
            out.append((f"matrix 删键（移除 {k}: {v.strip()}）",
                        text[:m.start(1)] + new_block + text[m.end(1):]))
        # 587 任务1：非法值替换（四键）
        bad_ln = _illegal_value_line(ln, _ILLEGAL_MATRIX_VALUE[k])
        if bad_ln is not None and bad_ln != ln:
            out.append((f"matrix 非法值（{k}: {v.strip()} → 首元素 {_ILLEGAL_MATRIX_VALUE[k]}）",
                        text[:m.start(1)] + block.replace(ln + "\n", bad_ln + "\n", 1)
                        + text[m.end(1):]))
    return out


def mut_m6(text: str) -> list[tuple[str, str]]:
    """M6 YAML 变形：重复键 / 缩进提升 / 全角键名（键层攻击，仍有效）+
    586 任务2 新增 matrix 值层**删键**（EV-MATRIX 可检测）+ 587 任务1 新增 matrix **非法值替换**
    （586 实测全逃逸，587 任务2 加值校验后应收口）+ 保留"块式→flow"（583 已证等价，
    由报告层单列 `equivalent_invalid` 不进可判分母，作等价判据的生产触发与回归锁）。"""
    out: list[tuple[str, str]] = []
    m = re.search(r"(?m)^id:\s*(\S+)\s*$", text)
    if m:
        out.append(("重复 id 键（后写覆盖前写）",
                    text[:m.end()] + f"\nid: {m.group(1)}" + text[m.end():]))
    m2 = re.search(r"(?m)^(\s*)(\w+):\s*(.+)$", text)
    if m2:
        out.append((f"缩进提升（{m2.group(2)} 多缩一格，改变嵌套归属）",
                    text[:m2.start(2)] + " " + text[m2.start(2):]))
    m3 = re.search(r"(?m)^id:", text)
    if m3:
        out.append(("全角键名（ｉｄ）",
                    text[:m3.start()] + "ｉｄ:" + text[m3.end():]))
    m4 = re.search(r"(?m)^(\s*)(\w+):\s*\n((?:\1  .+\n)+)", text)
    if m4:
        items = [ln.strip() for ln in m4.group(3).strip().split("\n")]
        out.append((f"块式 → flow 写法（{m4.group(2)}）",
                    text[:m4.start()] + f"{m4.group(1)}{m4.group(2)}: {{{', '.join(items)}}}\n"
                    + text[m4.end():]))
    # 586 任务2：matrix 值层变异（删键，EV-MATRIX 可检测）——与上面的等价 block→flow 互补
    out.extend(_mut_matrix_values(text))
    return out


def mut_m7(text: str) -> list[tuple[str, str]]:
    """M7 数值/哈希篡改：sha256 改一位 + 第一个读数整数 ±1。"""
    out: list[tuple[str, str]] = []
    m = re.search(r"(?m)^(artifact_sha256:\s*)([0-9a-fA-F]{8,})", text)
    if m:
        h = m.group(2)
        flip = ("0" if h[0].lower() != "0" else "1") + h[1:]
        out.append((f"sha256 改一位（{h[:8]}… → {flip[:8]}…）",
                    text[:m.start(2)] + flip + text[m.end(2):]))
    m2 = re.search(r"(?m)^.*?(\b\d{3,}\b).*$", text)
    if m2:
        n = int(m2.group(1))
        out.append((f"读数篡改（{n} → {n + 1}）",
                    text[:m2.start(1)] + str(n + 1) + text[m2.end(1):]))
    return out


MUTATORS = {"M1": mut_m1, "M2": mut_m2, "M3": mut_m3, "M4": mut_m4,
            "M5": mut_m5, "M6": mut_m6, "M7": mut_m7}


# ── 判决（B2：三分类，定义写死；不许把 n_a 当 blocked）────────────────────────
# 543 P1：kind → 取值字段的映射（与 `gate_engine._assert_targets` 对齐；监工实测口径）。
# 字段名写错的条目会让 `_assert_targets` 取空 ⇒ gate 侧 `if not texts: continue` 跳过
# ⇒ 判成"逃逸"，实为**畸形变体**（542 的 M4 `.file` 单数 text 就是这么栽的）。
KIND_FIELD: dict[str, str] = {
    "contains": "text", "absent": "text",
    "contains_any": "texts", "absent_any": "texts",
    "contains_in": "symbol", "absent_in": "symbol",
    "call_count": "symbols",
}


def _malformed_asserts(meta: dict[str, Any]) -> list[str]:
    """变体合法性自检：返回字段不合规（按 kind 取不到 targets）的条目描述；空 = 合法。"""
    bad: list[str] = []
    for r in meta.get("artifact_assert") or []:
        if not isinstance(r, dict):
            bad.append(f"条目非对象：{r!r}")
            continue
        kind = str(r.get("kind") or "")
        need = KIND_FIELD.get(kind)
        if need is None:
            bad.append(f"未知 kind：{kind!r}")
            continue
        val = r.get(need)
        if isinstance(val, list):
            ok = bool(val)
        else:
            ok = bool(str(val or "").strip())
        if not ok:
            bad.append(f"{kind} 缺 {need}（字段名写错 ⇒ targets 取空 ⇒ 假逃逸）")
    return bad


def classify(card: str, op: str, baseline: set[tuple[str, str, str]],
             variant_text: str, sandbox_card: Path, tmp: Path) -> dict[str, Any]:
    """跑一次变异体的判决。返回 {verdict, new_block, new_warn, detail}。"""
    try:
        meta = replay.parse_frontmatter(variant_text)
    except ValueError as exc:
        return {"verdict": "n_a", "why": f"变异文本 YAML 解析失败：{exc}"}
    mal = _malformed_asserts(meta)
    if mal:
        # **不算守住也不算逃逸**：畸形变体不进拦截率分母/分子（543 P1 的核心纪律）
        return {"verdict": "n_a", "malformed": True,
                "why": "畸形变体（artifact_assert 字段不合规）：" + "；".join(mal)}
    sandbox_card.write_text(variant_text, encoding="utf-8")
    ge.invalidate_meta(sandbox_card)          # 579：进程内改盘后显式失效 gate 盘缓存，
    # 否则等长同 tick 改写（如 M2 路径转大写）会撞 (path,mtime_ns,size) 键 ⇒ 全库 ge.run()
    # 基线被污染、verdict 非确定性（588 任务 2 实测：补 matrix 前后 M2 判决抖动即此因）
    try:
        new = _snapshot() - baseline
    except Exception as exc:                       # noqa: BLE001  门禁自身崩了 = 不适用
        return {"verdict": "n_a", "why": f"gate 执行失败：{type(exc).__name__}: {exc}"}
    finally:
        pass
    # 578 任务 1：`_findings_key` 已是 4 元组（含文案）⇒ 用 `*_` 兼容解包（键里第 4 位只用于
    #   集合去重，报告仍只打 `规则:目标`，免得同一卡同一规则的多条告警把输出刷爆）。
    new_block = sorted({f"{r}:{t}" for r, s, t, *_ in new if s == "block"})
    new_warn = sorted({f"{r}:{t}" for r, s, t, *_ in new if s == "warn"})
    detail: dict[str, Any] = {"new_block": new_block, "new_warn": new_warn}
    if op in REPLAY_OPS and new_block:
        # 548 Part 0：门禁已经**严格**拦截 ⇒ replay 只可能再往 new_block 里加一条（同 verdict）
        # ⇒ 跳过这次真编译（M1/M7 的 replay 是全量里第二贵的动作，1.3s/次）。
        # 注意：`new_warn` -only 或"门禁没命中"时**必须照跑**——543 P0 的教训就是
        # "只看 gate 会把删必需字段判成逃逸"。
        STATS["replay_skipped"] += 1
        detail["replay_skipped"] = "gate 已严格拦截，replay 不改变结论（为提速跳过）"
    elif op in REPLAY_OPS:
        STATS["replay_runs"] += 1
        try:
            verdict, _log = replay.replay_card(sandbox_card, do_sanitizer=False)
        except Exception as exc:                   # noqa: BLE001
            return {"verdict": "n_a", "why": f"replay 执行失败：{type(exc).__name__}: {exc}"}
        detail["replay"] = verdict
        if verdict.startswith("infra_error"):
            return {"verdict": "n_a", "why": f"replay {verdict}（环境故障，不计入拦截率）"}
        if verdict.startswith("refute"):
            new_block.append(f"replay:{verdict.split(':', 1)[1]}")
            detail["new_block"] = sorted(set(new_block))
    if new_block:
        return {"verdict": "blocked", "kind": "strict", **detail}
    if new_warn:
        return {"verdict": "blocked", "kind": "warn_only", **detail}
    return {"verdict": "escaped", **detail}


def pick_cards(spec: str) -> list[Path]:
    """`all` = 证据卡 + 原子卡；也接受相对 ROOT 的 glob（如 `atoms/**.md`）。"""
    if spec == "all":
        cards = sorted(ge.EVIDENCE.rglob("EV-*.md")) + sorted(ge.ATOMS.rglob("ATOM-*.md"))
        return [c for c in cards if "README" not in c.name]
    return sorted(p for p in ROOT.glob(spec) if p.is_file())


def _controlled_dirty() -> list[str]:
    """受控目录（`evidence/` `atoms/`）相对 HEAD 的**残留**文件（569 任务 3 退出自检）。

    为什么需要：变异是"写卡→跑门禁→还原"，一旦进程被打断/异常，残留就可能悄悄留在受控目录里
    （567 实测 `EV-CONC-001.md` 有 3 行 M4 注入残留）。护栏用 `git diff --name-only`（只看文件名，
    不读内容 ⇒ 无编码坑）；git 不可用/超时 ⇒ 返回 `[]`（自检是护栏，不该把正常路径变成红灯）。
    """
    try:
        r = subprocess.run(["git", "diff", "--name-only", "--", "evidence/", "atoms/"],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        # 只吞**环境类**故障（git 不在 PATH / 超时）。**不能**用裸 `except Exception`：
        # 570 实测——那样会把 `NameError: subprocess` 这种**代码错误**也吞掉，
        # 让自检静默空转成"永远绿"（正是 567 立规矩要防的"没查成却像查过"）。
        return []
    if r.returncode != 0:
        return []
    return [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()]


def _exit_selfcheck(inflight: bool = False) -> None:
    """跑完（含异常路径）校验受控目录零差异；有残留 ⇒ **fail-loud**。

    `inflight=True`（已有异常在传播）时**只报不抛**——不能用一个护栏异常把真正的错因盖掉。
    """
    dirty = _controlled_dirty()
    if not dirty:
        return
    msg = (f"[mutation] ❌ 退出自检：受控目录有未还原残留 {len(dirty)} 个：\n"
           + "".join(f"    {d}\n" for d in dirty)
           + "    修法：先 `git diff -- evidence/ atoms/` 看差异；确认是变异残留就逐文件还原"
             "（`git diff --quiet -- evidence/ atoms/` 必须 exit 0）")
    print(msg, file=sys.stderr)
    if not inflight:
        raise SystemExit(1)


def _selfcheck_on_exit(fn):
    """569 任务 3：给跑变异的函数套一层"退出即自检受控目录零差异"（含异常路径）。

    为什么用**装饰器**而不是把主体包进 `try/finally`：主体一行都不重排（无重缩进风险），
    且手动转存 `__name__`/`__doc__`/`__wrapped__` —— 文档字符串契约（"三分类/drill"那段）
    与 `inspect.getsource` 都保持不变（有既有测试锁这条契约）。
    """
    def _inner(*a, **k):
        try:
            return fn(*a, **k)
        finally:
            _exit_selfcheck(inflight=sys.exc_info()[0] is not None)

    _inner.__name__ = getattr(fn, "__name__", "_inner")
    _inner.__doc__ = getattr(fn, "__doc__", None)
    _inner.__wrapped__ = fn
    return _inner


# ── 583 任务 1（N5）：规范化等价变异体（**报告层字段，判决路径一行不改**）──────────────
# 规格：`_arch_v9/05_攻击生成系统化.md` §四。判据（全部满足才算等价）：
#   equivalent ⟺ P1 视角相同 ∧ P2 视角相同 ∧ 缩进信号相同 ∧ **正文逐字不变** ∧ op ∉ REPLAY_OPS
#   语义：`equivalent=True` ⇒ "该变体在任何**只读 frontmatter** 的规则下，都不可能产生与原文不同的
#   finding"（这是**保守**主张：任一视角存疑即判 False）。
# 为何必须双解析器：单解析器相等会把**解析器走私**洗成等价——例：全角键名 `ｉｄ`、重复键、
#   缩进提升，在仓内自写子集解析器（P1）与 PyYAML 硬化 loader（P2）下分叉（见 556/557 的
#   `[parse-diverge]`/`[type-diverge]`）。只看一个解析器=自己给自己发免检单。
# 为何要"正文逐字不变"：M6 的"块式→flow"正则可能命中**正文**行 ⇒ 正文变了就不是"只读 frontmatter"
#   能覆盖的问题（另有规则读正文/工件），必须保守判不等价。
# 为何 M1/M7 排除：它们的判决还走 replay 读**工件与命令**，frontmatter 相等**不足以**判等价
#   （需要 TCE 式产物比对，属冻结项 W2）。
# 为何不做跨类型归一：`1` vs `true`、`"00000000"` vs `0` 是 556/557 的**真实走私信号**，归一会洗掉它们。
_FM_OPEN = "---"


def _frontmatter_text(text: str) -> str | None:
    """取 frontmatter 原文（与 `replay.parse_frontmatter` 同一约定：`---` 起始、`\\n---` 结束）。"""
    if not text.startswith(_FM_OPEN):
        return None
    end = text.find("\n---", 3)
    if end < 0:
        return None
    return text[3:end].strip("\n")


def _body_text(text: str) -> str:
    """frontmatter 之后的正文（含结束标记行）；用作"正文逐字不变"这道保守闸。"""
    if not text.startswith(_FM_OPEN):
        return text
    end = text.find("\n---", 3)
    return text if end < 0 else text[end:]


def _canon(obj: Any) -> str:
    """P1/P2 视角的规范化序列化：**键按字典序**；**不做跨类型归一**（类型名进串）。"""
    if isinstance(obj, dict):
        return "{" + ",".join(f"{_canon(str(k))}:{_canon(obj[k])}"
                              for k in sorted(obj, key=str)) + "}"
    if isinstance(obj, (list, tuple)):
        return "[" + ",".join(_canon(v) for v in obj) + "]"
    if isinstance(obj, bool) or obj is None:
        return f"{type(obj).__name__}:{obj!r}"
    if isinstance(obj, (int, float)):
        return f"{type(obj).__name__}:{obj!r}"
    return f"{type(obj).__name__}:{json.dumps(obj, ensure_ascii=False, default=str)}"


def _p2_view(text: str) -> str:
    """P2 = gate 的硬化解析视角（PyYAML + `_UniqueKeyLoader` 语义：重复键即抛）。

    ⚠️ 那个 loader 是 `gate_engine.check_frontmatter_hardening()` 的**内嵌类**（模块外取不到），
    故此处按**同一语义**实现最小 loader；并配一条**漂移护栏测试**：拿 gate 的**真实入口**
    （`check_frontmatter_hardening()`，指向临时沙箱）交叉核对——对同一批形态，本视图的分叉判定
    与 gate 的硬化信号必须一致。gate 若改语义，该护栏会红（不许静默漂移）。
    """
    fm = _frontmatter_text(text)
    if fm is None:
        return "<no-frontmatter>"
    try:
        import yaml
        from yaml.constructor import ConstructorError
    except ImportError:
        return "<no-pyyaml>"                 # 与 gate 一样"可见化"；此处保守：两侧都返回同串，

    class _StrictLoader(yaml.SafeLoader):   # 会让"缺 pyyaml"的两侧相等（不因此判等价，见下）
        def construct_mapping(self, node, deep=False):
            mapping = super().construct_mapping(node, deep=deep)
            seen: set = set()
            for key_node, _v in node.value:
                k = self.construct_object(key_node, deep=deep)
                if k in seen:
                    raise ConstructorError(None, None, f"duplicate key: {k}",
                                           key_node.start_mark)
                seen.add(k)
            return mapping

    try:
        loaded = yaml.load(fm, Loader=_StrictLoader)
    except Exception as exc:                 # noqa: BLE001  解析失败本身是**可区分**的视角
        return f"<error:{type(exc).__name__}>"
    return _canon(loaded if loaded is not None else {})


def equivalent_variant(op: str, orig_text: str, variant_text: str) -> bool:
    """583 N5 判据本体（保守：任一视角存疑即 False）。"""
    if op in REPLAY_OPS:
        return False                         # 硬边界：M1/M7 还读工件/命令（需 TCE，冻结）
    if variant_text == orig_text:
        return False                         # 空操作另有 n_a 分类，不重复标记
    if _body_text(orig_text) != _body_text(variant_text):
        return False                         # 正文被改 ⇒ 有规则读正文 ⇒ 保守判不等价
    if _frontmatter_text(orig_text) is None or _frontmatter_text(variant_text) is None:
        return False                         # 无 frontmatter ⇒ 不可判
    try:
        p1_o = _canon(replay.parse_frontmatter(orig_text))
        p1_v = _canon(replay.parse_frontmatter(variant_text))
    except ValueError:
        return False                         # 任一侧 P1 解析失败 ⇒ 不可判（保守）
    if p1_o != p1_v:
        return False
    p2_o, p2_v = _p2_view(orig_text), _p2_view(variant_text)
    if p2_o != p2_v or p2_o.startswith(("<no-pyyaml>", "<error:", "<no-frontmatter>")):
        return False                         # 视角分叉，或"环境缺 pyyaml/dog 解析失败"⇒ 不可判
    fm_o = _frontmatter_text(orig_text) or ""
    fm_v = _frontmatter_text(variant_text) or ""
    if ge._indent_smuggle_lines(fm_o) != ge._indent_smuggle_lines(fm_v):
        return False                         # 硬化信号①（缩进走私）不经解析 ⇒ 单独比一次
    return True


def selfcheck_equivalent(rep: dict[str, Any]) -> tuple[bool, list[str]]:
    """583 任务 1：等价变异体的**保守性自证**（防"把真逃逸洗成等价"）。

    判据：`equivalent=True` ⇒ 该变体不可能产生新 finding ⇒ `classify` 的语义下 verdict 必为
    `escaped`（`new_block` 空 ∧ `new_warn` 空）。任一 `equivalent` 变体带 new_block/new_warn
    或 verdict != escaped ⇒ **判据假阳性** ⇒ 列清单 fail-loud（宁可漏标，不许错标）。
    """
    bad: list[str] = []
    for r in rep.get("results") or []:
        if not r.get("equivalent"):
            continue
        if r.get("verdict") != "escaped" or r.get("new_block") or r.get("new_warn"):
            bad.append(f"{r['card']} · {r['op']} · {r['point']}"
                       f"（verdict={r.get('verdict')} new_block={r.get('new_block')}"
                       f" new_warn={r.get('new_warn')}）")
    return (not bad), bad


def _card_variants(card: Path, ops: list[str], baseline: set[tuple[str, str, str, str]],
                   tmp: Path) -> list[dict[str, Any]]:
    """**单张卡**的全部算子/变体（卡内串行，卡末 `finally` 还原沙箱副本）；返回该卡的 per 记录。

    580 任务 2：这是从 `run_fuzz` **原样抽出的**逐卡主体（一句判决逻辑都没改），
    串行路径与进程池 worker **共用同一份** ⇒ "并行不改判决"由构造保证，而不是靠两处代码同步。
    调用方负责沙箱与 `baseline`（worker 内进程生命周期内复用一次）。
    """
    text = card.read_text(encoding="utf-8")
    sb_card = _rel_in_sandbox(card, tmp)
    rel = card.relative_to(ROOT).as_posix()
    per: list[dict[str, Any]] = []
    try:
        for op in ops:
            variants = MUTATORS[op](text)
            if not variants:
                per.append({"card": rel, "op": op, "point": "-", "verdict": "n_a",
                            "why": "该卡本就没有被变异的字段（不适用）",
                            "equivalent": False})       # 583：无变体文本 ⇒ 不可判等价（保守）
                continue
            for point, vtext in variants:
                if vtext is None:
                    # 558 Part B2：算子自判"该提问超出面"（M2 在门禁读取面内找不到路径）
                    per.append({"card": rel, "op": op, "point": point,
                                "verdict": "n_a", "out_of_scope": True,
                                "why": f"out_of_scope：{point}",
                                "equivalent": False})    # 583：无变体文本 ⇒ 不可判等价（保守）
                    continue
                if vtext == text:
                    per.append({"card": rel, "op": op, "point": point,
                                "verdict": "n_a", "why": "变异为空操作",
                                "equivalent": False})    # 583：空操作另有分类，不重复标记
                    continue
                r = classify(card.stem, op, baseline, vtext, sb_card, tmp)
                per.append({"card": rel, "op": op, "point": point,
                            "reproduce": (f".venv\\Scripts\\python.exe tools/mutation_fuzz.py "
                                          f"--cards {rel} --operators {op} --limit 1"),
                            **r,
                            # 583 N5：报告层字段（**不进** `_variant_index` 的 5 字段、
                            # 不进拦截率分子分母；只在 n_a 细类里单列计数）
                            "equivalent": equivalent_variant(op, text, vtext)})
    finally:
        # 568 任务 3（567 抓到的隐患）：还原进 **finally** —— 任何异常 / KeyboardInterrupt /
        # 提前 return 都必须把沙箱副本还原成原卡文本，绝不把变异留到下一张卡
        # （EV-CONC-001.md 的 3 行 M4 注入残留就是这么来的）。
        sb_card.write_text(text, encoding="utf-8")
        ge.invalidate_meta(sb_card)          # 还原后同样显式失效（见 classify 内同款注释）
    return per


def _report(selected: list[Path], ops: list[str], per: list[dict[str, Any]],
            stats: dict[str, int], elapsed: float, *,
            jobs: int = 1, parallel: bool = False) -> dict[str, Any]:
    """由 per 记录 + STATS 读数构造报告（**单一真源**：串行与并行共用；580 抽取时一字未改口径）。"""
    # 586 任务2：等价变异体（equivalent=True）是"只读 frontmatter 视角下不可能改变判决"的
    # 纯格式重排（典型：matrix 块式→flow）；它们被 classify 判为 escaped 但**非真逃逸**。
    # 必须从可判分母 / escaped_list 剔除，单列 equivalent_invalid，否则虚增逃逸率（度量诚实化债）。
    judge = [r for r in per if not r.get("equivalent")]   # 可判（去掉等价无效变异）
    counts = {k: sum(1 for r in judge if r["verdict"] == k)
              for k in ("blocked", "escaped", "n_a")}
    counts["malformed"] = sum(1 for r in judge if r.get("malformed"))    # n_a 里单列一类（543 P1）
    # 558 Part B2：n_a 里再单列"变异点落在**门禁读取面之外**"（M2 out_of_scope）——
    # 这类提问与门禁无关，混进 escaped 会虚增逃逸率（543 P2 逐逃逸定性的教训）。
    counts["out_of_scope"] = sum(1 for r in judge if r.get("out_of_scope"))
    # 583 N5：等价变异体；586 任务2：单列 equivalent_invalid（**不进** blocked/escaped/分母，
    # 只作细类计数 + 单列清单；与 out_of_scope/malformed 同列）。
    counts["equivalent"] = sum(1 for r in per if r.get("equivalent"))
    counts["equivalent_invalid"] = counts["equivalent"]
    strict = sum(1 for r in judge if r["verdict"] == "blocked" and r.get("kind") == "strict")
    treated = counts["blocked"]
    denom = counts["blocked"] + counts["escaped"] or 1
    by_op: dict[str, dict[str, int]] = {}
    by_card: dict[str, dict[str, int]] = {}
    for r in per:
        for bucket, key in ((by_op, r["op"]), (by_card, r["card"])):
            d = bucket.setdefault(key, {"blocked": 0, "escaped": 0, "n_a": 0,
                                        "equivalent_invalid": 0})
            if r.get("equivalent"):
                d["equivalent_invalid"] += 1
            else:
                d[r["verdict"]] += 1
    # 565 Part 2：口径块（**只加不删**——既有 strict_rate/treated_rate 逐字保留，
    # 免得打散 548 的对账锁与 T2 快照；新增的是"带分子分母 + 区间"的自洽口径）
    judged = counts["blocked"] + counts["escaped"]        # 可判分母（n_a/malformed 永不进）
    rates = {"judged": judged, "n_a": counts["n_a"], "malformed": counts["malformed"],
             "strict": _rate_block(strict, judged),
             "treated": _rate_block(treated, judged),
             "escape": _rate_block(counts["escaped"], judged),
             # 全分母率**正名**为 treated_all（不得叫 strict —— 565 口径纪律）
             "treated_all": _rate_block(treated, len(per))}
    op_rates, op_flags = _op_rates(per)
    return {"cards": [c.relative_to(ROOT).as_posix() for c in selected],
            "operators": ops, "variants": len(per), **counts,
            "strict_blocked": strict,
            "strict_rate": round(strict / denom, 4),
            "treated_rate": round(treated / denom, 4),
            "rates": rates, "by_operator_rates": op_rates, "rate_flags": op_flags,
            "by_operator": by_op, "by_card": by_card,
            "elapsed_s": round(elapsed, 2),
            "ge_runs": stats["ge_runs"], "replay_runs": stats["replay_runs"],
            "replay_skipped": stats["replay_skipped"],
            "escaped_list": [r for r in judge if r["verdict"] == "escaped"],
            # 583 任务 1（N5）：等价变异体清单（判决/分母零改）
            "equivalent_keys": [f"{r['card']} · {r['op']} · {r['point']}"
                                for r in per if r.get("equivalent")],
            # 586 任务2：等价无效变异清单（已从 escaped/分母剔除，单列；不再算进 blocked/escaped）
            "equivalent_invalid_list": [{"card": r["card"], "op": r["op"], "point": r["point"]}
                                        for r in per if r.get("equivalent")],
            # 580 任务 2：只**新增**字段（既有字段一字未改）
            "jobs": jobs, "parallel": bool(parallel),
            "results": per}


def _real_root_fingerprint() -> str:
    """真实根指纹：`Examples + atoms + evidence` 全树（排序后 路径 + 内容 sha256）。

    580 任务 3 的"输入冻结"双保险：进程池启动前/收尾后各算一次，不一致 ⇒ 根隔离回归
    （579 本应保证零副作用，这道是抓回归的哨兵）。口径与监工 579 验收用的一致。
    """
    h = hashlib.sha256()
    for name in ("Examples", "atoms", "evidence"):
        base = ROOT / name
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if p.is_file():
                h.update(p.relative_to(ROOT).as_posix().encode())
                h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


# ── 580 任务 2：卡间**进程**并行（`--jobs N>=2`；默认 OFF = 上面的串行路径）────────────
# 为什么进程池 + 每 worker 一个根：卡间共享一个 sandbox 根时，worker A 改卡 X 的全库 `ge.run()`
# 会读到 worker B 正在变异的卡 Y（跨卡污染，重现 548 之前的 bug），且 ge.run 持 GIL、模块全局
# STATS/缓存会竞态。每 worker 独占 `mutworker_*` 根（卡文本 + 工件同根自洽）后，卡间天然隔离。
_MUT_WORKER: dict[str, Any] = {}


def _worker_init(ops: list[str]) -> None:
    """worker 进程初始化：**一次性**建好本进程独占的 sandbox 根 + batch_root + 全库 baseline。"""
    tmp = Path(tempfile.mkdtemp(prefix="mutworker_"))
    for name in ("atoms", "evidence", "Examples"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, tmp / name)
    (tmp / "build").mkdir(exist_ok=True)
    ge.ATOMS, ge.EVIDENCE = tmp / "atoms", tmp / "evidence"
    cm = replay.batch_root(tmp)
    cm.__enter__()              # 手工进入：worker 生命周期内持续生效（退出时在 _worker_cleanup 还原）
    baseline = _snapshot()      # 本 worker 的全库基线（**在计数清零之前**：见下）
    for k in STATS:
        STATS[k] = 0            # 计数清零放在基线之后 ⇒ 增量只含**变体扫描**，可与串行口径对齐
    _MUT_WORKER.update({"tmp": tmp, "ops": list(ops), "cm": cm, "baseline": baseline,
                        "pid": os.getpid()})
    atexit.register(_worker_cleanup)


def _worker_cleanup() -> None:
    """worker 退出：还原跑批根与卡目录、删掉自己的 tmp 根（不在真实 build/ 留残片）。

    真 worker 是进程退出，不还原也无害；但**测试会在本进程直接调 `_worker_init`**（验证
    "异根/异锁"），故这里把所有副作用都还原干净（可重复调用、幂等）。
    """
    w = _MUT_WORKER
    if not w:
        return
    try:
        w["cm"].__exit__(None, None, None)
    except Exception:                       # noqa: BLE001 退出路径不反噬
        pass
    ge.ATOMS, ge.EVIDENCE = ROOT / "atoms", ROOT / "evidence"
    shutil.rmtree(w.get("tmp"), ignore_errors=True)
    _MUT_WORKER.clear()


def _worker_card(card_str: str) -> tuple[str, list[dict[str, Any]], dict[str, int], int]:
    """worker 内跑一张卡：返回 (卡 rel, 该卡全部变体的 per 记录, 本卡的 STATS 增量, worker pid)。

    判决逻辑 = 与串行**同一份** `_card_variants`（不复制、不改一字）。
    本卡增量只含**变体扫描**（基线已在 init 时计过并被清零）⇒ 与串行的"变体计数"同口径。
    """
    w = _MUT_WORKER
    card = Path(card_str)
    before = dict(STATS)
    per = _card_variants(card, w["ops"], w["baseline"], w["tmp"])
    delta = {k: STATS[k] - before[k] for k in STATS}
    return card.relative_to(ROOT).as_posix(), per, delta, int(w["pid"])


@_selfcheck_on_exit
def run_fuzz_parallel(cards: list[Path], ops: list[str], limit: int, jobs: int,
                      progress: bool = False) -> dict[str, Any]:
    """进程池并行跑批（卡维并行；卡内仍串行 + 卡末还原）。结果**按串行顺序重排**后交 `_report`。

    确定性纪律：完成顺序是不确定的，故主进程收齐后按 `selected` 顺序、卡内按 worker 返回的
    原始顺序拼接 ⇒ `results`/`by_operator`/`by_card`/counts 与 `--jobs 1` 逐条相等。
    """
    t0 = time.perf_counter()
    selected = cards[:limit]
    fp_before = _real_root_fingerprint()
    got: dict[str, tuple[list[dict[str, Any]], dict[str, int]]] = {}
    worker_pids: set[int] = set()
    with ProcessPoolExecutor(max_workers=jobs, initializer=_worker_init,
                             initargs=(list(ops),)) as ex:
        futs = {ex.submit(_worker_card, str(c)): c for c in selected}
        done = 0
        for fut in as_completed(futs):
            card = futs[fut]
            try:
                rel, per, delta, pid = fut.result()
                worker_pids.add(pid)
            except Exception as exc:        # noqa: BLE001  丢卡会改变分母 ⇒ fail-loud
                raise SystemExit(f"[mutation] ❌ worker 失败：卡 "
                                 f"{card.relative_to(ROOT).as_posix()} · "
                                 f"{type(exc).__name__}: {exc}") from exc
            got[rel] = (per, delta)
            done += 1
            if progress:
                print(f"[mutation] ({done}/{len(selected)}) {rel}", file=sys.stderr, flush=True)
    per_all: list[dict[str, Any]] = []
    stats = {k: 0 for k in STATS}
    for c in selected:                      # **按串行顺序**重排（确定性）
        rel = c.relative_to(ROOT).as_posix()
        if rel not in got:
            raise SystemExit(f"[mutation] ❌ 卡 {rel} 无结果（worker 静默丢卡 ⇒ 分母会变）")
        per, delta = got[rel]
        per_all.extend(per)
        for k in stats:
            stats[k] += delta[k]
    # 计数口径（与串行**同口径**，供对账）：`ge_runs` 记**逻辑**全库扫描数 = 1 次基线 + 每变体 1 次。
    # 每个 worker 实际各自 materialize 了一次基线（并行必需：不跨进程传大 set），真实次数记在
    # `parallel_baseline_scans`，**不**混进 ge_runs —— 否则 jobs1 与 jobsN 的三计数永远无法相等。
    stats["ge_runs"] += 1
    rep = _report(selected, ops, per_all, stats, time.perf_counter() - t0,
                  jobs=jobs, parallel=True)
    rep["parallel_baseline_scans"] = len(worker_pids)
    fp_after = _real_root_fingerprint()
    rep["root_fingerprint_ok"] = (fp_before == fp_after)
    if fp_before != fp_after:               # 任务 3.2：输入冻结哨兵
        rep["invalid"] = "真实根（Examples/atoms/evidence）跑批前后指纹不一致 ⇒ 结果标记 invalid"
    return rep


def _jobs_value(spec: str | int, n_cards: int) -> int:
    """`--jobs` 取值：`auto` = min(4, cpu_count-1, 卡数)（默认 1 = 串行）。"""
    if isinstance(spec, int):
        return max(1, spec)
    if str(spec).strip().lower() == "auto":
        return max(1, min(4, (os.cpu_count() or 2) - 1, n_cards))
    try:
        return max(1, int(str(spec).strip()))
    except ValueError:
        return 1


def _run_jobs(cards: list[Path], ops: list[str], limit: int, jobs: int = 1,
              progress: bool = False) -> dict[str, Any]:
    """分派：`jobs<=1` 走**今天的串行路径**（逐字节等价），否则走进程池。"""
    selected = cards[:limit]
    if jobs <= 1:
        return run_fuzz(cards, ops, limit, progress=progress)
    return run_fuzz_parallel(selected, ops, len(selected), jobs, progress=progress)


@_selfcheck_on_exit
def run_fuzz(cards: list[Path], ops: list[str], limit: int,
             progress: bool = False) -> dict[str, Any]:
    """主循环（drill 范式 + 548 Part 0 按卡批）：**卡维外层**，一张卡的全部变体共用一次全库基线。

    548 Part 0 的三条跑法约定（红线：不许为提速牺牲跨卡规则）：
     ① **按卡批**：外层是卡，一张卡的全部算子/变体连着跑；基线全库扫描（`_snapshot`）只在
        进沙箱时做 **1 次**，整轮所有卡共用；每张卡跑完统一还原沙箱副本（进下一张卡前不留残迹）。
     ② **跨卡规则不裁剪**：每个变体仍是**全库** `ge.run()`，diff 也是全量
        （`new - baseline`，不过滤 `target == 本卡`）——跨卡规则（EV-ID-UNIQUE / serves /
        relations / concepts…）的命中可能落在**别的卡**上，按卡裁剪会把它们漏掉。
     ③ **replay 按卡批省**：M1/M7 需要真跑 replay，但"门禁已严格拦截"的变体跳过（结论不变），
        见 `classify` 里的说明。
    提速的主杠杆不在这里，而在 `gate_engine` 的 frontmatter 解析缓存（见 548 §1）；本函数只
    负责**不浪费**扫描次数，并把 `ge_runs`/`replay_runs` 记进报告，便于事后核对。
    """
    t0 = time.perf_counter()
    for k in STATS:
        STATS[k] = 0
    selected = cards[:limit]
    per: list[dict[str, Any]] = []
    with sandbox() as tmp:
        baseline = _snapshot()          # 全库基线：所有卡共用这 **1 次**
        for ci, card in enumerate(selected, 1):
            rel = card.relative_to(ROOT).as_posix()
            if progress:                # 全量轮要能看出"跑到哪了 / 还活着"（不是静默 10 分钟）
                print(f"[mutation] ({ci}/{len(selected)}) {rel}", file=sys.stderr, flush=True)
            # 580 任务 2：逐卡主体已原样抽到 `_card_variants`（判决逻辑一字未动），
            # 串行路径与进程池 worker 共用同一份 ⇒ 并行不改判决由构造保证。
            per.extend(_card_variants(card, ops, baseline, tmp))
    return _report(selected, ops, per, dict(STATS), time.perf_counter() - t0,
                   jobs=1, parallel=False)


# ── 565 Part 2：报告口径层（**只影响呈现，不动任何判决/分类**）─────────────────
# 为什么必须做：563 N9 误报的教训是"同名不同义的率会直接误导决策"——平均分/裸比率看不出
# "M2 207/207 全逃逸"这种活雷，也看不出"M5 可判样本是 0（根本不该给率）"。
# 口径纪律（565b 监工确认）：
#   * 拦截率/处置率/逃逸率这类 k/n 一律用**双侧** `stat_bounds.cp_interval`（经 proportion()）；
#   * "零失效上界"这类陈述才用**单侧** `cp_upper_one_sided`（本文件当前无此类陈述）；
#   * **比率禁止无分母单独出现**；n_a / malformed **永不进分母**；
#   * 可判样本 n=0 ⇒ `insufficient evidence`，**不算率、不填 0**。
_SAMPLE_TARGET_59 = 59        # n_for_upper_bound_zero(0.05, 0.95)：零失效压到 ≤5% 所需样本量


def _rate_block(k: int, n: int, conf: float = 0.95) -> dict[str, Any]:
    """比率块：分子/分母/点估计/C-P 双侧区间；**n=0 ⇒ 明说 insufficient evidence**。"""
    if n <= 0:
        return {"numerator": k, "denominator": 0, "point": None, "cp_low": None,
                "cp_high": None, "conf": conf,
                "note": "insufficient evidence（可判样本 n=0：不算率、不填 0）"}
    blk = stat_bounds.proportion(k, n, conf)
    return {kk: (round(vv, 6) if isinstance(vv, float) else vv) for kk, vv in blk.items()}


def _rate_line(label: str, blk: dict[str, Any]) -> str:
    """人读行：`标签 分子/分母 = 点估计 · C-P 95% 区间 [lo, hi]`（n=0 走 note）。"""
    if blk["denominator"] <= 0:
        return f"{label} {blk['numerator']}/0 —— {blk['note']}"
    return (f"{label} {blk['numerator']}/{blk['denominator']} = {blk['point']:.2%}"
            f" · C-P {blk['conf']:.0%} 区间 [{blk['cp_low']:.2%}, {blk['cp_high']:.2%}]")


def _op_rates(per: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    """分算子口径块 + 需要显形的标注（活雷 / 样本不足 / 不可判）。"""
    out: dict[str, Any] = {}
    flags: list[str] = []
    for op in sorted({r["op"] for r in per}):
        # 586 任务2：等价无效变异不进分算子口径（与全局一致），单列 equivalent_invalid。
        rows = [r for r in per if r["op"] == op and not r.get("equivalent")]
        blocked = sum(1 for r in rows if r["verdict"] == "blocked")
        escaped = sum(1 for r in rows if r["verdict"] == "escaped")
        strict_op = sum(1 for r in rows
                        if r["verdict"] == "blocked" and r.get("kind") == "strict")
        n_a_op = sum(1 for r in rows if r["verdict"] == "n_a")
        eq_inv_op = sum(1 for r in per if r["op"] == op and r.get("equivalent"))
        judged = blocked + escaped                       # 可判样本（n_a 永不进）
        out[op] = {"judged": judged, "n_a": n_a_op,
                   "equivalent_invalid": eq_inv_op,
                   "strict": _rate_block(strict_op, judged),
                   "treated": _rate_block(blocked, judged),
                   "escape": _rate_block(escaped, judged)}
        if judged == 0:
            flags.append(f"{op}：可判样本 n=0 ⇒ insufficient evidence（不算率、不填 0）")
        elif escaped == judged:
            e = out[op]["escape"]
            flags.append(f"{op}：**活雷** —— 逃逸 {escaped}/{judged}"
                         f"（区间 [{e['cp_low']:.2%}, {e['cp_high']:.2%}]）")
        elif judged < _SAMPLE_TARGET_59:
            flags.append(f"{op}：可判样本仅 {judged} < {_SAMPLE_TARGET_59} ⇒ 样本不足；"
                         f"要宣称'逃逸率≤5%@95%'需补样至 n≥{_SAMPLE_TARGET_59}")
    return out, flags


# ── 579 任务 2：确定性自检（把"同一输入两次跑必须一致"变成机器判据）───────────────
# 为何必须自证：这类非确定性**只能靠重跑发现**——578 若不是"重跑一次核对提交产物"就完全看不见
# （测试全绿、单次跑也自洽）。子集至少覆盖"动工件层"的 M1/M7（真实工件被删建的源头）与
# "跨卡 finding"的 M6（034 幻影 finding 的观察面）。
_SELFCHECK_OPS = tuple(MUTATORS)
_SELFCHECK_FIELDS = ("verdict", "kind", "why", "new_block", "new_warn")
_SELFCHECK_CARDS_PATH = ROOT / "data" / "mutation" / "selfcheck_cards.json"


class SelfcheckCoverageError(RuntimeError):
    """自检小卡集对某算子 0 blocked ⇒ 选卡无效、自检空转（绿得没有判别力）⇒ fail-loud。"""


def _load_selfcheck_cards(path: Path | None = None) -> list[Path]:
    """加载**固定自检小卡集**（`data/mutation/selfcheck_cards.json`，相对仓库根）。

    该集固定、不随命令行 `--limit/--cards` 变化 ⇒ 自检结果跨运行稳定可比（主跑规模不再拖慢自检）。
    """
    p = Path(path) if path is not None else _SELFCHECK_CARDS_PATH
    data = json.loads(p.read_text(encoding="utf-8"))
    rels = data["cards"] if isinstance(data, dict) else data
    cards = [ROOT / str(r) for r in rels]
    missing = [str(c.relative_to(ROOT)) for c in cards if not c.is_file()]
    if missing:
        raise SelfcheckCoverageError(f"自检小卡集缺文件：{missing}")
    return cards


def _assert_selfcheck_coverage(rep: dict[str, Any], sub_ops: list[str]) -> None:
    """小卡集必须对**每个**算子都产出 ≥1 条 `blocked`；否则该算子自检空转 ⇒ fail-loud。"""
    blk: dict[str, int] = {o: 0 for o in sub_ops}
    for r in rep["results"]:
        if r["verdict"] == "blocked" and r["op"] in blk:
            blk[r["op"]] += 1
    bad = [o for o in sub_ops if blk[o] == 0]
    if bad:
        raise SelfcheckCoverageError(
            f"选卡失效：算子 {bad} 在自检小卡集上 0 blocked（逐算子 blocked 数={blk}）"
            " ⇒ 该算子自检空转、绿得没有判别力")


def _variant_index(rep: dict[str, Any]) -> dict[tuple[str, str, str], tuple[str, ...]]:
    """逐变体可比值索引。键 = (卡, 算子, 变异点)；值 = 判决相关字段的规范化快照。

    579 起 `gate_engine._rel()` 跟随跑批根 ⇒ finding 的 target 是**仓内相对形**，
    不含沙箱临时目录名 ⇒ 两次跑可直接逐字比对（此前必须手工归一化临时路径）。
    """
    out: dict[tuple[str, str, str], tuple[str, ...]] = {}
    for r in rep["results"]:
        out[(r["card"], r["op"], r["point"])] = tuple(
            json.dumps(r.get(f), ensure_ascii=False, sort_keys=True) for f in _SELFCHECK_FIELDS)
    return out


def selfcheck_determinism(cards: list[Path], ops: list[str], limit: int, first: dict[str, Any],
                          progress: bool = False, jobs: int = 1,
                          selfcheck_cards_path: Path | None = None) -> tuple[bool, list[str]]:
    """对**固定自检小卡集 × 全 7 算子**重跑并逐变体比对；返回 (是否一致, 抖动清单)。

    589 任务 1（本包）：重跑对象从"`_SELFCHECK_OPS`（原 3 算子：M1/M6/M7）× **全卡**"改为
    "**全 7 算子 × 固定小卡集**（`data/mutation/selfcheck_cards.json`）"，与主跑的
    `--cards/--limit` 解耦 ⇒ 自检覆盖更全（M2–M5 的非确定性也看得见）且不再退化成全量串行。
    启动前先断言小卡集对每个算子 ≥1 blocked（`_assert_selfcheck_coverage`，否则 fail-loud）。
    `jobs > 1` 时**再**用 `jobs=1` 串行对账**同一小卡集**（跨 jobs 判决一致性硬门）。
    """
    sc = _load_selfcheck_cards(selfcheck_cards_path)
    sub_ops = list(_SELFCHECK_OPS)                  # 全 7，固定（不随主跑 --operators 变）
    sc_rel = {c.relative_to(ROOT).as_posix() for c in sc}
    ref = _run_jobs(sc, sub_ops, len(sc), jobs=jobs, progress=progress)
    _assert_selfcheck_coverage(ref, sub_ops)        # 选卡有效性 fail-loud（0 blocked ⇒ 报错退出）
    a = _variant_index(ref)
    diffs: list[str] = []
    # ① 与主跑(first)的小卡集部分对账（主跑为全量时覆盖小卡集；--cards 很窄时该段自然为空）
    b_main = {k: v for k, v in _variant_index(first).items() if k[0] in sc_rel}
    for k in sorted(set(a) & set(b_main)):
        if a[k] != b_main[k]:
            diffs.append(f"[main] {k[0]} · {k[1]} · {k[2]}（{a[k]} ≠ {b_main[k]}）")
    # ② 跨 jobs 对账（jobs>1）或同 jobs 重跑（jobs==1）
    rounds: list[tuple[str, int]] = [("jobs1（串行对账）", 1)] if jobs > 1 else [("重跑", 1)]
    for tag, jn in rounds:
        other = _run_jobs(sc, sub_ops, len(sc), jobs=jn, progress=progress)
        b = _variant_index(other)
        for k in sorted(set(a) | set(b)):
            if a.get(k) != b.get(k):
                diffs.append(f"[{tag}] {k[0]} · {k[1]} · {k[2]}（{a.get(k)} ≠ {b.get(k)}）")
    return (not diffs), diffs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="539 · 自动变异器（L3 第一块）：找毒样例没覆盖的新逃逸")
    ap.add_argument("--cards", default="all", help="all | 相对 ROOT 的 glob（默认 all）")
    ap.add_argument("--operators", default=",".join(OPS), help=f"逗号分隔，可选 {','.join(OPS)}")
    ap.add_argument("--limit", type=int, default=5, help="最多处理多少张卡（默认 5，小批先跑通）")
    ap.add_argument("--report", default="data/mutation/last.json", help="JSON 报告落盘路径")
    ap.add_argument("--fail-on-escaped", action="store_true",
                    help="有 escaped 即 exit 1（默认恒 0：escaped 是本工具的**产物**，不是红灯）")
    ap.add_argument("--progress", action="store_true",
                    help="逐卡打印进度到 stderr（全量轮用：不许静默跑十分钟）")
    ap.add_argument("--selfcheck-determinism", action="store_true",
                    help="579：跑完立即对关键子集（M1/M6/M7）重跑一次并逐变体比对；"
                         "不一致 ⇒ fail-loud exit 2（非确定性未被容忍）")
    ap.add_argument("--jobs", default="1",
                    help="580：卡间进程并行度。`1`（默认）= 今天的串行路径；`auto` = "
                         "min(4, cpu_count-1, 卡数)；N>=2 = 进程池（每 worker 一个 sandbox 根）")
    ap.add_argument("--selfcheck-equivalent", action="store_true",
                    help="583：等价变异体判据的**保守性自证**——凡标 equivalent 的变体，其 "
                         "new_block/new_warn 必须为空（否则判据假阳性 ⇒ exit 2）。"
                         "--selfcheck-determinism 亦会带上本检查")
    a = ap.parse_args(argv)
    ops = [o for o in a.operators.split(",") if o]
    bad = [o for o in ops if o not in MUTATORS]
    if bad:
        print(f"[mutation] 未知算子：{bad}（可选 {','.join(OPS)}）", file=sys.stderr)
        return 2
    cards = pick_cards(a.cards)
    if not cards:
        print(f"[mutation] --cards {a.cards} 未匹配到任何卡", file=sys.stderr)
        return 2
    jobs = _jobs_value(a.jobs, min(len(cards), a.limit))
    rep = _run_jobs(cards, ops, a.limit, jobs, progress=a.progress)
    out = ROOT / a.report
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[mutation] 卡 {len(rep['cards'])} 张 · 算子 {len(ops)} 类 · 变体 {rep['variants']} 个")
    print(f"[mutation] blocked={rep['blocked']}（严格 {rep['strict_blocked']}） "
          f"escaped={rep['escaped']} n_a={rep['n_a']}（其中 malformed={rep['malformed']}）")
    print(f"[mutation] 严格拦截率 {rep['strict_rate']:.1%} · 含 warn 处置率 {rep['treated_rate']:.1%}")
    # 565 Part 2：口径自洽层（分子/分母 + 点估计 + C-P 双侧 95% 区间；**只用双侧**）
    _r = rep.get("rates") or {}
    if _r:
        print(f"[mutation] 可判分母 = {_r['judged']}"
              f"（变体 {rep['variants']} − n_a {_r['n_a']} − malformed {_r['malformed']}）"
              "；n_a/malformed **永不进拦截率分母**")
        print(f"[mutation] {_rate_line('严格拦截率', _r['strict'])}")
        print(f"[mutation] {_rate_line('含 warn 处置率', _r['treated'])}")
        print(f"[mutation] {_rate_line('逃逸率    ', _r['escape'])}")
        print(f"[mutation] {_rate_line('全分母率 treated_all', _r['treated_all'])}"
              "（**全分母率只叫 treated_all，不得叫 strict**）")
        print("[mutation] 分算子（可判 = blocked + escaped；n_a 单列）：")
        for _op, _d in (rep.get("by_operator_rates") or {}).items():
            if _d["judged"] == 0:
                print(f"[mutation]   {_op}  可判 0（n_a {_d['n_a']}）· "
                      "insufficient evidence（不算率、不填 0）")
                continue
            print(f"[mutation]   {_op}  可判 {_d['judged']}（n_a {_d['n_a']}）· "
                  f"严格 {_d['strict']['numerator']}/{_d['judged']} = "
                  f"{_d['strict']['point']:.2%} · 逃逸 {_d['escape']['numerator']}/"
                  f"{_d['judged']} = {_d['escape']['point']:.2%} · "
                  f"C-P95 [{_d['escape']['cp_low']:.2%}, {_d['escape']['cp_high']:.2%}]")
        for _f in (rep.get("rate_flags") or []):
            print(f"[mutation] ⚠ {_f}")
    print(f"[mutation] 全库扫描 ge.run={rep['ge_runs']} 次 · replay={rep['replay_runs']} 次"
          f"（门禁已拦而跳过 {rep['replay_skipped']} 次）· 耗时 {rep['elapsed_s']}s")
    for r in rep["escaped_list"]:
        print(f"[mutation] ✗ ESCAPED {r['card']} · {r['op']} · {r['point']}")
    try:                       # 548：--report/--out 可以是仓库外的绝对路径（cppbible 透传时会）
        shown = out.relative_to(ROOT).as_posix()
    except ValueError:
        shown = str(out)
    print(f"[mutation] 报告：{shown}")
    print(f"[mutation] 并行：jobs={jobs}（{'进程池' if jobs > 1 else '串行路径'}）"
          f" · 卡 {len(rep['cards'])} 张 · variants={rep['variants']}")
    if rep.get("root_fingerprint_ok") is False:      # 580 任务 3.2：输入冻结哨兵
        print(f"[mutation] ❌ {rep.get('invalid')}", file=sys.stderr)
        return 2
    # 583 任务 1（N5）：等价变异体计数 + 保守性自证（默认只打印计数；自检按开关/随确定性自检跑）
    _eq = int(rep.get("equivalent") or 0)
    print(f"[mutation] 等价变异体（规范化双解析器视角相同，**不进分母**）= {_eq}"
          f" / {rep['variants']}（其中 n_a {rep['n_a']}）")
    if a.selfcheck_equivalent or a.selfcheck_determinism:
        _okq, _badq = selfcheck_equivalent(rep)
        if not _okq:
            print(f"[mutation] ❌ 等价判据假阳性：{len(_badq)} 条标了 equivalent 却有新 finding"
                  "（判据把真逃逸洗成了等价 ⇒ 必须修判据，不许改 verdict）", file=sys.stderr)
            for _b in _badq[:10]:
                print(f"[mutation]   假阳性：{_b}", file=sys.stderr)
            return 2
        print("[mutation] ✓ 等价判据保守性自证：所有 equivalent 变体的 new_block/new_warn 均为空")
    if a.selfcheck_determinism:          # 579 任务 2：自证"同输入同输出"
        try:
            ok, diffs = selfcheck_determinism(cards, ops, a.limit, rep,
                                              progress=a.progress, jobs=jobs)
        except SelfcheckCoverageError as exc:      # 589 任务 1：选卡无效 ⇒ fail-loud（exit2）
            print(f"[mutation] ❌ 确定性自检覆盖失效：{exc}", file=sys.stderr)
            return 2
        if not ok:
            print(f"[mutation] ❌ 确定性自检不过：{len(diffs)} 个变体两次跑不一致"
                  "（尺子会抖 ⇒ 逃逸率不可复现）", file=sys.stderr)
            for d in diffs[:10]:
                print(f"[mutation]   抖动：{d}", file=sys.stderr)
            return 2
        _scn = len(_load_selfcheck_cards())
        print("[mutation] ✓ 确定性自检：全 7 算子 × 自检小卡集"
              f"（{_scn} 卡）两次跑逐变体一致（子集算子 {list(_SELFCHECK_OPS)}）")
    return 1 if (a.fail_on_escaped and rep["escaped"]) else 0

if "--check" in sys.argv:
    print("OK: mutation_fuzz --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)

if __name__ == "__main__":
    raise SystemExit(main())
