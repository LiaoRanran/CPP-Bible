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
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import atom_evidence_replay as replay   # noqa: E402
import gate_engine as ge                # noqa: E402

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
    for name in ("atoms", "evidence"):
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, tmp / name)
    orig_a, orig_e = ge.ATOMS, ge.EVIDENCE
    ge.ATOMS, ge.EVIDENCE = tmp / "atoms", tmp / "evidence"
    try:
        yield tmp
    finally:
        ge.ATOMS, ge.EVIDENCE = orig_a, orig_e
        shutil.rmtree(tmp, ignore_errors=True)


def _rel_in_sandbox(card: Path, tmp: Path) -> Path:
    return tmp / card.relative_to(ROOT)


def _findings_key(f: ge.Finding) -> tuple[str, str, str]:
    return (f.rule_id, f.severity, f.target)


def _snapshot() -> set[tuple[str, str, str]]:
    return {_findings_key(f) for f in ge.run(include_advice=False)}


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


def mut_m2(text: str) -> list[tuple[str, str]]:
    """M2 路径变形：对卡内**第一个带 `/` 的文件路径**做三种写法变形（同一物理文件的不同写法）。"""
    for m in re.finditer(
            r"[A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:cpp|cc|cxx|py|asm|out|md|json)", text):
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
    return []


def mut_m3(text: str) -> list[tuple[str, str]]:
    """M3 断言弱化：区间断言降级成全文存在性；去掉 -Werror；量化读数降成纯存在性。"""
    out: list[tuple[str, str]] = []
    if "contains_in" in text:
        out.append(("contains_in → contains（区间断言降级为全文存在性）",
                    text.replace("contains_in", "contains", 1)))
    if "absent_in" in text:
        out.append(("absent_in → absent（区间断言降级为全文不存在）",
                    text.replace("absent_in", "absent", 1)))
    if "-Werror" in text:
        out.append(("-Werror 被删（编译告警不再算失败）", text.replace("-Werror", "", 1)))
    m = re.search(r"(?m)^\s*(?:- )?\{?kind:\s*\w+.*?(?:count|min|max|\d+).*$", text)
    if m and "count:" in m.group(0):
        out.append(("量化断言降级（count: N → 纯存在性）",
                    text.replace(m.group(0), re.sub(r"count:\s*\d+", "", m.group(0)), 1)))
    return out


def mut_m4(text: str) -> list[tuple[str, str]]:
    """M4 恒真注入：往 artifact_assert 里塞通用符号 / ABI 帧符号 / `.file` 类恒真断言。"""
    m = re.search(r"(?m)^(\s*)artifact_assert:\s*$", text)
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
        out.append((tag, text[:m.end()] + "\n" + line + text[m.end():]))
    return out


def mut_m5(text: str) -> list[tuple[str, str]]:
    """M5 claim 自标：把推断/机制类 claim 改成 observation（测活性/工件断言闸是否拦）。"""
    out: list[tuple[str, str]] = []
    m = re.search(r"(?m)^(\s*)claim_type:\s*(\w+)\s*$", text)
    if m and m.group(2) != "observation":
        out.append((f"claim_type: {m.group(2)} → observation（自标绕过）",
                    text[:m.start(2)] + "observation" + text[m.end(2):]))
    return out


def mut_m6(text: str) -> list[tuple[str, str]]:
    """M6 YAML 变形：重复键 / 缩进提升 / 全角键名 / flow 写法（E07 缩进走私族复刻）。"""
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
    try:
        new = _snapshot() - baseline
    except Exception as exc:                       # noqa: BLE001  门禁自身崩了 = 不适用
        return {"verdict": "n_a", "why": f"gate 执行失败：{type(exc).__name__}: {exc}"}
    finally:
        pass
    new_block = sorted({f"{r}:{t}" for r, s, t in new if s == "block"})
    new_warn = sorted({f"{r}:{t}" for r, s, t in new if s == "warn"})
    detail: dict[str, Any] = {"new_block": new_block, "new_warn": new_warn}
    if op in REPLAY_OPS:
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


def run_fuzz(cards: list[Path], ops: list[str], limit: int) -> dict[str, Any]:
    """主循环（drill 范式）：逐卡逐算子逐变体判决；返回报告 dict。"""
    selected = cards[:limit]
    per: list[dict[str, Any]] = []
    with sandbox() as tmp:
        baseline = _snapshot()
        for card in selected:
            text = card.read_text(encoding="utf-8")
            sb_card = _rel_in_sandbox(card, tmp)
            for op in ops:
                variants = MUTATORS[op](text)
                if not variants:
                    per.append({"card": card.relative_to(ROOT).as_posix(), "op": op,
                                "point": "-", "verdict": "n_a",
                                "why": "该卡本就没有被变异的字段（不适用）"})
                    continue
                for point, vtext in variants:
                    if vtext == text:
                        per.append({"card": card.relative_to(ROOT).as_posix(), "op": op,
                                    "point": point, "verdict": "n_a", "why": "变异为空操作"})
                        continue
                    r = classify(card.stem, op, baseline, vtext, sb_card, tmp)
                    sb_card.write_text(text, encoding="utf-8")     # 还原沙箱副本再进下一个变体
                    per.append({"card": card.relative_to(ROOT).as_posix(), "op": op,
                                "point": point,
                                "reproduce": (f".venv\\Scripts\\python.exe tools/mutation_fuzz.py "
                                              f"--cards {card.relative_to(ROOT).as_posix()} "
                                              f"--operators {op} --limit 1"),
                                **r})
    counts = {k: sum(1 for r in per if r["verdict"] == k)
              for k in ("blocked", "escaped", "n_a")}
    counts["malformed"] = sum(1 for r in per if r.get("malformed"))    # n_a 里单列一类（543 P1）
    strict = sum(1 for r in per if r["verdict"] == "blocked" and r.get("kind") == "strict")
    treated = counts["blocked"]
    denom = counts["blocked"] + counts["escaped"] or 1
    return {"cards": [c.relative_to(ROOT).as_posix() for c in selected],
            "operators": ops, "variants": len(per), **counts,
            "strict_blocked": strict,
            "strict_rate": round(strict / denom, 4),
            "treated_rate": round(treated / denom, 4),
            "escaped_list": [r for r in per if r["verdict"] == "escaped"],
            "results": per}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="539 · 自动变异器（L3 第一块）：找毒样例没覆盖的新逃逸")
    ap.add_argument("--cards", default="all", help="all | 相对 ROOT 的 glob（默认 all）")
    ap.add_argument("--operators", default=",".join(OPS), help=f"逗号分隔，可选 {','.join(OPS)}")
    ap.add_argument("--limit", type=int, default=5, help="最多处理多少张卡（默认 5，小批先跑通）")
    ap.add_argument("--report", default="data/mutation/last.json", help="JSON 报告落盘路径")
    ap.add_argument("--fail-on-escaped", action="store_true",
                    help="有 escaped 即 exit 1（默认恒 0：escaped 是本工具的**产物**，不是红灯）")
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
    rep = run_fuzz(cards, ops, a.limit)
    out = ROOT / a.report
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[mutation] 卡 {len(rep['cards'])} 张 · 算子 {len(ops)} 类 · 变体 {rep['variants']} 个")
    print(f"[mutation] blocked={rep['blocked']}（严格 {rep['strict_blocked']}） "
          f"escaped={rep['escaped']} n_a={rep['n_a']}（其中 malformed={rep['malformed']}）")
    print(f"[mutation] 严格拦截率 {rep['strict_rate']:.1%} · 含 warn 处置率 {rep['treated_rate']:.1%}")
    for r in rep["escaped_list"]:
        print(f"[mutation] ✗ ESCAPED {r['card']} · {r['op']} · {r['point']}")
    print(f"[mutation] 报告：{out.relative_to(ROOT).as_posix()}")
    return 1 if (a.fail_on_escaped and rep["escaped"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
