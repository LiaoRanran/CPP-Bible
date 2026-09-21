# 05 · 论证系统工具链调研（Windows 可用性实测）

> 标注：【一方称】= 源自 564/590 调研，本次未独立安装/核验；本仓规模为判定依据。

## 5.1 clingo / ASP

- 【一方称：564 核实 clingo 5.8.2 有 cp313-win wheel 可装，Windows 可用】。
- grounded 标准 ASP 编码（最小模型语义）：
  ```
  arg(A) :- prop(A).
  attacked(A) :- attacks(B,A), in(B).
  in(A) :- arg(A), not attacked(A).   % 需配 --opt-mode 或势约束求最小模型
  ```
  纯 grounded 用"无攻击者即 IN"的规则 + 最小模型即可；preferred 需 disjunctive 规则或枚举扩展。
- 79 节点规模：clingo 求解在毫秒级（玩具级）。
- **判断**：本仓 grounded 手搓已 <0.5ms，**clingo 对 grounded 是 overkill**；仅当上 preferred/stable/加权 AF 时才有必要。

## 5.2 Tweety（Java 论证框架库）

- 跨平台 JVM，Windows 直接可用；API 支持 grounded/preferred/stable/semi-stable。
- 优点：成熟、文档全；缺点：Java 依赖、与本仓 Python 工具链割裂。

## 5.3 ConArg（约束编程求解器）

- 基于 CP，支持 AF 各种语义枚举；Windows 有原生二进制。适合"枚举所有 preferred 扩展"。

## 5.4 ArgTools / Dung-O-Matic

- 老旧（Java/SWI-Prolog），维护停滞；仅作兼容性参考，不推荐新项目。

## 5.5 Netica / GeNIe（贝叶斯网络）

- 与**加权 AF** 关系紧密：攻击强度/证据置信度可用 BN 表达（维度 9）。本仓若走加权 AF（维度 3 论证需要），BN 工具可承载"权重建模"，但本身是概率推理而非论证求解，二者互补非替代。

## 5.6 关键判断：本仓该用哪个？

| 需求 | 推荐 | 理由 |
|---|---|---|
| 仅 grounded（当前可用） | **手搓纯标准库**（已做） | 微秒级，零依赖，符合"只读/轻量"纪律 |
| 未来 preferred/stable 枚举 | clingo（已核实可装） | ASP 编码标准、Windows OK、规模无痛 |
| 加权 AF | 手搓 + 可选 BN 工具 | 权重来源是本仓自有字段（verified/machine_verified），无需外部引擎 |

**可判定选择标准**：① 规模 < 10⁴ 节点 ⇒ 手搓足够；② 只需 grounded ⇒ 不装任何引擎；③ 需要 non-grounded 语义或加权 ⇒ clingo 首选。
