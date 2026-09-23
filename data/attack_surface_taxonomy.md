# 629 B1 · 验证器攻击面分类学（v21 Top1）

> 工具：`tools/attack_surface_taxonomy.py`（纯标准库，只读；只输出分类学，不新增探针）
> 规模：**8 层 / 35 个攻击向量**（risk: high 27 · medium 8 · low 0）

## 一、为什么需要「验证器攻击面」（而不是只做 poison drill）

`poison_drill`（A1-A11）攻击的是**知识内容**（假知识、假证据）。但 v21 调研指出：真正的风险在**验证流水线自身**——AISI 2026-07 的结论是「所有受测模型都在某些设定下作弊、每个监控器都有洞」。内容层的探针查不出「验证器读错字段」「指标被 Goodhart 化」「日志可被重放」这类攻击。本分类学把流水线切成 8 段，逐段列攻击向量。

## 二、8 层攻击面模型

| 层 | 名称 | 向量数 | 已有探针 | 高危 |
|---|---|---|---|---|
| L1 | Claim 层（命题本身被构造/篡改/模糊） | 4 | 3 | 4 |
| L2 | Evidence 层（证据伪造、陈旧留痕、artifact hash 不匹配） | 4 | 3 | 3 |
| L3 | Parser 层（证据解析歧义、正则误伤、字段注入） | 4 | 4 | 2 |
| L4 | Rule 层（规则歧义、隐性预处理、regex heuristic 被绕过、执行时序） | 5 | 3 | 3 |
| L5 | Verifier 层（双实现 common-mode failure、独立验证者同源耦合、验证范围缺口） | 4 | 4 | 4 |
| L6 | Metrics 层（Goodhart 漂移、统计口径误用（CP 偷看）、数字漂移） | 4 | 4 | 3 |
| L7 | Human Review 层（批量授权、模板化人审、mirror shortcut、rubber-stamp） | 5 | 4 | 4 |
| L8 | Provenance 层（时间戳操纵、签名投毒、append-only 链断裂、透明日志伪造） | 5 | 4 | 4 |

## 三、攻击向量总表

| 向量 | 名称 | 描述 | risk | 阙疑已有探针 |
|---|---|---|---|---|
| `L1.1` | 命题等价改写 | 语义等价改写让原判据失效（或让新缺陷看起来等价） | high | tools/mutation_fuzz.py（M1-M7 算子） |
| `L1.2` | 命题多义指代 | 命题含模糊指代（「它」「该值」）⇒ 复核者各自解读不同 | high | **无** |
| `L1.3` | 命题范围偷换 | 悄悄扩大/缩小 claim 边界（∀→∃、单核→多核） | high | tools/atom_evidence_replay.py（frontmatter 冻结） |
| `L1.4` | 命题-证据错配 | 换了 claim 但 evidence 未换（或反之）⇒ 证据为别的命题服务 | high | gate_engine: OBSERVATION-LIVENESS（命题级活性锚） |
| `L2.1` | 证据内容漂移 | evidence 文件内容变了但 PCK/引用 hash 未更新 | high | tools/pck_hash_renewal_628.py + PCK 4 层验证 |
| `L2.2` | 悬空引用 | 引用的证据卡/原子卡不存在（删了或改 ID） | high | gate_engine: ATOM-REL-TARGET / EV 引用规则 |
| `L2.3` | 陈旧证据留痕 | 证据过时（上游结论已变）仍被当作有效引用 | medium | **无** |
| `L2.4` | 证据凭空伪造 | 直接造一个「看起来合规」的证据文件（内容为编造） | high | tools/poison_drill.py（伪造类样例） |
| `L3.1` | 解析歧义 | 同一文本有合法 YAML 两种解读 ⇒ 写者与验证者读到不同值 | high | tests/（hypothesis 差分生成器 T3） |
| `L3.2` | 正则误伤 | 合规文本被正则判为违规（假阳性） | medium | tools/autoimmune_probe_629.py（A2 格式微扰探针） |
| `L3.3` | 字段注入 | 字段里塞控制符/超长值/嵌套结构绕过解析 | high | 626 A2（339 控制字符清洗）+ gate YAML 硬化规则 |
| `L3.4` | 解析器特性绕过 | 利用 YAML 特性（锚点/别名/多文档）绕过解析器子集 | medium | gate_engine: EV-FM-YAML-HARDENING（真实 PyYAML 复核） |
| `L4.1` | 规则隐性预处理 | 规则内部先做归一化 ⇒ 绕过条件藏在预处理里（EV-MATRIX 案） | high | 618-620 专项（EV-MATRIX 显式化）+ 619 A 线 |
| `L4.2` | 阈值边界歧义 | 规则用 > 还是 >=、四舍五入方向未定义 ⇒ 边界样本判决不稳定 | medium | **无** |
| `L4.3` | regex heuristic 绕过 | 同义异形表达绕过关键词 heuristic 检测 | high | tools/mutation_fuzz.py（算子族）+ 623-624 高复杂度攻击 |
| `L4.4` | 规则优先级冲突 | 两条规则对同一事实给出相反结论（谁优先未定义） | medium | **无** |
| `L4.5` | 执行时序依赖 | 读方先于写方（验证器读到尚在写入的工件）⇒ 假红/假绿 | high | 622 B2 + .github/workflows/ci.yml（needs: [replay] 强制序） |
| `L5.1` | 双实现 common-mode failure | 两个实现共享同一错误假设 ⇒ 互相验证都过（W2 求解器案） | high | tools/independent_verifier_628.py（朴素重算）+ 627 A1（W2 归一化修复） |
| `L5.2` | 验证者同源耦合 | 验证端 import 被验证代码 ⇒「签发写错=验证也错」（VSA 案） | high | tools/independence_static_check.py（本批 C3 静态证明） |
| `L5.3` | 验证者自身被投毒 | 验证工具本体被改（或工具完整性尺子未覆盖该工具） | high | tools/tool_integrity.py（22 尺子）+ tools/.tool_checksums |
| `L5.4` | 验证范围缺口 | 验证器不查某类断言（规则触达盲区 31/67）⇒ 盲区内任意造假 | high | tools/uncovered_attack_surfaces.py（本批 B3）+ 沙箱触达矩阵 |
| `L6.1` | Goodhart 漂移 | 指标被当成目标优化 ⇒ 数字好看但目标未达（warn 治理案） | high | 616 专项（warn 治理 + Goodhart 登记） |
| `L6.2` | 连续偷看（CP） | 序贯决策里反复看置信序列 ⇒ 置信度失效 | high | 616 A 线（e-process 修正） |
| `L6.3` | 统计口径误用 | 分母/口径偷换（如把已授权当独立人审、把 warn 当质量评级） | high | 629 A1（自身免疫率口径分桶） |
| `L6.4` | 数字漂移 | 报告数字与实测不符（快照过期/手工录入） | medium | tools/baseline_629.py（B 线基线台账 + 差异标注） |
| `L7.1` | 批量授权 | 一次性授权大量条目（388 条批量授权案）⇒ 人审名存实亡 | high | 626 A3（review_method 五级 + decision_origin 四级） |
| `L7.2` | 模板化人审 | 理由复制粘贴 ⇒ 逐条审查退化为形式 | high | tools/blind_review_backfill_627.py（validate 语境） |
| `L7.3` | mirror shortcut | 把镜像/派生结论当独立证据（194 镜像边案） | high | 628 A3（76 自动证明 + 118 sidecar 待治理） |
| `L7.4` | rubber-stamp | 人审者不读即签（Pass A 展示 AI 推荐会引发自动化偏差） | high | 627 C1（Pass A 盲性严格不泄露既有裁定） |
| `L7.5` | 人审覆盖不足 | 低歧义样本被跳过抽查 ⇒ 漏审集中在「看起来没问题」的卡 | medium | **无** |
| `L8.1` | 时间戳操纵 | decided_at/verified_at 可被改写或不可复现（PE 案） | medium | 611 专项（PE 时间戳口径）+ 626 DecisionEvent （decided_at 冻结） |
| `L8.2` | 签名投毒 | HMAC 密钥泄露/丢失 ⇒ 可伪造凭证或让历史凭证假失败 | high | 628 B2（密钥不入库 + 缺密钥拒绝验证不新建密钥） |
| `L8.3` | append-only 链断裂 | 删改历史日志条目（或重放旧条目） | high | 628 B3（透明日志篡改/删除检测 + 幂等追加） |
| `L8.4` | 透明日志伪造 | 自建替身日志充当「已入册」证据（无外部见证者） | high | **无** |
| `L8.5` | 溯源缺口 | 无法从结论定位到输入哈希/commit/人签（51 旧式 ID 引用案） | high | 627 A2（supersedes ID 重映射）+ 628 B2（输入三重哈希锚定） |

## 四、覆盖概览

- 已有探针覆盖：**29/35** （83%）
- 零覆盖：**6** 个向量（未覆盖清单与优先级见 `data/uncovered_attack_surfaces.md`，B3）
- 覆盖判据：阙疑仓库里存在**针对性探针/工具**（不要求该向量已被成功攻击过；实际历史命中情况见 B2 映射表）。

## 五、与 628 A2（自身免疫）的关系

`L3.2 正则误伤` 属本分类学，628→629 A2 的格式微扰探针正是它的探针：实测 20 次语义等价格式改动零新增 warn ⇒ 该向量目前**未发现**可利用性（不是不存在）。

## 六、局限

- 分类学是**人为划分**（8 层 / 34 向量），层间存在重叠（如 L1.4 与 L2.2 都涉及引用错配）；
- `risk` 是主观分级（依据：是否可绕过全部现有机器检查 + 后果是否静默），未做定量风险评估，**需人审复核**；
- 覆盖标注只说「有探针」，不说「探针有效」——有效性要 B2（历史命中）与 B3（零覆盖）合起来看。
