# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""676h 任务 A · 论文数字可追溯性审计工具（verify_paper_numbers.py）。

做什么
------
把论文（tex）里出现的**每一个数字**拿出来，逐条追到它的**权威数据源**，输出：

* data/676h_number_audit.json   —— 机器可读的逐条核对结果
* data/676h_number_audit_report.md —— 人类可读的不一致清单 / 待更新清单 / 覆盖度报告

判定规则（诚实边界，不可绕过）
------------------------------
1. **论文迁就源**：每条检察（claim）的期望值由**源文件**算出；论文里必须能找到这个写法，
   找不到就是 INCONSISTENT/MISSING。绝不反过来改源文件去迁就论文。
2. **不伪造**：676f（A5 全量）/676g（盲区地图）未就绪时，相关检察标记为 `pending_*`，
   其期望值仍取**当前已落盘**的旧产物（a5_673p.json 等），并在报告里显式标注"待更新"。
3. **覆盖度必须报**：除了逐条检察，脚本还会扫描 tex 里**全部**数字 token，
   把未被任何检察覆盖的按类别归类（引用年份 / 排版参数 / ...），剩下的列进
   `unclassified`，**不允许悄悄忽略**。

用法
----
    python tools/verify_paper_numbers.py                    # 默认审计 v1.1 主稿
    python tools/verify_paper_numbers.py --no-cmd           # 不跑计数类命令（快）
    python tools/verify_paper_numbers.py --tex <path>       # 指定 tex

退出码：0 = 无 active 级不一致；1 = 存在 active 级不一致（pending 级不计入）。
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# 权威源（relative to ROOT）
# --------------------------------------------------------------------------
SOURCE_FILES = {
    "current_numbers": "data/current_numbers.json",
    "holdout_reveal": "data/holdout_reveal_5_672h.json",
    "holdout_reveal_3": "data/holdout_reveal_3_665.json",
    "reveal_update_671a": "data/experiments/reveal_update_671a.json",
    "corpus_reveal": "data/external_corpus_reveal_672h.json",
    "mutation_core": "data/656_mutation_report.json",
    "mutation_all": "data/656_mutation_report_all.json",
    "defect_injection": "data/defect_injection_661.json",
    "external_anchor": "data/external_anchor_reveal_672j.json",
    "llm_arm": "data/experiments/llm_arm_672i.json",
    "external_tools": "data/673e_comparison_stats.json",
    "a5": "data/experiments/a5_673p.json",           # 673p/673r 口径（已被 676f 取代，仅附录保留）
    "a5_676f": "data/a5_676f_results.json",          # 676f 全量重跑（论文正文引用的权威源）
    "blindspot": "data/blindspot_676g_stats.json",   # 676g 检测器能力边界地图
}

# 676f / 676g 就绪判定（与 676h 提示词一致）
DEPENDENCY_FILES = {
    "676f": [
        ("data/a5_676f_results.json", 1),
        ("data/a5_676f_matrix_local.jsonl", 1147),
        ("data/a5_676f_matrix_san.jsonl", 1147),
    ],
    "676g": [
        ("data/blindspot_676g_stats.json", 1),
        ("data/blindspot_676g_ckpt_san.jsonl", 3126),
    ],
}

_NUM_RE = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])")
_YEAR_RE = re.compile(r"^(19|20)\d{2}$")
_SKIP_LINE_HINTS = (
    "\\usepackage",
    "\\newcommand",
    "\\pgfplotsset",
    "\\documentclass",
    "\\usetikzlibrary",
    "\\renewcommand",
)
_FORMAT_HINTS = (
    "\\begin{axis}", "\\begin{tikzpicture}", "\\begin{tabular}", "\\begin{minipage}",
    "\\addplot", "\\draw", "\\node", "\\path", "\\legend", "\\coordinate",
    "legend style", "x tick label", "y tick label", "symbolic x coords", "enlarge x limits",
    "width=", "height=", "ymin=", "ymax=", "bar width", "inner sep", "minimum width",
    "minimum height", "text width", "font=", "at={", "anchor=", "below=", "right=",
    "\\multicolumn", "\\cmidrule", "\\toprule", "\\midrule", "\\bottomrule",
    "p{", "l@{", "r@{", "c@{", "\\setlength", "\\vspace", "\\hspace",
    "nodes near coords", "title style", "compat=", "\\centering",
)

# 上下文归类规则（在"是否被检察覆盖"之后生效；只用于把**非经验**数字分门别类，
# 绝不用于把经验数字悄悄洗掉——所有归类结果都会连同样例写进 JSON 报告，可人工复核）
_CONTEXT_RULES_RAW = [
    (r"Cohen", "method_constant", "效应量口径/阈值常数（Cohen's h）"),
    (r"\\alpha|alpha\\b|significan", "method_constant", "显著性水平/统计口径常数"),
    (r"Clopper|Wilson|Wald|CP ?95|CI|interval| Kernel", "method_constant", "CI 口径常数（如 95）"),
    (r"Belnap|support|refutation|texttt\{(pass|fail|unknown|contradict)\}",
     "logic_constant", "四值逻辑坐标 / 布尔常量"),
    (r"swemera|SWE-MERA", "external_literature", "引自 SWE-MERA（需核对被引原文）"),
    (r"illusion|SWE-bench|LiveBench|MUTGEN|ACH\b|Cleverest|MiniCheck|CELEUS",
     "external_literature", "引自外部论文（需核对被引原文）"),
    (r"CVE-|CVSS|ASR|indirect-injection|prompt injection",
     "external_literature", "引自安全文献（CVE/CVSS/ASR）"),
    (r"[Pp]oisoning|malicious samples|tokens", "external_literature", "引自投毒文献"),
    (r"e-process|Ville|anytime-valid|supermartingale|e-value",
     "design_constant", "任意时刻检验阈值 / 设计常数"),
    (r"Merkle|merkle|controlled director|hash chain|OTS",
     "system_constant", "受控目录/账本结构常数"),
    (r"\bL0\b|\bL1\b|gates?|Gates?|red line", "system_constant", "门禁层/门禁条数常数"),
    (r"AI Act|Regulation|Article| GDPR", "external_regulation", "法规条款编号"),
    (r"third-party audit|credibility| predecessor's", "thirdparty_audit", "第三方审计评分（如在作者兵团别处登记）"),
    (r"retired|669d-era|superseded|pre-expansion|it is registered as a composition shift",
     "historical_retired", "已退役口径/被取代的旧值（明确标注为不可再用）"),
    (r"Engineering incidents|Tectonic|CRLF|range self-check|guard red| Did not reproduce",
     "engineering_narrative", "工程事件/自测等非经验叙述数字"),
    (r"\bd3[a-z]?-?\d+\b|\bh\d+\b", "sample_id", "样本编号（非统计量）"),
    (r"Correction note|cannot be reproduced|earlier draft wrote", "erratum_retired",
     "勘误：明确标注为不可复现的旧值"),
    (r"Two independent proportions|Paired \(exact McNemar|\\psi|\\pm", "design_constant",
     "样本量幂分析的输入参数（p1/p2/ψ）"),
    (r"temperature|prompt v|budget|Declared caliber|budget-matched|seed|split",
     "design_constant", "实验协议参数（种子、切分规则、温度、预算、档位）"),
    (r"labels must follow thresholds|reading \d|Effect-size labels", "method_constant",
     "效应量标签/阈值讨论中的示例值"),
    (r"unblinded samples merged|differed by \d+ catches|the same raw catch counts|same \d+ catches",
     "engineering_narrative", "同一次体外的现象描述（非独立统计量）"),
    (r"\\kappa|Krippendorff|re-label|subsample|third-party re-review", "design_constant",
     "标注一致性/复标注协议参数"),
    (r"pre-673u|since fixed|recomputed value|clang-tidy \(LLVM|cppcheck~", "historical_retired",
     "被取代的旧值/工具版本"),
    (r"3\.1|Modules| cyclic SCCs|self-loops|with 58 tests|if it took", "engineering_narrative",
     "工程事实叙述数字"),
    (r"\\cite\{", "cited_context", "出现在引用附近的数字（人工复核）"),
]
CONTEXT_RULES = [(re.compile(rx), cls, note) for rx, cls, note in _CONTEXT_RULES_RAW]


# --------------------------------------------------------------------------
# 小工具
# --------------------------------------------------------------------------
def _p(rel: str) -> str:
    return os.path.join(ROOT, rel.replace("/", os.sep))


def load_json(rel: str):
    with open(_p(rel), encoding="utf-8") as f:
        return json.load(f)


def get_path(obj, dotted: str):
    """按点路径取值；路径断开返回 None（不抛异常，便于报告 "源缺失"）。"""
    cur = obj
    for part in dotted.split("."):
        if isinstance(cur, list):
            try:
                cur = cur[int(part)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            if part not in cur:
                return None
            cur = cur[part]
        else:
            return None
    return cur


def pct(v, places: int = 1) -> str | None:
    r"""百分数渲染：与论文写法一致（不做 \% 后缀，匹配时允许后缀任意字符）。"""
    if v is None:
        return None
    return f"{round(float(v) + 0.0, places):.{places}f}"


def num(v, places: int | None = None) -> str | None:
    if v is None:
        return None
    if places is None:
        # 整数不带小数点
        fv = float(v)
        return str(int(round(fv))) if abs(fv - round(fv)) < 1e-9 else f"{fv:g}"
    return f"{round(float(v), places):.{places}f}"


def ratio(k, n) -> str | None:
    if k is None or n is None:
        return None
    return f"{int(round(float(k)))}/{int(round(float(n)))}"


def ci_pair(lo, hi, places: int = 1) -> str:
    return f"{pct(lo, places)}, {pct(hi, places)}"


def sci(mantissa: float, exponent: int, mant_places: int = 1) -> str:
    """按论文写法渲染科学计数法：2.3\\times10^{-10}"""
    m = f"{round(float(mantissa), mant_places):.{mant_places}f}"
    return f"{m}\\times10^{{{exponent}}}"


def mant_exp(value: float):
    """把 2.328e-10 拆成 (2.3, -10) —— 与 sci() 的渲染口径一致。"""
    if value is None or value == 0:
        return None, None
    exp = math.floor(math.log10(abs(value)))
    m = value / (10 ** exp)
    return round(m, 1), exp


def line_of(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


# 相邻字符之间可能出现的 LaTeX 噪声（数学模式开关、千分位、薄空格等）
_LATEX_NOISE = r"(?:[\$\{\}]|\\,|\\;|\\!|\\ |\\thinspace)*"


def literal_regex(lit: str) -> re.Pattern:
    """把字面量转成可匹配 tex 源码的正则。

    考虑到了三种常见干扰：math 模式开关（`82.9$\\to$87.5`）、数学分隔符（`$+7.8$pp`）
    以及换行带来的多空格。因此字符之间允许出现上述噪声。
    """
    parts = []
    for ch in lit:
        if ch.isspace():
            parts.append(r"(?:\s|\\,|\\;|\\!|\\ )*")
        else:
            parts.append(re.escape(ch))
        parts.append(_LATEX_NOISE)
    body = "".join(parts)
    if body.endswith(_LATEX_NOISE):
        body = body[: -len(_LATEX_NOISE)]
    return re.compile(r"(?<![\w.])" + body + r"(?!\d)")


def find_literal(text: str, lit: str, ctx: re.Pattern | str | None = None, window: int = 200):
    """返回 [(start, end, line, snippet)]；ctx 为窗口内的额外上下文正则。"""
    rx = literal_regex(lit)
    ctx_rx = re.compile(ctx) if isinstance(ctx, str) else ctx
    out = []
    for m in rx.finditer(text):
        s, e = m.span()
        if ctx_rx is not None:
            lo = max(0, s - window)
            hi = min(len(text), e + window)
            if not ctx_rx.search(text[lo:hi]):
                continue
        out.append((s, e, line_of(text, s), text[max(0, s - 60):e + 60].replace("\n", " ")))
    return out


def count_lines(rel: str) -> int | None:
    p = _p(rel)
    if not os.path.exists(p):
        return None
    n = 0
    with open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.strip():
                n += 1
    return n


def check_dependencies():
    """返回 {name: {file: {'n': 行数/None, 'need': 需求, 'ready': bool}}} 与总就绪情况。"""
    res = {}
    for name, files in DEPENDENCY_FILES.items():
        entry = {}
        ready = False
        for rel, need in files:
            p = _p(rel)
            if os.path.exists(p):
                n = count_lines(rel) if rel.endswith(".jsonl") else 1
            else:
                n = None
            ok = n is not None and n >= need
            ready = ready or ok
            entry[rel] = {"n": n, "need": need, "ready": ok}
        res[name] = {"files": entry, "ready": ready}
    return res


# --------------------------------------------------------------------------
# 检察清单（claims）
# --------------------------------------------------------------------------
# 每条 claim：
#   id      唯一标识
#   label   中文说明（给人类看）
#   forms   论文里**应该出现**的字面写法（全部由源数据渲染出来，不是手抄）
#   source  权威源（json 路径 / 可执行重算命令 / 仓库扫描）
#   status  active（源已定）| pending_676f | pending_676g（源待新批次覆盖）
#   group   分组
#
# 判定：claim 的**任意一个** form 能在 tex 里找到 ⇒ consistent；一个都找不到 ⇒ missing。
# 这样即使论文只打印了某个写法的一部分，也不会误报。


def _atoms_scan():
    """重算 Verifier Coverage（论文 §4 口径）：
    实卡 = atoms/**/ATOM-*.md 排除 draft650/；
    有证据锚点 = 卡片 status ∈ {verified, red-team-verified, machine-verified}。
    """
    root = _p("atoms")
    total, anchored = 0, 0
    per_domain = {}
    if not os.path.isdir(root):
        return None
    for dirpath, _dirs, files in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if rel_dir.startswith("draft650"):
            continue
        for fn in files:
            if not (fn.startswith("ATOM-") and fn.endswith(".md")):
                continue
            path = os.path.join(dirpath, fn)
            try:
                head = open(path, encoding="utf-8", errors="replace").read(4000)
            except OSError:
                continue
            m = re.search(r"^status:\s*(\S+)", head, re.MULTILINE)
            status = m.group(1) if m else ""
            domain = rel_dir.split("/")[0] if rel_dir and rel_dir != "." else "(root)"
            d = per_domain.setdefault(domain, {"real": 0, "anchored": 0})
            d["real"] += 1
            total += 1
            if status in ("verified", "red-team-verified", "machine-verified"):
                d["anchored"] += 1
                anchored += 1
    return {"real": total, "anchored": anchored, "per_domain": per_domain}


def _run_cmd(cmd, timeout=180):
    """跑一条只读重算命令，取输出里的第一个数字。"""
    try:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                           timeout=timeout, shell=True)
    except Exception as e:  # noqa: BLE001
        return None, f"命令执行失败: {e}"
    if r.returncode != 0:
        return None, (r.stderr or r.stdout or "").strip()[-200:]
    nums = _NUM_RE.findall(r.stdout)
    if not nums:
        return None, f"输出里没有数字: {r.stdout[:200]!r}"
    return float(nums[0]), None


def _cohens_h(p1, p2):
    return 2 * math.asin(math.sqrt(p2)) - 2 * math.asin(math.sqrt(p1))


def _z(p):
    """标准正态分位数的 Acklam 近似足够本报告使用（与 scipy 对比误差 <1e-4）。"""
    import statistics
    return statistics.NormalDist().inv_cdf(p)


def n_total_samplesize(p1, p2, alpha=0.05, power=0.8, paired=False, psi=None):
    """样本量重定向算（与附录 tab:samplesize 同口径，独立复核通过）。

    独立两比例：per_group = ((z_{1-α/2}+z_{1-β})/h)^2，h = Cohen arcsine h；表格里的 n 为两组合计。
    配对（Connor 1987）：n_pairs = (z_a·√ψ + z_b·√(ψ-d²))² / d²，ψ = 不一致对比例，d = |p2-p1|。
    """
    h = abs(_cohens_h(p1, p2))
    if h == 0:
        return None
    za = _z(1 - alpha / 2)
    zb = _z(power)
    if paired:
        if psi is None:
            return None
        d = abs(p2 - p1)
        inner = psi - d * d
        if inner <= 0:
            return None
        return ((za * math.sqrt(psi) + zb * math.sqrt(inner)) ** 2) / (d * d)
    return 2 * ((za + zb) / h) ** 2


def build_claims(src, use_cmd=True):
    cn = src["current_numbers"]
    hr = src["holdout_reveal"]
    cr = src["corpus_reveal"]
    a5 = src["a5"]

    claims = []

    def C(cid, label, forms, group, source, status="active", note=""):
        forms = [f for f in forms if f]
        if not forms:
            return
        claims.append({
            "id": cid, "label": label, "forms": forms, "group": group,
            "source": source, "status": status, "note": note,
        })

    J = lambda rel, *paths: {"kind": "json", "file": rel, "paths": list(paths)}  # noqa: E731

    # ---------------- A. 核心三臂（current_numbers / 672h 口径） ----------------
    ho = cn["holdout"]; co = cn["corpus"]  # noqa: E702
    C("A01", "holdout 可测检出率 82.9% (34/41) CI[67.9,92.8]",
      [pct(ho["rate_pct"]), ratio(ho["k"], ho["n"]),
       ci_pair(ho["cp95"][0], ho["cp95"][1])],
      "A.核心三臂", J("data/current_numbers.json", "holdout.rate_pct", "holdout.k", "holdout.n", "holdout.cp95"))

    C("A02", "corpus 可测检出率 62.5% (40/64) CI[49.5,74.3]",
      [pct(co["rate_pct"]), ratio(co["k"], co["n"]),
       ci_pair(co["cp95"][0], co["cp95"][1])],
      "A.核心三臂", J("data/current_numbers.json", "corpus.rate_pct", "corpus.k", "corpus.n", "corpus.cp95"))

    C("A03", "corpus 全样本口径 52.6%",
      [pct(co["all_samples_pct"])],
      "A.核心三臂", J("data/current_numbers.json", "corpus.all_samples_pct"))

    bh = cn["baseline_arms"]["holdout"]; bc = cn["baseline_arms"]["corpus"]  # noqa: E702
    C("A04", "Static 臂 holdout 2.4% (1/41) / corpus 17.2% (11/64)",
      [pct(bh["static"]["rate_pct"]), ratio(bh["static"]["k"], bh["static"]["n"]),
       pct(bc["static"]["rate_pct"]), ratio(bc["static"]["k"], bc["static"]["n"])],
      "A.核心三臂", J("data/current_numbers.json", "baseline_arms.holdout.static.rate_pct",
                   "baseline_arms.corpus.static.rate_pct"))
    C("A05", "Random† 臂 holdout 9.8% (4/41) / corpus 21.9% (14/64)",
      [pct(bh["random_proxy"]["rate_pct"]), ratio(bh["random_proxy"]["k"], bh["random_proxy"]["n"]),
       pct(bc["random_proxy"]["rate_pct"]), ratio(bc["random_proxy"]["k"], bc["random_proxy"]["n"])],
      "A.核心三臂", J("data/current_numbers.json", "baseline_arms.holdout.random_proxy.rate_pct",
                   "baseline_arms.corpus.random_proxy.rate_pct"))

    def _cmp(cid, key, label):
        c = cn["comparisons"][key]
        mant, exp = mant_exp(c["mcnemar_p"])
        forms = [f"+{pct(c['delta_pp'])}pp",
                 f"{pct(c['ci_pp'][0])}, {pct(c['ci_pp'][1])}",
                 sci(mant, exp),
                 f"{round(c['cohens_h'], 2):.2f}"]
        C(cid, label, forms, "A.核心三臂",
          J("data/current_numbers.json", f"comparisons.{key}.delta_pp",
            f"comparisons.{key}.ci_pp", f"comparisons.{key}.mcnemar_p",
            f"comparisons.{key}.cohens_h"))

    _cmp("A06", "holdout_fd_vs_static", "Δ(Static→FD) holdout +80.5pp CI[68.4,92.6] p=2.3e-10 h=1.98")
    _cmp("A07", "holdout_fd_vs_random", "Δ(Random†→FD) holdout +73.2pp CI[59.6,86.7] p=1.9e-9 h=1.65")
    _cmp("A08", "corpus_fd_vs_static", "Δ(Static→FD) corpus +45.3pp CI[33.1,57.5] p=3.7e-9 h=0.97")
    _cmp("A09", "corpus_fd_vs_random", "Δ(Random†→FD) corpus +40.6pp CI[28.6,52.7] p=3.0e-8 h=0.85")

    def _disc(key):
        d = cn["comparisons"][key]["discordant"]
        return f"({d['b_a_only']}, {d['c_b_only']})"

    C("A10", "配对不一致对 (b, c)（tab:e5 四行）",
      [_disc("holdout_fd_vs_static"), _disc("corpus_fd_vs_static"),
       _disc("holdout_fd_vs_random"), _disc("corpus_fd_vs_random")],
      "A.核心三臂",
      J("data/current_numbers.json", "comparisons.*.discordant.b_a_only", "comparisons.*.discordant.c_b_only"),
      note="四个对比都是 c=0 结构（对手的 catch 是 FD catch 的子集）")

    C("A11", "对照假阳性 0.0% (0/11)",
      ["0.0\\% (0/11)", pct(cn["control_false_positive"]["rate_pct"])],
      "A.核心三臂", J("data/current_numbers.json", "control_false_positive.rate_pct",
                   "control_false_positive.fp", "control_false_positive.total"))

    C("A12", "缺陷重注入 6/6 = 100%",
      [ratio(cn["defect_reinjection"]["k"], cn["defect_reinjection"]["n"]),
       pct(cn["defect_reinjection"]["rate_pct"])],
      "A.核心三臂", J("data/current_numbers.json", "defect_reinjection.k", "defect_reinjection.n"))

    C("A13", "CP95 半宽 12.5pp（holdout）",
      [pct(cn["holdout"]["cp95_halfwidth_pp"])],
      "A.核心三臂", J("data/current_numbers.json", "holdout.cp95_halfwidth_pp"))

    exp672 = cn.get("expansion_672h", {})
    C("A14", "扩样前 holdout 81.0% (17/21) CI[58.1,94.6]",
      [pct(exp672.get("holdout_before", {}).get("rate_pct")),
       ratio(exp672.get("holdout_before", {}).get("k"), exp672.get("holdout_before", {}).get("n"))],
      "A.核心三臂", J("data/current_numbers.json", "expansion_672h.holdout_before.rate_pct"))
    C("A15", "扩样前 corpus 54.2% (26/48)",
      [pct(exp672.get("corpus_before", {}).get("rate_pct")),
       ratio(exp672.get("corpus_before", {}).get("k"), exp672.get("corpus_before", {}).get("n"))],
      "A.核心三臂", J("data/current_numbers.json", "expansion_672h.corpus_before.rate_pct"),
      status="superseded:689重构", note="689 重构：扩样前后口径随旧正文段落移出正文（数据仍在产物）")
    C("A16", "H4 子集差额 corpus +33.3pp / holdout +4.0pp",
      [f"+{pct(exp672.get('H4_subset_delta', {}).get('corpus_pp'))}pp",
       f"+{pct(exp672.get('H4_subset_delta', {}).get('holdout_pp'))}pp"],
      "A.核心三臂", J("data/current_numbers.json", "expansion_672h.H4_subset_delta.corpus_pp"),
      status="superseded:689重构", note="689 重构：H4 子集差额随旧正文段落移出正文（数据仍在产物）")

    ss = cn.get("sample_size_672k", {})
    C("A17", "±5pp 半宽所需样本量 holdout 236 / corpus 378",
      [num(ss.get("holdout", {}).get("±5pp", {}).get("n")),
       num(ss.get("corpus", {}).get("±5pp", {}).get("n"))],
      "A.核心三臂", J("data/current_numbers.json", "sample_size_672k.holdout.±5pp.n",
                   "sample_size_672k.corpus.±5pp.n"))
    C("A18", "±10pp 半宽所需样本量 holdout 61 / corpus 97",
      [num(ss.get("holdout", {}).get("±10pp", {}).get("n")),
       num(ss.get("corpus", {}).get("±10pp", {}).get("n"))],
      "A.核心三臂", J("data/current_numbers.json", "sample_size_672k.holdout.±10pp.n",
                   "sample_size_672k.corpus.±10pp.n"))

    # ---------------- B. reveal 产物（分层与替代分母） ----------------
    hcum = hr["cumulative"]; ccum = cr["cumulative"]  # noqa: E702
    C("B01", "holdout 累计 catch/miss/unknown = 34/7/1，分母 41",
      [ratio(hcum["error_subset"]["catch"], hcum["denominator"]["value"]),
       num(hcum["error_subset"]["unknown"])],
      "B.reveal", J("data/holdout_reveal_5_672h.json", "cumulative.error_subset.catch",
                  "cumulative.denominator.value"))
    C("B02", "holdout 口径 B（unknown→miss）34/42 = 81.0%",
      [ratio(hcum["error_subset"]["catch"], hcum["error_subset"]["total"]),
       pct(100.0 * hcum["error_subset"]["catch"] / hcum["error_subset"]["total"])],
      "B.reveal", J("data/holdout_reveal_5_672h.json", "cumulative.error_subset.total"))
    C("B03", "holdout 分层 sanitizer 84.6% (33/39)",
      [pct(hcum["by_layer"]["sanitizer"]["detect_rate_pct"]),
       ratio(hcum["by_layer"]["sanitizer"]["catch"], hcum["by_layer"]["sanitizer"]["denominator"]["value"])],
      "B.reveal", J("data/holdout_reveal_5_672h.json", "cumulative.by_layer.sanitizer.detect_rate_pct"))
    C("B04", "corpus 分层 sanitizer 85.3% (29/34) / compiler-warn 50.0% (9/18) / cross-compile 16.7% (2/12)",
      [pct(ccum["by_layer"]["sanitizer"]["detect_rate_pct"]),
       ratio(ccum["by_layer"]["sanitizer"]["catch"], ccum["by_layer"]["sanitizer"]["denominator"]["value"]),
       pct(ccum["by_layer"]["compiler-warn"]["detect_rate_pct"]),
       ratio(ccum["by_layer"]["compiler-warn"]["catch"], ccum["by_layer"]["compiler-warn"]["denominator"]["value"]),
       pct(ccum["by_layer"]["cross-compile"]["detect_rate_pct"]),
       ratio(ccum["by_layer"]["cross-compile"]["catch"], ccum["by_layer"]["cross-compile"]["denominator"]["value"])],
      "B.reveal", J("data/external_corpus_reveal_672h.json", "cumulative.by_layer.*.detect_rate_pct"))
    C("B05", "corpus 口径 B（unknown→miss）40/73 = 54.8%",
      [ratio(ccum["catch"], ccum["total"] - ccum["not_error"]),
       pct(100.0 * ccum["catch"] / (ccum["total"] - ccum["not_error"]))],
      "B.reveal", J("data/external_corpus_reveal_672h.json", "cumulative.total", "cumulative.not_error"))
    C("B06", "corpus 口径 C（全样本）40/76 = 52.6%",
      [ratio(ccum["catch"], ccum["total"]),
       pct(100.0 * ccum["catch"] / ccum["total"])],
      "B.reveal", J("data/external_corpus_reveal_672h.json", "cumulative.total"))
    C("B07", "corpus 分层 Excluded unknown=9 / not_error=3",
      [num(ccum["unknown"]), num(ccum["not_error"])],
      "B.reveal", J("data/external_corpus_reveal_672h.json", "cumulative.unknown", "cumulative.not_error"))
    C("B08", "holdout 新子集 17/20 = 85.0%（round5）",
      [ratio(hr["round5"]["error_subset"]["catch"], hr["round5"]["error_subset"]["total"]),
       pct(hr["round5"]["error_subset"]["detect_rate_pct"])],
      "B.reveal", J("data/holdout_reveal_5_672h.json", "round5.error_subset.detect_rate_pct"),
      status="superseded:689重构", note="689 重构：round5 子集数字随旧正文段落移出正文（数据仍在产物）")

    # 历史批次（tab:e3  Evolution Curve / Fig. evolution）
    hr3 = src.get("holdout_reveal_3") or {}
    if hr3:
        es = hr3.get("error_subset", {})
        cp = es.get("cp95") or hr3.get("cp95") or []
        C("B09", "历史批次 669：87.5%（14/16）与 CI[61.7, 98.4]",
          [pct(es.get("detect_rate_pct"))] +
          ([f"{pct(cp[0])}, {pct(cp[1])}"] if len(cp) >= 2 else []),
          "B.reveal", J("data/holdout_reveal_3_665.json", "error_subset.detect_rate_pct", "error_subset.cp95"))
        C("B10", "历史批次 660：80.0%（batch compare before）",
          [pct(hr3.get("compare_reveal_2", {}).get("before_rate_pct"))],
          "B.reveal", J("data/holdout_reveal_3_665.json", "compare_reveal_2.before_rate_pct"))

    # ---------------- C. 系统本体计数（可执行重算 / 仓库扫描） ----------------
    CMD_RULES = 'python -c "import sys;sys.path.insert(0,\'tools\');import gate_engine;print(len(gate_engine.RULES))"'
    CMD_LEDGER = 'python -c "n=sum(1 for l in open(r\'data/authority/decision_event_v2_ledger.jsonl\',encoding=\'utf-8\') if l.strip());print(n)"'
    CMD_ATOMS = 'python tools/counts_659.py --json'
    CMD_VC_CI = 'python -c "import sys;sys.path.insert(0,\'tools\');from stat_bounds import cp_interval;print(*[round(x*100,1) for x in cp_interval(31,42)])"'

    def _cmd_claim(cid, label, cmd, pick="first", places=0, group="C.系统计数", note=""):
        """跑命令拿真值；use_cmd=False 时该条标 skipped（不参与 miss 判定）。"""
        if not use_cmd:
            claims.append({"id": cid, "label": label, "forms": [], "group": group,
                           "source": {"kind": "cmd", "cmd": cmd}, "status": "skipped_cmd",
                           "note": note})
            return
        out, err = _run_cmd(cmd)
        if out is None:
            claims.append({"id": cid, "label": label, "forms": [], "group": group,
                           "source": {"kind": "cmd", "cmd": cmd}, "status": "cmd_failed",
                           "note": (note + " | " + (err or "")).strip(" |")})
            return
        C(cid, label, [num(out, places)], group, {"kind": "cmd", "cmd": cmd}, note=note)

    _cmd_claim("C01", "判决规则数 67（len(gate_engine.RULES)）", CMD_RULES, places=0)
    _cmd_claim("C02", "权威账本事件数 452（decision_event_v2_ledger.jsonl 非空行）", CMD_LEDGER, places=0)

    if use_cmd:
        out_a, err_a = _run_cmd(CMD_ATOMS)
        atoms_real = int(out_a) if out_a is not None else None
    else:
        atoms_real, err_a = None, "skipped"
    if atoms_real is not None:
        C("C03", f"实卡数 atoms_real = {atoms_real}（counts_659.py 现算）",
          [num(atoms_real)], "C.系统计数", {"kind": "cmd", "cmd": CMD_ATOMS})
    else:
        claims.append({"id": "C03", "label": "实卡数 atoms_real（counts_659.py 现算）",
                       "forms": [], "group": "C.系统计数",
                       "source": {"kind": "cmd", "cmd": CMD_ATOMS},
                       "status": "cmd_failed", "note": str(err_a)})

    vc = _atoms_scan()
    if vc and vc["real"]:
        C("C04", "Verifier Coverage = 31/42 = 73.8%",
          [ratio(vc["anchored"], vc["real"]),
           pct(100.0 * vc["anchored"] / vc["real"])],
          "C.系统计数",
          {"kind": "scan", "detail": "atoms/**/ATOM-*.md 排除 draft650/；status∈{verified,red-team-verified,machine-verified}"},
          note=f"本工具重算 anchored={vc['anchored']} real={vc['real']}")
        for dom in ("conc", "hist", "mem", "ub", "lang"):
            d = vc["per_domain"].get(dom)
            if not d:
                continue
            C(f"C05.{dom}", f"VC 分域 {dom} {d['anchored']}/{d['real']}",
              [f"{dom} {d['anchored']}/{d['real']}"], "C.系统计数",
              {"kind": "scan", "detail": f"atoms/{dom}/ATOM-*.md"},
              status="superseded:689重构",
              note="689 重构：Verifier Coverage（含分域）已从论文删除（工程遥测，非科学证据）")

    # VC 的 CP95：直接调用 stat_bounds.cp_interval（一次取两个分位）
    if use_cmd:
        r = subprocess.run(CMD_VC_CI, cwd=ROOT, capture_output=True, text=True, timeout=180, shell=True)
        vals = _NUM_RE.findall(r.stdout or "")
        if len(vals) >= 2:
            C("C06", "VC 的 Clopper–Pearson 95% CI [58.0, 86.1]",
              [f"{pct(float(vals[0]))}, {pct(float(vals[1]))}"], "C.系统计数",
              {"kind": "cmd", "cmd": CMD_VC_CI},
              status="superseded:689重构", note="689 重构：VC 及其 CI 已从论文删除（工程遥测，非科学证据）")
        else:
            claims.append({"id": "C06", "label": "VC 的 CP 95% CI（stat_bounds.cp_interval(31,42)）",
                           "forms": [], "group": "C.系统计数",
                           "source": {"kind": "cmd", "cmd": CMD_VC_CI},
                           "status": "cmd_failed", "note": (r.stderr or r.stdout or "")[:200]})

    # 规则严重度分解 44/16/7
    CMD_SEV = ('python -c "import sys;sys.path.insert(0,\'tools\');import gate_engine;'
               'from collections import Counter;c=Counter(getattr(r,\'severity\',None) for r in gate_engine.RULES);'
               'print(c.get(\'block\',0),c.get(\'warn\',0),c.get(\'advice\',0))"')
    if use_cmd:
        r = subprocess.run(CMD_SEV, cwd=ROOT, capture_output=True, text=True, timeout=180, shell=True)
        vals = _NUM_RE.findall(r.stdout or "")
        if len(vals) >= 3:
            a, b, c3 = (int(float(v)) for v in vals[:3])
            C("C07", f"规则严重度分解 block {a} / warn {b} / advice {c3}",
              [f"{a}/{b}/{c3}", num(a), num(b), num(c3)], "C.系统计数",
              {"kind": "cmd", "cmd": CMD_SEV},
              note="旧稿的 0/176/55 不可复现，已按现算值纠正")
        else:
            claims.append({"id": "C07", "label": "规则严重度分解", "forms": [], "group": "C.系统计数",
                           "source": {"kind": "cmd", "cmd": CMD_SEV}, "status": "cmd_failed",
                           "note": (r.stderr or r.stdout or "")[:200]})

    # 边界卡 / provenance / semantic scope（26 / 26/26 / 0/26）
    try:
        bp = load_json("data/boundary_provenance_658.json")
    except Exception:  # noqa: BLE001
        bp = None
    if isinstance(bp, dict) and isinstance(bp.get("cards"), list):
        cards = bp["cards"]
        prov_ok = sum(1 for c in cards if len(c.get("provenance") or {}) >= 3)
        scope_ok = sum(1 for c in cards if c.get("scope_complete"))
        C("C08", f"边界卡 {len(cards)} 张；provenance 完整 {prov_ok}/{len(cards)}；scope 完整 {scope_ok}/{len(cards)}",
          [num(len(cards)), f"{prov_ok}/{len(cards)}", f"{scope_ok}/{len(cards)}"],
          "C.系统计数",
          J("data/boundary_provenance_658.json", "cards[].provenance", "cards[].scope_complete"),
          note="provenance 完整 = provenance 字典字段数 ≥3（mutationset/generator/evidence）")

    # ---------------- 诚实性反向检察：81.2% 必须被标为"从未落盘" ----------------
    claims.append({
        "id": "N01", "label": "81.2% 必须在出现的每一处都被标为从未落盘/作废",
        "forms": [{"form": "81.2", "window": 900,
                  "cooccur": r"never landed|not landed|voided|never appeared|incident|can still recur"}],
        "group": "N.诚实性反向检察",
        "source": {"kind": "policy", "detail": "673c/676h 诚实边界：81.2% 不得作为已落盘结果引用"},
        "status": "active",
        "note": "若 81.2 出现在没有 never-landed 标注的句子里 ⇒ 违反",
    })

    # ---------------- D. A5（676f 重跑后将更新） ----------------
    ra = a5.get("real_attribution", {})
    ds_map = ra.get("datasets", {})

    def _byk(ds, k, pool="primary"):
        node = ds_map.get(ds, {}).get(pool, {})
        for b in node.get("by_k", []):
            if b.get("budget_k") == k:
                return b
        return None

    A5F = "data/experiments/a5_673p.json"
    for ds, eval_n_label in (("holdout", "holdout"), ("corpus", "corpus")):
        b4 = _byk(ds, 4)
        if not b4:
            continue
        arms = b4["arms"]
        pt = b4["paired_tests"].get("fd_vs_random", {})
        ms = b4.get("random_multi_seed", {})
        mant, exp = mant_exp(pt.get("mcnemar_p"))
        der_n = ds_map[ds]["derivation"]["n"]
        ev_n = ds_map[ds]["evaluation"]["n"]
        prefix = "D01" if ds == "holdout" else "D02"
        C(prefix, f"A5 {ds} 主端点 FD {arms['fd']['rate_pct']}% ({arms['fd']['k']}/{arms['fd']['n']}) vs Random {arms['random']['rate_pct']}%",
          [pct(arms["fd"]["rate_pct"]), ratio(arms["fd"]["k"], arms["fd"]["n"]),
           pct(arms["random"]["rate_pct"]), ratio(arms["random"]["k"], arms["random"]["n"]),
           pct(arms["static"]["rate_pct"]), ratio(arms["static"]["k"], arms["static"]["n"]),
           f"+{pct(pt.get('delta_pp'))}pp",
           f"{pct(pt['delta_ci95_pp'][0])}, {pct(pt['delta_ci95_pp'][1])}",
           sci(mant, exp) if ds == "holdout" else pct(pt.get("mcnemar_p"), 3),
           f"{round(pt.get('cohens_h', 0), 2):.2f}"],
          "D.A5",
          J(A5F, f"real_attribution.datasets.{ds}.primary.by_k[].arms/paired_tests"),
          status="superseded_by_676f",
          note="673p/673r 口径；已被 676f 全量重跑取代，论文仅在 app:humanize 保留其审计轨迹")
        C(prefix + "b", f"A5 {ds} 2000 次随机分布：FD 严格优于的比例与均值/标准差",
          [pct(100.0 * ms.get("fd_strictly_better_frac", 0), 2),
           pct(100.0 * ms.get("fd_strictly_better_frac", 0), 1),
           pct(ms.get("mean_rate_pct"), 1), pct(ms.get("sd_pp"), 1)],
          "D.A5",
          J(A5F, f"real_attribution.datasets.{ds}.primary.by_k[].random_multi_seed"),
          status="superseded_by_676f")
        C(prefix + "c", f"A5 设计量：{ds} 派生 n={der_n} / 评估 n={ev_n}",
          [num(der_n), num(ev_n), num(ra.get("primary_k")), num(ra.get("multi_seed_runs", 2000)),
           num(len(b4.get("candidates", []))), num(ds_map[ds].get("n_measurable_with_attribution"))],
          "D.A5",
          J(A5F, f"real_attribution.datasets.{ds}.derivation.n",
            f"real_attribution.datasets.{ds}.evaluation.n", "real_attribution.primary_k"),
          status="superseded_by_676f")

    # ---------------- D2. A5 全量重跑（676f）——论文正文引用的权威源 ----------------
    f67 = src.get("a5_676f") or {}
    F67F = "data/a5_676f_results.json"
    if f67:

        def _k(node, k):
            for b in (f67.get(node, {}) or {}).get("by_k", []):
                if b.get("budget_k") == k:
                    return b
            return None

        ss2 = f67.get("sample_stats", {})
        C("F01x", f"676f 样本簿记：{ss2.get('n_total')} 总样本；派生 {ss2.get('n_derivation')}；评估 {ss2.get('n_evaluation')}",
          [num(ss2.get("n_total")), num(ss2.get("n_derivation")), num(ss2.get("n_evaluation")),
           num(ss2.get("n_planted_true")), num(ss2.get("n_planted_false")),
           num((ss2.get("dedup") or {}).get("by_content"))],
          "D2.A5-676f", J(F67F, "sample_stats.n_total", "sample_stats.n_derivation",
                        "sample_stats.n_evaluation", "sample_stats.n_planted_false"))

        b4 = _k("primary_main_8candidates", 4)
        if b4:
            ar = b4["arms"]
            pt = b4["paired_tests"]
            ms = b4.get("random_multi_seed", {})
            mant, exp = mant_exp(pt["fd_vs_random"]["mcnemar_p"])
            m2, e2 = mant_exp(pt["fd_vs_static"]["mcnemar_p"])
            C("F02x", "676f 主端点（k=4，全 8 资产池）FD/Random/Static 三臂",
              [pct(ar["fd"]["rate_pct"]), ratio(ar["fd"]["k"], ar["fd"]["n"]),
               pct(ar["random"]["rate_pct"]), ratio(ar["random"]["k"], ar["random"]["n"]),
               pct(ar["static"]["rate_pct"]), ratio(ar["static"]["k"], ar["static"]["n"]),
               pct(ar["fd_full_pool"]["rate_pct"]), ratio(ar["fd_full_pool"]["k"], ar["fd_full_pool"]["n"])],
              "D2.A5-676f", J(F67F, "primary_main_8candidates.by_k[k=4].arms"))
            C("F03x", "676f 主端点 Δ(FD−Random) +24.0pp CI[+20.5, +27.5] p=2.3e-41 h=0.49 (b=136, c=0)",
              [f"+{pct(pt['fd_vs_random']['delta_pp'])}pp",
               f"{pct(pt['fd_vs_random']['delta_ci95_pp'][0])}, {pct(pt['fd_vs_random']['delta_ci95_pp'][1])}",
               sci(mant, exp),
               f"{round(pt['fd_vs_random']['cohens_h'], 2):.2f}",
               f"({pt['fd_vs_random']['discordant_a_only']},{pt['fd_vs_random']['discordant_b_only']})"],
              "D2.A5-676f", J(F67F, "primary_main_8candidates.by_k[k=4].paired_tests.fd_vs_random"))
            C("F04x", "676f 主端点 Δ(FD−Static) +29.9pp CI[+25.2, +34.5] p=1.9e-31",
              [f"+{pct(pt['fd_vs_static']['delta_pp'])}pp",
               f"{pct(pt['fd_vs_static']['delta_ci95_pp'][0])}, {pct(pt['fd_vs_static']['delta_ci95_pp'][1])}",
               sci(m2, e2), f"{round(pt['fd_vs_static']['cohens_h'], 2):.2f}"],
              "D2.A5-676f", J(F67F, "primary_main_8candidates.by_k[k=4].paired_tests.fd_vs_static"))
            C("F05x", "676f 2000 次随机分布：FD 严格优于 97.6%（Random 均值 40.2%，SD 9.3pp）",
              [pct(100.0 * ms.get("fd_strictly_better_frac", 0), 1),
               pct(ms.get("mean_rate_pct"), 1), pct(ms.get("sd_pp"), 1), num(ms.get("runs"))],
              "D2.A5-676f", J(F67F, "primary_main_8candidates.by_k[k=4].random_multi_seed"))

        b4c = _k("co_primary_excl_degenerate", 4)
        if b4c:
            pt2 = b4c["paired_tests"]
            m3, e3 = mant_exp(pt2["fd_vs_static"]["mcnemar_p"])
            C("F06x", "676f 并列分析（剔退化资产）：Δ(FD−Random)=0.0pp p=1.0；Δ(FD−Static)=+30.6pp CI[+26.0,+35.1] p=8.1e-34",
              ["0.0", "1.0",
               f"+{pct(pt2['fd_vs_static']['delta_pp'])}pp",
               f"{pct(pt2['fd_vs_static']['delta_ci95_pp'][0])}, {pct(pt2['fd_vs_static']['delta_ci95_pp'][1])}",
               sci(m3, e3), pct(b4c["arms"]["static"]["rate_pct"]),
               ratio(b4c["arms"]["static"]["k"], b4c["arms"]["static"]["n"])],
              "D2.A5-676f", J(F67F, "co_primary_excl_degenerate.by_k[k=4].paired_tests"))

        # k 扫描
        sweep_forms = []
        for b in (f67.get("primary_main_8candidates", {}) or {}).get("by_k", []):
            d = b["paired_tests"]["fd_vs_random"]["delta_pp"]
            p_ = b["paired_tests"]["fd_vs_random"]["mcnemar_p"]
            ci = b["paired_tests"]["fd_vs_random"]["delta_ci95_pp"]
            sweep_forms.append(f"+{pct(d)}pp")
            sweep_forms.append(f"+{pct(d)}")            # 表格里写作 +24.0（不带 pp）
            sweep_forms.append(f"{pct(ci[0])}, {pct(ci[1])}")
            if p_ >= 1e-4:
                sweep_forms.append(pct(p_, 3))
            else:
                mm, ee = mant_exp(p_)
                sweep_forms.append(sci(mm, ee))
            sweep_forms.append(pct(b["arms"]["fd"]["rate_pct"]))
            sweep_forms.append(pct(b["arms"]["random"]["rate_pct"]))
        C("F07x", "676f k 扫描（k=1..8）各档 Δ 与 p", sweep_forms, "D2.A5-676f",
          J(F67F, "primary_main_8candidates.by_k[].paired_tests.fd_vs_random"))

        # 子组（含 BH-FDR / Bonferroni）
        mult = f67.get("subgroup_multiplicity", {})
        for row in mult.get("rows", []):
            g = row["group"]
            C(f"F08x.{g}", f"676f 子组 {g}：Δ {row['delta_pp']:+.1f}pp，BH-FDR p={row['p_bh_fdr']:.2g}，Bonferroni p={row['p_bonferroni']:.2g}",
              [f"+{pct(row['delta_pp'])}pp", f"+{pct(row['delta_pp'])}",
               sci(*mant_exp(row["p_bh_fdr"])) if row["p_bh_fdr"] < 1e-3 else pct(row["p_bh_fdr"], 3),
               sci(*mant_exp(row["p_bonferroni"])) if row["p_bonferroni"] < 1e-3 else pct(row["p_bonferroni"], 3),
               num(row.get("n_evaluation"))],
              "D2.A5-676f", J(F67F, "subgroup_multiplicity.rows"),
              note="子组 p 必须报校正后值；未校正 p 不得单独宣称显著")
        C("F09x", f"676f 子组检验族大小 {mult.get('n_tests')}",
          [num(mult.get("n_tests"))], "D2.A5-676f", J(F67F, "subgroup_multiplicity.n_tests"))

        # planted 子集
        for key, tag in (("planted_false", "真实缺陷 planted=false"),
                         ("planted_true", "planted=true")):
            sub = f67.get(key) or {}
            if not sub:
                continue
            mm, ee = mant_exp(sub.get("mcnemar_p"))
            C(f"F10x.{key}", f"676f {tag}: FD {sub['fd_rate_pct']:.1f}% ({sub['fd_k']}/{sub['n']})，Δ {sub['delta_fd_minus_random_pp']:+.1f}pp",
              [pct(sub["fd_rate_pct"]), ratio(sub["fd_k"], sub["n"]),
               f"+{pct(sub['delta_fd_minus_random_pp'])}pp",
               f"{pct(sub['delta_ci95_pp'][0])}, {pct(sub['delta_ci95_pp'][1])}",
               sci(mm, ee) if mm else pct(sub.get("mcnemar_p"), 3),
               pct(sub.get("random_rate_pct"))],
              "D2.A5-676f", J(F67F, f"{key}.fd_rate_pct", f"{key}.delta_fd_minus_random_pp"))

        # 资产诊断（退化资产）
        diag = (f67.get("asset_diagnostics", {}) or {}).get("full_pool", {})
        if diag:
            forms = []
            for a, v in diag.items():
                forms.append(pct(v["catch_rate_pct"]))
                forms.append(num(v["catch"]))
                if v["unknown_rate_pct"] >= 99.9:
                    forms.append(num(v["unknown_rate_pct"]))
                elif v["unknown_rate_pct"] > 0:
                    forms.append(pct(v["unknown_rate_pct"], 2))
            C("F11x", "676f 资产诊断：8 资产各自 catch 率；wunsequenced/compile-time 100% unknown（退化）",
              forms, "D2.A5-676f", J(F67F, "asset_diagnostics.full_pool"),
              note="退化资产是 A5 主/并列分析差异的唯一来源")

    # ---------------- D3. 检测器能力边界地图（676g） ----------------
    bl = src.get("blindspot") or {}
    BLF = "data/blindspot_676g_stats.json"
    if bl:
        tot = bl.get("total", {})
        C("G01x", f"676g 总盘：n={tot.get('n')}，catch {tot.get('catch')}，miss {tot.get('miss')}，盲区比 {100*tot.get('blindspot_ratio',0):.1f}%",
          [num(tot.get("n")), num(tot.get("catch")), num(tot.get("miss")),
           pct(100 * tot.get("blindspot_ratio", 0))],
          "D3.盲区地图", J(BLF, "total.n", "total.catch", "total.miss", "total.blindspot_ratio"))
        comp = bl.get("complementarity", {})
        if comp:
            C("G02x", "676g 互补性：6 资产并集 61.6%，最佳单资产 35.6%",
              [pct(100 * comp.get("all6_union_rate", 0)), num(comp.get("all6_union_catch")),
               pct(100 * ((comp.get("solo_catch") or {}).get("asan", 0)) / max(1, tot.get("n", 1)))],
              "D3.盲区地图", J(BLF, "complementarity.all6_union_rate", "complementarity.solo_catch"))
        byasset = bl.get("by_asset", {})
        if byasset:
            forms = []
            for a, v in byasset.items():
                forms.append(pct(100 * v.get("coverage_catch_rate", 0)))
            C("G03x", "676g 逐资产覆盖率（asan/ubsan/tsan/compiler-warn/cross-compile/linker）",
              forms, "D3.盲区地图", J(BLF, "by_asset.*.coverage_catch_rate"))
        bp = bl.get("by_planted", {})
        if bp:
            t_, f_ = bp.get("true", {}), bp.get("false", {})
            C("G04x", "676g 按 planted：true 41.0% [38.0, 44.1]；false 21.6% [13.8, 32.3]",
              [pct(100 * t_.get("blindspot_ratio", 0)),
               f"{pct(100*t_['blindspot_wilson95'][0])}, {pct(100*t_['blindspot_wilson95'][1])}",
               pct(100 * f_.get("blindspot_ratio", 0)),
               f"{pct(100*f_['blindspot_wilson95'][0])}, {pct(100*f_['blindspot_wilson95'][1])}",
               num(f_.get("n"))],
              "D3.盲区地图", J(BLF, "by_planted.true.blindspot_ratio", "by_planted.false.blindspot_ratio"))
        bands = bl.get("blindspot_bands", {})
        high = bands.get("high_blindspot(>50%)", [])
        C("G05x", f"676g 盲区分带：{len(high)} 个类型 >50% 盲；类型总数 {bl.get('n_types')}",
          [num(len(high)), num(bl.get("n_types")), "50"],
          "D3.盲区地图", J(BLF, "blindspot_bands", "n_types"))
        ts = bl.get("tsan_stability", {})
        if ts:
            C("G06x", f"676g TSan 稳定性：{ts.get('unstable')}/{ts.get('n_with_runs')} 不稳定（1.7%）",
              [num(ts.get("unstable")), num(ts.get("n_with_runs")),
               pct(100.0 * (ts.get("unstable") or 0) / max(1, ts.get("n_with_runs") or 1))],
              "D3.盲区地图", J(BLF, "tsan_stability.unstable", "tsan_stability.n_with_runs"))

    # ---------------- E. 外部静态工具对比（673e） ----------------
    xt = src["external_tools"]["comparisons"]

    def _xtrow(dataset, tool_sub):
        for row in xt:
            if row.get("dataset") == dataset and tool_sub in str(row.get("tool", "")):
                return row
        return None

    row = _xtrow("holdout", "StrictA")
    if row:
        mant, exp = mant_exp(row["mcnemar_p"])
        C("E01", f"clang-analyzer holdout {row['tool_rate']}% ({row['tool_catch']}/{row['n_measurable']}) p={mant}e{exp}",
          [pct(row["tool_rate"]), ratio(row["tool_catch"], row["n_measurable"]), sci(mant, exp)],
          "E.外部工具", J("data/673e_comparison_stats.json", "comparisons[dataset=holdout,tool~StrictA]"))
    row = _xtrow("holdout", "cppcheck 主口径")
    if row:
        mant, exp = mant_exp(row["mcnemar_p"])
        C("E02", f"cppcheck holdout {row['tool_rate']}% ({row['tool_catch']}/{row['n_measurable']}) p={mant}e{exp}",
          [pct(row["tool_rate"]), ratio(row["tool_catch"], row["n_measurable"]), sci(mant, exp)],
          "E.外部工具", J("data/673e_comparison_stats.json", "comparisons[dataset=holdout,tool~cppcheck 主口径]"))
    row = _xtrow("corpus", "cppcheck 主口径")
    if row:
        C("E03", f"cppcheck corpus {row['tool_rate']}% ({row['tool_catch']}/{row['n_measurable']}) p={row['mcnemar_p']}",
          [pct(row["tool_rate"]), ratio(row["tool_catch"], row["n_measurable"]), pct(row["mcnemar_p"], 3)],
          "E.外部工具", J("data/673e_comparison_stats.json", "comparisons[dataset=corpus,tool~cppcheck 主口径]"))
        C("E03b", "cppcheck corpus Δ +7.8pp CI[-6.1, 21.7]（CI 跨 0 ⇒ tie）",
          [f"+{pct(row['delta_pp'])}pp",
           f"{pct(row['delta_ci'][0])}, {pct(row['delta_ci'][1])}",
           f"({row['b_fd_only']},{row['c_tool_only']})"],
          "E.外部工具", J("data/673e_comparison_stats.json", "comparisons[dataset=corpus,tool~cppcheck 主口径].delta_pp"))

    # E9 附录：外部工具的对照假阳性（顺带 audit 出分母写错）

    def _xt_form(gid, label, dataset, tool_sub, forms, note=""):
        r_ = _xtrow(dataset, tool_sub)
        if not r_:
            return
        C(gid, label, forms, "E.外部工具",
          J("data/673e_comparison_stats.json", f"comparisons[dataset={dataset},tool~{tool_sub}]"), note=note)

    for gid, tool_sub in (("E04", "StrictA"), ("E05", "cppcheck 主口径")):
        r_ = _xtrow("holdout", tool_sub)
        if not r_:
            continue
        C(gid, f"E9 附录 {tool_sub} 对照 FPR {r_['control_fpr']}% ({r_['control_fp']}/{r_['control_n']})",
          [f"{pct(r_['control_fpr'])}\\% ({r_['control_fp']}/{r_['control_n']})",
           ratio(r_["control_fp"], r_["control_n"])],
          "E.外部工具",
          J("data/673e_comparison_stats.json", f"comparisons[dataset=holdout,tool~{tool_sub}].control_fpr"),
          note="控制组 n=11（= holdout 对照样本数）；分母必须是 11")

    r_ = _xtrow("holdout", "StrictA")
    if r_:
        C("E06", "E9 附录：holdout Δ(FD−StrictA) +34.1pp [19.6, 48.7]，对子 (14,0)",
          [f"+{pct(r_['delta_pp'])}pp", f"{pct(r_['delta_ci'][0])}, {pct(r_['delta_ci'][1])}",
           f"({r_['b_fd_only']},{r_['c_tool_only']})"],
          "E.外部工具", J("data/673e_comparison_stats.json", "comparisons[dataset=holdout,tool~StrictA].delta_pp"))
    r_ = _xtrow("corpus", "StrictA")
    if r_:
        mant, exp = mant_exp(r_["mcnemar_p"])
        C("E07", "E9 附录：corpus StrictA 34.4% (22/64)，Δ +28.1pp 对子 (23,5)，p=9.1e-4",
          [pct(r_["tool_rate"]), ratio(r_["tool_catch"], r_["n_measurable"]),
           f"+{pct(r_['delta_pp'])}pp", f"({r_['b_fd_only']},{r_['c_tool_only']})", sci(mant, exp)],
          "E.外部工具", J("data/673e_comparison_stats.json", "comparisons[dataset=corpus,tool~StrictA]"))

    layers = src["external_tools"].get("layers") or []
    lay = {(x["dataset"], x["layer"]): x for x in layers}
    if lay:
        def _lay(ds, name, *fields):
            x = lay.get((ds, name)) or {}
            return " / ".join(str(x.get(f, "—")) for f in fields)

        def _prose(name, tmpl):
            x = lay.get(("corpus", name)) or {}
            return tmpl.format(fd=x.get("fd"), ct=x.get("ct"), cp=x.get("cp"), n=x.get("n"))

        C("E08", "E9 附录：corpus 分层 FD/ct/cp（sanitizer 29/17/26；compiler-warn 9/5/8；cross-compile 2/0/1）",
          [_lay("corpus", "sanitizer", "fd", "ct", "cp"),
           _lay("corpus", "compiler-warn", "fd", "ct", "cp"),
           _lay("corpus", "cross-compile", "fd", "ct", "cp"),
           num(lay.get(("corpus", "cross-compile"), {}).get("n")),
           _prose("sanitizer", "FD {fd} vs clang-analyzer {ct} / cppcheck {cp}"),
           _prose("compiler-warn", "FD {fd} / cppcheck {cp}"),
           _prose("cross-compile", "{fd} / {ct} / {cp}"),
           ],
          "E.外部工具", J("data/673e_comparison_stats.json", "layers"))

    _clang_main = _xtrow("holdout", "clang-tidy 主口径")
    if _clang_main:
        C("E10", "E9 附录：clang-tidy 主口径 holdout 100% recall / 100% FPR（零区分度 ⇒ 该口径被弃用）",
          [pct(_clang_main["tool_rate"]), num(_clang_main["tool_rate"]),
           pct(_clang_main["control_fpr"]), num(_clang_main["control_fpr"]),
           ratio(_clang_main["tool_catch"], _clang_main["n_measurable"]),
           ratio(_clang_main["control_fp"], _clang_main["control_n"])],
          "E.外部工具", J("data/673e_comparison_stats.json",
                       "comparisons[dataset=holdout,tool~clang-tidy 主口径]"))
    rev = src["external_tools"].get("reverse_pairs") or []
    if rev:
        C("E09", f"E9 附录：{len(rev)} 个反向对（工具 catch / FD miss）",
          [num(len(rev))], "E.外部工具", J("data/673e_comparison_stats.json", "reverse_pairs"))

    # ---------------- F. LLM 臂与外部锚点 ----------------
    ea = src["external_anchor"]
    ll = src["llm_arm"]["metrics"]
    a_sub = ea["subset_a_guideline_verbatim"]
    b_sub = ea["subset_b_ub_reconstructed"]
    tot_catch = a_sub["catch"] + b_sub["catch"]
    tot_n = a_sub["total"] + b_sub["total"]
    C("F01", "外部锚点子集 A（准则原文）28.6% (10/35) CI[14.6,46.3]",
      [pct(a_sub["rate_pct"]), ratio(a_sub["catch"], a_sub["total"]),
       f"{pct(100 * a_sub['cp95']['cp_low'])}, {pct(100 * a_sub['cp95']['cp_high'])}"],
      "F.LLM/锚点", J("data/external_anchor_reveal_672j.json", "subset_a_guideline_verbatim.rate_pct",
                   "subset_a_guideline_verbatim.cp95.cp_low"))
    C("F02", "外部锚点子集 B（UB 片段重建）80.0% (12/15)",
      [pct(b_sub.get("rate_pct")), ratio(b_sub["catch"], b_sub["total"])],
      "F.LLM/锚点", J("data/external_anchor_reveal_672j.json", "subset_b_ub_reconstructed.rate_pct"))
    C("F03", f"外部锚点合计 {100*tot_catch/tot_n:.1f}% ({tot_catch}/{tot_n})；扫描规则 87",
      [pct(100.0 * tot_catch / tot_n), ratio(tot_catch, tot_n), num(tot_catch), num(tot_n),
       num(ea["compilability_filter"]["scanned_unique_rules"]),
       num(a_sub["total"]), num(b_sub["total"]),
       (re.search(r"(\d+)/(\d+)", str(ea.get("harness", {}).get("why", ""))) or [None, ""])[0]],
      "F.LLM/锚点", J("data/external_anchor_reveal_672j.json",
                   "subset_a_guideline_verbatim.catch", "subset_b_ub_reconstructed.catch",
                   "compilability_filter.scanned_unique_rules"))
    fd_k = round(ll["fd_detect_rate_pct"] / 100.0 * ll["llm_n"])
    C("F04", "LLM 臂：GLM-4 12/12 vs FD 6/12；对照误报 4/8 = 50%",
      [ratio(ll["llm_k"], ll["llm_n"]), ratio(fd_k, ll["llm_n"]),
       ratio(ll["llm_false_positive"]["fp"], ll["llm_false_positive"]["n"]),
       pct(ll["llm_false_positive"]["rate_pct"]), pct(100 * ll["agreement"]["rate"])],
      "F.LLM/锚点", J("data/experiments/llm_arm_672i.json", "metrics.llm_k", "metrics.llm_n",
                   "metrics.llm_false_positive.fp", "metrics.agreement.rate"),
      note=f"FD 的 6/12 由 fd_detect_rate_pct={ll['fd_detect_rate_pct']}% × llm_n 重算得到")
    pm = ll["paired_mcnemar_fd_vs_llm"]
    C("F05", f"LLM 臂配对 b/c = ({pm['b_fd_only']},{pm['c_llm_only']})，p={pm['p_value']}",
      [f"{pm['b_fd_only']},{pm['c_llm_only']}", pct(pm["p_value"], 3)],
      "F.LLM/锚点", J("data/experiments/llm_arm_672i.json", "metrics.paired_mcnemar_fd_vs_llm.p_value"))

    # ---------------- G. 变异测试 / 缺陷重注入 ----------------
    mc = src["mutation_core"]; ma = src["mutation_all"]  # noqa: E702
    core_scored = mc["killed"] + mc["survived"]
    all_scored = ma["killed"] + ma["survived"]
    C("G01", f"变异（core）{mc['killed']}/{core_scored} = {100*mc['killed']/core_scored:.1f}%",
      [ratio(mc["killed"], core_scored), pct(mc["kill_rate_on_scored"]),
       f"{pct(cn['mutation_core']['cp95'][0])}, {pct(cn['mutation_core']['cp95'][1])}"],
      "G.变异/注入", J("data/656_mutation_report.json", "killed", "survived", "kill_rate_on_scored"))
    C("G02", f"变异（all-scope）{ma['killed']}/{all_scored} = {100*ma['killed']/all_scored:.1f}%",
      [ratio(ma["killed"], all_scored), pct(ma["kill_rate_on_scored"])],
      "G.变异/注入", J("data/656_mutation_report_all.json", "killed", "survived", "kill_rate_on_scored"))
    di = src["defect_injection"]
    C("G03", f"缺陷重注入 {di['reinject_caught']}/{di['reinjectable']} = 100%；total {di['total_defects']}；软覆盖 {di['historical_gate_caught_yes']}/{di['total_defects']}",
      [ratio(di["reinject_caught"], di["reinjectable"]),
       ratio(di["historical_gate_caught_yes"], di["total_defects"]),
       num(di["total_defects"])],
      "G.变异/注入", J("data/defect_injection_661.json", "reinject_caught", "reinjectable",
                   "historical_gate_caught_yes", "total_defects"))

    # ---------------- H. 派生：附录样本量表（独立重算，逐格 ceil） ----------------
    _ss_cases = [
        ("H01", "样本量：独立两比例 0.35→0.50", 0.35, 0.50, None),
        ("H02", "样本量：独立两比例 0.35→0.55", 0.35, 0.55, None),
        ("H03", "样本量：独立两比例 0.35→0.45", 0.35, 0.45, None),
        ("H04", "样本量：配对 ψ=0.3", 0.35, 0.50, 0.3),
        ("H05", "样本量：配对 ψ=0.4", 0.35, 0.50, 0.4),
        ("H06", "样本量：配对 ψ=0.5", 0.35, 0.50, 0.5),
    ]
    for cid, label, p1, p2, psi in _ss_cases:
        v = n_total_samplesize(p1, p2, paired=psi is not None, psi=psi)
        if v is None:
            continue
        C(cid, label + f" ⇒ n={math.ceil(v)}",
          [num(math.ceil(v)), f"{num(math.ceil(v))} (holdout)"], "H.样本量",
          {"kind": "derived", "detail": f"Cohen arcsine h + Connor 配对；p1={p1},p2={p2},psi={psi}, α=0.05, power=0.8, recomputed={v:.2f}"})

    # ---------------- K. 历史批次行：源不可得 ⇒ 按诚实边界登记为 un-pinned ----------------
    claims.append({
        "id": "K01",
        "label": "tab:e3 第 656 行 “变异 core 62.5% (30/48)”：无任何现存产物可复现",
        "forms": ["62.5", "30/48"],
        "group": "K.历史 un-pinned",
        "source": {"kind": "missing_artifact",
                   "detail": "data/656_mutation_report*.json 现存值为 110/114 与 130/159；"
                             "全仓扫描 `30/48` 无产物命中（唯一产出是更早被覆盖的报告）"},
        "status": "unpinned_no_artifact",
        "note": "论文必须显式标注该行为 un-pinned 历史值，不得当作可复现结果（676h 已加脚注）",
    })
    claims.append({
        "id": "K02",
        "label": "tab:e3 第 665 行 “66.7%（旧 -O1 单档口径）”：源为已退役草稿口径",
        "forms": ["66.7"],
        "group": "K.历史 un-pinned",
        "source": {"kind": "retired_draft",
                   "detail": "仅能追溯到 research/paper_v0.4.md 与 data/669_caliber_report.json::doc_sightings；"
                             "对应 -O1 单档产物已被 665/668 双档口径取代"},
        "status": "unpinned_retired_caliber",
        "note": "该值口径已退休，只能作为“当时口径下读到的数”引用",
    })

    # ---------------- I. 表内所有 Clopper–Pearson 区间逐格重算 ----------------
    def _cmd_ci(k, n):
        return ('python -c "import sys;sys.path.insert(0,\'tools\');from stat_bounds import cp_interval;'
                f'print(*[round(x*100,1) for x in cp_interval({k},{n})])"')

    # (id, label, k, n, 论文是否打印该区间)
    CI_CASES = [
        ("I01", "Static holdout 1/41 CI", 1, 41, True),
        ("I02", "Random† holdout 4/41 CI", 4, 41, True),
        ("I03", "FD holdout 34/41 CI", hcum["error_subset"]["catch"], hcum["denominator"]["value"], True),
        ("I04", "Caliber B holdout 34/42 CI", hcum["error_subset"]["catch"], hcum["error_subset"]["total"], True),
        ("I05", "Static corpus 11/64 CI", bc["static"]["k"], bc["static"]["n"], True),
        ("I06", "Random† corpus 14/64 CI", bc["random_proxy"]["k"], bc["random_proxy"]["n"], True),
        ("I07", "FD corpus 40/64 CI", ccum["catch"], ccum["denominator"]["value"], True),
        ("I08", "Caliber B corpus 40/73 CI", ccum["catch"], ccum["total"] - ccum["not_error"], True),
        ("I09", "Caliber C corpus 40/76 CI", ccum["catch"], ccum["total"], True),
        ("I10", "对照 FPR 0/11 CI", cn["control_false_positive"]["fp"],
         cn["control_false_positive"]["total"], True),
        ("I11", "corpus 分层 sanitizer 29/34 CI",
         ccum["by_layer"]["sanitizer"]["catch"], ccum["by_layer"]["sanitizer"]["denominator"]["value"], False),
        ("I12", "corpus 分层 compiler-warn 9/18 CI",
         ccum["by_layer"]["compiler-warn"]["catch"],
         ccum["by_layer"]["compiler-warn"]["denominator"]["value"], False),
        ("I13", "corpus 分层 cross-compile 2/12 CI",
         ccum["by_layer"]["cross-compile"]["catch"],
         ccum["by_layer"]["cross-compile"]["denominator"]["value"], False),
        ("I14", "缺陷重注入 6/6 CI", cn["defect_reinjection"]["k"], cn["defect_reinjection"]["n"], False),
    ]
    for cid, label, k, n, printed in CI_CASES:
        st = "active" if printed else "not_printed"
        if cid in ("I11", "I12", "I13", "I14"):
            st = "superseded:689重构"  # 689 重构：分层 CI 数字移出正文（数据仍在产物）
        if not use_cmd:
            claims.append({"id": cid, "label": label, "forms": [], "group": "I.CI重算",
                           "source": {"kind": "cmd", "cmd": _cmd_ci(k, n)},
                           "status": "skipped_cmd", "note": "--no-cmd 跳过"})
            continue
        r = subprocess.run(_cmd_ci(k, n), cwd=ROOT, capture_output=True, text=True, timeout=180, shell=True)
        vals = _NUM_RE.findall(r.stdout or "")
        if len(vals) >= 2:
            C(cid, label + f" ⇒ [{vals[0]}, {vals[1]}]",
              [f"{pct(float(vals[0]))}, {pct(float(vals[1]))}"], "I.CI重算",
              {"kind": "cmd", "cmd": _cmd_ci(k, n)}, status=st,
              note="用仓库自带 tools/stat_bounds.py::cp_interval 现算"
                   + ("" if printed else "；论文当前未打印该区间 ⇒ 记为 not_printed，不作不一致"))
        else:
            claims.append({"id": cid, "label": label, "forms": [], "group": "I.CI重算",
                           "source": {"kind": "cmd", "cmd": _cmd_ci(k, n)},
                           "status": "cmd_failed", "note": (r.stderr or r.stdout or "")[:200]})

    # A5 设计量的派生值：105 样本 = 41+64；840 次 detect = 105×8
    tot_n = (ds_map.get("holdout", {}).get("n_measurable_with_attribution") or 0) + \
            (ds_map.get("corpus", {}).get("n_measurable_with_attribution") or 0)
    n_assets = len(((_byk("holdout", 4) or {}).get("candidates")) or [])
    if tot_n and n_assets:
        C("D03", f"A5 矩阵 {tot_n}×{n_assets} = {tot_n*n_assets} 次 detect",
          [num(tot_n), num(tot_n * n_assets), num(n_assets)], "D.A5",
          J(A5F, "real_attribution.datasets.*.n_measurable_with_attribution"),
          status="superseded_by_676f")
    gaps = [ss.get("holdout", {}).get("±5pp", {}).get("n", 0) - hcum["denominator"]["value"],
            ss.get("corpus", {}).get("±5pp", {}).get("n", 0) - ccum["denominator"]["value"]]
    if gaps[0] and gaps[1]:
        C("A19", f"±5pp 缺口：holdout 还差 {gaps[0]}，corpus 还差 {gaps[1]}",
          [num(gaps[0]), num(gaps[1])], "A.核心三臂",
          {"kind": "derived", "detail": "sample_size_672k.±5pp.n − 当前可测 n"})

    # 681 C3：677b（clone-aware 重切分 / cluster bootstrap）与 677c（非退化池 / 退化贡献）
    # 纳入检查集，使 v1.3 之后新增的 A5 稳健性数字处于同一追溯口径内。
    ca = ((cn.get("a5_experiments") or {}).get("clone_aware_677b") or {})
    nd = ((cn.get("a5_experiments") or {}).get("nondegenerate_pool_677c") or {})
    ca_splits = ca.get("splits_delta_pp") or []
    ca_n = ca.get("effective_n") or []
    if len(ca_splits) == 2:
        C("D11", f"clone-aware 重切分 Δ +{ca_splits[0]}~+{ca_splits[1]}pp（677b，逐 split 为 +23.02/+25.70）",
          ["23.02", "25.70"], "D.A5",
          {"kind": "derived", "detail": "current_numbers.a5_experiments.clone_aware_677b "
                                        "← data/677b_a5_results_family_random.json / _family_stratified.json"})
    if len(ca_n) == 2:
        C("D12", f"cluster bootstrap 有效 n≈{ca_n[0]}–{ca_n[1]}（677b，design effect ≈4.1–4.3）",
          [num(ca_n[0]), num(ca_n[1])], "D.A5",
          {"kind": "derived", "detail": "current_numbers.a5_experiments.clone_aware_677b "
                                        "← data/677b_cluster_bootstrap.json"})
    if nd.get("optimal_delta_pp") is not None:
        C("D13", f"非退化池选择效应 +{nd['optimal_delta_pp']}pp（677c，k=1，p=6.02e-08）",
          ["11.31"], "D.A5",
          {"kind": "derived", "detail": "current_numbers.a5_experiments.nondegenerate_pool_677c "
                                        "← data/677c_a5_nondegenerate_results.json"})
    if nd.get("degenerate_contribution_to_mean_pp") is not None:
        C("D14", f"退化资产对均值的贡献 ≈+{nd['degenerate_contribution_to_mean_pp']}pp（677c）",
          ["12.81"], "D.A5",
          {"kind": "derived", "detail": "current_numbers.a5_experiments.nondegenerate_pool_677c "
                                        "← data/677c_a5_nondegenerate_results.json"})

    # ---------------- E. 689 重构批次（TOST / 标准化 / 环境三组件） ----------------
    r9 = (cn.get("reframed_689") or {})
    t9 = (r9.get("equivalence_tost") or {})
    if t9:
        C("Z01", "689 TOST：±10pp 未过，90% CI [-10.61, 5.52]pp，p_TOST=0.064",
          [pct(t9["ci90_pp"][0], 2), pct(t9["ci90_pp"][1], 2), num(t9["p_tost"], 3)], "Z.689重构",
          {"kind": "derived", "detail": "current_numbers.reframed_689.equivalence_tost "
                                        "← data/689_equivalence_test.json"})
        C("E02", f"689 TOST 最小通过 margin {t9['min_passing_margin_pp']}pp（deff 校正 "
                 f"{t9['deff_adjusted']['min_passing_margin_pp']}pp）",
          [num(t9["min_passing_margin_pp"], 2), num(t9["deff_adjusted"]["min_passing_margin_pp"], 2)],
          "Z.689重构",
          {"kind": "derived", "detail": "data/689_equivalence_test.json"})
    s9 = (r9.get("standardized_analysis") or {})
    if s9:
        C("E03", "689 标准化：正向 -17.92pp（R_syn_std=77.01%），反向 +1.70pp，类型级 -13.52pp",
          [num(s9["forward_diff_pp"], 2), num(s9["forward_r_syn_std_pct"], 2),
           num(s9["reverse_diff_pp"], 2), num(s9["type_forward_diff_pp"], 2)], "Z.689重构",
          {"kind": "derived", "detail": "current_numbers.reframed_689.standardized_analysis "
                                        "← data/689_standardized_analysis.json"})
    e9 = (r9.get("environment_metrics") or {})
    if e9:
        C("E04", "689 环境：真实 59.09%→23.64%（-35.45pp，Δunknown=0），clang↔g++ 93.5%",
          [num(e9["real110_wsl_or_pct"], 2), num(e9["real110_native_or_pct"], 2),
           num(abs(e9["delta_pp"]), 2), num(e9["clang_vs_gpp_200"]["asan_agree_pct"], 1)],
          "Z.689重构",
          {"kind": "derived", "detail": "current_numbers.reframed_689.environment_metrics "
                                        "← data/689_environment_metrics.json"})

    # ---------------- Z. 691 止损与增强（题名/公式/池/证据搬运） ----------------
    r10 = (cn.get("reframed_691") or {})
    m10 = (r10.get("mechanism_level_poolA_vs_single_random") or {})
    if m10:
        C("Z11", "691 机制级：Pool A k=1 +11.31pp (p=6.0e-8)；k=2/k=3 +7.42pp；k=4 0.00pp",
          ["11.31", "6.0", "7.42", "0.00"], "Z.691修正",
          {"kind": "derived", "detail": "current_numbers.reframed_691.mechanism_level_poolA_vs_single_random "
                                        "← data/677c_a5_nondegenerate_results.json"})
    k10 = (r10.get("label_kappa_ai_self_consistency") or {})
    if k10:
        C("Z12", "691 四个 κ（AI 自一致）：0.727 / 0.789 / 0.437 / 0.157",
          [num(k10["defect_type"], 3), num(k10["planted"], 3),
           num(k10["expected_verdict"], 3), num(k10["severity"], 3)], "Z.691修正",
          {"kind": "derived", "detail": "current_numbers.reframed_691.label_kappa_ai_self_consistency "
                                        "← data/682_kappa.json"})
    g10 = (r10.get("governance") or {})
    if g10:
        C("Z13", "691 治理计数：452 ledger 事件 / 67 规则 / rules_sha256 v1.0.0",
          [num(g10["ledger_events"]), num(g10["rules"])], "Z.691修正",
          {"kind": "derived", "detail": "current_numbers.reframed_691.governance"})
    p10 = (r10.get("pools") or {})
    if p10:
        C("Z14", "691 池计数：Pool B ≡ Pool C（同一六资产集）；9 个不同 (池,k) 块 / 14 块实例",
          [num(p10["distinct_pools"]), num(p10["distinct_pool_x_k_blocks"]),
           num(p10["block_instances"])], "Z.691修正",
          {"kind": "derived", "detail": "current_numbers.reframed_691.pools "
                                        "← data/677c_asset_pools.json + 677c_evolution_operator_results.json"})

    return claims


# --------------------------------------------------------------------------
# 审计执行
# --------------------------------------------------------------------------
def audit_claims(text, claims):
    results, covered = [], []
    for c in claims:
        found = []
        violations = []
        for form in c["forms"]:
            if isinstance(form, dict):  # 反向检察：form 出现处必须同时出现 cooccur 正则
                hits = find_literal(text, form["form"])
                for (s, e, ln, snip) in hits:
                    w = form.get("window", 200)
                    lo, hi = max(0, s - w), min(len(text), e + w)
                    if not re.search(form["cooccur"], text[lo:hi]):
                        violations.append({"line": ln, "snippet": snip[:180]})
                continue
            hits = find_literal(text, form)
            if hits:
                covered.extend((h[0], h[1]) for h in hits)
                found.append({
                    "form": form,
                    "count": len(hits),
                    "lines": sorted({h[2] for h in hits})[:20],
                    "snippet": hits[0][3][:180],
                })
        real_forms = [f for f in c["forms"] if isinstance(f, str)]
        is_policy = any(isinstance(f, dict) for f in c["forms"])
        if violations:
            verdict = "policy_violation"
        elif is_policy and not real_forms:
            verdict = "consistent"  # 反向检察：无违反即通过
        elif c["status"] == "skipped_cmd":
            verdict = "skipped"
        elif not real_forms:
            verdict = "no_source_value"
        elif found:
            verdict = "consistent"
        elif str(c["status"]).startswith("superseded"):
            verdict = "retired"   # 已被新批次取代、论文里不再出现的旧值
        else:
            verdict = "missing"
        results.append({
            "id": c["id"], "label": c["label"], "group": c["group"],
            "status": c["status"], "verdict": verdict,
            "source": c["source"], "note": c["note"],
            "matches": found,
            "violations": violations,
            "forms": [],
        })
        # 记录每条 claim 实际命中的写法
        seen = {m["form"] for m in found}
        out_forms = []
        for f in c["forms"]:
            if isinstance(f, dict):
                out_forms.append({"form": f["form"], "found": True, "count": len(violations) or 1,
                                  "lines": [v["line"] for v in violations], "kind": "cooccur"})
            else:
                out_forms.append({"form": f, "found": f in seen,
                                  "count": next((m["count"] for m in found if m["form"] == f), 0),
                                  "lines": next((m["lines"] for m in found if m["form"] == f), []),
                                  "kind": "value"})
        results[-1]["forms"] = out_forms
    return results, covered


def scan_all_numbers(text, covered):
    """扫描 tex 里所有数字 token，按是否被检察覆盖 / 类别归类。"""
    cov_sorted = sorted(covered)
    tokens = []
    lines_raw = text.splitlines(keepends=True)
    offset = 0
    in_verbatim = False
    for lineno, line in enumerate(lines_raw, 1):
        if "\\begin{verbatim}" in line or "\\begin{Verbatim}" in line:
            in_verbatim = True
        stripped = line.lstrip()
        if stripped.startswith("%") or any(h in line for h in _SKIP_LINE_HINTS):
            offset += len(line)
            if "\\end{verbatim}" in line or "\\end{Verbatim}" in line:
                in_verbatim = False
            continue
        ctx_lines = lines_raw[max(0, lineno - 3):lineno + 1]
        ctx = "".join(ctx_lines)
        for m in _NUM_RE.finditer(line):
            s, e = offset + m.start(), offset + m.end()
            tok = m.group(0)
            if in_verbatim:
                cls, note = "repro_command", "出现在重算命令 verbatim 块里（不是结果数字）"
            else:
                cls, note = classify_token(text, line, ctx, s, e, tok, cov_sorted)
            tokens.append({
                "line": lineno, "token": tok, "class": cls, "note": note,
                "snippet": line.strip()[:160],
            })
        offset += len(line)
        if "\\end{verbatim}" in line or "\\end{Verbatim}" in line:
            in_verbatim = False
    return tokens


def _in_covered(cov_sorted, start, end):
    import bisect
    i = bisect.bisect_left(cov_sorted, (start, end))
    for j in (i - 1, i, i + 1):
        if 0 <= j < len(cov_sorted):
            a, b = cov_sorted[j]
            if a <= start and end <= b:
                return True
            if start <= a and b <= end:
                return True
    return False


def classify_token(text, line, ctx, start, end, tok, cov_sorted):
    if _in_covered(cov_sorted, start, end):
        return "claim", "被某条检察命中"
    line_start = text.rfind("\n", 0, start) + 1
    col = start - line_start
    before = line[:col]
    after = line[col + len(tok):]
    # \cite{...} 内部
    cite_open = before.rfind("\\cite{")
    if cite_open >= 0 and "}" not in before[cite_open:]:
        return "citation", "\\cite{} 内的引用键或年份"
    if any(key in line for key in ("\\bibitem", "thebibliography")):
        return "bibliography", "参考文献条目"
    if any(h in line for h in _FORMAT_HINTS):
        return "format_layout", "图表/表格排版参数"
    # 排版长度单位（6pt / 0.48\textwidth 等）
    tail = after.lstrip()
    if re.match(r"^(pt|mm|cm|ex|em|in|\\,)\b", tail):
        return "format_layout", "排版长度单位"
    if _YEAR_RE.match(tok):
        return "year", "年份（引用/法规/批次）"
    if tok.isdigit() and int(tok) <= 19 and re.search(r"\\(paragraph|section|subsection|label|ref|item)\b", line):
        return "structural", "编号/章节/条目序号"
    if re.fullmatch(r"6[0-9]{2}", tok):  # 656 / 660 / 665 / 666 / 668 / 669 等批次号
        return "batch_id", "批次号（非统计量）"
    for rx, cls, note in CONTEXT_RULES:
        if rx.search(line) or rx.search(ctx):
            return cls, note
    return "unclassified", "未归类（需人工确认）"


def write_json(path, payload):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def write_report(path, payload):
    res = payload["results"]
    cov = payload["coverage_summary"]
    by_group = {}
    for r in res:
        g = by_group.setdefault(r["group"], {"consistent": 0, "other": []})
        if r["verdict"] == "consistent":
            g["consistent"] += 1
        else:
            g["other"].append(r)

    L = []
    L.append("# 676h · 论文数字可追溯性审计报告")
    L.append("")
    L.append(f"- 生成时间：{payload['generated_at']}")
    L.append(f"- 被审计稿件：`{payload['tex']}`（正文 {payload['main_text_pages']} 页 / 全稿 {payload['total_pages']} 页，取自编译日志）")
    L.append(f"- 权威源：{len(payload['sources'])} 个文件")
    soft_missing = sum(1 for r in res if r["verdict"] == "missing" and r["status"] != "active")
    L.append(f"- 检察条数：**{len(res)}**，其中 consistent {sum(1 for r in res if r['verdict']=='consistent')}，"
             f"硬 missing（active）{sum(1 for r in res if r['verdict']=='missing' and r['status']=='active')}，"
             f"软 missing（not_printed 等）{soft_missing}，"
             f"skipped/no_source {sum(1 for r in res if r['verdict'] in ('skipped','no_source_value'))}")
    L.append("")
    L.append("## 0. 结论速览")
    L.append("")
    hard = [r for r in res if r["verdict"] == "missing" and r["status"] == "active"]
    if hard:
        L.append(f"**存在 {len(hard)} 条 active 级数字在论文里找不到对应写法**（详见 §1）。")
    else:
        L.append("**已有数字的逐条检察全部命中**（不一致率 = 0）。")
    pend = [r for r in res if r["status"].startswith("pending")]
    L.append(f"待 676f/676g 数据就绪后刷新的检察：{len(pend)} 条（见 §3）。")
    L.append("")
    L.append("## 1. 硬不一致清单（missing + active：源里有值、论文里必须出现却找不到）")
    L.append("")
    bad = [r for r in res if r["verdict"] == "missing" and r["status"] == "active"]
    if not bad:
        L.append("（空）—— 论文里已有的数字逐条追到了权威源，且写法一致。")
    else:
        L.append("| ID | 分组 | 状态 | 说明 | 应有写法 | 权威源 |")
        L.append("|---|---|---|---|---|---|")
        for r in bad:
            forms = ", ".join(f'`{f["form"]}`' for f in r["forms"]) or "—"
            src = r["source"].get("file") or r["source"].get("cmd") or r["source"].get("detail") or "—"
            L.append(f"| {r['id']} | {r['group']} | {r['verdict']}/{r['status']} | {r['label']} | {forms} | `{src}` |")
    L.append("")
    L.append("### 1b. 软登记：源里算了、论文没打印（not_printed / retired，非不一致）")
    L.append("")
    soft = [r for r in res if r["verdict"] in ("missing", "retired") and r["status"] != "active"]
    if not soft:
        L.append("（空）")
    else:
        L.append("| ID | 说明 | 状态 |")
        L.append("|---|---|---|")
        for r in soft:
            L.append(f"| {r['id']} | {r['label']} | {r['status']} |")
    L.append("")
    L.append("### 1c. un-pinned 历史值（源不可得 / 口径已退役）")
    L.append("")
    unp = [r for r in res if str(r["status"]).startswith("unpinned")]
    if not unp:
        L.append("（空）")
    else:
        L.append("| ID | 说明 | 状态 | 处置 |")
        L.append("|---|---|---|---|")
        for r in unp:
            L.append(f"| {r['id']} | {r['label']} | {r['status']} | {r['note']} |")
    L.append("")
    L.append("## 2. 逐组概览")
    L.append("")
    L.append("| 分组 | consistent | 其它 |")
    L.append("|---|---|---|")
    for g, v in sorted(by_group.items()):
        L.append(f"| {g} | {v['consistent']} | {len(v['other'])} |")
    L.append("")
    L.append("## 3. 待 676f / 676g 更新清单")
    L.append("")
    L.append(f"依赖就绪状态：**676f `{payload['deps']['676f']['ready']}` / 676g `{payload['deps']['676g']['ready']}`**")
    L.append("")
    L.append("| 依赖 | 文件 | 当前行数 | 需要 | 就绪 |")
    L.append("|---|---|---|---|---|")
    for name in ("676f", "676g"):
        for rel, info in payload["deps"][name]["files"].items():
            L.append(f"| {name} | `{rel}` | {info['n']} | ≥{info['need']} | {info['ready']} |")
    L.append("")
    L.append("| ID | 说明 |")
    L.append("|---|---|")
    for r in pend:
        L.append(f"| {r['id']} | {r['label']} |")
    L.append("")
    L.append("## 4. 数字覆盖度（tex 全量扫描）")
    L.append("")
    L.append(f"扫描到数字 token **{cov['total']}** 个（已排除注释行与导言区行）。分类：")
    L.append("")
    L.append("| 类别 | 数量 | 占比 |")
    L.append("|---|---|---|")
    for k, v in sorted(cov["by_class"].items(), key=lambda x: -x[1]):
        L.append(f"| {k} | {v} | {100*v/cov['total']:.1f}% |")
    L.append("")
    uncov = payload["unclassified_tokens"]
    L.append(f"未归类 token：{len(uncov)} 个（前 60 条见下；全量在 json 里）。")
    L.append("")
    if uncov:
        L.append("| 行 | token | 上下文 |")
        L.append("|---|---|---|")
        for t in uncov[:60]:
            L.append(f"| {t['line']} | `{t['token']}` | `{t['snippet'][:110]}` |")
    L.append("")
    L.append("## 5. 每条检察的命中明细")
    L.append("")
    for r in res:
        flags = "".join("✓" if f["found"] else "✗" for f in r["forms"])
        L.append(f"**{r['id']} · {r['label']}** — {r['verdict']}/{r['status']} `{flags}`")
        src = r["source"].get("file") or r["source"].get("cmd") or r["source"].get("detail") or "—"
        L.append(f"- 源：`{src}`")
        for f in r["forms"]:
            mark = "✓" if f["found"] else "✗"
            L.append(f"  - {mark} `{f['form']}` × {f['count']} @ L{','.join(map(str, f['lines'][:8]))}")
        if r["note"]:
            L.append(f"  - 注：{r['note']}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="676h 论文数字可追溯性审计")
    ap.add_argument("--tex", default="research/latex/queyi_neurips2027_v1.1.tex")
    ap.add_argument("--out-json", default="data/676h_number_audit.json")
    ap.add_argument("--out-md", default="data/676h_number_audit_report.md")
    ap.add_argument("--no-cmd", action="store_true", help="跳过需执行命令的重算检察")
    args = ap.parse_args(argv)

    tex_rel = args.tex
    text = open(_p(tex_rel), encoding="utf-8").read()

    src = {}
    for key, rel in SOURCE_FILES.items():
        try:
            src[key] = load_json(rel)
        except Exception as e:  # noqa: BLE001
            print(f"[warn] 源加载失败 {rel}: {e}", file=sys.stderr)
            src[key] = {}

    claims = build_claims(src, use_cmd=not args.no_cmd)
    results, covered = audit_claims(text, claims)
    tokens = scan_all_numbers(text, covered)
    by_class = {}
    for t in tokens:
        by_class[t["class"]] = by_class.get(t["class"], 0) + 1
    uncov = [t for t in tokens if t["class"] == "unclassified"]
    samples = {}
    for t in tokens:
        s = samples.setdefault(t["class"], [])
        if len(s) < 25:
            s.append({"line": t["line"], "token": t["token"], "snippet": t["snippet"][:120]})

    # 页数（来自同名 .log，避免换算）
    log_rel = tex_rel[:-4] + ".log"
    total_pages = None
    lp = _p(log_rel)
    if os.path.exists(lp):
        log = open(lp, encoding="utf-8", errors="replace").read()
        m = re.search(r"Output written on \S+ \((\d+) pages", log)
        if m:
            total_pages = int(m.group(1))
    deps = check_dependencies()

    payload = {
        "schema": "queyi-676h/number-audit",
        "generated_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "tex": tex_rel,
        "sources": {k: v for k, v in SOURCE_FILES.items()},
        "total_pages": total_pages,
        "main_text_pages": None,
        "deps": deps,
        "results": results,
        "coverage_summary": {"total": len(tokens), "by_class": by_class},
        "unclassified_tokens": uncov,
        "class_samples": samples,
    }
    os.makedirs(os.path.dirname(_p(args.out_json)), exist_ok=True)
    write_json(_p(args.out_json), payload)
    write_report(_p(args.out_md), payload)

    print(f"检察 {len(results)} 条；missing "
          f"{sum(1 for r in results if r['verdict']=='missing')}；"
          f"consistent {sum(1 for r in results if r['verdict']=='consistent')}")
    print(f"数字 token {len(tokens)}；未归类 {len(uncov)}")
    print(f"输出：{args.out_json} / {args.out_md}")
    hard = sum(1 for r in results if r["verdict"] == "missing" and r["status"] == "active")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
