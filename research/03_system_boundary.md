# 03 · 系统边界（System Boundary）

## 系统之内（System Under Study）
- queyi 验证器：gate_engine（结构/符号/账本）、four_state_verdict（边界判决）、
  证据 replay（provenance）、web_logic_check（台账哈希）、dco_check、license_check。
- 其产出的**判决**（pass/fail/unknown）与**边界声明**（provenance / semantic scope）。

## 系统之外（不在研究范围）
- 书的**教学内容质量**本身（teaching quality 是 L1 advisory，不参与红绿）；
- C++ 编译器/标准库的正确性（那是外部 corpus 的源头，不是本系统）；
- 验证器的**实现性能**（AArch64 交叉编译、ASan/UBSan 等属 L1 advisory）；
- 人类作者写卡的主观判断（属 Authority Ledger，不由本实验评）。

## 边界判定准则
凡"验证器能否对自己产出的结论提供独立可验证证据"的，归系统之内；
凡"结论内容本身的对错/优劣"的，归系统之外。
