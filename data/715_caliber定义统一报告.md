# 715 · 任务 1.1：caliber 定义统一报告

- 批次：715 ｜ 任务：Part 1.1 ｜ 日期：2026-10-10
- 修改文件：`research/latex/paper2_measurement_drift.tex`（论文 1 **未改定义**，见 §2）
- 编译验证：`tectonic` 0 error / 0 undefined（论文 2）

---

## 1. 问题（评审/714 指出的硬冲突）

| | 论文 1 | 论文 2 |
|---|---|---|
| 定义 | `$Q=(D,A,E,\Theta,P)$`（`queyi_neurips2027_v1.1.tex` L284） | `$Q(M)=(A,E,\Theta,P)$`，并明写 "**$D$ is not part of it**"（`paper2_measurement_drift.tex` §3.1） |
| 后果 | 同一个符号 $Q$ 指两个元组；审稿人一眼抓到 | 更糟的是**论文 2 自己内部也不一致**：它的 §1（C1 贡献）与 §3.5（A8）两处都写 caliber 签名是 `$(D,A,E,\Theta,P,\lambda)$`，**含 $D$**，与 §3.1 的排除声明直接矛盾 |

即：这不只是"两篇不一致"，而是"同一篇里互相打架"。**715 之前无人发现这一点。**

---

## 2. 选定方案与理由（任务卡要求说明理由）

任务卡给了两个候选：

- 方案 1：论文 2 改为含 $D$，说明 $D$ 在理论分析中取固定值；
- 方案 2：论文 1 改为不含 $D$，说明 $D$ 是输入而非 caliber 组成部分。

**715 采用方案 1（论文 2 改为 $(D,A,E,\Theta,P)$）**，理由三条：

1. **改动面更小且立刻消除内部矛盾**：论文 2 已有两处（C1、A8）写的是含 $D$ 的签名，改 §3.1 一处即可自洽；改论文 1 则需要动正文、附录与 4 处引用，且论文 1 的"claim caliber"语义（$D$ 是**claim 级**义务：跨数据集不可比）本来就是它的方法论要点，不该被削。
2. **语义上 $D$ 属于 caliber 更好防**：一个率换数据集就不可比——这正是 caliber 漂移的一类；把 $D$ 排除在外等于**先验地**把一个漂移轴移出定义域。
3. **两篇共用同一五元组**后，读者可以拿论文 1 的 $D,A,E,\Theta,P$ 逐项去论文 2 找对应定理，反之亦然。

---

## 3. 具体改动（论文 2）

### 3.1 §3.1 Apparatus and caliber（原 L266–267）

**修改前**：

> We call $Q(M)=(A,E,\Theta,P)$ the *caliber*; $D$ is not part of it.

**修改后**：

> We call $Q(M)=(D,A,E,\Theta,P)$ the *caliber*—*the same five-slot tuple the companion paper uses for a claim's caliber*—so that a rate quoted by either paper carries the same coordinates. $D$ *is* a coordinate: a rate is not comparable across sample populations, which is exactly why the companion paper requires it. What is special here is not the definition but the scope of the analysis: every *drift generator* in this paper is applied at fixed $D$ (Section 4), so $D$ drops out of the derivations below and we write $\tau$'s action on $(A,E,\Theta,P)$ only. Dropping a coordinate that is held constant is a modelling convenience, not a definitional exclusion—an earlier draft of this paper did exclude $D$ from $Q$, which contradicted its own companion and is corrected here.

三点设计意图：

1. 明写"与论文 1 同一个五元组"，让审稿人**不必**去比对；
2. 把"为什么下文推导里看不到 $D$"讲清楚（**held constant**，不是 excluded）；
3. **自曝曾错**（"an earlier draft… is corrected here"）——比悄悄改掉更可信，也避免审稿人从旧稿件里发现矛盾。

### 3.2 A8 签名（3 处）

| 位置 | 修改前 | 修改后 |
|---|---|---|
| §3.5 A8 动机 | "the caliber signature $(A,E,\Theta,P)$ has no slot for $\lambda$" | "the caliber signature $(D,A,E,\Theta,P)$ has no slot for the label map $\lambda$" |
| §3.5 A8 注册 | "The signature is $(A,E,\Theta,P)$ and has no slot for it" | "The signature is $(D,A,E,\Theta,P)$ and has no slot for it" |
| 表 `tab:completeness` | "Type III inexpressible in $(A,E,\Theta,P)$" | "Type III inexpressible in $(D,A,E,\Theta,P)$" |

扩展签名 `$(D,A,E,\Theta,P,\lambda)$` 原有 3 处（C1、§3.5 扩展、附录 A8 正式化）**未改**——它们本来就含 $D$，现在与定义一致。

### 3.3 论文 1：**无需改动**

论文 1 的 `$Q=(D,A,E,\Theta,P)$` 是方案 1 的目标态，保持原样。仅在同一批的其它任务里动过符号周围的措辞（如"claim caliber"），**定义本身一字未改**。

---

## 4. 验收核验（可复跑）

```
# 两篇的 caliber 定义
python - <<'PY'
import re
for f in ["research/latex/queyi_neurips2027_v1.1.tex","research/latex/paper2_measurement_drift.tex"]:
    t=open(f,encoding="utf-8").read()
    print(f, "含 (D,A,E,Theta,P) 次数 =", t.count(r"(D,A,E,\Theta,P)"))
    print("   排除声明 'not part of it' =", "not part of it" in t)
PY
```

实测结果：

| 检查项 | 论文 1 | 论文 2 |
|---|---|---|
| 含 `$(D,A,E,\Theta,P)$` | ✅ 定义处 | ✅ 定义处 + A8 三处 |
| 是否仍有"$D$ is not part of it"式排除 | 无 | **已删除** |
| 扩展签名 `$(D,A,E,\Theta,P,\lambda)$` | — | ✅ 3 处，与定义一致 |
| 编译 | 0 error / 0 undefined | 0 error / 0 undefined |

**结论：两篇论文的 caliber 定义完全一致；论文 2 的内部矛盾同时消除。**
