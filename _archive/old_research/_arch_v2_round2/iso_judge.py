#!/usr/bin/env python3
"""533 V-iso 阴面最小 diff 机器判据原型（沙箱版，不动正式工具）。

判据 v1（delete_mechanism 单形态）：
  H1 单 hunk；A==0（只许纯删除，不许改名/替换/夹带新增）；
  1 ≤ 代码删除行数 D_code ≤ 3；删除 token 数 ≤ 40；
  所有删除行 100% 落在 anchor 函数体（花括号配对）内；
  writer 声明的 remove 文本必须真在被删行里；retain 文本（claim 主体支架）
  必须在阴面中逐字保留（防"连同循环一起删"冒充"只删机制"）；
  token 级改动率 ≤ 2%；纯注释/空白改动 = 零语义 diff，拒；
  anchor 与探针符号须同源（Itanium 修饰名嵌入校验，不需 demangler）。
"破坏充分性"不在本模块判——由 run_probe 实测翻转，writer 自说不算。
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field

_TOKEN_RE = re.compile(
    r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[A-Za-z_][A-Za-z0-9_]*|\d+(?:\.\d+)?|\S')
_COMMENT_LINE_RE = re.compile(r"^\s*//")
_BLANK_RE = re.compile(r"^\s*$")


def norm_nl(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def tokenize_code(text: str) -> list[str]:
    """去注释后的 token 序列（字符串字面量整体一个 token）。"""
    text = norm_nl(text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    out: list[str] = []
    for ln in text.split("\n"):
        ln = re.sub(r"//.*$", "", ln)
        out.extend(_TOKEN_RE.findall(ln))
    return out


def _changed_groups(a: list[str], b: list[str]) -> list[tuple[int, int, int, int]]:
    """返回非 equal 变更组 [(a_lo,a_hi,b_lo,b_hi)...]，相邻变更自动并组。"""
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


def find_func_span(src: str, anchor: str) -> tuple[int, int] | None:
    """定位 `anchor(...) ... { ... }` 函数定义体在源码中的行区间 [起, 止)。

    朴素但够用：找列 0 起、名字后紧跟 `(` 的定义行，从第一个 `{` 起花括号配对。
    """
    lines = norm_nl(src).split("\n")
    head = None
    pat = re.compile(rf"\b{re.escape(anchor)}\s*\(")
    for i, ln in enumerate(lines):
        m = pat.search(ln)
        if not m:
            continue
        # 定义 vs 调用：从 ( 起配平括号，) 之后先遇 '{' 即定义、先遇 ';' 即调用/声明。
        tail = ln[m.start():]
        depth = 0
        for k in range(i, min(i + 12, len(lines))):
            seg = (tail if k == i else lines[k])
            for ch in seg:
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        break
            if depth == 0:
                after = seg[seg.index(")") + 1:] if k == i else \
                    lines[k].split(")", 1)[-1]
                rest = (after + "\n" + "\n".join(lines[k + 1:k + 6]))
                bo, sc = rest.find("{"), rest.find(";")
                if bo != -1 and (sc == -1 or bo < sc):
                    head = i
                break
        if head is not None:
            break
    if head is None:
        return None
    depth = 0
    started = False
    for j in range(head, len(lines)):
        for ch in lines[j]:
            if ch == "{":
                depth += 1
                started = True
            elif ch == "}":
                depth -= 1
                if started and depth == 0:
                    return (head, j + 1)
    return None


def itanium_embeds(anchor: str, mangled: str) -> bool:
    """Itanium 修饰名 `_Z<长度><名>...` 是否嵌入源函数名（无需 demangler）。"""
    m = re.match(r"_Z(\d+)([A-Za-z0-9_]+)", mangled)
    if not m:
        return False
    n, name = int(m.group(1)), m.group(2)
    return name[:n] == anchor


@dataclass
class DiffVerdict:
    ok: bool
    reasons: list[str] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)


def judge_min_diff(yang_text: str, yin_text: str, *,
                   anchor: str, remove_text: str,
                   retain: list[str], probe_symbol: str | None = None,
                   max_code_lines: int = 3, max_tokens: int = 40,
                   max_token_ratio: float = 0.02) -> DiffVerdict:
    a = norm_nl(yang_text).split("\n")
    b = norm_nl(yin_text).split("\n")
    groups = _changed_groups(a, b)
    deleted: list[tuple[int, str]] = []   # (yang 行号 0-based, 文本)
    inserted: list[str] = []
    for i1, i2, j1, j2 in groups:
        deleted.extend((k, a[k]) for k in range(i1, i2))
        inserted.extend(b[k] for k in range(j1, j2))
    code_del = [(k, t) for k, t in deleted
                if not _BLANK_RE.match(t) and not _COMMENT_LINE_RE.match(t)]
    comment_del = [t for t in (_t for _, _t in deleted)
                   if _COMMENT_LINE_RE.match(t)]
    tok_a = tokenize_code(yang_text)
    tok_b = tokenize_code(yin_text)
    tok_del = len(tok_a) - max(0, len(tok_a) - abs(len(tok_a) - len(tok_b)))
    # 用 SM 在 token 层统计变动量
    sm = difflib.SequenceMatcher(None, tok_a, tok_b, autojunk=False)
    tok_changed = sum((i2 - i1) + (j2 - j1)
                      for tag, i1, i2, j1, j2 in sm.get_opcodes()
                      if tag != "equal")
    ratio = tok_changed / max(len(tok_a), 1)

    span = find_func_span(yang_text, anchor)
    inside = [k for k, _ in code_del if span and span[0] <= k < span[1]]
    coverage = len(inside) / len(code_del) if code_del else 0.0
    retain_hit = {t: (t in yin_text) for t in retain}
    remove_hit = any(remove_text.strip() in t for _, t in code_del)

    m = {
        "hunks": len(groups),
        "inserted_lines": len(inserted),
        "deleted_lines": len(deleted),
        "code_deleted_lines": len(code_del),
        "comment_only_deleted": len(comment_del),
        "tokens_yang": len(tok_a),
        "tokens_changed": tok_changed,
        "token_change_ratio": round(ratio, 5),
        "anchor_span": span,
        "anchor_coverage": round(coverage, 3),
        "remove_hit": remove_hit,
        "retain_hit": retain_hit,
        "deleted_code": [t.strip() for _, t in code_del],
    }
    reasons: list[str] = []
    if tok_changed == 0:
        reasons.append("零语义 diff（仅注释/空白）")
    if len(groups) != 1:
        reasons.append(f"变更组数={len(groups)}（要求 1）")
    if len(inserted) != 0:
        reasons.append(f"新增行={len(inserted)}（v1 纯删除形态要求 0，改名/替换即拒）")
    if not (1 <= len(code_del) <= max_code_lines):
        reasons.append(f"代码删除行={len(code_del)}（要求 1..{max_code_lines}）")
    if comment_del:
        reasons.append("删除行含纯注释行（噪声/凑 diff 稀释）")
    if tok_changed > max_tokens:
        reasons.append(f"变动 token={tok_changed}（≤{max_tokens}）")
    if ratio > max_token_ratio:
        reasons.append(f"token 改动率={ratio:.4f}（≤{max_token_ratio}）")
    if span is None:
        reasons.append(f"yang 中找不到 anchor 函数 {anchor!r}")
    elif coverage != 1.0:
        reasons.append(f"删除行 anchor 覆盖率={coverage:.0%}（要求 100%）")
    if not remove_hit:
        reasons.append("被删行中找不到声明的 remove 机制文本")
    missing_retain = [t for t, ok in retain_hit.items() if not ok]
    if missing_retain:
        reasons.append(f"claim 主体支架被删/改：{missing_retain}（retain 必须逐字保留）")
    if probe_symbol and not itanium_embeds(anchor, probe_symbol):
        reasons.append(f"探针符号 {probe_symbol!r} 与 anchor {anchor!r} 不同源")
    return DiffVerdict(ok=not reasons, reasons=reasons, metrics=m)
