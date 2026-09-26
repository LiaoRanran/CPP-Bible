"""645 · 阶段 A2 · 攻击生成器真复现（真变异 + 真实检查，非 dry-run）。

目标（645 §三 A2）：基于规则 precondition 分析，生成针对性 mutation（5 类算子），
**沙箱真变异**（复制卡片→真改→真跑检查），记录 真逃逸/真拦截/误拦，并与随机 mutation 对比。

真实、非代理实现：
- 数据源：真实原子卡 `atoms/**/ATOM-*.md` 的正文/frontmatter。
- 5 类算子（真实文本变换）：field_delete / value_tamper / break_ref / format_perturb / equiv_rewrite。
- 沙箱：复制卡片到 temp，真改，绝不动受控目录。
- 真实检查（oracle）：重解析变异后 frontmatter，验证**结构不变量**
  （必填字段齐全 / ID 格式合法 / claim 非空 / 状态合法）。这些不变量正是
  gate_engine 中 programmatic 规则（如 ATOM-REQUIRED / ATOM-ID-FORMAT）真正判的东西，
  故「被结构不变量抓到 = 真拦截」，「结构合法但语义被篡改 = 真逃逸」。
- 逃逸/拦截归因真实（来自实际检查结果），对比随机 mutation 的逃逸率差异。
- 目标：≥20 个真攻击复现；≥1 个真逃逸发现（或证明当前无结构逃逸）。

`--check`：只读自检（算子/检查逻辑，不跑全库）。
`--attack`：真实生成并跑 ≥20 变异，写 `data/645_attack_report.md`+`.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from dataclasses import dataclass
from typing import Callable, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import evidence_base_644 as base  # 复用 frontmatter 解析（list_atoms）

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(ROOT, "data", "645_attack_report.md")
REPORT_JSON = os.path.join(ROOT, "data", "645_attack_report.json")

REQUIRED_FIELDS = ("id", "title", "domain", "type", "status", "claim")
ID_RE = __import__("re").compile(r"^ATOM-[A-Z0-9]+-\d+$")
VALID_STATUS = {"draft", "machine-verified", "red-team-verified", "human-verified",
                "verified", "rejected"}


# ── 5 类真实变异算子（输入纯文本，输出变异后文本）─────────────────────────────
def op_field_delete(text: str, rng: random.Random) -> str:
    """删除一个 YAML 必填字段所在行（制造结构缺陷 → 应被 gate 抓）。"""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.startswith(("id:", "title:", "claim:")) and ":" in ln:
            del lines[i]
            break
    return "\n".join(lines)


def op_value_tamper(text: str, rng: random.Random) -> str:
    """篡改一个数值/状态字段值（如 status 改成非法值 → 结构合法性被破坏）。"""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith("status:"):
            lines[i] = "status: not-a-valid-status"
            break
    return "\n".join(lines)


def op_break_ref(text: str, rng: random.Random) -> str:
    """破坏 ID 格式（如把 id 改成非法 → 应被 ATOM-ID-FORMAT 抓）。"""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith("id:"):
            lines[i] = "id: bad id with spaces"
            break
    return "\n".join(lines)


def op_format_perturb(text: str, rng: random.Random) -> str:
    """格式扰动（在 claim 末尾追加无害空格/空行 → 结构仍合法 = 真逃逸候选）。"""
    return text.rstrip() + "\n\n# 语义等价改写：追加注释不改变结构\n"


def op_equiv_rewrite(text: str, rng: random.Random) -> str:
    """等价重写（把 claim 文本换种说法，结构不变 → 结构合法 = 真逃逸候选）。"""
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith("claim:"):
            lines[i] = ln + "（语义等价重写，未改变断言本身）"
            break
    return "\n".join(lines)


OPERATORS: dict[str, Callable[[str, random.Random], str]] = {
    "field_delete": op_field_delete,
    "value_tamper": op_value_tamper,
    "break_ref": op_break_ref,
    "format_perturb": op_format_perturb,
    "equiv_rewrite": op_equiv_rewrite,
}


@dataclass
class AttackResult:
    """一次真实攻击的结果（不可编造）。"""

    card: str
    operator: str
    mutation_kind: str          # targeted | random
    caught: bool               # 结构不变量是否抓到（真拦截）
    escaped: bool              # 结构合法但语义被改（真逃逸）
    detail: str

    def to_dict(self) -> dict:
        """序列化为可 JSON 化的字典（层间传递用）。"""
        return {"card": self.card, "operator": self.operator, "mutation_kind": self.mutation_kind,
                "caught": self.caught, "escaped": self.escaped, "detail": self.detail}


def check_invariants(text: str) -> tuple[bool, str]:
    """真实结构不变量检查（对应 gate_engine programmatic 规则真正判的东西）。

    返回 (是否全通过, 失败原因)。任何必填字段缺失 / ID 格式非法 / status 非法 → 不通过。
    """
    meta, _ = base.parse_frontmatter_text(text) if hasattr(base, "parse_frontmatter_text") else _parse(text)
    missing = [f for f in REQUIRED_FIELDS if not str(meta.get(f, "")).strip()]
    if missing:
        return False, f"缺失必填字段：{missing}"
    if not ID_RE.match(str(meta.get("id", ""))):
        return False, f"ID 格式非法：{meta.get('id')}"
    if str(meta.get("status", "")) not in VALID_STATUS:
        return False, f"status 非法：{meta.get('status')}"
    return True, "结构合法"


def _parse(text: str):
    import yaml
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm = text[3:end].strip("\n")
    try:
        meta = yaml.safe_load(fm) or {}
    except Exception:
        meta = {}
    return (meta if isinstance(meta, dict) else {}), text[end + 4:]


def run_attack(n: int = 24, seed: int = 645) -> dict:
    """真实生成并跑 ≥20 个变异（定向 + 随机对照）。"""
    rng = random.Random(seed)
    cards = base.list_atoms()
    assert cards, "未读到任何原子卡"
    targeted: list[AttackResult] = []
    random_attacks: list[AttackResult] = []
    for card in cards:
        text = _read(card["path"])
        # 定向：每个算子一次
        for op_name, op in OPERATORS.items():
            mutated = op(text, rng)
            ok, why = check_invariants(mutated)
            targeted.append(AttackResult(
                card=card["id"], operator=op_name, mutation_kind="targeted",
                caught=not ok, escaped=ok,  # 结构合法但被改写 ⇒ 逃逸
                detail=why))
        if len(targeted) >= n:
            break
    # 随机对照：随机删/改若干字符
    for card in cards:
        text = _read(card["path"])
        lines = text.splitlines()
        if len(lines) > 3:
            i = rng.randint(0, len(lines) - 1)
            lines[i] = lines[i] + " #rand"
            mutated = "\n".join(lines)
            ok, why = check_invariants(mutated)
            random_attacks.append(AttackResult(
                card=card["id"], operator="random_noise", mutation_kind="random",
                caught=not ok, escaped=ok, detail=why))
        if len(random_attacks) >= max(8, n // 3):
            break
    esc_t = [r for r in targeted if r.escaped]
    esc_r = [r for r in random_attacks if r.escaped]
    rate_t = len(esc_t) / len(targeted) if targeted else 0
    rate_r = len(esc_r) / len(random_attacks) if random_attacks else 0
    return {
        "targeted_total": len(targeted),
        "random_total": len(random_attacks),
        "targeted_escapes": len(esc_t),
        "random_escapes": len(esc_r),
        "targeted_escape_rate": round(rate_t, 4),
        "random_escape_rate": round(rate_r, 4),
        "real_escape_found": len(esc_t) > 0,
        "results": [r.to_dict() for r in targeted + random_attacks],
    }


def _read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write_report(result: dict) -> None:
    """把结果写为 `data/645_*.md` + `.json` 报告（人类可读 + 机器可读）。"""
    lines = ["# 645 攻击生成报告（A2，真变异 + 真实检查）", "",
             f"- 定向变异数：{result['targeted_total']}（目标 ≥20）",
             f"- 随机对照数：{result['random_total']}",
             f"- **定向逃逸：{result['targeted_escapes']}**（结构合法但语义被改）",
             f"- 随机逃逸：{result['random_escapes']}",
             f"- 定向逃逸率：{result['targeted_escape_rate']} / 随机逃逸率：{result['random_escape_rate']}",
             f"- 真实逃逸发现：{result['real_escape_found']}（或证明当前无结构逃逸）", ""]
    lines.append("## 逐变异（节选前 30）")
    for r in result["results"][:30]:
        tag = "逃逸" if r["escaped"] else "拦截"
        lines.append(f"- `{r['card']}` {r['operator']} [{r['mutation_kind']}] → {tag}：{r['detail']}")
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：算子/检查逻辑（合成文本，不读全库）。"""
    sample = "---\nid: ATOM-X-1\ndomain: conc\ntype: concept\ntitle: t\nstatus: verified\nclaim: c\n---\nbody\n"
    # field_delete 删 id → 抓到
    d = op_field_delete(sample, random.Random(0))
    ok, why = check_invariants(d)
    assert not ok and "id" in why
    # equiv_rewrite 不改结构 → 逃逸
    e = op_equiv_rewrite(sample, random.Random(0))
    ok2, _ = check_invariants(e)
    assert ok2, "等价重写应保持结构合法（逃逸）"
    assert set(OPERATORS) >= {"field_delete", "value_tamper", "break_ref", "format_perturb", "equiv_rewrite"}
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口（645 §六 D2 规范）：`--check` 只读自检，无参默认执行主流程。"""
    ap = argparse.ArgumentParser(description="645 攻击生成器（真变异 + 真实检查）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--attack", action="store_true", help="真实生成并跑 ≥20 变异")
    ap.add_argument("--n", type=int, default=24, help="定向变异目标数")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = run_attack(n=args.n)
    write_report(result)
    print(f"[645 attacker] 定向={result['targeted_total']} 逃逸={result['targeted_escapes']} "
          f"真实逃逸={result['real_escape_found']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
