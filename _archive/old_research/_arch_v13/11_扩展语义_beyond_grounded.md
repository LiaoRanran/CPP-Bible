# 11 · 论证框架的扩展语义（beyond grounded）

> 外部实证【一方称：ARGUS UAI 2026 复杂度、ICCMA 求解器竞赛，待核验】。

## 11.1 语义谱系与复杂度

| 语义 | 复杂度 | 本仓 79 节点可行性 |
|---|---|---|
| grounded | P（已证 <0.5ms） | ✅ 默认 |
| complete | P（存在性 trivial；枚举指数） | ✅ |
| ideal | P（grounded 超集） | ✅ |
| preferred | NP-完全（存在性） | ⚠️ 枚举可行（clingo 毫秒级，规模小） |
| stable | NP-完全 | ⚠️ 同上；但本仓 symmetric 构造下 stable 可能不存在 |

## 11.2 本仓该用哪个？

- **grounded 已够**：经 W2 加权后 IN=79/OUT=42/UNDEC=0，**非退化**（维度 2 实证）。grounded 是"最保守、唯一 P 类、单调"的语义，契合本仓"机器可核验"需求。
- **preferred/stable 的额外价值**：给出"最大可接受集"、消除 UNDECIDED。但本仓 W2 已使 UNDEC=0，故 preferred 的"消除不确定"收益在本仓**趋近于零**。
- **ideal**：grounded 超集，可作为"宽松视图"给人审看"还有哪些边界可争"，但非必需。

## 11.3 与加权/概率的组合

- 加权 preferred、概率 grounded 等组合语义存在，但**引入 NP/#P 复杂度**且本仓无对应需求 → 全属 W 段。
- ARGUS UAI 2026【一方称】复杂度结果支撑"grounded P 类"——与 Dung 1995 解析证明一致，但一手实验设定待核验。

## 11.4 本仓落地评估

- **默认只上 grounded（W2 加权）**。preferred/stable 仅在未来出现"需要多扩展对比"或"证据强烈冲突导致 grounded 过小"时才启用，且届时用 clingo（564 已核实 5.8.2 cp313-win 可装）。
- **发布门槛**：grounded 非退化（退化指数 <0.9）即可上线，不依赖 preferred。
