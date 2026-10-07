# 691 过度声明审计（B5）：逐条定位、原文、修正、理由

- 触发：690 指出"公式不是过度声明（评审错了），真正的过度声明在别处"
- 扫描方式：对 tex 全文按 7 组关键词正则扫描（见文末复算命令），逐条人工判定

---

## 1. 总表（六类）

| # | 类别 | 位置 | 689 原文 | 691 修正 | 理由 |
|---|---|---|---|---|---|
| O1 | **"三池验证"**（真过度声明） | 附录 677c 段 + 算子节 + F5 + 摘要 | "Three pools are pre-registered…"；"Ablation over **3 pools** × k tiers…beats FD in **3/14** tiers"；F5 "selection-identical … in **14/14** pool×k blocks"；摘要 "identical selections in 14/14 tier checks" | "**Two *distinct* pools** (A; B $=$ C, identical six-asset set ⇒ blocks numerically identical)"; "**9 distinct** pool×k blocks"; "**one** distinct improving tier ($k{=}4$, $+1.41$pp, $p{=}0.302$), replicated under three pool labels"; 摘要改 "selection-identical in every tested block; best tier +1.41pp" | `677c_asset_pools.json`：B/C 资产集相同；`677c_evolution_operator_results.json`：B/C 各 k 块数值**逐位相同**（如 k=1 均 fd 33.0389%、Δ 32.3322pp、p=3.4977e-50）。14 块实为 9 个不同配置；"3 个改进档"实为同 1 档被重复计数 |
| O2 | **公式"修正"表述**（记录层错误，非正文数学错误） | 文件头注释 | "**Hard fixes (689):** kd/n -> k*|D|/|A|" | "**Symbol disambiguation (689/691):** …(the original was the exact hypergeometric mean with n = pool size…)"；正文加 "Notation, not correction" + 拟合限度句 | `E[J]=kd/n` 是超几何精确均值（`n`=资产池=8）；原式正确。称"修正"会在记录中植入假错误（与 690-G 独立结论一致） |
| O3 | **演化残留增益** | 摘要 F5 / 附录算子节 | 摘要："over frequency selection (identical selections…)" 可读作"无效果"但未说清"档位只有 1 个" | 明确"one distinct improving tier…not significant"；算子节加 "identity, not similarity" 并标注 9 个不同块 | 避免读者把"3/14"误读为"三次机会里有三次赢" |
| O4 | **合成 ≡ 真实** | §5.4 / 683 附录节 | 683 节旧句曾以 `p=0.60` 承载"无差异" | 689 已改；691 复核：全文**无**"equivalent/no difference"用于合成 vs 真实之处（"equivalence"仅出现在 TOST 语境） | TOST 未过；`p>0.05` 不得暗示等价（红线 12 延续） |
| O5 | **Merkle 过强词** | §2 / tab:claim / T10 | 旧稿有"provenance chain fully auditable" | 现文：**"tamper-evident current-state integrity with partial historical reproducibility"**，并明写 "**not** an immutable log and **not** tamper-proofing"；全文 `immutable/tamper-proof` 仅出现在这句否定式 | 同一方控制工件与根即可重算二者；不得声称不可篡改 |
| O6 | **真实缺陷命名** | §4 / §5.2 / 附录 | "real-world defects"/"real CVE benchmark" | 统一为 **`source-derived reconstruction`**（110 条 = 真实 CVE/issue 的**单文件教学化重构**）；three-value provenance schema；明写 "not naturalistic artifacts" 且 "not usable for real-world defect distributions" | 避免把重构件当原始生产代码（外部效度诚实） |

**另核（未发现残留）**：
- "superiority over a real static detector" —— 全文仅以**否定式**出现（§附录 positioning："not superior ranking"；`app:related`："Not supported: superiority over…"）；
- "`FD beats`" —— 仅用于 **static calibration arm / random proxy arms** 且同批明示二者性质（caliber re-binning / instrument-level proxy）；
- `73.8%` / `1.9pp/rule` —— 0 命中（除变更日志说明句）。

## 2. 与 690 结论的对齐

| 690 判断 | 691 处置 |
|---|---|
| "公式错误指控本身是错的" | ✅ 采纳（O2）：改称符号消歧，**不改数学** |
| "真正该修的是'三池'" | ✅ 采纳（O1）：三池→两池/9 块，并追到 F5 与摘要 |
| "不要为了迎合评审而改错" | ✅ 遵守：本批**没有**任何为迎合评审而引入的数学改动 |
| "Merkle 已在三处声明局限" | ✅ 复核（O5）：边界句已在，691 只把它扩到正文 §2 并保留否定式 |

## 3. 复算命令

```bash
# 过度声明扫描（691 自查）
python -c "import re,pathlib;src=pathlib.Path('research/latex/queyi_neurips2027_v1.1.tex').read_text(encoding='utf-8');[print(p, len(re.findall(p, src))) for p in ['immutable','tamper-proof','3 pools','three pools','3/14','kd/n','superior']]"
# 池等价性（逐位比对）
python -c "import json;d=json.load(open('data/677c_evolution_operator_results.json',encoding='utf-8'));print(d['pools']['B']['assets']==d['pools']['C']['assets'])"
```
