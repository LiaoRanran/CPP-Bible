#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
705-A · 真实缺陷案例深读生成器（只读，不调用 detect()）。

输入（冻结，只读）：
  - data/683_real_world_detection_matrix.json   （110 条真实缺陷的 8 资产判定）
  - data/683_real_world_failure_cases.md        （40 条 miss 深读，含归因/输出/改进）
  - data/683_real_world_success_cases.md        （24 条 catch 深读，含独苗命中）

输出（本批产物）：
  - data/case_studies/<CVE_ID>.md   （案例卡片）
  - data/case_studies/README.md      （按失败模式分组的索引）
  - data/705_case_study_report.md    （汇总报告）

红线：不修改论文正文/bib、不跑 detect、不改动冻结矩阵。本脚本仅读取。
"""
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(REPO, "data")
OUT_DIR = os.path.join(DATA, "case_studies")
os.makedirs(OUT_DIR, exist_ok=True)

MATRIX = os.path.join(DATA, "683_real_world_detection_matrix.json")
FAIL_MD = os.path.join(DATA, "683_real_world_failure_cases.md")
SUCC_MD = os.path.join(DATA, "683_real_world_success_cases.md")

ASSETS = ["asan", "ubsan", "tsan", "compiler-warn", "wunsequenced",
          "cross-compile", "linker", "compile-time"]


def load_matrix():
    with open(MATRIX, encoding="utf-8") as f:
        m = json.load(f)
    idx = {}
    for s in m["samples"]:
        fields = s.get("fields", {})
        sev = ""
        yr = ""
        fm = fields.get("year", "")
        # 形如 "2014 | severity: HIGH | source_type: cve"
        parts = [p.strip() for p in fm.split("|")]
        for p in parts:
            if p.lower().startswith("severity:"):
                sev = p.split(":", 1)[1].strip()
            elif re.match(r"^\d{4}$", p):
                yr = p
        idx[s["rw_id"]] = {
            "rw_id": s["rw_id"],
            "cve": s.get("cve_id", ""),
            "project": s.get("project", ""),
            "defect_type": s.get("defect_type", ""),
            "severity": sev,
            "year": yr,
            "source_url": fields.get("source_url", ""),
            "mechanism": fields.get("mechanism", ""),
            "notes": fields.get("notes", ""),
            "file": s.get("file", ""),
            "per_asset": s.get("per_asset", {}),
        }
    return m, idx


def parse_blocks(md_path):
    """解析 ### Fx. / ### Sx. 块，返回 {rw_id: {...}}。"""
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    blocks = {}
    # 按 '### ' 行切分
    for m in re.finditer(r"^###\s+([FS]\d+)\.\s*(.+)$", text, re.M):
        kind, header = m.group(1), m.group(2)
        # 找该块范围（到下一个 ### 或文件尾）
        start = m.end()
        nxt = re.search(r"^###\s+", text[start:], re.M)
        body = text[start:start + nxt.start()] if nxt else text[start:]
        rw = re.search(r"RW-\d+", header)
        cve = re.search(r"CVE-\d{4}-\d+", header)
        proj = re.search(r"·\s*([^（]+?)\s*（", header)
        dt = re.search(r"（`([^`]+)`）", header)
        verdicts = re.search(r"8 资产判定\**\s*[：:]\s*(.+)", body)
        attr = re.search(r"归因\**\s*[：:]\s*\*\*\s*([a-f])_([^*]+?)\*\*", body)
        out_a = re.search(r"输出摘录\**\s*[（(]([^)）]+)[)）]\**\s*[：:]\s*(.+)", body)
        out_b = re.search(r"([a-z\-]+)\s*输出摘录\**\s*[：:]\s*(.+)", body)
        if out_a:
            out = (out_a.group(1).strip(), out_a.group(2).strip())
        elif out_b:
            out = (out_b.group(1).strip(), out_b.group(2).strip())
        else:
            out = ("", "")
        imp = re.search(r"改进建议\**\s*[：:]\s*(.+)", body)
        rw_id = rw.group(0) if rw else None
        if not rw_id:
            continue
        blocks[rw_id] = {
            "kind": kind,
            "cve": cve.group(0) if cve else "",
            "project": proj.group(1).strip() if proj else "",
            "defect_type": dt.group(1).strip() if dt else "",
            "verdicts_raw": verdicts.group(1).strip() if verdicts else "",
            "attribution": (attr.group(1), attr.group(2).strip()) if attr else ("", ""),
            "output": out,
            "improvement": imp.group(1).strip() if imp else "",
        }
    return blocks


def verdict_from_matrix(sample):
    """返回 (per_asset verdict dict, or_status)。"""
    pa = sample.get("per_asset", {})
    verdicts = {}
    catches = 0
    unknowns = 0
    for a in ASSETS:
        v = pa.get(a, {}).get("verdict", "unknown")
        verdicts[a] = v
        if v == "catch":
            catches += 1
        elif v == "unknown":
            unknowns += 1
    if catches > 0:
        or_status = "catch"
    elif unknowns == len(ASSETS):
        or_status = "unknown"
    else:
        or_status = "miss"
    return verdicts, or_status


# ---- 推理字典（基于 683 归因，诚实注明是"基于冻结数据的推理"）----

SIGNAL = {
    "asan": "内存越界/释放类动作（AddressSanitizer 在真实执行路径上观测堆/栈溢出、double-free、memory leak）",
    "ubsan": "未定义行为事件（如 signed integer overflow 的 runtime error）",
    "tsan": "数据竞争/并发语义（ThreadSanitizer 观测跨线程非同步访问）",
    "cross-compile": "编译器间分歧（g++ 与 clang++ 对同一输入的输出不一致，暴露 UB/ODR 类问题）",
    "compiler-warn": "编译期告警（警告级诊断）",
}

ATTR_TEXT = {
    "a": "检测器能力盲区（逻辑/并发语义）：内存/UB 检测器的可观测量是程序真实执行路径上的内存动作与 UB 事件；本缺陷在内存动作层面没有可观测信号（程序不越界、不竞争、不溢出，只是'做了不该做的事'），属检测范式边界，需性质化测试/状态机建模才能覆盖（683 §2.a）。",
    "c": "检测器配置缺口：UB 子类未启用（如 unsigned-integer-overflow / float-cast-overflow / alignment / strict-aliasing 检查面不足）。这是可修复缺口，但补开关会改变既有 676f/676g 口径，本批口径冻结优先，登记为改进方向（683 §2.c）。",
    "d": "真实与自造的本质差异：真实缺陷的跨模块/长生命周期形态与单 TU 重构不同，检测链观测口径存在差异；重构保真度损失的方向不可先验判定（683 §2.d）。",
    "f": "不可复现/超时观测：挂起类样本（无限循环、永久等待、自死锁）观测为'运行超时→无报告→miss'，是如实测量口径，非检测器缺陷（683 §2.f）。",
    "b": "样本复杂度（多文件/环境依赖）：真实缺陷常以多文件/跨模块形态出现，单 TU 重构导致保真度损失（683 §2.b）。",
}

PAPER_MEANING = {
    "complement": "支撑论文贡献 2（资产互补性与子模增益）：单资产预算下必漏、8 资产 OR 组合才覆盖的案例，是 682 精确 Shapley（asan 贡献最大 +19.53pp）与 684 贪心=最优 ratio 1.0 的微观注脚。",
    "logic": "支撑论文能力边界 Finding：检测器对语义不可观测的逻辑缺陷无能为力，OR 检出率的'低'来自缺陷类型构成（logic_error 族 OR 仅 3.23%），不是工具链退化；呼应 Real-World Validation 附录的诚实边界声明。",
    "config": "支撑论文口径冻结的诚实性：配置缺口导致的 miss 被如实登记为'待补改进'而非掩盖，说明当前 8 资产口径对 UB 子类覆盖不均。",
    "concurrency": "支撑论文并发语义边界：data race 需 tsan + 压力重现（setarch -R 关 ASLR）；单 TU 重构难以复现真实跨模块 race，呼应 692 环境感知结论。",
    "context": "支撑论文生态效度边界：真实跨模块缺陷在单 TU 重构下保真度损失——本批提升了生态效度（项目/年份跨度），但未提升上下文保真度。",
}


def why_text(sample, block, sole_asset, or_status):
    dt = sample["defect_type"]
    if or_status == "catch" and sole_asset:
        sig = SIGNAL.get(sole_asset, "该资产专属的可观测信号")
        return (
            f"本缺陷的可观测信号只有「{sig}」一类；其余 7 个资产不观测该类事件，"
            f"因此在单资产预算下必然漏检，只有在 8 资产 OR 组合预算下才被覆盖。"
            f"这正是资产互补性的直接证据（与 682 精确 Shapley 方向一致：asan 贡献最大 +19.53pp；"
            f"真实靶场 110 条里 27 条为独苗命中，占 catch 的 41.5%）。"
        )
    # 全 miss / unknown
    code, _ = block.get("attribution", ("", ""))
    base = ATTR_TEXT.get(code, ATTR_TEXT["a"])
    if dt == "logic_error":
        meaning_key = "logic"
    elif dt in ("integer_overflow", "type_punning"):
        meaning_key = "config"
    elif dt == "data_race":
        meaning_key = "concurrency"
    else:
        meaning_key = "context"
    return base


def meaning_text(sample, or_status, sole_asset):
    dt = sample["defect_type"]
    if or_status == "catch" and sole_asset:
        return PAPER_MEANING["complement"]
    if dt == "logic_error":
        return PAPER_MEANING["logic"]
    if dt in ("integer_overflow", "type_punning"):
        return PAPER_MEANING["config"]
    if dt == "data_race":
        return PAPER_MEANING["concurrency"]
    return PAPER_MEANING["context"]


# ---- 选择 28 条代表性案例 ----
# 独苗命中（S，全部为 unique-hit，直接证明互补性）22 条 + 全漏（F）6 条
SELECT_S = ["RW-001", "RW-003", "RW-006", "RW-008", "RW-015", "RW-016",
            "RW-019", "RW-020", "RW-027", "RW-029", "RW-032", "RW-034",
            "RW-045", "RW-049", "RW-051", "RW-057", "RW-059", "RW-060",
            "RW-062", "RW-064", "RW-075", "RW-096"]
SELECT_F = ["RW-002", "RW-025", "RW-074", "RW-005", "RW-012", "RW-090"]
SELECTION = [(r, "catch") for r in SELECT_S] + [(r, "miss") for r in SELECT_F]


def card(sample, block, sole_asset, or_status):
    cve = sample["cve"] or block.get("cve", "")
    proj = sample["project"] or block.get("project", "")
    dt = sample["defect_type"] or block.get("defect_type", "")
    sev = sample["severity"] or "数据待补"
    yr = sample["year"] or "数据待补"
    url = sample["source_url"] or "数据待补"
    verdicts, _ = verdict_from_matrix(sample)
    pa_lines = "\n".join(
        f"- {a}: {verdicts[a]}" for a in ASSETS
    )
    # 独苗命中资产
    if or_status == "catch":
        catchers = [a for a in ASSETS if verdicts[a] == "catch"]
        sole = catchers[0] if len(catchers) == 1 else ""
        sole_line = "（独苗命中）" if sole else "（多资产联合命中）"
    else:
        sole = ""
        sole_line = "（8 资产全漏）"
    mech = (sample["mechanism"] or "").strip()
    notes = (sample["notes"] or "").strip()
    defect_what = (mech + (" " + notes if notes else "")).strip() or "数据待补"
    why = why_text(sample, block, sole, or_status)
    meaning = meaning_text(sample, or_status, sole)
    out_asset, out_txt = block.get("output", ("", ""))
    out_block = ""
    if out_txt:
        out_block = f"\n- {out_asset} 输出摘录：{out_txt}\n"
    imp = block.get("improvement", "")
    imp_block = f"\n## 改进方向\n- {imp}\n" if imp else "\n## 改进方向\n- 数据待补\n"
    title = f"{cve}: {proj} {dt} 缺陷{sole_line}"
    md = f"""# {title}

## 基本信息
- 项目：{proj}
- 缺陷类型：{dt}
- 严重度：{sev}
- 年份：{yr}
- 修复 commit：数据待补（见 NVD 来源：{url}）
- RW 编号：{sample['rw_id']}

## 缺陷是什么
{defect_what}

## 检测器表现
- asan: {verdicts['asan']}
- ubsan: {verdicts['ubsan']}
- tsan: {verdicts['tsan']}
- compiler-warn: {verdicts['compiler-warn']}
- wunsequenced: {verdicts['wunsequenced']}
- cross-compile: {verdicts['cross-compile']}
- linker: {verdicts['linker']}
- compile-time: {verdicts['compile-time']}
- OR 检出率：{or_status}{out_block}
## 为什么漏了 / 为什么只有 {sole or 'X'} 能抓到
{why}

## 对论文的意义
{meaning}
{imp_block}
> 来源：基于 683 冻结检测矩阵（data/683_real_world_detection_matrix.json）与 683 失败/成功案例深读（只读，未跑新 detect）。结论为既有数据的推理，非新实验。
"""
    return md


def main():
    m, idx = load_matrix()
    fail_blocks = parse_blocks(FAIL_MD)
    succ_blocks = parse_blocks(SUCC_MD)
    blocks = {}
    blocks.update(fail_blocks)
    blocks.update(succ_blocks)

    written = []
    groups = {}  # defect_type -> list of (cve, rw, or_status)
    for rw_id, or_status in SELECTION:
        sample = idx.get(rw_id)
        block = blocks.get(rw_id)
        if not sample:
            print(f"[skip] {rw_id} 不在矩阵中")
            continue
        if not block:
            print(f"[skip] {rw_id} 无深读块")
            continue
        verdicts, computed = verdict_from_matrix(sample)
        # 以矩阵计算的 OR 为准
        or_status = computed
        sole_asset = ""
        if computed == "catch":
            catchers = [a for a in ASSETS if verdicts[a] == "catch"]
            if len(catchers) == 1:
                sole_asset = catchers[0]
        cve = sample["cve"] or block.get("cve", rw_id)
        md = card(sample, block, sole_asset, computed)
        fname = cve.replace("/", "_") + ".md"
        with open(os.path.join(OUT_DIR, fname), "w", encoding="utf-8") as f:
            f.write(md)
        written.append((rw_id, cve, sample["defect_type"], computed, sole_asset))
        groups.setdefault(sample["defect_type"], []).append(
            (cve, rw_id, computed, sole_asset))

    # README 索引
    readme = ["# 真实缺陷案例深读 · 索引（705-A）", "",
              f"共 {len(written)} 条案例卡片（独苗命中 + 全漏），基于 683 冻结数据只读生成。",
              "", "## 按缺陷类型分组", ""]
    for dt, items in sorted(groups.items(), key=lambda x: -len(x[1])):
        readme.append(f"### {dt}（{len(items)} 条）")
        for cve, rw, st, sole in items:
            tag = f"独苗={sole}" if sole else ("全漏" if st == "miss" else st)
            readme.append(f"- [{cve}]({cve.replace('/', '_')}.md) · {rw} · {tag}")
        readme.append("")
    readme.append("## 一句话摘要（按代表性）")
    readme.append("")
    for rw_id, cve, dt, st, sole in written:
        tag = f"独苗命中({sole})" if sole else ("8资产全漏" if st == "miss" else st)
        readme.append(f"- **{cve}** ({rw_id}, {dt})：{tag}")
    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(readme))

    # 汇总报告
    n_catch = sum(1 for w in written if w[3] == "catch")
    n_miss = sum(1 for w in written if w[3] == "miss")
    report = f"""# 705-A · 真实缺陷案例深读汇总报告

- 生成：只读 683 冻结检测矩阵 + 683 失败/成功案例深读，未跑新 detect()。
- 案例总数：**{len(written)}** 条
  - 独苗命中（unique-hit，单资产 catch 其余 miss）：{sum(1 for w in written if w[4])} 条
  - 8 资产全漏（miss）：{n_miss} 条
  - 多资产联合命中：{n_catch - sum(1 for w in written if w[4])} 条
- 覆盖缺陷类型：{', '.join(sorted(groups.keys()))}

## 选择标准
按任务卡优先级：① 8 资产全漏的（最有故事性）；② 独苗命中的（说明为何只有该检测器能抓）；
③ 跨类型（内存安全/UB/逻辑/并发各选）；④ 高知名度项目（OpenSSL/Linux/FFmpeg/curl/glibc 等）。

## 文件清单
- `data/case_studies/<CVE_ID>.md`（{len(written)} 个）
- `data/case_studies/README.md`

## 诚实边界
- 案例卡片的'为什么漏了'基于 683 归因分类（a/c/d/f）推理，非新实验。
- '修复 commit' 在 683 冻结数据中缺失，统一标'数据待补'（见 NVD 来源链接）。
- '对论文的意义'是素材建议，最终采用权在作者；本批未改论文正文。
"""
    with open(os.path.join(DATA, "705_case_study_report.md"), "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[done] 写入 {len(written)} 张卡片 + README + 报告")


if __name__ == "__main__":
    main()
