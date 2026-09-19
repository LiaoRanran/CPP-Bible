# MIS-CONC-006（misconception）

## 正面

【误解】MIS-CONC-006 compare_exchange 失败后 expected 变量保持不变
触发说法：CAS 失败了我还能用原来的 expected

## 背面

为什么错：compare_exchange_weak/strong 失败时会把**实际值**写入 expected（按引用传参）→ 原值被覆盖
