# 方向 50：大厂在做什么（OpenAI / Anthropic / Google / Meta）

## 核心结论
1. 大厂的精力集中在**"把模型做得更强/更会推理/更会自检"**（能力侧），而非**"做独立可审计的第三方验证"**（信任侧）。这留下了 QueYi 的生态位：大厂做"更强的运动员"，没人做"可信的裁判"。
2. 具体：OpenAI 押推理模型 + 过程奖励；Anthropic 押可解释性 + Constitutional AI + 工具验证；Google 押形式化（AlphaProof）+ Gemini；Meta 押开源 Llama + 自评。**"验证"多为模型内生（tool use / self-critique），非外部审计**。
3. 对双非单人：**不要与它们拼模型**，要拼"独立、便宜、可审计"的细分供给；潜在路径是大厂开源模型 + QueYi 做其评测/审计层（互补而非竞争）。

## 精确数字与案例
- **OpenAI**：o 系列推理模型、process reward models（对推理步骤打分）、code interpreter 自验证；重点是"让模型自己更对"。
- **Anthropic**：Constitutional AI、可解释性（对内部特征）、Claude 的 tool use（可跑代码验证）；强调"可信"但仍是模型自证。
- **Google/DeepMind**：AlphaProof/AlphaGeometry（形式化数学证明，IMO 级）、Gemini 代码；**形式化验证**是最接近"外部验证"的大厂方向。
- **Meta**：Llama 开源、CodeCompose、"Self-Taught Evaluator"（模型自评改模型）；把评测也开源化。
- **共同盲区**：它们**不做"防篡改的第三方审计基准"**（无 append-only 哈希链接管各自模型）——QueYi 正补此。
- **案例**：NeurIPS 2026 披露 E&D track AI 写作污染 10 倍增长（方向 02），但大厂未出"独立检测基准"——公共品缺口。

## 对阙疑的 3 条具体行动
1. **定位"大厂之外的信任层"**：稿件/邮件明确"大厂做能力，QueYi 做独立可审计验证"，占生态位而非对撞。
2. **对接大厂开源生态**：把 QueYi 做成能评 Llama/开源模型的 benchmark（方向 10/48），借大厂模型拉自己存在感。
3. **跟踪 AlphaProof 类形式化**：若大厂把形式化验证推到代码领域，QueYi 需转向"轻量可审计"差异（形式化太贵），或与形式化结合（方向 24）。

## 盲区（诚实标注）
- 大厂动态更新极快，本文件基于 2025–2026 公开信息，非内部情报；2027 需刷新。
- "大厂不做第三方审计"是当前观察，不排除其未来推出（如签名推理日志）——需持续跟踪（方向 47）。
- 我未找到大厂在"C++ 知识验证基准"上的直接产品，可能是我检索盲区。

## 来源
- [1] AI 写作污染（NeurIPS 2026）— 方向 02 来源
- [2] AlphaProof 类形式化 — DeepMind 公开资料
- [3] Self-Taught Evaluator — Meta 公开资料
- [4] 方向 47/48（内置验证/小验证器）
