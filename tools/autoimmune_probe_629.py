"""629 A2 · 误报注入探针（Negative Control，纯标准库，只读）

**目的**：A1 只能度量「已验证卡被 warn 多少」（含大量口径错配）。A2 要回答更难的问题：
gate 规则是否**对格式微调过敏**（真·自身免疫）？

**方法**：
1. 取 5 张干净卡（A1 主口径，按 id 排序取前 5）。
2. 把 `atoms/` + `evidence/` 整树**镜像到系统临时目录**，把 `gate_engine.ATOMS/EVIDENCE`
   重定向到镜像（跑批机制，测试/跑批既有手法），**真实仓库零写入**。
3. 对每张卡生成若干「微扰动副本」：只改**格式**（行尾空白 / 引号风格 / 顶层键间插空行或注释 /
   flow 映射改块映射），**不动语义**。
   **语义等价的证明**：每次扰动后都用 `atom_evidence_replay.parse_frontmatter`
   重新解析，**解析结果必须与原文逐键相等**，否则该扰动判为 `non_neutral` 并**丢弃**
   （不计入自身免疫）—— 这是本工具可信度的关键，避免「把语义改动误报成格式过敏」。
4. 对每个扰动副本跑一次 `ge.run()`，比较**该卡**的 warn 规则集合：
   - 新增 warn 规则 ⇒ **假阳性（自身免疫）证据**
   - 无变化 ⇒ 该规则不是格式驱动（内容/口径驱动）

**混淆矩阵口径（诚实标注来源）**：
- 真阴性：镜像机制本身不引入偏差（原样卡在镜像中的 warn 集合 == 真实仓库中的 warn 集合）
- 假阳性：本工具实测（语义不变的副本被新增 warn）
- 真阳性：引用 §一 poison `124/124`（**不重跑** poison_drill，§零.1 禁跑监工门禁）
- 假阴性：引用 §一 mutation 契约逃逸 `1/1406`
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "autoimmune_probe_results.md")
SAMPLE_N = 5
POISON_BASELINE = "124/124（诚实覆盖率 95.5%）"
ESCAPE_BASELINE = "1/1406（CS anytime 上界 0.9062%）"

PERTURBATIONS = ("trailing_ws", "quote_style", "blank_line", "comment", "flow_to_block")


# ── 文本工具 ─────────────────────────────────────────────────────

def split_frontmatter(text: str) -> Optional[tuple[str, str, str, str]]:
    """切成 (前导, frontmatter 体, 围栏, 其余)；无 frontmatter 返回 None。"""
    m = re.match(r"^(---\n)(.*?)(\n---\n?)(.*)$", text, re.DOTALL)
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3), m.group(4)


def _perturb_trailing_ws(body: str) -> Optional[str]:
    if all(ln.endswith(" ") for ln in body.split("\n") if ln):
        return None
    return "\n".join(ln + " " if ln and not ln.endswith(" ") else ln
                     for ln in body.split("\n"))


_PLAIN_OK = re.compile(r"^[^:#{}\[\]&*!|>'\"%@,\n]+$")


def _perturb_quote_style(body: str) -> Optional[str]:
    """把「可以安全写成 plain scalar」的双引号标量去引号（YAML 语义等价）。

    只对不含 YAML 特殊字符、无首尾空白、不含 `: ` 的内层做，其余保持原样 ——
    是否真的等价仍由 `fm_equal`（`parse_frontmatter` 逐键比对）复核，不等价即丢弃。
    """
    changed = False

    def _sub(m: re.Match[str]) -> str:
        nonlocal changed
        inner = str(m.group(1))
        if not _PLAIN_OK.match(inner) or inner != inner.strip() or ": " in inner:
            return str(m.group(0))
        changed = True
        return inner

    out = re.sub(r'"([^"\n]*)"', _sub, body)
    return out if changed else None


def _perturb_blank_line(body: str) -> Optional[str]:
    if "\n\n" in body:
        return None
    return re.sub(r"\n(?=[a-z_]+:)", "\n\n", body)


def _perturb_comment(body: str) -> Optional[str]:
    """在顶层键前插入注释行（注释不参与解析；卡里已有注释也照样插新注释）。"""
    out = re.sub(r"\n(?=[a-z_]+:)", "\n# 629 probe comment\n", body)
    return out if out != body else None


def _perturb_flow_to_block(body: str) -> Optional[str]:
    """`- {a: 1, b: 2}` → 块映射（YAML 语义等价）。"""
    out, changed = [], False
    for ln in body.split("\n"):
        m = re.match(r"^(\s*)- \{(.+)\}$", ln)
        if not m or "{" in m.group(2) or "}" in m.group(2):
            out.append(ln)
            continue
        indent, inner = m.group(1), m.group(2)
        pairs = [p.strip() for p in inner.split(",")]
        if not all(re.match(r"^[\w.-]+: ", p) for p in pairs):
            out.append(ln)
            continue
        out.append(f"{indent}- {pairs[0]}")
        out.extend(f"{indent}  {p}" for p in pairs[1:])
        changed = True
    return "\n".join(out) if changed else None


_PERTURB_FN = {
    "trailing_ws": _perturb_trailing_ws,
    "quote_style": _perturb_quote_style,
    "blank_line": _perturb_blank_line,
    "comment": _perturb_comment,
    "flow_to_block": _perturb_flow_to_block,
}


def perturb(kind: str, text: str) -> Optional[str]:
    """返回扰动后的全文；不适用返回 None。"""
    parts = split_frontmatter(text)
    if parts is None:
        return None
    head, body, fence, rest = parts
    new_body = _PERTURB_FN[kind](body)
    if new_body is None:
        return None
    return f"{head}{new_body}{fence}{rest}"


def fm_equal(a: str, b: str) -> bool:
    """解析后 frontmatter 逐键相等 ⇒ 语义等价（本工具的语义不变判据）。"""
    import atom_evidence_replay as replay

    try:
        return replay.parse_frontmatter(a) == replay.parse_frontmatter(b)
    except ValueError:
        return False


# ── 镜像沙箱 ─────────────────────────────────────────────────────

def mirror(dst: str) -> dict[str, str]:
    for sub in ("atoms", "evidence"):
        src = os.path.join(ROOT, sub)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(dst, sub))
    return {"atoms": os.path.join(dst, "atoms"),
            "evidence": os.path.join(dst, "evidence")}


class Redirect:
    """把 gate_engine 的 ATOMS/EVIDENCE 指到镜像；退出时还原 + 清缓存。"""

    def __init__(self, paths: dict[str, str]) -> None:
        self.paths = paths
        self._old: dict[str, Any] = {}

    def __enter__(self) -> "Redirect":
        import pathlib

        import gate_engine as ge

        for name in ("ATOMS", "EVIDENCE"):
            if name.lower() in self.paths:
                self._old[name] = getattr(ge, name)
                setattr(ge, name, pathlib.Path(self.paths[name.lower()]))
        ge.clear_meta_cache()
        return self

    def __exit__(self, *exc: Any) -> None:
        import gate_engine as ge

        for name, val in self._old.items():
            setattr(ge, name, val)
        ge.clear_meta_cache()


def warn_rules(card_name: str) -> set[str]:
    """跑一次全库（当前 ATOMS/EVIDENCE 指向）并取该卡的 warn 规则集合。

    按 `Finding.target` **后缀**匹配：镜像在系统临时目录时 `_rel()` 会退化成绝对路径。
    """
    import gate_engine as ge

    out = set()
    for f in ge.run(include_advice=True):
        if str(f.target).endswith(card_name) and f.severity == "warn":
            out.add(f.rule_id)
    return out


# ── 主测量 ───────────────────────────────────────────────────────

def measure() -> dict[str, Any]:
    import autoimmune_rate_framework as A
    import gate_engine as ge

    picked = A.cards(A.CLEAN_PRIMARY)[:SAMPLE_N]
    rows: list[dict[str, Any]] = []
    non_neutral: list[dict[str, Any]] = []
    fp_events: list[dict[str, Any]] = []

    # 真实仓库读数必须在**重定向之前**取（重定向后 target 会变成临时绝对路径）
    real = {r["id"]: {h["rule"] for h in r["warn"]} for r in A.measure()["cards"]}

    tmp = tempfile.mkdtemp(prefix="queyi_629_probe_")
    try:
        paths = mirror(tmp)
        with Redirect(paths) as red:
            baseline = {c["id"]: warn_rules(os.path.basename(c["path"]))
                        for c in picked}
            # 真阴性：镜像里原样卡的 warn 集合必须 == 真实仓库（A1）读数
            tn_ok = all(real.get(cid) == rules for cid, rules in baseline.items())
            for c in picked:
                name = os.path.basename(c["path"])
                src = os.path.join(red.paths["atoms"],
                                   os.path.relpath(c["path"], A.ATOMS))
                with open(src, encoding="utf-8") as fh:
                    text = fh.read()
                base = baseline[c["id"]]
                for kind in PERTURBATIONS:
                    new_text = perturb(kind, text)
                    if new_text is None:
                        rows.append({"card": c["id"], "kind": kind,
                                     "status": "not_applicable"})
                        continue
                    if not fm_equal(text, new_text):
                        non_neutral.append({"card": c["id"], "kind": kind})
                        rows.append({"card": c["id"], "kind": kind,
                                     "status": "non_neutral_discarded"})
                        continue
                    with open(src, "w", encoding="utf-8", newline="\n") as fh:
                        fh.write(new_text)
                    ge.clear_meta_cache()
                    after = warn_rules(name)
                    added = sorted(after - base)
                    rows.append({"card": c["id"], "kind": kind, "status": "measured",
                                 "new_warn": added, "semantics_equal": True})
                    if added:
                        fp_events.append({"card": c["id"], "kind": kind,
                                          "new_rules": added})
                    with open(src, "w", encoding="utf-8", newline="\n") as fh:
                        fh.write(text)
                    ge.clear_meta_cache()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    measured = [r for r in rows if r["status"] == "measured"]
    return {"cards": [c["id"] for c in picked], "rows": rows,
            "non_neutral": non_neutral, "fp_events": fp_events,
            "measured": len(measured),
            "na": sum(1 for r in rows if r["status"] == "not_applicable"),
            "tn_ok": tn_ok,
            "false_positive_rate": (len(fp_events) / len(measured)) if measured else 0.0,
            "poison": POISON_BASELINE, "escape": ESCAPE_BASELINE,
            "perturbation_kinds": list(PERTURBATIONS)}


def write_report() -> str:
    m = measure()
    fp_rules = sorted({r for e in m["fp_events"] for r in e["new_rules"]})
    lines = [
        "# 629 A2 · 误报注入探针结果（Negative Control，自身免疫证据）", "",
        "> 工具：`tools/autoimmune_probe_629.py`（纯标准库，**真实仓库零写入**："
        "`atoms/`+`evidence/` 整树镜像到系统临时目录，用完即删）", "",
        "## 一、方法", "",
        f"- 样本：A1 主口径干净卡按 id 排序取前 {SAMPLE_N} 张 —— "
        f"{'、'.join('`' + c + '`' for c in m['cards'])}",
        f"- 扰动种类（只改格式）：{', '.join('`' + k + '`' for k in m['perturbation_kinds'])}",
        "- **语义等价判据**：扰动后 `parse_frontmatter` 解析结果与原文**逐键相等**；"
        f"不等价的扰动一律丢弃（本次丢弃 {len(m['non_neutral'])} 次）。",
        "- 判据：扰动后该卡**新增 warn 规则** = 假阳性（自身免疫）证据。", "",
        "## 二、混淆矩阵（来源标注）", "",
        "| 格 | 含义 | 值 | 来源 |", "|---|---|---|---|",
        f"| 真阴性 TN | 镜像中原样卡 warn 集合 == 真实仓库读数（阴性对照成立） | "
        f"{'✅ 一致' if m['tn_ok'] else '❌ 不一致'} | 本工具实测 |",
        f"| 假阳性 FP | 语义不变的格式微扰副本被**新增 warn** | "
        f"**{len(m['fp_events'])} / {m['measured']}** 次扰动 | 本工具实测 |",
        f"| 真阳性 TP | 毒样例被 block | {m['poison']} | §一 standing baseline（poison_drill "
        "不重跑，§零.1） |",
        f"| 假阴性 FN | 错误知识逃逸 | {m['escape']} | §一 standing baseline（616 修正） |",
        "",
        f"**格式过敏率（假阳性率）= {m['false_positive_rate'] * 100:.1f}%**"
        f"（{len(m['fp_events'])}/{m['measured']} 次有效扰动）", "",
        "## 三、逐扰动明细", "",
        "| 卡 | 扰动 | 状态 | 新增 warn 规则 |", "|---|---|---|---|",
    ]
    for r in m["rows"]:
        st = {"measured": "已测", "not_applicable": "不适用",
              "non_neutral_discarded": "语义不等价（丢弃）"}[r["status"]]
        nr = "、".join(f"`{x}`" for x in r.get("new_warn", [])) or "—"
        lines.append(f"| `{r['card']}` | `{r['kind']}` | {st} | {nr} |")
    lines += ["", "## 四、结论", ""]
    if not m["fp_events"]:
        lines += [
            f"- **{m['measured']} 次语义不变的格式微扰，零新增 warn ⇒ 格式过敏率 0%**。"
            "这说明现有 warn 规则**不是格式驱动**：A1 里 100% 的 warn 来自**内容/口径**"
            "（命题级字段缺失、object 非规范概念短语、引用目标不存在），不是标点/空白/引号。",
            "- 对自身免疫问题的含义：**靠放宽格式救不了**——要降自身免疫率，必须改**规则口径**"
            "（命题级字段对新卡必需、对老卡豁免）或**补齐卡字段**，二者都需人审裁决。", "",
        ]
    else:
        lines += [
            f"- 检出 **{len(m['fp_events'])} 次格式过敏**，涉及规则："
            f"{'、'.join('`' + r + '`' for r in fp_rules)}",
            "- 这些规则对纯格式差异敏感 ⇒ 自身免疫真实存在，建议按此清单收紧规则的输入口径"
            "（先规范化 YAML 再判定），并列入交人项。", "",
        ]
    if m["non_neutral"]:
        lines += [
            f"- 另有 {len(m['non_neutral'])} 次扰动被判**语义不等价**而丢弃"
            f"（{'、'.join(e['card'] + '/' + e['kind'] for e in m['non_neutral'])}）——"
            "如实登记，不把语义改动计入自身免疫。", ""]
    lines += [
        "## 五、局限", "",
        "- 样本 5 张卡 × 最多 5 类扰动，**不是统计抽样**：结论只能证伪（「某类格式过敏存在」），"
        "不能证明「所有格式都不过敏」。",
        "- 镜像只复制 `atoms/` + `evidence/`；跨到 `Examples/` / `golden` / `misconceptions` 的"
        "规则读的是真实仓库（两侧一致，故差分有效，但**镜像内卡与真实仓库其他根的组合**"
        "可能在真实流程里不出现）。",
        "- 语义等价用 `parse_frontmatter` 判据（本项目的解析器）；若解析器与实际 YAML 语义"
        "有偏差，判据随之偏差 —— 已如实登记。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    txt = ('---\nid: ATOM-T-001\nstatus: verified\ntitle: "带引号的标题"\n'
           "history:\n  - {level: draft, at: legacy, by: writer:agent}\n---\n\n正文\n")
    chk("扰动器覆盖 5 类", len(PERTURBATIONS) == 5)
    for kind in PERTURBATIONS:
        p = perturb(kind, txt)
        chk(f"扰动 {kind} 适用且语义等价", p is not None and fm_equal(txt, p),
            "" if p is not None else "(不适用)")
    chk("语义改动被判不等价",
        not fm_equal(txt, txt.replace("status: verified", "status: draft")))
    m = measure()
    chk("真实仓库零写入（atoms/evidence 未被改动）", _repo_clean(),
        f"({_git_dirty()})")
    chk("阴性对照成立（镜像读数 == 真实读数）", m["tn_ok"])
    chk("样本数 = 5 张干净卡", len(m["cards"]) == SAMPLE_N)
    chk("至少发生 1 次有效扰动", m["measured"] >= 1, f"({m['measured']})")
    chk("报告存在且含混淆矩阵", os.path.exists(OUT_MD)
        and "混淆矩阵" in open(OUT_MD, encoding="utf-8").read())
    print(f"A2 autoimmune probe check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _git_dirty() -> str:
    import subprocess

    p = subprocess.run(["git", "status", "--porcelain", "--", "atoms", "evidence"],
                       capture_output=True, text=True, cwd=ROOT, check=False)
    return p.stdout.strip()


def _repo_clean() -> bool:
    return _git_dirty() == ""


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 A2 误报注入探针（只读）")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写 data/autoimmune_probe_results.md")
    ap.add_argument("--json", action="store_true", help="打印实测 JSON")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        print(f"written {write_report()}")
        return 0
    m = measure()
    if args.json:
        print(json.dumps({k: v for k, v in m.items() if k != "rows"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"sampled={len(m['cards'])} measured={m['measured']} "
          f"fp={len(m['fp_events'])} rate={m['false_positive_rate'] * 100:.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
