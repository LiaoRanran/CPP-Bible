#!/usr/bin/env python3
"""535 批次2 · V-iso 阴面最小 diff 机器判据（533 §2.2 正式化，原型：`_arch_v2_round2/iso_judge.py`）。

**要解决的问题**：observation 卡可以"全绿但 claim 空转"——断言在机制被删掉之后照样成立，
于是它没有判别力。V-iso 要求每条关键 observation 配一个**阴夹具**（把机制删掉的同构变体），
并断言探针读数在阴夹具上必须翻转。本模块只管**形态判据**（diff 长得对不对、删得是不是地方），
"破坏是否充分"由 replay 实编译实跑后比对读数（`atom_evidence_replay.check_negative_controls`）。

判据 v1（delete_mechanism 单一形态，全部 AND，任一不过即拒）：
  ① 单 hunk；② 新增行 == 0（纯删除——"改名/替换"这类一行攻击物理上含插入行，结构性击毙）；
  ③ 代码删除行 1..3；④ 纯注释删除行 == 0；⑤ 变动 token ≤ 40；⑥ token 改动率 ≤ 2%；
  ⑦ 删除行 100% 落在 anchor 函数体内（花括号配对）；⑧ 声明的 `remove` 文本真在被删行里；
  ⑨ `retain`（claim 主体支架）在阴面中逐字保留——**这是"连主体带机制一起删"的唯一硬拦点**
     （实测：那种攻击能编译、探针同样翻转，只有 retain 能识破）；
  ⑩ 探针符号与 anchor 同源（Itanium 修饰名 `_Z<len><name>` 嵌入校验，无需 demangler）。
  零语义 diff（只动注释/空白）直接拒——那是"凑 diff"，不是阴面。

**诚实残余（534/533 §3.1 A2）**：机器只能保证"删的是 anchor 内、且卡上声明的探针翻转"；
"这行是不是 claim 口述的那个机制"是语义判断，留给人签/红队——人审成本被压到看一个 ≤3 行的 hunk。

纯函数模块：判据不碰盘、不 import 仓库其它工具（存在性/样板文本判定由调用方注入谓词），
便于 gate 与 pytest 直接复用（同 EV-FALSIFICATION 的 gate/replay 双侧复用模式）。
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from typing import Any, Callable

# ── v1 阈值（533 §2.2「实测校准」列；改阈值 = 改判据，必须配毒样例与记录，不许静默调参）──
MAX_HUNKS = 1
MAX_INSERTED_LINES = 0
MAX_CODE_DELETED_LINES = 3
MAX_COMMENT_DELETED_LINES = 0
MAX_TOKENS_CHANGED = 40
MAX_TOKEN_CHANGE_RATIO = 0.02
REQUIRE_ANCHOR_COVERAGE = 1.0

# ── schema 常量（533 §2.1）──────────────────────────────────────────────────
NC_VARIANTS = ("v1",)                    # 见到 v2 即 bad_schema（未实现不许预写）
NC_MUTATIONS = ("delete_mechanism",)     # v1 只许纯删除
NC_ARTIFACT_OPS = ("changes", "decreases", "increases", "becomes_absent", "becomes_present")
NC_RUNKEY_OPS = ("changes", "becomes_absent")
NC_FIXTURE_SUFFIXES = (".cpp", ".cc", ".cxx")
_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,31}$")
_ANCHOR_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,63}$")

# token = 注释剥离后：字符串/字符字面量整体一个 token，标识符/数字/其余非空白各一个
_TOKEN_RE = re.compile(
    r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|\S')
_COMMENT_LINE_RE = re.compile(r"^\s*//")
_BLANK_RE = re.compile(r"^\s*$")


def norm_nl(text: str) -> str:
    """CRLF/CR → LF（Windows 夹具必须先归一，否则行级 diff 全是伪变更）。"""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def strip_comments(text: str) -> str:
    """剥注释但**保持行数**（块注释退化成同数量的空行）：花括号配对要在原行号坐标系里做。"""
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), norm_nl(text),
                  flags=re.S)
    return "\n".join(re.sub(r"//.*$", "", ln) for ln in text.split("\n"))


def tokenize_code(text: str) -> list[str]:
    """去注释后的 token 序列（注释/空白/缩进变动 ⇒ token 序列不变 ⇒ 零语义 diff）。"""
    out: list[str] = []
    for ln in strip_comments(text).split("\n"):
        out.extend(_TOKEN_RE.findall(ln))
    return out


def _changed_groups(a: list[str], b: list[str]) -> list[tuple[int, int, int, int]]:
    """非 equal 变更组 `[(a_lo,a_hi,b_lo,b_hi)...]`；间隔 ≤3 相等行则并组（=一个 hunk）。"""
    groups: list[tuple[int, int, int, int]] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
            None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        if groups and i1 <= groups[-1][1] + 3 and j1 <= groups[-1][3] + 3:
            p = groups[-1]
            groups[-1] = (p[0], i2, p[2], j2)
        else:
            groups.append((i1, i2, j1, j2))
    return groups


def _after_params(lines: list[str], start: int, col: int) -> str | None:
    """从 `anchor(` 的 `(` 起配平括号，返回**参数表之后到函数体/分号**的文本片段。

    必须继续吞后续行：本仓夹具是 Allman 风格（`int f()` 与 `{` 分两行），只看同行的
    形态会把所有真夹具判成"找不到 anchor"（实测踩过）。
    """
    depth = 0
    frag: list[str] = []
    for k in range(start, min(start + 40, len(lines))):
        seg = lines[k][col:] if k == start else lines[k]
        for idx, ch in enumerate(seg):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    tail = seg[idx + 1:]
                    frag.append(tail)
                    if "{" in tail or ";" in tail:
                        return "\n".join(frag)
                    for k2 in range(k + 1, min(k + 6, len(lines))):
                        frag.append(lines[k2])
                        if "{" in lines[k2] or ";" in lines[k2]:
                            break
                    return "\n".join(frag)
        frag.append(seg)
    return None


def _is_definition(lines: list[str], i: int, col: int) -> bool:
    """`)` 之后先遇 `{`（定义）还是先遇 `;`（声明/调用）。"""
    frag = _after_params(lines, i, col)
    if frag is None:
        return False
    bo, sc = frag.find("{"), frag.find(";")
    return bo != -1 and (sc == -1 or bo < sc)


def _brace_span(lines: list[str], head: int) -> tuple[tuple[int, int] | None, bool]:
    """从定义行起做花括号配对 → 函数体行区间 `[head, end)`；字符串内出现花括号 ⇒ 判不准。"""
    depth, started = 0, False
    for j in range(head, len(lines)):
        ln, i = lines[j], 0
        while i < len(ln):
            ch = ln[i]
            if ch in "\"'":
                q = ch
                i += 1
                while i < len(ln):
                    if ln[i] == "\\":
                        i += 2
                        continue
                    if ln[i] == q:
                        break
                    if ln[i] in "{}":
                        return None, True          # v1 fail-closed：不猜，直接拒
                    i += 1
                i += 1
                continue
            if ch == "{":
                depth += 1
                started = True
            elif ch == "}":
                depth -= 1
                if started and depth == 0:
                    return (head, j + 1), False
            i += 1
    return None, False


@dataclass
class AnchorScan:
    """阳夹具里 anchor 的定位结果：`defs` 是所有**定义**的行区间（重名/重载 ⇒ >1）。"""
    defs: list[tuple[int, int]] = field(default_factory=list)
    literal_brace: bool = False

    @property
    def count(self) -> int:
        return len(self.defs)

    @property
    def span(self) -> tuple[int, int] | None:
        return self.defs[0] if len(self.defs) == 1 else None


def find_func_defs(src: str, anchor: str) -> AnchorScan:
    """在阳夹具源码中定位 `anchor` 的**全部**函数定义（不猜第一个：重名一律交调用方拒收）。"""
    lines = strip_comments(src).split("\n")
    pat = re.compile(rf"\b{re.escape(anchor)}\s*\(")
    scan = AnchorScan()
    for i, ln in enumerate(lines):
        m = pat.search(ln)
        if not m or not _is_definition(lines, i, m.start()):
            continue
        span, lit = _brace_span(lines, i)
        scan.literal_brace = scan.literal_brace or lit
        if span:
            scan.defs.append(span)
    return scan


def itanium_embeds(anchor: str, mangled: str) -> bool:
    """Itanium 修饰名 `_Z<长度><名>...` 是否嵌入了源函数名（无需 demangler）。"""
    m = re.match(r"_Z(\d+)([A-Za-z0-9_]+)", str(mangled or ""))
    if not m:
        return False
    n, name = int(m.group(1)), m.group(2)
    return name[:n] == anchor


@dataclass
class DiffVerdict:
    ok: bool
    reasons: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)


def judge_min_diff(yang_text: str, yin_text: str, *, anchor: str, remove_text: str,
                   retain: list[str], probe_symbol: str | None = None,
                   max_code_lines: int = MAX_CODE_DELETED_LINES,
                   max_tokens: int = MAX_TOKENS_CHANGED,
                   max_token_ratio: float = MAX_TOKEN_CHANGE_RATIO) -> DiffVerdict:
    """v1 形态判据（纯函数，无 IO）。`ok=True` 只代表"形态合规"，**不代表机制被破坏**。"""
    a = norm_nl(yang_text).split("\n")
    b = norm_nl(yin_text).split("\n")
    groups = _changed_groups(a, b)
    deleted: list[tuple[int, str]] = []
    inserted: list[str] = []
    for i1, i2, j1, j2 in groups:
        deleted.extend((k, a[k]) for k in range(i1, i2))
        inserted.extend(b[k] for k in range(j1, j2))
    code_del = [(k, t) for k, t in deleted
                if not _BLANK_RE.match(t) and not _COMMENT_LINE_RE.match(t)]
    comment_del = [t for _, t in deleted if _COMMENT_LINE_RE.match(t)]

    tok_a, tok_b = tokenize_code(yang_text), tokenize_code(yin_text)
    tok_changed = sum((i2 - i1) + (j2 - j1)
                      for tag, i1, i2, j1, j2 in
                      difflib.SequenceMatcher(None, tok_a, tok_b, autojunk=False).get_opcodes()
                      if tag != "equal")
    ratio = tok_changed / max(len(tok_a), 1)

    scan = find_func_defs(yang_text, anchor)
    span = scan.span
    inside = [k for k, _ in code_del if span and span[0] <= k < span[1]]
    coverage = len(inside) / len(code_del) if code_del else 0.0
    retain_hit = {t: (t in yin_text) for t in retain}
    remove_hit = any(remove_text.strip() in t for _, t in code_del)

    metrics: dict[str, Any] = {
        "hunks": len(groups),
        "inserted_lines": len(inserted),
        "deleted_lines": len(deleted),
        "code_deleted_lines": len(code_del),
        "comment_only_deleted": len(comment_del),
        "tokens_yang": len(tok_a),
        "tokens_changed": tok_changed,
        "token_change_ratio": round(ratio, 5),
        "anchor_defs": scan.count,
        "anchor_span": span,
        "anchor_coverage": round(coverage, 3),
        "remove_hit": remove_hit,
        "retain_hit": retain_hit,
        "deleted_code": [t.strip() for _, t in code_del],
    }
    reasons: list[str] = []
    if tok_changed == 0:
        reasons.append("零语义 diff（只动注释/空白/缩进 = 凑 diff，不是阴面）")
    if len(groups) != MAX_HUNKS:
        reasons.append(f"变更组数={len(groups)}（v1 要求恰 {MAX_HUNKS}）")
    if len(inserted) != MAX_INSERTED_LINES:
        reasons.append(f"新增行={len(inserted)}（v1 纯删除形态要求 {MAX_INSERTED_LINES}："
                       f"改名/替换/夹带即拒）")
    if not (1 <= len(code_del) <= max_code_lines):
        reasons.append(f"代码删除行={len(code_del)}（要求 1..{max_code_lines}）")
    if len(comment_del) > MAX_COMMENT_DELETED_LINES:
        reasons.append("删除行含纯注释行（噪声/稀释 diff）")
    if tok_changed > max_tokens:
        reasons.append(f"变动 token={tok_changed}（≤{max_tokens}）")
    if ratio > max_token_ratio:
        reasons.append(f"token 改动率={ratio:.4f}（≤{max_token_ratio}）")
    if scan.count == 0:
        reasons.append(f"阳夹具中找不到 anchor 函数 {anchor!r}")
    elif scan.count > 1:
        reasons.append(f"anchor {anchor!r} 在阳夹具中有 {scan.count} 处定义"
                       f"（重名/重载歧义 ⇒ 拒收，不猜第一个：改用唯一名夹具）")
    elif coverage != REQUIRE_ANCHOR_COVERAGE:
        reasons.append(f"删除行 anchor 覆盖率={coverage:.0%}（要求 "
                       f"{REQUIRE_ANCHOR_COVERAGE:.0%}：必须全在机制函数体内）")
    if scan.literal_brace:
        reasons.append("anchor 函数体内字符串字面量含花括号：v1 无法可靠配对 ⇒ fail-closed 拒收")
    if not remove_hit:
        reasons.append("被删行中找不到声明的 remove 机制文本（remove_hit=false）")
    missing = [t for t, hit in retain_hit.items() if not hit]
    if missing:
        reasons.append(f"claim 主体支架被删/改：{missing}（retain 必须逐字保留）")
    if probe_symbol and not itanium_embeds(anchor, probe_symbol):
        reasons.append(f"探针符号 {probe_symbol!r} 与 anchor {anchor!r} 不同源"
                       f"（Itanium 嵌入校验不过）")
    return DiffVerdict(ok=not reasons, reasons=reasons, metrics=metrics)


# ── `negative_controls:` frontmatter schema 校验（533 §2.1）──────────────────
# 缺省 = 字段整体缺失（行为与现状逐字一致）；一旦写了，任何字段不合规即 fail-closed。
# 纯函数：文件存在性 / anchor 定义数 / 样板文本 / 已声明 run 键 都由调用方注入（不碰盘）。


@dataclass
class SchemaVerdict:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_nc_schema(nc: dict[str, Any], *, fixture_exists: Callable[[str], bool] | None = None,
                       anchor_def_count: int | None = None,
                       declared_run_keys: set[str] | None = None,
                       is_boilerplate: Callable[[str], bool] | None = None,
                       yang_fixture: str | None = None) -> SchemaVerdict:
    """校验单条 `negative_controls` 项。返回 (errors, warnings)；errors 非空 ⇒ bad_schema。"""
    errs: list[str] = []
    warns: list[str] = []
    nid = str(nc.get("id") or "")
    if not _ID_RE.match(nid):
        errs.append(f"id 不合规：{nid!r}（要求 ^[a-z0-9][a-z0-9_-]{{0,31}}$）")
    tag = nid or "<无 id>"
    if nc.get("variant") not in NC_VARIANTS:
        errs.append(f"{tag}: variant={nc.get('variant')!r} 不允许（v1 只认 {NC_VARIANTS}；"
                    f"v2 未实现不许预写）")
    if nc.get("mutation") not in NC_MUTATIONS:
        errs.append(f"{tag}: mutation={nc.get('mutation')!r} 不允许（v1 只认 {NC_MUTATIONS}）")

    fixture = str(nc.get("fixture") or "")
    if not fixture:
        errs.append(f"{tag}: 缺 fixture")
    else:
        posix = fixture.replace("\\", "/")
        if posix.startswith("/") or ":" in posix.split("/")[0]:
            errs.append(f"{tag}: fixture 必须是 posix 相对路径：{fixture!r}")
        if not posix.endswith(NC_FIXTURE_SUFFIXES):
            errs.append(f"{tag}: fixture 后缀必须是 {NC_FIXTURE_SUFFIXES}：{fixture!r}")
        if posix.startswith("build/") or "/build/" in posix:
            errs.append(f"{tag}: fixture 不许指向 build/ 内（那是生成物，不是夹具）")
        if yang_fixture and posix == yang_fixture.replace("\\", "/"):
            errs.append(f"{tag}: fixture 不许指向阳夹具自身（那是零判别力的原型）")
        if fixture_exists is not None and not fixture_exists(posix):
            errs.append(f"{tag}: fixture 不存在：{fixture!r}（negative_control_missing）")
        stem = posix.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        # 身份锚（547 B3 / 533 §2.1）：阴面 fixture 必须与本卡阳夹具同源——
        # stem 必须等于 `阳夹具主干名 + nc_id后缀`，防借别卡/别优化级产物冒充翻转证据。
        # 有 yang_fixture 时升 block（fail-closed，第一道身份门不能开着）；
        # 无上下文（纯 schema 单测，调用方没传阳夹具）时退化为命名规约告警，不误伤。
        suffix = f".{nid}" if nid.startswith("nc") else f".nc{nid}"
        if yang_fixture:
            yang_stem = yang_fixture.replace("\\", "/").rsplit("/", 1)[-1].rsplit(".", 1)[0]
            expected = f"{yang_stem}{suffix}"
            if nid and stem != expected:
                errs.append(f"{tag}: 阴面 fixture 未锚定本卡阳夹具：{posix!r} "
                            f"期望 `{expected}<后缀>`"
                            f"（身份绑定，防借别卡产物冒充翻转证据）")
        else:
            if nid and not stem.endswith(suffix):
                warns.append(f"{tag}: 命名规约建议 `阳夹具主干名{suffix}<后缀>`（当前 {posix!r}）")

    anchor = str(nc.get("anchor") or "")
    if not _ANCHOR_RE.match(anchor):
        errs.append(f"{tag}: anchor 不合规：{anchor!r}（标识符正则）")
    elif anchor_def_count is not None and anchor_def_count != 1:
        errs.append(f"{tag}: anchor {anchor!r} 在阳夹具中定义数={anchor_def_count}"
                    f"（要求恰 1：找不到或重名歧义都拒收，不猜第一个）")

    remove = str(nc.get("remove") or "")
    if not (1 <= len(remove.strip()) <= 120):
        errs.append(f"{tag}: remove 去空白后长度须 1..120（当前 {len(remove.strip())}）")

    retain = nc.get("retain")
    if not isinstance(retain, list) or not (1 <= len(retain) <= 6):
        errs.append(f"{tag}: retain 须为 1..6 项的 flow list（当前 {type(retain).__name__}）")
    else:
        for r in retain:
            if not (1 <= len(str(r).strip()) <= 80):
                errs.append(f"{tag}: retain 项去空白后长度须 1..80：{str(r)[:60]!r}")

    probe = nc.get("probe")
    if not isinstance(probe, dict):
        errs.append(f"{tag}: probe 须为单个 flow map（当前 {type(probe).__name__}）")
    else:
        ch = probe.get("channel")
        if ch == "artifact":
            sym, op = str(probe.get("symbol") or ""), probe.get("op")
            txt = str(probe.get("text") or "")
            if not sym:
                errs.append(f"{tag}: artifact 通道缺 symbol")
            elif anchor and not itanium_embeds(anchor, sym):
                errs.append(f"{tag}: probe.symbol {sym!r} 与 anchor {anchor!r} 不同源"
                            f"（Itanium 嵌入校验不过）")
            if not txt:
                errs.append(f"{tag}: artifact 通道缺 text")
            elif is_boilerplate is not None and is_boilerplate(txt):
                errs.append(f"{tag}: probe.text 命中样板文本（无判别力）")
            if op not in NC_ARTIFACT_OPS:
                errs.append(f"{tag}: artifact op={op!r} 不在 {NC_ARTIFACT_OPS}")
        elif ch == "run_key":
            key, op = str(probe.get("key") or ""), probe.get("op")
            if not key:
                errs.append(f"{tag}: run_key 通道缺 key")
            else:
                if declared_run_keys is not None and key not in declared_run_keys:
                    errs.append(f"{tag}: run_key {key!r} 未在卡 actual.run_match_keys 声明")
                if anchor and anchor not in key:
                    errs.append(f"{tag}: run_key {key!r} 未包含 anchor 子串 {anchor!r}"
                                f"（探针与机制不同源 ⇒ 该卡此通道机器上不可用）")
            if op not in NC_RUNKEY_OPS:
                errs.append(f"{tag}: run_key op={op!r} 不在 {NC_RUNKEY_OPS}")
        elif ch == "run_rc":
            errs.append(f"{tag}: run_rc 通道 v1 显式不开放（崩溃冒充无法绑定机制，留 v2）")
        else:
            errs.append(f"{tag}: probe.channel={ch!r} 未知（v1 只认 artifact/run_key）")

    note = str(nc.get("note") or "")
    if len(note) > 200:
        errs.append(f"{tag}: note 长度 {len(note)} > 200（只给人看，别塞判定语义）")
    return SchemaVerdict(errors=errs, warnings=warns)
