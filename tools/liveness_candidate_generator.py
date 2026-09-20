"""612 B1 · 活性锚自动候选生成工具（**只读** · 不填卡、不改任何命题文件）。

读取 79 命题中 **50 条缺 `liveness` 的 observation**（同 `proposition_liveness_audit` 判据），
对每条抽取其证据卡（`evidence` 字段）工件里的符号（函数名/宏/静态变量），按三维度评估质量并给候选：

  * **唯一性**：该符号是否只出现在本命题引用的工件（1 张卡=high；多张=medium；通用符号=low）
  * **可观测性**：该卡是否用断言/输出观测到该符号（有=high；否则 medium）
  * **命题相关性**：命题 `statement` 是否直接提到该符号（提到=high；否则 medium/low）

每条命题最多 3 个候选（按质量排序）。分类：
  * **A**（高置信，可自动补）：存在 confidence=high 的候选
  * **B**（中置信，需人审选）：最高候选为 medium
  * **C**（无法用单一工件符号证伪）：无候选 / 只有通用符号 ⇒ **建议改标 inference**（不实际改）

⚠️ 只读：不写卡、不改命题；符号扫描用正则，不调 LLM（可复算）。
CLI：`--write`（写 jsonl + md）/ `--stats` / `--check`（exit 0=通过）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

VERSION = "1.0"
JSONL_OUT = ROOT / "data" / "liveness_candidates_612.jsonl"
MD_OUT = ROOT / "data" / "liveness_candidates_612.md"

GENERIC = {"main", "printf", "scanf", "malloc", "free", "cout", "cin", "endl", "std",
           "int", "void", "char", "bool", "float", "double", "auto", "const", "static",
           "return", "if", "else", "for", "while", "sizeof", "new", "delete", "class",
           "struct", "public", "private", "template", "namespace", "using", "include",
           "nullptr", "true", "false", "unsigned", "signed", "long", "short", "size_t",
           "switch", "case", "break", "continue", "typedef", "enum", "union", "virtual",
           "override", "operator", "this", "inline", "extern", "goto", "do", "default",
           "try", "catch", "throw", "null", "NULL", "asm", "volatile", "register", "and",
           "or", "not", "xor", "bitand", "bitor", "compl", "wchar_t", "uint8_t",
           "uint16_t", "uint32_t", "uint64_t", "int8_t", "int16_t", "int32_t", "int64_t"}
_FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
_TICK = re.compile(r"`([A-Za-z_][A-Za-z0-9_:]*)`")
_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
NOISE = {"None", "True", "False", "print", "self", "def", "import", "range", "argv"}
_OBS = re.compile(r"(?:assert|static_assert|cout|printf|cerr|std::cout|std::cerr)")


def load_missing_props() -> list[dict]:
    import proposition_liveness_audit as pla  # noqa: E402
    res = pla.audit()
    out: list[dict] = []
    for c in res["cards"]:
        for e in c["missing"]:
            # 命题 id 在卡内唯一、跨卡重名 ⇒ 用卡级复合键（与 weighted_af_solver 的 `卡::prop-N` 同源）
            out.append({"proposition_id": f"{c['card']}::{e['id']}", "card": c["card"],
                        "statement": e.get("statement") or "",
                        "evidence": [x for x in (e.get("evidence") or []) if isinstance(x, str)]})
    return out


def load_corpus() -> dict[str, str]:
    texts: dict[str, str] = {}
    for base in (ROOT / "atoms", ROOT / "evidence"):
        for p in sorted(base.rglob("*.md")):
            texts[p.stem] = p.read_text(encoding="utf-8", errors="replace")
    return texts


def symbols_in(text: str) -> list[str]:
    """从卡文本抽取候选符号：代码围栏内的标识符 + 行内反引号包裹的标识符。

    本仓证据卡把工件（.asm/.cpp 片段）以代码围栏/行内反引号内嵌在 Markdown 里
    （`atoms/ evidence/` 下**没有**独立代码文件），故符号从卡文本自身抽取。
    """
    syms: set[str] = set()
    for block in _FENCE.findall(text):
        syms |= set(_WORD.findall(block))
    syms |= set(_TICK.findall(text))
    # 只留「像符号」的标识符：含下划线或大写字母（滤掉纯小写英文词/保留字噪声）
    return sorted(s for s in syms
                  if len(s) > 2 and s not in GENERIC and s not in NOISE
                  and ("_" in s or any(c.isupper() for c in s)))


def symbol_index(corpus: dict[str, str]) -> dict[str, set[str]]:
    idx: dict[str, set[str]] = {}
    for cid, text in corpus.items():
        for s in symbols_in(text):
            idx.setdefault(s, set()).add(cid)
    return idx


def _w(level: str) -> int:
    return {"high": 2, "medium": 1, "low": 0}[level]


def candidates_for(prop: dict, corpus: dict[str, str],
                   index: dict[str, set[str]]) -> list[dict]:
    ev = [e for e in prop["evidence"] if e in corpus]
    cands: list[dict] = []
    stmt = prop["statement"]
    for ev_card in ev:
        text = corpus[ev_card]
        for sym in symbols_in(text):
            n_cards = len(index.get(sym, set()))
            uniq = "high" if n_cards <= 1 else ("medium" if n_cards <= 3 else "low")
            # 可观测性：该卡是否用断言/输出**观测到**该符号（同行同现=high；卡有断言=medium；无=low）
            co_obs = any(sym in ln and _OBS.search(ln) for ln in text.splitlines())
            obs = "high" if co_obs else ("medium" if _OBS.search(text) else "low")
            rel = "high" if sym.lower() in stmt.lower() else "medium"
            score = _w(uniq) + _w(obs) + _w(rel)
            conf = "high" if score >= 5 else ("medium" if score >= 3 else "low")
            cands.append({"proposition_id": prop["proposition_id"], "kind": "fixture_symbol",
                          "symbol": sym, "confidence": conf, "source_file": ev_card,
                          "card": prop["card"], "scores": {"uniqueness": uniq,
                                                           "observability": obs, "relevance": rel}})
    cands.sort(key=lambda c: (-_w(c["confidence"]), c["symbol"]))
    # 去重取前 3
    seen: set[str] = set()
    top: list[dict] = []
    for c in cands:
        if c["symbol"] in seen:
            continue
        seen.add(c["symbol"])
        top.append(c)
        if len(top) >= 3:
            break
    return top


def classify_prop(cands: list[dict]) -> str:
    if not cands:
        return "C"
    best = max(_w(c["confidence"]) for c in cands)
    return "A" if best >= 2 else ("B" if best == 1 else "C")


def build() -> dict:
    props = load_missing_props()
    corpus = load_corpus()
    index = symbol_index(corpus)
    rows: list[dict] = []
    per_prop: list[dict] = []
    for p in props:
        cands = candidates_for(p, corpus, index)
        cls = classify_prop(cands)
        for c in cands:
            rows.append({**c, "class": cls})
        per_prop.append({"proposition_id": p["proposition_id"], "card": p["card"],
                         "statement": p["statement"], "class": cls,
                         "candidates": [{"symbol": c["symbol"], "confidence": c["confidence"],
                                         "source_file": c["source_file"]} for c in cands]})
    counts = Counter(x["class"] for x in per_prop)
    return {"version": VERSION, "total_props": len(props),
            "counts": {"A": counts.get("A", 0), "B": counts.get("B", 0), "C": counts.get("C", 0)},
            "rows": rows, "per_prop": per_prop}


def render(d: dict) -> str:
    L = ["# 612 B1 · 活性锚自动候选（只读 · 建议，不填卡）", "",
         "> 扫描 50 条缺 liveness 的 observation 命题的证据卡工件符号；三维度评估（唯一性/可观测性/相关性）。",
         "> 候选只是**建议**（A 类可自动补 / B 类需人审选 / C 类建议改标 inference），本工具不填卡。", "",
         "## 一、总览", "",
         f"- 缺锚命题 **{d['total_props']}** 条；分类：A（高置信）**{d['counts']['A']}** · "
         f"B（中置信）**{d['counts']['B']}** · C（建议改标 inference）**{d['counts']['C']}**",
         f"- 候选总数 {len(d['rows'])}（每条命题 ≤3）", "",
         "## 二、逐条清单（节选 Top 30）", "",
         "| 命题 | 卡 | 类 | 候选（符号/置信度） |",
         "|---|---|---|---|"]
    for p in d["per_prop"][:30]:
        cs = ", ".join(f"`{c['symbol']}`({c['confidence']})" for c in p["candidates"]) or "—（无）"
        L.append(f"| `{p['proposition_id']}` | `{p['card']}` | {p['class']} | {cs} |")
    if len(d["per_prop"]) > 30:
        L.append(f"| … | | | 其余 {len(d['per_prop']) - 30} 条见 JSON |")
    L += ["", "## 三、口径与边界", "",
          "- **只读**：不填 `liveness`、不改命题文件；符号扫描用正则（不调 LLM，可复算）；",
          "- **通用符号**（main/printf/malloc…）一律标 low，不作高置信候选；",
          "- **C 类**：无单一工件符号可证伪 ⇒ 建议人审改标 inference（本工具不实际改）；",
          "- A/B/C 为自动建议，最终由人审确认（见 B2）。", ""]
    return "\n".join(L)


def check(d: dict) -> list[str]:
    problems: list[str] = []
    if d["total_props"] != 50:
        problems.append(f"缺锚命题应为 50（实测 {d['total_props']}）")
    ids = [p["proposition_id"] for p in d["per_prop"]]
    if len(set(ids)) != len(ids):
        problems.append(f"proposition_id 不唯一（{len(ids)} 条中仅 {len(set(ids))} 个）")
    if any(d["counts"][k] == 0 for k in ("A", "B", "C")):
        problems.append(f"A/B/C 分类退化（应三类都有）：{d['counts']}")
    # 通用符号不得为 high
    for r in d["rows"]:
        if r["symbol"] in GENERIC and r["confidence"] == "high":
            problems.append(f"通用符号被标 high：{r['symbol']}")
            break
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="liveness_candidate_generator", description="612 B1 活性锚候选（只读）")
    ap.add_argument("--version", action="version", version=f"liveness_candidate_generator {VERSION}")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--stats", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    d = build()
    if a.stats:
        print(json.dumps({"counts": d["counts"], "total_props": d["total_props"],
                          "rows": len(d["rows"]), "per_prop": d["per_prop"]},
                         ensure_ascii=False, indent=1))
        return 0
    if a.check:
        problems = check(d)
        if problems:
            for p in problems:
                print(f"[B1] ❌ {p}", file=sys.stderr)
            return 2
        print(f"[B1] ✓ 候选锁定（{d['total_props']} 条；A {d['counts']['A']} / "
              f"B {d['counts']['B']} / C {d['counts']['C']}）")
        return 0
    if a.write:
        JSONL_OUT.parent.mkdir(parents=True, exist_ok=True)
        JSONL_OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in d["rows"]) + "\n",
                             encoding="utf-8", newline="\n")
        MD_OUT.write_text(render(d), encoding="utf-8", newline="\n")
        print(f"[B1] 已写 {JSONL_OUT.relative_to(ROOT).as_posix()}（{len(d['rows'])} 候选）"
              f" + {MD_OUT.relative_to(ROOT).as_posix()}")
        return 0
    print(f"缺锚 {d['total_props']} · A {d['counts']['A']} / B {d['counts']['B']} / C {d['counts']['C']} · "
          f"候选 {len(d['rows'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
